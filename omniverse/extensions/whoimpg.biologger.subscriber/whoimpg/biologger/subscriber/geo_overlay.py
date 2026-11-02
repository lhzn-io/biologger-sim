# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Positional-uncertainty overlay: the reachable region (space-time prism lens) per entity.

The simulator publishes the region at the current playback time as a convex polygon of
(north, east) metres from the origin (``prism`` in the ``<topic>/meta`` message). It is drawn
as an orange band along the region's edge just above the sea surface, one mesh per entity
under ``/World/Uncertainty``; an outline leaves the animal and the seafloor inside visible,
where a filled disk hid them (RTX real-time ignored OmniPBR's fractional opacity at runtime).
Array building is plain NumPy; USD is touched only in ``write_prism_mesh``.
"""

from __future__ import annotations

import re
from typing import Any

import numpy as np

SCENE_SCALE = 100.0  # metres -> scene centimetres
SURFACE_OFFSET_CM = 30.0  # above the sea surface (y = 0) to avoid z-fighting
BAND_FRACTION = 0.03  # band width as a share of the region's mean radius
BAND_MIN_M = 40.0
BAND_MAX_M = 400.0
# Low albedo: the scene's sun is strong, and a bright orange clips to cream under it.
BAND_RGB = (0.25, 0.08, 0.0)
ROOT = "/World/Uncertainty"


def band_width_m(radii_m: np.ndarray) -> float:
    """Band width for a region with these vertex radii: a few percent of its size, clamped."""
    width = float(np.clip(BAND_FRACTION * float(np.mean(radii_m)), BAND_MIN_M, BAND_MAX_M))
    return min(width, 0.5 * float(np.min(radii_m)))


def prism_band_arrays(
    polygon_ne: list[list[float]] | list[tuple[float, float]],
    y_cm: float = SURFACE_OFFSET_CM,
    scale: float = SCENE_SCALE,
) -> tuple[np.ndarray, np.ndarray, np.ndarray] | None:
    """Points, face counts and indices for a band inside a convex polygon's edge, or None.

    Points are the outer ring (the polygon) then the inner ring, each inner vertex moved
    toward the centroid by the band width; one quad joins each edge to its inner copy.
    """
    poly = np.asarray(polygon_ne, dtype=np.float64).reshape(-1, 2)
    if len(poly) < 3:
        return None
    centre = poly.mean(axis=0)
    offset = poly - centre
    radii = np.hypot(offset[:, 0], offset[:, 1])
    if float(radii.min()) <= 0.0:
        return None
    inner = poly - offset / radii[:, None] * band_width_m(radii)
    ne = np.vstack([poly, inner])
    points = np.stack(
        [ne[:, 1] * scale, np.full(len(ne), y_cm), -ne[:, 0] * scale], axis=-1
    ).astype(np.float32)
    m = len(poly)
    i = np.arange(m)
    j = (i + 1) % m
    quads = np.stack([i, j, m + j, m + i], axis=-1)
    counts = np.full(m, 4, dtype=np.int32)
    return points, counts, quads.astype(np.int32).ravel()


def prim_path(sim_id: str) -> str:
    return f"{ROOT}/{re.sub(r'[^A-Za-z0-9_]', '_', sim_id) or 'entity'}"


def write_prism_mesh(stage: Any, sim_id: str, polygon_ne: list[list[float]], visible: bool) -> None:
    """Creates or updates the overlay mesh for one entity; hides it when there is no region."""
    from pxr import Gf, Sdf, UsdGeom, UsdShade, Vt

    path = prim_path(sim_id)
    arrays = prism_band_arrays(polygon_ne) if visible else None
    prim = stage.GetPrimAtPath(path)
    if arrays is None:
        if prim and prim.IsValid():
            UsdGeom.Imageable(prim).MakeInvisible()
        return

    points, counts, indices = arrays
    UsdGeom.Xform.Define(stage, ROOT)  # an Xform so vertical exaggeration can scale it
    mesh = UsdGeom.Mesh.Define(stage, path)
    mesh.GetPointsAttr().Set(Vt.Vec3fArray.FromNumpy(points))
    mesh.GetFaceVertexCountsAttr().Set(Vt.IntArray.FromNumpy(counts))
    mesh.GetFaceVertexIndicesAttr().Set(Vt.IntArray.FromNumpy(indices))
    mesh.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
    mesh.CreateDoubleSidedAttr(True)
    lo, hi = points.min(axis=0), points.max(axis=0)
    mesh.GetExtentAttr().Set([Gf.Vec3f(*(float(v) for v in lo)), Gf.Vec3f(*(float(v) for v in hi))])
    UsdGeom.Imageable(mesh.GetPrim()).MakeVisible()
    # Without this the band's shadows draw extra rings on the seafloor (one per scene light).
    UsdGeom.PrimvarsAPI(mesh.GetPrim()).CreatePrimvar(
        "doNotCastShadows", Sdf.ValueTypeNames.Bool
    ).Set(True)

    mat_path = f"{ROOT}/Looks/PrismBand"
    if not stage.GetPrimAtPath(mat_path).IsValid():
        material = UsdShade.Material.Define(stage, mat_path)
        shader = UsdShade.Shader.Define(stage, f"{mat_path}/PreviewSurface")
        shader.CreateIdAttr("UsdPreviewSurface")
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*BAND_RGB))
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.9)
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
    UsdShade.MaterialBindingAPI.Apply(mesh.GetPrim()).Bind(
        UsdShade.Material(stage.GetPrimAtPath(mat_path))
    )
