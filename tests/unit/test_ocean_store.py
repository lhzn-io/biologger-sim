# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""The current sampled from a local z-v3 store, without a forcingkit service."""

from pathlib import Path
from typing import Any

import numpy as np
import pytest

from biologger_sim.core.currents import compute_current_drift, make_sampler
from biologger_sim.core.georef import GeoFix, GeoReference
from biologger_sim.core.types import CurrentCorrectionConfig, DeadReckoningConfig
from biologger_sim.processors.lab import PostFactoProcessor

pytest.importorskip("forcingkit_client")
xr = pytest.importorskip("xarray")
pd = pytest.importorskip("pandas")

from biologger_sim.core.ocean_store import OceanStoreSampler  # noqa: E402

T0 = 1660357808.0  # 2022-08-13 02:30:08 UTC
ORIGIN = GeoReference(start=GeoFix(T0, 35.534425, -45.694675))
FREQ = 4


IDENTITY = {
    "model_id": "test-regional",
    "model_label": "Test regional model",
    "model_credit": "Test Observatory",
    "w_source": "model",
    "caveat": "tides too strong near the surface",
}


def _store(root: Path, **extra_attrs: str) -> Path:
    """u = 0.3 + 0.001 z (0.2 m/s at 100 m, 0.298 at the top level), v = 0.05, dry east of -45.5."""
    lon = np.linspace(-45.99, -45.39, 7)
    lat = np.linspace(35.33, 35.83, 6)
    z = np.array([-400.0, -200.0, -100.0, -50.0, -2.0])
    time = pd.date_range("2022-08-13T01:00", periods=4, freq="1h")
    u = np.broadcast_to((0.3 + 0.001 * z)[None, :, None, None], (4, 5, 6, 7)).copy()
    v = np.full(u.shape, 0.05)
    u[..., lon > -45.5] = np.nan
    v[..., lon > -45.5] = np.nan
    path = root / "test_domain_run" / "test_box.zarr"
    xr.Dataset(
        {
            "u": (("time", "z", "lat", "lon"), u.astype(np.float32)),
            "v": (("time", "z", "lat", "lon"), v.astype(np.float32)),
        },
        coords={"time": time, "z": z, "lat": lat, "lon": lon},
        attrs={
            "schema": "z-v3",
            "box": "test_box",
            "run_id": "some-model-test_domain-20261122-222632",
            "donor_commit": "7c90042",
            "source": "a private name",
            **extra_attrs,
        },
    ).to_zarr(path)
    return path


def _track(hours: float = 1.0, depth_m: float = 100.0) -> tuple[np.ndarray, ...]:
    n = int(hours * 3600 * FREQ)
    t = T0 + np.arange(n) / FREQ
    dt = np.full(n, 1.0 / FREQ)
    north = (t - T0) * 1.0  # 1 m/s north, staying west of the dry cells
    east = np.zeros(n)
    return t, dt, north, east, np.full(n, depth_m)


def test_samples_the_store_like_the_service(tmp_path: Path) -> None:
    sampler = OceanStoreSampler(_store(tmp_path))
    t, dt, north, east, depth = _track()
    drift = compute_current_drift(sampler, t, north, east, depth, ORIGIN, dt)
    assert drift.n_missing == 0
    assert drift.drift_east[-1] == pytest.approx(0.2 * 3600, rel=1e-4)
    assert drift.drift_north[-1] == pytest.approx(0.05 * 3600, rel=1e-4)
    assert drift.attrs["forcingkit_ocean_donor"] == "test_box"
    assert drift.attrs["forcingkit_ocean_store_id"] == "test_domain_run/test_box.zarr"
    assert drift.attrs["forcingkit_ocean_store_version"] == "20261122-222632"


def test_surface_takes_the_top_level(tmp_path: Path) -> None:
    sampler = OceanStoreSampler(_store(tmp_path))
    t, dt, north, east, depth = _track(0.25, depth_m=0.0)
    drift = compute_current_drift(sampler, t, north, east, depth, ORIGIN, dt)
    assert drift.n_missing == 0
    assert drift.u == pytest.approx(0.298, rel=1e-5)


def test_dry_cells_are_missing(tmp_path: Path) -> None:
    sampler = OceanStoreSampler(_store(tmp_path))
    lat, lon = ORIGIN.start.lat, -45.42
    ds = sampler.interpolate_trajectory(
        [lon], [lat], np.array(["2022-08-13T02:30"], dtype="datetime64[ms]"), [-100.0]
    )
    assert np.isnan(ds["u"].values).all()


def test_records_only_public_facts(tmp_path: Path) -> None:
    sampler = OceanStoreSampler(_store(tmp_path))
    assert sampler.provenance == {
        "name": "test_box",
        "path": "test_domain_run/test_box.zarr",
        "model_commit": "7c90042",
        "run_time": "20261122-222632",
    }
    kept = " ".join(map(str, sampler.store.attrs.values()))
    assert "private" not in kept and "some-model" not in kept


def test_records_the_model_identity_the_store_publishes(tmp_path: Path) -> None:
    sampler = OceanStoreSampler(_store(tmp_path, **IDENTITY))
    assert {k: sampler.provenance[k] for k in IDENTITY} == IDENTITY
    assert sampler.store.attrs["forcingkit_donor"] == "test-regional"


def test_processor_names_the_model(tmp_path: Path) -> None:
    cfg = CurrentCorrectionConfig(ocean_store=_store(tmp_path, **IDENTITY), max_passes=1)
    proc: Any = PostFactoProcessor(
        dr_cfg=DeadReckoningConfig(current_correction=cfg), georef=ORIGIN
    )
    t, dt, north, east, depth = _track(0.25)
    proc.batch_results = {"pseudo_x": north, "pseudo_y": east, "Depth": depth}
    proc._add_current_drift(t, dt)
    rec = proc.current_correction_record
    assert rec["donor_used"] == "test-regional"
    assert rec["donor_label"] == "Test regional model"
    assert rec["donor_credit"] == "Test Observatory"
    assert rec["donor_caveat"] == "tides too strong near the surface"
    assert rec["w_source"] == "model"


def test_rejects_a_store_without_currents(tmp_path: Path) -> None:
    path = tmp_path / "no_currents.zarr"
    xr.Dataset({"temp": ("x", np.zeros(3))}).to_zarr(path)
    with pytest.raises(ValueError, match="not a z-v3 ocean store"):
        OceanStoreSampler(path)
    with pytest.raises(FileNotFoundError):
        OceanStoreSampler(tmp_path / "absent.zarr")


def test_config_selects_the_store(tmp_path: Path) -> None:
    cfg = CurrentCorrectionConfig(ocean_store=_store(tmp_path))
    assert cfg.enabled
    assert isinstance(make_sampler(cfg), OceanStoreSampler)


def test_processor_records_the_store(tmp_path: Path) -> None:
    cfg = CurrentCorrectionConfig(ocean_store=_store(tmp_path), max_passes=1)
    proc: Any = PostFactoProcessor(
        dr_cfg=DeadReckoningConfig(current_correction=cfg), georef=ORIGIN
    )
    t, dt, north, east, depth = _track(0.25)
    proc.batch_results = {"pseudo_x": north, "pseudo_y": east, "Depth": depth}
    proc._add_current_drift(t, dt)
    rec = proc.current_correction_record
    assert rec["applied"] is True
    assert rec["donor_used"] == "test_box"
    assert "donor_label" not in rec and "w_source" not in rec
    assert rec["ocean_store"]["path"] == "test_domain_run/test_box.zarr"
    assert proc.batch_results["current_u"] == pytest.approx(0.2, rel=1e-4)
