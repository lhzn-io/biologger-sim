# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import json
from typing import Any

import numpy as np
import zmq
from scipy.spatial.transform import Rotation

from ..core.types import SimulationConfig


class ZMQPublisher:
    """
    Publishes sensor data and simulation state via ZeroMQ.
    Connects to the NVIDIA Omniverse extension.
    """

    def __init__(self, config: SimulationConfig, debug_level: int = 0) -> None:
        self.config = config
        self.debug_level = debug_level
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

    def publish_state(self, state: dict[str, Any]) -> None:
        """
        Publishes the simulation state to Omniverse in the expected format.
        Converts Euler angles to Quaternions (w, x, y, z).

        Args:
            state: Dictionary containing 'pitch_radians', 'roll_radians', 'heading_radians',
                   'X_Dynamic', 'Y_Dynamic', 'Z_Dynamic', 'VeDBA'.
        """
        # Extract Euler angles (default to 0 if missing/nan)
        roll = state.get("roll_radians", 0.0)
        pitch = state.get("pitch_radians", 0.0)
        heading = state.get("heading_radians", 0.0)

        if np.isnan(roll):
            roll = 0.0
        if np.isnan(pitch):
            pitch = 0.0
        if np.isnan(heading):
            heading = 0.0

        # Convert to Quaternion (w, x, y, z)
        # Sequence: 'zyx' (yaw, pitch, roll) is standard for aerospace/navigation
        # Note: heading is yaw (Z), pitch is Y, roll is X
        rot = Rotation.from_euler("zyx", [heading, pitch, roll], degrees=False)
        quat = rot.as_quat()  # Returns (x, y, z, w) by default in scipy

        # Reorder to (w, x, y, z) for Omniverse
        # scipy: [x, y, z, w] -> omni: [w, x, y, z]
        quat_omni = [quat[3], quat[0], quat[1], quat[2]]

        # Construct payload matching architecture.rst
        payload = {
            "transform": {"quat": quat_omni},
            "physics": {
                "accel_dynamic": [
                    state.get("X_Dynamic", 0.0),
                    state.get("Y_Dynamic", 0.0),
                    state.get("Z_Dynamic", 0.0),
                ],
                "vedba": state.get("VeDBA", 0.0),
            },
        }

        # Handle numpy types for JSON serialization
        def default_converter(o: Any) -> Any:
            if isinstance(o, np.int64 | np.int32):
                return int(o)
            if isinstance(o, np.float64 | np.float32):
                return float(o)
            if isinstance(o, np.ndarray):
                return o.tolist()
            return str(o)

        # Send with topic prefix
        message = json.dumps(payload, default=default_converter)
        topic = self.config.zmq.topic
        if self.debug_level >= 2:
            print(f"DEBUG: Sending ZMQ: {topic} {message[:50]}...")
        self.socket.send_string(f"{topic} {message}")

    def close(self) -> None:
        """Clean up ZMQ resources."""
        self.socket.close()
        self.context.term()
