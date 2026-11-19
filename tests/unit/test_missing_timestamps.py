# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Post-facto dead reckoning needs one timestamp per accelerometer sample, or it fails clearly."""

import numpy as np
import pytest

from biologger_sim.core.processor_interface import TrackUnavailableError
from biologger_sim.processors.lab import PostFactoProcessor

T0 = 1660182480.0
FREQ = 16


def _processor(n_timestamps: int, n: int = 320) -> PostFactoProcessor:
    """A batch of a level tag turning slowly, with ``n_timestamps`` timestamps recorded."""
    proc = PostFactoProcessor(
        tag_id="TAG.NOTS",
        freq=FREQ,
        r_exact_mode=True,
        compute_attachment_angles=True,
        compute_mag_offsets=True,
    )
    theta = np.linspace(0.0, 4.0 * np.pi, n)
    assert proc.batch_accel_data is not None
    assert proc.batch_mag_data is not None
    assert proc.batch_timestamps is not None
    proc.batch_accel_data.extend([[0.0, 0.0, 10.0]] * n)
    proc.batch_mag_data.extend(
        [[float(np.cos(t)), float(np.sin(t)), 0.5 * float(np.sin(2.0 * t))] for t in theta]
    )
    proc.batch_timestamps.extend((T0 + np.arange(n_timestamps) / FREQ).tolist())
    return proc


@pytest.mark.parametrize("n_timestamps", [0, 319])
def test_missing_or_short_timestamps_fail_clearly(n_timestamps: int) -> None:
    proc = _processor(n_timestamps)
    with pytest.raises(TrackUnavailableError, match=r"TAG.NOTS: the batch has no timestamps"):
        proc.calibrate_from_batch_data()


def test_matching_timestamps_give_a_track() -> None:
    proc = _processor(320)
    proc.calibrate_from_batch_data()
    assert proc.batch_results is not None
    assert np.isfinite(proc.batch_results["pseudo_x"]).all()
