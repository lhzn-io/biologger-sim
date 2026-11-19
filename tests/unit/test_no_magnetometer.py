# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""A tag without a magnetometer has no heading: dead reckoning fails clearly, fixes still work."""

from typing import Any

import numpy as np
import pytest

from biologger_sim.core.georef import GeoFix, GeoReference
from biologger_sim.core.processor_interface import TrackUnavailableError
from biologger_sim.core.types import CurrentCorrectionConfig, DeadReckoningConfig, TrackModel
from biologger_sim.processors.lab import PostFactoProcessor

T0 = 1660182480.0
START = GeoFix(T0, 35.5, -45.7)
_END_LAT, _END_LON = GeoReference(start=START).to_latlon(3000.0, -1000.0)
FIXES = GeoReference(start=START, end=GeoFix(T0 + 3000.0, _END_LAT, _END_LON))


class NeverSampler:
    def __init__(self) -> None:
        self.calls = 0

    def interpolate_trajectory(self, *args: Any, **kwargs: Any) -> Any:
        self.calls += 1
        raise AssertionError("the current must not be sampled without a track")


def _processor(model: TrackModel, sampler: Any = None, url: str | None = None) -> Any:
    proc = PostFactoProcessor(
        tag_id="TAG.NOMAG",
        dr_cfg=DeadReckoningConfig(
            track_model=model, current_correction=CurrentCorrectionConfig(forcingkit_url=url)
        ),
        georef=FIXES,
        current_sampler=sampler,
    )
    n = 3600
    nan = np.full(n, np.nan)
    proc.batch_results = {
        "heading_rad": nan.copy(),
        "heading_deg": nan.copy(),
        "pseudo_x": nan.copy(),
        "pseudo_y": nan.copy(),
        "Depth": np.full(n, 20.0),
    }
    return proc, T0 + np.arange(n, dtype=float)


@pytest.mark.parametrize("model", [TrackModel.DEAD_RECKONING, TrackModel.FIX_PINNED])
def test_dead_reckoned_models_fail_clearly(model: TrackModel) -> None:
    proc, _ = _processor(model)
    with pytest.raises(TrackUnavailableError, match=r"TAG.NOMAG: no heading.*fix_interpolation"):
        proc._require_heading()


def test_fix_interpolation_goes_ahead() -> None:
    proc, t = _processor(TrackModel.FIX_INTERPOLATION)
    proc._require_heading()
    proc._place_track(t)
    res = proc.batch_results
    assert np.isfinite(res["pseudo_x"]).all()
    assert proc.track_quality["end_fix_miss_before_placement_m"] is None
    assert proc.track_quality["end_fix_miss_m"] == pytest.approx(0.0, abs=1e-6)


def test_current_is_not_sampled_without_a_track() -> None:
    sampler = NeverSampler()
    proc, t = _processor(TrackModel.FIX_INTERPOLATION, sampler, "http://fk.test")
    proc._add_current_drift(t, np.ones(len(t)))
    assert sampler.calls == 0
    rec = proc.current_correction_record
    assert rec["configured"] and not rec["applied"]
    assert "no heading" in rec["error"]


def test_a_heading_passes_the_check() -> None:
    proc, _ = _processor(TrackModel.DEAD_RECKONING)
    proc.batch_results["heading_rad"][10] = 0.5
    proc._require_heading()
