# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import logging
from typing import Any

import numpy as np

try:
    import mlx.core as mx
except ImportError:
    mx = None

from biologger_sim.core.processor_interface import BiologgerProcessor


class MLXInertialTensorProcessor(BiologgerProcessor):
    """
    Massively parallel GPU-resident processor for biomimetic swarms (50k+ entities)
    optimized for Apple Silicon using the MLX framework.

    Architecture:
    - Resident State: Maintains 'num_entities' filter buffers directly in GPU Unified Memory.
    - Zero-Copy Logic: Graph compilation JIT (mx.compile) processes batched inputs.
    - Minimal IO: Python overhead is minimized via JIT tracing.
    """

    def __init__(
        self,
        num_entities: int,
        filt_len: int = 48,
        freq: int = 16,
        debug_level: int = 0,
        device: str = "gpu",
        **kwargs: Any,
    ) -> None:
        self.num_entities = num_entities
        self.filt_len = filt_len
        self.freq = freq
        self.debug_level = debug_level
        self.device_type = device

        self.logger = logging.getLogger(__name__)
        if debug_level > 0:
            self.logger.setLevel(logging.DEBUG)

        if mx is None:
            raise ImportError(
                "Apple MLX not found. MLXInertialTensorProcessor requires 'mlx'."
            )

        # Configure default device
        if device == "gpu":
            if mx.metal.is_available():
                mx.set_default_device(mx.gpu)
                self.logger.info("MLX using Apple Silicon GPU (Metal)")
            else:
                self.logger.warning("Metal GPU not available for MLX, falling back to CPU")
                mx.set_default_device(mx.cpu)
                self.device_type = "cpu"
        else:
            mx.set_default_device(mx.cpu)
            self.device_type = "cpu"

        # --- A. Resident State (GPU Unified Memory) ---
        self.accel_history = mx.zeros((num_entities, filt_len, 3))
        self.buffer_indices = mx.zeros((num_entities,), dtype=mx.int32)
        self.accel_sum = mx.zeros((num_entities, 3))
        self.orientation_out = mx.zeros((num_entities, 3))

        # Compile the JIT graph for step execution
        self._compile_step()

        self.logger.info(
            f"MLXInertialTensorProcessor initialized for {num_entities} "
            f"entities on {self.device_type}"
        )

    def reset(self) -> None:
        """Clear all GPU state."""
        self.accel_history = mx.zeros_like(self.accel_history)
        self.buffer_indices = mx.zeros_like(self.buffer_indices)
        self.accel_sum = mx.zeros_like(self.accel_sum)
        self.orientation_out = mx.zeros_like(self.orientation_out)

    def _compile_step(self) -> None:
        """Compiles the JIT-optimized graph for batch update."""

        @mx.compile
        def step(
            accel_history: mx.array,
            buffer_indices: mx.array,
            accel_sum: mx.array,
            orientation_out: mx.array,
            indices: mx.array,
            new_accel: mx.array,
        ) -> tuple[mx.array, mx.array, mx.array, mx.array]:
            ptrs = buffer_indices[indices]
            old_vals = accel_history[indices, ptrs]

            # 1. Update Sum: sum = sum - old + new
            new_sums = accel_sum[indices] - old_vals + new_accel
            accel_sum[indices] = new_sums

            # 2. Overwrite history ring buffer
            accel_history[indices, ptrs] = new_accel

            # 3. Advance pointers
            new_ptrs = (ptrs + 1) % self.filt_len
            buffer_indices[indices] = new_ptrs

            # 4. Compute Orientation
            scale = float(self.filt_len) * 10.0
            mean_accels = new_sums / scale
            ax_g = mean_accels[:, 0]
            ay_g = mean_accels[:, 1]
            az_g = mean_accels[:, 2]

            mag_yz = mx.sqrt(ax_g * ax_g + az_g * az_g)
            pitch_rad = -mx.arctan2(ax_g, mag_yz)

            # Safety check to avoid division by zero
            cond = (mx.abs(az_g) > 1.0e-6) | (mx.abs(ay_g) > 1.0e-6)
            roll_rad = mx.where(cond, mx.arctan2(ay_g, az_g), 0.0)

            sp = mx.sin(pitch_rad)
            cp = mx.cos(pitch_rad)
            sr = mx.sin(roll_rad)
            cr = mx.cos(roll_rad)

            accel_world_z = -sp * ax_g + cp * sr * ay_g + cp * cr * az_g
            new_orientations = mx.stack([roll_rad, pitch_rad, accel_world_z], axis=-1)

            # Store in output buffer
            orientation_out[indices] = new_orientations

            return accel_history, buffer_indices, accel_sum, orientation_out

        self._step_fn = step

    def process_vectors(
        self,
        indices: Any,  # List[int] or mx.array
        accel_data: Any,  # (B, 3) numpy or mx.array
    ) -> dict[str, Any]:
        """
        Process a block of accelerometer updates for specific entities (Vectorized).

        Args:
            indices: List or array of entity indices (len=B)
            accel_data: List or array of new [ax, ay, az] samples (len=B, 3)

        Returns:
            Dict containing vector results (numpy arrays):
            {
                "roll_rad": (B,),
                "pitch_rad": (B,),
                "world_z": (B,)
            }
        """
        # Convert inputs to MLX Arrays (Zero-copy in unified memory if passing numpy/lists)
        if isinstance(indices, mx.array):
            mx_indices = indices
        else:
            mx_indices = mx.array(np.array(indices, dtype=np.int32))

        if isinstance(accel_data, mx.array):
            mx_accel = accel_data
        else:
            mx_accel = mx.array(np.array(accel_data, dtype=np.float32))

        # Run compiled step
        self.accel_history, self.buffer_indices, self.accel_sum, self.orientation_out = (
            self._step_fn(
                self.accel_history,
                self.buffer_indices,
                self.accel_sum,
                self.orientation_out,
                mx_indices,
                mx_accel,
            )
        )

        # Force evaluation of the modified state arrays on GPU
        mx.eval(self.orientation_out)

        # Retrieve outputs (gather updated values from unified memory)
        block_res = np.array(self.orientation_out[mx_indices])

        return {
            "roll_rad": block_res[:, 0],
            "pitch_rad": block_res[:, 1],
            "world_z": block_res[:, 2],
        }

    def process(self, record: dict[str, Any] | Any) -> dict[str, Any]:
        """
        Single-record processing is NOT supported by this architecture.
        Use process_vectors() instead.
        """
        raise NotImplementedError(
            "MLXInertialTensorProcessor is vector-only. Use process_vectors()."
        )

    def calibrate_from_batch_data(self) -> None:
        pass

    def get_performance_summary(self) -> dict[str, Any]:
        return {
            "processor_type": "MLXInertialTensorProcessor",
            "device": self.device_type,
            "num_entities": self.num_entities,
        }

    def update_config(self, config_updates: dict[str, Any]) -> None:
        pass

    def get_current_state(self) -> dict[str, Any]:
        return {"status": "Running", "device": self.device_type}
