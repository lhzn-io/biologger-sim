# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import logging
import math
from collections import deque
from typing import Any

import numpy as np
from scipy.signal import butter, lfilter, lfilter_zi

from biologger_sim.core.ins import INSSolution
from biologger_sim.core.numeric_utils import safe_float
from biologger_sim.core.processor_interface import BiologgerProcessor
from biologger_sim.functions.depth_smoother import DepthSmoother
from biologger_sim.io.zmq_publisher import ZMQPublisher


class StreamingProcessor(BiologgerProcessor):
    """
    Causal (real-time) streaming processor for digital twin and on-tag simulation.
    """

    def __init__(
        self,
        filt_len: int = 48,
        freq: int = 16,
        debug_level: int = 0,
        locked_attachment_roll_deg: float | None = None,
        locked_attachment_pitch_deg: float | None = None,
        locked_mag_offset_x: float | None = None,
        locked_mag_offset_y: float | None = None,
        locked_mag_offset_z: float | None = None,
        locked_mag_sphere_radius: float | None = None,
        ema_fast_alpha: float = 0.2,
        ema_slow_alpha: float = 0.02,
        ema_cross_threshold: float = 0.5,
        zmq_publisher: ZMQPublisher | None = None,
        eid: int | None = None,
        sim_id: str = "default",
        tag_id: str = "unknown",
        dead_reckoning_speed_model: str = "odba_scaled",
        dead_reckoning_constant_speed: float = 1.0,
        dead_reckoning_odba_factor: float = 2.0,
        highpass_cutoff: float = 0.1,
        **kwargs: Any,
    ) -> None:
        self.filt_len = filt_len
        self.freq = freq
        self.dt = 1.0 / freq
        self.debug_level = debug_level
        self.zmq_publisher = zmq_publisher
        self.eid = eid
        self.sim_id = sim_id
        self.tag_id = tag_id

        self.logger = logging.getLogger(__name__)
        if debug_level > 0:
            self.logger.setLevel(logging.DEBUG)

        self.ema_fast_alpha = ema_fast_alpha
        self.ema_slow_alpha = ema_slow_alpha
        self.ema_cross_threshold = ema_cross_threshold
        self.fast_ema_odba = 0.0
        self.slow_ema_odba = 0.0
        self.logging_state = "STEADY"

        # Locked Calibration
        self.locked_attachment_roll_rad = (
            math.radians(locked_attachment_roll_deg)
            if locked_attachment_roll_deg is not None
            else None
        )
        self.locked_attachment_pitch_rad = (
            math.radians(locked_attachment_pitch_deg)
            if locked_attachment_pitch_deg is not None
            else None
        )

        # Lock mag offset if all values provided, else None
        self.locked_mag_offset: tuple[float, float, float, float] | None = None
        if all(
            x is not None
            for x in [
                locked_mag_offset_x,
                locked_mag_offset_y,
                locked_mag_offset_z,
                locked_mag_sphere_radius,
            ]
        ):
            self.locked_mag_offset = (
                float(locked_mag_offset_x or 0),
                float(locked_mag_offset_y or 0),
                float(locked_mag_offset_z or 0),
                float(locked_mag_sphere_radius or 1),
            )

        self.accel_buffer: deque[tuple[float, float, float]] = deque(maxlen=filt_len)
        self.accel_sum = [0.0, 0.0, 0.0]

        self.gravity = 9.81
        # INSSolution provides full Kalman filter depth estimation (match reference)
        self.ins_solution = INSSolution(sample_rate=freq, biological_constraints=None)
        self.current_time = 0.0  # Accumulated time for INSSolution

        self.dead_reckoning_speed_model = dead_reckoning_speed_model
        self.dead_reckoning_constant_speed = dead_reckoning_constant_speed
        self.dead_reckoning_odba_factor = dead_reckoning_odba_factor

        nyquist = 0.5 * freq
        self.highpass_b, self.highpass_a = butter(2, highpass_cutoff / nyquist, btype="high")
        self.hp_s1 = 0.0
        self.hp_s2 = 0.0
        self.highpass_zi_init = False

        self.record_count = 0
        self.pseudo_x = 0.0
        self.pseudo_y = 0.0
        self.last_timestamp: float | None = None

        self.depth_smoother = DepthSmoother(freq=freq)
        self.logger.info(f"StreamingProcessor initialized: filt_len={filt_len}, freq={freq}Hz")

    def reset(self) -> None:
        self.accel_buffer.clear()
        self.accel_sum = [0.0, 0.0, 0.0]
        self.fast_ema_odba = 0.0
        self.slow_ema_odba = 0.0
        self.record_count = 0
        self.pseudo_x = 0.0
        self.pseudo_y = 0.0
        self.hp_s1 = 0.0
        self.hp_s2 = 0.0
        self.highpass_zi_init = False
        self.ins_solution.reset()
        self.current_time = 0.0

    def process(self, record: dict[str, Any] | Any) -> dict[str, Any]:
        self.record_count += 1

        def get_field(record: dict[str, Any], q: str, u: str) -> float:
            return safe_float(record.get(q, record.get(u, 0.0)))

        # 1. Input Acquisition
        # Data is in 0.1g units
        ax_m = get_field(record, '"int aX"', "int aX")
        ay_m = get_field(record, '"int aY"', "int aY")
        az_m = get_field(record, '"int aZ"', "int aZ")
        if ax_m is None or ay_m is None or az_m is None:
            return {}
        # Ensure data is valid for math operations
        ax_m = float(ax_m)
        ay_m = float(ay_m)
        az_m = float(az_m)
        depth_raw = get_field(record, '"Depth"', "Depth")
        ts = record.get("timestamp", 0.0)

        # 2. Attachment Correction (X then Y)
        if self.locked_attachment_roll_rad is not None:
            assert self.locked_attachment_roll_rad is not None
            assert self.locked_attachment_pitch_rad is not None
            sr_a, cr_a = (
                math.sin(self.locked_attachment_roll_rad),
                math.cos(self.locked_attachment_roll_rad),
            )
            sp_a, cp_a = (
                math.sin(self.locked_attachment_pitch_rad),
                math.cos(self.locked_attachment_pitch_rad),
            )
            # Xb(roll): y' = y*c - z*s, z' = y*s + z*c
            ay_r = ay_m * cr_a - az_m * sr_a
            az_r = ay_m * sr_a + az_m * cr_a
            # Yb(pitch): x' = x*c - z*s, z' = x*s + z*c
            ax_att = ax_m * cp_a - az_r * sp_a
            ay_att = ay_r
            az_att = ax_m * sp_a + az_r * cp_a
        else:
            ax_att, ay_att, az_att = ax_m, ay_m, az_m

        # 3. Window Management (O(1))
        if len(self.accel_buffer) == self.filt_len:
            old = self.accel_buffer[0]
            self.accel_sum[0] -= old[0]
            self.accel_sum[1] -= old[1]
            self.accel_sum[2] -= old[2]

        self.accel_buffer.append((ax_att, ay_att, az_att))
        self.accel_sum[0] += ax_att
        self.accel_sum[1] += ay_att
        self.accel_sum[2] += az_att

        # Dead Reckoning Timing
        actual_dt = self.dt if self.last_timestamp is None else ts - self.last_timestamp
        if actual_dt <= 0:
            actual_dt = self.dt
        self.last_timestamp = ts

        # 4. Gsep & Static Components
        # During warmup: use raw accel as static approximation, 0 for dynamic
        # After warmup: proper Gsep separation
        if len(self.accel_buffer) < self.filt_len:
            # Warmup: use raw acceleration as static estimate (assumes low motion at start)
            static_x, static_y, static_z = ax_att, ay_att, az_att
            # No dynamic separation yet - use 0 (reasonable for deployment start)
            dyn_x, dyn_y, dyn_z = 0.0, 0.0, 0.0
            odba_g = 0.0
        else:
            div = self.filt_len
            static_x, static_y, static_z = (
                self.accel_sum[0] / div,
                self.accel_sum[1] / div,
                self.accel_sum[2] / div,
            )
            dyn_x, dyn_y, dyn_z = ax_att - static_x, ay_att - static_y, az_att - static_z
            odba_g = (abs(dyn_x) + abs(dyn_y) + abs(dyn_z)) / 10.0

        # 5. Orientation (R-style)
        # static_x/y/z are always valid: raw accel during warmup, Gsep-averaged after
        ax_g, ay_g, az_g = static_x / 10.0, static_y / 10.0, static_z / 10.0

        mag_yz = math.sqrt(ay_g**2 + az_g**2)
        pitch_rad = -math.atan2(ax_g, mag_yz)
        roll_rad = math.atan2(ay_g, az_g) if abs(az_g) > 1e-6 or abs(ay_g) > 1e-6 else 0.0
        sp, cp = math.sin(pitch_rad), math.cos(pitch_rad)
        sr, cr = math.sin(roll_rad), math.cos(roll_rad)

        # 6. World-frame vertical acceleration (matching pseudotrack exactly)
        # Rotation: -sin(p)*ax + cos(p)*sin(r)*ay + cos(p)*cos(r)*az
        accel_world_z = -sp * ax_g + cp * sr * ay_g + cp * cr * az_g

        # Remove gravity: For level sensor, accel_world_z ≈ 1.0g, so subtract 1g
        accel_z_no_gravity = accel_world_z * self.gravity - self.gravity

        # 7. High-pass Filter (bias removal)
        # Use lfilter with zi state to support 4th order filter correctly
        # (Manual implementation was truncated to 2nd order)
        if not self.highpass_zi_init:
            # Initialize filter state matching reference
            # Use accel_z_no_gravity for initialization (assumes steady state at start)
            self.highpass_zi = lfilter_zi(self.highpass_b, self.highpass_a) * accel_z_no_gravity
            self.highpass_zi_init = True

        accel_z_filtered_array, self.highpass_zi = lfilter(
            self.highpass_b, self.highpass_a, [accel_z_no_gravity], zi=self.highpass_zi
        )
        accel_z_filtered = accel_z_filtered_array[0]
        # 8. Depth Processing via INSSolution (full Kalman predict+update cycle)
        # Update accumulated time for INSSolution
        self.current_time += actual_dt

        # During warmup (ODBA is NaN), use 0.0 vertical accel to avoid unreliable predictions
        # INS still runs to build up state, just without integrating unreliable acceleration
        if math.isnan(odba_g):
            # Warmup: run INS but don't integrate unreliable vertical acceleration
            accel_world = np.array([0.0, 0.0, 0.0])
        else:
            # Post-warmup: full INS pipeline with filtered vertical acceleration
            accel_world = np.array([0.0, 0.0, accel_z_filtered])

        depth_measurement = depth_raw if not math.isnan(depth_raw) else None
        ins_result = self.ins_solution.update(
            accel_world, depth_measurement, actual_dt, self.current_time
        )
        depth_kalman_filtered = ins_result["depth_kalman_filtered"]

        # Apply multi-scale depth smoothing to KF output
        # Pass ODBA in 0.1g units to match pseudotrack's DepthSmoother thresholds
        odba_01g = abs(dyn_x) + abs(dyn_y) + abs(dyn_z)
        final_depth = self.depth_smoother.update(depth_kalman_filtered, odba_01g)

        # 9. Magnetometer & Heading (R-style)
        heading_deg = float("nan")
        if self.locked_mag_offset is not None:
            # Unpack with explicit None->0.0 fallback for type safety
            ox = self.locked_mag_offset[0] or 0.0
            oy = self.locked_mag_offset[1] or 0.0
            oz = self.locked_mag_offset[2] or 0.0
            orad = self.locked_mag_offset[3] or 1.0  # Avoid div by zero
            mx_val = get_field(record, '"int mX"', "int mX")
            my_val = get_field(record, '"int mY"', "int mY")
            mz_val = get_field(record, '"int mZ"', "int mZ")
            mx_n = (mx_val - ox) / orad
            my_n = (my_val - oy) / orad
            mz_n = (mz_val - oz) / orad

            # Att correction (X then Y)
            roll_att = self.locked_attachment_roll_rad
            pitch_att = self.locked_attachment_pitch_rad
            if roll_att is not None and pitch_att is not None:
                sr_a, cr_a = math.sin(roll_att), math.cos(roll_att)
                sp_a, cp_a = math.sin(pitch_att), math.cos(pitch_att)
                # Xb(roll): y' = y*c - z*s, z' = y*s + z*c
                my_r = my_n * cr_a - mz_n * sr_a
                mz_r = my_n * sr_a + mz_n * cr_a
                # Yb(pitch): x' = x*c - z*s, z' = x*s + z*c
                mx_att_m = mx_n * cp_a - mz_r * sp_a
                my_att_m = my_r
                mz_att_m = mx_n * sp_a + mz_r * cp_a
            else:
                mx_att_m, my_att_m, mz_att_m = mx_n, my_n, mz_n

            # World Rotation (v @ Yb(-p) @ Xb(r))
            # Yb(-p): angle = -p. sin(-p) = -sp.
            # x' = x*c - z*(-s) = x*c + z*s
            # z' = x*(-s) + z*c = -x*s + z*c
            mx_m_p = mx_att_m * cp + mz_att_m * sp
            mz_m_p = -mx_att_m * sp + mz_att_m * cp
            my_m_w = my_att_m * cr - mz_m_p * sr
            mx_m_w = mx_m_p
            heading_deg = math.degrees(math.atan2(-my_m_w, mx_m_w))

        # 10. Dead Reckoning Integration
        speed = (
            max(0.0, odba_g * self.dead_reckoning_odba_factor)
            if self.dead_reckoning_speed_model == "odba_scaled"
            else self.dead_reckoning_constant_speed
        )
        dist = speed * actual_dt
        self.pseudo_x += (
            dist * math.cos(math.radians(heading_deg)) if not math.isnan(heading_deg) else 0.0
        )
        self.pseudo_y += (
            dist * math.sin(math.radians(heading_deg)) if not math.isnan(heading_deg) else 0.0
        )

        # 11. Derived Metrics & Publishing
        vedba_g = math.sqrt(dyn_x**2 + dyn_y**2 + dyn_z**2) / 10.0

        # Helper to sanitize NaN values for ZMQ (extension can't handle NaN in trail rendering)
        def nan_to_zero(x: float) -> float:
            return 0.0 if math.isnan(x) else x

        result = {
            "record_count": self.record_count,
            "timestamp": ts,
            "Depth": nan_to_zero(final_depth),
            "roll_degrees": nan_to_zero(math.degrees(roll_rad)),
            "pitch_degrees": nan_to_zero(math.degrees(pitch_rad)),
            "heading_degrees": nan_to_zero(heading_deg),
            "pseudo_x": self.pseudo_x,
            "pseudo_y": self.pseudo_y,
            "ODBA": nan_to_zero(odba_g),
            "VeDBA": nan_to_zero(vedba_g),
            "velocity": nan_to_zero(speed),
            "vertical_velocity": 0.0,  # TODO: Expose from KF
            "X_Dynamic": nan_to_zero(dyn_x / 10.0),
            "Y_Dynamic": nan_to_zero(dyn_y / 10.0),
            "Z_Dynamic": nan_to_zero(dyn_z / 10.0),
            "X_Static": nan_to_zero(static_x / 10.0),
            "Y_Static": nan_to_zero(static_y / 10.0),
            "Z_Static": nan_to_zero(static_z / 10.0),
        }

        if self.zmq_publisher:
            assert self.eid is not None
            self.zmq_publisher.publish_state(self.eid, self.sim_id, self.tag_id, result)

        return result

    def calibrate_from_batch_data(self) -> None:
        pass

    def get_performance_summary(self) -> dict[str, Any]:
        return {"processor_type": "StreamingProcessor", "records_processed": self.record_count}

    def update_config(self, config_updates: dict[str, Any]) -> None:
        pass

    def get_current_state(self) -> dict[str, Any]:
        return {
            "record_count": self.record_count,
            "X_Track": self.pseudo_x,
            "Y_Track": self.pseudo_y,
        }
