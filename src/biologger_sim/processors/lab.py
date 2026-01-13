# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.
#
# PostFactoProcessor - R-Compatible Post-Hoc Biologger Analysis
# ==============================================================
#
# Non-causal processor for post-facto biologger data analysis.
# Achieves perfect R tie-out (<0.1° error target) through R-compatible filtering.
#
# Key Differences from StreamingProcessor:
#   - NON-CAUSAL: Uses centered filter (R's filter(sides=2, circular=TRUE))
#     instead of lfilter (causal)
#   - R-COMPATIBLE: Exact match with gRumble R package for scientific validation
#   - FIXED MEMORY: Streaming architecture with fixed buffer size (not in-memory batch)
#   - POST-HOC: Analysis after data collection complete, not real-time
#
# Processing Architecture:
#   1. Buffering: Maintains filt_len sample window for centered filter
#   2. Gsep: R-style centered filter (sides=2, circular=TRUE) for static/dynamic separation
#   3. Orientation: R-style pitchRoll2 from static acceleration
#   4. Output: Same schema as StreamingProcessor for drop-in compatibility
#
# For complete architecture documentation, see:
#   biologger_pseudotrack/postfacto/README.md (TODO)

import logging
import math
from collections import deque
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray

from biologger_sim.core.numeric_utils import safe_float
from biologger_sim.core.processor_interface import BiologgerProcessor
from biologger_sim.core.types import ClockSource, DepthAlgorithm, DepthConfig
from biologger_sim.functions.filters import gsep_batch_circular, gsep_streaming
from biologger_sim.functions.rotation import xb, yb
from biologger_sim.io.zmq_publisher import ZMQPublisher


class PostFactoProcessor(BiologgerProcessor):
    """
    Post-facto (non-causal) biologger processor for R-compatibility.

    This processor uses R's centered moving average filter (filter(sides=2, circular=TRUE))
    to achieve exact tie-out with the gRumble R package. Unlike StreamingProcessor which uses
    causal lfilter (trailing window), this uses a centered window looking both forward and
    backward in time, which is only possible for post-hoc analysis.

    Memory Footprint:
        - Fixed size: O(filt_len) samples (48 samples @ 16Hz for 3s window)
        - Independent of dataset size (unlike batch/ which loads all data)

    Validation Target:
        - <0.1° error vs R (pitch, roll, heading)
        - Exact ODBA/VeDBA match
    """

    def __init__(
        self,
        filt_len: int = 48,
        freq: int = 16,
        debug_level: int = 0,
        r_exact_mode: bool = False,
        compute_attachment_angles: bool = True,
        locked_attachment_roll_deg: float | None = None,
        locked_attachment_pitch_deg: float | None = None,
        compute_mag_offsets: bool = True,
        locked_mag_offset_x: float | None = None,
        locked_mag_offset_y: float | None = None,
        locked_mag_offset_z: float | None = None,
        locked_mag_sphere_radius: float | None = None,
        depth_cfg: DepthConfig | None = None,
        zmq_publisher: ZMQPublisher | None = None,
        eid: int | None = None,
        sim_id: str | None = None,
        tag_id: str = "unknown",
        clock_source: ClockSource = ClockSource.FIXED_FREQ,
        **kwargs: Any,
    ) -> None:
        """
        Initialize PostFactoProcessor.

        Args:
            filt_len (int): Filter window length in samples (default 48 = 3s @ 16Hz)
            freq (int): Sampling frequency in Hz (default 16Hz)
            debug_level (int): Debug verbosity (0=off, 1=basic, 2=detailed)
            r_exact_mode (bool): Enable full R-exact compatibility (batch calibration
                from full dataset)
            compute_attachment_angles (bool): Compute attachment angles from data (True)
                or use locked values (False)
            locked_attachment_roll_deg (float): Pre-computed attachment roll angle
                (degrees)
            locked_attachment_pitch_deg (float): Pre-computed attachment pitch angle
            compute_mag_offsets (bool): Compute magnetometer offsets from data (True)
                or use locked values (False)
            locked_mag_offset_x (float): Pre-computed mag X-axis hard iron offset
            locked_mag_offset_y (float): Pre-computed mag Y-axis hard iron offset
            locked_mag_offset_z (float): Pre-computed mag Z-axis hard iron offset
            locked_mag_sphere_radius (float): Pre-computed mag calibration sphere radius
            depth_cfg (DepthConfig | None): Depth estimation configuration
            zmq_publisher (ZMQPublisher | None): Optional ZMQ publisher for real-time viz
            eid (int | None): Entity identifier for ZMQ publishing
            sim_id (str | None): Simulation view name for ZMQ publishing
            clock_source (ClockSource): Time step source for integration
                (FIXED_FREQ or SENSOR_TIME).
            **kwargs: Additional parameters (for compatibility)
        """
        self.filt_len = filt_len
        self.freq = freq
        self.debug_level = debug_level
        self.r_exact_mode = r_exact_mode
        self.clock_source = clock_source
        self.true_integration = clock_source == ClockSource.SENSOR_TIME
        self.compute_attachment_angles = compute_attachment_angles
        self.compute_mag_offsets = compute_mag_offsets

        # Handle Depth Configuration
        if depth_cfg is None:
            depth_cfg = DepthConfig()

        # Derive interpolation flag from algorithm choice
        # Used for buffer initialization below
        enable_depth_interpolation = depth_cfg.algorithm == DepthAlgorithm.ACAUSAL_INTERP
        self.enable_depth_interpolation = enable_depth_interpolation

        self.zmq_publisher = zmq_publisher
        self.eid = eid
        self.sim_id = sim_id
        self.tag_id = tag_id

        # Locked calibration parameters (for streaming mode)
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

        # Computed calibration parameters (set during batch processing)
        self.computed_attachment_roll_rad: float | None = None
        self.computed_attachment_pitch_rad: float | None = None
        self.computed_mag_offset: NDArray[np.float64] | None = None

        # Circular buffer for R-style centered filter (needs filt_len samples)
        self.accel_buffer: deque[tuple[float, float, float]] = deque(maxlen=filt_len)
        self.mag_buffer: deque[tuple[float, float, float]] | None = (
            deque(maxlen=filt_len)
            if compute_mag_offsets or self.locked_mag_offset is not None
            else None
        )
        self.depth_buffer: deque[float] | None = deque() if enable_depth_interpolation else None

        # Record buffer for delayed processing (to align with centered filter output)
        # The centered filter introduces a delay of filt_len // 2 samples
        # We need to buffer the original records to emit them with the correct filtered values
        self.record_buffer: deque[dict[str, Any]] = deque(maxlen=filt_len)

        # Batch calibration data storage (only used in r_exact_mode)
        self.batch_accel_data: list[list[float]] | None = [] if r_exact_mode else None
        self.batch_mag_data: list[list[float]] | None = [] if r_exact_mode else None
        self.batch_depth_data: list[float] | None = (
            [] if r_exact_mode and enable_depth_interpolation else None
        )
        self.batch_velocity_data: list[float] | None = [] if r_exact_mode else None
        self.batch_timestamps: list[float] | None = [] if r_exact_mode else None
        self.batch_results: dict[str, Any] | None = None  # Store pre-computed results for Pass 2
        self.calibration_complete = False

        # Record counter
        self.record_count = 0
        self.valid_record_indices: set[int] = set()
        self.processing_idx = 0

        # Dead Reckoning State
        self.pseudo_x = 0.0
        self.pseudo_y = 0.0

        # Sub-second Interpolation State
        self.last_ts = -1.0
        self.sub_sec_idx = 0

        # Logger
        self.logger = logging.getLogger(__name__)
        if debug_level > 0:
            self.logger.setLevel(logging.DEBUG)

        self.logger.info(
            f"PostFactoProcessor initialized: filt_len={filt_len}, freq={freq}Hz, "
            f"r_exact_mode={r_exact_mode}, clock_source={clock_source}, "
            f"compute_attachment_angles={compute_attachment_angles}, "
            f"compute_mag_offsets={compute_mag_offsets}, "
            f"enable_depth_interpolation={enable_depth_interpolation}"
        )

    def _compute_attachment_angles_batch(self) -> None:
        """
        Compute attachment angles from full dataset using R-style colMeans approach.

        This implements the two-step rotation correction from
        swordRED_pseudotrack-clean.R (lines 135-147):
        1. Calculate roll from mean Y/Z components
        2. Apply Xb(roll) rotation, recalculate mean
        3. Calculate pitch from rotated mean X/Z components
        """
        if not self.batch_accel_data:
            self.logger.warning(
                "No batch acceleration data collected for attachment angle computation"
            )
            return

        # Convert list of [x, y, z] to numpy array
        accel_array = np.array(self.batch_accel_data)

        # Step 1: Calculate mean acceleration (R's colMeans)
        pos_mean = accel_array.mean(axis=0)

        # Step 2: Calculate roll from Y/Z components
        roll = np.arctan2(pos_mean[1], pos_mean[2])

        if self.debug_level >= 1:
            self.logger.debug(f"Batch calibration - posMean_Accel: {np.round(pos_mean, 3)}")
            self.logger.debug(f"Batch calibration - roll: {roll:.6f} rad ({np.degrees(roll):.2f}°)")

        # Step 3: Rotate accelerometer data by roll (R's %*% Xb(roll))
        accel_rotated = accel_array @ xb(roll)

        # Step 4: Recalculate mean from rotated data
        pos_mean2 = accel_rotated.mean(axis=0)

        if self.debug_level >= 1:
            self.logger.debug(f"Batch calibration - posMean_AccelR: {np.round(pos_mean2, 3)}")

        # Step 5: Calculate pitch from rotated X/Z components
        pitch = np.arctan(pos_mean2[0] / pos_mean2[2])

        if self.debug_level >= 1:
            self.logger.debug(
                f"Batch calibration - pitch: {pitch:.6f} rad ({np.degrees(pitch):.2f}°)"
            )

        # Store computed values
        self.computed_attachment_roll_rad = roll
        self.computed_attachment_pitch_rad = pitch

        self.logger.info(
            f"Computed attachment angles: roll={np.degrees(roll):.3f}°, "
            f"pitch={np.degrees(pitch):.3f}°"
        )

    def _compute_mag_offset_batch(self) -> None:
        """
        Compute magnetometer hard iron offsets from full dataset using R's MagOffset function.

        This implements MagOffset from swordRED_pseudotrack-clean.R (lines 21-33):
        Hard iron calibration using least squares to find sphere center and radius.
        """
        if not self.batch_mag_data:
            self.logger.warning("No batch magnetometer data collected for offset computation")
            return

        # Convert list of [x, y, z] to numpy array
        mag_array = np.array(self.batch_mag_data)

        # R's MagOffset function:
        # A = cbind(Mag[,1]*2, Mag[,2]*2, Mag[,3]*2, 1)
        # f = matrix(Mag[,1]^2 + Mag[,2]^2 + Mag[,3]^2, ncol=1)
        # C = solve(crossprod(A), crossprod(A, f))
        # rad = sqrt((C[1]^2 + C[2]^2 + C[3]^2) + C[4])

        a_mat = np.column_stack(
            [
                mag_array[:, 0] * 2,
                mag_array[:, 1] * 2,
                mag_array[:, 2] * 2,
                np.ones(len(mag_array)),
            ]
        )
        f = (mag_array[:, 0] ** 2 + mag_array[:, 1] ** 2 + mag_array[:, 2] ** 2).reshape(-1, 1)

        # Solve: C = (A^T A)^-1 (A^T f)
        c_vec = np.linalg.solve(a_mat.T @ a_mat, a_mat.T @ f).flatten()

        # Calculate sphere radius
        rad = np.sqrt(c_vec[0] ** 2 + c_vec[1] ** 2 + c_vec[2] ** 2 + c_vec[3])

        # Store as [offset_x, offset_y, offset_z, radius]
        self.computed_mag_offset = np.array([c_vec[0], c_vec[1], c_vec[2], rad])

        if self.debug_level >= 1:
            self.logger.debug(
                f"Batch calibration - MagOffset: {np.round(self.computed_mag_offset, 3)}"
            )

        self.logger.info(
            f"Computed mag offsets: x={c_vec[0]:.3f}, y={c_vec[1]:.3f}, "
            f"z={c_vec[2]:.3f}, radius={rad:.3f}"
        )

    def calibrate_from_batch_data(self) -> None:
        """
        Perform batch calibration from collected data.

        This should be called after the first pass through the dataset in r_exact_mode.
        Computes attachment angles and magnetometer offsets from full dataset.
        """
        if not self.r_exact_mode:
            self.logger.warning("calibrate_from_batch_data called but r_exact_mode is False")
            return

        self.logger.info("Starting batch calibration from full dataset...")

        # Compute attachment angles if requested
        if self.compute_attachment_angles and self.batch_accel_data:
            self._compute_attachment_angles_batch()

        # Compute magnetometer offsets if requested
        if self.compute_mag_offsets and self.batch_mag_data:
            self._compute_mag_offset_batch()

        # Pre-compute all results for Pass 2
        self._process_batch_data()

        self.calibration_complete = True
        self.logger.info("Batch calibration complete")

    def _process_batch_data(self) -> None:
        """
        Process the entire batch of data using R-exact methods (circular filtering).
        Populates self.batch_results.
        """
        if not self.batch_accel_data:
            return

        self.logger.info("Processing full batch with circular Gsep...")
        accel_data = np.array(self.batch_accel_data)

        # Get attachment angles
        att_roll, att_pitch = self._get_attachment_angles()

        # Rotate accelerometer data
        if att_roll is not None and att_pitch is not None:
            # Apply Xb(roll) then Yb(pitch) rotation (R-style: Data %*% Rotation)
            accel_rotated = accel_data @ xb(att_roll)
            accel_rotated = accel_rotated @ yb(att_pitch)
        else:
            accel_rotated = accel_data

        # Apply Gsep with circular wrapping
        static, dynamic, odba, vedba = gsep_batch_circular(accel_rotated, self.filt_len)

        # Compute pitch/roll from static components (R's pitchRoll2)
        static_mag = np.sqrt(np.sum(static**2, axis=1))
        # Avoid division by zero
        static_mag[static_mag == 0] = 1.0
        static_norm = static / static_mag[:, np.newaxis]

        pitch_deg = -np.degrees(
            np.arctan2(static_norm[:, 0], np.sqrt(static_norm[:, 1] ** 2 + static_norm[:, 2] ** 2))
        )
        roll_deg = np.degrees(np.arctan2(static_norm[:, 1], static_norm[:, 2]))

        # Store results
        self.batch_results = {
            "static": static,
            "dynamic": dynamic,
            "ODBA": odba,
            "VeDBA": vedba,
            "pitch_deg": pitch_deg,
            "roll_deg": roll_deg,
            "pitch_rad": np.radians(pitch_deg),
            "roll_rad": np.radians(roll_deg),
            "accel_rotated": accel_rotated,
        }

        # Store depth if available (with interpolation)
        if self.batch_depth_data:
            depth_arr = np.array(self.batch_depth_data)
            # Interpolate NaNs if present (acausal/batch interpolation)
            nans = np.isnan(depth_arr)
            if np.any(nans):
                # Create x-axis indices
                x = np.arange(len(depth_arr))
                # Interpolate nans using valid data points
                # Note: This handles gaps in the 1Hz/0.2Hz depth data
                depth_arr[nans] = np.interp(x[nans], x[~nans], depth_arr[~nans])

            # Apply 5-second moving average smoothing (R-compatible)
            # R: stats::filter(dat$Depth, filter=rep(1,freq * 5) / (freq * 5))
            window_size = int(self.freq * 5)
            if len(depth_arr) >= window_size:
                kernel = np.ones(window_size) / window_size
                # Use mode='same' to match centered filter behavior
                # Note: This introduces edge effects (zeros assumed outside)
                # To mitigate, we could pad, but for now we stick to simple convolution
                # or we can use a more robust method if needed.
                # R's stats::filter produces NAs at ends. We prefer valid values.
                # Let's use 'valid' and pad with edge values to avoid zero-assumption artifacts
                pad_width = window_size // 2
                depth_padded = np.pad(depth_arr, pad_width, mode="edge")
                depth_smoothed = np.convolve(depth_padded, kernel, mode="valid")

                # Trim to original length if necessary
                # (should match exactly if window is odd/even handled right)
                # If window is even (e.g. 80), 'valid' on padded (N + 80) -> N + 1?
                # Let's check sizes.
                # Len(padded) = N + 2*pad_width.
                # Len(valid) = Len(padded) - window_size + 1 = N + 2*(W//2) - W + 1.
                # If W=80, pad=40. Len = N + 80 - 80 + 1 = N + 1.
                # We might have one extra sample.

                if len(depth_smoothed) > len(depth_arr):
                    depth_smoothed = depth_smoothed[: len(depth_arr)]
                elif len(depth_smoothed) < len(depth_arr):
                    # Should not happen with this padding logic usually
                    pass

                depth_arr = depth_smoothed

            self.batch_results["Depth"] = depth_arr

            # Calculate vertical velocity (R-style: diff of depth)
            # dat$vertical_velocity <- c(0, diff(dat$Depth))
            # dat$vertical_velocity <- c(stats::filter(dat$vertical_velocity,
            #                                          filter = rep(1,5) / 5))

            # 1. Calculate diff (prepend 0 to maintain length)
            vert_vel = np.diff(depth_arr, prepend=depth_arr[0])

            # 2. Smooth
            # R code uses `rep(1,5)/5` which is explicitly 5 samples, despite comments in R code
            # mentioning "5 second running mean". We stick to the code implementation (5 samples)
            # rather than the comment intent (5 seconds) to ensure exact output matching.
            vv_window_size = 5
            if len(vert_vel) >= vv_window_size:
                vv_kernel = np.ones(vv_window_size) / vv_window_size
                vv_pad_width = vv_window_size // 2
                vv_padded = np.pad(vert_vel, vv_pad_width, mode="edge")
                vv_smoothed = np.convolve(vv_padded, vv_kernel, mode="valid")

                if len(vv_smoothed) > len(vert_vel):
                    vv_smoothed = vv_smoothed[: len(vert_vel)]

                vert_vel = vv_smoothed

            self.batch_results["vertical_velocity"] = vert_vel

        # Store velocity if available (with interpolation)
        if self.batch_velocity_data:
            vel_arr = np.array(self.batch_velocity_data)
            # Interpolate NaNs if present
            nans = np.isnan(vel_arr)
            if np.any(nans):
                x = np.arange(len(vel_arr))
                # Only interpolate if we have at least some valid data
                if np.any(~nans):
                    vel_arr[nans] = np.interp(x[nans], x[~nans], vel_arr[~nans])

            # Apply smoothing (same as depth)
            window_size = int(self.freq * 5)
            if len(vel_arr) >= window_size:
                kernel = np.ones(window_size) / window_size
                pad_width = window_size // 2
                vel_padded = np.pad(vel_arr, pad_width, mode="edge")
                vel_smoothed = np.convolve(vel_padded, kernel, mode="valid")

                if len(vel_smoothed) > len(vel_arr):
                    vel_smoothed = vel_smoothed[: len(vel_arr)]

                vel_arr = vel_smoothed

            self.batch_results["velocity"] = vel_arr

        # Also process magnetometer if available
        if self.batch_mag_data:
            mag_data = np.array(self.batch_mag_data)
            mag_offset = self._get_mag_offset()

            if mag_offset is not None:
                # Apply hard iron offset and normalization
                # mag_offset is [x, y, z, radius]
                mag_adj = (mag_data - mag_offset[:3]) / mag_offset[3]

                # Rotate by attachment angles
                if att_roll is not None and att_pitch is not None:
                    mag_rotated = mag_adj @ xb(att_roll)
                    mag_rotated = mag_rotated @ yb(att_pitch)
                else:
                    mag_rotated = mag_adj

                # Correct for pitch/roll (per-row local rotation)
                # R-style: Mag %*% Yb(-pitch) %*% Xb(roll)
                heading_deg = np.zeros(len(mag_data))

                # R-style Local Rotation Corrected Magnetometer
                # We use the row-vector convention: v_corr = v_rot @ Yb(-pitch) @ Xb(roll)
                for i in range(len(mag_data)):
                    p_rad = np.radians(pitch_deg[i])
                    r_rad = np.radians(roll_deg[i])

                    # Apply Yb(-p) then Xb(r)
                    # v_corr = v_rot @ Yb(-p) @ Xb(r)

                    m_vec = mag_rotated[i]
                    m_corr = m_vec @ yb(-p_rad)
                    m_corr = m_corr @ xb(r_rad)

                    # Heading
                    heading_deg[i] = math.degrees(math.atan2(-m_corr[1], m_corr[0]))

                self.batch_results["heading_deg"] = heading_deg
                self.batch_results["heading_rad"] = np.radians(heading_deg)
                self.batch_results["mag_rotated"] = mag_rotated

                # Calculate Pseudo Track (Dead Reckoning)
                # R: dat$pseudo_x <- cumsum(cos(dat$heading_radians) * (1 / freq) * 1)
                # Assumes 1 m/s speed
                speed = 1.0
                # Calculate Pseudo Track (Dead Reckoning) using REAL TIMESTAMPS (True Integration)
                # Matches position changes to actual time deltas, eliminating velocity jitter
                speed = 1.0
                dt = 1.0 / self.freq

                if self.batch_timestamps and len(self.batch_timestamps) == len(
                    self.batch_accel_data
                ):
                    ts_arr = np.array(self.batch_timestamps)
                    # Calculate actual dt between samples
                    # Prepend assumption for first sample
                    dt_arr = np.diff(ts_arr, prepend=ts_arr[0] - (1.0 / self.freq))

                    # Calculate Clock Drift
                    # drift = Actual - Synthetic
                    # Synthetic = Start + i * (1/freq)
                    synthetic_ts = ts_arr[0] + np.arange(len(ts_arr)) * (1.0 / self.freq)
                    drift_arr = ts_arr - synthetic_ts

                    self.batch_results["clock_drift_sec"] = drift_arr

                    # Use real dt (True Integration) or fixed dt (R-Compat)
                    dt_vector = dt_arr if self.true_integration else np.full(len(dt_arr), dt)

                    self.batch_results["pseudo_x"] = np.cumsum(
                        np.cos(self.batch_results["heading_rad"]) * speed * dt_vector
                    )
                    self.batch_results["pseudo_y"] = np.cumsum(
                        np.sin(self.batch_results["heading_rad"]) * speed * dt_vector
                    )
                else:
                    # Fallback if timestamps missing (legacy behavior)
                    self.batch_results["pseudo_x"] = np.cumsum(
                        np.cos(self.batch_results["heading_rad"]) * speed * dt
                    )
                    self.batch_results["pseudo_y"] = np.cumsum(
                        np.sin(self.batch_results["heading_rad"]) * speed * dt
                    )

    def _get_attachment_angles(self) -> tuple[float | None, float | None]:
        """Get attachment angles (either computed, locked, or None)."""
        if self.computed_attachment_roll_rad is not None:
            return self.computed_attachment_roll_rad, self.computed_attachment_pitch_rad
        elif self.locked_attachment_roll_rad is not None:
            return self.locked_attachment_roll_rad, self.locked_attachment_pitch_rad
        else:
            return None, None

    def _get_mag_offset(self) -> NDArray[np.float64] | None:
        """Get magnetometer offset (either computed, locked, or None)."""
        if self.computed_mag_offset is not None:
            return self.computed_mag_offset
        elif self.locked_mag_offset is not None:
            return self.locked_mag_offset
        else:
            return None

    def process(self, data: dict[str, Any] | np.ndarray) -> dict[str, Any]:
        """
        Process a single record using non-causal filtfilt.

        Args:
            data: Raw sensor record (dict or array)

        Returns:
            Dictionary with processed state, or minimal state if record is skipped.
        """
        # Increment record count
        self.record_count += 1
        record = data if isinstance(data, dict) else cast(dict[str, Any], data)

        # Extract accelerometer data (handle both quoted and unquoted field names)
        def get_field(record: dict[str, Any], quoted_name: str, unquoted_name: str) -> Any:
            return record.get(quoted_name, record.get(unquoted_name, "nan"))

        # Extract timestamp (look for internal DateTimeP from data_loader first, then Date)
        timestamp_obj = record.get("DateTimeP")
        if timestamp_obj is not None and not isinstance(timestamp_obj, float):
            # Already a datetime object from data_loader
            try:
                timestamp = timestamp_obj.timestamp()
            except (AttributeError, ValueError):
                timestamp = float("nan")
        else:
            # Try to extract Date (Excel serial date) and convert
            date_val = safe_float(
                get_field(record, '"Date"', "Date"),
                "Date",
                self.debug_level,
                self.record_count,
            )
            if not math.isnan(date_val):
                from datetime import datetime, timedelta, timezone

                base_date = datetime(1899, 12, 30, tzinfo=timezone.utc)
                try:
                    dt = base_date + timedelta(days=date_val)
                    timestamp = dt.timestamp()
                except Exception:
                    timestamp = float("nan")
            else:
                # Try Time as fallback
                timestamp = safe_float(
                    get_field(record, '"Time"', "Time"),
                    "Time",
                    self.debug_level,
                    self.record_count,
                )

        # Sub-second interpolation
        if not math.isnan(timestamp):
            # If timestamp matches previous, increment index
            if timestamp == self.last_ts:
                self.sub_sec_idx += 1
            else:
                self.last_ts = timestamp
                self.sub_sec_idx = 0

            # Apply offset: index * period
            # e.g. at 16Hz: 0.0, 0.0625, 0.125...
            timestamp += self.sub_sec_idx * (1.0 / self.freq)

        # 1. Collection Phase (Pass 1)
        if self.r_exact_mode and not self.calibration_complete:
            # Extract raw values for batch collection
            x_accel_raw = safe_float(
                get_field(record, '"int aX"', "int aX"),
                "int aX",
                self.debug_level,
                self.record_count,
            )
            y_accel_raw = safe_float(
                get_field(record, '"int aY"', "int aY"),
                "int aY",
                self.debug_level,
                self.record_count,
            )
            z_accel_raw = safe_float(
                get_field(record, '"int aZ"', "int aZ"),
                "int aZ",
                self.debug_level,
                self.record_count,
            )
            x_mag_raw = safe_float(
                get_field(record, '"int mX"', "int mX"),
                "int mX",
                self.debug_level,
                self.record_count,
            )
            y_mag_raw = safe_float(
                get_field(record, '"int mY"', "int mY"),
                "int mY",
                self.debug_level,
                self.record_count,
            )
            z_mag_raw = safe_float(
                get_field(record, '"int mZ"', "int mZ"),
                "int mZ",
                self.debug_level,
                self.record_count,
            )

            # Extract depth data (if available)
            depth_raw = (
                safe_float(
                    get_field(record, '"Depth"', "Depth"),
                    "Depth",
                    self.debug_level,
                    self.record_count,
                )
                if self.depth_buffer is not None
                else float("nan")
            )

            # Extract velocity data (if available)
            velocity_raw = (
                safe_float(
                    get_field(record, '"velocity"', "velocity"),
                    "velocity",
                    self.debug_level,
                    self.record_count,
                )
                if self.depth_buffer is not None
                else float("nan")
            )

            # Check for validity (R script filters out NaNs in 'int aX')
            is_valid = (
                not math.isnan(x_accel_raw)
                and not math.isnan(y_accel_raw)
                and not math.isnan(z_accel_raw)
            )

            if is_valid:
                if self.batch_accel_data is not None:
                    self.batch_accel_data.append([x_accel_raw, y_accel_raw, z_accel_raw])
                if self.batch_mag_data is not None:
                    self.batch_mag_data.append([x_mag_raw, y_mag_raw, z_mag_raw])
                if self.batch_depth_data is not None:
                    self.batch_depth_data.append(depth_raw)
                if self.batch_velocity_data is not None:
                    self.batch_velocity_data.append(velocity_raw)
                if self.batch_timestamps is not None:
                    self.batch_timestamps.append(timestamp)

                # Store that this record_count was valid for Pass 2 indexing
                self.valid_record_indices.add(self.record_count)

            # Return minimal output during collection phase
            return {
                "record_count": self.record_count,
                "timestamp": timestamp,
                "X_Accel_raw": x_accel_raw,
                "Y_Accel_raw": y_accel_raw,
                "Z_Accel_raw": z_accel_raw,
                "skipped": not is_valid,
            }

        # 2. Processing Phase (Pass 2)
        if self.r_exact_mode and self.calibration_complete and self.batch_results:
            # Check if this record was actually included in the batch calculations
            if self.record_count not in self.valid_record_indices:
                return {
                    "record_count": self.record_count,
                    "timestamp": timestamp,
                    "skipped": True,
                }

            # Map the actual record index to its position in the filtered batch results
            res = self.batch_results
            idx = self.processing_idx
            self.processing_idx += 1

            x_accel_raw = safe_float(
                get_field(record, '"int aX"', "int aX"),
                "int aX",
                self.debug_level,
                self.record_count,
            )
            y_accel_raw = safe_float(
                get_field(record, '"int aY"', "int aY"),
                "int aY",
                self.debug_level,
                self.record_count,
            )
            z_accel_raw = safe_float(
                get_field(record, '"int aZ"', "int aZ"),
                "int aZ",
                self.debug_level,
                self.record_count,
            )
            x_mag_raw = safe_float(
                get_field(record, '"int mX"', "int mX"),
                "int mX",
                self.debug_level,
                self.record_count,
            )
            y_mag_raw = safe_float(
                get_field(record, '"int mY"', "int mY"),
                "int mY",
                self.debug_level,
                self.record_count,
            )
            z_mag_raw = safe_float(
                get_field(record, '"int mZ"', "int mZ"),
                "int mZ",
                self.debug_level,
                self.record_count,
            )
            depth_raw = safe_float(
                get_field(record, '"Depth"', "Depth"),
                "Depth",
                self.debug_level,
                self.record_count,
            )
            velocity_raw = safe_float(
                get_field(record, '"velocity"', "velocity"),
                "velocity",
                self.debug_level,
                self.record_count,
            )

            # Step 1: Apply attachment angle rotation to raw accelerometer (if available)
            static = res["static"][idx]
            dynamic = res["dynamic"][idx]
            accel_rot = res["accel_rotated"][idx]

            attachment_roll, attachment_pitch = self._get_attachment_angles()

            # Calculate final depth and velocity values
            final_depth = res["Depth"][idx] if "Depth" in res else depth_raw

            final_vertical_velocity = 0.0
            if "vertical_velocity" in res:
                final_vertical_velocity = res["vertical_velocity"][idx]

            # Use 0.0 for speed calc if vertical velocity is NaN
            vv_safe = final_vertical_velocity if not math.isnan(final_vertical_velocity) else 0.0

            # Compute 3D speed from vertical velocity + assumed horizontal speed (1.0 m/s)
            # This ensures invalid input velocity doesn't zero out the HUD
            final_velocity = math.sqrt(1.0**2 + vv_safe**2)

            output = {
                "record_count": self.record_count,
                "timestamp": timestamp,
                "X_Accel_raw": x_accel_raw,
                "Y_Accel_raw": y_accel_raw,
                "Z_Accel_raw": z_accel_raw,
                "X_Mag_raw": x_mag_raw,
                "Y_Mag_raw": y_mag_raw,
                "Z_Mag_raw": z_mag_raw,
                "Depth": final_depth,
                "velocity": final_velocity,
                "vertical_velocity": final_vertical_velocity,
                "X_Accel_rotate": accel_rot[0],
                "Y_Accel_rotate": accel_rot[1],
                "Z_Accel_rotate": accel_rot[2],
                "X_Static": static[0],
                "Y_Static": static[1],
                "Z_Static": static[2],
                "X_Dynamic": dynamic[0],
                "Y_Dynamic": dynamic[1],
                "Z_Dynamic": dynamic[2],
                "ODBA": res["ODBA"][idx],
                "VeDBA": res["VeDBA"][idx],
                "pitch_degrees": res["pitch_deg"][idx],
                "roll_degrees": res["roll_deg"][idx],
                "pitch_radians": res["pitch_rad"][idx],
                "roll_radians": res["roll_rad"][idx],
            }

            if "clock_drift_sec" in res:
                output["clock_drift_sec"] = res["clock_drift_sec"][idx]

            if "heading_deg" in res:
                output["heading_degrees"] = res["heading_deg"][idx]
                output["heading_radians"] = res["heading_rad"][idx]

            if "pseudo_x" in res:
                output["pseudo_x"] = res["pseudo_x"][idx]
                output["pseudo_y"] = res["pseudo_y"][idx]

            # Publish to ZMQ if enabled
            if self.zmq_publisher and self.eid is not None and self.sim_id is not None:
                self.zmq_publisher.publish_state(self.eid, self.sim_id, self.tag_id, output)

            return output

        # Get attachment angles (for rotation)
        attachment_roll, attachment_pitch = self._get_attachment_angles()

        # Step 1: Apply attachment angle rotation to raw accelerometer (if available)
        if attachment_roll is not None and attachment_pitch is not None:
            # Create numpy array for rotation
            accel_vec = np.array([x_accel_raw, y_accel_raw, z_accel_raw])
            # Apply Xb(roll) then Yb(pitch) rotation (R-style: Data %*% Rotation)
            # Note: We use vector @ matrix to match R's row-vector convention
            accel_rotated = accel_vec @ xb(attachment_roll)
            accel_rotated = accel_rotated @ yb(attachment_pitch)
            x_accel_rotate = accel_rotated[0]
            y_accel_rotate = accel_rotated[1]
            z_accel_rotate = accel_rotated[2]
        else:
            # No attachment angle correction - use raw values
            x_accel_rotate = x_accel_raw
            y_accel_rotate = y_accel_raw
            z_accel_rotate = z_accel_raw

        # Step 2: Apply filtfilt-based Gsep to rotated accelerometer
        (
            static_x,
            static_y,
            static_z,
            dyn_x,
            dyn_y,
            dyn_z,
            odba,
            vedba,
        ) = gsep_streaming(
            x_accel_rotate,
            y_accel_rotate,
            z_accel_rotate,
            self.filt_len,
            self.accel_buffer,
        )

        # Buffer the current record for delayed emission
        # We store the raw values and the computed rotation
        buffered_record = record.copy()
        buffered_record["_x_accel_rotate"] = x_accel_rotate
        buffered_record["_y_accel_rotate"] = y_accel_rotate
        buffered_record["_z_accel_rotate"] = z_accel_rotate
        self.record_buffer.append(buffered_record)

        # If we haven't filled the buffer enough to account for the centered filter delay,
        # we can't emit a valid record yet.
        # The centered filter output corresponds to the sample at index: len(buffer) - 1 - delay
        # delay = (filt_len - 1) // 2
        delay = (self.filt_len - 1) // 2
        if len(self.record_buffer) <= delay:
            return {}  # Still warming up

        # Retrieve the record that corresponds to the current filter output
        # The filter output (static_x, etc.) corresponds to the record 'delay' samples ago
        # record_buffer[-1] is current, record_buffer[-(delay+1)] is the target
        target_record = self.record_buffer[-(delay + 1)]

        # Step 3: Compute pitch and roll from static acceleration (R-style pitchRoll2)
        # Uses xb, yb rotation functions from biologger_sim.functions.rotation
        if not math.isnan(static_x):
            # Convert static acceleration to unit vector
            static_mag = math.sqrt(static_x**2 + static_y**2 + static_z**2)
            if static_mag > 0:
                static_x_norm = static_x / static_mag
                static_y_norm = static_y / static_mag
                static_z_norm = static_z / static_mag

                # Compute pitch and roll using R-style atan2
                # pitch = atan2(xb, sqrt(yb^2 + zb^2))
                # roll = atan2(yb, zb)
                pitch_rad = math.atan2(
                    static_x_norm, math.sqrt(static_y_norm**2 + static_z_norm**2)
                )
                roll_rad = math.atan2(static_y_norm, static_z_norm)
                pitch_deg = math.degrees(pitch_rad)
                roll_deg = math.degrees(roll_rad)
            else:
                pitch_rad = float("nan")
                roll_rad = float("nan")
                pitch_deg = float("nan")
                roll_deg = float("nan")
        else:
            pitch_rad = float("nan")
            roll_rad = float("nan")
            pitch_deg = float("nan")
            roll_deg = float("nan")

        # Step 4: Process magnetometer data (if available)
        mag_offset = self._get_mag_offset()
        if mag_offset is not None and not math.isnan(x_mag_raw):
            # Apply hard iron offset and normalization
            x_mag_adj = (x_mag_raw - mag_offset[0]) / mag_offset[3]
            y_mag_adj = (y_mag_raw - mag_offset[1]) / mag_offset[3]
            z_mag_adj = (z_mag_raw - mag_offset[2]) / mag_offset[3]

            # Rotate magnetometer by attachment angles (if available)
            if attachment_roll is not None and attachment_pitch is not None:
                mag_vec = np.array([x_mag_adj, y_mag_adj, z_mag_adj])
                # Apply Xb(roll) then Yb(pitch) rotation (R-style: Data %*% Rotation)
                mag_rotated = mag_vec @ xb(attachment_roll)
                mag_rotated = mag_rotated @ yb(attachment_pitch)
                x_mag_rotate = mag_rotated[0]
                y_mag_rotate = mag_rotated[1]
                z_mag_rotate = mag_rotated[2]
            else:
                x_mag_rotate = x_mag_adj
                y_mag_rotate = y_mag_adj
                z_mag_rotate = z_mag_adj

            # Correct magnetometer for pitch/roll (R-style, per-row local rotation)
            if not math.isnan(pitch_rad) and not math.isnan(roll_rad):
                mag_vec_corr = np.array([x_mag_rotate, y_mag_rotate, z_mag_rotate])
                # Apply Yb(-pitch) then Xb(roll) rotation (R-style: Data %*% Rotation)
                mag_corrected = mag_vec_corr @ yb(-pitch_rad)
                mag_corrected = mag_corrected @ xb(roll_rad)
                x_mag_corrected = mag_corrected[0]
                y_mag_corrected = mag_corrected[1]
                z_mag_corrected = mag_corrected[2]

                # Calculate heading from corrected magnetometer
                heading_rad = math.atan2(-y_mag_corrected, x_mag_corrected)
                heading_deg = math.degrees(heading_rad)
            else:
                x_mag_corrected = float("nan")
                y_mag_corrected = float("nan")
                z_mag_corrected = float("nan")
                heading_rad = float("nan")
                heading_deg = float("nan")
        else:
            x_mag_adj = float("nan")
            y_mag_adj = float("nan")
            z_mag_adj = float("nan")
            x_mag_rotate = float("nan")
            y_mag_rotate = float("nan")
            z_mag_rotate = float("nan")
            x_mag_corrected = float("nan")
            y_mag_corrected = float("nan")
            z_mag_corrected = float("nan")
            heading_rad = float("nan")
            heading_deg = float("nan")

        # Calculate Dead Reckoning (Pseudo Track)
        if not math.isnan(heading_rad):
            # R uses constant 1 m/s speed
            speed = 1.0
            delta_t = 1.0 / self.freq
            dx = speed * math.cos(heading_rad) * delta_t
            dy = speed * math.sin(heading_rad) * delta_t
            self.pseudo_x += dx
            self.pseudo_y += dy
        else:
            # If heading is NaN, position doesn't change (or should it be NaN?)
            # For visualization, keeping last known position is usually better than NaN
            pass

        # Build output record (expanded schema for R-compatibility)
        # Use target_record for raw values to ensure alignment
        # Get batch-computed vertical velocity (R-style smoothing applied in Pass 1)
        vert_vel = 0.0
        results = self.batch_results
        if results is not None and "vertical_velocity" in results:
            vv_list = results["vertical_velocity"]
            res_idx = self.record_count - 1 - delay
            if 0 <= res_idx < len(vv_list):
                vert_vel = vv_list[res_idx]

        # Calculate 3D velocity magnitude (Horizontal 1.0 m/s + Vertical Rate)
        # This provides a non-zero, dynamic velocity readout for the HUD
        total_speed_3d = math.sqrt(1.0 + vert_vel**2)

        # Build output record (expanded schema for R-compatibility)
        # Use target_record for raw values to ensure alignment
        output = {
            "record_count": self.record_count - delay,  # Adjust count for delay
            "X_Accel_raw": safe_float(
                get_field(target_record, '"int aX"', "int aX"),
                "int aX",
                0,
                0,
            ),
            "Y_Accel_raw": safe_float(
                get_field(target_record, '"int aY"', "int aY"),
                "int aY",
                0,
                0,
            ),
            "Z_Accel_raw": safe_float(
                get_field(target_record, '"int aZ"', "int aZ"),
                "int aZ",
                0,
                0,
            ),
            "X_Mag_raw": safe_float(
                get_field(target_record, '"int mX"', "int mX"),
                "int mX",
                0,
                0,
            ),
            "Y_Mag_raw": safe_float(
                get_field(target_record, '"int mY"', "int mY"),
                "int mY",
                0,
                0,
            ),
            "Z_Mag_raw": safe_float(
                get_field(target_record, '"int mZ"', "int mZ"),
                "int mZ",
                0,
                0,
            ),
            "Depth": safe_float(
                get_field(target_record, '"Depth"', "Depth"),
                "Depth",
                0,
                0,
            ),
            "X_Accel_rotate": target_record.get("_x_accel_rotate", float("nan")),
            "Y_Accel_rotate": target_record.get("_y_accel_rotate", float("nan")),
            "Z_Accel_rotate": target_record.get("_z_accel_rotate", float("nan")),
            "X_Static": static_x,
            "Y_Static": static_y,
            "Z_Static": static_z,
            "X_Dynamic": dyn_x,
            "Y_Dynamic": dyn_y,
            "Z_Dynamic": dyn_z,
            "ODBA": odba,
            "VeDBA": vedba,
            "pitch_radians": pitch_rad,
            "roll_radians": roll_rad,
            "pitch_degrees": pitch_deg,
            "roll_degrees": roll_deg,
            "X_Mag_adj": x_mag_adj,
            "Y_Mag_adj": y_mag_adj,
            "Z_Mag_adj": z_mag_adj,
            "X_Mag_rotate": x_mag_rotate,
            "Y_Mag_rotate": y_mag_rotate,
            "Z_Mag_rotate": z_mag_rotate,
            "X_Mag_corrected": x_mag_corrected,
            "Y_Mag_corrected": y_mag_corrected,
            "Z_Mag_corrected": z_mag_corrected,
            "heading_radians": heading_rad,
            "heading_degrees": heading_deg,
            "velocity": total_speed_3d,
            "vertical_velocity": vert_vel,
            "pseudo_x": self.pseudo_x,
            "pseudo_y": self.pseudo_y,
        }

        # Publish to ZMQ if enabled
        if self.zmq_publisher and self.eid is not None and self.sim_id is not None:
            if self.debug_level >= 2:
                self.logger.debug(f"Publishing to ZMQ: {output.get('record_count')}")
            self.zmq_publisher.publish_state(self.eid, self.sim_id, self.tag_id, output)

        if self.debug_level >= 2 and self.record_count <= 10:
            self.logger.debug(f"Record #{self.record_count}: {output}")

        return output

    def reset(self) -> None:
        """Reset processor to initial state."""
        self.accel_buffer.clear()
        if self.mag_buffer is not None:
            self.mag_buffer.clear()
        if self.depth_buffer is not None:
            self.depth_buffer.clear()
        self.record_buffer.clear()
        self.record_count = 0
        self.processing_idx = 0
        self.pseudo_x = 0.0
        self.pseudo_y = 0.0
        self.logger.info("PostFactoProcessor reset")

    def get_performance_summary(self) -> dict[str, Any]:
        """Get performance metrics."""
        return {
            "processor_type": "PostFactoProcessor",
            "records_processed": self.record_count,
            "filt_len": self.filt_len,
            "buffer_size": len(self.accel_buffer),
            "buffer_max_size": self.accel_buffer.maxlen,
        }

    def update_config(self, config_updates: dict[str, Any]) -> None:
        """Update processor configuration."""
        if "filt_len" in config_updates:
            self.filt_len = config_updates["filt_len"]
            # Recreate buffer with new size
            old_buffer = list(self.accel_buffer)
            self.accel_buffer = deque(old_buffer, maxlen=self.filt_len * 2)
            self.logger.info(f"Updated filt_len to {self.filt_len}")

        if "debug_level" in config_updates:
            self.debug_level = config_updates["debug_level"]
            self.logger.info(f"Updated debug_level to {self.debug_level}")

    def get_current_state(self) -> dict[str, Any]:
        """Get current processor state."""
        return {
            "record_count": self.record_count,
            "buffer_fill": len(self.accel_buffer),
            "buffer_capacity": self.accel_buffer.maxlen,
            "ready_for_output": len(self.accel_buffer) >= self.filt_len * 2,
        }

    def get_output_schema(self) -> list[str]:
        """Get list of output fields (R-compatible expanded schema)."""
        return [
            "record_count",
            "X_Accel_raw",
            "Y_Accel_raw",
            "Z_Accel_raw",
            "X_Mag_raw",
            "Y_Mag_raw",
            "Z_Mag_raw",
            "Depth",
            "X_Accel_rotate",
            "Y_Accel_rotate",
            "Z_Accel_rotate",
            "X_Static",
            "Y_Static",
            "Z_Static",
            "X_Dynamic",
            "Y_Dynamic",
            "Z_Dynamic",
            "ODBA",
            "VeDBA",
            "pitch_radians",
            "roll_radians",
            "pitch_degrees",
            "roll_degrees",
            "X_Mag_adj",
            "Y_Mag_adj",
            "Z_Mag_adj",
            "X_Mag_rotate",
            "Y_Mag_rotate",
            "Z_Mag_rotate",
            "X_Mag_corrected",
            "Y_Mag_corrected",
            "Z_Mag_corrected",
            "heading_radians",
            "heading_degrees",
            "velocity",
            "vertical_velocity",
            "pseudo_x",
            "pseudo_y",
        ]
