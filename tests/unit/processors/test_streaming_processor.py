# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import pytest

from biologger_sim.processors.streaming import StreamingProcessor


class TestStreamingProcessor:
    @pytest.fixture
    def processor(self) -> StreamingProcessor:
        return StreamingProcessor(
            filt_len=5,  # Small window for testing
            freq=1,
            locked_attachment_roll_deg=0.0,
            locked_attachment_pitch_deg=0.0,
        )

    def test_initialization(self, processor: StreamingProcessor) -> None:
        assert processor.record_count == 0
        assert len(processor.accel_buffer) == 0
        assert processor.get_performance_summary()["processor_type"] == "StreamingProcessor"

    def test_gsep_calculation(self, processor: StreamingProcessor) -> None:
        # Feed constant acceleration in 0.1g units (10.0 = 1.0g)
        data = {
            "int aX": 10.0,
            "int aY": 0.0,
            "int aZ": 0.0,
            "int mX": 0.0,
            "int mY": 0.0,
            "int mZ": 0.0,
            "Depth": 0.0,
        }

        # Warmup phase: Fill the buffer (filt_len=5)
        for _ in range(5):
            processor.process(data)

        # Now 6th sample should use averaged static
        # Current [10, 10, 10, 10, 10] -> Mean 10 (1.0g)
        # Feed 20.0 (2.0g)
        data2 = data.copy()
        data2["int aX"] = 20.0
        res = processor.process(data2)

        # Buffer now: [10, 10, 10, 10, 20] -> Mean 12.0 (1.2g)
        # Dynamic: 2.0g - 1.2g = 0.8g
        assert abs(res["X_Static"] - 1.2) < 0.001
        assert abs(res["X_Dynamic"] - 0.8) < 0.001
        assert abs(res["ODBA"] - 0.8) < 0.001

    def test_orientation_output(self, processor: StreamingProcessor) -> None:
        # Static Z=1.0g (10.0 units) -> Pitch=0, Roll=0
        data = {
            "int aX": 0.0,
            "int aY": 0.0,
            "int aZ": 10.0,
            "int mX": 1.0,
            "int mY": 0.0,
            "int mZ": 0.0,
        }
        # Process enough to get out of warmup for static estimate
        for _ in range(5):
            res = processor.process(data)

        # Allow small float error
        assert abs(res["pitch_degrees"]) < 0.01
        assert abs(res["roll_degrees"]) < 0.01

        # Test Pitch down (X = 1g = 10.0 units)
        data2 = {
            "int aX": 10.0,
            "int aY": 0.0,
            "int aZ": 0.0,
            "int mX": 0.0,
            "int mY": 0.0,
            "int mZ": 0.0,
        }

        # Re-init processor to clear buffer
        proc2 = StreamingProcessor(filt_len=5, freq=1)
        for _ in range(5):
            res2 = proc2.process(data2)

        # Static X should be 1.0g
        assert abs(res2["X_Static"] - 1.0) < 0.001

        # Pitch calculation: -degrees(atan2(1, 0)) = -90
        assert abs(res2["pitch_degrees"] + 90.0) < 0.01

    def test_locked_calibration(self) -> None:
        # Test that locked attachment angles rotate input
        # Rotate 90 deg around X (Roll)
        proc = StreamingProcessor(
            locked_attachment_roll_deg=90.0, locked_attachment_pitch_deg=0.0, filt_len=5
        )

        # Input Y=10.0 (1g lateral)
        data = {"int aX": 0.0, "int aY": 10.0, "int aZ": 0.0}

        for _ in range(5):
            res = proc.process(data)

        # Rotated Z should be 1.0g (after div 10)
        assert abs(res["Z_Static"] - 1.0) < 0.01
        assert abs(res["Y_Static"]) < 0.01
