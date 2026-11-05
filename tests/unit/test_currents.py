# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Tests for the ocean-current drift correction; no forcingkit service needed."""

from typing import Any, ClassVar

import numpy as np
import pytest

from biologger_sim.core.currents import compute_current_drift, thin_indices
from biologger_sim.core.georef import GeoFix, GeoReference
from biologger_sim.core.types import CurrentCorrectionConfig, DeadReckoningConfig
from biologger_sim.processors.lab import PostFactoProcessor

T0 = 1660357808.0  # RED001 start fix, 2022-08-13 02:30:08 UTC
ORIGIN = GeoReference(start=GeoFix(T0, 39.904425, -69.504675))
FREQ = 16


class _Var:
    def __init__(self, values: np.ndarray) -> None:
        self.values = values


class _Trajectory(dict[str, _Var]):
    """Stands in for the CF trajectory Dataset: ds["u"].values and ds.attrs."""

    attrs: ClassVar[dict[str, str]] = {
        "forcingkit_ocean_donor": "fake",
        "forcingkit_ocean_store_id": "obc_test",
    }


class FakeSampler:
    """A uniform current, recording every call."""

    def __init__(self, u: float = 0.2, v: float = -0.1, missing: slice | None = None) -> None:
        self.u, self.v, self.missing = u, v, missing
        self.calls: list[dict[str, Any]] = []

    def interpolate_trajectory(
        self, lon: Any, lat: Any, time: Any, z: Any = None, **kwargs: Any
    ) -> _Trajectory:
        self.calls.append({"lon": lon, "lat": lat, "time": time, "z": z, **kwargs})
        u = np.full(len(lon), self.u)
        v = np.full(len(lon), self.v)
        if self.missing is not None:
            u[self.missing] = np.nan
            v[self.missing] = np.nan
        return _Trajectory(u=_Var(u), v=_Var(v))


def _track(hours: float = 1.0) -> tuple[np.ndarray, ...]:
    n = int(hours * 3600 * FREQ)
    t = T0 + np.arange(n) / FREQ
    dt = np.full(n, 1.0 / FREQ)
    north = np.cumsum(np.full(n, 1.0) * dt)  # 1 m/s due north through the water
    east = np.zeros(n)
    depth = np.linspace(-0.5, 200.0, n)  # starts with a surface excursion
    return t, dt, north, east, depth


class TestThinning:
    def test_one_per_minute_with_both_ends(self) -> None:
        t = T0 + np.arange(int(9.2 * 3600 * FREQ)) / FREQ
        idx = thin_indices(t, 60.0)
        assert idx[0] == 0 and idx[-1] == len(t) - 1
        assert len(idx) == pytest.approx(9.2 * 60, abs=2)
        assert np.all(np.diff(t[idx]) <= 60.0 + 1e-6)

    def test_empty(self) -> None:
        assert len(thin_indices(np.zeros(0), 60.0)) == 0


class TestComputeDrift:
    def test_uniform_current_integrates_exactly(self) -> None:
        t, dt, north, east, depth = _track()
        drift = compute_current_drift(FakeSampler(), t, north, east, depth, ORIGIN, dt)
        assert drift.drift_east[-1] == pytest.approx(0.2 * 3600, rel=1e-9)
        assert drift.drift_north[-1] == pytest.approx(-0.1 * 3600, rel=1e-9)
        assert drift.n_missing == 0
        assert drift.attrs["forcingkit_ocean_donor"] == "fake"

    def test_request_geometry(self) -> None:
        t, dt, north, east, depth = _track()
        sampler = FakeSampler()
        compute_current_drift(sampler, t, north, east, depth, ORIGIN, dt)
        call = sampler.calls[0]
        assert len(call["lon"]) == 61  # one a minute plus the last record
        assert call["variables"] == ("u", "v")
        # z is metres positive up: the animal's depth is negative, surface excursions clamp to 0
        assert np.all(call["z"] <= 0.0)
        assert call["z"][0] == 0.0
        assert call["z"][-1] == pytest.approx(-200.0)
        # positions come from the dead-reckoned track: 3.6 km north after an hour
        assert call["lat"][0] == pytest.approx(ORIGIN.start.lat)
        assert call["lat"][-1] == pytest.approx(ORIGIN.to_latlon(3600.0, 0.0)[0], abs=1e-4)
        assert call["time"][0] == np.datetime64("2022-08-13T02:30:08.000", "ms")

    def test_missing_samples_are_still_water(self) -> None:
        t, dt, north, east, depth = _track()
        drift = compute_current_drift(
            FakeSampler(missing=slice(30, None)), t, north, east, depth, ORIGIN, dt
        )
        assert drift.n_missing == 31
        assert 0.0 < drift.drift_east[-1] < 0.2 * 3600 * 0.55

    def test_all_missing_raises(self) -> None:
        t, dt, north, east, depth = _track(0.1)
        with pytest.raises(ValueError, match="no current"):
            compute_current_drift(
                FakeSampler(missing=slice(None)), t, north, east, depth, ORIGIN, dt
            )


def _processor(cfg: CurrentCorrectionConfig, sampler: Any, georef: Any = ORIGIN) -> Any:
    proc = PostFactoProcessor(
        dr_cfg=DeadReckoningConfig(current_correction=cfg),
        georef=georef,
        current_sampler=sampler,
    )
    t, dt, north, east, depth = _track(0.25)
    proc.batch_results = {"pseudo_x": north, "pseudo_y": east, "Depth": depth}
    proc._add_current_drift(t, dt)
    return proc


class TestProcessor:
    def test_off_without_url(self) -> None:
        cfg = CurrentCorrectionConfig()
        assert not cfg.enabled
        sampler = FakeSampler()
        proc = _processor(cfg, sampler)
        assert sampler.calls == []
        assert "current_u" not in proc.batch_results

    def test_applies_drift_and_keeps_water_track(self) -> None:
        proc = _processor(CurrentCorrectionConfig(forcingkit_url="http://fk.test"), FakeSampler())
        res = proc.batch_results
        assert res["pseudo_y"][-1] - res["pseudo_y_water"][-1] == pytest.approx(0.2 * 900)
        assert res["pseudo_x"][-1] - res["pseudo_x_water"][-1] == pytest.approx(-0.1 * 900)
        assert np.all(res["current_u"] == pytest.approx(0.2))
        assert proc.current_drift is not None

    def test_failure_leaves_track_uncorrected(self) -> None:
        proc = _processor(
            CurrentCorrectionConfig(forcingkit_url="http://fk.test"),
            FakeSampler(missing=slice(None)),
        )
        assert "pseudo_x_water" not in proc.batch_results
        assert proc.current_drift is None

    def test_needs_start_fix(self) -> None:
        sampler = FakeSampler()
        _processor(CurrentCorrectionConfig(forcingkit_url="http://fk.test"), sampler, georef=None)
        assert sampler.calls == []


class TestWithForcingkitClient:
    """The real client's interpolation against a synthetic z-v3 store (no network)."""

    def test_interpolates_store_along_track(self) -> None:
        pytest.importorskip("forcingkit_client")
        import pandas as pd
        import xarray as xr
        from forcingkit_client.trajectory import interpolate_trajectory

        # u varies with depth only, v is constant: linear interpolation reproduces both.
        lon = np.linspace(-69.8, -69.2, 7)
        lat = np.linspace(39.7, 40.2, 6)
        z = np.array([-400.0, -200.0, -100.0, -50.0, 0.0])
        time = pd.date_range("2022-08-13T01:00", periods=4, freq="1h")
        u = np.broadcast_to((0.3 + 0.001 * z)[None, :, None, None], (4, 5, 6, 7))
        store = xr.Dataset(
            {
                "u": (("time", "z", "lat", "lon"), u.astype(np.float32)),
                "v": (("time", "z", "lat", "lon"), np.full(u.shape, 0.05, np.float32)),
            },
            coords={"time": time, "z": z, "lat": lat, "lon": lon},
            attrs={"schema": "z-v3", "forcingkit_store_id": "obc_synthetic"},
        )

        class StoreClient:
            def __init__(self) -> None:
                self.requests: list[tuple[Any, ...]] = []

            def ocean(self, bbox: Any, start: Any, hours: Any, **options: Any) -> xr.Dataset:
                self.requests.append((bbox, start, hours, options))
                return store

            def interpolate_trajectory(
                self, lon: Any, lat: Any, time: Any, z: Any = None, **kw: Any
            ) -> Any:
                return interpolate_trajectory(self, lon, lat, time, z, **kw)  # type: ignore[arg-type]

        t, dt, north, east, _ = _track(1.0)
        depth = np.full(len(t), 100.0)  # u = 0.2 m/s at z = -100
        client = StoreClient()
        drift = compute_current_drift(
            client, t, north, east, depth, ORIGIN, dt, vertical_spacing_m=10.0
        )
        assert drift.n_missing == 0
        assert drift.drift_east[-1] == pytest.approx(0.2 * 3600, rel=1e-4)
        assert drift.drift_north[-1] == pytest.approx(0.05 * 3600, rel=1e-4)
        assert client.requests[0][3] == {"vertical_spacing_m": 10.0}
        assert drift.attrs["forcingkit_ocean_store_id"] == "obc_synthetic"
