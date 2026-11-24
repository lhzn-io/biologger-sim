# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Ocean-current drift for the dead-reckoned track.

Dead reckoning integrates the animal's velocity through the water. Adding the water's own
velocity, sampled from a parent ocean model along the track, gives the velocity over ground:

    north[i] = north[i-1] + (speed cos(heading) + v) dt
    east[i]  = east[i-1]  + (speed sin(heading) + u) dt

The forcing is sampled through ``forcingkit-client`` on a thinned copy of the track (one point
per ``sample_interval_s``, default a minute: the parent models resolve hours and kilometers),
at the animal's depth, then interpolated back to every record. The parent's vertical velocity
``w`` is sampled with ``u`` and ``v`` when its store has one (NECOFS does, HYCOM does not); it is
recorded for display and plays no part in the drift. The caller chooses the
positions: the post-facto processor samples in passes, first along the through-water track,
then along each placed track until it settles (docs/source/tracks.rst, "Where the current is
sampled").
"""

from __future__ import annotations

import ctypes
import ctypes.util
import gc
import logging
from dataclasses import dataclass, field
from typing import Any, Protocol

import numpy as np
from numpy.typing import NDArray

from .georef import GeoReference
from .types import CurrentCorrectionConfig

logger = logging.getLogger(__name__)


class TrajectorySampler(Protocol):
    """The part of ``forcingkit_client.Client`` used here (a fake in tests)."""

    def interpolate_trajectory(
        self, lon: Any, lat: Any, time: Any, z: Any = None, **kwargs: Any
    ) -> Any: ...


@dataclass
class CurrentDrift:
    """Per-record current and its cumulative displacement, plus provenance."""

    u: NDArray[np.float64]  # eastward current (m/s), per record
    v: NDArray[np.float64]  # northward current (m/s), per record
    drift_north: NDArray[np.float64]  # cumulative displacement (m), per record
    drift_east: NDArray[np.float64]
    n_samples: int
    n_missing: int  # samples with no value (land, below the sea floor, outside the grid)
    # Per record: True where the interpolated current leans on a missing sample (still water).
    missing: NDArray[np.bool_]
    attrs: dict[str, Any] = field(default_factory=dict)
    # Upward current (m/s), per record, NaN where a sample has none; None when the parent has no
    # vertical velocity at all.
    w: NDArray[np.float64] | None = None


def time_windows(t: NDArray[np.float64], window_s: float) -> list[slice]:
    """Consecutive slices of ``t`` (sorted) that each span less than ``window_s`` seconds."""
    t = np.asarray(t, dtype=float)
    if len(t) == 0:
        return []
    bins = np.floor((t - t[0]) / window_s)
    starts = np.flatnonzero(np.diff(bins, prepend=-1.0) > 0)
    ends = np.append(starts[1:], len(t))
    return [slice(int(a), int(b)) for a, b in zip(starts, ends, strict=True)]


def release_memory() -> None:
    """Frees what the last forcing request left behind, and hands it back to the system.

    A store is interpolated in memory, and glibc keeps freed heap pages for reuse, so without
    the trim a run's resident memory grows with every request (2026-11-18: the whale shark's
    sampling passes reached the export's 18 GB limit).
    """
    gc.collect()
    name = ctypes.util.find_library("c")
    if name is None:
        return
    try:
        trim = ctypes.CDLL(name).malloc_trim
    except (OSError, AttributeError):  # not glibc (macOS, musl)
        return
    trim(0)


def thin_indices(t: NDArray[np.float64], interval_s: float) -> NDArray[np.intp]:
    """Indices of about one record per ``interval_s``, always including the first and last."""
    t = np.asarray(t, dtype=float)
    if len(t) == 0:
        return np.zeros(0, dtype=np.intp)
    bins = np.floor((t - t[0]) / interval_s)
    idx = np.flatnonzero(np.diff(bins, prepend=-1.0) > 0)
    if idx[-1] != len(t) - 1:
        idx = np.append(idx, len(t) - 1)
    return idx.astype(np.intp)


def compute_current_drift(
    sampler: TrajectorySampler,
    t: NDArray[np.float64],
    north: NDArray[np.float64],
    east: NDArray[np.float64],
    depth_m: NDArray[np.float64] | None,
    georef: GeoReference,
    dt: NDArray[np.float64],
    sample_interval_s: float = 60.0,
    window_s: float | None = 21600.0,
    **ocean_options: Any,
) -> CurrentDrift:
    """Samples u and v along the track and integrates them over ``dt``.

    The samples are requested in time windows of ``window_s`` (None: one request for the whole
    track). forcingkit serves each request as one store covering its points' bounding box and
    hours, interpolated in memory, so a long or wide track asked for at once can need more
    memory than the machine has; windows keep each store small.

    t: Unix seconds (UTC); north, east: dead-reckoned meters from the start fix; depth_m:
    meters, positive down (None samples at the surface); dt: the step used by dead reckoning,
    so ``drift`` and the dead-reckoned track integrate on the same clock. Missing samples count
    as still water.

    ``w`` is asked for too; a store without it (KeyError naming ``'w'``) is asked again for
    ``u`` and ``v`` alone, and the rest of the track is sampled without it.
    """
    t = np.asarray(t, dtype=float)
    idx = thin_indices(t, sample_interval_s)
    lat = np.empty(len(idx))
    lon = np.empty(len(idx))
    for k, i in enumerate(idx):
        lat[k], lon[k] = georef.to_latlon(float(north[i]), float(east[i]))
    # forcingkit z is meters positive up; surface excursions (negative depth) clamp to 0.
    z = np.zeros(len(idx)) if depth_m is None else -np.clip(np.asarray(depth_m)[idx], 0.0, None)
    times = np.asarray(np.round(t[idx] * 1e3), dtype="int64").astype("datetime64[ms]")

    u_s: NDArray[np.float64] = np.empty(len(idx), dtype=np.float64)
    v_s: NDArray[np.float64] = np.empty(len(idx), dtype=np.float64)
    w_s: NDArray[np.float64] = np.full(len(idx), np.nan, dtype=np.float64)
    vertical = True
    attrs: dict[str, Any] = {}
    windows = time_windows(t[idx], window_s) if window_s else [slice(0, len(idx))]

    def request(w: slice, names: tuple[str, ...]) -> Any:
        return sampler.interpolate_trajectory(
            lon[w],
            lat[w],
            times[w],
            z[w],
            variables=names,
            trajectory_id="biologger",
            **ocean_options,
        )

    for w in windows:
        if vertical:
            try:
                ds = request(w, ("u", "v", "w"))
            except KeyError as e:
                if "'w'" not in str(e):
                    raise
                vertical = False
        if not vertical:
            ds = request(w, ("u", "v"))
        u_s[w] = np.asarray(ds["u"].values, dtype=float)
        v_s[w] = np.asarray(ds["v"].values, dtype=float)
        if vertical and "w" in ds:
            w_s[w] = np.asarray(ds["w"].values, dtype=float)
        for key, val in getattr(ds, "attrs", {}).items():
            if key.startswith("forcingkit_"):
                seen = attrs.setdefault(key, [])
                if val not in seen:
                    seen.append(val)
        del ds
        release_memory()
    missing = ~(np.isfinite(u_s) & np.isfinite(v_s))
    if missing.all():
        raise ValueError("the parent ocean has no current along the track (all samples missing)")
    if missing.any():
        logger.warning(
            f"Current correction: {int(missing.sum())} of {len(idx)} samples missing; "
            "treated as still water"
        )
    u_s = np.where(missing, 0.0, u_s)
    v_s = np.where(missing, 0.0, v_s)

    u = np.interp(t, t[idx], u_s)
    v = np.interp(t, t[idx], v_s)
    dt = np.asarray(dt, dtype=float)
    return CurrentDrift(
        u=u,
        v=v,
        drift_north=np.cumsum(v * dt),
        drift_east=np.cumsum(u * dt),
        n_samples=len(idx),
        n_missing=int(missing.sum()),
        missing=np.interp(t, t[idx], missing.astype(float)) > 0.0,
        # One value per key, or the distinct values of the windows joined with ", ".
        attrs={key: ", ".join(str(v) for v in vals) for key, vals in attrs.items()},
        w=np.interp(t, t[idx], w_s) if np.isfinite(w_s).any() else None,
    )


def make_sampler(cfg: CurrentCorrectionConfig) -> Any:
    """A ``forcingkit_client.Client`` for ``cfg``, or an ``OceanStoreSampler`` when
    ``cfg.ocean_store`` is set; raises ImportError without the package."""
    if cfg.ocean_store is not None:
        from .ocean_store import OceanStoreSampler

        return OceanStoreSampler(cfg.ocean_store)
    try:
        from forcingkit_client import Client  # type: ignore[import-not-found]
    except ImportError as e:
        raise ImportError(
            "current correction needs forcingkit-client (Python 3.11+): "
            "pip install 'biologger-sim[currents]'"
        ) from e
    kwargs: dict[str, Any] = {"timeout_s": cfg.timeout_s}
    if cfg.cache_dir is not None:
        kwargs["cache_dir"] = cfg.cache_dir
    return Client(cfg.forcingkit_url, **kwargs)
