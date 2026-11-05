# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Ocean-current drift for the dead-reckoned track.

Dead reckoning integrates the animal's velocity through the water. Adding the water's own
velocity, sampled from a parent ocean model along the track, gives the velocity over ground:

    north[i] = north[i-1] + (speed cos(heading) + v) dt
    east[i]  = east[i-1]  + (speed sin(heading) + u) dt

The forcing is sampled through ``forcingkit-client`` on a thinned copy of the track (one point
per ``sample_interval_s``, default a minute: the parent models resolve hours and kilometres),
at the animal's depth, then interpolated back to every record. The sampling positions are the
uncorrected dead-reckoned ones: over a deployment the drift is a few kilometres, well inside
one parent-model cell, so a second pass at the corrected positions changes little.
"""

from __future__ import annotations

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
    attrs: dict[str, Any] = field(default_factory=dict)


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
    **ocean_options: Any,
) -> CurrentDrift:
    """Samples u and v along the track and integrates them over ``dt``.

    t: Unix seconds (UTC); north, east: dead-reckoned metres from the start fix; depth_m:
    metres, positive down (None samples at the surface); dt: the step used by dead reckoning,
    so ``drift`` and the dead-reckoned track integrate on the same clock. Missing samples count
    as still water.
    """
    t = np.asarray(t, dtype=float)
    idx = thin_indices(t, sample_interval_s)
    lat = np.empty(len(idx))
    lon = np.empty(len(idx))
    for k, i in enumerate(idx):
        lat[k], lon[k] = georef.to_latlon(float(north[i]), float(east[i]))
    # forcingkit z is metres positive up; surface excursions (negative depth) clamp to 0.
    z = np.zeros(len(idx)) if depth_m is None else -np.clip(np.asarray(depth_m)[idx], 0.0, None)
    times = np.asarray(np.round(t[idx] * 1e3), dtype="int64").astype("datetime64[ms]")

    ds = sampler.interpolate_trajectory(
        lon, lat, times, z, variables=("u", "v"), trajectory_id="biologger", **ocean_options
    )
    u_s = np.asarray(ds["u"].values, dtype=float)
    v_s = np.asarray(ds["v"].values, dtype=float)
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
        attrs={
            key: val
            for key, val in getattr(ds, "attrs", {}).items()
            if key.startswith("forcingkit_")
        },
    )


def make_sampler(cfg: CurrentCorrectionConfig) -> Any:
    """A ``forcingkit_client.Client`` for ``cfg``; raises ImportError without the package."""
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
