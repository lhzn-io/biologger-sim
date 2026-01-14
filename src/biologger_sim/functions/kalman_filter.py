# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.


class KalmanFilter:
    """
    Simple Kalman filter for depth estimation.

    State vector: [depth, vertical_velocity]
    Observation: depth (typically lower frequency than acceleration)
    """

    def __init__(
        self,
        process_noise_depth: float = 1e-4,
        process_noise_velocity: float = 1e-3,
        measurement_noise: float = 0.02,
        initial_depth: float = 0.0,
    ):
        # State: [depth, vertical_velocity]
        self.x0 = initial_depth
        self.x1 = 0.0

        # Covariance P: [[p00, p01], [p10, p11]]
        self.p00 = 10.0
        self.p01 = 0.0
        self.p11 = 10.0

        # Process noise Q (assume diagonal)
        self.q00 = process_noise_depth
        self.q11 = process_noise_velocity

        # Measurement noise R
        self.r = measurement_noise

    def predict(self, dt: float, accel_z_filtered: float) -> None:
        """Prediction step (optimized scalar math)."""
        # x = F*x + B*u
        self.x0 = self.x0 + self.x1 * dt + 0.5 * dt**2 * accel_z_filtered
        self.x1 = self.x1 + dt * accel_z_filtered

        # P = F*P*F' + Q
        # F = [[1, dt], [0, 1]]
        # F*P = [[p00 + p01*dt, p01 + p11*dt], [p01, p11]] (since p10=p01)
        # F*P*F' = [[p00 + 2*p01*dt + p11*dt**2, p01 + p11*dt], [p01 + p11*dt, p11]]
        self.p00 = self.p00 + 2.0 * self.p01 * dt + self.p11 * dt**2 + self.q00
        self.p01 = self.p01 + self.p11 * dt
        # self.p11 is unchanged by state transition, only gets process noise
        self.p11 = self.p11 + self.q11

    def update(self, depth_measurement: float) -> None:
        """Update step (optimized scalar math)."""
        # H = [[1, 0]], so y = z - x0
        y = depth_measurement - self.x0

        # S = H*P*H' + R = p00 + r
        s = self.p00 + self.r

        # K = P*H' * inv(S) = [[p00], [p01]] / s
        k0 = self.p00 / s
        k1 = self.p01 / s

        # x = x + K*y
        self.x0 = self.x0 + k0 * y
        self.x1 = self.x1 + k1 * y

        # P = (I - K*H) * P
        # I - K*H = [[1-k0, 0], [-k1, 1]]
        # New P = [[(1-k0)*p00, (1-k0)*p01], [-k1*p00 + p01, -k1*p01 + p11]]
        self.p00 = (1.0 - k0) * self.p00
        self.p01 = (1.0 - k0) * self.p01
        self.p11 = -k1 * self.p01 + self.p11

    def get_depth(self) -> float:
        return float(self.x0)

    def get_velocity(self) -> float:
        return float(self.x1)
