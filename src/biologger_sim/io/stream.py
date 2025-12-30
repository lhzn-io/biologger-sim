from collections.abc import Generator
from typing import Any, cast

import pandas as pd

from ..core.types import SimulationConfig


class SensorStream:
    """
    Handles loading and streaming of biologger data.
    Simulates a real-time sensor feed from a CSV file.
    """

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.file_path = config.input_file
        self.data: pd.DataFrame | None = None
        self._load_data()

    def _load_data(self) -> None:
        """Loads the CSV data into memory."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.file_path}")

        # Load only necessary columns for now to save memory if file is huge
        # In a real scenario, we might use chunking for massive files
        self.data = pd.read_csv(self.file_path)

        # Ensure DateTime is parsed
        if "DateTimeP" in self.data.columns:
            self.data["DateTimeP"] = pd.to_datetime(self.data["DateTimeP"])

        # Sort by time just in case
        self.data = self.data.sort_values("DateTimeP")

    def stream(self, chunk_size: int = 1) -> Generator[dict[str, Any], None, None]:
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
