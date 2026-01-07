# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import logging
import math
from collections import deque
from typing import Any

import numpy as np

from biologger_sim.core.numeric_utils import safe_float
from biologger_sim.core.processor_interface import BiologgerProcessor
from biologger_sim.functions.rotation import xb, yb
from biologger_sim.io.zmq_publisher import ZMQPublisher


class StreamingProcessor(BiologgerProcessor):
    """
    Causal (real-time) streaming processor for digital twin and on-tag simulation.

    This processor uses strictly causal filters (looking only at past data) to simulate
    what a tag could compute in real-time. It enables selective logging and
    behavioral response simulation.

    Features:
    - Causal Gsep (Gravity Separation): Uses trailing window mean for static acceleration.
    - Locked Calibration: Uses pre-determined attachment angles and mag offsets.
    - EMA Crossover: Fast/Slow Exponential Moving Average for behavioral state detection.
    - R-Equivalent Pitch/Roll: Uses same geometric formulas as Lab mode but on causal data.

    Comparison to Lab Mode:
    - Lab Mode: Centered filter (looks forward/backward), maximal accuracy, 1.5s delay.
    - Streaming Mode: Causal filter (looks backward only), ~0.5-1° lag, 0 delay.
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
        **kwargs: Any,
    ) -> None:
        """
        Initialize StreamingProcessor.

        Args:
            filt_len: Filter window length (samples).
            freq: Sampling frequency (Hz).
            debug_level: Debug verbosity.
            locked_attachment_roll_deg: Locked attachment roll (degrees).
            locked_attachment_pitch_deg: Locked attachment pitch (degrees).
            locked_mag_offset_x: Locked mag hard-iron X offset.
            locked_mag_offset_y: Locked mag hard-iron Y offset.
            locked_mag_offset_z: Locked mag hard-iron Z offset.
            locked_mag_sphere_radius: Locked mag calibration radius.
            ema_fast_alpha: Alpha for fast EMA (0.0-1.0).
            ema_slow_alpha: Alpha for slow EMA (0.0-1.0).
            ema_cross_threshold: Threhold for crossover signal to trigger state change.
            zmq_publisher: Optional ZMQ publisher for real-time output.
        """
        self.filt_len = filt_len
        self.freq = freq
        self.debug_level = debug_level
        self.zmq_publisher = zmq_publisher

        # EMA Crossover Logic
        self.ema_fast_alpha = ema_fast_alpha
        self.ema_slow_alpha = ema_slow_alpha
        self.ema_cross_threshold = ema_cross_threshold

        # State variables for EMA
        # We track EMA of the "Activity Signal" - typically ODBA or Acceleration Magnitude variance?
        # Roadmap suggests: fast_ema = alpha * raw + ...
        # If the goal is "Inflection Detector" for orientation changes, we might
        # want EMA on Pitch/Roll?
        # Or EMA on specific axis?
        # Roadmap example: "fast_ema = alpha_fast * raw + ..."
        # Let's apply it to a derived "Signal" - for generic behavior change, ODBA is good.
        # But specifically "sudden orientation and acceleration changes".
        # Let's track EMA of ODBA for activity change, and maybe EMA of Pitch?
        # Roadmap v1 section: "Fast/slow EMA crossover (MACD-inspired)..."
        # It doesn't explicitly say WHICH signal.
        # "fast_ema - slow_ema... if abs(signal) > threshold: log_full_resolution()"
        # Let's use ODBA as the primary signal for "Activity State".
        # And we can also track Pitch change.
        # For simplicity in v1, let's implement the EMA on ODBA.
        self.fast_ema_odba = 0.0
        self.slow_ema_odba = 0.0
        self.crossover_signal = 0.0
        self.logging_state = "STEADY"  # STEADY, TRANSITION, RAPID_CHANGE

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

        self.locked_mag_offset = (
            np.array(
                [
                    locked_mag_offset_x,
                    locked_mag_offset_y,
                    locked_mag_offset_z,
                    locked_mag_sphere_radius,
                ]
            )
            if all(
                x is not None
                for x in [
                    locked_mag_offset_x,
                    locked_mag_offset_y,
                    locked_mag_offset_z,
                    locked_mag_sphere_radius,
                ]
            )
            else None
        )

        # Causal Buffers
        self.accel_buffer: deque[tuple[float, float, float]] = deque(maxlen=filt_len)

        # Dead Reckoning State
        self.pseudo_x = 0.0
        self.pseudo_y = 0.0

        self.record_count = 0
        self.logger = logging.getLogger(__name__)
        if debug_level > 0:
            self.logger.setLevel(logging.DEBUG)

        self.logger.info(
            f"StreamingProcessor initialized: filt_len={filt_len}, freq={freq}Hz, "
            f"EMA(fast={ema_fast_alpha}, slow={ema_slow_alpha})"
        )

    def reset(self) -> None:
        """Reset processor state."""
        self.accel_buffer.clear()
        self.fast_ema_odba = 0.0
        self.slow_ema_odba = 0.0
        self.record_count = 0
        self.pseudo_x = 0.0
        self.pseudo_y = 0.0
        self.logger.info("StreamingProcessor reset")

    def get_performance_summary(self) -> dict[str, Any]:
        """Get performance metrics."""
        return {
            "processor_type": "StreamingProcessor",
            "records_processed": self.record_count,
            "buffer_current": len(self.accel_buffer),
        }

    def update_config(self, config_updates: dict[str, Any]) -> None:
        """Update runtime config."""
        if "debug_level" in config_updates:
            self.debug_level = config_updates["debug_level"]
        if "ema_fast_alpha" in config_updates:
            self.ema_fast_alpha = config_updates["ema_fast_alpha"]
        if "ema_slow_alpha" in config_updates:
            self.ema_slow_alpha = config_updates["ema_slow_alpha"]

    def get_current_state(self) -> dict[str, Any]:
        """Get current state."""
        return {
            "record_count": self.record_count,
            "crossover_signal": self.crossover_signal,
            "logging_state": self.logging_state,
            "buffer_fill": len(self.accel_buffer),
        }

    def process(self, data: dict[str, Any] | np.ndarray) -> dict[str, Any]:
        """
        Process a single record.

        Args:
            data: Dictionary containing sensor data.

        Returns:
            Processed record with derived metrics.
        """
        if isinstance(data, np.ndarray):
            raise TypeError("StreamingProcessor expects dict input")

        record = data
        self.record_count += 1

        # 1. Parse Input
        # Helper to get field
        def get_field(rec: dict[str, Any], quoted: str, unquoted: str) -> Any:
            return rec.get(quoted, rec.get(unquoted, "nan"))

        x_accel_raw = safe_float(get_field(record, '"int aX"', "int aX"), "int aX")
        y_accel_raw = safe_float(get_field(record, '"int aY"', "int aY"), "int aY")
        z_accel_raw = safe_float(get_field(record, '"int aZ"', "int aZ"), "int aZ")

        x_mag_raw = safe_float(get_field(record, '"int mX"', "int mX"), "int mX")
        y_mag_raw = safe_float(get_field(record, '"int mY"', "int mY"), "int mY")
        z_mag_raw = safe_float(get_field(record, '"int mZ"', "int mZ"), "int mZ")

        depth_raw = safe_float(get_field(record, '"Depth"', "Depth"), "Depth")

        # 2. Apply Locked Attachment Rotation (if configured)
        # Note: Raw is typically in 0.1g or similar depending on sensor.
        # But `postfacto` uses raw directly?
        # Biologger-pseudotrack used /10.0 for unit conversion.
        # Let's check `postfacto/processor.py` in `biologger-sim`:
        # It takes `x_accel_raw` and passes it to `xb(roll)`.
        # It does NOT divide by 10 before rotation.
        # BUT inside `gsep_streaming` in pseudotrack:
        # `accel_attachment_corrected_01g = accel_attachment_corrected * 10.0`
        # Implies `accel_meas` was in g-units?
        # In `streaming/processor.py` (pseudotrack):
        # `accel_meas = np.array([mapped["X_Accel"] / 10.0 ...])`
        # So raw was 0.1g integer counts? "int aX".
        # Biologger-sim's Lab/PostFacto processor:
        # It does NOT divide by 10 in `process`.
        # Wait, let's verify Lab implementation in `biologger-sim`.
        # Line 617: `x_accel_raw = safe_float(...)`
        # Line 745: `accel_rotated = accel_data @ xb(...)` (Batch results)
        # It seems `Lab` processor assumes inputs are implicitly handled or matched?
        # The key distinction: `StreamingProcessor` in pseudotrack explicitly divided by 10.
        # PostFactoProcessor in biologger-sim/pseudotrack might treat "int aX" as
        # just raw values.
        # However, `gsep` depends on units if we interpret ODBA in g's.
        # If "int aX" is 10 = 1g.
        # I should probably assume the standard convention: Input is raw
        # (likely 0.1g counts or similar).
        # I will preserve the raw values as-is for the "Raw" fields, but convert for
        # calculations if needed.
        # In `lab.py`:
        # `static, dynamic, ... = gsep_batch_circular(accel_rotated, ...)`
        # If `accel_rotated` is in ints, then ODBA is in ints.
        # For consistency with lab.py, I will stick to the same units as input for
        # the main pipeline, unless explicit conversion is required.

        # Rotation
        accel_vec = np.array([x_accel_raw, y_accel_raw, z_accel_raw])
        if (
            self.locked_attachment_roll_rad is not None
            and self.locked_attachment_pitch_rad is not None
        ):
            accel_rotated = xb(self.locked_attachment_roll_rad) @ accel_vec
            accel_rotated = yb(self.locked_attachment_pitch_rad) @ accel_rotated
            x_accel_rot, y_accel_rot, z_accel_rot = accel_rotated
        else:
            x_accel_rot, y_accel_rot, z_accel_rot = x_accel_raw, y_accel_raw, z_accel_raw

        # 3. Causal Gsep (Trailing Moving Average)
        # maintain buffer
        self.accel_buffer.append((x_accel_rot, y_accel_rot, z_accel_rot))

        if len(self.accel_buffer) < 1:
            static_x, static_y, static_z = x_accel_rot, y_accel_rot, z_accel_rot
        else:
            # Mean of buffer (Causal Static Estimate)
            buff_arr = np.array(list(self.accel_buffer))
            static_x = np.mean(buff_arr[:, 0])
            static_y = np.mean(buff_arr[:, 1])
            static_z = np.mean(buff_arr[:, 2])

        dyn_x = x_accel_rot - static_x
        dyn_y = y_accel_rot - static_y
        dyn_z = z_accel_rot - static_z

        odba = abs(dyn_x) + abs(dyn_y) + abs(dyn_z)
        vedba = math.sqrt(dyn_x**2 + dyn_y**2 + dyn_z**2)

        # 4. EMA Crossover Update
        if self.record_count == 1:
            self.fast_ema_odba = odba
            self.slow_ema_odba = odba
        else:
            self.fast_ema_odba = (self.ema_fast_alpha * odba) + (
                (1 - self.ema_fast_alpha) * self.fast_ema_odba
            )
            self.slow_ema_odba = (self.ema_slow_alpha * odba) + (
                (1 - self.ema_slow_alpha) * self.slow_ema_odba
            )

        self.crossover_signal = self.fast_ema_odba - self.slow_ema_odba

        # State Detection
        if self.crossover_signal > (self.ema_cross_threshold * 2):
            self.logging_state = "RAPID_CHANGE"
        elif self.crossover_signal > self.ema_cross_threshold:
            self.logging_state = "TRANSITION"
        elif self.crossover_signal < -self.ema_cross_threshold:
            self.logging_state = "STABILIZING"
        elif abs(self.crossover_signal) < (self.ema_cross_threshold / 2):
            self.logging_state = "STEADY"

        # 5. Orientation (R-equivalent pitchRoll2 on Static)
        # pitch = atan2(-StaticX, sqrt(StaticY^2 + StaticZ^2)) ??
        # Wait, checking lab.py implementation of pitch/roll.
        # lab.py: pitch_deg = -np.degrees(
        #     np.arctan2(static_norm[:,0], np.sqrt(static_norm[:,1]**2 + ...))
        # )
        # Matches R convention.

        # Normalize static
        s_mag = math.sqrt(static_x**2 + static_y**2 + static_z**2)
        if s_mag > 0:
            sx_n, sy_n, sz_n = static_x / s_mag, static_y / s_mag, static_z / s_mag

            pitch_deg = -math.degrees(math.atan2(sx_n, math.sqrt(sy_n**2 + sz_n**2)))
            roll_deg = math.degrees(math.atan2(sy_n, sz_n))
            pitch_rad = math.radians(pitch_deg)
            roll_rad = math.radians(roll_deg)
        else:
            pitch_deg, roll_deg = 0.0, 0.0
            pitch_rad, roll_rad = 0.0, 0.0

        # 6. Magnetometer Processing (if available)
        if (
            self.locked_mag_offset is not None
            and not math.isnan(x_mag_raw)
            and not math.isnan(y_mag_raw)
            and not math.isnan(z_mag_raw)
        ):
            # Unpack offset: [x, y, z, r]
            ox, oy, oz, orad = self.locked_mag_offset

            # Hard Iron Correction
            mx_adj = (x_mag_raw - ox) / orad
            my_adj = (y_mag_raw - oy) / orad
            mz_adj = (z_mag_raw - oz) / orad

            # Rotation
            mag_vec = np.array([mx_adj, my_adj, mz_adj])
            if (
                self.locked_attachment_roll_rad is not None
                and self.locked_attachment_pitch_rad is not None
            ):
                mag_rot = mag_vec @ xb(self.locked_attachment_roll_rad)
                mag_rot = mag_rot @ yb(self.locked_attachment_pitch_rad)
                mx_rot, my_rot, mz_rot = mag_rot
            else:
                mx_rot, my_rot, mz_rot = mx_adj, my_adj, mz_adj

            # Tilt Compensation (Heading)
            # Apply Yb(-pitch) then Xb(roll)
            # Note: pitch_rad here is from R-style which might be negated?
            # Lab.py: used -pitch_rad in Yb.
            # And Lab.py Pitch was -degrees(atan2).
            # So if we used -pitch_rad in Yb, we are using +degrees(atan2).
            # Let's trust Lab.py's implementation pattern.

            # Apply Yb(-pitch_rad) @ Xb(roll_rad)
            # But wait. Lab.py: `m_corr = m_vec @ yb(-p_rad)` then `@ xb(r_rad)`.
            # `p_rad` was `radians(pitch_deg)`.
            # `pitch_deg` was `-degrees(...)`.
            # So `p_rad` is negative. `-p_rad` is positive.

            vec_corr = np.array([mx_rot, my_rot, mz_rot])
            vec_corr = vec_corr @ yb(-pitch_rad)
            vec_corr = vec_corr @ xb(roll_rad)

            mx_corr, my_corr, _ = vec_corr

            heading_deg = math.degrees(math.atan2(-my_corr, mx_corr))
            heading_rad = math.radians(heading_deg)
        else:
            mx_adj, my_adj, mz_adj = float("nan"), float("nan"), float("nan")
            mx_rot, my_rot, mz_rot = float("nan"), float("nan"), float("nan")
            mx_corr, my_corr, _ = float("nan"), float("nan"), float("nan")
            heading_deg, heading_rad = float("nan"), float("nan")

        # 7. Dead Reckoning (Simple 2D approx)
        if not math.isnan(heading_rad):
            speed = 1.0  # m/s assumed
            dt = 1.0 / self.freq
            self.pseudo_x += math.cos(heading_rad) * speed * dt
            self.pseudo_y += math.sin(heading_rad) * speed * dt

        # Output
        output = {
            "record_count": self.record_count,
            "timestamp": 0.0,  # Placeholder
            # Calibration States
            "logging_state": self.logging_state,
            "crossover_signal": self.crossover_signal,
            "ema_fast_odba": self.fast_ema_odba,
            "ema_slow_odba": self.slow_ema_odba,
            # Raw
            "X_Accel_raw": x_accel_raw,
            "Y_Accel_raw": y_accel_raw,
            "Z_Accel_raw": z_accel_raw,
            "X_Mag_raw": x_mag_raw,
            "Y_Mag_raw": y_mag_raw,
            "Z_Mag_raw": z_mag_raw,
            "Depth": depth_raw,
            # Processed Accel
            "X_Accel_rotate": x_accel_rot,
            "Y_Accel_rotate": y_accel_rot,
            "Z_Accel_rotate": z_accel_rot,
            "X_Static": static_x,
            "Y_Static": static_y,
            "Z_Static": static_z,
            "X_Dynamic": dyn_x,
            "Y_Dynamic": dyn_y,
            "Z_Dynamic": dyn_z,
            "ODBA": odba,
            "VeDBA": vedba,
            # Orientation
            "pitch_degrees": pitch_deg,
            "roll_degrees": roll_deg,
            "pitch_radians": pitch_rad,
            "roll_radians": roll_rad,
            # Mag
            "X_Mag_adj": mx_adj,
            "Y_Mag_adj": my_adj,
            "Z_Mag_adj": mz_adj,
            "X_Mag_rotate": mx_rot,
            "Y_Mag_rotate": my_rot,
            "Z_Mag_rotate": mz_rot,
            "heading_degrees": heading_deg,
            "heading_radians": heading_rad,
            # DR
            "pseudo_x": self.pseudo_x,
            "pseudo_y": self.pseudo_y,
        }

        # Publish
        if self.zmq_publisher:
            self.zmq_publisher.publish_state(output)

        return output
