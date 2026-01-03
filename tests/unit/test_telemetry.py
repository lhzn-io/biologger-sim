# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import time
from unittest.mock import patch

from biologger_sim.core.telemetry import TelemetryManager


def test_telemetry_initialization() -> None:
    """Test that TelemetryManager initializes correctly."""
    tm = TelemetryManager(window_size=50)
    assert tm.window_size == 50
    assert len(tm.latencies) == 0
    assert len(tm.frame_times) == 0
    assert tm.frame_count == 0


def test_telemetry_update() -> None:
    """Test updating telemetry with new frames."""
    tm = TelemetryManager(window_size=10)

    # Simulate a frame update
    with patch("time.time") as mock_time:
        # Initial time set in __init__
        start_time = 1000.0
        tm.last_frame_time = start_time

        # First update after 0.1s
        mock_time.return_value = start_time + 0.1
        tm.update(processing_latency=0.05)

        assert len(tm.latencies) == 1
        assert len(tm.frame_times) == 1
        assert tm.frame_count == 1
        assert tm.latencies[0] == 0.05
        # frame_time should be approx 0.1
        assert abs(tm.frame_times[0] - 0.1) < 1e-6


def test_telemetry_metrics_empty() -> None:
    """Test metrics when no data has been recorded."""
    tm = TelemetryManager()
    metrics = tm.get_metrics()

    assert metrics["fps"] == 0.0
    assert metrics["latency_ms"] == 0.0
    assert metrics["frame_count"] == 0


def test_telemetry_metrics_calculation() -> None:
    """Test calculation of FPS and latency."""
    tm = TelemetryManager(window_size=10)

    # Manually populate deque for predictable results
    # 10 frames, each taking 0.1s (10 FPS)
    # Latency 0.01s (10ms)
    for _ in range(10):
        tm.frame_times.append(0.1)
        tm.latencies.append(0.01)

    tm.frame_count = 10
    tm.start_time = time.time() - 1.0  # 1 second uptime

    metrics = tm.get_metrics()

    assert metrics["fps"] == 10.0
    assert metrics["latency_ms"] == 10.0
    assert metrics["frame_count"] == 10
    assert "uptime_s" in metrics
