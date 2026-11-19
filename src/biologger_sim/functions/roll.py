# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Roll continuity: cumulative (phase-unwrapped) roll, roll rate and an unwrap-quality flag.

The pipeline's ``roll_degrees`` comes from the static acceleration, a centred moving average
over ``filt_len`` samples (3 s at 16 Hz, 1.92 s at 25 Hz). That average suppresses roll
faster than about 1/window (0.33 to 0.52 Hz), so a barrel roll at 0.5 to 1 rev/s averages the
Y/Z gravity components towards zero and its static roll is noise. Counting full rotations needs
the attachment-rotated acceleration at the native rate, smoothed only lightly
(:data:`SMOOTH_S`), and unwrapping before any decimation: at 1 Hz, rotation faster than about
0.25 to 0.3 rev/s aliases.

The roll angle is ``atan2(ay, az)`` (the R ``pitchRoll2`` convention, the same as
``roll_degrees``). A step between native samples is uncertain when it exceeds
:data:`STEP_LIMIT_DEG` (the unwrap cannot tell its direction), when ``|pitch|`` exceeds
:data:`PITCH_LIMIT_DEG` (roll from gravity is ill-conditioned near vertical), when ``|a|`` is
more than :data:`ACCEL_NORM_TOL` from the deployment's median magnitude (taken as 1 g, so the
check works in g or m/s^2), when less than :data:`AYZ_MIN` of 1 g is left in the y-z plane
(the roll angle's own ill-conditioning, which the pitch limit misses under dynamic
acceleration), or when it spans missing data or a time gap. The thresholds are the starting
values of the portal's roll visualisation note (section 4.2), with the |a| tolerance widened
from 0.25 g on the static component to 0.3 g on the lightly smoothed raw signal, which keeps
more tailbeat.

The tags carry no gyroscope. Magnetometer-assisted unwrapping is not attempted: roll from the
field is undefined when the body axis lies along it, and three of the six swordfish tags have
no magnetometer, so the accelerometer is the one source common to all of them.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy.signal import butter, sosfiltfilt

SMOOTH_S = 0.2
RATE_CUTOFF_HZ = 0.15  # Segre et al. 2016
STEP_LIMIT_DEG = 135.0
PITCH_LIMIT_DEG = 65.0
ACCEL_NORM_TOL = 0.3  # fraction of 1 g
AYZ_MIN = 0.35  # fraction of 1 g left in the y-z plane
GAP_FACTOR = 2.0  # a time step longer than this many native periods is a gap


@dataclass(frozen=True)
class RollContinuity:
    """Native-rate roll continuity series, aligned with the input samples."""

    roll_unwrapped_deg: NDArray[np.float64]
    roll_rate_dps: NDArray[np.float64]
    uncertain: NDArray[np.bool_]
    native_rate_hz: float


def _empty() -> RollContinuity:
    z = np.zeros(0)
    return RollContinuity(z, z.copy(), np.zeros(0, dtype=bool), float("nan"))


def native_rate(t: NDArray[np.float64]) -> float:
    """The median sample rate of a non-decreasing time series, in Hz (NaN if undefined)."""
    dt = np.diff(t)
    dt = dt[np.isfinite(dt) & (dt > 0)]
    return float(1.0 / np.median(dt)) if dt.size else float("nan")


def roll_continuity(
    t: NDArray[np.float64],
    ax: NDArray[np.float64],
    ay: NDArray[np.float64],
    az: NDArray[np.float64],
    *,
    smooth_s: float = SMOOTH_S,
    rate_cutoff_hz: float = RATE_CUTOFF_HZ,
    step_limit_deg: float = STEP_LIMIT_DEG,
    pitch_limit_deg: float = PITCH_LIMIT_DEG,
    accel_norm_tol: float = ACCEL_NORM_TOL,
    ayz_min: float = AYZ_MIN,
) -> RollContinuity:
    """Unwrapped roll, low-passed roll rate and per-sample uncertainty at the native rate.

    ``t`` is in seconds and non-decreasing; ``ax``, ``ay`` and ``az`` are the attachment-rotated
    accelerations in any consistent unit. Samples before the first valid roll are NaN; across
    missing samples the unwrapped roll holds its last value and the next step is flagged.
    """
    n = len(t)
    if n == 0:
        return _empty()
    fs = native_rate(t)
    acc = pd.DataFrame({"x": ax, "y": ay, "z": az}, dtype=np.float64)
    w = round(smooth_s * fs) if np.isfinite(fs) else 1
    if w > 1:
        acc = acc.rolling(w, center=True, min_periods=1).mean()
    x, y, z = (acc[c].to_numpy() for c in ("x", "y", "z"))

    roll = np.arctan2(y, z)
    pitch = np.degrees(np.arctan2(x, np.hypot(y, z)))
    norm = np.sqrt(x * x + y * y + z * z)
    valid = np.isfinite(roll) & np.isfinite(t)
    if not valid.any():
        nan = np.full(n, np.nan)
        return RollContinuity(nan, nan.copy(), np.ones(n, dtype=bool), fs)

    vi = np.flatnonzero(valid)
    step = np.zeros(n)
    d = np.diff(roll[vi])
    step[vi[1:]] = (d + np.pi) % (2.0 * np.pi) - np.pi  # wrapped to [-pi, pi)
    unwrapped = np.degrees(roll[vi[0]] + np.cumsum(step))
    unwrapped[: vi[0]] = np.nan

    g_ref = float(np.nanmedian(norm[valid]))
    with np.errstate(invalid="ignore"):
        uncertain = ~valid
        uncertain |= np.abs(np.degrees(step)) > step_limit_deg
        uncertain |= np.abs(pitch) > pitch_limit_deg
        if g_ref > 0:
            uncertain |= np.abs(norm / g_ref - 1.0) > accel_norm_tol
            uncertain |= np.hypot(y, z) / g_ref < ayz_min
    # The step into a valid sample after missing data spans the gap.
    after_gap = vi[1:][np.diff(vi) > 1]
    uncertain[after_gap] = True
    if np.isfinite(fs):
        dt = np.diff(t)
        uncertain[1:] |= dt > GAP_FACTOR / fs
    uncertain[: vi[0]] = True

    # Rate: derivative of the unwrapped roll, then a zero-phase low-pass.
    filled = unwrapped.copy()
    filled[: vi[0]] = filled[vi[0]]
    tt = t.astype(np.float64)
    rate = np.gradient(filled, tt) if n > 1 else np.zeros(n)
    rate = np.where(np.isfinite(rate), rate, 0.0)
    if np.isfinite(fs) and 0 < rate_cutoff_hz < fs / 2:
        sos = butter(2, rate_cutoff_hz, btype="low", fs=fs, output="sos")
        if n > 3 * (2 * len(sos) + 1):
            rate = sosfiltfilt(sos, rate)
    rate[: vi[0]] = np.nan
    return RollContinuity(unwrapped, rate, uncertain, fs)
