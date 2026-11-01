# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Per-entity metadata message: georeference, track model and positional uncertainty.

Published on ``<telemetry topic>/meta`` about once a second. Positions are (north, east) metres
from ``origin`` (the start fix), the same frame as ``px``/``py`` in state packets; times are Unix
seconds (UTC). The visualizer uses ``origin`` to place the scene and DEM, ``prefetch_bounds_ne``
to prefetch terrain, and ``prism`` to draw the reachable region at ``t``.
"""

from __future__ import annotations

from typing import Any

from .georef import GeoReference
from .track_models import prism_bounds, prism_lens
from .types import TrackModel

META_SCHEMA = "entity-meta-v1"


def build_entity_meta(
    *,
    eid: int,
    sim_id: str,
    tag_id: str | None,
    species: str,
    georef: GeoReference | None,
    track_model: TrackModel,
    v_max: float,
    t_now: float | None,
    t_last: float | None,
    heading_correction_deg: float = 0.0,
) -> dict[str, Any]:
    """Builds the metadata payload for one entity at playback time ``t_now``.

    ``heading_correction_deg`` is the rotation a fix-pinned track applied to the tag heading.
    """
    meta: dict[str, Any] = {
        "schema": META_SCHEMA,
        "eid": eid,
        "sim_id": sim_id,
        "tag_id": tag_id,
        "sp": species,
        "track_model": track_model.value,
        "heading_correction_deg": heading_correction_deg,
        "v_max_m_s": v_max,
        "t": t_now,
        "origin": None,
        "fixes": [],
        "prefetch_bounds_ne": None,
        "prism": [],
    }
    if georef is None:
        return meta

    meta["origin"] = {"lat": georef.start.lat, "lon": georef.start.lon}
    meta["fixes"] = [
        {"t": f.t, "lat": f.lat, "lon": f.lon} for f in (georef.start, georef.end) if f is not None
    ]
    if georef.end is not None or t_last is not None:
        meta["prefetch_bounds_ne"] = list(prism_bounds(georef, v_max, t_last))
    if t_now is not None:
        meta["prism"] = [[n, e] for n, e in prism_lens(t_now, georef, v_max)]
    return meta
