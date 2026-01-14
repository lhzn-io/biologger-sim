# Copyright (c) 2025 Daniel Fry
# MIT License. See LICENSE file in the project root for full license text.

"""
Shared INS (Inertial Navigation System) module for biologger data.

Ported from biologger-pseudotrack to achieve exact depth parity with R baseline.

This module provides reusable INS capabilities including:
- Kalman filtering for depth/velocity fusion
- Vertical velocity estimation via acceleration integration
- Optional biological constraint enforcement (velocity/acceleration limits)
- State persistence across algorithm transitions

Biological constraints can be disabled by passing None (R-style streaming).
"""

import logging
import math
from typing import Any

import numpy as np

from biologger_sim.functions.kalman_filter import KalmanFilter


class VelocityEstimator:
    """Kalman filter wrapper for vertical velocity estimation."""

    def __init__(
        self,
        process_noise_depth: float = 1e-4,
        process_noise_velocity: float = 1e-3,
        measurement_noise: float = 0.02,
    ):
        """
        Initialize velocity estimator.

        Args:
            process_noise_depth: Process noise for depth state
            process_noise_velocity: Process noise for velocity state
            measurement_noise: Measurement noise for depth observations
        """
        self.process_noise_depth = process_noise_depth
        self.process_noise_velocity = process_noise_velocity
        self.measurement_noise = measurement_noise
        self.kalman_filter: KalmanFilter | None = None
        self.logger = logging.getLogger(__name__)

    def initialize(self, initial_depth: float) -> None:
        """
        Initialize Kalman filter with first depth measurement.

        Args:
            initial_depth: Initial depth value for filter initialization
        """
        self.kalman_filter = KalmanFilter(
            process_noise_depth=self.process_noise_depth,
            process_noise_velocity=self.process_noise_velocity,
            measurement_noise=self.measurement_noise,
            initial_depth=initial_depth,
        )

    def predict(self, dt: float, vertical_acceleration: float) -> None:
        """
        Prediction step of Kalman filter.

        Args:
            dt: Time step in seconds
            vertical_acceleration: Filtered vertical acceleration in m/s²
        """
        if self.kalman_filter is not None:
            self.kalman_filter.predict(dt, vertical_acceleration)

    def update(self, depth_measurement: float) -> None:
        """
        Update step of Kalman filter with depth measurement.

        Args:
            depth_measurement: Measured depth value
        """
        if self.kalman_filter is not None:
            self.kalman_filter.update(depth_measurement)

    def get_velocity(self) -> float:
        """
        Get current velocity estimate.

        Returns:
            Estimated vertical velocity in m/s
        """
        if self.kalman_filter is not None:
            return self.kalman_filter.get_velocity()
        return 0.0

    def get_depth(self) -> float:
        """
        Get current depth estimate.

        Returns:
            Estimated depth in meters
        """
        if self.kalman_filter is not None:
            return self.kalman_filter.get_depth()
        return 0.0

    def apply_biological_constraints(self, max_velocity: float) -> None:
        """
        Apply biological constraints to velocity estimate.

        Args:
            max_velocity: Maximum biologically plausible velocity (m/s)
        """
        if self.kalman_filter is not None:
            current_velocity = self.kalman_filter.get_velocity()
            if abs(current_velocity) > max_velocity:
                constrained_velocity = float(np.sign(current_velocity)) * max_velocity
                # Update the Kalman filter state directly
                self.kalman_filter.x1 = constrained_velocity

    def is_initialized(self) -> bool:
        """
        Check if the velocity estimator is initialized.

        Returns:
            True if Kalman filter is initialized
        """
        return self.kalman_filter is not None

    def reset(self) -> None:
        """Reset velocity estimator to initial state."""
        self.kalman_filter = None


class INSSolution:
    """6-DOF INS solution with Kalman filtering for depth estimation."""

    def __init__(
        self,
        sample_rate: float,
        biological_constraints: dict[str, float] | None = None,
    ):
        """
        Initialize INS solution.

        Args:
            sample_rate: Data sampling rate in Hz
            biological_constraints: Dict with 'max_velocity' and 'max_acceleration' keys.
                                   Set to None to disable constraints (R-style streaming).
        """
        self.sample_rate = sample_rate
        self.max_velocity = (
            biological_constraints.get("max_velocity", 3.0) if biological_constraints else None
        )
        self.max_acceleration = (
            biological_constraints.get("max_acceleration", 2.0) if biological_constraints else None
        )

        # Velocity estimator using Kalman filtering
        self.velocity_estimator = VelocityEstimator()

        # Simple velocity integration state
        self.vertical_velocity = 0.0

        # Depth tracking state
        self.last_depth_measurement: float | None = None
        self.last_depth_time: float | None = None
        self.last_kf_depth_used: float | None = None
        self.last_kf_update_time: float | None = None

        # Position state (for future extensions)
        self.position = np.array([0.0, 0.0, 0.0])  # [x, y, depth]

    def update(
        self,
        accel_world: np.ndarray,
        depth_measurement: float | None,
        dt: float,
        current_time: float,
    ) -> dict[str, Any]:
        """
        Update INS solution with new measurements.

        Args:
            accel_world: World-frame acceleration [ax, ay, az] in m/s²
            depth_measurement: Depth measurement in meters, None if not available
            dt: Time step since last update in seconds
            current_time: Current timestamp

        Returns:
            Dictionary with updated state estimates
        """
        # Extract vertical acceleration (Z component in world frame)
        accel_z_world = float(accel_world[2])

        # Apply biological constraints to acceleration (if enabled)
        if self.max_acceleration is not None and abs(accel_z_world) > self.max_acceleration:
            accel_z_world = float(np.sign(accel_z_world)) * self.max_acceleration

        # Step 1: Simple velocity integration
        self.vertical_velocity += accel_z_world * dt

        depth_val: float | None = None
        if depth_measurement is not None and math.isfinite(depth_measurement):
            depth_val = depth_measurement

            # Zero velocity estimate at each depth reading (as prescribed)
            # Only zero if depth changed significantly or enough time passed
            if self.last_depth_measurement is not None and (
                abs(depth_val - self.last_depth_measurement) > 0.1
                or (self.last_depth_time is not None and current_time - self.last_depth_time > 1.0)
            ):
                self.vertical_velocity = 0.0

            self.last_depth_measurement = depth_val
            self.last_depth_time = current_time

        # Step 3: Kalman filter for depth estimation
        if not self.velocity_estimator.is_initialized() and depth_val is not None:
            # Initialize Kalman filter with first depth measurement
            self.velocity_estimator.initialize(depth_val)

        if self.velocity_estimator.is_initialized():
            # Prediction step
            self.velocity_estimator.predict(dt, accel_z_world)

            # Update step (only at ~1Hz or when depth value changes materially)
            if depth_val is not None:
                should_update = False
                if (
                    self.last_kf_update_time is None
                    or (current_time - self.last_kf_update_time) >= 0.9
                ):
                    should_update = True

                last_used = self.last_kf_depth_used
                if last_used is None or abs(depth_val - last_used) > 1e-6:
                    should_update = True

                if should_update:
                    self.velocity_estimator.update(depth_val)
                    self.last_kf_depth_used = depth_val
                    self.last_kf_update_time = current_time

            # Get Kalman filter estimates
            depth_kalman_filtered = self.velocity_estimator.get_depth()
            velocity_kalman_estimate = self.velocity_estimator.get_velocity()

            # Apply biological constraints (if enabled)
            if self.max_velocity is not None:
                self.velocity_estimator.apply_biological_constraints(self.max_velocity)
                velocity_kalman_estimate = self.velocity_estimator.get_velocity()

        else:
            depth_kalman_filtered = depth_val if depth_val is not None else float("nan")
            velocity_kalman_estimate = self.vertical_velocity

        # Apply biological constraints to simple velocity integration (if enabled)
        if self.max_velocity is not None and abs(self.vertical_velocity) > self.max_velocity:
            self.vertical_velocity = float(np.sign(self.vertical_velocity)) * self.max_velocity

        return {
            "depth_kalman_filtered": depth_kalman_filtered,
            "velocity_estimate": velocity_kalman_estimate,
            "vertical_velocity": self.vertical_velocity,
            "position": self.position.copy(),
            "kalman_initialized": self.velocity_estimator.is_initialized(),
        }

    def get_velocity_estimate(self) -> tuple[float, float, float]:
        """
        Get current velocity estimate.

        Returns:
            Tuple of (vx, vy, vz) velocity components in m/s
        """
        # For now, only vertical velocity is estimated
        if self.velocity_estimator.is_initialized():
            vz = self.velocity_estimator.get_velocity()
        else:
            vz = self.vertical_velocity

        return (0.0, 0.0, vz)

    def get_position_estimate(self) -> tuple[float, float, float]:
        """
        Get current position estimate.

        Returns:
            Tuple of (x, y, z) position components
        """
        if self.velocity_estimator.is_initialized():
            depth = self.velocity_estimator.get_depth()
            return (self.position[0], self.position[1], depth)
        else:
            return (self.position[0], self.position[1], self.position[2])

    def get_state(self) -> dict[str, Any]:
        """
        Get current INS state information.

        Returns:
            Dictionary with complete state information
        """
        velocity = self.get_velocity_estimate()
        position = self.get_position_estimate()

        return {
            "velocity": velocity,
            "position": position,
            "vertical_velocity": self.vertical_velocity,
            "kalman_initialized": self.velocity_estimator.is_initialized(),
            "last_depth_measurement": self.last_depth_measurement,
            "last_depth_time": self.last_depth_time,
            "biological_constraints": {
                "max_velocity": self.max_velocity,
                "max_acceleration": self.max_acceleration,
            },
        }

    def reset(self) -> None:
        """Reset INS solution to initial state."""
        self.velocity_estimator.reset()
        self.vertical_velocity = 0.0
        self.position.fill(0.0)
        self.last_depth_measurement = None
        self.last_depth_time = None
        self.last_kf_depth_used = None
        self.last_kf_update_time = None
