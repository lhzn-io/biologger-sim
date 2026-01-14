# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import logging
from typing import Any

import msgpack
import numpy as np
import zmq

from ..core.types import SimulationConfig


class ZMQPublisher:
    """
    Publishes sensor data and simulation state via ZeroMQ.
    Connects to the NVIDIA Omniverse extension using MessagePack.
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

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"ZMQ Publisher bound to {self.address} (using MessagePack)")

    def _default_converter(self, o: Any) -> Any:
        """Fallback for numpy types during MessagePack packing."""
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if hasattr(o, "isoformat"):  # datetime
            return o.isoformat()
        return str(o)

    def publish(self, topic: str, data: dict[str, Any]) -> None:
        """
        Publishes a message to a specific topic using MessagePack.

        Args:
            topic: The topic string (e.g., "sensor/imu", "sim/state").
            data: The data dictionary to publish.
        """
        try:
            packed = msgpack.packb(data, use_bin_type=True)
        except TypeError:
            packed = msgpack.packb(data, default=self._default_converter, use_bin_type=True)

        self.socket.send_multipart([topic.encode(), packed])

    def publish_state(self, eid: int, sim_id: str, tag_id: str, state: dict[str, Any]) -> None:
        """
        Publishes the simulation state to Omniverse in the expected format.
        Sends Euler angles (degrees) for the receiver to handle rotation.

        Args:
            eid: Integer entity identifier.
            sim_id: String simulation identifier (e.g., "SF_RED001_v2").
            state: Dictionary containing 'pitch_degrees', 'roll_degrees', 'heading_degrees',
                   'X_Dynamic', 'Y_Dynamic', 'Z_Dynamic', 'VeDBA'.
        """
        # Explicit float conversion for speed
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
        x_static = float(state.get("X_Static", 0.0) or 0.0)
        y_static = float(state.get("Y_Static", 0.0) or 0.0)
        z_static = float(state.get("Z_Static", 0.0) or 0.0)
        vedba = float(state.get("VeDBA", 0.0) or 0.0)
        odba = float(state.get("ODBA", 0.0) or 0.0)
        depth = float(state.get("Depth", 0.0) or 0.0)
        velocity = float(state.get("velocity", 0.0) or 0.0)
        v_velocity = float(state.get("vertical_velocity", 0.0) or 0.0)
        pseudo_x = float(state.get("pseudo_x", 0.0) or 0.0)
        pseudo_y = float(state.get("pseudo_y", 0.0) or 0.0)
        timestamp = float(state.get("timestamp", 0.0) or 0.0)
        clock_drift_sec = float(state.get("clock_drift_sec", 0.0) or 0.0)

        # Construct efficient payload (short keys for msgpack optimization)
        payload = {
            "eid": eid,
            "sim_id": sim_id,
            "tag_id": tag_id,
            "ts": timestamp,
            "rot": [roll, pitch, heading],
            "phys": {
                "dacc": [x_dyn, y_dyn, z_dyn],
                "sacc": [x_static, y_static, z_static],
                "vedba": vedba,
                "odba": odba,
                "d": depth,
                "v": velocity,
                "vv": v_velocity,
                "px": pseudo_x,
                "py": pseudo_y,
                "cd": clock_drift_sec,
            },
        }

        packed = msgpack.packb(payload, use_bin_type=True)
        topic = self.config.zmq.topic

        if self.debug_level >= 2:
            self.logger.debug(f"ZMQ Send [eid={eid}]: {payload}")

        self.socket.send_multipart([topic.encode(), packed])

    def close(self) -> None:
        """Clean up ZMQ resources."""
        self.socket.close()
        self.context.term()
