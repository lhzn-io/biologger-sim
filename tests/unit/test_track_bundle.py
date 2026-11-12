# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Tests for track bundles (track.json, track.f32, track.geojson) and run back-fill."""

import json
import math
import struct
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from biologger_sim.core.georef import GeoFix, GeoReference
from biologger_sim.io.track_bundle import (
    COLUMNS,
    SCHEMA,
    Provenance,
    decimate,
    douglas_peucker,
    read_bundle,
    to_latlon,
    write_bundle,
)
from biologger_sim.io.track_export import (
    TRACK_META_SUFFIX,
    bundles_from_run,
    track_meta_from_log,
)

# RED001 fixes from biologger_meta.csv
T0 = 1660357807.999992
T1 = 1660391340.0
RED001 = GeoReference(
    start=GeoFix(T0, 39.904425, -69.504675),
    end=GeoFix(T1, 39.8845, -69.6602),
)

META_HEADER = (
    "time_start_utc,species,start_lat,start_lon,start_location_time,tag_id,"
    "time_end_utc,end_lat,end_lon\n"
)


def output_rows(n: int = 160, rate_hz: float = 16.0, t_start: float = T0) -> pd.DataFrame:
    """A small <sim_id>_output.csv: a 1 m/s swim north-east with a slow dive."""
    t = t_start + np.arange(n) / rate_hz
    s = np.arange(n) / rate_hz
    df: pd.DataFrame = pd.DataFrame(
        {
            "record_count": np.arange(1, n + 1),
            "timestamp": t,
            "Depth": 2.0 + 0.1 * s,
            "VeDBA": np.full(n, 0.5),
            "pitch_degrees": np.full(n, -10.0),
            "roll_degrees": np.full(n, 3.0),
            "heading_degrees": np.full(n, 45.0),
            "pseudo_x": s * math.cos(math.radians(45.0)),
            "pseudo_y": s * math.sin(math.radians(45.0)),
        }
    )
    return df


class TestLatLon:
    def test_round_trip_within_10_cm(self) -> None:
        grid = np.linspace(-50_000.0, 50_000.0, 21)
        north, east = (a.ravel() for a in np.meshgrid(grid, grid))
        lat, lon = to_latlon(RED001, north, east)
        for n, e, la, lo in zip(north, east, lat, lon, strict=True):
            n2, e2 = RED001.to_ne(float(la), float(lo))
            assert math.hypot(n2 - n, e2 - e) < 0.1

    def test_matches_scalar(self) -> None:
        lat, lon = to_latlon(RED001, np.array([1234.5]), np.array([-678.9]))
        assert (lat[0], lon[0]) == RED001.to_latlon(1234.5, -678.9)


class TestDecimate:
    def test_16_hz_to_1_hz_keeps_first_of_each_second(self) -> None:
        t = 100.0 + np.arange(160) / 16.0
        idx = decimate(t, 1.0)
        assert list(idx) == list(range(0, 160, 16))

    def test_rate_at_or_above_native_keeps_all(self) -> None:
        t = np.arange(50) / 16.0
        assert len(decimate(t, 16.0)) == 50
        assert len(decimate(t, 100.0)) == 50

    def test_gap_skips_empty_bins(self) -> None:
        t = np.array([0.0, 0.5, 1.0, 1.5, 10.0, 10.5])
        assert list(decimate(t, 1.0)) == [0, 2, 4]

    def test_rejects_non_positive_rate(self) -> None:
        with pytest.raises(ValueError):
            decimate(np.arange(3.0), 0.0)


class TestDouglasPeucker:
    def test_straight_line_keeps_ends(self) -> None:
        x = np.linspace(0, 1000, 500)
        y = 2.0 * np.sin(x)  # wobble under the 5 m tolerance
        assert list(douglas_peucker(x, y, 5.0)) == [0, 499]

    def test_corner_is_kept(self) -> None:
        x = np.concatenate([np.linspace(0, 100, 51), np.full(50, 100.0)])
        y = np.concatenate([np.zeros(51), np.linspace(2, 100, 50)])
        assert list(douglas_peucker(x, y, 5.0)) == [0, 50, 100]

    def test_short_inputs(self) -> None:
        assert list(douglas_peucker(np.zeros(1), np.zeros(1), 5.0)) == [0]
        assert list(douglas_peucker(np.zeros(2), np.ones(2), 5.0)) == [0, 1]


class TestWriteBundle:
    def write(self, tmp_path: Path, georef: GeoReference | None = RED001) -> dict:
        prov = Provenance(deployment_id="RED001_20220812", sim_id="sword", run_id="r1")
        return write_bundle(tmp_path, output_rows(), georef, prov, rate_hz=1.0)

    def test_byte_layout(self, tmp_path: Path) -> None:
        meta = self.write(tmp_path)
        count = meta["count"]
        assert count == 10
        raw = (tmp_path / "track.f32").read_bytes()
        assert len(raw) == len(COLUMNS) * count * 4 == meta["data"]["bytes"]
        names = [c["name"] for c in meta["columns"]]
        assert names == [
            "t",
            "north_m",
            "east_m",
            "depth_m",
            "heading_deg",
            "pitch_deg",
            "roll_deg",
            "vedba",
        ]

        # Column blocks: value i of column c sits at (c * count + i) * 4, little-endian.
        def value(col: str, i: int) -> float:
            offset = next(c["offset_bytes"] for c in meta["columns"] if c["name"] == col)
            assert offset == names.index(col) * count * 4
            return float(struct.unpack_from("<f", raw, offset + 4 * i)[0])

        assert value("t", 0) == 0.0
        assert value("t", 3) == pytest.approx(3.0)
        assert value("depth_m", 3) == pytest.approx(2.3, abs=1e-5)
        assert value("north_m", 9) == pytest.approx(9 * math.cos(math.radians(45)), abs=1e-5)
        assert value("vedba", 9) == pytest.approx(0.5)
        assert meta["t0"] == pytest.approx(T0)

    def test_json_fields(self, tmp_path: Path) -> None:
        meta = self.write(tmp_path)
        on_disk = json.loads((tmp_path / "track.json").read_text())
        assert on_disk == meta
        assert meta["schema"] == SCHEMA
        assert meta["rate_hz"] == 1.0
        assert meta["origin"] == {"lat": 39.904425, "lon": -69.504675}
        assert [f["kind"] for f in meta["fixes"]] == ["start", "end"]
        units = {c["name"]: c["unit"] for c in meta["columns"]}
        assert units["vedba"] == "m/s^2" and units["t"] == "s"
        assert meta["bounds"]["depth_m"] == pytest.approx([2.0, 2.9])
        lat_lo, lat_hi = meta["bounds"]["lat"]
        assert lat_lo == pytest.approx(39.904425) and lat_hi > lat_lo

    def test_read_bundle_round_trip(self, tmp_path: Path) -> None:
        self.write(tmp_path)
        meta, cols = read_bundle(tmp_path)
        assert cols["t"].dtype == np.dtype("<f4")
        assert len(cols["east_m"]) == meta["count"]
        np.testing.assert_allclose(cols["heading_deg"], 45.0)

    def test_geojson_simplified_and_georeferenced(self, tmp_path: Path) -> None:
        meta = self.write(tmp_path)
        gj = json.loads((tmp_path / "track.geojson").read_text())
        coords = gj["features"][0]["geometry"]["coordinates"]
        assert len(coords) == meta["geojson"]["points"] == 2  # a straight swim
        lon, lat = coords[-1]
        n, e = RED001.to_ne(lat, lon)
        end = 9 * math.cos(math.radians(45))  # north and east at 9 s on a 45 degree course
        assert math.hypot(n - end, e - end) < 0.1

    def test_no_georef_skips_geojson(self, tmp_path: Path) -> None:
        meta = self.write(tmp_path, georef=None)
        assert not (tmp_path / "track.geojson").exists()
        assert meta["origin"] is None and meta["bounds"]["lat"] is None


def make_run(
    tmp_path: Path,
    *,
    track_model: str = "fix_pinned",
    with_end_fix: bool = True,
    log: str = "",
) -> tuple[Path, Path]:
    """A run directory and a config directory laid out like pipeline-runs/ and config/."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    datasets = tmp_path / "datasets"
    datasets.mkdir()
    end = "8/13/22 11:49,39.8845,-69.6602" if with_end_fix else ",,"
    (datasets / "biologger_meta.csv").write_text(
        META_HEADER
        + "8/13/22 02:37,Xiphias gladius,39.904425,-69.504675,"
        + f"2022-08-13T02:30:07.999992Z,RED001_20220812,{end}\n"
    )
    run_dir = tmp_path / "pipeline-runs" / "20261105-165452_red001"
    run_dir.mkdir(parents=True)
    config = {
        "mode": "LAB",
        "simulation": {
            "meta_file": "../datasets/biologger_meta.csv",
            "entities": [
                {
                    "sim_id": "sword",
                    "tag_id": "RED001_20220812",
                    "dead_reckoning": {"track_model": track_model},
                }
            ],
        },
    }
    (run_dir / "config.yaml").write_text(yaml.safe_dump(config))
    output_rows().to_csv(run_dir / "sword_output.csv", index=False)
    (run_dir / "messages.log").write_text(log)
    return run_dir, config_dir


PINNED_LOG = (
    "2026-11-05 16:55:01,158 [INFO] biologger_sim.processors.lab: "
    "Track model: fix_pinned (configured fix_pinned)\n"
    "2026-11-05 16:55:01,176 [INFO] biologger_sim.processors.lab: "
    "Heading corrected by 69.8 deg to match the fix-pinned track\n"
)


class TestFromRun:
    def test_log_parse(self, tmp_path: Path) -> None:
        (tmp_path / "messages.log").write_text(PINNED_LOG)
        assert track_meta_from_log(tmp_path / "messages.log") == ("fix_pinned", 69.8)
        assert track_meta_from_log(tmp_path / "missing.log") == (None, None)

    def test_back_fill_from_log(self, tmp_path: Path) -> None:
        run_dir, config_dir = make_run(tmp_path, log=PINNED_LOG)
        (dest,) = bundles_from_run(run_dir, config_dir=config_dir)
        assert dest == run_dir / "track"
        meta = json.loads((dest / "track.json").read_text())
        assert meta["deployment_id"] == "RED001_20220812"
        assert meta["run_id"] == run_dir.name
        assert meta["track_model_used"] == "fix_pinned"
        assert meta["heading_correction_deg"] == 69.8
        assert meta["heading_correction_source"] == "messages.log"
        assert meta["species"] == "Xiphias gladius"
        assert meta["v_max_m_s"] > 0
        assert meta["provenance"]["source"] == "from-run"
        assert len(meta["provenance"]["config_sha256"]) == 64
        assert meta["count"] == 10

    def test_no_end_fix_falls_back_to_dead_reckoning(self, tmp_path: Path) -> None:
        run_dir, config_dir = make_run(tmp_path, with_end_fix=False)
        (dest,) = bundles_from_run(run_dir, tmp_path / "out", config_dir=config_dir)
        meta = json.loads((dest / "track.json").read_text())
        assert meta["track_model_configured"] == "fix_pinned"
        assert meta["track_model_used"] == "dead_reckoning"
        assert meta["heading_correction_deg"] == 0.0
        assert [f["kind"] for f in meta["fixes"]] == ["start"]

    def test_pinned_without_log_records_unknown_heading(self, tmp_path: Path) -> None:
        run_dir, config_dir = make_run(tmp_path)
        (dest,) = bundles_from_run(run_dir, config_dir=config_dir)
        meta = json.loads((dest / "track.json").read_text())
        assert meta["heading_correction_deg"] is None
        assert any("Heading correction" in n for n in meta["provenance"]["notes"])

    def test_sidecar_wins(self, tmp_path: Path) -> None:
        run_dir, config_dir = make_run(tmp_path, log=PINNED_LOG)
        sidecar = {
            "sim_id": "sword",
            "tag_id": "RED001_20220812",
            "species": "Xiphias gladius",
            "track_model_configured": "fix_pinned",
            "track_model_used": "fix_pinned",
            "heading_correction_deg": 91.3,
            "v_max_m_s": 2.0,
            "vedba_unit": "m/s^2",
            "sim_git_commit": "abc123",
            "sim_git_dirty": False,
        }
        (run_dir / f"sword{TRACK_META_SUFFIX}").write_text(json.dumps(sidecar))
        (dest,) = bundles_from_run(run_dir, config_dir=config_dir)
        meta = json.loads((dest / "track.json").read_text())
        assert meta["heading_correction_deg"] == 91.3
        assert meta["heading_correction_source"] == "run"
        assert meta["provenance"]["sim_git_commit"] == "abc123"

    def test_missing_output_csv_is_skipped(self, tmp_path: Path) -> None:
        run_dir, config_dir = make_run(tmp_path)
        (run_dir / "sword_output.csv").unlink()
        assert bundles_from_run(run_dir, config_dir=config_dir) == []
