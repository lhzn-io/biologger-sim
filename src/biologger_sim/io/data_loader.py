# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import logging
import warnings
from pathlib import Path
from typing import Any, cast

import numpy as np
import pandas as pd
import pyarrow.feather as feather

from biologger_sim.core.datetime_utils import excel_date_to_datetime_ns
from biologger_sim.core.types import SensorSigns

from .converter import convert_csv_to_feather

SENSOR_CHANNELS = ("int aX", "int aY", "int aZ", "int mX", "int mY", "int mZ")

# The lab's "standard" export (datasets/README.md, ``*-standard.csv``): one column schema for
# every tag model, mapped here onto the MK10 export names the pipeline reads.
STANDARD_COLUMNS = {
    "depth_m": "Depth",
    "temperature_c": "External Temperature",
    "accelX_total_raw": "int aX",
    "accelY_total_raw": "int aY",
    "accelZ_total_raw": "int aZ",
    "magX_raw": "int mX",
    "magY_raw": "int mY",
    "magZ_raw": "int mZ",
}
STANDARD_GRAVITY = 9.80665  # m/s^2 per g


def from_standard_export(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a standard export with the MK10 column names and the accelerometer in m/s^2.

    The standard export keeps each tag's own sensor units: the MK10 reports m/s^2 (a
    magnitude near 9.8 at rest) and the Axy tags report g (near 1). The unit is told apart by
    the median magnitude, and g is scaled to m/s^2, the unit the pipeline's thresholds assume.
    Frames that are not standard exports are returned as is.
    """
    if "accelX_total_raw" not in df.columns or "int aX" in df.columns:
        return df
    out: pd.DataFrame = df.rename(columns=STANDARD_COLUMNS)
    out["DateTimeP"] = pd.to_datetime(out.pop("datetime_utc"), utc=True, format="ISO8601")
    acc = ["int aX", "int aY", "int aZ"]
    a = out[acc].apply(pd.to_numeric, errors="coerce").to_numpy(float)
    magnitude = float(np.nanmedian(np.sqrt((a**2).sum(axis=1))))
    if magnitude < 3.0:
        out[acc] = a * STANDARD_GRAVITY
        logging.getLogger(__name__).info(
            f"Standard export accelerometer in g (median |a| {magnitude:.2f}); scaled to m/s^2"
        )
    return out


def apply_sensor_signs(df: pd.DataFrame, signs: SensorSigns) -> pd.DataFrame:
    """Returns the frame with the accelerometer and magnetometer in the R pipeline's convention.

    With ``SensorSigns.NEGATED``, every accelerometer and magnetometer channel present
    (``int aX`` and so on, quoted or not) is negated; otherwise the frame is returned as is.
    """
    if SensorSigns(signs) is not SensorSigns.NEGATED:
        return df
    out: pd.DataFrame = df.copy()
    for name in SENSOR_CHANNELS:
        for col in (name, f'"{name}"'):
            if col in out.columns:
                out[col] = -pd.to_numeric(out[col], errors="coerce")
    return out


def fit_accel_depth_bias(df: pd.DataFrame, window: str = "2s") -> np.ndarray:
    """Fits an accelerometer offset that grows linearly with depth.

    Returns ``[b0x, b0y, b0z, b1x, b1y, b1z, scale]``: the offset at the surface (m/s^2),
    its change per 100 m of depth and a common scale, chosen so that ``|(a - b0 - b1 d) *
    scale|`` is 1 g on ``window`` means of the record (where the tail beat averages out).
    A robust loss keeps bursts and turns from pulling the fit.
    """
    from scipy.optimize import least_squares

    acc = list(SENSOR_CHANNELS[:3])
    frame = df[[*acc, "Depth"]].apply(pd.to_numeric, errors="coerce")
    frame["Depth"] = frame["Depth"].interpolate(limit_direction="both")
    means = frame.set_index(pd.DatetimeIndex(df["DateTimeP"])).resample(window).mean().dropna()
    a = means[acc].to_numpy(float)
    d = means["Depth"].to_numpy(float) / 100.0

    def residual(p: np.ndarray) -> np.ndarray:
        corrected = (a - p[:3] - np.outer(d, p[3:6])) * p[6]
        out: np.ndarray = np.linalg.norm(corrected, axis=1) - STANDARD_GRAVITY
        return out

    start = np.r_[np.zeros(6), 1.0]
    fit = least_squares(residual, start, loss="soft_l1", f_scale=0.02 * STANDARD_GRAVITY)
    params: np.ndarray = fit.x
    return params


def correct_accel_depth_bias(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the frame with the depth-linear accelerometer offset removed.

    Some tags' accelerometers shift with depth. On WHOI.001 (big Axy) the static acceleration
    of a fish swimming level reads 0.99 g near the surface and 1.08 g below 300 m, with the x
    axis tilted 21 degrees further: no change of posture alters the magnitude of gravity, and
    the pipeline's single attachment angle then turns the shift into a false pitch (+15
    degrees all night, -10 all day). The fit (fit_accel_depth_bias) brings the magnitude to
    1 g at every depth.
    """
    p = fit_accel_depth_bias(df)
    acc = list(SENSOR_CHANNELS[:3])
    depth = pd.to_numeric(df["Depth"], errors="coerce").interpolate(limit_direction="both")
    a = df[acc].apply(pd.to_numeric, errors="coerce").to_numpy(float)
    out: pd.DataFrame = df.copy()
    out[acc] = (a - p[:3] - np.outer(depth.to_numpy(float) / 100.0, p[3:6])) * p[6]
    g = STANDARD_GRAVITY
    logging.getLogger(__name__).info(
        "Accelerometer depth bias removed: offset at the surface "
        f"{np.round(p[:3] / g, 3).tolist()} g, per 100 m {np.round(p[3:6] / g, 4).tolist()} g, "
        f"scale {p[6]:.3f}"
    )
    return out


def load_metadata(meta_path: Path, tag_id: str) -> dict:
    """
    Load metadata for a specific tag.

    Args:
        meta_path: Path to the metadata CSV file.
        tag_id: The tag ID to filter for (e.g., 'RED001_20220812').

    Returns:
        Dictionary containing metadata for the tag.
    """
    df = pd.read_csv(meta_path)

    # Filter for the tag
    # The R script does: tag_id_short <- sub("_.*", "", uid) but then filters meta
    # by tag_id == tag_id_short
    # In the CSV, tag_id column has 'RED001_20220812'.
    # Let's assume exact match on tag_id column for now.

    tag_meta = df[df["tag_id"] == tag_id]

    if tag_meta.empty:
        # Try fuzzy match: Check if any tag_id in CSV is a prefix of requested, or vice versa
        # This handles the mismatch between "RED001" (config) and "RED001_2022..." (CSV)
        # or vice versa.
        for idx, row in df.iterrows():
            curr_id = str(row["tag_id"])
            if tag_id.startswith(curr_id) or curr_id.startswith(tag_id):
                logger = logging.getLogger(__name__)
                logger.info(f"Soft-matched tag_id '{tag_id}' to metadata entry '{curr_id}'")
                tag_meta = df.loc[[idx]]
                break

    if tag_meta.empty:
        available_ids = df["tag_id"].tolist()
        raise ValueError(
            f"No metadata found for tag_id: '{tag_id}'. "
            f"Available IDs in {meta_path}: {available_ids}"
        )

    row = tag_meta.iloc[0]

    # Parse times
    # Format in CSV: 8/13/22 02:37
    time_start = pd.to_datetime(row["time_start_utc"], format="%m/%d/%y %H:%M").tz_localize("UTC")
    time_end = pd.to_datetime(row["time_end_utc"], format="%m/%d/%y %H:%M").tz_localize("UTC")

    return {
        "time_start_utc": time_start,
        "time_end_utc": time_end,
        "tag_id": row["tag_id"],
        # Add other fields as needed
    }


def load_and_filter_data(data_path: Path, meta_path: Path, tag_id: str) -> pd.DataFrame:
    """
    Load sensor data and filter by deployment time from metadata.

    Args:
        data_path: Path to the sensor data CSV.
        meta_path: Path to the metadata CSV.
        tag_id: Tag ID to look up in metadata.

    Returns:
        Filtered DataFrame.
    """
    # Load metadata
    meta = load_metadata(meta_path, tag_id)

    # Load data
    feather_path = data_path.with_suffix(".feather")

    if feather_path.exists():
        # Load from Feather (fast)
        df = feather.read_table(feather_path).to_pandas()
    else:
        # Load from CSV (slow) and auto-convert
        try:
            logger = logging.getLogger(__name__)
            logger.info(f"Auto-converting {data_path} to Feather for performance...")
            try:
                feather_path = convert_csv_to_feather(data_path)
                df = feather.read_table(feather_path).to_pandas()
            except Exception as e:
                logger.warning(f"Auto-conversion failed: {e}. Falling back to CSV.")
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=pd.errors.ParserWarning)
                    df = pd.read_csv(
                        data_path,
                        comment=";",
                        index_col=False,
                        engine="python",
                        on_bad_lines="warn",
                    )
        except pd.errors.ParserError:
            # Fallback if python engine fails (unlikely for this specific issue)
            raise

    df = from_standard_export(df)

    # Filter out rows where 'int aX' is NA (R script: dat <- dat[!is.na(dat$"int aX"),])
    if "int aX" in df.columns:
        df = df.dropna(subset=["int aX"])

    # Ensure DateTimeP exists and is datetime
    if "DateTimeP" not in df.columns:
        if "Date" in df.columns:
            # Excel serial date conversion using high-precision utility
            def safe_excel_to_datetime(x: Any) -> Any:
                if pd.isna(x) or x is None or x == "":
                    return pd.NaT
                try:
                    return excel_date_to_datetime_ns(float(x))[0]
                except (ValueError, TypeError):
                    return pd.NaT

            df["DateTimeP"] = df["Date"].apply(safe_excel_to_datetime)
        else:
            raise ValueError("Could not find or construct DateTimeP column")
    elif not pd.api.types.is_datetime64_any_dtype(df["DateTimeP"]):
        df["DateTimeP"] = pd.to_datetime(df["DateTimeP"])

    # Filter by time
    # R: dat <- dat %>% dplyr::filter(DateTimeP > meta$time_start_utc)
    df_filtered = df[df["DateTimeP"] > meta["time_start_utc"]].copy()

    # Also filter by end time if available
    if pd.notna(meta["time_end_utc"]):
        df_filtered = df_filtered[df_filtered["DateTimeP"] < meta["time_end_utc"]]

    # Pre-calculate unix timestamp (float) for high-performance streaming
    # This avoids pd.Timestamp.timestamp() overhead in the yield loop
    ts_ns = df_filtered["DateTimeP"].values.astype("int64")
    df_filtered["timestamp"] = ts_ns // 10**9 + (ts_ns % 10**9) / 10**9

    return cast(pd.DataFrame, df_filtered)
