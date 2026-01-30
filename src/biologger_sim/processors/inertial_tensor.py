import logging
from typing import Any

import numpy as np

try:
    import warp as wp
except ImportError:
    wp = None

from biologger_sim.core.processor_interface import BiologgerProcessor


class InertialTensorProcessor(BiologgerProcessor):
    """
    Massively parallel GPU-resident processor for biomimetic swarms (50k+ entities).

    Architecture:
    - Resident State: Maintains 'num_entities' filter buffers directly in GPU VRAM
      (Inertial Tensor).
    - Zero-Copy Logic: Accepts batch tensors, launches kernels, returns batch tensors.
    - Minimal IO: Python overhead is O(1) per batch, not O(N).

    Usage:
        processor = InertialTensorProcessor(num_entities=50000)
        processor.process_batch(indices, accel_data, ...)
    """

    def __init__(
        self,
        num_entities: int,
        filt_len: int = 48,
        freq: int = 16,
        debug_level: int = 0,
        device: str = "cuda",
        **kwargs: Any,
    ) -> None:
        self.num_entities = num_entities
        self.filt_len = filt_len
        self.freq = freq
        self.debug_level = debug_level
        self.device = device

        self.logger = logging.getLogger(__name__)
        if debug_level > 0:
            self.logger.setLevel(logging.DEBUG)

        if wp is None:
            raise ImportError(
                "NVIDIA Warp not found. InertialTensorProcessor requires 'warp-lang'."
            )

        if not wp.is_cuda_available() and "cuda" in device:
            self.logger.warning("CUDA not available, falling back to CPU for Warp (Slow!)")
            self.device = "cpu"

        # --- A. Resident State (The Inertial Tensor) ---
        # 1. Accelerometer History Ring Buffer: (N, filt_len)
        #    Used for sliding window smoothing/filtering.
        self.accel_history = wp.zeros((num_entities, filt_len), dtype=wp.vec3, device=self.device)

        # 2. Ring Buffer Pointer: (N,)
        #    Current write index for each entity.
        self.buffer_indices = wp.zeros(num_entities, dtype=wp.int32, device=self.device)

        # 3. Static Acceleration (Gravity): (N,)
        #    Running sum or computed mean for orientation.
        self.accel_sum = wp.zeros(num_entities, dtype=wp.vec3, device=self.device)
        self.static_accel = wp.zeros(
            num_entities, dtype=wp.vec3, device=self.device
        )  # Calculated mean

        # 4. State Output: (N,) -> [Roll, Pitch, WorldZ] (stored as vec3)
        self.orientation_out = wp.zeros(
            num_entities, dtype=wp.vec3, device=self.device
        )  # Roll, Pitch, WorldZ

        self.logger.info(
            f"InertialTensorProcessor initialized for {num_entities} entities on {self.device}"
        )

    def reset(self) -> None:
        """Clear all GPU state."""
        self.accel_history.zero_()
        self.buffer_indices.zero_()
        self.accel_sum.zero_()
        self.static_accel.zero_()
        self.orientation_out.zero_()

    def process_vectors(
        self,
        indices: Any,  # List[int] or wp.array(int)
        accel_data: Any,  # (N_block, 3) numpy or wp.array
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
        if not hasattr(self, "warp_ops"):
            import biologger_sim.processors.warp_ops as warp_ops

            self.warp_ops = warp_ops

        # 1. Inputs to Device
        # TODO: Optimization - If inputs are already on device, skip copy.
        if isinstance(indices, wp.array):
            d_indices = indices
        else:
            d_indices = wp.from_numpy(
                np.array(indices, dtype=np.int32), dtype=wp.int32, device=self.device
            )

        if isinstance(accel_data, wp.array):
            d_accel = accel_data
        else:
            d_accel = wp.from_numpy(
                np.array(accel_data, dtype=np.float32),
                dtype=wp.vec3,
                device=self.device,
            )

        block_size = d_indices.shape[0]

        # 2. Update Ring Buffer & Sum (Kernel)
        wp.launch(
            kernel=self.warp_ops.update_ring_buffer_kernel,
            dim=block_size,
            inputs=[
                d_indices,
                d_accel,
                self.accel_history,
                self.buffer_indices,
                self.accel_sum,
                self.filt_len,
            ],
            device=self.device,
        )

        # 3. Compute Orientation (Kernel) -> Writes to self.orientation_out at 'idx'
        # We use the indirect kernel to only update the modified entities
        wp.launch(
            kernel=self.warp_ops.compute_orientation_indirect_kernel,
            dim=block_size,
            inputs=[d_indices, self.accel_sum, self.filt_len, self.orientation_out],
            device=self.device,
        )

        # 4. Result Retrieval
        # We need to gather the results for the requested indices from the global state
        # A simple way is to read back 'orientation_out' but that is (N, 3).
        # We only want (B, 3).
        # We can implement a gather or just copy the whole thing if N is small?
        # No, N=50k, B=100. Copying 50k is waste.
        # Let's assume for now we want the results back on CPU for rendering/logging.
        # In a generic "Gather" kernel: out_batch[tid] = global_state[indices[tid]]

        # Ideally, we keep results on GPU for the renderer.
        # But to satisfy the generic API, let's pull back to CPU numpy.

        # Alloc temp output buffer for batch gather
        # d_result_block = wp.zeros(block_size, dtype=wp.vec3, device=self.device)

        # We can reuse a kernel or use wp.struct with gather? Warp doesn't have
        # simple wp.gather(src, indices).
        # Reuse compute kernel? No, that computes.
        # Let's define a tiny gather kernel or just read inputs?
        # Actually, self.orientation_out IS being updated by the kernel above.
        # If I modify compute_orientation_indirect_kernel to write to a "batch_output"
        # buffer INSTEAD of global state?
        # But we probably want GLOBAL state to be up to date for other consumers.
        # So we write to global, AND maybe write to a temporary batch output?
        # Or just launch a gather kernel.

        # For MVP, let's just rely on the fact that `compute_orientation_indirect_kernel`
        # computes the values we want.
        # I'll create a dedicated `gather_results_kernel` in warp_ops as well?
        # Or, just let the compute kernel write to TWO outputs: global state + batch stream.
        # Adding an extra argument to compute kernel is easy.

        # For now, let's leave result retrieval empty/dummy or full copy
        # to confirm execution, then optimize.
        # Full copy of 50k * 12 bytes = 600KB. It's tiny.
        # PCIe latency dominates, not bandwidth.
        # So `self.orientation_out.numpy()` is actually fine for <1MB.

        all_orient = self.orientation_out.numpy()
        # Filter on CPU (using original cpu indices)
        # This is strictly for API return values.
        # The visualizer should likely read `self.orientation_out` directly from GPU
        # memory if possible.

        # Map: indices (list/arr) -> block_results
        # indices might need to be host numpy
        h_indices = indices if not isinstance(indices, wp.array) else indices.numpy()

        block_res = all_orient[h_indices]  # (B, 3)

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
        raise NotImplementedError("InertialTensorProcessor is vector-only. Use process_vectors().")

    def calibrate_from_batch_data(self) -> None:
        pass

    def get_performance_summary(self) -> dict[str, Any]:
        return {
            "processor_type": "InertialTensorProcessor",
            "device": self.device,
            "num_entities": self.num_entities,
        }

    def update_config(self, config_updates: dict[str, Any]) -> None:
        pass

    def get_current_state(self) -> dict[str, Any]:
        """
        Returns a simplified state. For 50k entities, we can't return everything.
        """
        return {"status": "Running", "device": self.device}
