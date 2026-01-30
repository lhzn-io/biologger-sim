# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import warp as wp


@wp.kernel
def apply_attachment_correction_kernel(
    accel_in: wp.array(dtype=wp.vec3),  # type: ignore
    roll_sin: float,
    roll_cos: float,
    pitch_sin: float,
    pitch_cos: float,
    accel_out: wp.array(dtype=wp.vec3),  # type: ignore
) -> None:
    """
    Applies attachment orientation correction (rotation) to accelerometer data.
    Order: Roll (X) then Pitch (Y).
    """
    tid = wp.tid()
    val = accel_in[tid]
    ax = val[0]
    ay = val[1]
    az = val[2]

    # Xb(roll): y' = y*c - z*s, z' = y*s + z*c
    ay_r = ay * roll_cos - az * roll_sin
    az_r = ay * roll_sin + az * roll_cos

    # Yb(pitch): x' = x*c - z*s, z' = x*s + z*c
    # In streaming.py logic:
    # ax_att = ax_m * cp_a - az_r * sp_a
    # az_att = ax_m * sp_a + az_r * cp_a
    ax_out = ax * pitch_cos - az_r * pitch_sin
    ay_out = ay_r
    az_out = ax * pitch_sin + az_r * pitch_cos

    accel_out[tid] = wp.vec3(ax_out, ay_out, az_out)


@wp.kernel
def compute_orientation_and_gravity_kernel(
    accel_static: wp.array(dtype=wp.vec3),  # type: ignore
    outputs: wp.array(dtype=wp.vec3),  # type: ignore
) -> None:
    """
    Computes Roll, Pitch, and World-Z acceleration from static acceleration (G-vector).

    outputs[tid]: (roll_rad, pitch_rad, accel_world_z)
    """
    tid = wp.tid()
    val = accel_static[tid]

    # Scale: streaming.py divides by 10.0 (accel is in 0.1g units usually?)
    # Wait, in streaming.py:
    # ax_g, ay_g, az_g = static_x / 10.0, ...
    # So input here should be raw static sum/avg.
    # We will assume input is ALREADY scaled to G units or we scale here?
    # streaming.py: static_x is sum/div (so mean).
    # Then ax_g = static_x / 10.0.
    # Let's perform the scaling here to match streaming.py exactly if we pass unscaled mean.
    # actually let's assume input 'accel_static' is the MEAN (static_x, static_y, static_z).
    # So we divide by 10.0 inside.

    ax_g = val[0] / 10.0
    ay_g = val[1] / 10.0
    az_g = val[2] / 10.0

    # 1. Orientation
    # mag_yz = sqrt(ay^2 + az^2)
    mag_yz = wp.sqrt(ay_g * ay_g + az_g * az_g)

    # pitch = -atan2(ax, mag_yz)
    # wp.atan2(y, x)
    pitch_rad = -wp.atan2(ax_g, mag_yz)

    # roll = atan2(ay, az)
    # Protection: if abs(az) > 1e-6 or abs(ay) > 1e-6
    roll_rad = 0.0
    if wp.abs(az_g) > 1.0e-6 or wp.abs(ay_g) > 1.0e-6:
        roll_rad = wp.atan2(ay_g, az_g)

    sp = wp.sin(pitch_rad)
    cp = wp.cos(pitch_rad)
    sr = wp.sin(roll_rad)
    cr = wp.cos(roll_rad)

    # 2. World-Z
    # accel_world_z = -sin(p)*ax + cos(p)*sin(r)*ay + cos(p)*cos(r)*az
    accel_world_z = -sp * ax_g + cp * sr * ay_g + cp * cr * az_g

    outputs[tid] = wp.vec3(roll_rad, pitch_rad, accel_world_z)


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
    Computes kinematics for specific entities (indirection) based on their running sum.
    Same logic as compute_orientation_and_gravity_kernel but with indirection.
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

    # --- Orientation Logic (Copy of compute_orientation_and_gravity_kernel) ---
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
