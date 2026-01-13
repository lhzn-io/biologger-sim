# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import warnings
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pyarrow.feather as feather

from biologger_sim.core.datetime_utils import excel_date_to_datetime_ns

from .converter import convert_csv_to_feather


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
                print(f"[biologger] Soft-matched tag_id '{tag_id}' to metadata entry '{curr_id}'")
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
            print(f"Auto-converting {data_path} to Feather for performance...")
            try:
                feather_path = convert_csv_to_feather(data_path)
                df = feather.read_table(feather_path).to_pandas()
            except Exception as e:
                print(f"Auto-conversion failed: {e}. Falling back to CSV.")
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

    return cast(pd.DataFrame, df_filtered)
