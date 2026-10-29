# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Agent camera and capture routes on the omni.services HTTP server.

Lets an agent (or any local HTTP client) frame shots without driving the
desktop window. Routes are served under /agent on the app's services port
(8011 by default). The app .kit file binds that server to 127.0.0.1.

  GET  /agent/status                 active animal, follow mode, camera
                                     (scene routes return 503 until the stage is loaded)
  GET  /agent/animals                streamed entities (eid, species, prim path)
  POST /agent/animal  {eid}          make an entity the active animal
  POST /agent/follow  {enabled}      toggle 3rd-person follow mode
  GET  /agent/view                   active camera eye and forward vector
  POST /agent/view    {eye, target}  place the active camera (world coordinates)
  POST /agent/frame   {path?, offset?}  look at a prim (default: active animal)
  GET  /agent/bounds?path=...        world bounding box of a prim
  POST /agent/capture {name}         write viewport PNG to the capture folder
  GET  /agent/prims?root=/World      list prim paths (depth-limited)
"""

from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING, Any

import carb
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
        return {
            "active_eid": ext._active_eid,
            "active_path": active_path(),
            "follow_mode": ext._follow_mode_enabled,
            "entities": len(ext._entities_state),
            "view": _view(),
        }

    @router.get("/agent/status")
    async def status() -> dict[str, Any]:
        return status_payload()

    @router.get("/agent/animals")
    async def animals() -> dict[str, Any]:
        return {
            "animals": [
                {"eid": eid, "species": s.get("sp"), "path": s.get("path")}
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
        cap = capture_viewport_to_file(get_active_viewport(), path)
        await cap.wait_for_result()
        # The PNG is written asynchronously after the capture result resolves
        for _ in range(100):
            if os.path.exists(path) and os.path.getsize(path) > 0:
                await asyncio.sleep(0.2)
                return {"path": path, "bytes": os.path.getsize(path)}
            await asyncio.sleep(0.1)
        return {"path": path, "error": "timed out waiting for file"}

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
