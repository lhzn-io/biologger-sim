# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Tests for georeferencing, track models and space-time prism geometry."""

import math
from pathlib import Path

import numpy as np
import pytest

from biologger_sim.core.entity_meta import META_SCHEMA, build_entity_meta
from biologger_sim.core.georef import GeoFix, GeoReference, georeference_from_row, parse_utc
from biologger_sim.core.registry import EcosystemRegistry
from biologger_sim.core.species import max_sustained_speed
from biologger_sim.core.track_models import (
    apply_track_model,
    fix_pinning_factor,
    prism_bounds,
    prism_lens,
)
from biologger_sim.core.types import TrackModel

# RED001 fixes from biologger_meta.csv
T0 = parse_utc("2022-08-13T02:30:07.999992Z")
T1 = parse_utc("8/13/22 11:49")
assert T0 is not None and T1 is not None
RED001 = GeoReference(
    start=GeoFix(T0, 39.904425, -69.504675),
    end=GeoFix(T1, 39.8845, -69.6602),
)


class TestGeoref:
    def test_parse_utc_formats(self) -> None:
        assert parse_utc("2022-08-13T02:30:07.999992Z") == pytest.approx(1660357807.999992)
        assert parse_utc("8/13/22 11:49") == 1660391340.0
        assert parse_utc("") is None
        assert parse_utc("TBD") is None

    def test_round_trip(self) -> None:
        north, east = RED001.to_ne(39.8845, -69.6602)
        lat, lon = RED001.to_latlon(north, east)
        assert lat == pytest.approx(39.8845, abs=1e-9)
        assert lon == pytest.approx(-69.6602, abs=1e-9)

    def test_red001_end_offset(self) -> None:
        end = RED001.end_ne()
        assert end is not None
        assert end[0] == pytest.approx(-2213, abs=5)  # about 2.2 km south
        assert end[1] == pytest.approx(-13270, abs=20)  # about 13.3 km west

    def test_row_without_end_fix(self) -> None:
        row = {
            "start_lat": "39.904167",
            "start_lon": "-70.100617",
            "start_location_time": "2025-07-23T19:10:00Z",
            "time_end_utc": "7/26/25 09:24",
            "end_lat": "",
            "end_lon": "",
        }
        georef = georeference_from_row(row)
        assert georef is not None
        assert georef.end is None

    def test_registry_loads_fixes(self) -> None:
        meta = Path(__file__).parents[1] / "data" / "biologger_meta.csv"
        registry = EcosystemRegistry(meta_file=meta)
        registry.register("sword", tag_id="RED001_20220812")
        georef = registry.get_georeference("sword")
        assert georef is not None and georef.end is not None
        assert georef.start.t == pytest.approx(RED001.start.t)
        assert georef.end.lat == pytest.approx(39.8845)


class TestTrackModels:
    def _pseudo(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        # A wiggly northward track at 1 m/s spanning the fix window.
        t = np.linspace(RED001.start.t, RED001.end.t, 2001)  # type: ignore[union-attr]
        s = t - t[0]
        return t, s.copy(), 200.0 * np.sin(s / 600.0)

    def test_dead_reckoning_unchanged(self) -> None:
        t, n, e = self._pseudo()
        out_n, out_e, used = apply_track_model(TrackModel.DEAD_RECKONING, t, n, e, RED001)
        assert used == TrackModel.DEAD_RECKONING
        np.testing.assert_array_equal(out_n, n)
        np.testing.assert_array_equal(out_e, e)

    def test_interpolation_hits_fixes(self) -> None:
        t, n, e = self._pseudo()
        out_n, out_e, used = apply_track_model(TrackModel.FIX_INTERPOLATION, t, n, e, RED001)
        end = RED001.end_ne()
        assert used == TrackModel.FIX_INTERPOLATION and end is not None
        assert (out_n[0], out_e[0]) == pytest.approx((0.0, 0.0))
        assert (out_n[-1], out_e[-1]) == pytest.approx(end)
        mid = len(t) // 2
        assert (out_n[mid], out_e[mid]) == pytest.approx((end[0] / 2, end[1] / 2), rel=1e-3)

    def test_pinning_hits_fixes_and_keeps_shape(self) -> None:
        t, n, e = self._pseudo()
        out_n, out_e, used = apply_track_model(TrackModel.FIX_PINNED, t, n, e, RED001)
        end = RED001.end_ne()
        assert used == TrackModel.FIX_PINNED and end is not None
        assert (out_n[0], out_e[0]) == pytest.approx((0.0, 0.0), abs=1e-6)
        assert (out_n[-1], out_e[-1]) == pytest.approx(end, abs=1e-6)
        # Similarity transform: ratios of segment lengths are preserved.
        seg_in = np.hypot(np.diff(n), np.diff(e))
        seg_out = np.hypot(np.diff(out_n), np.diff(out_e))
        np.testing.assert_allclose(seg_out / seg_in, (seg_out / seg_in)[0], rtol=1e-9)

    def test_pinning_rotation_turns_every_segment(self) -> None:
        # The heading correction uses this angle: every pinned segment turns by exactly it, so
        # a heading rotated by the same angle points along the pinned track.
        t, n, e = self._pseudo()
        k = fix_pinning_factor(t, n, e, RED001)
        assert k is not None
        out_n, out_e, _ = apply_track_model(TrackModel.FIX_PINNED, t, n, e, RED001)
        turn = np.angle(np.diff(out_n + 1j * out_e) / np.diff(n + 1j * e))
        np.testing.assert_allclose(turn, np.angle(k), atol=1e-9)
        # Northward dead reckoning against a west-south-west fix: a large counter-clockwise turn.
        assert math.degrees(np.angle(k)) == pytest.approx(-99.5, abs=2.0)
        assert fix_pinning_factor(t, n, e, GeoReference(start=RED001.start)) is None

    def test_fallback_without_end_fix(self) -> None:
        t, n, e = self._pseudo()
        start_only = GeoReference(start=RED001.start)
        _, _, used = apply_track_model(TrackModel.FIX_INTERPOLATION, t, n, e, start_only)
        assert used == TrackModel.DEAD_RECKONING


class TestPrism:
    def test_lens_collapses_at_fixes(self) -> None:
        v = 1.5
        start = prism_lens(RED001.start.t, RED001, v)
        assert all(math.hypot(*p) < 1e-6 for p in start)
        end = prism_lens(RED001.end.t, RED001, v)  # type: ignore[union-attr]
        end_ne = RED001.end_ne()
        assert end_ne is not None
        assert all(math.hypot(p[0] - end_ne[0], p[1] - end_ne[1]) < 1e-6 for p in end)

    def test_lens_respects_both_disks(self) -> None:
        v = 1.5
        t = RED001.start.t + 0.4 * (RED001.end.t - RED001.start.t)  # type: ignore[union-attr]
        end_ne = RED001.end_ne()
        assert end_ne is not None
        r0 = v * (t - RED001.start.t)
        r1 = v * (RED001.end.t - t)  # type: ignore[union-attr]
        lens = prism_lens(t, RED001, v)
        assert len(lens) > 10
        for p in lens:
            assert math.hypot(*p) <= r0 * (1 + 1e-6)
            assert math.hypot(p[0] - end_ne[0], p[1] - end_ne[1]) <= r1 * (1 + 1e-6)

    def test_lens_empty_when_speed_too_low(self) -> None:
        # 13.5 km in 9.3 h needs at least about 0.4 m/s.
        t = RED001.start.t + 0.5 * (RED001.end.t - RED001.start.t)  # type: ignore[union-attr]
        assert prism_lens(t, RED001, 0.2) == []

    def test_bounds_contain_lenses(self) -> None:
        v = 1.5
        min_n, max_n, min_e, max_e = prism_bounds(RED001, v)
        span = RED001.end.t - RED001.start.t  # type: ignore[union-attr]
        for f in np.linspace(0.05, 0.95, 19):
            for n, e in prism_lens(RED001.start.t + f * span, RED001, v):
                assert min_n - 1 <= n <= max_n + 1
                assert min_e - 1 <= e <= max_e + 1
        # Major axis v * 9.3 h is about 50 km.
        assert max(max_n - min_n, max_e - min_e) == pytest.approx(v * span, rel=0.01)

    def test_entity_meta(self) -> None:
        t_mid = RED001.start.t + 3600.0
        meta = build_entity_meta(
            eid=0,
            sim_id="sword",
            tag_id="RED001_20220812",
            species="Xiphias gladius",
            georef=RED001,
            track_model=TrackModel.FIX_INTERPOLATION,
            v_max=1.5,
            t_now=t_mid,
            t_last=None,
        )
        assert meta["schema"] == META_SCHEMA
        assert meta["origin"] == {"lat": 39.904425, "lon": -69.504675}
        assert len(meta["fixes"]) == 2
        assert meta["prefetch_bounds_ne"] is not None and len(meta["prefetch_bounds_ne"]) == 4
        assert len(meta["prism"]) > 10
        no_geo = build_entity_meta(
            eid=1,
            sim_id="x",
            tag_id=None,
            species="unknown",
            georef=None,
            track_model=TrackModel.DEAD_RECKONING,
            v_max=1.5,
            t_now=None,
            t_last=None,
        )
        assert no_geo["origin"] is None and no_geo["prism"] == []

    def test_species_speed(self) -> None:
        assert max_sustained_speed("Xiphias gladius") == 1.5
        assert max_sustained_speed("Xiphias gladius", override=2.0) == 2.0
        assert max_sustained_speed(None) == 1.5
