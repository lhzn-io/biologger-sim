# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import time
from collections import deque
from typing import Any


class TelemetryManager:
    """
    Manages performance telemetry for the simulation loop.
    Tracks FPS, processing latency, and other metrics.
    """

    def __init__(self, window_size: int = 100) -> None:
        self.window_size = window_size
        self.latencies: deque[float] = deque(maxlen=window_size)
        self.frame_times: deque[float] = deque(maxlen=window_size)
        self.last_frame_time = time.time()
        self.start_time = time.time()
        self.frame_count = 0

    def update(self, processing_latency: float) -> None:
        """
        Updates telemetry with the latest frame's metrics.

        Args:
            processing_latency: Time spent processing the current frame (seconds).
        """
        current_time = time.time()
        frame_delta = current_time - self.last_frame_time
        self.last_frame_time = current_time

        self.latencies.append(processing_latency)
        self.frame_times.append(frame_delta)
        self.frame_count += 1

    def get_metrics(self) -> dict[str, Any]:
        """Returns the current performance metrics."""
        if not self.frame_times:
            return {
                "fps": 0.0,
                "latency_ms": 0.0,
                "uptime_s": 0.0,
                "frame_count": 0,
            }

        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        avg_latency = sum(self.latencies) / len(self.latencies)

        return {
            "fps": round(fps, 2),
            "latency_ms": round(avg_latency * 1000, 2),
            "uptime_s": round(time.time() - self.start_time, 2),
            "frame_count": self.frame_count,
        }
