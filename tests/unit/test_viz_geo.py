# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Tests for the Kit-free parts of the viz extension's DEM tiles and uncertainty overlay.

The extension package imports Kit modules, so the two plain-NumPy modules are loaded by path.
"""

import importlib.util
import math
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

from biologger_sim.core.georef import GeoFix, GeoReference

EXT = (
    Path(__file__).parents[2]
    / "omniverse/extensions/whoimpg.biologger.subscriber/whoimpg/biologger/subscriber"
)
ORIGIN = (39.904425, -69.504675)  # RED001 start fix


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"viz_{name}", EXT / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dem = _load("dem_tiles")
overlay = _load("geo_overlay")
look = _load("scene_look")
view = _load("view_scale")


class TestTileMaths:
    def test_origin_tile(self) -> None:
        assert dem.latlon_to_tile(*ORIGIN, 11) == (628, 776)

    def test_ne_matches_simulator(self) -> None:
        georef = GeoReference(start=GeoFix(0.0, *ORIGIN))
        n_sim, e_sim = georef.to_ne(39.8845, -69.6602)
        n_viz, e_viz = dem.latlon_to_ne(39.8845, -69.6602, ORIGIN)
        assert float(n_viz) == pytest.approx(n_sim)
        assert float(e_viz) == pytest.approx(e_sim)
        assert dem.ne_to_latlon(n_sim, e_sim, ORIGIN) == pytest.approx((39.8845, -69.6602))

    def test_tiles_for_red001_bounds(self) -> None:
        tiles = dem.tiles_for_bounds(ORIGIN, (-25400, 23200, -31800, 18500))
        assert (11, 628, 776) in tiles
        assert 12 <= len(tiles) <= 25  # about 50 km square at about 15 km per tile

    def test_tiles_around(self) -> None:
        assert len(dem.tiles_around(ORIGIN, 0.0, 0.0, radius=1)) == 9

    def test_sample_latlon_order(self) -> None:
        lats, lons = dem.tile_sample_latlon((11, 628, 776), grid=8)
        assert np.all(np.diff(lats) < 0)  # north to south
        assert np.all(np.diff(lons) > 0)  # west to east


class TestTileMesh:
    def test_arrays_shape_and_placement(self) -> None:
        elev = np.full((512, 512), -1000.0, dtype=np.float32)
        elev[0, 0] = np.nan
        key = (11, 628, 776)
        points, counts, indices, colors, normals = dem.build_tile_arrays(
            elev, key, ORIGIN, grid=16, skirt_m=100.0
        )
        assert colors.shape == points.shape and colors.min() >= 0.0 and colors.max() <= 1.0
        assert normals.shape == points.shape
        assert np.allclose(np.linalg.norm(normals, axis=1), 1.0)
        surface = points[: 16 * 16]
        skirt = points[16 * 16 :]
        assert len(skirt) == 4 * 16 - 4
        assert np.allclose(surface[:, 1], -1000.0 * 100)  # NaN filled with the median
        assert np.allclose(skirt[:, 1], (-1000.0 - 100.0) * 100)
        assert len(counts) == 15 * 15 + len(skirt) and np.all(counts == 4)
        assert indices.max() == len(points) - 1
        # The origin lies inside its own tile: x (east) and -z (north) bracket zero.
        assert surface[:, 0].min() < 0 < surface[:, 0].max()
        assert surface[:, 2].min() < 0 < surface[:, 2].max()

    def test_surface_faces_up(self) -> None:
        elev = np.zeros((512, 512), dtype=np.float32)
        points, _, indices, _, normals = dem.build_tile_arrays(elev, (11, 628, 776), ORIGIN, grid=4)
        a, b, c = (points[i] for i in indices[:3])
        normal = np.cross(b - a, c - b)
        assert normal[1] > 0
        assert np.allclose(normals, [0.0, 1.0, 0.0])  # flat seafloor: vertex normals point up

    def test_normals_follow_slope(self) -> None:
        # Seafloor rising to the east (1 in 10) and to the north (1 in 20).
        n = np.linspace(1000, -1000, 11)
        e = np.linspace(-1000, 1000, 11)
        north, east = np.meshgrid(n, e, indexing="ij")
        normals = dem.surface_normals(-500 + 0.1 * east + 0.05 * north, north, east)
        expected = np.array([-0.1, 1.0, 0.05]) / np.linalg.norm([-0.1, 1.0, 0.05])
        assert np.allclose(normals, expected)  # tilted west (-x) and south (+z, scene south)

    def test_depth_ramp_and_hillshade(self) -> None:
        shelf, slope, abyss = dem.depth_colors(np.array([-60.0, -1500.0, -6000.0]))
        assert shelf.sum() > slope.sum()  # shelf lighter than slope
        assert slope[2] > slope[1] > slope[0]  # red lost first, then green
        assert np.allclose(abyss, dem.WATER_RGB, atol=1e-3)  # fades to water, not black
        # Never white: every channel stays below the brightest sediment albedo.
        all_depths = dem.depth_colors(np.linspace(-5000.0, 0.0, 501))
        assert all_depths.max() <= 0.33
        t = dem.water_transmission(np.array([0.0, -100.0]))
        assert np.allclose(t[0], 1.0)
        assert t[1][0] == pytest.approx(math.exp(-2 * dem.WATER_KD[0] * 100 / dem.WATER_CLARITY))
        # A slope facing the north-west light is brighter than one facing south-east.
        n = np.linspace(1000, -1000, 21)
        e = np.linspace(-1000, 1000, 21)
        north, east = np.meshgrid(n, e, indexing="ij")
        facing_light = dem.hillshade(-north * 0.1 + east * 0.1 - 500, north, east)
        facing_away = dem.hillshade(north * 0.1 - east * 0.1 - 500, north, east)
        assert facing_light.mean() > facing_away.mean()
        flat = dem.hillshade(np.full_like(north, -500.0), north, east)
        assert np.allclose(flat, math.cos(math.radians(90 - dem.HILLSHADE_ALTITUDE_DEG)))

    def test_parse_npz(self) -> None:
        import io

        buf = io.BytesIO()
        np.savez(buf, elevation=np.ones((4, 4), dtype=np.float32))
        arr = dem.parse_tile_npz(buf.getvalue())
        assert arr is not None and arr.shape == (4, 4)


def _write_test_geotiff(elev: np.ndarray, x0: float, y0: float, px: float) -> bytes:
    """A minimal uncompressed, striped float32 GeoTIFF like GDAL's GTiff defaults."""
    import struct

    h, w = elev.shape
    pixels = elev.astype("<f4").tobytes()
    entries: list[tuple[int, int, int, bytes]] = []  # tag, type, count, payload

    def short(tag: int, v: int) -> None:
        entries.append((tag, 3, 1, struct.pack("<H", v)))

    def long_(tag: int, v: int) -> None:
        entries.append((tag, 4, 1, struct.pack("<I", v)))

    def doubles(tag: int, vs: list[float]) -> None:
        entries.append((tag, 12, len(vs), struct.pack(f"<{len(vs)}d", *vs)))

    long_(256, w)
    long_(257, h)
    short(258, 32)
    short(259, 1)
    short(262, 1)
    long_(273, 0)  # patched below
    short(277, 1)
    long_(278, h)
    long_(279, len(pixels))
    short(339, 3)
    doubles(33550, [px, px, 0.0])
    doubles(33922, [0.0, 0.0, 0.0, x0, y0, 0.0])
    entries.sort()

    ifd_off = 8
    data_off = ifd_off + 2 + 12 * len(entries) + 4
    extra = b""
    body = b""
    for tag, typ, n, payload in entries:
        if len(payload) <= 4:
            value = payload.ljust(4, b"\0")
        else:
            value = struct.pack("<I", data_off + len(extra))
            extra += payload
        body += struct.pack("<HHI", tag, typ, n) + value
    pix_off = data_off + len(extra)
    body = body.replace(
        struct.pack("<HHI", 273, 4, 1) + struct.pack("<I", 0),
        struct.pack("<HHI", 273, 4, 1) + struct.pack("<I", pix_off),
    )
    header = b"II" + struct.pack("<HI", 42, ifd_off)
    ifd = struct.pack("<H", len(entries)) + body + struct.pack("<I", 0)
    return header + ifd + extra + pixels


class TestFusedGrid:
    def test_geotiff_round_trip(self) -> None:
        elev = np.arange(12, dtype=np.float32).reshape(3, 4) - 500.0
        data = _write_test_geotiff(elev, x0=-7780000.0, y0=4850000.0, px=30.0)
        out, xs, ys = dem.parse_geotiff(data)
        np.testing.assert_array_equal(out, elev)
        assert xs[0] == pytest.approx(-7780000.0 + 15.0)
        assert ys[0] == pytest.approx(4850000.0 - 15.0)
        assert np.all(np.diff(ys) < 0)

    def test_rejects_compressed(self) -> None:
        data = bytearray(_write_test_geotiff(np.zeros((2, 2)), 0.0, 0.0, 1.0))
        import struct

        i = data.find(struct.pack("<HHI", 259, 3, 1))
        data[i + 8 : i + 10] = struct.pack("<H", 8)  # deflate
        with pytest.raises(ValueError, match="compressed"):
            dem.parse_geotiff(bytes(data))

    def test_blocks_cover_grid_without_gaps(self) -> None:
        rows, cols = 600, 700
        elev = np.full((rows, cols), -800.0, dtype=np.float32)
        # Grid around the origin in EPSG:3857.
        lat0, lon0 = ORIGIN
        x0 = math.radians(lon0) * dem.WEB_MERCATOR_R
        y0 = math.log(math.tan(math.pi / 4 + math.radians(lat0) / 2)) * dem.WEB_MERCATOR_R
        xs = x0 + (np.arange(cols) - cols / 2) * 30.0
        ys = y0 - (np.arange(rows) - rows / 2) * 30.0
        blocks = list(dem.grid_blocks(elev, xs, ys, ORIGIN, block_px=256, stride=2))
        assert len(blocks) == 9  # 3 x 3 blocks of 256 px
        east_edges = sorted({round(float(b[3][0, -1])) for b in blocks})
        west_edges = sorted({round(float(b[3][0, 0])) for b in blocks})
        assert set(east_edges[:-1]) <= set(west_edges)  # neighbours share their edge column
        names = {b[0] for b in blocks}
        assert "grid_r0_c0" in names
        # The origin falls inside the covered area.
        all_n = np.concatenate([b[2].ravel() for b in blocks])
        all_e = np.concatenate([b[3].ravel() for b in blocks])
        assert all_n.min() < 0 < all_n.max() and all_e.min() < 0 < all_e.max()

    def test_latlon_bounds(self) -> None:
        west, south, east, north = dem.latlon_bounds(ORIGIN, (-25400, 23200, -31800, 18500))
        assert west < ORIGIN[1] < east and south < ORIGIN[0] < north


class TestPrismOverlay:
    def test_band(self) -> None:
        # Square 4 km across centred on (2000, 2000): the band is 3% of the mean radius.
        square = [[0, 0], [0, 4000], [4000, 4000], [4000, 0]]
        arrays = overlay.prism_band_arrays(square)
        assert arrays is not None
        points, counts, indices = arrays
        assert len(points) == 8 and len(counts) == 4 and np.all(counts == 4)
        assert indices.max() == 7
        assert all(math.isclose(p[1], overlay.SURFACE_OFFSET_CM) for p in points)
        # Outer ring is the polygon (east, north from x and -z); inner ring sits inside it.
        assert points[1][0] == pytest.approx(4000 * 100) and points[1][2] == pytest.approx(0.0)
        r = math.hypot(2000, 2000)
        width = overlay.band_width_m(np.full(4, r))
        assert width == pytest.approx(overlay.BAND_FRACTION * r)
        centre = np.array([2000 * 100, -2000 * 100])
        outer = np.hypot(points[:4, 0] - centre[0], points[:4, 2] - centre[1])
        inner = np.hypot(points[4:, 0] - centre[0], points[4:, 2] - centre[1])
        assert np.allclose(outer - inner, width * 100)

    def test_band_width_clamped(self) -> None:
        assert overlay.band_width_m(np.full(8, 100.0)) == pytest.approx(overlay.BAND_MIN_M)
        assert overlay.band_width_m(np.full(8, 1e6)) == pytest.approx(overlay.BAND_MAX_M)
        assert overlay.band_width_m(np.full(8, 50.0)) == pytest.approx(25.0)  # half the radius

    def test_degenerate(self) -> None:
        assert overlay.prism_band_arrays([]) is None
        assert overlay.prism_band_arrays([[0, 0], [1, 1]]) is None

    def test_prim_path_sanitised(self) -> None:
        assert overlay.prim_path("sword-postfacto v2") == "/World/Uncertainty/sword_postfacto_v2"


class TestSceneLook:
    def test_sun_on_deployment_morning(self) -> None:
        from datetime import datetime, timezone

        el, az = look.sun_position(*ORIGIN, datetime(2022, 8, 13, 13, 0, tzinfo=timezone.utc))
        assert el == pytest.approx(35.6, abs=1.0)  # 09:00 EDT: low morning sun
        assert az == pytest.approx(100.7, abs=1.5)  # just south of east

    def test_solar_time(self) -> None:
        # RED001 starts 2022-08-13 02:30 UTC, which is the evening of 12 August locally.
        when = look.solar_time_utc(1660357808.0, ORIGIN[1], 9.0)
        assert (when.month, when.day) == (8, 12)
        hours = when.hour + when.minute / 60
        assert hours == pytest.approx(9.0 - ORIGIN[1] / 15.0, abs=0.02)

    def test_sun_rotation_points_light_down_from_sun(self) -> None:
        for el, az in [(35.6, 100.7), (60.0, 180.0), (10.0, 270.0)]:
            rx, ry, _ = (math.radians(a) for a in look.sun_rotate_xyz(el, az))
            # USD rotateXYZ: X first, then Y; a DistantLight shines along its local -Z.
            v = np.array([0.0, 0.0, -1.0])
            v = np.array(
                [
                    v[0],
                    v[1] * math.cos(rx) - v[2] * math.sin(rx),
                    v[1] * math.sin(rx) + v[2] * math.cos(rx),
                ]
            )
            v = np.array(
                [
                    v[0] * math.cos(ry) + v[2] * math.sin(ry),
                    v[1],
                    -v[0] * math.sin(ry) + v[2] * math.cos(ry),
                ]
            )
            assert np.allclose(v, -look.sun_vector(el, az), atol=1e-9)

    def test_sky(self) -> None:
        img = look.sky_equirect(35.6, 100.7, width=128)
        assert img.shape == (64, 128, 3) and np.isfinite(img).all() and img.min() >= 0
        zenith = img[0].mean(axis=0)
        assert zenith[2] > zenith[1] > zenith[0]  # blue overhead
        horizon = img[30:32].reshape(-1, 3).mean(axis=0)
        assert horizon[0] < horizon[1] < horizon[2]  # pale blue, not violet, at the horizon
        # Near the horizon the sun's side is brighter than the opposite side.
        row = img[28]
        col_sun = int((100.7 + 180) / 360 * 128)
        col_anti = (col_sun + 64) % 128
        assert row[col_sun].sum() > row[col_anti].sum()

    def test_hdr_round_trip(self, tmp_path: Path) -> None:
        path = str(tmp_path / "sky.hdr")
        look.write_hdr(path, np.ones((4, 8, 3), dtype=np.float32))
        assert look.read_hdr_size(path) == (4, 8)
        data = Path(path).read_bytes()
        assert data.endswith(bytes([128, 128, 128, 129]))  # 1.0 in RGBE

    def test_underwater_fog_toggles_once(self) -> None:
        class Settings:
            def __init__(self) -> None:
                self.calls: list[tuple[str, object]] = []

            def set(self, key: str, value: object) -> None:
                self.calls.append((key, value))

        s = Settings()
        crossings: list[bool] = []
        deeps: list[bool] = []
        fog = look.UnderwaterFog(
            s, visibility_m=40.0, on_change=crossings.append, on_deep=deeps.append
        )
        fog.update(1000.0)
        fog.update(500.0)
        assert [c for c in s.calls if c[0].startswith("/rtx/fog")] == [("/rtx/fog/enabled", False)]
        assert ("/rtx/background/source/type", 0) in s.calls  # the sky above the deep water
        fog.update(-200.0)
        assert ("/rtx/fog/enabled", True) in s.calls
        assert ("/rtx/fog/fogEndDist", 4000.0) in s.calls
        # The surface reflection follows each crossing (off below the surface).
        assert crossings == [False, True]
        fog.reset()  # after the look is re-applied, the current state is applied again
        fog.update(-150.0)
        assert crossings == [False, True, True]
        # Past DEEP_WATER_M the water volume goes and the background turns the water colour
        assert deeps == [False, False]
        fog.update(-(look.DEEP_WATER_M + 1.0) * 100.0)
        assert deeps == [False, False, True]
        assert s.calls[-1] == ("/rtx/background/source/type", 1)
        assert crossings == [False, True, True]  # still under, no new crossing


class TestViewScale:
    def test_exaggeration_steps_up_and_down(self) -> None:
        assert view.step_exaggeration(1.0, 1) == 2.0
        assert view.step_exaggeration(5.0, 1) == 10.0
        assert view.step_exaggeration(10.0, 1) == 10.0  # stays at the top step
        assert view.step_exaggeration(3.0, -1) == 2.0
        assert view.step_exaggeration(1.0, -1) == 1.0
        assert view.step_exaggeration(4.0, -1) == 3.0  # off-step factors rejoin the steps
        assert view.step_exaggeration(4.0, 1) == 5.0

    def test_trail_width_follows_distance_in_powers_of_two(self) -> None:
        # 15 km away: ideal 30 m, nearest step 5 cm * 2^9 = 25.6 m
        assert view.adaptive_trail_width_cm(1_500_000.0, 5.0) == pytest.approx(2560.0)
        # Close up the width bottoms out at the close-up width
        assert view.adaptive_trail_width_cm(100.0, 2560.0) == view.TRAIL_WIDTH_MIN_CM
        # Very far away it is capped
        assert view.adaptive_trail_width_cm(1e9, 5.0) == view.TRAIL_WIDTH_MAX_CM

    def test_trail_width_hysteresis(self) -> None:
        def distance_for(width_cm: float) -> float:
            return width_cm / float(view.TRAIL_WIDTH_PER_DISTANCE)

        # Within 0.75 powers of two of the current width (1.6x is 0.68), nothing changes
        assert view.adaptive_trail_width_cm(distance_for(2560.0 * 1.6), 2560.0) == 2560.0
        assert view.adaptive_trail_width_cm(distance_for(2560.0 / 1.6), 2560.0) == 2560.0
        # Past it, the width steps
        assert view.adaptive_trail_width_cm(distance_for(2560.0 * 2.0), 2560.0) == pytest.approx(
            5120.0
        )


class TestInSituSeafloor:
    def test_in_situ_is_sediment_in_the_light_left_at_depth(self) -> None:
        elev = np.array([-600.0])
        tint = dem.downwelling_tint(elev)[0]
        # Blue light is all that is left at canyon depths, scaled to full strength
        assert tint[2] == pytest.approx(1.0)
        assert tint[0] < 0.01 < tint[1] < tint[2]
        surface = dem.depth_colors(elev)[0]
        try:
            assert dem.set_in_situ(True)
            assert not dem.set_in_situ(True)  # unchanged
            in_situ = dem.depth_colors(elev)[0]
        finally:
            dem.set_in_situ(False)
        # The floor's own colour in that light, not the deep-water colour seen from above
        # (blue albedo between the -500 m and -1200 m sediment stops)
        assert in_situ[2] == pytest.approx(0.092 + (0.070 - 0.092) * 100.0 / 700.0)
        assert not np.allclose(in_situ, surface)

    def test_normal_shade_follows_the_sun(self) -> None:
        before = (dem.HILLSHADE_ALTITUDE_DEG, dem.HILLSHADE_AZIMUTH_DEG)
        try:
            dem.set_sun(30.0, 180.0)
            up = np.array([[0.0, 1.0, 0.0]])
            facing_sun = np.array([[0.0, 0.0, 1.0]])  # south-facing (scene +Z is south)
            assert dem.normal_shade(up)[0] == pytest.approx(0.5)
            assert dem.normal_shade(facing_sun)[0] == pytest.approx(math.cos(math.radians(30.0)))
        finally:
            dem.set_sun(*before)


class TestSeafloorDetail:
    def test_heightfield_tiles_seamlessly(self) -> None:
        h = dem.detail_heightfield(size=64)
        assert h.shape == (64, 64)
        assert h.min() == pytest.approx(0.0) and h.max() == pytest.approx(1.0)
        # Wrapping edges differ no more than neighbouring interior rows do
        interior = np.abs(np.diff(h, axis=0)).max()
        assert np.abs(h[0] - h[-1]).max() <= interior + 1e-9
        assert np.abs(h[:, 0] - h[:, -1]).max() <= np.abs(np.diff(h, axis=1)).max() + 1e-9

    def test_normal_map_is_flat_for_a_flat_field(self) -> None:
        rgb = dem.detail_normal_map(np.zeros((8, 8)))
        assert rgb.dtype == np.uint8
        assert np.all(rgb[..., 0] == 128) and np.all(rgb[..., 2] == 255)

    def test_normal_map_has_the_target_median_tilt(self) -> None:
        rgb = dem.detail_normal_map(dem.detail_heightfield(size=128), tilt_deg=18.0)
        n = rgb.astype(float) / 255.0 * 2.0 - 1.0
        tilt = np.degrees(np.arccos(n[..., 2] / np.linalg.norm(n, axis=-1)))
        assert float(np.median(tilt)) == pytest.approx(18.0, abs=1.0)  # 8-bit quantisation

    def test_png_writer_round_trips(self, tmp_path: Path) -> None:
        import struct
        import zlib

        rgb = np.arange(2 * 3 * 3, dtype=np.uint8).reshape(2, 3, 3)
        path = tmp_path / "t.png"
        dem.write_png_rgb(str(path), rgb)
        data = path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", data[16:24])
        assert (width, height) == (3, 2)
        idat_len = struct.unpack(">I", data[33:37])[0]
        raw = zlib.decompress(data[41 : 41 + idat_len])
        assert raw == b"\x00" + rgb[0].tobytes() + b"\x00" + rgb[1].tobytes()


class TestEdgeFade:
    def test_fade_is_full_at_the_edge_and_gone_inside(self) -> None:
        try:
            dem.set_edge_extent((-10000.0, 10000.0, -20000.0, 20000.0))
            north = np.array([10000.0, 9000.0, 0.0, 0.0])
            east = np.array([0.0, 0.0, 0.0, -20000.0 + dem.EDGE_FADE_M / 2])
            fade = dem.edge_fade(north, east)
            assert fade[0] == pytest.approx(1.0)  # on the edge
            assert 0.0 < fade[1] < 1.0  # inside the fade band
            assert fade[2] == pytest.approx(0.0)  # well inside
            assert fade[3] == pytest.approx(0.5)  # halfway through the band (smoothstep)
            rgb = dem.fade_to_water(np.array([[0.3, 0.3, 0.3]]), np.array([1.0]))
            assert np.allclose(rgb[0], dem.WATER_RGB)
        finally:
            dem.set_edge_extent(None)
        assert dem.edge_fade(np.array([0.0]), np.array([0.0]))[0] == 0.0  # tiles: no fade


class TestSkyBelowHorizon:
    def test_lower_hemisphere_is_deep_water_when_set(self) -> None:
        plain = look.sky_equirect(40.0, 120.0, width=64)
        sea = look.sky_equirect(40.0, 120.0, width=64, below_gain=6.0)
        assert np.allclose(sea[:16], plain[:16])  # the sky above the horizon is unchanged
        assert np.allclose(sea[16:], np.asarray(look.WATER_RGB) * 6.0)


class TestTrailArrays:
    def test_smooth_trail_keeps_the_ends_and_averages_inside(self) -> None:
        ts = np.arange(0.0, 10.0, 0.0625)  # 16 Hz for 10 s
        pos = np.stack([ts * 100.0, np.where(np.arange(len(ts)) % 2, 50.0, -50.0), 0 * ts], axis=1)
        odba = np.where(np.arange(len(ts)) % 2, 1.0, 0.0)
        t2, p2, o2 = view.smooth_trail(ts, pos, odba, window_s=2.0, width_cm=0.0)
        assert t2[0] == ts[0] and t2[-1] == ts[-1]
        assert np.allclose(p2[0], pos[0]) and np.allclose(p2[-1], pos[-1])
        # Inside, the saw-tooth and the alternating ODBA average out
        assert np.allclose(p2[1:-1, 1], 0.0, atol=4.0)
        assert np.allclose(o2[1:-1], 0.5, atol=0.05)
        assert len(t2) == 2 + 5  # five 2 s windows plus the exact ends

    def test_width_averaging_merges_samples_within_a_width(self) -> None:
        ts = np.arange(11, dtype=float)
        pos = np.stack([np.arange(11) * 10.0, 0 * ts, 0 * ts], axis=1)  # 10 cm apart
        t2, p2, _ = view.smooth_trail(ts, pos, np.zeros(11), window_s=0.0, width_cm=30.0)
        assert len(t2) == 2 + 3  # nine inner samples, 30 cm bins
        assert np.all(np.diff(p2[:, 0]) > 0)

    def test_odba_colours_match_the_hsv_ramp(self) -> None:
        import colorsys

        odba = np.array([0.0, 0.1, 0.85, 1.6, 3.0])
        rgb = view.odba_colors(odba)
        for o, c in zip(odba, rgb, strict=True):
            n = min(max((o - 0.1) / 1.5, 0.0), 1.0)
            expected = colorsys.hsv_to_rgb((180 - 180 * n) / 360, 0.8 + 0.2 * n, 0.7 + 0.3 * n)
            assert np.allclose(c, expected, atol=1e-9)
