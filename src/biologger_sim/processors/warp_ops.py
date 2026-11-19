# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import warp as wp


@wp.kernel
def update_ring_buffer_kernel(
    entity_indices: wp.array(dtype=int),  # type: ignore
    new_accel: wp.array(dtype=wp.vec3),  # type: ignore
    accel_history: wp.array(dtype=wp.vec3, ndim=2),  # type: ignore
    buffer_indices: wp.array(dtype=int),  # type: ignore
    accel_sum: wp.array(dtype=wp.vec3),  # type: ignore
    filt_len: int,
) -> None:
    """
    Updates the sliding window ring buffer and running sum for a batch of entities.
    """
    tid = wp.tid()

    # 1. Helper: Get Entity info
    idx = entity_indices[tid]  # Entity ID
    val = new_accel[tid]  # New measurement

    # 2. Get current buffer pointer for this entity
    ptr = buffer_indices[idx]

    # 3. Retrieve Oldest Value (to subtract from sum)
    # accel_history[idx, ptr]
    old_val = accel_history[idx, ptr]

    # 4. Update Sum (Incremental Mean)
    # sum = sum - old + new
    current_sum = accel_sum[idx]
    new_sum = current_sum - old_val + val
    accel_sum[idx] = new_sum

    # 5. Overwrite History with New Value
    accel_history[idx, ptr] = val

    # 6. Advance Pointer (Wrap around)
    buffer_indices[idx] = (ptr + 1) % filt_len


@wp.kernel
def compute_orientation_indirect_kernel(
    entity_indices: wp.array(dtype=int),  # type: ignore
    accel_sum: wp.array(dtype=wp.vec3),  # type: ignore
    filt_len: int,
    outputs: wp.array(dtype=wp.vec3),  # type: ignore
) -> None:
    """
    Computes kinematics for specific entities (indirection) based on their running sum:
    roll and pitch from the mean static acceleration (in g), and the world-Z acceleration.

    outputs[tid]: (roll_rad, pitch_rad, accel_world_z)
    """
    tid = wp.tid()
    idx = entity_indices[tid]

    # Get Mean Static Accel
    # sum / filt_len
    sum_val = accel_sum[idx]

    # Scale: The sum is of raw input values.
    # In streaming.py we divide by (filt_len * 10.0) effectively?
    #   static_x = accel_sum / filt_len
    #   ax_g = static_x / 10.0
    # So we divide by (filt_len * 10.0)

    scale = float(filt_len) * 10.0
    ax_g = sum_val[0] / scale
    ay_g = sum_val[1] / scale
    az_g = sum_val[2] / scale

    # --- Orientation: pitch = -atan2(ax, |(ay, az)|), roll = atan2(ay, az) ---
    mag_yz = wp.sqrt(ay_g * ay_g + az_g * az_g)
    pitch_rad = -wp.atan2(ax_g, mag_yz)

    roll_rad = 0.0
    if wp.abs(az_g) > 1.0e-6 or wp.abs(ay_g) > 1.0e-6:
        roll_rad = wp.atan2(ay_g, az_g)

    sp = wp.sin(pitch_rad)
    cp = wp.cos(pitch_rad)
    sr = wp.sin(roll_rad)
    cr = wp.cos(roll_rad)

    accel_world_z = -sp * ax_g + cp * sr * ay_g + cp * cr * az_g

    # Write Output to the specific entity index
    outputs[idx] = wp.vec3(roll_rad, pitch_rad, accel_world_z)
