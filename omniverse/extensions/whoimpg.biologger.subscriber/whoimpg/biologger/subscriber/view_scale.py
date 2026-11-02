# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""View scaling for overviews: vertical exaggeration steps and distance-adaptive trail width.

Plain Python, no Kit imports, so it can be unit tested outside Kit.
"""

from __future__ import annotations

import math

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
