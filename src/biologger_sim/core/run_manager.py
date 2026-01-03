# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import datetime
import logging
from pathlib import Path
from typing import Any

import yaml


class RunManager:
    """
    Manages the output directory structure for a pipeline run.
    Creates a timestamped directory and provides methods to save artifacts.
    """

    def __init__(self, base_dir: Path = Path("pipeline-runs"), context: str | None = None):
        self.base_dir = base_dir
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        if context:
            self.run_id = f"{timestamp}_{context}"
        else:
            self.run_id = timestamp
        self.run_dir = self.base_dir / self.run_id
        self.logger = logging.getLogger(__name__)

    def setup(self) -> Path:
        """Creates the run directory."""
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Initialized run directory: {self.run_dir}")
        return self.run_dir

    def save_config(self, config: Any) -> None:
        """Saves the configuration to config.yaml."""
        # Handle Pydantic model or dict
        if hasattr(config, "model_dump"):
            cfg_dict = config.model_dump()
        elif hasattr(config, "dict"):
            cfg_dict = config.dict()
        else:
            cfg_dict = config

        with open(self.run_dir / "config.yaml", "w") as f:
            yaml.dump(cfg_dict, f)

    def get_output_path(self, filename: str) -> Path:
        """Returns the full path for an output file within the run directory."""
        return self.run_dir / filename
