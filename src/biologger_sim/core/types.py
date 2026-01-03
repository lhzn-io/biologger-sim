# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from enum import Enum
from pathlib import Path

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


class SimulationConfig(BaseModel):
    """Configuration for the simulation playback."""

    input_file: Path
    rate_hz: float = 100.0
    loop: bool = False
    zmq: ZMQConfig = Field(default_factory=ZMQConfig)


class PipelineConfig(BaseModel):
    """Global pipeline configuration."""

    mode: ProcessingMode = ProcessingMode.SIMULATION
    calibration: CalibrationConfig = Field(default_factory=CalibrationConfig)
    depth: DepthConfig = Field(default_factory=DepthConfig)
    ahrs: AHRSConfig = Field(default_factory=AHRSConfig)
    simulation: SimulationConfig

    @model_validator(mode="after")
    def set_defaults_based_on_mode(self) -> "PipelineConfig":
        """
        Smart defaults:
        - If mode is LAB, default to BATCH_COMPUTE calibration and INTERPOLATE depth.
        - If mode is SIMULATION, default to FIXED calibration and REALTIME depth.
        """
        if self.mode == ProcessingMode.LAB:
            # Force R-parity defaults for LAB mode
            self.calibration.attachment_angle_mode = CalibrationMode.BATCH_COMPUTE
            self.calibration.magnetometer_mode = CalibrationMode.BATCH_COMPUTE
            self.depth.mode = DepthMode.INTERPOLATE
            self.ahrs.enabled = False  # Lab mode typically uses direct calculation, not AHRS fusion

        elif self.mode == ProcessingMode.SIMULATION:
            # Ensure defaults for SIMULATION mode if not set
            if self.calibration.attachment_angle_mode == CalibrationMode.BATCH_COMPUTE:
                # Warn or just allow it? For now, let's allow mixed modes but default to FIXED
                pass

        return self
