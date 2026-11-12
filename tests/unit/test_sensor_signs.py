# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Tests for calibration.sensor_signs (MK10 accelerometer and magnetometer sign conventions)."""

import math

import numpy as np
import pandas as pd
import pytest

from biologger_sim.core.types import CalibrationConfig, EntityConfig, SensorSigns
from biologger_sim.io.data_loader import (
    SENSOR_CHANNELS,
    STANDARD_GRAVITY,
    apply_sensor_signs,
    correct_accel_depth_bias,
    fit_accel_depth_bias,
    from_standard_export,
)
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


class TestStandardExport:
    def _frame(self, accel: list[float]) -> pd.DataFrame:
        frame: pd.DataFrame = pd.DataFrame(
            {
                "datetime_utc": ["2025-08-27T22:24:23Z", "2025-08-27T22:24:23.040Z"],
                "depth_m": [0.0, 1.5],
                "temperature_c": [23.06, 23.0],
                "accelX_total_raw": [accel[0]] * 2,
                "accelY_total_raw": [accel[1]] * 2,
                "accelZ_total_raw": [accel[2]] * 2,
                "magX_raw": [-247.5] * 2,
                "magY_raw": [463.5] * 2,
                "magZ_raw": [15.0] * 2,
            }
        )
        return frame

    def test_maps_columns_and_scales_g(self) -> None:
        out = from_standard_export(self._frame([0.0, 0.6, 0.8]))
        assert out["DateTimeP"].iloc[1] == pd.Timestamp("2025-08-27T22:24:23.040Z")
        assert out["Depth"].iloc[1] == 1.5
        assert out["int aZ"].iloc[0] == pytest.approx(0.8 * STANDARD_GRAVITY)
        assert out["int mX"].iloc[0] == -247.5  # magnetometer kept as recorded

    def test_keeps_m_per_s2(self) -> None:
        out = from_standard_export(self._frame([0.15, -3.45, -9.05]))
        assert out["int aZ"].iloc[0] == -9.05

    def test_leaves_mk10_exports(self) -> None:
        df = pd.DataFrame({"int aX": [1.0], "Date": [44784.15]})
        assert from_standard_export(df) is df


class TestAccelDepthBias:
    def test_recovers_and_removes_a_depth_linear_offset(self) -> None:
        rng = np.random.default_rng(1)
        n = 6000  # 2 s means of 1 Hz samples: 3000 fitted points
        # Attitudes spread around level, at depths from the surface to 800 m, each held for
        # 20 s (the fit averages 2 s windows, which would shorten a vector that turns within one)
        down = rng.normal([0.0, 0.3, 1.0], [0.25, 0.25, 0.1], size=(n // 20, 3))
        down = np.repeat(down / np.linalg.norm(down, axis=1, keepdims=True), 20, axis=0)
        depth = np.repeat(rng.uniform(0, 800, n // 20), 20)
        b1 = np.array([0.06, -0.01, 0.008]) * STANDARD_GRAVITY  # per 100 m
        acc = down * STANDARD_GRAVITY + np.outer(depth / 100.0, b1)
        df = pd.DataFrame(acc, columns=["int aX", "int aY", "int aZ"]).assign(
            Depth=depth,
            DateTimeP=pd.date_range("2025-08-28", periods=n, freq="1s", tz="UTC"),
        )
        p = fit_accel_depth_bias(df)
        assert p[3:6] == pytest.approx(b1, abs=0.003 * STANDARD_GRAVITY)
        out = correct_accel_depth_bias(df)
        mag = np.linalg.norm(out[["int aX", "int aY", "int aZ"]].to_numpy(), axis=1)
        assert np.abs(mag / STANDARD_GRAVITY - 1).max() < 0.01

    def test_off_by_default(self) -> None:
        assert CalibrationConfig().accel_depth_bias is False


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
