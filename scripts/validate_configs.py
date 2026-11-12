# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from pathlib import Path

import yaml

from biologger_sim.core.types import PipelineConfig


def validate_config(config_path: Path) -> None:
    print(f"Validating {config_path}...")
    with open(config_path) as f:
        data = yaml.safe_load(f)

    try:
        config = PipelineConfig(**data)
        print(f"✅ {config_path.name} is valid.")
        print(f"   Mode: {config.mode}")
        for entity in config.simulation.entities:
            print(f"   Entity: {entity.sim_id}")
            print(f"   AHRS Enabled: {entity.ahrs.enabled}")
            if entity.ahrs.enabled:
                print(f"   AHRS Algorithm: {entity.ahrs.algorithm}")
    except Exception as e:
        print(f"❌ {config_path.name} is INVALID.")
        print(e)


if __name__ == "__main__":
    base_path = Path("config")
    configs = [
        "Swordfish-RED001_20220812_19A0564-postfacto.yaml",
        "Swordfish-RED001_20220812_19A0564-causal.yaml",
        "Swordfish-RED001_20220812_19A0564-ahrs.yaml",
    ]

    for c in configs:
        validate_config(base_path / c)
