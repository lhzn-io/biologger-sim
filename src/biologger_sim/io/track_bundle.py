# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Track bundles: a compact, georeferenced export of one deployment's placed track.

A bundle is a directory of three files, written by :func:`write_bundle`:

``track.json``
    Metadata (schema ``track-bundle-v1``): deployment and sim IDs, provenance (sim git commit,
    config hash), the track model applied, the deployment origin and fixes, ``t0``, the sample
    rate and count, the column list with units, and bounds in the local frame and in lat/lon.
    ``pipeline`` lists the steps that made the track and ``metrics`` the numbers it is judged
    by, each in the fixed shape of :mod:`biologger_sim.core.provenance` with open ``params``;
    ``reproducibility`` holds the recipe and its fingerprint
    (:mod:`biologger_sim.io.reproducibility`), with ``config.yaml``, ``environment.txt`` and,
    for a dirty tree, ``code.patch`` written next to ``track.json``.
    ``roll_continuity`` records how the roll continuity columns were derived (null when the
    rows carry no rotated acceleration).
``track.f32``
    Little-endian Float32 samples stored as column blocks: ``count`` values of the first
    column, then ``count`` values of the second, and so on, in the order of
    :data:`COLUMNS`, then any :data:`OPTIONAL_COLUMNS` the run produced (``track.json``
    lists the columns present and their offsets). ``t`` is seconds since ``t0`` (Float32
    cannot hold Unix seconds to better than about 128 s; relative times hold 16 ms over two
    days).
``track.geojson``
    The track as a GeoJSON LineString in WGS84, simplified with Douglas-Peucker at
    :data:`SIMPLIFY_TOLERANCE_M` in the local north/east frame. Written only when the
    deployment has a start fix (without one there is no lat/lon).

North and east are metres from the deployment origin (the start fix), as everywhere in the
simulator; latitude and longitude come from :meth:`GeoReference.to_latlon`.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from biologger_sim.core import provenance as core_provenance
from biologger_sim.core.georef import GeoReference
from biologger_sim.functions import roll
from biologger_sim.functions.roll import native_rate, roll_continuity

from . import reproducibility

SCHEMA = "track-bundle-v1"
SIMPLIFY_TOLERANCE_M = 5.0

# (name, unit, source column in a <sim_id>_output.csv). VeDBA's and ODBA's unit depends on the
# processor and is filled in from Provenance.vedba_unit. The roll continuity columns have no
# source column: they are derived at the native rate from the attachment-rotated acceleration
# (ACCEL_SOURCE_COLUMNS) by biologger_sim.functions.roll before decimation.
COLUMNS: tuple[tuple[str, str, str | None], ...] = (
    ("t", "s", "timestamp"),
    ("north_m", "m", "pseudo_x"),
    ("east_m", "m", "pseudo_y"),
    ("depth_m", "m", "Depth"),
    ("heading_deg", "deg", "heading_degrees"),
    ("pitch_deg", "deg", "pitch_degrees"),
    ("roll_deg", "deg", "roll_degrees"),
    ("vedba", "", "VeDBA"),
    ("odba", "", "ODBA"),
    ("roll_unwrapped_deg", "deg", None),
    ("roll_rate_dps", "deg/s", None),
    ("roll_quality", "flag", None),
)
ACCEL_SOURCE_COLUMNS = ("X_Accel_rotate", "Y_Accel_rotate", "Z_Accel_rotate")
# Written after COLUMNS, and only when the run produced their source column: the current the
# correction applied and the through-water speed dead reckoning used.
OPTIONAL_COLUMNS: tuple[tuple[str, str, str], ...] = (
    ("current_east_m_s", "m/s", "current_u"),
    ("current_north_m_s", "m/s", "current_v"),
    ("current_missing", "flag", "current_missing"),
    ("speed_m_s", "m/s", "speed_through_water"),
)
# Flags that mark a stretch: 1 if set anywhere since the previous output sample.
STRETCH_FLAGS = ("roll_quality", "current_missing")

COLUMN_DESCRIPTIONS = {
    "roll_unwrapped_deg": "Cumulative roll, unwrapped at the native rate; value at sample time",
    "roll_rate_dps": "Roll rate, zero-phase low-passed; value at sample time",
    "roll_quality": "0 = fine, 1 = an uncertain unwrap step since the previous output sample",
    "current_east_m_s": "Eastward current applied at the animal's depth; value at sample time",
    "current_north_m_s": "Northward current applied at the animal's depth; value at sample time",
    "current_missing": (
        "0 = modeled current, 1 = a missing forcing sample (still water) since the previous "
        "output sample"
    ),
    "speed_m_s": (
        "Through-water speed used by dead reckoning, before placement (a fix-pinned track "
        "scales it by the placement step's scale)"
    ),
}

# Lab mode (PostFactoProcessor) computes VeDBA from accelerations in m/s^2; streaming mode
# (StreamingProcessor) works in g, so its VeDBA is about 1/9.81 of the lab value.
VEDBA_UNIT_LAB = "m/s^2"
VEDBA_UNIT_STREAMING = "g"


@dataclass
class Provenance:
    """Where a track came from; written into ``track.json``."""

    deployment_id: str
    sim_id: str
    run_id: str | None = None
    source: str = "pipeline"  # "pipeline" (export-track) or "from-run" (back-filled)
    sim_git_commit: str | None = None
    sim_git_dirty: bool | None = None
    config_file: str | None = None
    config_sha256: str | None = None
    species: str | None = None
    track_model_configured: str | None = None
    track_model_used: str | None = None
    heading_correction_deg: float | None = None
    heading_correction_source: str | None = None
    v_max_m_s: float | None = None
    vedba_unit: str = VEDBA_UNIT_LAB
    notes: list[str] = field(default_factory=list)
    # How the track was made, step by step, and the numbers it is judged by; see
    # biologger_sim.core.provenance. None when unknown (back-filled runs).
    pipeline: list[dict[str, Any]] | None = None
    metrics: list[dict[str, Any]] | None = None
    # See biologger_sim.io.reproducibility.
    reproducibility: dict[str, Any] | None = None


def git_state(repo_dir: Path) -> tuple[str | None, bool | None]:
    """Returns (HEAD commit, working tree dirty) for ``repo_dir``, or (None, None) outside git."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None, None
    return commit, bool(status.strip())


def sha256_file(path: Path) -> str:
    """Hex SHA-256 of a file's bytes."""
    return reproducibility.sha256_file(path)


def decimate(t: NDArray[np.float64], rate_hz: float) -> NDArray[np.intp]:
    """Indices of the first sample in each 1/rate_hz bin, counted from ``t[0]``.

    Keeps recorded samples (no interpolation, so headings never average across north). A
    rate at or above the native rate keeps every sample. ``t`` must be non-decreasing.
    """
    if len(t) == 0:
        return np.zeros(0, dtype=np.intp)
    if rate_hz <= 0:
        raise ValueError("rate_hz must be positive")
    bins = np.floor((t - t[0]) * rate_hz + 1e-9).astype(np.int64)
    keep = np.ones(len(t), dtype=bool)
    keep[1:] = bins[1:] != bins[:-1]
    return np.flatnonzero(keep)


def douglas_peucker(x: NDArray[np.float64], y: NDArray[np.float64], tol: float) -> NDArray[np.intp]:
    """Indices of the points kept by Douglas-Peucker simplification at tolerance ``tol``.

    Distances are to the chord between segment ends (to the end point when the chord has zero
    length). Iterative, so long tracks cannot overflow the recursion limit.
    """
    n = len(x)
    if n <= 2:
        return np.arange(n, dtype=np.intp)
    keep = np.zeros(n, dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        i, j = stack.pop()
        if j - i < 2:
            continue
        xs, ys = x[i + 1 : j], y[i + 1 : j]
        dx, dy = x[j] - x[i], y[j] - y[i]
        chord = float(np.hypot(dx, dy))
        if chord == 0.0:
            d = np.hypot(xs - x[i], ys - y[i])
        else:
            d = np.abs(dy * (xs - x[i]) - dx * (ys - y[i])) / chord
        k = int(np.argmax(d))
        if d[k] > tol:
            m = i + 1 + k
            keep[m] = True
            stack.append((i, m))
            stack.append((m, j))
    return np.flatnonzero(keep)


def to_latlon(
    georef: GeoReference, north: NDArray[np.float64], east: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Vectorised :meth:`GeoReference.to_latlon` over arrays of north/east metres."""
    pairs = [georef.to_latlon(float(n), float(e)) for n, e in zip(north, east, strict=True)]
    if not pairs:
        return np.zeros(0), np.zeros(0)
    lat, lon = np.array(pairs, dtype=np.float64).T
    return lat, lon


def _iso(t: float) -> str:
    return datetime.fromtimestamp(t, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _finite_bounds(a: NDArray[Any]) -> list[float] | None:
    a = a[np.isfinite(a)]
    return [float(a.min()), float(a.max())] if a.size else None


def _georef_json(georef: GeoReference | None) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if georef is None:
        return None, []
    origin = {"lat": georef.start.lat, "lon": georef.start.lon}
    fixes = [
        {
            "kind": "start",
            "t": georef.start.t,
            "time_utc": _iso(georef.start.t),
            "lat": georef.start.lat,
            "lon": georef.start.lon,
            "north_m": 0.0,
            "east_m": 0.0,
        }
    ]
    end_ne = georef.end_ne()
    if georef.end is not None and end_ne is not None:
        fixes.append(
            {
                "kind": "end",
                "t": georef.end.t,
                "time_utc": _iso(georef.end.t),
                "lat": georef.end.lat,
                "lon": georef.end.lon,
                "north_m": end_ne[0],
                "east_m": end_ne[1],
            }
        )
    return origin, fixes


def track_columns(rows: pd.DataFrame) -> dict[str, NDArray[np.float64]]:
    """Pulls the bundle columns (absolute Unix ``t``) out of an output-CSV DataFrame.

    Missing optional columns (heading without a magnetometer, say) become NaN; rows with a
    missing timestamp are dropped, and the rest are sorted by time.
    """
    if "timestamp" not in rows or "pseudo_x" not in rows or "pseudo_y" not in rows:
        raise ValueError("rows need timestamp, pseudo_x and pseudo_y columns")
    df = rows[rows["timestamp"].notna()].sort_values("timestamp", kind="stable")
    out: dict[str, NDArray[np.float64]] = {}
    for name, _, src in COLUMNS:
        if src is not None and src in df:
            out[name] = pd.to_numeric(df[src], errors="coerce").to_numpy(dtype=np.float64)
        else:
            out[name] = np.full(len(df), np.nan)
    for name, _, src in OPTIONAL_COLUMNS:
        if src in df:
            out[name] = pd.to_numeric(df[src], errors="coerce").to_numpy(dtype=np.float64)
    if all(c in df for c in ACCEL_SOURCE_COLUMNS):
        ax, ay, az = (
            pd.to_numeric(df[c], errors="coerce").to_numpy(dtype=np.float64)
            for c in ACCEL_SOURCE_COLUMNS
        )
        rc = roll_continuity(out["t"], ax, ay, az)
        out["roll_unwrapped_deg"] = rc.roll_unwrapped_deg
        out["roll_rate_dps"] = rc.roll_rate_dps
        out["roll_quality"] = rc.uncertain.astype(np.float64)
    return out


def decimate_quality(flags: NDArray[np.float64], idx: NDArray[np.intp]) -> NDArray[np.float64]:
    """Per output sample, 1 if any flag is set since the previous output sample, else 0.

    Output sample ``k`` covers native samples ``idx[k-1] + 1`` to ``idx[k]`` (just ``idx[0]``
    for the first), so the flag marks the stretch a chart draws between ``k - 1`` and ``k``.
    All-NaN flags (no acceleration to derive them from) stay NaN.
    """
    if len(idx) == 0:
        return np.zeros(0)
    if np.isnan(flags).all():
        return np.full(len(idx), np.nan)
    c = np.cumsum(np.nan_to_num(flags) > 0)
    hits = c[idx]
    out = np.empty(len(idx))
    out[0] = float(hits[0] > (c[idx[0] - 1] if idx[0] > 0 else 0))
    out[1:] = (np.diff(hits) > 0).astype(np.float64)
    return out


def write_bundle(
    out_dir: Path,
    rows: pd.DataFrame,
    georef: GeoReference | None,
    provenance: Provenance,
    rate_hz: float = 1.0,
    tolerance_m: float = SIMPLIFY_TOLERANCE_M,
) -> dict[str, Any]:
    """Writes ``track.json``, ``track.f32`` and (with a georeference) ``track.geojson``.

    ``rows`` holds pipeline output records (the columns of ``<sim_id>_output.csv``) at the
    native rate; they are decimated to ``rate_hz``. Returns the ``track.json`` content.
    """
    cols = track_columns(rows)
    native_hz = native_rate(cols["t"])
    has_roll = not np.isnan(cols["roll_quality"]).all()
    uncertain_fraction = float(np.nanmean(cols["roll_quality"])) if has_roll else None
    idx = decimate(cols["t"], rate_hz)
    flags = {k: decimate_quality(cols[k], idx) for k in STRETCH_FLAGS if k in cols}
    # Every other column (roll_unwrapped_deg included) takes the value at the sample time,
    # which keeps the cumulative roll cumulative.
    cols = {k: v[idx] for k, v in cols.items()}
    cols.update(flags)
    names = [name for name, _, _ in COLUMNS] + [n for n, _, _ in OPTIONAL_COLUMNS if n in cols]
    count = len(idx)
    if count == 0:
        raise ValueError("no samples to export")
    t0 = float(cols["t"][0])
    cols["t"] = cols["t"] - t0

    core_provenance.validate(provenance.pipeline or [], provenance.metrics or [])
    out_dir.mkdir(parents=True, exist_ok=True)

    # Column blocks, little-endian Float32.
    block = np.stack([cols[name] for name in names]).astype("<f4")
    (out_dir / "track.f32").write_bytes(block.tobytes(order="C"))

    north, east = cols["north_m"], cols["east_m"]
    lat_bounds = lon_bounds = None
    geojson_points = 0
    if georef is not None:
        lat, lon = to_latlon(georef, north, east)
        lat_bounds, lon_bounds = _finite_bounds(lat), _finite_bounds(lon)
        ok = np.flatnonzero(np.isfinite(north) & np.isfinite(east))
        kept = ok[douglas_peucker(north[ok], east[ok], tolerance_m)]
        geojson_points = len(kept)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[round(float(lon[i]), 7), round(float(lat[i]), 7)] for i in kept],
            },
            "properties": {
                "schema": SCHEMA,
                "deployment_id": provenance.deployment_id,
                "sim_id": provenance.sim_id,
                "run_id": provenance.run_id,
                "simplify_tolerance_m": tolerance_m,
                "time_start_utc": _iso(t0),
                "time_end_utc": _iso(t0 + float(cols["t"][-1])),
            },
        }
        collection = {"type": "FeatureCollection", "features": [feature]}
        (out_dir / "track.geojson").write_text(json.dumps(collection, separators=(",", ":")))

    origin, fixes = _georef_json(georef)
    units = {name: unit for name, unit, _ in (*COLUMNS, *OPTIONAL_COLUMNS)}
    units["vedba"] = units["odba"] = provenance.vedba_unit
    roll_meta = (
        {
            "source": "accelerometer",
            "input_columns": list(ACCEL_SOURCE_COLUMNS),
            "native_rate_hz": native_hz,
            "roll_smoothing_s": roll.SMOOTH_S,
            "rate_cutoff_hz": roll.RATE_CUTOFF_HZ,
            "step_limit_deg": roll.STEP_LIMIT_DEG,
            "pitch_limit_deg": roll.PITCH_LIMIT_DEG,
            "accel_norm_tol_g": roll.ACCEL_NORM_TOL,
            "ayz_min_g": roll.AYZ_MIN,
            "gap_factor": roll.GAP_FACTOR,
            "uncertain_native_fraction": uncertain_fraction,
        }
        if has_roll
        else None
    )
    meta: dict[str, Any] = {
        "schema": SCHEMA,
        "deployment_id": provenance.deployment_id,
        "sim_id": provenance.sim_id,
        "run_id": provenance.run_id,
        "created_utc": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "provenance": {
            "source": provenance.source,
            "sim_git_commit": provenance.sim_git_commit,
            "sim_git_dirty": provenance.sim_git_dirty,
            "config_file": provenance.config_file,
            "config_sha256": provenance.config_sha256,
            "notes": provenance.notes,
        },
        "species": provenance.species,
        "track_model_configured": provenance.track_model_configured,
        "track_model_used": provenance.track_model_used,
        "heading_correction_deg": provenance.heading_correction_deg,
        "heading_correction_source": provenance.heading_correction_source,
        "v_max_m_s": provenance.v_max_m_s,
        "pipeline": provenance.pipeline,
        "metrics": provenance.metrics,
        "reproducibility": provenance.reproducibility,
        "origin": origin,
        "fixes": fixes,
        "t0": t0,
        "t0_utc": _iso(t0),
        "duration_s": float(cols["t"][-1]),
        "rate_hz": rate_hz,
        "count": count,
        "data": {
            "file": "track.f32",
            "dtype": "float32",
            "byte_order": "little",
            "layout": "column_blocks",
            "bytes": int(block.nbytes),
        },
        "columns": [
            {
                "name": name,
                "unit": units[name],
                "offset_bytes": i * count * 4,
                **({"relative_to": "t0"} if name == "t" else {}),
                **(
                    {"description": COLUMN_DESCRIPTIONS[name]}
                    if name in COLUMN_DESCRIPTIONS
                    else {}
                ),
            }
            for i, name in enumerate(names)
        ],
        "roll_continuity": roll_meta,
        "bounds": {
            "north_m": _finite_bounds(north),
            "east_m": _finite_bounds(east),
            "depth_m": _finite_bounds(cols["depth_m"]),
            "lat": lat_bounds,
            "lon": lon_bounds,
        },
        "geojson": (
            {"file": "track.geojson", "points": geojson_points, "simplify_tolerance_m": tolerance_m}
            if georef is not None
            else None
        ),
    }
    (out_dir / "track.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def read_bundle(bundle_dir: Path) -> tuple[dict[str, Any], dict[str, NDArray[np.float32]]]:
    """Reads a bundle back: (``track.json`` content, column name to Float32 array)."""
    meta = json.loads((bundle_dir / "track.json").read_text())
    raw = np.frombuffer((bundle_dir / "track.f32").read_bytes(), dtype="<f4")
    count = int(meta["count"])
    names = [c["name"] for c in meta["columns"]]
    if raw.size != count * len(names):
        raise ValueError(f"track.f32 has {raw.size} values, expected {count * len(names)}")
    return meta, {name: raw[i * count : (i + 1) * count] for i, name in enumerate(names)}
