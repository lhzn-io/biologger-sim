# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import logging
import math


class DepthSmoother:
    """
    Multi-scale EMA depth smoothing for reducing high-frequency variance while preserving accuracy.
    Implements adaptive blending of multiple EMA filters with different time constants:
    - Fast EMA (2-3 second response): Captures rapid depth changes during active periods
    - Medium EMA (10-15 second response): Balanced response for general smoothing
    - Slow EMA (30-60 second response): Provides stability during low-activity periods

    Adaptive blending ratios based on ODBA.
    """

    def __init__(
        self,
        freq: int = 16,
        low_activity_threshold: float = 0.15,
        high_activity_threshold: float = 0.20,
        debug_level: int = 0,
    ):
        self.freq = freq
        self.low_activity_threshold = low_activity_threshold
        self.high_activity_threshold = high_activity_threshold
        self.debug_level = debug_level

        self.alpha_fast = 2.0 / (freq * 3 + 1)
        self.alpha_medium = 2.0 / (freq * 12 + 1)
        self.alpha_slow = 2.0 / (freq * 45 + 1)

        self.depth_ema_fast: float | None = None
        self.depth_ema_medium: float | None = None
        self.depth_ema_slow: float | None = None

        self.last_weights = (0.0, 0.3, 0.7)
        self.logger = logging.getLogger(__name__)

    def update(self, depth_estimate: float, odba: float) -> float:
        """
        Update smoothing with new depth estimate and activity level.
        """
        if not math.isfinite(depth_estimate):
            return depth_estimate

        if (
            self.depth_ema_fast is None
            or self.depth_ema_medium is None
            or self.depth_ema_slow is None
        ):
            self.depth_ema_fast = depth_estimate
            self.depth_ema_medium = depth_estimate
            self.depth_ema_slow = depth_estimate
            return depth_estimate

        # Static analysis hints: these cannot be None anymore
        assert self.depth_ema_fast is not None
        assert self.depth_ema_medium is not None
        assert self.depth_ema_slow is not None

        # Update EMAs
        self.depth_ema_fast = (self.alpha_fast * depth_estimate) + (
            1 - self.alpha_fast
        ) * self.depth_ema_fast
        self.depth_ema_medium = (self.alpha_medium * depth_estimate) + (
            1 - self.alpha_medium
        ) * self.depth_ema_medium
        self.depth_ema_slow = (self.alpha_slow * depth_estimate) + (
            1 - self.alpha_slow
        ) * self.depth_ema_slow

        # Calculate weights based on activity (ODBA)
        if math.isfinite(odba):
            if odba <= self.low_activity_threshold:
                w = 0.0
            elif odba >= self.high_activity_threshold:
                w = 1.0
            else:
                w = (odba - self.low_activity_threshold) / (
                    self.high_activity_threshold - self.low_activity_threshold
                )

            w = max(0.0, min(1.0, w))

            # Adaptive blending
            fast = 0.4 * w
            medium = 0.3 * (1.0 - w) + 0.6 * w
            slow = 0.7 * (1.0 - w)
            weights = (fast, medium, slow)
            self.last_weights = weights
        else:
            weights = self.last_weights

        final_depth = (
            weights[0] * self.depth_ema_fast
            + weights[1] * self.depth_ema_medium
            + weights[2] * self.depth_ema_slow
        )

        return final_depth
