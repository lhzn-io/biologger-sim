from dataclasses import dataclass
from enum import Enum, auto


class ProcessingMode(Enum):
    """
    Defines the processing mode for the pipeline.

    LAB: Post-hoc analysis using acausal filters (filtfilt) for maximum accuracy.
         Matches R implementation.
    SIMULATION: Real-time simulation using causal filters (lfilter/EMA).
                Simulates on-tag processing constraints.
    """

    LAB = auto()
    SIMULATION = auto()


@dataclass
class SensorConfig:
    """Configuration for sensor streams."""

    sampling_rate_hz: float
    noise_sigma: float = 0.0
    bias_stability: float = 0.0


@dataclass
class SimulationConfig:
    """Global simulation configuration."""

    mode: ProcessingMode
    playback_speed: float = 1.0  # 1.0 = real-time
    loop_playback: bool = False
    zmq_port: int = 5555
    zmq_host: str = "127.0.0.1"
