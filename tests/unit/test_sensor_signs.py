# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Tests for calibration.sensor_signs (MK10 accelerometer and magnetometer sign conventions)."""

import math

import numpy as np
import pandas as pd
import pytest

from biologger_sim.core.types import CalibrationConfig, EntityConfig, SensorSigns
from biologger_sim.io.data_loader import SENSOR_CHANNELS, apply_sensor_signs
from biologger_sim.processors.lab import PostFactoProcessor

DIP = math.radians(66.0)  # field dip off New England, downward


def _rot(heading: float, pitch: float, roll: float) -> np.ndarray:
    """Body (forward, right, down) to world (north, east, down); angles in degrees."""
    h, p, r = (math.radians(a) for a in (heading, pitch, roll))
    rz = np.array([[math.cos(h), -math.sin(h), 0], [math.sin(h), math.cos(h), 0], [0, 0, 1]])
    ry = np.array([[math.cos(p), 0, math.sin(p)], [0, 1, 0], [-math.sin(p), 0, math.cos(p)]])
    rx = np.array([[1, 0, 0], [0, math.cos(r), -math.sin(r)], [0, math.sin(r), math.cos(r)]])
    m: np.ndarray = rz @ ry @ rx
    return m


def _mk10_frame(heading: float, pitch: float, roll: float, n: int = 200) -> pd.DataFrame:
    """Readings of an MK10 with +x forward and +z out of the base (down), as recorded.

    The accelerometer reads specific force (up; Z = -9.8 m/s/s at rest) and the magnetometer
    reads the negative of the field, as on RED001.
    """
    to_body = _rot(heading, pitch, roll).T
    up = to_body @ np.array([0.0, 0.0, -1.0]) * 9.8
    field = to_body @ np.array([math.cos(DIP), 0.0, math.sin(DIP)])
    row = dict(zip(SENSOR_CHANNELS, [*up, *(-field)], strict=True))
    frame: pd.DataFrame = pd.DataFrame([row] * n).assign(Depth=50.0)
    return frame


def _process(df: pd.DataFrame) -> dict[str, np.ndarray]:
    proc = PostFactoProcessor(
        compute_attachment_angles=False,
        compute_mag_offsets=False,
        locked_attachment_roll_deg=0.0,
        locked_attachment_pitch_deg=0.0,
        locked_mag_offset_x=0.0,
        locked_mag_offset_y=0.0,
        locked_mag_offset_z=0.0,
        locked_mag_sphere_radius=1.0,
    )
    proc.batch_accel_data = df[["int aX", "int aY", "int aZ"]].to_numpy().tolist()
    proc.batch_mag_data = df[["int mX", "int mY", "int mZ"]].to_numpy().tolist()
    proc._process_batch_data()
    assert proc.batch_results is not None
    return proc.batch_results


def _wrap(a: float) -> float:
    return (a + 180.0) % 360.0 - 180.0


class TestSetting:
    def test_default_is_r_script(self) -> None:
        assert CalibrationConfig().sensor_signs is SensorSigns.R_SCRIPT

    def test_parses_from_config(self) -> None:
        cfg = CalibrationConfig.model_validate({"sensor_signs": "negated"})
        assert cfg.sensor_signs is SensorSigns.NEGATED

    def test_negates_only_the_sensor_channels(self) -> None:
        df = pd.DataFrame({"int aX": [1.0], '"int mZ"': [2.0], "Depth": [30.0], "Events": ["x"]})
        out = apply_sensor_signs(df, SensorSigns.NEGATED)
        assert out["int aX"].iloc[0] == -1.0
        assert out['"int mZ"'].iloc[0] == -2.0
        assert out["Depth"].iloc[0] == 30.0 and out["Events"].iloc[0] == "x"
        assert df["int aX"].iloc[0] == 1.0  # input untouched

    def test_strict_r_parity_keeps_the_r_signs(self) -> None:
        with pytest.warns(UserWarning, match="sensor_signs"):
            ent = EntityConfig.model_validate(
                {
                    "sim_id": "parity",
                    "input_file": "x.csv",
                    "strict_r_parity": True,
                    "calibration": {"sensor_signs": "negated"},
                }
            )
        assert ent.calibration.sensor_signs is SensorSigns.R_SCRIPT

    def test_r_script_leaves_the_frame(self) -> None:
        df = pd.DataFrame({"int aX": [1.0]})
        assert apply_sensor_signs(df, SensorSigns.R_SCRIPT) is df


# (heading, pitch, roll, heading tolerance). The R tilt correction removes pitch before roll,
# which is exact when either is zero and off by a few degrees when both are large.
ATTITUDES = [
    (0.0, 0.0, 0.0, 0.5),
    (90.0, 0.0, 0.0, 0.5),
    (200.0, -25.0, 0.0, 0.5),
    (300.0, 0.0, -30.0, 0.5),
    (45.0, 20.0, 15.0, 5.0),
]


class TestMK10Attitude:
    @pytest.mark.parametrize(("heading", "pitch", "roll", "tol"), ATTITUDES)
    def test_negated_recovers_the_attitude(
        self, heading: float, pitch: float, roll: float, tol: float
    ) -> None:
        res = _process(apply_sensor_signs(_mk10_frame(heading, pitch, roll), SensorSigns.NEGATED))
        assert _wrap(float(res["heading_deg"][-1]) - heading) == pytest.approx(0.0, abs=tol)
        assert float(res["pitch_deg"][-1]) == pytest.approx(pitch, abs=0.5)
        assert float(res["roll_deg"][-1]) == pytest.approx(roll, abs=0.5)

    @pytest.mark.parametrize("heading", [0.0, 70.0, 200.0])
    def test_as_recorded_mirrors_a_level_heading(self, heading: float) -> None:
        res = _process(_mk10_frame(heading, 0.0, 0.0))
        mirrored = 180.0 - heading
        assert _wrap(float(res["heading_deg"][-1]) - mirrored) == pytest.approx(0.0, abs=0.5)

    def test_as_recorded_flips_pitch(self) -> None:
        res = _process(_mk10_frame(0.0, -25.0, 0.0))
        assert float(res["pitch_deg"][-1]) == pytest.approx(25.0, abs=0.5)
