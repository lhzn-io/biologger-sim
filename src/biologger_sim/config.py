# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import contextlib
from pathlib import Path
from typing import Any

import yaml

from .core.types import PipelineConfig


def _apply_overrides(config: dict[str, Any], overrides: dict[str, Any]) -> None:
    """
    Recursively updates the config dictionary with values from overrides.
    Handles dot-notation keys in overrides (e.g. "simulation.rate_hz").
    """
    for key, value in overrides.items():
        parts = key.split(".")
        target = config
        for part in parts[:-1]:
            target = target.setdefault(part, {})

        # Handle type conversion if possible based on existing value
        last_key = parts[-1]
        if last_key in target and target[last_key] is not None:
            # Simple type inference/conversion
            current_val = target[last_key]
            if isinstance(current_val, bool):
                if str(value).lower() in ("true", "1", "yes"):
                    value = True
                elif str(value).lower() in ("false", "0", "no"):
                    value = False
            elif isinstance(current_val, int):
                with contextlib.suppress(ValueError):
                    value = int(value)
            elif isinstance(current_val, float):
                with contextlib.suppress(ValueError):
                    value = float(value)

        target[last_key] = value


def load_config(config_path: str | Path, overrides: list[str] | None = None) -> PipelineConfig:
    """
    Load the pipeline configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.
        overrides: List of "key=value" strings to override config values.

    Returns:
        PipelineConfig: The validated configuration object.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(path) as f:
        config_data = yaml.safe_load(f)

    if overrides:
        override_dict = {}
        for item in overrides:
            if "=" not in item:
                continue
            key, value = item.split("=", 1)
            override_dict[key.strip()] = value.strip()

        _apply_overrides(config_data, override_dict)

    return PipelineConfig(**config_data)
