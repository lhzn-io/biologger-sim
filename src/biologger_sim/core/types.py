# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator


class ProcessingMode(str, Enum):
    """
    Defines the processing mode for the pipeline.

    LAB: Post-hoc analysis using acausal filters (filtfilt) for maximum accuracy.
         Matches R implementation.
    SIMULATION: Real-time simulation using causal filters (lfilter/EMA).
                Simulates on-tag processing constraints.
    """

    LAB = "LAB"
    SIMULATION = "SIMULATION"


class CalibrationMode(str, Enum):
    """
    Defines how sensor calibration parameters are determined.

    BATCH_COMPUTE: Calculate from the full dataset (R-style, acausal).
    FIXED: Use pre-determined constants (Real-time/Tag-style).
    """

    BATCH_COMPUTE = "batch_compute"
    FIXED = "fixed"


class DepthMode(str, Enum):
    """
    Defines how depth data is processed.

    INTERPOLATE: Acausal interpolation of missing values (R-style).
    REALTIME: Causal processing (hold last value or predict).
    """

    INTERPOLATE = "interpolate"
    REALTIME = "realtime"


class AHRSAlgorithm(str, Enum):
    """
    Defines the AHRS algorithm to use for sensor fusion.
    """

    MADGWICK = "madgwick"
    MAHONY = "mahony"
    COMPLEMENTARY = "complementary"
    EKF = "ekf"


class AHRSConfig(BaseModel):
    """Configuration for AHRS sensor fusion."""

    enabled: bool = False
    algorithm: AHRSAlgorithm = AHRSAlgorithm.MADGWICK

    # Algorithm parameters
    beta: float = 0.1  # Madgwick gain
    kp: float = 0.5  # Mahony proportional gain
    ki: float = 0.0  # Mahony integral gain

    # Adaptive fusion settings
    use_adaptive: bool = False
    normal_gravity_threshold: float = 0.05
    slip_gravity_threshold: float = 0.15

    # Geometric smoothing
    smoothing_alpha: float = 0.01


class CalibrationConfig(BaseModel):
    """Configuration for sensor calibration."""

    attachment_angle_mode: CalibrationMode = Field(
        default=CalibrationMode.BATCH_COMPUTE,
        description="Method for determining attachment angle.",
    )
    magnetometer_mode: CalibrationMode = Field(
        default=CalibrationMode.BATCH_COMPUTE,
        description="Method for determining magnetometer offsets.",
    )

    # Fixed values (optional, used if mode is FIXED)
    locked_attachment_roll_deg: float | None = None
    locked_attachment_pitch_deg: float | None = None

    locked_mag_offset_x: float | None = None
    locked_mag_offset_y: float | None = None
    locked_mag_offset_z: float | None = None
    locked_mag_sphere_radius: float | None = None


class DepthConfig(BaseModel):
    """Configuration for depth processing."""

    mode: DepthMode = DepthMode.REALTIME


class ZMQConfig(BaseModel):
    """Configuration for ZeroMQ communication."""

    port: int = 5555
    host: str = "127.0.0.1"
    topic: str = "biologger/telemetry"


class EntityConfig(BaseModel):
    """Configuration for a single entity-simulation instance."""

    sim_id: str  # Unique view handle (e.g., "sword_r_exact")
    tag_id: str | None = None  # Key for biologger_meta.csv (defaults to sim_id)
    input_file: Path
    sampling_rate_hz: float = 16.0  # Recording frequency of this specific entity

    # Temporal alignment
    start_time_offset: float = 0.0

    # Processing parameters (moved from top-level for per-entity control)
    true_integration: bool = False  # Enable True Integration (vs R-Compatible)
    calibration: CalibrationConfig = Field(default_factory=CalibrationConfig)
    depth: DepthConfig = Field(default_factory=DepthConfig)
    ahrs: AHRSConfig = Field(default_factory=AHRSConfig)


class SimulationConfig(BaseModel):
    """Configuration for simulation-wide settings."""

    entities: list[EntityConfig] = Field(default_factory=list)
    meta_file: Path | None = None  # Global biologger_meta.csv for species lookup

    playback_speed: float = 1.0  # Real-time multiplier (CLI --speed)
    loop: bool = False
    zmq: ZMQConfig = Field(default_factory=ZMQConfig)

    @model_validator(mode="before")
    @classmethod
    def validate_simulation_source(cls, values: Any) -> Any:
        """Ensures that either 'entities' or 'input_file' (legacy/simple) is provided."""
        entities = values.get("entities")
        input_file = values.get("input_file")

        if not entities and not input_file:
            raise ValueError("Either 'entities' list or 'input_file' must be provided")

        # If entities is empty but input_file is set, populate entities with a default
        # and wrap it in a list so the validator below sees it.
        if not entities and input_file:
            # Use the filename as a default sim_id if not explicitly provided
            default_sim_id = Path(input_file).stem if isinstance(input_file, str) else "default"
            values["entities"] = [EntityConfig(sim_id=default_sim_id, input_file=input_file)]
        return values


class PipelineConfig(BaseModel):
    """Global multi-entity pipeline configuration."""

    mode: ProcessingMode = ProcessingMode.SIMULATION
    simulation: SimulationConfig
