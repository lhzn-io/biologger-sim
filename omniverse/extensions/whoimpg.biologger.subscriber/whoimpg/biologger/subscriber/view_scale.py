# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""View scaling for overviews: vertical exaggeration steps, distance-adaptive trail width, and
the trail's sample averaging and colours.

Plain Python and NumPy, no Kit imports, so it can be unit tested outside Kit.
"""

from __future__ import annotations

import math

import numpy as np

# Vertical exaggeration factors the V / Shift+V keys step through.
EXAGGERATION_STEPS = (1.0, 2.0, 3.0, 5.0, 10.0)
EXAGGERATION_MAX = 20.0

# Adaptive trail width: the tube is this fraction of the camera's distance to the nearest
# trail point (about 4 px across at a 60 degree field of view on a 2560 px viewport), held
# to powers of two times the close-up width so the trail is only re-rendered on a step.
TRAIL_WIDTH_PER_DISTANCE = 0.002
TRAIL_WIDTH_MIN_CM = 5.0
TRAIL_WIDTH_MAX_CM = 10000.0
# A step is taken only once the ideal width is this many powers of two away from the
# current one, so a camera parked near a boundary does not flicker between two widths.
TRAIL_WIDTH_HYSTERESIS = 0.75


def step_exaggeration(current: float, direction: int) -> float:
    """The next exaggeration step up (direction > 0) or down from ``current``."""
    if direction > 0:
        return next((s for s in EXAGGERATION_STEPS if s > current + 1e-6), EXAGGERATION_STEPS[-1])
    return next(
        (s for s in reversed(EXAGGERATION_STEPS) if s < current - 1e-6), EXAGGERATION_STEPS[0]
    )


def adaptive_trail_width_cm(distance_cm: float, current_cm: float) -> float:
    """Trail width for a camera ``distance_cm`` from the nearest trail point.

    Returns ``current_cm`` unchanged unless the ideal width has moved past the hysteresis.
    """
    ideal = min(max(distance_cm * TRAIL_WIDTH_PER_DISTANCE, TRAIL_WIDTH_MIN_CM), TRAIL_WIDTH_MAX_CM)
    if current_cm > 0 and abs(math.log2(ideal / current_cm)) < TRAIL_WIDTH_HYSTERESIS:
        return current_cm
    step = round(math.log2(ideal / TRAIL_WIDTH_MIN_CM))
    return float(min(TRAIL_WIDTH_MIN_CM * 2.0**step, TRAIL_WIDTH_MAX_CM))


def _group_means(
    keys: np.ndarray, ts: np.ndarray, pos: np.ndarray, odba: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Means of consecutive runs of equal ``keys``; each run's time is its middle sample's."""
    if len(keys) == 0:
        return ts, pos, odba
    starts = np.r_[0, np.flatnonzero(np.diff(keys)) + 1]
    counts = np.diff(np.r_[starts, len(keys)])
    return (
        ts[starts + counts // 2],
        np.add.reduceat(pos, starts, axis=0) / counts[:, None],
        np.add.reduceat(odba, starts) / counts,
    )


def smooth_trail(
    ts: np.ndarray, pos: np.ndarray, odba: np.ndarray, window_s: float, width_cm: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Averages trail samples over ``window_s`` record seconds, then over each ``width_cm``
    of track (time ``ts`` (n,), positions ``pos`` (n, 3), ``odba`` (n,)).

    Every sample on its own shows the depth sensor's steps as a saw-tooth (worse under
    vertical exaggeration) and stripes with per-sample ODBA; detail finer than the tube is
    wide only beads its surface. Time windows are aligned to record time, so neighbouring
    segments and re-renders agree. The first and last samples are kept exactly, so segments
    still meet and the trail still ends at the animal.
    """
    if len(ts) < 3:
        return ts, pos, odba
    mid = slice(1, len(ts) - 1)
    t_in, p_in, o_in = ts[mid], pos[mid], odba[mid]
    if window_s > 0:
        t_in, p_in, o_in = _group_means(np.floor(t_in / window_s), t_in, p_in, o_in)
    if width_cm > 0 and len(t_in) > 1:
        travelled = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(p_in, axis=0), axis=1))]
        t_in, p_in, o_in = _group_means(np.floor(travelled / width_cm), t_in, p_in, o_in)
    return (
        np.r_[ts[:1], t_in, ts[-1:]],
        np.vstack([pos[:1], p_in, pos[-1:]]),
        np.r_[odba[:1], o_in, odba[-1:]],
    )


def odba_colors(odba: np.ndarray) -> np.ndarray:
    """Trail colours (n, 3) for ODBA: cyan at rest (0.1), through yellow-green for steady
    swimming, to red for bursts (1.6 and up), brightening and saturating with effort."""
    norm = np.clip((np.asarray(odba, dtype=float) - 0.1) / 1.5, 0.0, 1.0)
    h = (180.0 - 180.0 * norm) / 60.0  # hue sextant, 3 (cyan) down to 0 (red)
    s = 0.8 + 0.2 * norm
    v = 0.7 + 0.3 * norm
    i = np.floor(h).astype(int) % 6
    f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    rgb = np.select(
        [i[:, None] == k for k in range(6)],
        [
            np.stack(c, axis=1)
            for c in ((v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q))
        ],
    )
    return np.asarray(rgb)
