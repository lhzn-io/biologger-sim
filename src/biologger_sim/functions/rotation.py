# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from typing import cast

import numpy as np
from numpy.typing import NDArray


def xb(angle: float) -> NDArray[np.float64]:
    """
    local implementation of gRumble Xb(angle)
    Return the rotation matrix for a rotation about the X-axis by the given angle.

    CRITICAL: Must match R's gRumble::Xb() sign convention exactly!
    R uses: [[1, 0, 0], [0, cos(b), sin(b)], [0, -sin(b), cos(b)]]

    Parameters
    ----------
    angle : float
        The rotation angle in radians.
    Returns
    -------
    numpy.ndarray
        A 3x3 rotation matrix representing a rotation about the X-axis.
    """
    c, s = np.cos(angle), np.sin(angle)
    # Match R's sign convention (positive sin in [1,2], negative sin in [2,1])
    # R's Xb: [[1, 0, 0], [0, c, s], [0, -s, c]]
    return np.array([[1, 0, 0], [0, c, s], [0, -s, c]])


def yb(angle: float) -> NDArray[np.float64]:
    """
    local implementation of gRumble Yb(angle)
    Return the rotation matrix for a rotation about the Y-axis by the given angle.

    CRITICAL: Must match R's gRumble::Yb() sign convention exactly!
    R uses: [[cos(b), 0, sin(b)], [0, 1, 0], [-sin(b), 0, cos(b)]]

    Parameters
    ----------
    angle : float
        The rotation angle in radians.
    Returns
    -------
    numpy.ndarray
        A 3x3 rotation matrix representing a rotation about the Y-axis.
    """
    c, s = np.cos(angle), np.sin(angle)
    # Match R's sign convention (positive sin in [0,2], negative sin in [2,0])
    # R's Yb: [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def mag_offset(mag: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Estimate the offset and radius of a sphere fitted to 3D magnetometer data.
    This function fits a sphere to the provided 3D magnetometer measurements using
    least squares, estimating the hard-iron offset (bias) and the radius of the sphere.
    The offset can be used to correct magnetometer readings for hard-iron distortions.
    Parameters
    ----------
    mag : numpy.ndarray
        An (N, 3) array of magnetometer measurements, where each row represents
        a 3D vector [Mx, My, Mz].
    Returns
    -------
    numpy.ndarray
        A 1D array of length 4: [offset_x, offset_y, offset_z, radius], where
        offset_x, offset_y, and offset_z are the estimated offsets for each axis,
        and radius is the estimated radius of the fitted sphere.
    """
    a_mat = np.column_stack((2 * mag[:, 0], 2 * mag[:, 1], 2 * mag[:, 2], np.ones(mag.shape[0])))
    f = (mag[:, 0] ** 2 + mag[:, 1] ** 2 + mag[:, 2] ** 2).reshape(-1, 1)
    c_vec, *_ = np.linalg.lstsq(a_mat, f, rcond=None)
    c_vec = c_vec.flatten()
    rad = np.sqrt(c_vec[0] ** 2 + c_vec[1] ** 2 + c_vec[2] ** 2 + c_vec[3])
    return cast(
        NDArray[np.float64], np.array([c_vec[0], c_vec[1], c_vec[2], rad], dtype=np.float64)
    )


def compute_pitch(static_accel: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Calculates pitch angles from static acceleration data.
    Parameters
    ----------
    static_accel : np.ndarray
        A 2D NumPy array of shape (n_samples, 3), where each row contains the x, y, and z components
        of the static acceleration vector.
    Returns
    -------
    np.ndarray
        A 1D NumPy array of shape (n_samples,), where each element is the pitch angle (in radians)
        corresponding to the input acceleration vector.
    Notes
    -----
    Pitch is calculated as arctan2(-x, sqrt(y^2 + z^2)).
    """
    return cast(
        NDArray[np.float64],
        np.arctan2(-static_accel[:, 0], np.sqrt(static_accel[:, 1] ** 2 + static_accel[:, 2] ** 2)),
    )


def compute_roll(static_accel: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Calculates roll angles from static acceleration data.
    Parameters
    ----------
    static_accel : np.ndarray
        A 2D NumPy array of shape (n_samples, 3), where each row contains the x, y, and z components
        of the static acceleration vector.
    Returns
    -------
    np.ndarray
        A 1D NumPy array of shape (n_samples,), where each element is the roll angle (in radians)
        corresponding to the input acceleration vector.
    Notes
    -----
    Roll is calculated as arctan2(y, z).
    """
    return cast(NDArray[np.float64], np.arctan2(static_accel[:, 1], static_accel[:, 2]))
