# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from typing import Any, cast

import numpy as np
from numpy.typing import NDArray


def running_mean_circular(x: NDArray[np.float64], window: int) -> NDArray[np.float64]:
    """
    Mimics R's stats::filter(x, rep(1, window)/window, sides=2, circular=TRUE)
    - Centered running mean (even window: center left)
    - Circular (wrap) padding
    - Output is same length as input
    """
    n = len(x)
    w = window
    # For even window, R centers left: offset = -(w//2 - 1)
    offset = 0 if w % 2 == 1 else -(w // 2 - 1)
    # Build indices for each output position
    idxs = (np.arange(n)[:, None] + np.arange(offset, offset + w)) % n
    return cast(NDArray[np.float64], np.mean(x[idxs], axis=1))


def gsep(
    accel: NDArray[np.float64], filt_len: int, debug: int = 0, logger: Any | None = None
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """
    Separates acceleration data into static (gravitational) and dynamic (movement) components.
    Uses a centered running mean with circular (wrap) padding to match R's
    filter(sides=2, circular=TRUE).
    Returns static, dynamic, and ODBA (overall dynamic body acceleration) as in the
    R implementation.
    debug: 0 (off), 1 (basic), 2 (detailed)
    logger: optional, for debug output
    """
    static = np.empty_like(accel, dtype=np.float64)
    for i in range(accel.shape[1]):
        static[:, i] = running_mean_circular(accel[:, i], filt_len)
        if logger is not None and debug >= 2:
            logger.debug(f"Gsep: static col {i} preview: {static[:10, i]}")
    dynamic = accel - static
    odba = np.abs(dynamic).sum(axis=1)
    if logger is not None and debug >= 2:
        logger.debug(f"Gsep: dynamic preview: {dynamic[:10, :]}")
        logger.debug(f"Gsep: ODBA preview: {odba[:10]}")
    return static, dynamic, odba
