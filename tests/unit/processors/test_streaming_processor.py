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
            ema_fast_alpha=0.5,
            ema_slow_alpha=0.1,
        )

    def test_initialization(self, processor: StreamingProcessor) -> None:
        assert processor.record_count == 0
        assert len(processor.accel_buffer) == 0
        assert processor.get_performance_summary()["processor_type"] == "StreamingProcessor"

    def test_gsep_calculation(self, processor: StreamingProcessor) -> None:
        # Feed constant acceleration (should become static)
        data = {
            "int aX": 1.0,
            "int aY": 0.0,
            "int aZ": 0.0,
            "int mX": 0.0,
            "int mY": 0.0,
            "int mZ": 0.0,
            "Depth": 0.0,
        }

        # 1st sample
        res1 = processor.process(data)
        assert res1["X_Static"] == 1.0  # Buffer size 1, mean is 1.0
        assert res1["X_Dynamic"] == 0.0

        # Feed varying data
        # [1.0, 2.0] -> Mean 1.5. Current 2.0. Dynamic = 2.0 - 1.5 = 0.5
        data2 = data.copy()
        data2["int aX"] = 2.0
        res2 = processor.process(data2)

        assert res2["X_Static"] == 1.5
        assert res2["X_Dynamic"] == 0.5
        assert res2["ODBA"] == 0.5  # Only X changed

    def test_crossover_logic(self, processor: StreamingProcessor) -> None:
        # Initial state should be STEADY
        res = processor.process(
            {
                "int aX": 1.0,
                "int aY": 0.0,
                "int aZ": 0.0,
                "int mX": 0.0,
                "int mY": 0.0,
                "int mZ": 0.0,
            }
        )
        assert res["logging_state"] == "STEADY"

        # Create a sudden spike to trigger crossover
        # ODBA will jump
        data_spike = {
            "int aX": 10.0,  # Massive jump
            "int aY": 0.0,
            "int aZ": 0.0,
            "int mX": 0.0,
            "int mY": 0.0,
            "int mZ": 0.0,
        }

        # Sample 1: ODBA ~9.0 (current 10 - mean ~something low)
        # Processor buffer: [1.0, 2.0, 10.0] -> Mean ~4.3. Dynamic ~5.7.
        # Fast EMA (0.5) updates fast. Slow EMA (0.1) lags.
        # Difference should differ.

        res_spike = processor.process(data_spike)

        assert res_spike["crossover_signal"] > 0.5  # Should be positive
        assert res_spike["logging_state"] in ["TRANSITION", "RAPID_CHANGE"]

    def test_orientation_output(self, processor: StreamingProcessor) -> None:
        # Static Z=1g (upright) -> Pitch=0, Roll=0
        data = {
            "int aX": 0.0,
            "int aY": 0.0,
            "int aZ": 1.0,
            "int mX": 1.0,
            "int mY": 0.0,
            "int mZ": 0.0,
        }
        res = processor.process(data)

        # Allow small float error
        assert abs(res["pitch_degrees"]) < 0.001
        assert abs(res["roll_degrees"]) < 0.001

        # Test Pitch down (X = 1g)
        # Pitch = -atan2(ax, ...)
        # If X=1, pitch should be -90 deg?
        # Check coordinates: X forward, Y right, Z down.
        # Nose down -> +Pitch? Or -Pitch?
        # R code: pitch = atan2(-x, ...)
        # If x=1, atan2(-1, 0) = -pi/2 = -90.
        # So X=1 is -90 degrees pitch.

        data2 = {
            "int aX": 1.0,
            "int aY": 0.0,
            "int aZ": 0.0,
            "int mX": 0.0,
            "int mY": 0.0,
            "int mZ": 0.0,
        }

        # Re-init processor to clear buffer
        proc2 = StreamingProcessor(filt_len=5, freq=1)
        res2 = proc2.process(data2)

        # Static X should be 1.0 (mean of [1.0])
        assert abs(res2["X_Static"] - 1.0) < 0.001

        # Pitch calculation: -degrees(atan2(1, 0)) = -90
        assert abs(res2["pitch_degrees"] + 90.0) < 0.001

    def test_locked_calibration(self) -> None:
        # Test that locked attachment angles rotate input
        # Rotate 90 deg around X (Roll)
        # Input Y=1 -> Output Z=1 (approx)

        proc = StreamingProcessor(locked_attachment_roll_deg=90.0, locked_attachment_pitch_deg=0.0)

        data = {"int aX": 0.0, "int aY": 1.0, "int aZ": 0.0}

        res = proc.process(data)

        # Rotated values
        # Y=1 rotated 90 deg roll -> Z=-1.0 (based on xb matrix definition)
        assert abs(res["Z_Accel_rotate"] + 1.0) < 0.001
        assert abs(res["Y_Accel_rotate"]) < 0.001
