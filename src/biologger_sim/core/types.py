# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import warnings
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


class AHRSAlgorithm(str, Enum):
    """
    Defines the AHRS algorithm to use for sensor fusion.
    """

    MADGWICK = "madgwick"
    MAHONY = "mahony"
    COMPLEMENTARY = "complementary"
    EKF = "ekf"


class SpeedModel(str, Enum):
    """
    Defines the model used for speed estimation (dead reckoning).
    """

    CONSTANT = "constant"
    ODBA_SCALED = "odba_scaled"


class DeadReckoningConfig(BaseModel):
    """Configuration for dead reckoning and speed estimation."""

    speed_model: SpeedModel = SpeedModel.ODBA_SCALED
    constant_speed_m_s: float = 1.0
    odba_speed_factor: float = 2.0


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


class DepthAlgorithm(str, Enum):
    """
    Defines the algorithm used for depth estimation.

    ACAUSAL_INTERP: Post-hoc, full-batch interpolation (R-compatible).
    CAUSAL_SAMPLE_HOLD: Simple hold/nearest neighbor for real-time.
    """

    ACAUSAL_INTERP = "acausal_interpolate"
    CAUSAL_SAMPLE_HOLD = "causal_sample_hold"
    OFF = "off"


class ClockSource(str, Enum):
    """
    Defines the source of time steps for integration.

    FIXED_FREQ: Use fixed 1/sampling_rate_hz steps. (R-Compatible)
    SENSOR_TIME: Use actual differential timestamps from sensor data.
    """

    FIXED_FREQ = "fixed_frequency"
    SENSOR_TIME = "sensor_timestamps"


class DepthConfig(BaseModel):
    """Configuration for depth estimation."""

    algorithm: DepthAlgorithm = DepthAlgorithm.CAUSAL_SAMPLE_HOLD

    # Acausal Parameters
    interpolation_max_gap: float = 5.0  # Max gap in seconds to interpolate


class ZMQConfig(BaseModel):
    """Configuration for ZeroMQ communication."""

    port: int = 5555
    host: str = "127.0.0.1"
    topic: str = "biologger/telemetry"


class EntityConfig(BaseModel):
    """Configuration for a single simulation entity."""

    sim_id: str
    tag_id: str | None = None  # Key for biologger_meta.csv (defaults to sim_id)
    input_file: Path
    sampling_rate_hz: int = 16  # Recording frequency of this specific entity

    # Temporal alignment
    start_time_offset: float = 0.0
    metadata_file: Path | None = None

    # Processing parameters (moved from top-level for per-entity control)
    clock_source: ClockSource = ClockSource.FIXED_FREQ  # Default: R-Compatible
    strict_r_parity: bool = False  # Enforce R-compatible settings
    calibration: CalibrationConfig = Field(default_factory=CalibrationConfig)
    depth_estimation: DepthConfig = Field(default_factory=DepthConfig)
    dead_reckoning: DeadReckoningConfig = Field(default_factory=DeadReckoningConfig)
    ahrs: AHRSConfig = Field(default_factory=AHRSConfig)

    # Output control
    save_telemetry: bool = False

    @model_validator(mode="after")
    def enforce_r_parity(self) -> "EntityConfig":
        """Enforces R-parity settings if strict mode is enabled."""
        if self.strict_r_parity:
            # 1. Clock Source (formerly True Integration)
            if self.clock_source != ClockSource.FIXED_FREQ:
                warnings.warn(
                    f"[{self.sim_id}] strict_r_parity overrides clock_source to FIXED_FREQ.",
                    stacklevel=2,
                )
                self.clock_source = ClockSource.FIXED_FREQ

            # 2. Calibration Modes
            if self.calibration.attachment_angle_mode != CalibrationMode.BATCH_COMPUTE:
                warnings.warn(
                    f"[{self.sim_id}] strict_r_parity overrides attachment_angle_mode "
                    "to BATCH_COMPUTE.",
                    stacklevel=2,
                )
                self.calibration.attachment_angle_mode = CalibrationMode.BATCH_COMPUTE

            if self.calibration.magnetometer_mode != CalibrationMode.BATCH_COMPUTE:
                warnings.warn(
                    f"[{self.sim_id}] strict_r_parity overrides magnetometer_mode "
                    "to BATCH_COMPUTE.",
                    stacklevel=2,
                )
                self.calibration.magnetometer_mode = CalibrationMode.BATCH_COMPUTE

            # 3. Depth Algorithm
            if self.depth_estimation.algorithm != DepthAlgorithm.ACAUSAL_INTERP:
                warnings.warn(
                    f"[{self.sim_id}] strict_r_parity overrides depth algorithm to ACAUSAL_INTERP.",
                    stacklevel=2,
                )
                self.depth_estimation.algorithm = DepthAlgorithm.ACAUSAL_INTERP

        return self


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
    publish_zmq: bool = True
    simulation: SimulationConfig
