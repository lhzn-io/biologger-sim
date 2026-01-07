# Copyright (c) 2025-2026 Long Horizon Observatory
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

    def __init__(self, config: SimulationConfig, debug_level: int = 0) -> None:
        self.config = config
        self.debug_level = debug_level
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)

        # Optimize socket for high throughput / low latency
        # LINGER: 0 to discard messages on close immediately
        self.socket.setsockopt(zmq.LINGER, 0)
        # SNDHWM: High Water Mark (limit queue size)
        self.socket.setsockopt(zmq.SNDHWM, 10000)

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
        # Fast-path: try standard dump first (optimistically assume primitives)
        try:
            message = json.dumps(data)
        except TypeError:
            # Fallback for numpy types
            def default_converter(o: Any) -> Any:
                if isinstance(o, np.integer):
                    return int(o)
                if isinstance(o, np.floating):
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
        Sends Euler angles (degrees) for the receiver to handle rotation.

        Args:
            state: Dictionary containing 'pitch_degrees', 'roll_degrees', 'heading_degrees',
                   'X_Dynamic', 'Y_Dynamic', 'Z_Dynamic', 'VeDBA'.
        """
        # Explicit float conversion for speed (avoiding numpy overhead in json serialization)
        # Using cast to float() ensures fast JSON encoding
        roll = float(state.get("roll_degrees", 0.0) or 0.0)
        pitch = float(state.get("pitch_degrees", 0.0) or 0.0)
        heading = float(state.get("heading_degrees", 0.0) or 0.0)

        if np.isnan(roll):
            roll = 0.0
        if np.isnan(pitch):
            pitch = 0.0
        if np.isnan(heading):
            heading = 0.0

        # Physics extraction with explicit casting
        x_dyn = float(state.get("X_Dynamic", 0.0) or 0.0)
        y_dyn = float(state.get("Y_Dynamic", 0.0) or 0.0)
        z_dyn = float(state.get("Z_Dynamic", 0.0) or 0.0)
        vedba = float(state.get("VeDBA", 0.0) or 0.0)
        odba = float(state.get("ODBA", 0.0) or 0.0)
        depth = float(state.get("Depth", 0.0) or 0.0)
        velocity = float(state.get("Velocity", 0.0) or 0.0)
        v_velocity = float(state.get("Vertical_Velocity", 0.0) or 0.0)
        pseudo_x = float(state.get("pseudo_x", 0.0) or 0.0)
        pseudo_y = float(state.get("pseudo_y", 0.0) or 0.0)
        timestamp = float(state.get("timestamp", 0.0) or 0.0)

        # Construct payload matching architecture.rst
        payload = {
            "timestamp": timestamp,
            "rotation": {
                "euler_deg": [roll, pitch, heading],
                "order": "zyx",  # Intrinsic ZYX (Yaw, Pitch, Roll)
            },
            "physics": {
                "accel_dynamic": [x_dyn, y_dyn, z_dyn],
                "vedba": vedba,
                "odba": odba,
                "depth": depth,
                "velocity": velocity,
                "vertical_velocity": v_velocity,
                "pseudo_x": pseudo_x,
                "pseudo_y": pseudo_y,
            },
        }

        # Optimized send: payload is now guaranteed to be standard python types
        # so we can use standard json.dumps directly
        msg = json.dumps(payload)
        topic = self.config.zmq.topic

        if self.debug_level >= 2:
            print(f"DEBUG: Sending ZMQ: {topic} {msg[:50]}...")

        self.socket.send_string(f"{topic} {msg}")

    def close(self) -> None:
        """Clean up ZMQ resources."""
        self.socket.close()
        self.context.term()
