# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""DEM tile streaming from topobathykit, placed relative to the deployment origin.

topobathykit serves Web Mercator tiles (``/tiles/{z}/{x}/{y}.npz``, 512 x 512 float32
elevation, positive up, row 0 at the north edge). Each tile becomes its own mesh under
``/World/Bathymetry`` so tiles can be added and dropped as the camera and animals move.

Frames: positions are (north, east) metres from the origin (the simulator's start fix, the same
frame as ``px``/``py``), converted with the same equirectangular approximation the simulator
uses. Scene: USD Y-up in centimetres, east -> +X, up -> +Y, north -> -Z (see ``warp_logic``).

The tile maths and mesh arrays are plain NumPy (testable without Kit); USD and HTTP are only
touched by ``DemTileStreamer``.
"""

from __future__ import annotations

import asyncio
import io
import math
import time
from collections.abc import Callable, Iterable
from typing import Any

import numpy as np

EARTH_RADIUS_M = 6371000.0
TILE_ZOOM = 11  # about 15 km per tile and 29 m per source pixel at 40 deg N
TILE_PIXELS = 512
MESH_GRID = 128  # vertices per tile side after downsampling (about 117 m spacing at zoom 11)
SKIRT_M = 150.0  # downward edge skirt hiding seams between neighbouring tiles
SCENE_SCALE = 100.0  # metres -> scene centimetres
DEM_ROOT = "/World/Bathymetry"  # parent of the DEM meshes
NO_DATA_FILL_M = -100.0  # used only if a tile has no valid samples at all
MAX_TILE_ATTEMPTS = 4
RETRY_BACKOFF_S = 30.0  # times the attempt number

TileKey = tuple[int, int, int]  # (z, x, y)


# --- Web Mercator tile maths -------------------------------------------------------------


def latlon_to_tile(lat: float, lon: float, zoom: int) -> tuple[int, int]:
    """The (x, y) tile containing a point."""
    n = 2.0**zoom
    x = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return x, y


def _mercator_y_to_lat(y: np.ndarray | float, n: float) -> np.ndarray:
    return np.asarray(np.degrees(np.arctan(np.sinh(math.pi * (1.0 - 2.0 * np.asarray(y) / n)))))


def tile_sample_latlon(key: TileKey, grid: int = MESH_GRID) -> tuple[np.ndarray, np.ndarray]:
    """Latitudes (north to south) and longitudes (west to east) of the sampled pixel centres."""
    z, x, y = key
    n = 2.0**z
    idx = sample_indices(grid)
    frac = (idx + 0.5) / TILE_PIXELS
    lats = _mercator_y_to_lat(y + frac, n)
    lons = (x + frac) / n * 360.0 - 180.0
    return lats, lons


def sample_indices(grid: int = MESH_GRID) -> np.ndarray:
    """Source pixel indices kept when downsampling a tile, including both edges."""
    return np.round(np.linspace(0, TILE_PIXELS - 1, grid)).astype(int)


def latlon_to_ne(
    lat: np.ndarray | float, lon: np.ndarray | float, origin: tuple[float, float]
) -> tuple[np.ndarray, np.ndarray]:
    """(north, east) metres from ``origin``; matches biologger_sim.core.georef."""
    lat0, lon0 = origin
    north = np.radians(np.asarray(lat) - lat0) * EARTH_RADIUS_M
    east = np.radians(np.asarray(lon) - lon0) * EARTH_RADIUS_M * math.cos(math.radians(lat0))
    return north, east


def ne_to_latlon(north: float, east: float, origin: tuple[float, float]) -> tuple[float, float]:
    lat0, lon0 = origin
    lat = lat0 + math.degrees(north / EARTH_RADIUS_M)
    lon = lon0 + math.degrees(east / (EARTH_RADIUS_M * math.cos(math.radians(lat0))))
    return lat, lon


def tiles_for_bounds(
    origin: tuple[float, float], bounds_ne: Iterable[float], zoom: int = TILE_ZOOM
) -> set[TileKey]:
    """Tiles covering (min_n, max_n, min_e, max_e) metres around the origin."""
    min_n, max_n, min_e, max_e = bounds_ne
    lat_s, lon_w = ne_to_latlon(min_n, min_e, origin)
    lat_n, lon_e = ne_to_latlon(max_n, max_e, origin)
    x0, y0 = latlon_to_tile(lat_n, lon_w, zoom)
    x1, y1 = latlon_to_tile(lat_s, lon_e, zoom)
    return {(zoom, x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


def tiles_around(
    origin: tuple[float, float],
    north: float,
    east: float,
    radius: int = 1,
    zoom: int = TILE_ZOOM,
) -> set[TileKey]:
    """The tile under a point plus ``radius`` rings of neighbours."""
    lat, lon = ne_to_latlon(north, east, origin)
    cx, cy = latlon_to_tile(lat, lon, zoom)
    return {
        (zoom, x, y)
        for x in range(cx - radius, cx + radius + 1)
        for y in range(cy - radius, cy + radius + 1)
    }


# --- Mesh arrays -------------------------------------------------------------------------


def fill_no_data(elev: np.ndarray) -> np.ndarray:
    """Replaces NaN samples with the tile's median so holes do not become spikes."""
    out = np.array(elev, dtype=np.float32)
    bad = ~np.isfinite(out)
    if bad.any():
        good = out[~bad]
        out[bad] = float(np.median(good)) if good.size else NO_DATA_FILL_M
    return out


# Seafloor colour seen from the surface through the water column (linear RGB), after the
# underwater image-formation model, per channel c and depth d:
#     colour_c = albedo_c(d) * t_c + water_c * (1 - t_c),   t_c = exp(-2 Kd_c d / clarity)
# The renderer does not attenuate light through the water, so this is baked into the albedo.
# Albedo is wet-sediment reflectance (shelf sand to slope mud, at most about 0.3), so the
# seafloor cannot clip to white under the sun; with depth it fades to the deep-water colour,
# never to black.
_SEDIMENT_STOPS_M = np.array([-3000.0, -1200.0, -500.0, -200.0, -120.0, -40.0, 0.0, 50.0])
_SEDIMENT_RGB = np.array(
    [
        [0.060, 0.062, 0.065],  # lower slope clay
        [0.075, 0.074, 0.070],  # slope mud
        [0.110, 0.105, 0.092],  # upper slope silt
        [0.170, 0.155, 0.125],  # shelf break muddy sand
        [0.230, 0.205, 0.155],  # outer shelf sand
        [0.290, 0.255, 0.190],  # shelf sand
        [0.320, 0.285, 0.210],  # shallow sand
        [0.120, 0.130, 0.080],  # land
    ]
)
# Diffuse attenuation (1/m) at 610, 545 and 465 nm, Jerlov oceanic type IB (approximate):
# red is lost first, then green, so the seafloor turns teal and then blue with depth.
WATER_KD = np.array([0.29, 0.062, 0.024])
WATER_RGB = np.array([0.010, 0.040, 0.115])  # optically deep water seen from above
# Visualisation exaggeration of the light path (1 is physical): at 20 the 600 m canyon floor
# keeps some contrast while the order in which colours fade stays physical.
WATER_CLARITY = 20.0

# Baked relief shading, lit from the scene's sun (``set_sun``); the scene's own lighting shades
# the geometry too, so this only adds definition to low-relief slopes.
HILLSHADE_AZIMUTH_DEG = 315.0  # default: light from the north-west, cartographic convention
HILLSHADE_ALTITUDE_DEG = 40.0
HILLSHADE_WEIGHT = 0.35  # 0: flat colour, 1: full hillshade
HILLSHADE_EXAGGERATION = 3.0  # vertical exaggeration for shading only (geometry is true scale)

# In-situ colour (``set_in_situ``): the seafloor as seen from close by, for a camera down in the
# canyons: sediment lit by the blue light left at its depth, with no water column between it
# and the camera baked in. It is brightened to full strength; at canyon depths the real floor
# is close to dark.
IN_SITU = False


def set_sun(elevation_deg: float, azimuth_deg: float) -> None:
    """Bakes later meshes' hillshade from this sun (degrees, azimuth clockwise from north)."""
    global HILLSHADE_ALTITUDE_DEG, HILLSHADE_AZIMUTH_DEG
    HILLSHADE_ALTITUDE_DEG = float(np.clip(elevation_deg, 5.0, 90.0))
    HILLSHADE_AZIMUTH_DEG = float(azimuth_deg) % 360.0


def set_in_situ(on: bool) -> bool:
    """Selects in-situ (True) or seen-from-the-surface seafloor colour; returns if it changed."""
    global IN_SITU
    changed = bool(on) != IN_SITU
    IN_SITU = bool(on)
    return changed


def water_transmission(elev: np.ndarray, clarity: float = WATER_CLARITY) -> np.ndarray:
    """Per-channel share (..., 3) of the seafloor's own colour that reaches the surface."""
    depth = np.clip(-np.asarray(elev, dtype=float), 0.0, None)[..., None]
    return np.asarray(np.exp(-2.0 * WATER_KD * depth / clarity))


def downwelling_tint(elev: np.ndarray, clarity: float = WATER_CLARITY) -> np.ndarray:
    """Hue (..., 3) of the sunlight left at depth, scaled so its strongest channel is 1.

    The one-way path from the surface strips red, then green: the in-situ seafloor takes this
    hue at full brightness (the brightening is the visualisation's, not the ocean's).
    """
    depth = np.clip(-np.asarray(elev, dtype=float), 0.0, None)[..., None]
    t = np.exp(-WATER_KD * depth / clarity)
    return np.asarray(t / t.max(axis=-1, keepdims=True))


def depth_colors(elev: np.ndarray) -> np.ndarray:
    """RGB (..., 3) per elevation: sediment albedo seen through the water column."""
    e = np.clip(np.asarray(elev, dtype=float), _SEDIMENT_STOPS_M[0], _SEDIMENT_STOPS_M[-1])
    albedo = np.stack(
        [np.interp(e, _SEDIMENT_STOPS_M, _SEDIMENT_RGB[:, i]) for i in range(3)], axis=-1
    )
    if IN_SITU:
        return np.asarray(albedo * downwelling_tint(elev))
    t = water_transmission(elev)
    return np.asarray(albedo * t + WATER_RGB * (1.0 - t))


def hillshade(elev: np.ndarray, north: np.ndarray, east: np.ndarray) -> np.ndarray:
    """Hillshade in [0, 1] for a grid (rows north to south) with per-cell metre coordinates."""
    z = np.asarray(elev, dtype=float) * HILLSHADE_EXAGGERATION
    dz_dn, dz_de = np.gradient(z, north[:, 0], east[0, :])
    slope = np.arctan(np.hypot(dz_dn, dz_de))
    # Downslope direction as a compass azimuth (0 = north, clockwise).
    aspect = np.arctan2(-dz_de, -dz_dn)
    zenith = math.radians(90.0 - HILLSHADE_ALTITUDE_DEG)
    azimuth = math.radians(HILLSHADE_AZIMUTH_DEG)
    shade = math.cos(zenith) * np.cos(slope) + math.sin(zenith) * np.sin(slope) * np.cos(
        azimuth - aspect
    )
    return np.asarray(np.clip(shade, 0.0, 1.0))


# Seafloor detail (``set_seafloor_detail``): a tiling sediment normal map on the seabed
# material, so the surface catches light like sediment between DEM samples. It is decoration,
# not data: the geometry stays the DEM's, and the texture is off by default.
DETAIL_TILE_M = 24.0  # ground size of one texture repeat
DETAIL_PIXELS = 512
DETAIL_STRENGTH = 3.0  # height-to-normal gain; larger gives deeper-looking texture


def detail_heightfield(size: int = DETAIL_PIXELS, seed: int = 7) -> np.ndarray:
    """Tileable fractal noise in [0, 1] (size x size): sums of random-phase Fourier modes.

    Built in the frequency domain with integer wave numbers, so it wraps seamlessly. The 1/f
    falloff gives ripples and pits at a few scales, like reworked sediment.
    """
    rng = np.random.default_rng(seed)
    k = np.fft.fftfreq(size) * size
    kx, ky = np.meshgrid(k, k, indexing="xy")
    radius = np.hypot(kx, ky)
    amp = np.where(
        (radius >= 2.0) & (radius <= size / 4), 1.0 / np.maximum(radius, 1.0) ** 1.6, 0.0
    )
    phase = rng.uniform(0.0, 2.0 * np.pi, (size, size))
    field = np.real(np.fft.ifft2(amp * np.exp(1j * phase)))
    field -= field.min()
    return np.asarray(field / max(float(field.max()), 1e-12))


def detail_normal_map(height: np.ndarray, strength: float = DETAIL_STRENGTH) -> np.ndarray:
    """Tangent-space normal map (rows, cols, 3) as uint8 RGB from a wrapping height field."""
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * 0.5 * strength
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * 0.5 * strength
    n = np.stack([-dx, -dy, np.ones_like(height)], axis=-1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return np.asarray(np.clip((n * 0.5 + 0.5) * 255.0 + 0.5, 0, 255).astype(np.uint8))


def write_png_rgb(path: str, rgb: np.ndarray) -> None:
    """Writes an 8-bit RGB PNG with the standard library (Kit has no imaging package)."""
    import struct
    import zlib

    rows, cols, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[r].tobytes() for r in range(rows))  # filter type 0 per row

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", cols, rows, 8, 2, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(
            chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b"")
        )


def normal_shade(normals: np.ndarray) -> np.ndarray:
    """Lambert shade in [0, 1] of unit scene-axis normals (x east, y up, z south) from the sun.

    Stands in for ``hillshade`` when meshes are recoloured in place and only their vertex
    normals are at hand.
    """
    alt = math.radians(HILLSHADE_ALTITUDE_DEG)
    az = math.radians(HILLSHADE_AZIMUTH_DEG)
    sun = np.array([math.sin(az) * math.cos(alt), math.sin(alt), -math.cos(az) * math.cos(alt)])
    return np.asarray(np.clip(np.asarray(normals, dtype=float) @ sun, 0.0, 1.0))


def surface_normals(elev: np.ndarray, north: np.ndarray, east: np.ndarray) -> np.ndarray:
    """Unit vertex normals (rows, cols, 3) in scene axes (x east, y up, z south).

    Authored on the mesh so the renderer shades the surface smoothly; without them it lights
    each triangle of the non-planar grid quads flat, which shows as diamonds on steep slopes.
    """
    dz_dn, dz_de = np.gradient(np.asarray(elev, dtype=float), north[:, 0], east[0, :])
    n = np.stack([-dz_de, np.ones_like(dz_de), dz_dn], axis=-1)
    return np.asarray(n / np.linalg.norm(n, axis=-1, keepdims=True))


def build_tile_arrays(
    elevation: np.ndarray,
    key: TileKey,
    origin: tuple[float, float],
    grid: int = MESH_GRID,
    skirt_m: float = SKIRT_M,
    scale: float = SCENE_SCALE,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Points (N, 3) in scene units, face counts, face indices, vertex colours and normals.

    The surface is ``grid`` x ``grid`` quads' corners; a skirt of ``skirt_m`` runs down from
    every edge vertex so small gaps between neighbouring tiles are not visible. Colours combine
    the depth ramp with a baked hillshade, so relief reads even under flat scene lighting.
    """
    idx = sample_indices(grid)
    elev = np.asarray(elevation)[np.ix_(idx, idx)]
    lats, lons = tile_sample_latlon(key, grid)
    lat_grid, lon_grid = np.meshgrid(lats, lons, indexing="ij")
    north, east = latlon_to_ne(lat_grid, lon_grid, origin)
    return grid_mesh_arrays(elev, north, east, skirt_m, scale)


def grid_mesh_arrays(
    elevation: np.ndarray,
    north: np.ndarray,
    east: np.ndarray,
    skirt_m: float = SKIRT_M,
    scale: float = SCENE_SCALE,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Mesh arrays for a rows x cols elevation grid (row 0 north) at (north, east) metres.

    Returns points (N, 3) in scene units, face counts, face indices, vertex colours and vertex
    normals (the skirt reuses its edge vertex's normal). A skirt
    of ``skirt_m`` runs down from every edge vertex so small gaps between neighbouring meshes
    are not visible. Colours combine the depth ramp with a baked hillshade, so relief reads
    even under flat scene lighting.
    """
    elev = fill_no_data(elevation)
    rows, cols = elev.shape
    surface = np.stack([east * scale, elev * scale, -north * scale], axis=-1).reshape(-1, 3)
    shade = hillshade(elev, north, east)
    surface_rgb = depth_colors(elev) * (
        (1.0 - HILLSHADE_WEIGHT) + HILLSHADE_WEIGHT * shade[..., None]
    )
    surface_rgb = surface_rgb.reshape(-1, 3)

    # Quads (row r is north of row r + 1); counter-clockwise seen from above (+Y).
    r, c = np.meshgrid(np.arange(rows - 1), np.arange(cols - 1), indexing="ij")
    tl = (r * cols + c).ravel()
    quads = np.stack([tl, tl + cols, tl + cols + 1, tl + 1], axis=-1)

    # Skirt: perimeter ring (clockwise from the north-west corner), lowered copies below it.
    ring = np.concatenate(
        [
            np.arange(0, cols),  # north edge, west to east
            np.arange(1, rows) * cols + (cols - 1),  # east edge, north to south
            (rows - 1) * cols + np.arange(cols - 2, -1, -1),  # south edge, east to west
            np.arange(rows - 2, 0, -1) * cols,  # west edge, south to north
        ]
    )
    lowered = surface[ring].copy()
    lowered[:, 1] -= skirt_m * scale
    base = len(surface)
    k = np.arange(len(ring))
    k1 = (k + 1) % len(ring)
    skirt = np.stack([ring[k], base + k, base + k1, ring[k1]], axis=-1)

    points = np.concatenate([surface, lowered]).astype(np.float32)
    indices = np.concatenate([quads, skirt]).astype(np.int32).ravel()
    counts = np.full(len(quads) + len(skirt), 4, dtype=np.int32)
    colors = np.concatenate([surface_rgb, surface_rgb[ring] * 0.6]).astype(np.float32)
    surface_n = surface_normals(elev, north, east).reshape(-1, 3)
    normals = np.concatenate([surface_n, surface_n[ring]]).astype(np.float32)
    return points, counts, indices, colors, normals


# --- Fused grids from /fuse (GeoTIFF, EPSG:3857) ------------------------------------------

WEB_MERCATOR_R = 6378137.0
GRID_BLOCK_PX = 256  # source pixels per mesh block side (before decimation)
GRID_STRIDE = 1  # every pixel: 30 m vertex spacing from a 30 m fusion (about 66k per mesh)

_TIFF_TYPES = {1: "B", 2: "c", 3: "H", 4: "I", 11: "f", 12: "d", 16: "Q"}


def parse_geotiff(data: bytes) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Elevation grid and pixel-centre coordinates from a single-band GeoTIFF.

    Supports what topobathykit's ``/fuse`` writes (GDAL GTiff defaults): uncompressed,
    striped, one float band, little- or big-endian, with ModelPixelScale and ModelTiepoint.
    Returns (elevation rows x cols with row 0 north, x per column, y per row) in the file's
    CRS units. Anything else raises ValueError rather than guessing.
    """
    import struct

    order = {b"II": "<", b"MM": ">"}.get(data[:2])
    if order is None or struct.unpack(order + "H", data[2:4])[0] != 42:
        raise ValueError("not a classic TIFF")
    ifd = struct.unpack(order + "I", data[4:8])[0]
    (count,) = struct.unpack(order + "H", data[ifd : ifd + 2])
    tags: dict[int, tuple[Any, ...]] = {}
    for i in range(count):
        entry = data[ifd + 2 + 12 * i : ifd + 14 + 12 * i]
        tag, typ, n = struct.unpack(order + "HHI", entry[:8])
        fmt = _TIFF_TYPES.get(typ)
        if fmt is None:
            continue
        size = struct.calcsize(fmt) * n
        raw = (
            entry[8:12]
            if size <= 4
            else data[(o := struct.unpack(order + "I", entry[8:12])[0]) : o + size]
        )
        tags[tag] = struct.unpack(order + fmt * n, raw[:size])

    width, height = tags[256][0], tags[257][0]
    if tags.get(259, (1,))[0] != 1:
        raise ValueError(f"compressed GeoTIFF (compression {tags[259][0]}) is not supported")
    if 322 in tags:
        raise ValueError("tiled GeoTIFF is not supported")
    if tags.get(277, (1,))[0] != 1:
        raise ValueError("multi-band GeoTIFF is not supported")
    bits = tags.get(258, (32,))[0]
    sample_format = tags.get(339, (3,))[0]
    if sample_format != 3 or bits not in (32, 64):
        raise ValueError(f"expected float32/64 samples, got format {sample_format}, {bits} bits")
    dtype = np.dtype(order + ("f4" if bits == 32 else "f8"))
    strips = b"".join(data[o : o + c] for o, c in zip(tags[273], tags[279], strict=True))
    elev = np.frombuffer(strips, dtype=dtype, count=width * height).reshape(height, width)

    scale_x, scale_y = tags[33550][0], tags[33550][1]
    tie = tags[33922]  # (i, j, k, x, y, z): raster point (i, j) maps to model (x, y)
    x0 = tie[3] - tie[0] * scale_x
    y0 = tie[4] + tie[1] * scale_y
    xs = x0 + (np.arange(width) + 0.5) * scale_x
    ys = y0 - (np.arange(height) + 0.5) * scale_y
    return elev.astype(np.float32), xs, ys


def mercator_to_latlon(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lon = np.degrees(np.asarray(x) / WEB_MERCATOR_R)
    lat = np.degrees(np.arctan(np.sinh(np.asarray(y) / WEB_MERCATOR_R)))
    return lat, lon


def grid_blocks(
    elev: np.ndarray,
    xs: np.ndarray,
    ys: np.ndarray,
    origin: tuple[float, float],
    block_px: int = GRID_BLOCK_PX,
    stride: int = GRID_STRIDE,
) -> Iterable[tuple[str, np.ndarray, np.ndarray, np.ndarray]]:
    """Cuts an EPSG:3857 grid into overlapping blocks: (name, elevation, north, east).

    Neighbouring blocks share their edge row and column, so meshes meet without gaps.
    """
    rows, cols = elev.shape
    step = block_px - (block_px % stride)
    for r0 in range(0, rows - 1, step):
        for c0 in range(0, cols - 1, step):
            r_idx = np.arange(r0, min(r0 + step, rows - 1) + 1, stride)
            c_idx = np.arange(c0, min(c0 + step, cols - 1) + 1, stride)
            if r_idx[-1] != min(r0 + step, rows - 1):
                r_idx = np.append(r_idx, min(r0 + step, rows - 1))
            if c_idx[-1] != min(c0 + step, cols - 1):
                c_idx = np.append(c_idx, min(c0 + step, cols - 1))
            if len(r_idx) < 2 or len(c_idx) < 2:
                continue
            lat, lon = mercator_to_latlon(xs[c_idx][None, :], ys[r_idx][:, None])
            lat, lon = np.broadcast_arrays(lat, lon)
            north, east = latlon_to_ne(lat, lon, origin)
            yield f"grid_r{r0}_c{c0}", elev[np.ix_(r_idx, c_idx)], north, east


def latlon_bounds(origin: tuple[float, float], bounds_ne: Iterable[float]) -> list[float]:
    """[west, south, east, north] degrees for (min_n, max_n, min_e, max_e) metres."""
    min_n, max_n, min_e, max_e = bounds_ne
    south, west = ne_to_latlon(min_n, min_e, origin)
    north, east = ne_to_latlon(max_n, max_e, origin)
    return [west, south, east, north]


# --- USD (Kit side) ------------------------------------------------------------------------


def recolour_dem_meshes(stage: Any, root: str = DEM_ROOT) -> int:
    """Re-bakes the colour of every DEM mesh under ``root`` (after ``set_in_situ``).

    Uses each mesh's own points and normals, so no tile is fetched or rebuilt. Returns how many
    meshes were recoloured.
    """
    from pxr import Sdf, Usd, UsdGeom, Vt

    base = stage.GetPrimAtPath(root)
    if not base or not base.IsValid():
        return 0
    count = 0
    for prim in Usd.PrimRange(base):
        if not prim.IsA(UsdGeom.Mesh):
            continue
        mesh = UsdGeom.Mesh(prim)
        points = mesh.GetPointsAttr().Get()
        normals = mesh.GetNormalsAttr().Get()
        if not points or not normals or len(points) != len(normals):
            continue
        elev = np.asarray(points, dtype=float)[:, 1] / SCENE_SCALE
        shade = normal_shade(np.asarray(normals, dtype=float))
        rgb = depth_colors(elev) * ((1.0 - HILLSHADE_WEIGHT) + HILLSHADE_WEIGHT * shade[:, None])
        UsdGeom.PrimvarsAPI(prim).CreatePrimvar(
            "displayColor", Sdf.ValueTypeNames.Color3fArray, UsdGeom.Tokens.vertex
        ).Set(Vt.Vec3fArray.FromNumpy(rgb.astype(np.float32)))
        count += 1
    return count


def write_dem_mesh(
    stage: Any,
    root: str,
    name: str,
    points: np.ndarray,
    counts: np.ndarray,
    indices: np.ndarray,
    colors: np.ndarray,
    normals: np.ndarray,
) -> None:
    """Writes one DEM mesh under ``root`` with the depth-shaded seabed material."""
    from pxr import Gf, Sdf, UsdGeom, UsdShade, Vt

    UsdGeom.Xform.Define(stage, root)
    mesh = UsdGeom.Mesh.Define(stage, f"{root}/{name}")
    mesh.GetPointsAttr().Set(Vt.Vec3fArray.FromNumpy(points))
    mesh.GetFaceVertexCountsAttr().Set(Vt.IntArray.FromNumpy(counts))
    mesh.GetFaceVertexIndicesAttr().Set(Vt.IntArray.FromNumpy(indices))
    mesh.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
    mesh.GetNormalsAttr().Set(Vt.Vec3fArray.FromNumpy(normals))
    mesh.SetNormalsInterpolation(UsdGeom.Tokens.vertex)
    mesh.CreateDoubleSidedAttr(True)  # skirt walls face inward; render both sides
    lo, hi = points.min(axis=0), points.max(axis=0)
    mesh.GetExtentAttr().Set([Gf.Vec3f(*(float(v) for v in lo)), Gf.Vec3f(*(float(v) for v in hi))])
    UsdGeom.PrimvarsAPI(mesh.GetPrim()).CreatePrimvar(
        "displayColor", Sdf.ValueTypeNames.Color3fArray, UsdGeom.Tokens.vertex
    ).Set(Vt.Vec3fArray.FromNumpy(colors))
    # Ground-plane texture coordinates (east, north) in detail-texture repeats
    st = np.stack([points[:, 0], -points[:, 2]], axis=-1) / (SCENE_SCALE * DETAIL_TILE_M)
    UsdGeom.PrimvarsAPI(mesh.GetPrim()).CreatePrimvar(
        "st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.vertex
    ).Set(Vt.Vec2fArray.FromNumpy(st.astype(np.float32)))
    UsdShade.MaterialBindingAPI.Apply(mesh.GetPrim()).Bind(seabed_material(stage, root))
    floor = stage.GetPrimAtPath("/World/SeaFloor")
    if floor and floor.IsValid():
        UsdGeom.Imageable(floor).MakeInvisible()


def seabed_material(stage: Any, root: str) -> Any:
    """Matte seabed whose base colour is the per-vertex depth ramp and hillshade."""
    from pxr import Gf, Sdf, UsdShade

    path = f"{root}/Looks/Seabed"
    if not stage.GetPrimAtPath(path).IsValid():
        material = UsdShade.Material.Define(stage, path)
        reader = UsdShade.Shader.Define(stage, f"{path}/DisplayColor")
        reader.CreateIdAttr("UsdPrimvarReader_float3")
        reader.CreateInput("varname", Sdf.ValueTypeNames.Token).Set("displayColor")
        # Dark fallback: if the primvar reader is not honoured the seafloor shows uniformly dark,
        # which is visibly wrong, rather than a plausible grey.
        reader.CreateInput("fallback", Sdf.ValueTypeNames.Float3).Set(Gf.Vec3f(0.03, 0.03, 0.05))
        reader_out = reader.CreateOutput("result", Sdf.ValueTypeNames.Float3)
        shader = UsdShade.Shader.Define(stage, f"{path}/PreviewSurface")
        shader.CreateIdAttr("UsdPreviewSurface")
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(reader_out)
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.95)
        shader.CreateInput("specularColor", Sdf.ValueTypeNames.Color3f).Set(
            Gf.Vec3f(0.02, 0.02, 0.02)
        )
        shader.CreateInput("useSpecularWorkflow", Sdf.ValueTypeNames.Int).Set(1)
        # Detail normal map (see set_seafloor_detail); scale 0 and bias +Z keep it flat (off)
        st_reader = UsdShade.Shader.Define(stage, f"{path}/St")
        st_reader.CreateIdAttr("UsdPrimvarReader_float2")
        st_reader.CreateInput("varname", Sdf.ValueTypeNames.Token).Set("st")
        st_out = st_reader.CreateOutput("result", Sdf.ValueTypeNames.Float2)
        detail = UsdShade.Shader.Define(stage, f"{path}/Detail")
        detail.CreateIdAttr("UsdUVTexture")
        detail.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(st_out)
        detail.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat")
        detail.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat")
        detail.CreateInput("sourceColorSpace", Sdf.ValueTypeNames.Token).Set("raw")
        detail.CreateInput("scale", Sdf.ValueTypeNames.Float4).Set(Gf.Vec4f(0, 0, 0, 1))
        detail.CreateInput("bias", Sdf.ValueTypeNames.Float4).Set(Gf.Vec4f(0, 0, 1, 0))
        detail_out = detail.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)
        shader.CreateInput("normal", Sdf.ValueTypeNames.Normal3f).ConnectToSource(detail_out)
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
    return UsdShade.Material(stage.GetPrimAtPath(path))


def set_seafloor_detail(stage: Any, on: bool, cache_dir: str, root: str = DEM_ROOT) -> bool:
    """Turns the seafloor detail normal map on or off; returns False if there is no seabed
    material yet (no DEM mesh written), True once applied.

    The texture is generated once into ``cache_dir``. Off, the map's scale is zero and its bias
    the flat normal, so the material shades exactly as without it.
    """
    import os

    from pxr import Gf, Sdf, UsdShade

    prim = stage.GetPrimAtPath(f"{root}/Looks/Seabed/Detail")
    if not prim or not prim.IsValid():
        return False
    detail = UsdShade.Shader(prim)
    if on:
        path = os.path.join(cache_dir, f"seafloor_detail_v1_{DETAIL_PIXELS}.png")
        if not os.path.exists(path):
            os.makedirs(cache_dir, exist_ok=True)
            write_png_rgb(path, detail_normal_map(detail_heightfield()))
        detail.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(path)
        detail.GetInput("scale").Set(Gf.Vec4f(2, 2, 2, 1))
        detail.GetInput("bias").Set(Gf.Vec4f(-1, -1, -1, 0))
    else:
        detail.GetInput("scale").Set(Gf.Vec4f(0, 0, 0, 1))
        detail.GetInput("bias").Set(Gf.Vec4f(0, 0, 1, 0))
    return True


def tile_prim_name(key: TileKey) -> str:
    z, x, y = key
    return f"z{z}_{x}_{y}"


def parse_tile_npz(data: bytes) -> np.ndarray | None:
    """The elevation array from a topobathykit ``.npz`` tile, or None."""
    with np.load(io.BytesIO(data)) as npz:
        for name in ("elevation", "arr_0"):
            if name in npz:
                return np.array(npz[name], dtype=np.float32)
    return None


# --- Streaming (Kit side) ----------------------------------------------------------------


class DemTileStreamer:
    """Keeps a working set of DEM tile meshes under ``root`` for one origin.

    ``set_prefetch`` pins the tiles covering the deployment's uncertainty bounds;
    ``update`` adds tiles around focus points (camera, active animal) and drops the farthest
    unpinned tiles once ``max_tiles`` is exceeded. Fetches run on Kit's asyncio loop, at most
    ``concurrency`` at a time; a generation counter discards results after ``shutdown``.
    Failed tiles are retried on later ``update`` calls with growing backoff, up to
    ``MAX_TILE_ATTEMPTS``; pinned tiles are retried by re-requesting them on each update.
    """

    def __init__(
        self,
        get_stage: Callable[[], Any],
        origin: tuple[float, float],
        service_url: str,
        log: Callable[[str], None],
        root: str = DEM_ROOT,
        max_tiles: int = 48,
        concurrency: int = 4,
        timeout_s: float = 900.0,
    ) -> None:
        self._get_stage = get_stage
        self.origin = origin
        self.service_url = service_url.rstrip("/")
        self._log = log
        self.root = root
        self.max_tiles = max_tiles
        self._timeout_s = timeout_s
        self._sem = asyncio.Semaphore(concurrency)
        self._pinned: set[TileKey] = set()
        self._loaded: set[TileKey] = set()
        self._pending: set[TileKey] = set()
        # key -> (attempts, earliest retry time); cold tiles often answer 503 at first
        self._failed: dict[TileKey, tuple[int, float]] = {}
        self._tasks: set[asyncio.Future[None]] = set()  # the loop only holds weak references
        self._generation = 0

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)

    def set_prefetch(self, bounds_ne: Iterable[float]) -> None:
        self._pinned = tiles_for_bounds(self.origin, bounds_ne)
        self._log(f"DEM prefetch: {len(self._pinned)} tiles at zoom {TILE_ZOOM}")
        self._request(self._pinned)

    def update(self, focus_ne: Iterable[tuple[float, float]]) -> None:
        focus = list(focus_ne)
        wanted: set[TileKey] = set(self._pinned)  # re-request pinned tiles that failed
        for north, east in focus:
            wanted |= tiles_around(self.origin, north, east, radius=1)
        self._request(wanted)
        self._evict(focus_ne=focus)

    def shutdown(self) -> None:
        self._generation += 1
        self._pending.clear()

    # -- internals --

    def _request(self, keys: Iterable[TileKey]) -> None:
        now = time.monotonic()
        for key in keys:
            if key in self._loaded or key in self._pending:
                continue
            attempts, retry_at = self._failed.get(key, (0, 0.0))
            if attempts >= MAX_TILE_ATTEMPTS or now < retry_at:
                continue
            self._pending.add(key)
            task = asyncio.ensure_future(self._fetch_and_build(key, self._generation))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

    async def _fetch_and_build(self, key: TileKey, generation: int) -> None:
        import aiohttp

        z, x, y = key
        url = f"{self.service_url}/tiles/{z}/{x}/{y}.npz"
        try:
            async with self._sem:
                if generation != self._generation:
                    return
                timeout = aiohttp.ClientTimeout(total=self._timeout_s)
                async with (
                    aiohttp.ClientSession(timeout=timeout) as session,
                    session.get(url) as resp,
                ):
                    if resp.status != 200:
                        raise RuntimeError(f"HTTP {resp.status}")
                    data = await resp.read()
            elevation = parse_tile_npz(data)
            if elevation is None:
                raise RuntimeError("no elevation array in tile")
            if generation != self._generation:
                return
            arrays = build_tile_arrays(elevation, key, self.origin)
            stage = self._get_stage()
            if stage is None:
                return
            write_dem_mesh(stage, self.root, tile_prim_name(key), *arrays)
            self._loaded.add(key)
            self._failed.pop(key, None)
            lo, hi = float(np.nanmin(elevation)), float(np.nanmax(elevation))
            self._log(
                f"DEM tile {z}/{x}/{y} loaded ({len(self._loaded)} total; "
                f"elevation {lo:.0f} to {hi:.0f} m)"
            )
        except Exception as e:  # network, service and parse errors are logged, not raised
            attempts = self._failed.get(key, (0, 0.0))[0] + 1
            self._failed[key] = (attempts, time.monotonic() + RETRY_BACKOFF_S * attempts)
            final = " (giving up)" if attempts >= MAX_TILE_ATTEMPTS else ""
            self._log(f"DEM tile {z}/{x}/{y} failed, attempt {attempts}: {e}{final}")
        finally:
            self._pending.discard(key)

    def _evict(self, focus_ne: list[tuple[float, float]]) -> None:
        if len(self._loaded) <= self.max_tiles:
            return
        stage = self._get_stage()
        if stage is None or not focus_ne:
            return

        def distance(key: TileKey) -> float:
            lats, lons = tile_sample_latlon(key, grid=2)
            n, e = latlon_to_ne(float(lats.mean()), float(lons.mean()), self.origin)
            return min(math.hypot(float(n) - fn, float(e) - fe) for fn, fe in focus_ne)

        candidates = sorted(self._loaded - self._pinned, key=distance, reverse=True)
        for key in candidates[: len(self._loaded) - self.max_tiles]:
            stage.RemovePrim(f"{self.root}/{tile_prim_name(key)}")
            self._loaded.discard(key)


class DemGridSource:
    """One fused DEM for the deployment area, fetched with a custom topobathykit policy.

    ``/tiles`` only serves the server's default policy, so with a policy configured the viz
    asks ``POST /fuse`` once for the prefetch bounds (hydrate that area first so it returns
    from cache), keeps the GeoTIFF in ``cache_dir`` keyed by policy, bounds and resolution,
    and cuts it into meshes. It never calls ``/tiles`` or the server's policy endpoints.
    Same interface as ``DemTileStreamer``; ``update`` is a no-op.
    """

    def __init__(
        self,
        get_stage: Callable[[], Any],
        origin: tuple[float, float],
        service_url: str,
        policy_yaml: str,
        cache_dir: str,
        log: Callable[[str], None],
        resolution_m: float = 30.0,
        root: str = DEM_ROOT,
        timeout_s: float = 3 * 3600.0,
    ) -> None:
        self._get_stage = get_stage
        self.origin = origin
        self.service_url = service_url.rstrip("/")
        self._policy_yaml = policy_yaml
        self._cache_dir = cache_dir
        self._log = log
        self.resolution_m = resolution_m
        self.root = root
        self._timeout_s = timeout_s
        self._generation = 0
        self._started = False
        self._blocks = 0
        self._task: asyncio.Future[None] | None = None  # the loop only holds a weak reference

    @property
    def loaded_count(self) -> int:
        return self._blocks

    def set_prefetch(self, bounds_ne: Iterable[float]) -> None:
        if self._started:
            return
        self._started = True
        bbox = [round(v, 4) for v in latlon_bounds(self.origin, bounds_ne)]
        self._task = asyncio.ensure_future(self._load(bbox, self._generation))

    def update(self, focus_ne: Iterable[tuple[float, float]]) -> None:
        pass  # the whole prefetch area is loaded at once

    def shutdown(self) -> None:
        self._generation += 1

    def cache_path(self, bbox: list[float]) -> str:
        import hashlib
        import os

        key = hashlib.sha256(
            f"{self._policy_yaml}|{bbox}|{self.resolution_m}".encode()
        ).hexdigest()[:16]
        return os.path.join(self._cache_dir, f"fuse_{key}.tif")

    async def _load(self, bbox: list[float], generation: int) -> None:
        import os

        path = self.cache_path(bbox)
        try:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    data = f.read()
                self._log(f"DEM grid from cache: {path}")
            else:
                data = await self._fetch(bbox)
                os.makedirs(self._cache_dir, exist_ok=True)
                with open(path, "wb") as f:
                    f.write(data)
                self._log(f"DEM grid fused and cached: {path} ({len(data) / 1e6:.1f} MB)")
            if generation != self._generation:
                return
            elev, xs, ys = parse_geotiff(data)
            self._build(elev, xs, ys)
        except Exception as e:  # network, service and parse errors are logged, not raised
            self._log(f"DEM grid failed: {e}")

    async def _fetch(self, bbox: list[float]) -> bytes:
        import aiohttp

        self._log(f"DEM grid: POST /fuse bbox {bbox} at {self.resolution_m:.0f} m (custom policy)")
        body = {
            "bbox": bbox,
            "resolution": self.resolution_m,
            "format": "geotiff",
            "policy_yaml": self._policy_yaml,
        }
        timeout = aiohttp.ClientTimeout(total=self._timeout_s)
        async with (
            aiohttp.ClientSession(timeout=timeout) as session,
            session.post(f"{self.service_url}/fuse", json=body) as resp,
        ):
            if resp.status != 200:
                raise RuntimeError(f"HTTP {resp.status}: {(await resp.text())[:200]}")
            data: bytes = await resp.read()
            return data

    def _build(self, elev: np.ndarray, xs: np.ndarray, ys: np.ndarray) -> None:
        stage = self._get_stage()
        if stage is None:
            return
        for name, block, north, east in grid_blocks(elev, xs, ys, self.origin):
            write_dem_mesh(stage, self.root, name, *grid_mesh_arrays(block, north, east))
            self._blocks += 1
        valid = elev[np.isfinite(elev)]
        self._log(
            f"DEM grid loaded: {elev.shape[1]} x {elev.shape[0]} px in {self._blocks} meshes; "
            f"elevation {float(valid.min()):.0f} to {float(valid.max()):.0f} m"
            if valid.size
            else "DEM grid loaded but has no valid elevation"
        )
