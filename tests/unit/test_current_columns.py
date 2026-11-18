# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""The current and speed columns a bundle carries, and the dead-reckoning step's record.

Positions and times are synthetic (an origin in open ocean far from any deployment).
"""

from pathlib import Path
from typing import Any, ClassVar

import numpy as np
import pandas as pd
import pytest

from biologger_sim.core.currents import compute_current_drift
from biologger_sim.core.georef import GeoFix, GeoReference
from biologger_sim.core.types import CurrentCorrectionConfig, DeadReckoningConfig, SpeedModel
from biologger_sim.io.track_bundle import (
    COLUMNS,
    OPTIONAL_COLUMNS,
    Provenance,
    read_bundle,
    write_bundle,
)
from biologger_sim.processors.lab import PostFactoProcessor

T0 = 1_700_000_000.0
ORIGIN = GeoReference(start=GeoFix(T0, 10.0, -30.0))
FREQ = 4


class _Var:
    def __init__(self, values: np.ndarray) -> None:
        self.values = values


class _Trajectory(dict[str, _Var]):
    attrs: ClassVar[dict[str, str]] = {"forcingkit_ocean_donor": "fake"}


class FakeSampler:
    """A uniform current with an optional run of missing samples."""

    def __init__(self, missing: slice | None = None) -> None:
        self.missing = missing

    def interpolate_trajectory(
        self, lon: Any, lat: Any, time: Any, z: Any = None, **kwargs: Any
    ) -> _Trajectory:
        u = np.full(len(lon), 0.3)
        v = np.full(len(lon), -0.4)
        if self.missing is not None:
            u[self.missing] = np.nan
            v[self.missing] = np.nan
        return _Trajectory(u=_Var(u), v=_Var(v))


def _track(minutes: int = 10) -> tuple[np.ndarray, ...]:
    n = minutes * 60 * FREQ
    t = T0 + np.arange(n) / FREQ
    dt = np.full(n, 1.0 / FREQ)
    north = np.cumsum(dt)
    return t, dt, north, np.zeros(n), np.full(n, 50.0)


class TestMissingMask:
    def test_marks_records_that_lean_on_a_missing_sample(self) -> None:
        t, dt, north, east, depth = _track()
        # Samples are one a minute plus the last record: 11; the last three are missing.
        drift = compute_current_drift(
            FakeSampler(missing=slice(8, None)), t, north, east, depth, ORIGIN, dt
        )
        assert drift.n_missing == 3
        first_bad = np.flatnonzero(drift.missing)[0]
        # Records strictly between samples 7 and 8 already interpolate toward still water.
        assert t[first_bad] == pytest.approx(T0 + 7 * 60 + 1 / FREQ)
        assert drift.missing[first_bad:].all()
        assert not drift.missing[:first_bad].any()

    def test_none_missing(self) -> None:
        t, dt, north, east, depth = _track()
        drift = compute_current_drift(FakeSampler(), t, north, east, depth, ORIGIN, dt)
        assert not drift.missing.any()
        assert drift.missing.shape == t.shape


def _rows(n: int = 40, with_current: bool = True) -> pd.DataFrame:
    s = np.arange(n) / FREQ
    df: pd.DataFrame = pd.DataFrame(
        {
            "timestamp": T0 + s,
            "pseudo_x": s,
            "pseudo_y": np.zeros(n),
            "Depth": np.full(n, 5.0),
            "heading_degrees": np.zeros(n),
            "speed_through_water": np.full(n, 1.0),
        }
    )
    if with_current:
        df["current_u"] = 0.3
        df["current_v"] = -0.4
        missing = np.zeros(n)
        missing[9] = 1.0  # one native record, at t = 2.25 s
        df["current_missing"] = missing
    return df


class TestBundleColumns:
    def write(self, tmp_path: Path, rows: pd.DataFrame) -> dict[str, Any]:
        prov = Provenance(deployment_id="SYN001", sim_id="syn", run_id="r1")
        return write_bundle(tmp_path, rows, ORIGIN, prov, rate_hz=1.0)

    def test_written_after_the_fixed_columns(self, tmp_path: Path) -> None:
        meta = self.write(tmp_path, _rows())
        names = [c["name"] for c in meta["columns"]]
        assert names == [n for n, _, _ in COLUMNS] + [n for n, _, _ in OPTIONAL_COLUMNS]
        units = {c["name"]: c["unit"] for c in meta["columns"]}
        assert units["current_east_m_s"] == "m/s" and units["current_missing"] == "flag"
        optional = {n for n, _, _ in OPTIONAL_COLUMNS}
        assert all("description" in c for c in meta["columns"] if c["name"] in optional)
        _, cols = read_bundle(tmp_path)
        assert cols["current_east_m_s"] == pytest.approx(np.full(meta["count"], 0.3))
        assert cols["current_north_m_s"] == pytest.approx(np.full(meta["count"], -0.4))
        assert cols["speed_m_s"] == pytest.approx(np.full(meta["count"], 1.0))

    def test_missing_flag_marks_the_stretch(self, tmp_path: Path) -> None:
        self.write(tmp_path, _rows())
        _, cols = read_bundle(tmp_path)
        # Output samples are native records 0, 4, 8, ...; record 9 (t = 2.25 s) lies between
        # output samples 2 and 3, so sample 3 carries the flag for that stretch.
        assert list(cols["current_missing"]) == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

    def test_absent_without_a_correction(self, tmp_path: Path) -> None:
        meta = self.write(tmp_path, _rows(with_current=False))
        names = [c["name"] for c in meta["columns"]]
        assert "current_east_m_s" not in names and "current_missing" not in names
        assert names[-1] == "speed_m_s"
        raw = (tmp_path / "track.f32").read_bytes()
        assert len(raw) == len(names) * meta["count"] * 4 == meta["data"]["bytes"]


class TestProcessorColumns:
    def test_current_missing_reaches_the_batch(self) -> None:
        proc = PostFactoProcessor(
            dr_cfg=DeadReckoningConfig(
                current_correction=CurrentCorrectionConfig(forcingkit_url="http://fk.test")
            ),
            georef=ORIGIN,
            current_sampler=FakeSampler(missing=slice(8, None)),
        )
        t, dt, north, east, depth = _track()
        proc.batch_results = {"pseudo_x": north, "pseudo_y": east, "Depth": depth}
        proc._add_current_drift(t, dt)
        flag = proc.batch_results["current_missing"]
        assert flag.dtype == np.float64
        assert flag[0] == 0.0 and flag[-1] == 1.0


class TestDeadReckoningStep:
    def step(self, cfg: DeadReckoningConfig) -> dict[str, Any]:
        record = PostFactoProcessor(dr_cfg=cfg).provenance_record()
        return next(s for s in record["pipeline"] if s["step"] == "dead_reckoning")

    def test_records_the_constant_speed_actually_used(self) -> None:
        s = self.step(DeadReckoningConfig(speed_model=SpeedModel.ODBA_SCALED))
        assert s["method"] == "constant"
        assert s["params"]["constant_speed_m_s"] == 1.0
        assert s["params"]["configured_speed_model"] == "odba_scaled"
        assert "odba_speed_factor" not in s["params"]

    def test_constant_configured(self) -> None:
        s = self.step(DeadReckoningConfig(speed_model=SpeedModel.CONSTANT, constant_speed_m_s=0.8))
        assert s["method"] == "constant"
        assert s["params"]["constant_speed_m_s"] == 0.8
        assert "configured_speed_model" not in s["params"]
