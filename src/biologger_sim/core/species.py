# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Per-species movement parameters used for positional uncertainty.

``MAX_SUSTAINED_SPEED_M_S`` bounds how far an animal can travel between position fixes; it sets
the size of the space-time prism. The values are working placeholders pending review with the
WHOI Marine Predators Group, and any entity can override them in its config
(``dead_reckoning.max_sustained_speed_m_s``).
"""

from __future__ import annotations

DEFAULT_MAX_SUSTAINED_SPEED_M_S = 1.5

MAX_SUSTAINED_SPEED_M_S: dict[str, float] = {
    "xiphias gladius": 1.5,  # swordfish (placeholder)
    "rhincodon typus": 1.0,  # whale shark (placeholder)
}


def max_sustained_speed(species: str | None, override: float | None = None) -> float:
    """Returns the sustained-speed bound (m/s) for a species, honouring an explicit override."""
    if override is not None and override > 0:
        return override
    if species:
        return MAX_SUSTAINED_SPEED_M_S.get(species.strip().lower(), DEFAULT_MAX_SUSTAINED_SPEED_M_S)
    return DEFAULT_MAX_SUSTAINED_SPEED_M_S
