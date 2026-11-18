# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""How far a placed, current-corrected track runs from where its current was sampled.

The current correction samples the ocean current once, along the dead-reckoned through-water
positions, before placement (see docs/source/tracks.rst, "Known limit"). This script measures
that gap for one deployment from two track bundles of the same sim commit:

``SAMPLED``
    The ``dr`` variant (``track_model: dead_reckoning``, no current correction). Its track is
    the through-water dead-reckoned path, which is where the current was sampled.
``PLACED``
    A variant with the current correction applied (``pin_cur``, for example).

It prints the separation between the two tracks (median and maximum, at every bundle sample
and at the correction's sample interval), the drift the correction applied (from the PLACED
bundle's ``current_correction`` step), and the placement's rotation and scale. With
``--forcingkit-url`` it also re-samples the current along the PLACED track through
forcingkit-client and integrates it the same way, to show the drift the correction would add
at the placed positions. No data is read except the two bundles given on the command line.

Usage::

    python scripts/current_sampling_offset.py <tracks>/<run>_dr <tracks>/<run>_pin_cur \\
        [--forcingkit-url http://host:9598]
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from biologger_sim.core.currents import compute_current_drift
from biologger_sim.core.georef import GeoFix, GeoReference
from biologger_sim.io.track_bundle import read_bundle


def _step(meta: dict[str, Any], name: str) -> dict[str, Any] | None:
    for step in meta.get("pipeline") or []:
        if step.get("step") == name:
            return dict(step)
    return None


def _metric(meta: dict[str, Any], name: str) -> float | None:
    for m in meta.get("metrics") or []:
        if m.get("name") == name:
            value = m.get("value")
            return None if value is None else float(value)
    return None


def _georef(meta: dict[str, Any]) -> GeoReference:
    fixes = {f["kind"]: f for f in meta.get("fixes") or []}
    if "start" not in fixes:
        raise SystemExit("the PLACED bundle has no start fix, so it has no latitude/longitude")
    start = GeoFix(fixes["start"]["t"], fixes["start"]["lat"], fixes["start"]["lon"])
    end = fixes.get("end")
    return GeoReference(start, GeoFix(end["t"], end["lat"], end["lon"]) if end else None)


def _bearing_km(north_m: float, east_m: float) -> str:
    bearing = math.degrees(math.atan2(east_m, north_m)) % 360.0
    return f"{math.hypot(north_m, east_m) / 1000.0:.1f} km toward {bearing:.0f} deg"


def _thinned(t: NDArray[np.float64], interval_s: float) -> NDArray[np.intp]:
    bins = np.floor((t - t[0]) / interval_s)
    return np.flatnonzero(np.diff(bins, prepend=-1.0) > 0)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("sampled", type=Path, help="bundle of the dr variant (no current)")
    parser.add_argument("placed", type=Path, help="bundle with the current correction applied")
    parser.add_argument(
        "--forcingkit-url",
        default=None,
        help="re-sample the current along the PLACED track through this forcingkit service",
    )
    parser.add_argument("--timeout-s", type=float, default=1800.0, help="forcingkit timeout")
    args = parser.parse_args(argv)

    meta_s, cols_s = read_bundle(args.sampled)
    meta_p, cols_p = read_bundle(args.placed)
    for label, meta in (("sampled", meta_s), ("placed", meta_p)):
        prov = meta.get("provenance") or {}
        print(
            f"{label}: {meta.get('deployment_id')} {meta.get('sim_id')}, "
            f"sim {str(prov.get('sim_git_commit'))[:7]} (dirty: {prov.get('sim_git_dirty')}), "
            f"track model {meta.get('track_model_used')}, {meta['count']} samples "
            f"at {meta['rate_hz']} Hz"
        )

    cc = _step(meta_p, "current_correction")
    if _step(meta_s, "current_correction") is not None:
        print("warning: the SAMPLED bundle has a current correction; use the dr variant")
    if cc is None or cc.get("status") != "applied":
        print("error: the PLACED bundle has no applied current_correction step", file=sys.stderr)
        return 1
    commit_s = (meta_s.get("provenance") or {}).get("sim_git_commit")
    commit_p = (meta_p.get("provenance") or {}).get("sim_git_commit")
    if commit_s != commit_p:
        print("warning: the bundles come from different sim commits")
    t_s = meta_s["t0"] + cols_s["t"].astype(np.float64)
    t_p = meta_p["t0"] + cols_p["t"].astype(np.float64)
    if len(t_s) != len(t_p) or np.max(np.abs(t_s - t_p)) > 0.5:
        print("error: the bundles do not share sample times", file=sys.stderr)
        return 1

    params = cc.get("params") or {}
    interval = float(params.get("sample_interval_s", 60.0))
    sep = np.hypot(
        cols_p["north_m"].astype(np.float64) - cols_s["north_m"],
        cols_p["east_m"].astype(np.float64) - cols_s["east_m"],
    )
    ok = np.isfinite(sep)
    k = _thinned(t_p, interval)
    k = k[ok[k]]
    print(
        f"separation, placed vs sampled: median {np.median(sep[ok]) / 1000:.1f} km, "
        f"max {np.max(sep[ok]) / 1000:.1f} km (every sample); "
        f"median {np.median(sep[k]) / 1000:.1f} km, max {np.max(sep[k]) / 1000:.1f} km "
        f"(one per {interval:.0f} s)"
    )

    drift = params.get("drift_end_m") or {}
    print(
        f"applied drift (current_correction.drift_end_m): "
        f"{_bearing_km(float(drift['north']), float(drift['east']))}, "
        f"donor {params.get('donor_used')}, {params.get('samples')} samples, "
        f"{params.get('missing')} missing"
    )
    placement = (_step(meta_p, "placement") or {}).get("params") or {}
    if "rotation_deg" in placement:
        print(
            f"placement: rotation {placement['rotation_deg']:.1f} deg, "
            f"scale {placement['scale']:.3f}"
        )
    for label, meta in (("sampled", meta_s), ("placed", meta_p)):
        miss = _metric(meta, "end_fix_miss_before_placement")
        if miss is not None:
            print(f"end_fix_miss_before_placement ({label}): {miss / 1000:.1f} km")

    if args.forcingkit_url:
        from biologger_sim.core.currents import make_sampler
        from biologger_sim.core.types import CurrentCorrectionConfig

        cfg = CurrentCorrectionConfig(
            forcingkit_url=args.forcingkit_url,
            sample_interval_s=interval,
            vertical_spacing_m=float(params.get("vertical_spacing_m", 10.0)),
            timeout_s=args.timeout_s,
        )
        dt = np.diff(t_p, prepend=t_p[0])
        resampled = compute_current_drift(
            make_sampler(cfg),
            t_p,
            cols_p["north_m"].astype(np.float64),
            cols_p["east_m"].astype(np.float64),
            cols_p["depth_m"].astype(np.float64),
            _georef(meta_p),
            dt,
            sample_interval_s=cfg.sample_interval_s,
            vertical_spacing_m=cfg.vertical_spacing_m,
        )
        print(
            f"re-sampled along the placed track: "
            f"{_bearing_km(float(resampled.drift_north[-1]), float(resampled.drift_east[-1]))}, "
            f"donor {resampled.attrs.get('forcingkit_ocean_donor')}, "
            f"{resampled.n_samples} samples, {resampled.n_missing} missing"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
