# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import json
from typing import Any

import numpy as np
import zmq

from ..core.types import SimulationConfig


class ZMQPublisher:
    """
    Publishes sensor data and simulation state via ZeroMQ.
    Connects to the NVIDIA Omniverse extension.
    """

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.address = f"tcp://{self.config.zmq.host}:{self.config.zmq.port}"
        self.socket.bind(self.address)
        print(f"ZMQ Publisher bound to {self.address}")

    def publish(self, topic: str, data: dict[str, Any]) -> None:
        """
        Publishes a message to a specific topic.

        Args:
            topic: The topic string (e.g., "sensor/imu", "sim/state").
            data: The data dictionary to publish.
        """

        # Handle numpy types for JSON serialization
        def default_converter(o: Any) -> Any:
            if isinstance(o, np.int64 | np.int32):
                return int(o)
            if isinstance(o, np.float64 | np.float32):
                return float(o)
            if isinstance(o, np.ndarray):
                return o.tolist()
            if hasattr(o, "isoformat"):  # datetime
                return o.isoformat()
            return str(o)

        message = json.dumps(data, default=default_converter)
        self.socket.send_string(f"{topic} {message}")

    def close(self) -> None:
        """Clean up ZMQ resources."""
        self.socket.close()
        self.context.term()
