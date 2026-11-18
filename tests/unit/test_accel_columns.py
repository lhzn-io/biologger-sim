# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""The static and dynamic acceleration a bundle carries. Positions and times are synthetic."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from biologger_sim.core.georef import GeoFix, GeoReference
from biologger_sim.io.track_bundle import (
    ACCEL_COLUMNS,
    COLUMNS,
    VEDBA_UNIT_LAB,
    Provenance,
    read_bundle,
    write_bundle,
)

T0 = 1_700_000_000.0
ORIGIN = GeoReference(start=GeoFix(T0, 10.0, -30.0))
FREQ = 4


def _rows(n: int = 40, with_accel: bool = True) -> pd.DataFrame:
    s = np.arange(n) / FREQ
    df: pd.DataFrame = pd.DataFrame(
        {
            "timestamp": T0 + s,
            "pseudo_x": s,
            "pseudo_y": np.zeros(n),
            "Depth": np.full(n, 5.0),
            "heading_degrees": np.zeros(n),
        }
    )
    if with_accel:
        df["X_Static"], df["Y_Static"], df["Z_Static"] = 1.0, 2.0, 9.0
        df["X_Dynamic"] = s  # distinct per record, to check the value at sample time
        df["Y_Dynamic"], df["Z_Dynamic"] = -0.5, 0.25
    return df


def _write(tmp_path: Path, rows: pd.DataFrame, unit: str = VEDBA_UNIT_LAB) -> dict:
    prov = Provenance(deployment_id="SYN001", sim_id="syn", run_id="r1", vedba_unit=unit)
    return write_bundle(tmp_path, rows, ORIGIN, prov, rate_hz=1.0)


def test_written_after_the_fixed_columns_with_the_runs_unit(tmp_path: Path) -> None:
    meta = _write(tmp_path, _rows())
    names = [c["name"] for c in meta["columns"]]
    assert names == [n for n, _, _ in COLUMNS] + list(ACCEL_COLUMNS)
    units = {c["name"]: c["unit"] for c in meta["columns"]}
    assert {units[n] for n in ACCEL_COLUMNS} == {VEDBA_UNIT_LAB}
    described = [c["description"] for c in meta["columns"] if c["name"] in ACCEL_COLUMNS]
    assert len(described) == 6 and all("forward-right-down" in d for d in described)


def test_unit_follows_the_run(tmp_path: Path) -> None:
    meta = _write(tmp_path, _rows(), unit="g")
    assert {c["unit"] for c in meta["columns"] if c["name"] in ACCEL_COLUMNS} == {"g"}


def test_values_at_sample_time(tmp_path: Path) -> None:
    meta = _write(tmp_path, _rows())
    _, cols = read_bundle(tmp_path)
    n = meta["count"]
    assert cols["accel_static_z"] == pytest.approx(np.full(n, 9.0))
    assert cols["accel_dynamic_y"] == pytest.approx(np.full(n, -0.5))
    # Output samples are native records 0, 4, 8, ...: dynamic x there is 0, 1, 2, ... (record / 4).
    assert cols["accel_dynamic_x"] == pytest.approx(np.arange(n, dtype=float))


def test_absent_without_the_source_columns(tmp_path: Path) -> None:
    meta = _write(tmp_path, _rows(with_accel=False))
    names = {c["name"] for c in meta["columns"]}
    assert names.isdisjoint(ACCEL_COLUMNS)
