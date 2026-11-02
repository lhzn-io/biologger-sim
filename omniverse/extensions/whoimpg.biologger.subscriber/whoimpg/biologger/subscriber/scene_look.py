# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Scene look: the real sun, a matching analytic sky, a water surface and underwater haze.

Once the simulator's georeference arrives, the sun is placed where it stood over the
deployment's start fix at a chosen local solar time on the deployment date (default 09:00).
The sky dome is a Preetham (1999) clear-sky image computed for that sun and written as a
Radiance HDR, so the sky's colour and brightness gradient match the light on the seafloor. The
water surface is a thin refractive interface (index 1.333) that reflects the sky at grazing
angles. Below the surface, distance fog in the deep-water colour stands in for the
attenuation of the water column, with a configurable horizontal visibility.

Array building is plain NumPy; Kit and USD are touched only in ``apply_scene_look`` and
``update_underwater``.
"""

from __future__ import annotations

import math
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import numpy as np

# Linear sRGB of optically deep water seen from above (matches dem_tiles.WATER_RGB).
WATER_RGB = (0.010, 0.040, 0.115)
WATER_IOR = 1.333
DEFAULT_SOLAR_HOUR = 9.0  # local solar time on the deployment date
NEUTRAL_SUN = (45.0, 135.0)  # elevation, azimuth before a georeference arrives
DEFAULT_TURBIDITY = 2.0  # clear maritime air
# Direct sun against sky light: on level ground 7000 * sin(43 deg) is about 3.4 times the sky
# dome's irradiance at 300, close to a clear morning's direct-to-diffuse ratio.
DEFAULT_SUN_INTENSITY = 7000.0
DEFAULT_SKY_INTENSITY = 300.0
DEFAULT_F_NUMBER = 11.0  # fixed exposure (ISO 100, 1/50 s): shelf mid-tone, sky unclipped
# How RTX (Kit 109) shows our lat-long sky on this Y-up stage. Its lat-long domes are Z-up, so
# the dome is tilted -90 degrees about X; a further -90 degree yaw puts the sky's circumsolar
# peak on the sun light. Calibrated by locating that peak in captures with the sun at azimuths
# 108 and 250 degrees (both within 1 degree). Overridable for recalibration
# (``look/domeTiltXDeg``, ``look/domeYawDeg``, ``look/domeFlipV``).
DOME_FLIP_V = False
DOME_YAW_DEG = -90.0
DOME_TILT_X_DEG = -90.0
LOOK_SETTINGS = "/exts/whoimpg.biologger.subscriber/look"
DEFAULT_VISIBILITY_M = 40.0  # horizontal visibility underwater (about 4.8 / beam attenuation)
DEEP_WATER_M = 150.0  # scene depth below which the surface is out of view (see UnderwaterFog)
SKY_WIDTH = 1024
HORIZON_WHITE = (0.86, 0.93, 1.0)  # white-balance target for the mean horizon (R, G, B ratio)
SKY_MODEL_VERSION = 2  # part of the sky cache name: bump whenever sky_equirect's output changes
SCENE_SCALE = 100.0  # metres -> scene centimetres

SUN_PATH = "/World/SunLight"
DOME_PATH = "/World/EnvironmentLight"
WATER_PRIM = "/World/OceanVolume"
WATER_MATERIAL = "/World/Looks/SeaSurface"


# --- Sun ---------------------------------------------------------------------------------


def sun_position(lat: float, lon: float, when: datetime) -> tuple[float, float]:
    """Solar elevation and azimuth (degrees; azimuth clockwise from north) at a UTC time.

    NOAA general solar position approximation, good to about half a degree.
    """
    when = when.astimezone(timezone.utc)
    doy = when.timetuple().tm_yday
    hour = when.hour + when.minute / 60 + when.second / 3600
    g = 2 * math.pi / 365 * (doy - 1 + (hour - 12) / 24)
    eqt = 229.18 * (
        0.000075
        + 0.001868 * math.cos(g)
        - 0.032077 * math.sin(g)
        - 0.014615 * math.cos(2 * g)
        - 0.040849 * math.sin(2 * g)
    )
    decl = (
        0.006918
        - 0.399912 * math.cos(g)
        + 0.070257 * math.sin(g)
        - 0.006758 * math.cos(2 * g)
        + 0.000907 * math.sin(2 * g)
        - 0.002697 * math.cos(3 * g)
        + 0.00148 * math.sin(3 * g)
    )
    ha = math.radians((hour * 60 + eqt + 4 * lon) / 4 - 180)
    phi = math.radians(lat)
    cos_z = math.sin(phi) * math.sin(decl) + math.cos(phi) * math.cos(decl) * math.cos(ha)
    zen = math.acos(max(-1.0, min(1.0, cos_z)))
    az = math.degrees(
        math.atan2(math.sin(ha), math.cos(ha) * math.sin(phi) - math.tan(decl) * math.cos(phi))
    )
    return 90.0 - math.degrees(zen), (az + 180.0) % 360.0


def solar_time_utc(epoch_s: float, lon: float, solar_hour: float) -> datetime:
    """UTC time of ``solar_hour`` local mean solar time on the local date of ``epoch_s``."""
    local = datetime.fromtimestamp(epoch_s, tz=timezone.utc) + timedelta(hours=lon / 15.0)
    midnight = datetime(local.year, local.month, local.day, tzinfo=timezone.utc)
    return midnight + timedelta(hours=solar_hour - lon / 15.0)


def sun_rotate_xyz(elevation_deg: float, azimuth_deg: float) -> tuple[float, float, float]:
    """``rotateXYZ`` for a DistantLight (shines along its -Z) with this sun, Y-up stage.

    Scene axes: x east, y up, z south.
    """
    return (-elevation_deg, 180.0 - azimuth_deg, 0.0)


def sun_vector(elevation_deg: float, azimuth_deg: float) -> np.ndarray:
    """Unit vector toward the sun in scene axes (x east, y up, z south)."""
    el, az = math.radians(elevation_deg), math.radians(azimuth_deg)
    return np.array([math.cos(el) * math.sin(az), math.sin(el), -math.cos(el) * math.cos(az)])


# --- Sky (Preetham clear-sky model) --------------------------------------------------------

_XYZ_TO_RGB = np.array(
    [[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]]
)


def _perez(theta: np.ndarray, gamma: np.ndarray, c: tuple[float, ...]) -> np.ndarray:
    a, b, cc, d, e = c
    cos_t = np.maximum(np.cos(theta), 0.01)
    return np.asarray(
        (1 + a * np.exp(b / cos_t)) * (1 + cc * np.exp(d * gamma) + e * np.cos(gamma) ** 2)
    )


def sky_radiance(
    dirs: np.ndarray, sun_el_deg: float, turbidity: float = DEFAULT_TURBIDITY
) -> np.ndarray:
    """Linear sRGB sky radiance (..., 3) for unit view directions (x, y up, z).

    Preetham, Shirley and Smits (1999). Relative units (the zenith luminance in kcd/m2).
    Directions are relative to the sun's azimuth, which the caller rotates out: the sun lies
    in the y-z plane on the -z side, so only its elevation matters here. Below the horizon
    the sky is held at its horizon value.
    """
    t = turbidity
    theta_s = math.radians(90.0 - max(sun_el_deg, 0.5))
    cy = (
        0.1787 * t - 1.4630,
        -0.3554 * t + 0.4275,
        -0.0227 * t + 5.3251,
        0.1206 * t - 2.5771,
        -0.0670 * t + 0.3703,
    )
    cx = (
        -0.0193 * t - 0.2592,
        -0.0665 * t + 0.0008,
        -0.0004 * t + 0.2125,
        -0.0641 * t - 0.8989,
        -0.0033 * t + 0.0452,
    )
    cyy = (
        -0.0167 * t - 0.2608,
        -0.0950 * t + 0.0092,
        -0.0079 * t + 0.2102,
        -0.0441 * t - 1.6537,
        -0.0109 * t + 0.0529,
    )
    chi = (4.0 / 9.0 - t / 120.0) * (math.pi - 2 * theta_s)
    yz = (4.0453 * t - 4.9710) * math.tan(chi) - 0.2155 * t + 2.4192
    th = theta_s
    xz = (
        t * t * (0.00166 * th**3 - 0.00375 * th**2 + 0.00209 * th)
        + t * (-0.02903 * th**3 + 0.06377 * th**2 - 0.03202 * th + 0.00394)
        + (0.11693 * th**3 - 0.21196 * th**2 + 0.06052 * th + 0.25886)
    )
    yyz = (
        t * t * (0.00275 * th**3 - 0.00610 * th**2 + 0.00317 * th)
        + t * (-0.04214 * th**3 + 0.08970 * th**2 - 0.04153 * th + 0.00516)
        + (0.15346 * th**3 - 0.26756 * th**2 + 0.06670 * th + 0.26688)
    )
    d = np.asarray(dirs, dtype=float)
    up = np.clip(d[..., 1], 0.0, 1.0)  # below the horizon: horizon value
    theta = np.arccos(up)
    sun = np.array([0.0, math.cos(th), -math.sin(th)])
    gamma = np.arccos(np.clip(d @ sun, -1.0, 1.0))
    big_y = yz * _perez(theta, gamma, cy) / _perez(np.array(0.0), np.array(th), cy)
    x = xz * _perez(theta, gamma, cx) / _perez(np.array(0.0), np.array(th), cx)
    y = yyz * _perez(theta, gamma, cyy) / _perez(np.array(0.0), np.array(th), cyy)
    xyz = np.stack([x / y * big_y, big_y, (1 - x - y) / y * big_y], axis=-1)
    return np.asarray(np.clip(xyz @ _XYZ_TO_RGB.T, 0.0, None))


def sky_equirect(
    sun_el_deg: float,
    sun_az_deg: float,
    width: int = SKY_WIDTH,
    turbidity: float = DEFAULT_TURBIDITY,
) -> np.ndarray:
    """Latitude-longitude sky image (height, width, 3), row 0 at the zenith.

    Columns run in longitude phi from -180 to 180 degrees, the compass azimuth each column
    shows (0 north, 90 east; the image centre faces north). Normalised so the zenith is 1.
    """
    height = width // 2
    phi = (np.arange(width) + 0.5) / width * 2 * math.pi - math.pi
    lat = math.pi / 2 - (np.arange(height) + 0.5) / height * math.pi
    # Azimuth relative to the sun, so the sun's column maps to sky_radiance's sun on -z.
    lat_g, phi_g = np.meshgrid(lat, phi - math.radians(sun_az_deg), indexing="ij")
    dirs = np.stack(
        [np.cos(lat_g) * np.sin(phi_g), np.sin(lat_g), -np.cos(lat_g) * np.cos(phi_g)], axis=-1
    )
    rgb = sky_radiance(dirs, sun_el_deg, turbidity)
    # White balance: Preetham's chromaticities drift violet near the horizon (red above green),
    # which reads as a lavender band. One gain per channel, as a camera's white balance would
    # apply, makes the mean horizon a pale blue; relative radiances within the sky are unchanged.
    horizon = rgb[int(height * 0.47) : int(height * 0.5)].reshape(-1, 3).mean(axis=0)
    gains = np.asarray(HORIZON_WHITE) / np.maximum(horizon / max(float(horizon[2]), 1e-6), 1e-6)
    rgb = rgb * gains
    zenith = sky_radiance(np.array([0.0, 1.0, 0.0]), sun_el_deg, turbidity) * gains
    return np.asarray(rgb / max(float(zenith.mean()), 1e-6), dtype=np.float32)


def write_hdr(path: str, rgb: np.ndarray) -> None:
    """Writes a float RGB image as an uncompressed Radiance RGBE (.hdr) file."""
    img = np.asarray(rgb, dtype=np.float64)
    h, w, _ = img.shape
    m = img.max(axis=-1)
    e = np.where(m > 1e-32, np.floor(np.log2(np.maximum(m, 1e-32))) + 1, -128)
    scale = np.where(m > 1e-32, 256.0 / np.power(2.0, e), 0.0)
    rgbe = np.zeros((h, w, 4), dtype=np.uint8)
    rgbe[..., :3] = np.clip(img * scale[..., None], 0, 255).astype(np.uint8)
    rgbe[..., 3] = np.clip(e + 128, 0, 255).astype(np.uint8)
    header = f"#?RADIANCE\nFORMAT=32-bit_rle_rgbe\n\n-Y {h} +X {w}\n".encode()
    with open(path, "wb") as f:
        f.write(header + rgbe.tobytes())


def read_hdr_size(path: str) -> tuple[int, int]:
    """(height, width) from a Radiance header; used by tests."""
    with open(path, "rb") as f:
        for line in f:
            if line.startswith(b"-Y"):
                parts = line.split()
                return int(parts[1]), int(parts[3])
    raise ValueError("no resolution line")


# --- Kit / USD -----------------------------------------------------------------------------


def apply_scene_look(
    stage: Any,
    settings: Any,
    origin: tuple[float, float] | None,
    start_epoch_s: float | None,
    cache_dir: str,
    log: Any,
    solar_hour: float = DEFAULT_SOLAR_HOUR,
    turbidity: float = DEFAULT_TURBIDITY,
    sun_intensity: float = DEFAULT_SUN_INTENSITY,
    sky_intensity: float = DEFAULT_SKY_INTENSITY,
    f_number: float = DEFAULT_F_NUMBER,
) -> tuple[float, float]:
    """Places the sun, writes and binds the sky, and sets the water surface and tone mapping.

    Without an ``origin`` (no georeference yet) the sun is NEUTRAL_SUN, so the scene has the
    look from startup; it is re-applied with the real sun once the simulator's metadata
    arrives. Returns the sun's (elevation, azimuth) in degrees.
    """
    from pxr import Gf, Sdf, UsdGeom, UsdLux, UsdShade

    if origin is None:
        sun_el, sun_az = NEUTRAL_SUN
        log(
            f"Scene look: neutral sun (elevation {sun_el:.0f}, azimuth {sun_az:.0f}) until a "
            "georeference arrives"
        )
    else:
        when = (
            solar_time_utc(start_epoch_s, origin[1], solar_hour)
            if start_epoch_s is not None
            else datetime.now(timezone.utc)
        )
        sun_el, sun_az = sun_position(origin[0], origin[1], when)
        log(
            f"Scene look: sun at {when:%Y-%m-%d %H:%M} UTC (solar {solar_hour:.1f} h): "
            f"elevation {sun_el:.1f} deg, azimuth {sun_az:.1f} deg"
        )
    sun_el_lit = max(sun_el, 2.0)  # keep a usable light if the chosen time is at night

    sun = stage.GetPrimAtPath(SUN_PATH)
    if sun and sun.IsValid():
        xf = UsdGeom.Xformable(sun)
        xf.ClearXformOpOrder()
        xf.AddRotateXYZOp().Set(Gf.Vec3f(*sun_rotate_xyz(sun_el_lit, sun_az)))
        light = UsdLux.DistantLight(sun)
        light.CreateAngleAttr().Set(0.53)  # the sun's true angular diameter
        light.CreateColorAttr().Set(Gf.Vec3f(1.0, 0.96, 0.90))
        light.CreateIntensityAttr().Set(sun_intensity)
    for name in ("KeyLight", "SkyFill"):
        prim = stage.GetPrimAtPath(f"/World/{name}")
        if prim and prim.IsValid():
            prim.SetActive(False)

    def look_setting(name: str, default: Any) -> Any:
        value = settings.get(f"{LOOK_SETTINGS}/{name}")
        return default if value is None else value

    yaw = float(look_setting("domeYawDeg", DOME_YAW_DEG))
    tilt = float(look_setting("domeTiltXDeg", DOME_TILT_X_DEG))
    flip_v = bool(look_setting("domeFlipV", DOME_FLIP_V))

    os.makedirs(cache_dir, exist_ok=True)
    sky_path = os.path.join(
        cache_dir,
        f"sky_v{SKY_MODEL_VERSION}_el{sun_el_lit:.1f}_az{sun_az:.1f}_t{turbidity:.1f}"
        f"_f{int(flip_v)}.hdr",
    )
    if not os.path.exists(sky_path):
        img = sky_equirect(sun_el_lit, sun_az, turbidity=turbidity)
        write_hdr(sky_path, img[::-1] if flip_v else img)
    dome = stage.GetPrimAtPath(DOME_PATH)
    if dome and dome.IsValid():
        dome_light = UsdLux.DomeLight(dome)
        dome_light.CreateTextureFileAttr().Set(Sdf.AssetPath(sky_path.replace("\\", "/")))
        dome_light.CreateTextureFormatAttr().Set(UsdLux.Tokens.latlong)
        dome_light.CreateColorAttr().Set(Gf.Vec3f(1.0, 1.0, 1.0))
        dome_light.CreateIntensityAttr().Set(sky_intensity)
        # Lines the sky's glow up with the sun light (see DOME_YAW_DEG).
        dome_xf = UsdGeom.Xformable(dome)
        dome_xf.ClearXformOpOrder()
        dome_xf.AddRotateYOp().Set(yaw)  # applied after the tilt: yaw about the stage's up
        if tilt:
            dome_xf.AddRotateXOp().Set(tilt)
    log(f"Scene look: sky {sky_path}")

    water = stage.GetPrimAtPath(WATER_PRIM)
    if water and water.IsValid():
        material = UsdShade.Material.Define(stage, WATER_MATERIAL)
        shader = UsdShade.Shader.Define(stage, f"{WATER_MATERIAL}/Shader")
        shader.CreateImplementationSourceAttr(UsdShade.Tokens.sourceAsset)
        shader.SetSourceAsset(Sdf.AssetPath("OmniGlass.mdl"), "mdl")
        shader.SetSourceAssetSubIdentifier("OmniGlass", "mdl")
        shader.CreateInput("glass_ior", Sdf.ValueTypeNames.Float).Set(WATER_IOR)
        shader.CreateInput("thin_walled", Sdf.ValueTypeNames.Bool).Set(True)
        shader.CreateInput("glass_color", Sdf.ValueTypeNames.Color3f).Set(
            Gf.Vec3f(0.80, 0.93, 0.95)
        )
        shader.CreateInput("frosting_roughness", Sdf.ValueTypeNames.Float).Set(0.02)
        shader.CreateInput("reflection_color", Sdf.ValueTypeNames.Color3f).Set(
            Gf.Vec3f(1.0, 1.0, 1.0)
        )
        out = shader.CreateOutput("out", Sdf.ValueTypeNames.Token)
        material.CreateSurfaceOutput("mdl").ConnectToSource(out)
        material.CreateVolumeOutput("mdl").ConnectToSource(out)
        UsdShade.MaterialBindingAPI.Apply(water).Bind(material)

    # Filmic tone mapping at a fixed exposure, so the image does not drift as the camera moves.
    settings.set("/rtx/post/tonemap/op", 6)  # ACES
    settings.set("/rtx/post/tonemap/fNumber", f_number)
    hold_fixed_exposure(settings)
    return sun_el, sun_az


AUTO_EXPOSURE = "/rtx/post/tonemap/autoExposure/enabled"


def hold_fixed_exposure(settings: Any) -> None:
    """Keeps auto-exposure off; the app's startup code turns it back on after a stage opens."""
    if settings.get(AUTO_EXPOSURE):
        settings.set(AUTO_EXPOSURE, False)
    if settings.get("/rtx/post/histogram/enabled"):
        settings.set("/rtx/post/histogram/enabled", False)


def set_water_reflection(stage: Any, on: bool) -> None:
    """Turns the water surface's reflection on (above water) or off (below it).

    From below, the surface mirrors the scene outside Snell's window (total internal
    reflection). In real water that reflected light has crossed hundreds of metres of water
    and is absorbed to the deep-water colour, but the renderer's fog only acts on direct
    view distance, so the mirrored seafloor would show at full brightness. Without the
    reflection the surface shows the sky overhead, fading into the fog toward the horizon.
    """
    from pxr import Gf, UsdShade

    prim = stage.GetPrimAtPath(f"{WATER_MATERIAL}/Shader")
    if prim and prim.IsValid():
        value = Gf.Vec3f(1.0, 1.0, 1.0) if on else Gf.Vec3f(0.0, 0.0, 0.0)
        UsdShade.Shader(prim).GetInput("reflection_color").Set(value)


class UnderwaterFog:
    """Turns distance fog on in the deep-water colour while the camera is below the surface.

    ``on_change(under)`` runs on each crossing, for effects tied to it (the surface reflection).

    Deeper than ``DEEP_WATER_M`` the camera is past any view of the surface, and
    ``on_deep(deep)`` runs (the extension hides the water volume, whose inner faces and the sun
    seen through them would otherwise show as a horizon line and a sun disc kilometres down);
    the background is then the deep-water colour instead of the sky.
    """

    def __init__(
        self,
        settings: Any,
        visibility_m: float = DEFAULT_VISIBILITY_M,
        on_change: Any = None,
        on_deep: Any = None,
    ) -> None:
        self._settings = settings
        self.visibility_m = visibility_m
        self._on_change = on_change
        self._on_deep = on_deep
        self._under: bool | None = None
        self._deep: bool | None = None

    def reset(self) -> None:
        """Forgets the last state, so the next update re-applies (after the look is re-applied)."""
        self._under = None
        self._deep = None

    def update(self, camera_y_cm: float) -> None:
        deep = camera_y_cm < -DEEP_WATER_M * SCENE_SCALE
        if deep != self._deep:
            self._deep = deep
            if self._on_deep is not None:
                self._on_deep(deep)
            self._settings.set("/rtx/background/source/color", list(WATER_RGB))
            self._settings.set("/rtx/background/source/type", 1 if deep else 0)  # 1: colour
        under = camera_y_cm < 0.0
        if under == self._under:
            return
        self._under = under
        if self._on_change is not None:
            self._on_change(under)
        self._settings.set("/rtx/fog/enabled", under)
        if under:
            self._settings.set("/rtx/fog/fogColor", list(WATER_RGB))
            self._settings.set("/rtx/fog/fogStartDist", 0.0)
            self._settings.set("/rtx/fog/fogEndDist", self.visibility_m * SCENE_SCALE)
