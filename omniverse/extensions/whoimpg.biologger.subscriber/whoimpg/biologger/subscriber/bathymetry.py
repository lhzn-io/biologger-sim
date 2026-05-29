import io
import math

import aiohttp
import carb
import numpy as np
from pxr import Gf, Usd, UsdGeom


class BathymetryBridge:
    def __init__(self, service_url: str = "http://localhost:9595"):
        self.service_url = service_url
        self.points_x = 512
        self.points_y = 512

    async def fetch_elevation(
        self, north: float, south: float, west: float, east: float
    ) -> np.ndarray | None:
        """
        Fetches and stitches elevation data from the topobathysim tiled service.
        Returns a float32 numpy array or None on failure.
        """
        import asyncio

        from scipy.ndimage import zoom

        cov_url = f"{self.service_url}/tiles/coverage"
        params = {
            "north": str(north),
            "south": str(south),
            "west": str(west),
            "east": str(east),
            "zoom": "11",
        }

        try:
            async with aiohttp.ClientSession() as session:
                carb.log_warn(
                    f"[BathymetryBridge] Requesting coverage: {cov_url} with params {params}"
                )
                async with session.get(cov_url, params=params, timeout=30) as resp:
                    if resp.status != 200:
                        carb.log_error(
                            f"[BathymetryBridge] Coverage returned {resp.status}: {await resp.text()}"
                        )
                        return None
                    coverage_data = await resp.json()

                tiles = coverage_data.get("tiles", [])
                if not tiles:
                    carb.log_warn("[BathymetryBridge] No tiles returned for coverage.")
                    return None

                xs = [t["x"] for t in tiles]
                ys = [t["y"] for t in tiles]
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)

                cols = max_x - min_x + 1
                rows = max_y - min_y + 1

                full_w = cols * 512
                full_h = rows * 512

                stitched = np.full((full_h, full_w), -100.0, dtype=np.float32)

                all_norths = [t["bounds"]["north"] for t in tiles if "bounds" in t]
                all_souths = [t["bounds"]["south"] for t in tiles if "bounds" in t]
                all_easts = [t["bounds"]["east"] for t in tiles if "bounds" in t]
                all_wests = [t["bounds"]["west"] for t in tiles if "bounds" in t]

                if not all_norths:
                    carb.log_error("[BathymetryBridge] No bounds found in tile data.")
                    return None

                grid_north = max(all_norths)
                grid_south = min(all_souths)
                grid_east = max(all_easts)
                grid_west = min(all_wests)

                async def fetch_tile(t: dict) -> bool:
                    z, x, y = t["z"], t["x"], t["y"]
                    tile_url = f"{self.service_url}/tiles/{z}/{x}/{y}.npz"
                    for attempt in range(1, 4):
                        try:
                            async with session.get(tile_url, timeout=300) as tile_resp:
                                if tile_resp.status == 200:
                                    data_bytes = await tile_resp.read()
                                    with io.BytesIO(data_bytes) as f, np.load(f) as data_loaded:
                                        tile_data = None
                                        if "elevation" in data_loaded:
                                            tile_data = data_loaded["elevation"]
                                        elif "arr_0" in data_loaded:
                                            tile_data = data_loaded["arr_0"]

                                            if tile_data is not None:
                                                # Standardize tile to 512x512
                                                if tile_data.shape != (512, 512):
                                                    tile_data = zoom(
                                                        tile_data.astype(np.float32),
                                                        (
                                                            512.0 / tile_data.shape[0],
                                                            512.0 / tile_data.shape[1],
                                                        ),
                                                        order=1,
                                                    )

                                                c_idx = x - min_x
                                                r_idx = y - min_y
                                                y_start = r_idx * 512
                                                x_start = c_idx * 512
                                                stitched[
                                                    y_start : y_start + 512, x_start : x_start + 512
                                                ] = tile_data
                                                return True
                                return False
                        except Exception as e:
                            if attempt == 3:
                                carb.log_warn(
                                    f"[BathymetryBridge] Tile {z}/{x}/{y} failed on attempt {attempt}: {e}"
                                )
                            await asyncio.sleep(2 * attempt)
                    return False

                # Concurrently fetch all required tiles
                carb.log_info(f"[BathymetryBridge] Queuing {len(tiles)} tile fetch tasks...")
                fetch_tasks = [fetch_tile(t) for t in tiles]
                results = await asyncio.gather(*fetch_tasks)

                carb.log_info(
                    f"[BathymetryBridge] Successfully fetched and stitched {sum(results)}/{len(tiles)} tiles."
                )

                lon_span = grid_east - grid_west
                lat_span = grid_north - grid_south
                if lon_span > 0 and lat_span > 0:
                    px_west_f = (west - grid_west) / lon_span * full_w
                    px_east_f = (east - grid_west) / lon_span * full_w
                    py_north_f = (grid_north - north) / lat_span * full_h
                    py_south_f = (grid_north - south) / lat_span * full_h

                    r0 = int(np.clip(py_north_f, 0, full_h - 1))
                    r1 = int(np.clip(py_south_f, 1, full_h))
                    c0 = int(np.clip(px_west_f, 0, full_w - 1))
                    c1 = int(np.clip(px_east_f, 1, full_w))

                    if r1 > r0 and c1 > c0:
                        cropped = stitched[r0:r1, c0:c1].astype(np.float32)
                        carb.log_info(
                            f"[BathymetryBridge] Final crop: grid {full_w}x{full_h}px -> {cropped.shape[1]}x{cropped.shape[0]}px"
                        )
                        return cropped

                return stitched.astype(np.float32)

        except Exception as e:
            carb.log_error(f"[BathymetryBridge] Failed: {e}")
            return None

    def create_mesh(
        self,
        stage: Usd.Stage,
        path: str,
        elevation: np.ndarray,
        bounds: tuple[float, float, float, float],
    ) -> UsdGeom.Mesh:
        """
        Creates a UsdGeom.Mesh at the specified path using the elevation data.

        Args:
            stage: The Usd.Stage to write to.
            path: The prim path (e.g. "/World/Bathymetry").
            elevation: 2D numpy array of heights (Z-up in source, becomes Y-up in USD).
            bounds: (north, south, west, east) in degrees.
        """
        north, south, west, east = bounds

        rows, cols = elevation.shape
        # Total Real-World Dimensions
        # Approximate conversion: 1 deg lat ~= 111km, 1 deg lon ~= 111km * cos(lat)
        # We need to map this to USD units (assuming meters).

        # Center lat for scaling
        center_lat = (north + south) / 2.0
        deg_to_m_lat = 111320.0
        deg_to_m_lon = 111320.0 * math.cos(math.radians(center_lat))

        # Calculate dimensions in meters
        height_m = (north - south) * deg_to_m_lat
        width_m = (east - west) * deg_to_m_lon

        # Grid spacing
        # Note: 'elevation' is typically [y, x] ie [row, col]
        # Rows correspond to Latitude (North to South usually)
        # Cols correspond to Longitude (West to East)

        # Create Mesh Points
        # USD: Y-Up.  Map:
        # Real North (+Lat) -> -Z (Standard USD convention: -Z is forward/north)
        # Real East  (+Lon) -> +X
        # Real Up    (+Alt) -> +Y

        # Mesh Construction
        # Generate grid of X, Z coords centered at (0,0,0) or matching the bounds?
        # Usually we want the mesh processing to center the tile at (0,0) local,
        # and we assume the stage origin represents the center of our bounds.

        points = []

        # Iterate rows (North to South) -> USD -Z to +Z
        # Wait:
        # If rows[0] is North (max lat), that corresponds to -Z (assuming -Z is North)
        # If rows[-1] is South (min lat), that corresponds to +Z

        # Let's align center:
        # X range: -width/2 to +width/2
        # Z range: -height/2 to +height/2

        # Source data: 0 is Top-Left (North-West)

        for r in range(rows):
            # Z coordinate:
            # Row 0 is North -> -height/2
            # Row N is South -> +height/2
            # Wait, usually we map 0 to min and N to max, or vice versa?
            # Creating a grid:
            # Actually, if Row 0 is North, and North is -Z (Forward),
            # Then Row 0 should be -Z_max (or min Z).
            # Let's stick to standard map tile logic:
            # y=0 is North.
            # So z should go from -half to +half?
            # Let's verify standard USD orientation. Usually -Z is "forward" into the screen.
            # If North is forward, North is -Z.
            # So Row 0 (North) -> z = -height_m / 2.0
            # Row N (South) -> z = +height_m / 2.0
            # This implies Z increases as we go South. Correct.

            z = (r / (rows - 1)) * height_m - (height_m / 2.0)
            # Re-verify:
            # r=0 -> -h/2 (North)
            # r=max -> +h/2 (South)

            for c in range(cols):
                # X coordinate:
                # Col 0 (West) -> -width/2
                # Col N (East) -> +width/2
                x = (c / (cols - 1)) * width_m - (width_m / 2.0)

                # Y coordinate (Height)
                # Elevation data in meters
                y = float(elevation[r, c])

                # Check for NaN (Topobathy uses NaN for no data?)
                # If NaN, set to a deep value or interpolate?
                if np.isnan(y):
                    y = -100.0  # Default Deep

                points.append(Gf.Vec3f(x, y, z))

        # Define Topology (Quads)
        # (rows-1) * (cols-1) quads
        face_vertex_counts = []
        face_vertex_indices = []

        for r in range(rows - 1):
            for c in range(cols - 1):
                # Quad vertices:
                # Top-Left: (r, c)
                # Top-Right: (r, c+1)
                # Bottom-Right: (r+1, c+1)
                # Bottom-Left: (r+1, c)

                idx_tl = r * cols + c
                idx_tr = r * cols + (c + 1)
                idx_br = (r + 1) * cols + (c + 1)
                idx_bl = (r + 1) * cols + c

                # Winding order: CCW for front face?
                # USD default is Right-Handed, CCW.
                # Let's try standard CCW: TL -> BL -> BR -> TR ?
                # Or TL -> TR -> BR -> BL ?
                # If we look from top (+Y), and use (x, z):
                # TL: (-x, -z)
                # TR: (+x, -z)
                # BR: (+x, +z)
                # BL: (-x, +z)
                # CCW would be: TL -> BL -> BR -> TR?
                # Let's try: TL, TR, BR, BL

                face_vertex_counts.append(4)
                face_vertex_indices.extend([idx_tl, idx_tr, idx_br, idx_bl])

        # Create USD Prim
        mesh = UsdGeom.Mesh.Define(stage, path)
        mesh.GetPointsAttr().Set(points)
        mesh.GetFaceVertexCountsAttr().Set(face_vertex_counts)
        mesh.GetFaceVertexIndicesAttr().Set(face_vertex_indices)

        # Set Extent (Bounding Box) for culling
        # Optional but good practice
        # Casting numpy results to float to avoid Boost.Python ArgumentError
        extent = [
            Gf.Vec3f(-width_m / 2, float(np.nanmin(elevation)), -height_m / 2),
            Gf.Vec3f(width_m / 2, float(np.nanmax(elevation)), height_m / 2),
        ]
        mesh.GetExtentAttr().Set(extent)

        carb.log_info(f"[BathymetryBridge] Created mesh at {path} with {len(points)} vertices.")

        # Cleanup Pre-existing Floor
        # Try to find common floor names and hide them
        floor_names = [
            "/World/OceanFloor",
            "/World/GroundPlane",
            "/World/Ground",
            "/World/sea_bottom",
        ]
        for p in floor_names:
            prim = stage.GetPrimAtPath(p)
            if prim.IsValid():
                carb.log_info(f"[BathymetryBridge] Hiding existing floor: {p}")
                # Set visibility to invisible
                imageable = UsdGeom.Imageable(prim)
                imageable.MakeInvisible()

        return mesh
