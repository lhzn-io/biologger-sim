# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""How a pseudo track was made: an ordered list of steps, and the numbers it is judged by.

The outer shape is fixed so every reader (the hub, the viewer, a review) can rely on it; what
goes inside a step is open, so a new track algorithm needs no format change.

A **step** is ``{"step", "method", "version", "status", "params"}``:

- ``step`` is the stage of the pipeline (``dead_reckoning``, ``current_correction``,
  ``placement``; later ones, such as a bathymetry constraint or a smoother, are new names);
- ``method`` is the algorithm used for it (``fix_pinned``, ``forcingkit``);
- ``version`` is :data:`METHOD_VERSIONS` for that method. Bump it whenever a method's output
  changes for the same inputs, so two tracks that name the same method are known to mean the
  same computation;
- ``status`` is ``applied`` or ``failed`` (a failed step left the track as it was);
- ``params`` is free-form JSON: whatever that method needs to be understood and compared.

A **metric** is ``{"name", "value", "unit", "by"}``, where ``by`` names what computed it
(``export-track`` here; the hub adds seafloor metrics). Readers pick metrics by name.
"""

from __future__ import annotations

import math
from typing import Any

STEP_KEYS = ("step", "method", "version", "status", "params")
METRIC_KEYS = ("name", "value", "unit", "by")
STATUSES = ("applied", "failed")

# Per method; bump when its output changes for the same inputs.
METHOD_VERSIONS: dict[str, int] = {
    # dead_reckoning
    "odba_scaled": 1,
    "constant": 1,
    # current_correction
    "forcingkit": 1,
    "ocean_store": 1,
    # placement
    "dead_reckoning": 1,
    "fix_interpolation": 1,
    "fix_pinned": 1,
}


def step(name: str, method: str, params: dict[str, Any], status: str = "applied") -> dict[str, Any]:
    """One pipeline step; ``method`` must have a version in :data:`METHOD_VERSIONS`."""
    if status not in STATUSES:
        raise ValueError(f"step status must be one of {STATUSES}, not {status!r}")
    return {
        "step": name,
        "method": method,
        "version": METHOD_VERSIONS[method],
        "status": status,
        "params": params,
    }


def metric(name: str, value: float | None, unit: str, by: str = "export-track") -> dict[str, Any]:
    """One metric; a non-finite value is written as None."""
    if value is not None and not math.isfinite(value):
        value = None
    return {"name": name, "value": value, "unit": unit, "by": by}


def validate(pipeline: list[dict[str, Any]], metrics: list[dict[str, Any]]) -> None:
    """Checks the fixed outer shape; raises ValueError naming the first problem."""
    for i, s in enumerate(pipeline):
        missing = [k for k in STEP_KEYS if k not in s]
        if missing:
            raise ValueError(f"pipeline[{i}] lacks {missing}")
        if not isinstance(s["params"], dict) or not isinstance(s["version"], int):
            raise ValueError(f"pipeline[{i}]: params must be an object, version an integer")
        if s["status"] not in STATUSES:
            raise ValueError(f"pipeline[{i}]: status {s['status']!r} not in {STATUSES}")
    for i, m in enumerate(metrics):
        missing = [k for k in METRIC_KEYS if k not in m]
        if missing:
            raise ValueError(f"metrics[{i}] lacks {missing}")


def find_step(pipeline: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    """The last step called ``name``, or None."""
    return next((s for s in reversed(pipeline) if s.get("step") == name), None)
