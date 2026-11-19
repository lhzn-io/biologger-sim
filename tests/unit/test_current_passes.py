# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""The current is sampled where the placed track is, and pinning leaves the current unrotated."""

import math
from typing import Any, ClassVar

import numpy as np
import pytest

from biologger_sim.core.georef import EARTH_RADIUS_M, GeoFix, GeoReference
from biologger_sim.core.track_models import apply_track_model, fix_pinning_factor
from biologger_sim.core.types import CurrentCorrectionConfig, DeadReckoningConfig, TrackModel
from biologger_sim.processors.lab import PostFactoProcessor

T0 = 1660357808.0
FREQ = 16
START = GeoFix(T0, 35.534425, -45.694675)
_ORIGIN = GeoReference(start=START)
# An end fix 2 km north and 2 km west of the start, 3500 s later.
_END_LAT, _END_LON = _ORIGIN.to_latlon(2000.0, -2000.0)
FIXES = GeoReference(start=START, end=GeoFix(T0 + 3500.0, _END_LAT, _END_LON))


def _east_m(lon: np.ndarray) -> np.ndarray:
    lon_m = EARTH_RADIUS_M * math.cos(math.radians(START.lat))
    return np.radians(np.asarray(lon) - START.lon) * lon_m


class FieldSampler:
    """An eastward current that weakens to the west: u = 0.1 + 2e-5 * east (m/s), v = 0."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def interpolate_trajectory(
        self, lon: Any, lat: Any, time: Any, z: Any = None, **kw: Any
    ) -> Any:
        self.calls.append({"lon": np.asarray(lon), "lat": np.asarray(lat)})
        u = 0.1 + 2e-5 * _east_m(lon)

        class _V:
            def __init__(self, values: np.ndarray) -> None:
                self.values = values

        class _Ds(dict[str, Any]):
            attrs: ClassVar[dict[str, str]] = {"forcingkit_ocean_donor": "field"}

        return _Ds(u=_V(u), v=_V(np.zeros(len(u))))


def _water(hours: float = 1.0) -> tuple[np.ndarray, ...]:
    n = int(hours * 3600 * FREQ)
    t = T0 + np.arange(n) / FREQ
    dt = np.full(n, 1.0 / FREQ)
    s = t - T0
    return t, dt, s.copy(), 300.0 * np.sin(s / 900.0)  # 1 m/s north, with a wiggle


class TestPinningWithDrift:
    def test_meets_both_fixes(self) -> None:
        t, _, n, e = _water()
        dn, de = np.zeros(len(t)), 0.2 * (t - T0)
        out_n, out_e, used = apply_track_model(TrackModel.FIX_PINNED, t, n, e, FIXES, dn, de)
        end = FIXES.end_ne()
        assert used == TrackModel.FIX_PINNED and end is not None
        assert (np.interp(T0, t, out_n), np.interp(T0, t, out_e)) == pytest.approx((0, 0), abs=1e-6)
        assert (
            np.interp(FIXES.end.t, t, out_n),  # type: ignore[union-attr]
            np.interp(FIXES.end.t, t, out_e),  # type: ignore[union-attr]
        ) == pytest.approx(end, abs=1e-6)

    def test_rotates_only_the_water_track(self) -> None:
        t, _, n, e = _water()
        dn, de = np.zeros(len(t)), 0.2 * (t - T0)
        k = fix_pinning_factor(t, n, e, FIXES, dn, de)
        assert k is not None
        out_n, out_e, _ = apply_track_model(TrackModel.FIX_PINNED, t, n, e, FIXES, dn, de)
        # Taking the drift back out leaves the water track turned and scaled by k alone.
        water_placed = (out_n - dn) + 1j * (out_e - de)
        np.testing.assert_allclose(water_placed, k * (n + 1j * e), atol=1e-6)

    def test_without_drift_matches_the_plain_model(self) -> None:
        t, _, n, e = _water()
        zeros = np.zeros(len(t))
        for model in TrackModel:
            plain = apply_track_model(model, t, n, e, FIXES)
            with_zero = apply_track_model(model, t, n, e, FIXES, zeros, zeros)
            np.testing.assert_allclose(plain[0], with_zero[0], atol=1e-9)
            np.testing.assert_allclose(plain[1], with_zero[1], atol=1e-9)
        assert fix_pinning_factor(t, n, e, FIXES) == pytest.approx(
            fix_pinning_factor(t, n, e, FIXES, zeros, zeros)
        )

    def test_dead_reckoning_adds_the_drift(self) -> None:
        t, _, n, e = _water()
        dn, de = np.full(len(t), 5.0), np.full(len(t), -3.0)
        out_n, out_e, _ = apply_track_model(TrackModel.DEAD_RECKONING, t, n, e, FIXES, dn, de)
        np.testing.assert_allclose(out_n, n + 5.0)
        np.testing.assert_allclose(out_e, e - 3.0)


def _run(cfg: CurrentCorrectionConfig, model: TrackModel) -> tuple[Any, FieldSampler, np.ndarray]:
    sampler = FieldSampler()
    proc = PostFactoProcessor(
        dr_cfg=DeadReckoningConfig(track_model=model, current_correction=cfg),
        georef=FIXES,
        current_sampler=sampler,
    )
    t, dt, n, e = _water()
    proc.batch_results = {"pseudo_x": n, "pseudo_y": e, "Depth": np.full(len(t), 50.0)}
    proc._add_current_drift(t, dt)
    proc._place_track(t)
    return proc, sampler, t


class TestSamplingPasses:
    def test_pinned_track_samples_where_it_is_placed(self) -> None:
        cfg = CurrentCorrectionConfig(forcingkit_url="http://fk.test")
        proc, sampler, t = _run(cfg, TrackModel.FIX_PINNED)
        rec = proc.current_correction_record
        assert rec["applied"] and rec["converged"]
        assert 2 <= rec["passes"] == len(sampler.calls) <= cfg.max_passes
        assert rec["pass_shift_max_m"][-1] <= cfg.convergence_m
        # The last pass sampled within convergence_m of the final placed track.
        res = proc.batch_results
        last = sampler.calls[-1]
        idx = np.searchsorted(t, t[0] + 60.0 * np.arange(len(last["lon"]) - 1))
        placed_e = res["pseudo_y"][idx]
        assert np.max(np.abs(_east_m(last["lon"][:-1]) - placed_e)) <= cfg.convergence_m
        # The first pass sampled along the water track, which never goes west of 300 m.
        assert _east_m(sampler.calls[0]["lon"]).min() >= -300.5
        assert proc.track_model_used == TrackModel.FIX_PINNED

    def test_dead_reckoned_track_also_iterates(self) -> None:
        cfg = CurrentCorrectionConfig(forcingkit_url="http://fk.test")
        proc, _, _ = _run(cfg, TrackModel.DEAD_RECKONING)
        rec = proc.current_correction_record
        assert rec["converged"] and rec["passes"] >= 2
        res = proc.batch_results
        drift = proc.current_drift
        np.testing.assert_allclose(res["pseudo_y"], res["pseudo_y_water"] + drift.drift_east)

    def test_one_pass_samples_the_water_track_only(self) -> None:
        cfg = CurrentCorrectionConfig(forcingkit_url="http://fk.test", max_passes=1)
        proc, sampler, _ = _run(cfg, TrackModel.FIX_PINNED)
        assert len(sampler.calls) == 1
        assert proc.current_correction_record["passes"] == 1
        assert not proc.current_correction_record["converged"]
