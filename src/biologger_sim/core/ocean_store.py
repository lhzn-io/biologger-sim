# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""A parent ocean read from a local store instead of a forcingkit service.

The store has forcingkit's z-v3 layout: ``u`` and ``v`` (m/s, east and north) on ``time``, ``z``
(meters, positive up), ``lat`` and ``lon``, NaN on land and below the sea floor. A regional ocean
model's output packaged as a parent ocean is one such store. The sampler hands the store to
forcingkit-client's own trajectory interpolation, so a local store and the service are sampled
the same way: linearly in time, z, lat and lon, NaN where a neighbor is dry, and the shallowest
level's value between it and the surface.

Only public-safe facts about the store are recorded with a run: its name (the ``box`` attribute,
else the folder name), the last two parts of its path, the commit and run time of the model that
wrote it. Other attributes stay in the store.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


class OceanStoreSampler:
    """Serves a local z-v3 store to ``forcingkit_client.trajectory.interpolate_trajectory``."""

    def __init__(self, path: str | Path) -> None:
        try:
            import xarray as xr
            from forcingkit_client.trajectory import (  # type: ignore[import-not-found]
                interpolate_trajectory,
            )
        except ImportError as e:
            raise ImportError(
                "a local ocean store needs forcingkit-client (Python 3.11+): "
                "pip install 'biologger-sim[currents]'"
            ) from e
        self._interpolate = interpolate_trajectory
        self.path = Path(path).expanduser()
        if not self.path.exists():
            raise FileNotFoundError(f"ocean store not found: {self.path}")
        ds = xr.open_zarr(self.path, consolidated=None)
        missing = [n for n in ("u", "v") if n not in ds.data_vars]
        missing += [d for d in ("time", "z", "lat", "lon") if d not in ds.coords]
        if missing:
            raise ValueError(f"{self.path} is not a z-v3 ocean store: no {', '.join(missing)}")
        self.provenance = store_provenance(self.path, ds.attrs)
        # forcingkit-client names the store from these four attributes (forcingkit_ocean_*).
        self.store = ds.copy(deep=False)
        self.store.attrs = {
            "forcingkit_store_id": self.provenance["path"],
            "forcingkit_store_version": self.provenance["run_time"],
            "forcingkit_donor": self.provenance["name"],
            "forcingkit_schema": str(ds.attrs.get("schema", "")),
        }

    def ocean(self, bbox: Any, start: Any, hours: Any, **options: Any) -> Any:
        """The whole store, opened lazily; the interpolation reads only the cells it needs.
        Service options (vertical spacing, padding) do not apply: the store has its own levels."""
        return self.store

    def interpolate_trajectory(
        self, lon: Any, lat: Any, time: Any, z: Any = None, **kw: Any
    ) -> Any:
        return self._interpolate(self, lon, lat, time, z, **kw)


def store_provenance(path: Path, attrs: dict[str, Any]) -> dict[str, str]:
    """Name, path tail, model commit and run time of a store, from its root attributes."""
    run_id = str(attrs.get("run_id", ""))
    run_time = re.search(r"(\d{8}-\d{6})$", run_id)
    return {
        "name": str(attrs.get("box") or path.stem),
        "path": "/".join(path.parts[-2:]),
        "model_commit": str(attrs.get("donor_commit", "")),
        "run_time": run_time.group(1) if run_time else "",
    }
