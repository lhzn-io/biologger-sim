# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Agent camera and capture routes on the omni.services HTTP server.

Lets an agent (or any local HTTP client) frame shots without driving the
desktop window. Routes are served under /agent on the app's services port
(8011 by default). The app .kit file binds that server to 127.0.0.1.

  GET  /agent/status                 active animal, follow mode, camera
                                     (scene routes return 503 until the stage is loaded)
  GET  /agent/animals                streamed entities (eid, species, prim path) and samples
                                     received, with gaps, an estimate of samples missing and
                                     the samples in the trail
  POST /agent/animal  {eid}          make an entity the active animal
  POST /agent/follow  {enabled}      toggle 3rd-person follow mode
  GET  /agent/view                   active camera eye and forward vector
  POST /agent/view    {eye, target}  place the active camera (world coordinates)
  POST /agent/frame   {path?, offset?}  look at a prim (default: active animal)
  GET  /agent/bounds?path=...        world bounding box of a prim
  POST /agent/capture {name, clean?} write viewport PNG to the capture folder; clean (default
                                     true) hides the selection outline for the shot
  GET  /agent/prims?root=/World      list prim paths (depth-limited)
  GET  /agent/settings?path=/rtx/... read a carb setting or subtree
  POST /agent/settings {path, value} set one; only render (/rtx/) and look settings
  POST /agent/look                   re-apply the scene look from the current look settings
  POST /agent/trail {width_cm?, auto?}  trail width by hand (turns the adaptive width
                                     off), or {auto: true} to follow the camera distance again
  POST /agent/exaggeration {factor}  vertical exaggeration of the scene (1 to 20)
  POST /agent/showcase {on}          screen-recording layout: hide every window but the
                                     viewport and HUD, and the menus; {on: false} restores
  POST /agent/layers {uncertainty?}  show or hide the position uncertainty band (HUD box)
  POST /agent/time {seconds?, deepest?}  move the replay head (seconds from the session
                                     start), or to the active animal's deepest sample
"""

from __future__ import annotations

import asyncio
import os
from bisect import bisect_left
from typing import TYPE_CHECKING, Any

import carb
import numpy as np
import omni.kit.app
import omni.usd
from fastapi import HTTPException
from omni.kit.viewport.utility import capture_viewport_to_file, get_active_viewport
from pxr import Gf, Usd, UsdGeom
from pydantic import BaseModel

if TYPE_CHECKING:
    from .extension import CreateSetupExtension

CAPTURE_SUBDIR = os.path.join("omniverse-logs", "agent-captures")
DEFAULT_FRAME_OFFSET = (-900.0, 250.0, 700.0)


class ViewArg(BaseModel):
    eye: list[float]
    target: list[float]


class FrameArg(BaseModel):
    path: str | None = None
    offset: list[float] | None = None


class EidArg(BaseModel):
    eid: int


class FollowArg(BaseModel):
    enabled: bool


class CaptureArg(BaseModel):
    name: str
    clean: bool = True


class SettingArg(BaseModel):
    path: str
    value: Any


class TrailArg(BaseModel):
    width_cm: float | None = None
    auto: bool | None = None


class ExaggerationArg(BaseModel):
    factor: float


class ShowcaseArg(BaseModel):
    on: bool = True
    hud_x: float = 5.0  # HUD position in workspace units; (0, 0) is the window's top left
    hud_y: float = 5.0


class LayersArg(BaseModel):
    uncertainty: bool | None = None


class TimeArg(BaseModel):
    seconds: float | None = None
    deepest: bool = False


# Settings an agent may change: renderer and look tuning only, nothing that touches files,
# networking or extensions.
SETTING_PREFIXES = ("/rtx/", "/exts/whoimpg.biologger.subscriber/look/")


def sample_stats(times: list[float]) -> dict[str, Any]:
    """Received samples, gaps (intervals over 1.5 times the median) and samples missing in them.

    The record interval is the median, so dropped messages show as gaps without knowing the
    tag's sampling rate.
    """
    if len(times) < 3:
        return {"samples": len(times), "gaps": 0, "missing_est": 0}
    dt = np.diff(np.asarray(times, dtype=float))
    step = float(np.median(dt))
    long = dt[dt > 1.5 * step] if step > 0 else dt[:0]
    return {
        "samples": len(times),
        "gaps": int(long.size),
        "missing_est": int(np.round(long / step - 1.0).sum()) if long.size else 0,
        "interval_s": step,
    }


def trail_samples(trail_state: dict[str, Any] | None) -> int:
    """Distinct samples in an animal's trail: baked segments plus the active one.

    Each segment after the first starts with the previous segment's last sample.
    """
    if not trail_state:
        return 0
    baked = trail_state.get("baked", {})
    total = len(trail_state.get("buffer", [])) + sum(len(b) for b in baked.values())
    return max(0, total - len(baked))


def _stage() -> Usd.Stage:
    stage = omni.usd.get_context().get_stage()
    if stage is None or get_active_viewport() is None:
        # Polled during startup before the scene and viewport exist
        raise HTTPException(status_code=503, detail="stage not ready")
    return stage


def _camera() -> Usd.Prim:
    return _stage().GetPrimAtPath(str(get_active_viewport().camera_path))


def _up() -> Gf.Vec3d:
    return Gf.Vec3d(0, 0, 1) if UsdGeom.GetStageUpAxis(_stage()) == "Z" else Gf.Vec3d(0, 1, 0)


def _world_bounds(path: str) -> Gf.Range3d:
    cache = UsdGeom.BBoxCache(
        Usd.TimeCode.Default(), [UsdGeom.Tokens.default_, UsdGeom.Tokens.render]
    )
    return cache.ComputeWorldBound(_stage().GetPrimAtPath(path)).ComputeAlignedRange()


def _view() -> dict[str, Any]:
    cam = _camera()
    m = UsdGeom.Xformable(cam).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    return {
        "camera": str(cam.GetPath()),
        "eye": list(m.ExtractTranslation()),
        "forward": list(m.TransformDir(Gf.Vec3d(0, 0, -1)).GetNormalized()),
        "up_axis": UsdGeom.GetStageUpAxis(_stage()),
    }


def _place_camera(eye: Gf.Vec3d, target: Gf.Vec3d) -> dict[str, Any]:
    cam = _camera()
    world = Gf.Matrix4d().SetLookAt(eye, target, _up()).GetInverse()
    parent = UsdGeom.Xformable(cam.GetParent()).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    xf = UsdGeom.Xformable(cam)
    xf.ClearXformOpOrder()
    xf.AddTransformOp().Set(world * parent.GetInverse())
    return _view()


def register(ext: CreateSetupExtension) -> Any:
    """Register the /agent routes.

    Returns the router for deregister(), or None if omni.services is not loaded.
    """
    try:
        from omni.services.core import main, routers
    except ImportError:
        carb.log_warn("[whoimpg.biologger] omni.services.core not loaded; agent routes disabled")
        return None

    from .extension import REPO_ROOT

    capture_dir = str(REPO_ROOT / CAPTURE_SUBDIR)
    router = routers.ServiceAPIRouter()

    def active_path() -> str | None:
        state = ext._entities_state.get(ext._active_eid)
        return state.get("path") if state else None

    def status_payload() -> dict[str, Any]:
        # Slowest frame-update sections (ms) since the last status read, then reset
        frame_ms = {k: round(v, 1) for k, v in ext._frame_ms_max.items()}
        ext._frame_ms_max.clear()
        return {
            "frame_ms_max": frame_ms,
            "active_eid": ext._active_eid,
            "active_path": active_path(),
            "follow_mode": ext._follow_mode_enabled,
            "entities": len(ext._entities_state),
            "view": _view(),
            "trail_update_ms": round(ext._last_trail_update_ms, 1),  # last frame's trail work
        }

    @router.get("/agent/status")
    async def status() -> dict[str, Any]:
        return status_payload()

    @router.get("/agent/animals")
    async def animals() -> dict[str, Any]:
        return {
            "animals": [
                {
                    "eid": eid,
                    "species": s.get("sp"),
                    "path": s.get("path"),
                    **sample_stats(ext._entity_history.get(eid, {}).get("times", [])),
                    "trail_samples": trail_samples(ext._entities_trail_buffers.get(eid)),
                }
                for eid, s in sorted(ext._entities_state.items())
            ]
        }

    @router.post("/agent/animal")
    async def set_animal(a: EidArg) -> dict[str, Any]:
        eids = sorted(ext._entities_state.keys())
        if a.eid not in eids:
            return {"error": f"unknown eid {a.eid}", "eids": eids}
        ext._cycle_active_animal(0, index=eids.index(a.eid))
        return status_payload()

    @router.post("/agent/follow")
    async def set_follow(f: FollowArg) -> dict[str, Any]:
        # Goes through the HUD checkbox so the extension's own handler runs
        ext._follow_mode_checkbox.model.set_value(f.enabled)
        return status_payload()

    @router.get("/agent/view")
    async def get_view() -> dict[str, Any]:
        return _view()

    @router.post("/agent/view")
    async def set_view(v: ViewArg) -> dict[str, Any]:
        return _place_camera(Gf.Vec3d(*v.eye), Gf.Vec3d(*v.target))

    @router.post("/agent/frame")
    async def frame(f: FrameArg) -> dict[str, Any]:
        path = f.path or active_path()
        if not path:
            return {"error": "no path given and no active animal"}
        center = _world_bounds(path).GetMidpoint()
        offset = Gf.Vec3d(*(f.offset or DEFAULT_FRAME_OFFSET))
        return _place_camera(center + offset, center)

    @router.get("/agent/bounds")
    async def bounds(path: str) -> dict[str, Any]:
        box = _world_bounds(path)
        return {
            "min": list(box.GetMin()),
            "max": list(box.GetMax()),
            "center": list(box.GetMidpoint()),
        }

    @router.post("/agent/capture")
    async def capture(c: CaptureArg) -> dict[str, Any]:
        # Only a bare PNG name: callers must not choose where files are written
        name = os.path.basename(c.name)
        if name != c.name or not name.lower().endswith(".png"):
            return {"error": "name must be a bare *.png filename"}
        os.makedirs(capture_dir, exist_ok=True)
        path = os.path.join(capture_dir, name)
        if os.path.exists(path):
            os.remove(path)
        # Selecting an animal (cycling, follow mode) draws an outline and bounding box on it;
        # a clean shot clears the selection for the capture and restores it after
        selection = omni.usd.get_context().get_selection()
        selected = list(selection.get_selected_prim_paths()) if c.clean else []
        if selected:
            selection.clear_selected_prim_paths()
            # The outline is drawn a few frames behind the selection
            for _ in range(10):
                await omni.kit.app.get_app().next_update_async()
        try:
            cap = capture_viewport_to_file(get_active_viewport(), path)
            await cap.wait_for_result()
            # The PNG is written asynchronously after the capture result resolves
            for _ in range(100):
                if os.path.exists(path) and os.path.getsize(path) > 0:
                    await asyncio.sleep(0.2)
                    return {"path": path, "bytes": os.path.getsize(path)}
                await asyncio.sleep(0.1)
            return {"path": path, "error": "timed out waiting for file"}
        finally:
            if selected:
                selection.set_selected_prim_paths(selected, False)

    @router.get("/agent/prims")
    async def prims(root: str = "/World", depth: int = 3) -> dict[str, Any]:
        base = _stage().GetPrimAtPath(root)
        base_depth = len(base.GetPath().pathString.split("/"))
        out = [
            f"{p.GetPath()} [{p.GetTypeName()}]"
            for p in Usd.PrimRange(base)
            if len(p.GetPath().pathString.split("/")) - base_depth <= depth
        ]
        return {"prims": out[:500]}

    @router.get("/agent/settings")
    async def get_setting(path: str) -> dict[str, Any]:
        return {"path": path, "value": carb.settings.get_settings().get(path)}

    @router.post("/agent/settings")
    async def set_setting(s: SettingArg) -> dict[str, Any]:
        if not s.path.startswith(SETTING_PREFIXES) or ".." in s.path:
            return {"error": f"only settings under {', '.join(SETTING_PREFIXES)}"}
        settings = carb.settings.get_settings()
        settings.set(s.path, s.value)
        return {"path": s.path, "value": settings.get(s.path)}

    @router.post("/agent/look")
    async def reapply_look() -> dict[str, Any]:
        _stage()
        ext.apply_scene_look()
        return {"applied": True, "note": "DEM hillshade keeps the sun it was built with"}

    @router.post("/agent/trail")
    async def trail(t: TrailArg) -> dict[str, Any]:
        _stage()
        if t.width_cm is not None:
            if not 0.1 <= t.width_cm <= 10000.0:
                return {"error": "width_cm must be between 0.1 and 10000"}
            ext.set_trail_width(t.width_cm)
        if t.auto is not None:
            ext.set_trail_width_auto(t.auto)
        return {"width_cm": ext._trail_width_cm, "auto": ext._trail_width_auto}

    @router.post("/agent/exaggeration")
    async def exaggeration(e: ExaggerationArg) -> dict[str, Any]:
        if not 1.0 <= e.factor <= 20.0:
            return {"error": "factor must be between 1 and 20"}
        _stage()
        return {"factor": ext.set_vertical_exaggeration(e.factor)}

    hidden_windows: list[str] = []

    @router.post("/agent/showcase")
    async def showcase(sc: ShowcaseArg) -> dict[str, Any]:
        """Screen-recording layout: only the viewport and the HUD, no panels or menus."""
        import omni.ui as ui

        keep = {"Viewport", "Biologger HUD"}
        changed: list[str] = []
        if sc.on:
            for w in ui.Workspace.get_windows():
                title = getattr(w, "title", "")
                if title and title not in keep and getattr(w, "visible", False):
                    w.visible = False
                    hidden_windows.append(title)
                    changed.append(title)
        else:
            for title in hidden_windows:
                w = ui.Workspace.get_window(title)
                if w is not None:
                    w.visible = True
                    changed.append(title)
            hidden_windows.clear()
        # Main menu bar, the viewport's toolbars, its stats overlay (FPS, memory) and axis gizmo
        try:
            import omni.kit.mainwindow

            omni.kit.mainwindow.get_main_window().get_main_menu_bar().visible = not sc.on
        except Exception as e:
            carb.log_warn(f"[whoimpg.biologger] Main menu bar: {e}")
        try:
            from omni.kit.viewport.menubar.core import get_instance as menubars

            for menubar in menubars().get_menubars():
                menubar.visible = not sc.on
        except Exception as e:
            carb.log_warn(f"[whoimpg.biologger] Viewport toolbars: {e}")
        vp_id = get_active_viewport().id
        settings = carb.settings.get_settings()
        # hud/metrics/assembler: the stage-units label ("cm") in the lower left corner
        for key in ("hud/visible", "guide/axis/visible", "hud/metrics/assembler/visible"):
            settings.set(f"/persistent/app/viewport/{vp_id}/{key}", not sc.on)
            settings.set(f"/app/viewport/{vp_id}/{key}", not sc.on)
        # The HUD sits in the top left corner, over the viewport (the extension re-places it
        # every frame, so the pin goes through it); off, it returns to its usual place
        hud = ui.Workspace.get_window("Biologger HUD")
        if sc.on:
            if hud is not None:
                hud.visible = True
            ext._hud_pin = (sc.hud_x, sc.hud_y)
        else:
            ext._hud_pin = None
        return {"showcase": sc.on, "windows": changed, "hud_pin": ext._hud_pin}

    @router.post("/agent/layers")
    async def layers(lay: LayersArg) -> dict[str, Any]:
        # Same switch as the HUD box; the geo layers read it within a second
        box = getattr(ext, "_uncertainty_checkbox", None)
        if box is None:
            raise HTTPException(status_code=503, detail="HUD not ready")
        if lay.uncertainty is not None:
            box.model.set_value(lay.uncertainty)
        return {"uncertainty": box.model.get_value_as_bool()}

    @router.post("/agent/time")
    async def replay_time(t: TimeArg) -> dict[str, Any]:
        _stage()
        hist = ext._entity_history.get(ext._active_eid)
        if not hist or not hist["times"]:
            return {"error": "no history for the active animal"}
        if t.deepest:
            i = int(np.argmax(np.fromiter((p[2] for p in hist["pos"]), dtype=float)))
            seconds = hist["times"][i] - ext._session_start_time
        elif t.seconds is not None:
            seconds = t.seconds
        else:
            return {"error": "give seconds or deepest"}
        # The viewer poses every animal from its history at the new time, without moving
        # Kit's timeline (see set_replay_time)
        ext.set_replay_time(seconds)
        for _ in range(3):
            await omni.kit.app.get_app().next_update_async()
        # Times are sorted: a binary search, not a scan of every sample on the main thread
        # (a scan held Kit for a fraction of a second per call)
        i = min(bisect_left(hist["times"], ext._session_start_time + seconds), len(hist["pos"]) - 1)
        prim = _stage().GetPrimAtPath(
            ext._entities_state.get(ext._active_eid, {}).get("path") or "/"
        )
        position = (
            list(
                UsdGeom.Xformable(prim)
                .ComputeLocalToWorldTransform(Usd.TimeCode.Default())
                .ExtractTranslation()
            )
            if prim.IsValid() and not prim.IsPseudoRoot()
            else None
        )
        return {
            "seconds": seconds,
            "duration_s": hist["times"][-1] - ext._session_start_time,
            "depth_m": hist["pos"][i][2],
            "position": position,
        }

    main.register_router(router)
    carb.log_info(
        f"[whoimpg.biologger] Agent routes registered under /agent (captures: {capture_dir})"
    )
    return router


def deregister(router: Any) -> None:
    if router is None:
        return
    try:
        from omni.services.core import main

        main.deregister_router(router)
    except Exception as e:  # Shutdown must not raise
        carb.log_warn(f"[whoimpg.biologger] Failed to deregister agent routes: {e}")
