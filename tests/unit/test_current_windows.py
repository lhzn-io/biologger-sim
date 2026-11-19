# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""The current is requested in time windows, so each forcing store stays small."""

from typing import Any

import numpy as np
import pytest

from biologger_sim.core.currents import compute_current_drift, release_memory, time_windows
from biologger_sim.core.georef import GeoFix, GeoReference

T0 = 1660357808.0
ORIGIN = GeoReference(start=GeoFix(T0, 35.534425, -45.694675))


class _V:
    def __init__(self, values: np.ndarray) -> None:
        self.values = values


class _Ds(dict[str, Any]):
    """Stands in for the CF trajectory Dataset: ds["u"].values and ds.attrs."""

    def __init__(self, attrs: dict[str, str], **variables: _V) -> None:
        super().__init__(**variables)
        self.attrs = attrs


class WindowSampler:
    """u is the request's start hour; each request reports its own store id."""

    def __init__(self) -> None:
        self.calls: list[np.ndarray] = []

    def interpolate_trajectory(
        self, lon: Any, lat: Any, time: Any, z: Any = None, **kw: Any
    ) -> _Ds:
        times = np.asarray(time)
        self.calls.append(times)
        n = len(lon)
        store = f"obc_{len(self.calls)}"

        attrs = {"forcingkit_ocean_donor": "necofs", "forcingkit_ocean_store_id": store}
        return _Ds(attrs, u=_V(np.full(n, 0.1 * len(self.calls))), v=_V(np.zeros(n)))


def _track(hours: float) -> tuple[np.ndarray, ...]:
    n = int(hours * 3600)
    t = T0 + np.arange(n, dtype=np.float64)
    return t, np.ones(n), np.zeros(n), np.zeros(n)


def test_time_windows_cover_every_index_once() -> None:
    t = T0 + np.arange(0.0, 20 * 3600.0, 60.0, dtype=np.float64)
    windows = time_windows(t, 6 * 3600.0)
    assert len(windows) == 4  # 0-6, 6-12, 12-18, 18-20 h
    covered = np.concatenate([np.arange(len(t))[w] for w in windows])
    np.testing.assert_array_equal(covered, np.arange(len(t)))
    assert all(t[w][-1] - t[w][0] < 6 * 3600.0 for w in windows)
    assert time_windows(np.zeros(0), 60.0) == []


def test_one_request_per_window_in_order() -> None:
    t, dt, north, east = _track(13.0)
    sampler = WindowSampler()
    drift = compute_current_drift(sampler, t, north, east, None, ORIGIN, dt, window_s=6 * 3600.0)
    assert len(sampler.calls) == 3
    assert all(c[-1] - c[0] < np.timedelta64(6 * 3600, "s") for c in sampler.calls)
    # Each window's own values land on its own records.
    assert drift.u[0] == pytest.approx(0.1)
    assert drift.u[7 * 3600] == pytest.approx(0.2)
    assert drift.u[-1] == pytest.approx(0.3)
    assert drift.n_samples == sum(len(c) for c in sampler.calls)
    # The donor is reported once; the per-window stores are all named.
    assert drift.attrs["forcingkit_ocean_donor"] == "necofs"
    assert drift.attrs["forcingkit_ocean_store_id"] == "obc_1, obc_2, obc_3"


def test_no_window_is_one_request() -> None:
    t, dt, north, east = _track(13.0)
    sampler = WindowSampler()
    compute_current_drift(sampler, t, north, east, None, ORIGIN, dt, window_s=None)
    assert len(sampler.calls) == 1


def test_release_memory_is_safe_to_call() -> None:
    release_memory()
