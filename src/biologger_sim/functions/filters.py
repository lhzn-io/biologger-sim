# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""
Non-causal filtering for post-facto biologger analysis.

This module provides filtfilt-based (bidirectional, zero-phase) filtering
to achieve R-compatibility for scientific validation. Unlike the streaming
module which uses causal lfilter, these filters look both forward and backward
in time, which is only possible for post-hoc analysis.

Key functions:
- gsep_filtfilt: R-compatible gravitational separation using scipy.signal.filtfilt
"""

from collections import deque
from typing import cast

import numpy as np
from numpy.typing import NDArray
from scipy.signal import butter, filtfilt


def gsep_batch_circular(
    accel_array: NDArray[np.float64], filt_len: int
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """
    Batch Gsep with circular wrapping - exact R match.

    This matches R's: filter(xyz, filter=filt, sides=2, circular=TRUE)

    Args:
        accel_array (np.ndarray): Full accelerometer data, shape (N, 3)
        filt_len (int): Filter window length

    Returns:
        tuple: (static, dynamic, ODBA, VeDBA) each shape (N, 3) or (N,)
    """
    weights = np.ones(filt_len) / filt_len

    # Apply R's circular filter to each axis
    static = np.zeros_like(accel_array)
    for axis in range(3):
        # Pad with circular wrapping (centered: (filt_len-1)//2 left, filt_len//2 right)
        pad_left = (filt_len - 1) // 2
        pad_right = filt_len // 2
        padded = np.pad(accel_array[:, axis], (pad_left, pad_right), mode="wrap")
        # Convolve and extract valid region
        static[:, axis] = np.convolve(padded, weights, mode="valid")

    # Compute dynamic
    dynamic = accel_array - static

    # ODBA and VeDBA
    odba = np.sum(np.abs(dynamic), axis=1)
    vedba = np.sqrt(np.sum(dynamic**2, axis=1))

    return static, dynamic, odba, vedba


def gsep_streaming(
    x: float,
    y: float,
    z: float,
    filt_len: int,
    buffer: deque[tuple[float, float, float]],
) -> tuple[float, float, float, float, float, float, float, float]:
    """
    Streaming Gsep without circular wrapping - for non-circular mode.

    This uses a centered filter on available samples only (no wrap-around).
    Edge effects at first/last ~filt_len/2 samples.

    Args:
        x, y, z (float): Current accelerometer readings (0.1g units)
        filt_len (int): Filter window length
        buffer (deque): Rolling buffer of samples

    Returns:
        tuple: (static_x, static_y, static_z, dyn_x, dyn_y, dyn_z, ODBA, VeDBA)
    """
    buffer.append((x, y, z))

    # Warmup period
    if len(buffer) < filt_len:
        return (float("nan"),) * 8

    accel_array = np.array(list(buffer))
    weights = np.ones(filt_len) / filt_len

    # Centered filter: compute static for center point of buffer
    # For streaming, we want the filtered value at the center of our window
    center_idx = filt_len // 2
    static_filtered = np.convolve(accel_array[:, 0], weights, mode="same")
    static_x = float(static_filtered[center_idx])

    static_filtered = np.convolve(accel_array[:, 1], weights, mode="same")
    static_y = float(static_filtered[center_idx])

    static_filtered = np.convolve(accel_array[:, 2], weights, mode="same")
    static_z = float(static_filtered[center_idx])

    # Dynamic acceleration (for center point)
    dyn_x = float(accel_array[center_idx, 0] - static_x)
    dyn_y = float(accel_array[center_idx, 1] - static_y)
    dyn_z = float(accel_array[center_idx, 2] - static_z)

    # ODBA and VeDBA
    odba = abs(dyn_x) + abs(dyn_y) + abs(dyn_z)
    vedba = np.sqrt(dyn_x**2 + dyn_y**2 + dyn_z**2)

    return (static_x, static_y, static_z, dyn_x, dyn_y, dyn_z, odba, vedba)


def butterworth_filtfilt(
    data: NDArray[np.float64], cutoff: float, fs: float, order: int = 5
) -> NDArray[np.float64]:
    """
    Apply Butterworth low-pass filter using filtfilt for zero-phase filtering.

    Args:
        data (np.ndarray): Input signal
        cutoff (float): Cutoff frequency in Hz
        fs (float): Sampling frequency in Hz
        order (int): Filter order (default 5)

    Returns:
        np.ndarray: Filtered signal
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return cast(NDArray[np.float64], filtfilt(b, a, data, padtype="even"))
