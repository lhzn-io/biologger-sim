# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Horizontal track models and space-time prism geometry.

All positions are (north, east) metres from the deployment origin (the start fix); times are
Unix seconds (UTC). The simulator computes these and publishes the results (see
``ZMQPublisher.publish_meta``), so the Kit viz needs no copy of this code.

Space-time prism: with a start fix at t0, an end fix at t1 and a sustained-speed bound v, the
animal at time t lies within v(t - t0) of the start and within v(t1 - t) of the end. The
reachable set is the intersection (a lens) of those two disks; over the whole deployment the
lenses fill an ellipse with the fixes as foci and major axis v(t1 - t0).
"""

from __future__ import annotations

import logging
import math

import numpy as np

from .georef import GeoReference
from .types import TrackModel

logger = logging.getLogger(__name__)

# Below this net dead-reckoned displacement (m) a pinning rotation is ill-defined.
_MIN_PIN_DISPLACEMENT_M = 1.0


def apply_track_model(
    model: TrackModel,
    t: np.ndarray,
    pseudo_north: np.ndarray,
    pseudo_east: np.ndarray,
    georef: GeoReference | None,
) -> tuple[np.ndarray, np.ndarray, TrackModel]:
    """Places the pseudo track according to ``model``.

    Returns (north, east, model_used). Models that need an end fix fall back to
    DEAD_RECKONING when the deployment has none; ``model_used`` reports what was applied.
    """
    north = np.asarray(pseudo_north, dtype=float)
    east = np.asarray(pseudo_east, dtype=float)
    end_ne = georef.end_ne() if georef is not None else None

    if model == TrackModel.DEAD_RECKONING or georef is None or end_ne is None:
        if model != TrackModel.DEAD_RECKONING:
            logger.warning(
                f"Track model {model.value} needs start and end fixes; using dead reckoning"
            )
        return north, east, TrackModel.DEAD_RECKONING

    assert georef.end is not None
    t = np.asarray(t, dtype=float)
    t0, t1 = georef.start.t, georef.end.t

    if model == TrackModel.FIX_INTERPOLATION:
        frac = np.clip((t - t0) / (t1 - t0), 0.0, 1.0)
        return frac * end_ne[0], frac * end_ne[1], model

    # FIX_PINNED: one complex factor k rotates and scales the dead-reckoned displacement
    # between the fix times onto the fix-to-fix vector.
    k = fix_pinning_factor(t, north, east, georef)
    if k is None:
        logger.warning("Dead-reckoned displacement too small to pin; using fix interpolation")
        return apply_track_model(TrackModel.FIX_INTERPOLATION, t, north, east, georef)
    logger.info(f"Fix pinning: scale {abs(k):.3f}, rotation {math.degrees(np.angle(k)):.1f} deg")
    dr0 = np.interp(t0, t, north) + 1j * np.interp(t0, t, east)
    pinned = k * (north + 1j * east - dr0)
    return pinned.real, pinned.imag, model


def fix_pinning_factor(
    t: np.ndarray, north: np.ndarray, east: np.ndarray, georef: GeoReference
) -> complex | None:
    """The complex factor that maps the dead-reckoned fix-to-fix displacement onto the fixes.

    In the north + i*east plane, its angle is a compass rotation (positive clockwise) and its
    modulus a speed scale. None without an end fix or when the dead-reckoned displacement is
    too small to define a rotation.
    """
    end_ne = georef.end_ne()
    if georef.end is None or end_ne is None:
        return None
    t = np.asarray(t, dtype=float)
    t0, t1 = georef.start.t, georef.end.t
    dr0 = np.interp(t0, t, north) + 1j * np.interp(t0, t, east)
    dr1 = np.interp(t1, t, north) + 1j * np.interp(t1, t, east)
    if abs(dr1 - dr0) < _MIN_PIN_DISPLACEMENT_M:
        return None
    return complex((end_ne[0] + 1j * end_ne[1]) / (dr1 - dr0))


def prism_lens(
    t: float,
    georef: GeoReference,
    v_max: float,
    n_points: int = 72,
) -> list[tuple[float, float]]:
    """Reachable region at time ``t`` as a convex polygon of (north, east) vertices.

    With only a start fix the region is the disk of radius v(t - t0). Returns an empty list
    before the start fix or when the fixes are farther apart than ``v_max`` allows.
    """
    t0 = georef.start.t
    if t < t0:
        return []
    end_ne = georef.end_ne()
    r0 = v_max * (t - t0)
    if georef.end is None or end_ne is None:
        return _circle((0.0, 0.0), r0, n_points)

    r1 = v_max * max(georef.end.t - t, 0.0)
    d = math.hypot(*end_ne)
    if r0 + r1 < d:
        return []  # speed bound inconsistent with the fixes
    if r0 >= d + r1:
        return _circle(end_ne, r1, n_points)  # end disk inside the start disk
    if r1 >= d + r0:
        return _circle((0.0, 0.0), r0, n_points)  # start disk inside the end disk

    # Lens: arc of each circle that lies inside the other, merged and sorted by angle.
    eps = 1e-6 * max(r0, r1, 1.0)
    pts = [p for p in _circle((0.0, 0.0), r0, n_points) if _dist(p, end_ne) <= r1 + eps]
    pts += [p for p in _circle(end_ne, r1, n_points) if math.hypot(*p) <= r0 + eps]
    pts += _circle_intersections((0.0, 0.0), r0, end_ne, r1)
    if len(pts) < 3:
        return []
    cn = sum(p[0] for p in pts) / len(pts)
    ce = sum(p[1] for p in pts) / len(pts)
    return sorted(pts, key=lambda p: math.atan2(p[1] - ce, p[0] - cn))


def prism_bounds(
    georef: GeoReference, v_max: float, t_last: float | None = None
) -> tuple[float, float, float, float]:
    """Axis-aligned bounds (min_n, max_n, min_e, max_e) of the whole-deployment prism.

    With both fixes this is the box around the ellipse with the fixes as foci; with only a
    start fix it is the box around the disk of radius v(t_last - t0).
    """
    end_ne = georef.end_ne()
    if georef.end is None or end_ne is None:
        if t_last is None:
            raise ValueError("t_last is required without an end fix")
        r = v_max * max(t_last - georef.start.t, 0.0)
        return (-r, r, -r, r)

    d = math.hypot(*end_ne)
    a = max(v_max * (georef.end.t - georef.start.t), d) / 2.0
    c = d / 2.0
    b = math.sqrt(max(a * a - c * c, 0.0))
    theta = math.atan2(end_ne[1], end_ne[0])  # angle of the focal axis in (north, east)
    half_n = math.sqrt((a * math.cos(theta)) ** 2 + (b * math.sin(theta)) ** 2)
    half_e = math.sqrt((a * math.sin(theta)) ** 2 + (b * math.cos(theta)) ** 2)
    cn, ce = end_ne[0] / 2.0, end_ne[1] / 2.0
    return (cn - half_n, cn + half_n, ce - half_e, ce + half_e)


def _circle(center: tuple[float, float], r: float, n: int) -> list[tuple[float, float]]:
    if r <= 0:
        return [center] if r == 0 else []
    return [
        (
            center[0] + r * math.cos(2 * math.pi * i / n),
            center[1] + r * math.sin(2 * math.pi * i / n),
        )
        for i in range(n)
    ]


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _circle_intersections(
    c0: tuple[float, float], r0: float, c1: tuple[float, float], r1: float
) -> list[tuple[float, float]]:
    """The two crossing points of circles that properly intersect (the lens corners)."""
    d = _dist(c0, c1)
    if d == 0 or d > r0 + r1 or d < abs(r0 - r1):
        return []
    a = (r0 * r0 - r1 * r1 + d * d) / (2 * d)
    h = math.sqrt(max(r0 * r0 - a * a, 0.0))
    un, ue = (c1[0] - c0[0]) / d, (c1[1] - c0[1]) / d
    pn, pe = c0[0] + a * un, c0[1] + a * ue
    return [(pn - h * ue, pe + h * un), (pn + h * ue, pe - h * un)]
