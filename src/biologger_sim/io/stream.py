# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from collections.abc import Generator
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pyarrow.feather as feather

from ..core.types import SimulationConfig


class SensorStream:
    """
    Handles loading and streaming of biologger data.
    Simulates a real-time sensor feed from a CSV or Feather file.
    """

    def __init__(self, config: SimulationConfig, file_path: Path, data: pd.DataFrame | None = None):
        self.config = config
        self.file_path = file_path
        self.data = data
        self.metadata: dict[str, str] = {}
        if self.data is None:
            self._load_data()

    def _load_data(self) -> None:
        """Loads the data into memory."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.file_path}")

        if self.file_path.suffix == ".feather":
            self._load_feather()
        elif self.file_path.suffix == ".csv":
            # Check if a feather version exists
            feather_path = self.file_path.with_suffix(".feather")
            if feather_path.exists():
                # Use the feather file instead
                self.file_path = feather_path
                self._load_feather()
            else:
                # Auto-convert to Feather for performance
                try:
                    # Import here to avoid circular dependency if any (though unlikely)
                    from .converter import convert_csv_to_feather

                    # Only convert if file is large enough? Or always?
                    # Plan says "configure Lab to output to Feather by default (>100MB datasets)"
                    # But for input, let's just convert.
                    print(f"Auto-converting {self.file_path} to Feather for performance...")
                    feather_path = convert_csv_to_feather(self.file_path)
                    self.file_path = feather_path
                    self._load_feather()
                except Exception as e:
                    print(f"Auto-conversion failed: {e}. Falling back to CSV.")
                    self._load_csv()
        else:
            # Fallback to CSV loader for other extensions if supported, or raise error
            # For now assume CSV if not feather
            self._load_csv()

    def _load_feather(self) -> None:
        """Loads data from a Feather file with metadata."""
        table = feather.read_table(self.file_path)
        self.data = table.to_pandas()

        if self.data is None:
            raise RuntimeError("Failed to load data from Feather file")

        # Extract metadata
        if table.schema.metadata:
            self.metadata = {
                k.decode("utf-8"): v.decode("utf-8") for k, v in table.schema.metadata.items()
            }

        # Ensure DateTime is parsed if not already
        # (Feather preserves types, so likely not needed but safe)
        if "DateTimeP" in self.data.columns and not pd.api.types.is_datetime64_any_dtype(
            self.data["DateTimeP"]
        ):
            self.data["DateTimeP"] = pd.to_datetime(self.data["DateTimeP"])

        # Sort by time just in case
        if "DateTimeP" in self.data.columns:
            self.data = self.data.sort_values("DateTimeP")

    def _load_csv(self) -> None:
        """Loads the CSV data into memory."""
        # Load only necessary columns for now to save memory if file is huge
        # In a real scenario, we might use chunking for massive files
        self.data = pd.read_csv(self.file_path)

        # Ensure DateTime is parsed
        if "DateTimeP" in self.data.columns:
            self.data["DateTimeP"] = pd.to_datetime(self.data["DateTimeP"])

        # Sort by time just in case
        self.data = self.data.sort_values("DateTimeP")

    def stream(self, chunk_size: int = 100000) -> Generator[dict[str, Any], None, None]:
        """
        Yields data chunks simulating real-time arrival.

        Args:
            chunk_size: Number of samples to yield per step.
        """
        if self.data is None:
            raise RuntimeError("Data not loaded")

        num_samples = len(self.data)
        current_idx = 0

        while True:
            if current_idx >= num_samples:
                if self.config.loop:
                    current_idx = 0
                else:
                    break

            # Extract chunk
            end_idx = min(current_idx + chunk_size, num_samples)
            chunk = self.data.iloc[current_idx:end_idx]

            # Convert to dict records for easy consumption
            records = cast(list[dict[str, Any]], chunk.to_dict("records"))

            yield from records

            current_idx = end_idx
