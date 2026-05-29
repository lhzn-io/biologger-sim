import logging
import math

import numpy as np
import requests


class TopobathymetryClient:
    """
    Client for fetching and querying topobathymetry elevation from the topobathysim service.

    Architecture:
    - Fetches 512x512 float32 tiles (NPY format) from localhost:9595
    - Caches tiles in memory (LRU)
    - specific query(lat, lon) -> elevation_meters (MSL)
    """

    def __init__(self, base_url: str = "http://localhost:9595", max_cache_size: int = 16):
        self.base_url = base_url
        self.max_cache_size = max_cache_size
        self.cache: dict[
            tuple[int, int, int], tuple[np.ndarray, tuple[float, float, float, float]]
        ] = {}
        self.access_order: list[tuple[int, int, int]] = []
        self.logger = logging.getLogger(__name__)

    def _latlon_to_tile(self, lat: float, lon: float, zoom: int) -> tuple[int, int]:
        """Convert lat/lon to Web Mercator tile coordinates."""
        n = 2.0**zoom
        xtile = int((lon + 180.0) / 360.0 * n)
        lat_rad = math.radians(lat)
        ytile = int(
            (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n
        )
        return xtile, ytile

    def _tile_to_bounds(
        self, xtile: int, ytile: int, zoom: int
    ) -> tuple[float, float, float, float]:
        """
        Returns (min_lat, max_lat, min_lon, max_lon) for a given tile.
        """
        n = 2.0**zoom
        lon_min = xtile / n * 360.0 - 180.0
        lon_max = (xtile + 1) / n * 360.0 - 180.0

        # Lat is trickier due to mercator
        def y_to_lat(y):
            return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))

        lat_max = y_to_lat(ytile)
        lat_min = y_to_lat(ytile + 1)
        return lat_min, lat_max, lon_min, lon_max

    def fetch_tile(self, z: int, x: int, y: int) -> np.ndarray | None:
        """Fetches NPZ tile from service."""
        key = (z, x, y)
        if key in self.cache:
            # Update LRU
            if key in self.access_order:
                self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key][0]

        url = f"{self.base_url}/tiles/{z}/{x}/{y}.npz"
        try:
            resp = requests.get(url, timeout=300)
            if resp.status_code == 200:
                import io

                buf = io.BytesIO(resp.content)
                with np.load(buf) as data_loaded:
                    arr = None
                    if "elevation" in data_loaded:
                        arr = data_loaded["elevation"]
                    elif "arr_0" in data_loaded:
                        arr = data_loaded["arr_0"]

                    if arr is None:
                        self.logger.warning(f"Failed to find elevation array in tile {z}/{x}/{y}")
                        return None

                    # Convert to standard numpy array copy to detach from the closed npz file handle
                    arr = np.array(arr)

                # Cache it
                bounds = self._tile_to_bounds(x, y, z)

                # Evict if full
                if len(self.cache) >= self.max_cache_size:
                    evict = self.access_order.pop(0)
                    del self.cache[evict]

                self.cache[key] = (arr, bounds)
                self.access_order.append(key)
                return arr
            else:
                self.logger.warning(f"Failed to fetch tile {z}/{x}/{y}: {resp.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Error fetching tile {z}/{x}/{y}: {e}")
            return None

    def get_elevation_bilinear(self, lat: float, lon: float, zoom: int = 11) -> float | None:
        """
        Gets elevation at specific lat/lon using bilinear interpolation on the tile.
        """
        xtile, ytile = self._latlon_to_tile(lat, lon, zoom)

        arr = self.fetch_tile(zoom, xtile, ytile)
        if arr is None:
            return None

        # Get bounds to map lat/lon to pixel coordinates
        # Cached bounds are (min_lat, max_lat, min_lon, max_lon)
        # Note: self.cache[key] returns (arr, bounds)
        # Check carefully: fetch_tile returns just arr, but we stored bounds in cache.
        # Let's retrieve properly.
        key = (zoom, xtile, ytile)
        _, (min_lat, max_lat, min_lon, max_lon) = self.cache[key]

        # Array shape is likely (512, 512).
        # Pixel calculation:
        # 0,0 is usually TOP-LEFT (max_lat, min_lon) in image coords
        # Rasterio conventions depend on the service write.
        # Assuming standard Image coordinates: Y goes DOWN, X goes RIGHT.
        # Config: 512x512

        rows, cols = arr.shape

        # Normalize lat/lon to [0, 1] within the tile
        # Lon: min -> max
        x_norm = (lon - min_lon) / (max_lon - min_lon)

        # Lat: max -> min (Y axis inverted in image)
        # Mercator is non-linear, but for a single Level 13 tile (approx 2-4km), linear approx is okay?
        # Ideally we map the exact mercator projection, but linear is fast.
        # Let's use linear scaling from bounds.
        y_norm = (max_lat - lat) / (max_lat - min_lat)

        # Pixel coords
        x_px = x_norm * (cols - 1)
        y_px = y_norm * (rows - 1)

        # Bilinear Interpolation
        x0 = int(x_px)
        x1 = min(x0 + 1, cols - 1)
        y0 = int(y_px)
        y1 = min(y0 + 1, rows - 1)

        # Clamp
        x0 = max(0, min(x0, cols - 1))
        y0 = max(0, min(y0, rows - 1))

        # Weights
        wx = x_px - x0
        wy = y_px - y0

        # Values
        # Note: arr is (Y, X) usually
        v00 = arr[y0, x0]
        v10 = arr[y0, x1]
        v01 = arr[y1, x0]
        v11 = arr[y1, x1]

        # Interpolate X (top and bottom)
        top = v00 * (1 - wx) + v10 * wx
        bot = v01 * (1 - wx) + v11 * wx

        # Interpolate Y
        val = top * (1 - wy) + bot * wy

        return float(val)

    def prefetch_grid(self, lat: float, lon: float, zoom: int = 11, radius: int = 1) -> None:
        """
        Pre-fetches a grid of tiles around the given location to ensure cache is hot.
        radius=1 fetches a 3x3 grid (center + neighbors).
        """
        center_x, center_y = self._latlon_to_tile(lat, lon, zoom)

        self.logger.info(
            f"Prefetching topobathymetry grid around {lat}, {lon} (Tile {center_x}, {center_y}) radius={radius}"
        )

        count = 0
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                tx = center_x + dx
                ty = center_y + dy
                # Check if already cached to avoid log spam/redundant checks
                if (zoom, tx, ty) not in self.cache:
                    self.fetch_tile(zoom, tx, ty)
                    count += 1

        self.logger.info(f"Prefetched {count} topobathymetry tiles.")
