# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Tests for roll continuity (unwrapped roll, roll rate, unwrap quality) and its bundle columns."""

import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from biologger_sim.functions.roll import roll_continuity
from biologger_sim.io.track_bundle import (
    Provenance,
    decimate_quality,
    read_bundle,
    write_bundle,
)

G = 9.80665


def spin(rev_s: float, fs: float = 25.0, seconds: float = 20.0, g: float = G) -> tuple:
    """Body-frame gravity for a fish rolling at a constant rate, level pitch."""
    t = np.arange(int(seconds * fs)) / fs
    phi = 2.0 * math.pi * rev_s * t
    return t, np.zeros_like(t), g * np.sin(phi), g * np.cos(phi)


class TestRollContinuity:
    def test_barrel_roll_counts_full_turns(self) -> None:
        t, ax, ay, az = spin(0.75)
        rc = roll_continuity(t, ax, ay, az)
        # Interior samples: the smoothing window is truncated at the ends.
        turns = (rc.roll_unwrapped_deg[-10] - rc.roll_unwrapped_deg[9]) / 360.0
        assert turns == pytest.approx(0.75 * (t[-10] - t[9]), abs=0.01)
        assert not rc.uncertain.any()
        assert rc.native_rate_hz == pytest.approx(25.0)
        mid = slice(len(t) // 4, 3 * len(t) // 4)
        np.testing.assert_allclose(rc.roll_rate_dps[mid], 270.0, rtol=0.05)

    def test_negative_spin_counts_down(self) -> None:
        t, ax, ay, az = spin(-0.5)
        rc = roll_continuity(t, ax, ay, az)
        assert rc.roll_unwrapped_deg[-1] - rc.roll_unwrapped_deg[0] < -0.5 * 360 * 19

    def test_rocking_has_no_net_roll(self) -> None:
        fs = 25.0
        t = np.arange(int(60 * fs)) / fs
        phi = np.radians(40.0) * np.sin(2 * math.pi * 0.5 * t)
        rc = roll_continuity(t, np.zeros_like(t), G * np.sin(phi), G * np.cos(phi))
        assert np.nanmax(np.abs(rc.roll_unwrapped_deg)) < 45.0
        assert not rc.uncertain.any()

    def test_units_do_not_matter(self) -> None:
        t, ax, ay, az = spin(0.3, g=1.0)
        rc = roll_continuity(t, ax, ay, az)
        assert not rc.uncertain.any()

    def test_step_over_limit_is_uncertain(self) -> None:
        t, ax, ay, az = spin(10.0, seconds=2.0)  # 144 deg per sample at 25 Hz
        rc = roll_continuity(t, ax, ay, az, smooth_s=0.0)
        assert rc.uncertain[1:].all()

    def test_steep_pitch_is_uncertain(self) -> None:
        t = np.arange(50) / 25.0
        pitch = np.radians(np.where(t > 1.0, 80.0, 0.0))
        ax, az = G * np.sin(pitch), G * np.cos(pitch)
        rc = roll_continuity(t, ax, np.zeros_like(t), az, smooth_s=0.0)
        assert not rc.uncertain[t < 1.0].any()
        assert rc.uncertain[t > 1.0].all()

    def test_high_dynamic_acceleration_is_uncertain(self) -> None:
        t, ax, ay, az = spin(0.1, seconds=4.0)
        ax = ax.copy()
        ax[40:50] = 2.0 * G
        rc = roll_continuity(t, ax, ay, az, smooth_s=0.0)
        assert rc.uncertain[40:50].all()
        assert not rc.uncertain[:40].any()

    def test_missing_samples_hold_and_flag(self) -> None:
        t, ax, ay, az = spin(0.2, seconds=4.0)
        ay = ay.copy()
        ay[30:35] = np.nan
        rc = roll_continuity(t, ax, ay, az, smooth_s=0.0)
        assert rc.uncertain[30:36].all()
        assert rc.roll_unwrapped_deg[34] == rc.roll_unwrapped_deg[29]

    def test_time_gap_is_uncertain(self) -> None:
        t, ax, ay, az = spin(0.1, seconds=4.0)
        t = t.copy()
        t[50:] += 10.0
        rc = roll_continuity(t, ax, ay, az, smooth_s=0.0)
        assert rc.uncertain[50] and not rc.uncertain[49] and not rc.uncertain[51]

    def test_empty(self) -> None:
        rc = roll_continuity(np.zeros(0), np.zeros(0), np.zeros(0), np.zeros(0))
        assert len(rc.roll_unwrapped_deg) == 0


class TestDecimateQuality:
    def test_flags_mark_the_stretch_since_the_previous_sample(self) -> None:
        flags = np.array([0, 0, 0, 1, 0, 0, 0, 0, 1, 0], dtype=float)
        idx = np.array([0, 4, 8], dtype=np.intp)
        # 3 falls in (0, 4]; 8 in (4, 8].
        np.testing.assert_array_equal(decimate_quality(flags, idx), [0.0, 1.0, 1.0])

    def test_first_sample_flag(self) -> None:
        np.testing.assert_array_equal(
            decimate_quality(np.array([1.0, 0.0, 0.0]), np.array([0, 2])), [1.0, 0.0]
        )

    def test_all_nan_stays_nan(self) -> None:
        out = decimate_quality(np.full(4, np.nan), np.array([0, 2]))
        assert np.isnan(out).all()


class TestBundleColumns:
    def rows(self, rev_s: float = 0.75, fs: float = 25.0, seconds: float = 30.0) -> pd.DataFrame:
        t, ax, ay, az = spin(rev_s, fs, seconds)
        n = len(t)
        df: pd.DataFrame = pd.DataFrame(
            {
                "timestamp": 1.7e9 + t,
                "pseudo_x": t,
                "pseudo_y": np.zeros(n),
                "Depth": np.full(n, 5.0),
                "pitch_degrees": np.zeros(n),
                "roll_degrees": np.zeros(n),
                "VeDBA": np.full(n, 0.4),
                "ODBA": np.full(n, 0.6),
                "X_Accel_rotate": ax,
                "Y_Accel_rotate": ay,
                "Z_Accel_rotate": az,
            }
        )
        return df

    def test_one_hz_bundle_keeps_the_native_turn_count(self, tmp_path: Path) -> None:
        prov = Provenance(deployment_id="spin", sim_id="spin")
        meta = write_bundle(tmp_path, self.rows(), None, prov, rate_hz=1.0)
        _, cols = read_bundle(tmp_path)
        # At 1 Hz, 0.75 rev/s aliases to -0.25 rev/s; the native unwrap must not.
        turns = (cols["roll_unwrapped_deg"][-1] - cols["roll_unwrapped_deg"][0]) / 360.0
        assert turns == pytest.approx(0.75 * 29.0, abs=0.1)
        assert np.all(np.diff(cols["roll_unwrapped_deg"]) > 0)
        np.testing.assert_allclose(cols["odba"], 0.6)
        np.testing.assert_array_equal(cols["roll_quality"], 0.0)
        units = {c["name"]: c["unit"] for c in meta["columns"]}
        assert units["odba"] == units["vedba"] == "m/s^2"
        assert units["roll_unwrapped_deg"] == "deg" and units["roll_rate_dps"] == "deg/s"
        rc = meta["roll_continuity"]
        assert rc["source"] == "accelerometer"
        assert rc["native_rate_hz"] == pytest.approx(25.0)
        assert rc["uncertain_native_fraction"] == 0.0

    def test_without_acceleration_the_roll_columns_are_nan(self, tmp_path: Path) -> None:
        rows = self.rows().drop(columns=["X_Accel_rotate", "Y_Accel_rotate", "Z_Accel_rotate"])
        meta = write_bundle(tmp_path, rows, None, Provenance("a", "b"), rate_hz=1.0)
        _, cols = read_bundle(tmp_path)
        assert np.isnan(cols["roll_unwrapped_deg"]).all()
        assert np.isnan(cols["roll_quality"]).all()
        assert meta["roll_continuity"] is None
