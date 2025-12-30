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
        print(f"   AHRS Enabled: {config.ahrs.enabled}")
        if config.ahrs.enabled:
            print(f"   AHRS Algorithm: {config.ahrs.algorithm}")
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
