# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from pathlib import Path

import yaml

from .core.types import PipelineConfig


def load_config(config_path: str | Path) -> PipelineConfig:
    """
    Load the pipeline configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        PipelineConfig: The validated configuration object.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(path) as f:
        config_data = yaml.safe_load(f)

    return PipelineConfig(**config_data)
