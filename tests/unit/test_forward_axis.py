# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Tests for the tag forward-axis setting (a tag mounted with +x toward the tail)."""

from typing import Any

import numpy as np
import pytest

from biologger_sim.core.types import CalibrationConfig, TagForwardAxis, reverse_heading_deg
from biologger_sim.processors.lab import PostFactoProcessor
from biologger_sim.processors.streaming import StreamingProcessor

LOCKED: dict[str, Any] = {
    "locked_attachment_roll_deg": 0.0,
    "locked_attachment_pitch_deg": 0.0,
    "locked_mag_offset_x": 0.0,
    "locked_mag_offset_y": 0.0,
    "locked_mag_offset_z": 0.0,
    "locked_mag_sphere_radius": 1.0,
}


def _sensors(n: int = 400) -> tuple[np.ndarray, np.ndarray]:
    """Accelerometer (gravity, tag frame) and magnetometer rows for a pitching, turning fish."""
    i = np.arange(n)
    pitch = np.radians(25.0 * np.sin(i / 40.0))  # elevation of the tag's +x
    roll = np.radians(10.0 * np.cos(i / 55.0))
    acc = np.c_[-np.sin(pitch), np.cos(pitch) * np.sin(roll), np.cos(pitch) * np.cos(roll)]
    turn = i / 90.0
    mag = np.c_[np.cos(turn), np.sin(turn), np.full(n, 0.6)]
    return acc, mag


def _wrapped_diff(a: Any, b: Any) -> np.ndarray:
    d: np.ndarray = (np.asarray(a) - np.asarray(b) + 180.0) % 360.0 - 180.0
    return d


class TestSetting:
    def test_default_is_r_convention(self) -> None:
        assert CalibrationConfig().forward_axis is TagForwardAxis.POS_X
        assert not TagForwardAxis.POS_X.is_reversed

    def test_parses_from_config(self) -> None:
        cfg = CalibrationConfig.model_validate({"forward_axis": "-x"})
        assert cfg.forward_axis is TagForwardAxis.NEG_X
        assert cfg.forward_axis.is_reversed

    def test_rejects_other_axes(self) -> None:
        with pytest.raises(ValueError):
            CalibrationConfig.model_validate({"forward_axis": "+y"})

    @pytest.mark.parametrize(
        ("heading", "expected"), [(0.0, -180.0), (90.0, -90.0), (-90.0, 90.0), (179.0, -1.0)]
    )
    def test_reverse_heading(self, heading: float, expected: float) -> None:
        assert reverse_heading_deg(heading) == pytest.approx(expected)

    def test_reverse_heading_array_stays_in_range(self) -> None:
        h = np.linspace(-180.0, 179.9, 50)
        r = reverse_heading_deg(h)
        assert np.all((r >= -180.0) & (r < 180.0))
        assert np.allclose(np.abs(_wrapped_diff(r, h)), 180.0)


def _batch(axis: TagForwardAxis) -> dict[str, Any]:
    proc = PostFactoProcessor(
        compute_attachment_angles=False,
        compute_mag_offsets=False,
        forward_axis=axis,
        **LOCKED,
    )
    acc, mag = _sensors()
    proc.batch_accel_data = acc.tolist()
    proc.batch_mag_data = mag.tolist()
    proc._process_batch_data()
    assert proc.batch_results is not None
    return proc.batch_results


class TestPostFacto:
    def test_level_tag_heading_points_at_the_head(self) -> None:
        proc = PostFactoProcessor(
            compute_attachment_angles=False, compute_mag_offsets=False, **LOCKED
        )
        n = 200
        proc.batch_accel_data = [[0.0, 0.0, 1.0]] * n
        proc.batch_mag_data = [[1.0, 0.0, 0.0]] * n  # field along +x: +x points north
        proc._process_batch_data()
        fwd = proc.batch_results
        proc_rev = PostFactoProcessor(
            compute_attachment_angles=False,
            compute_mag_offsets=False,
            forward_axis=TagForwardAxis.NEG_X,
            **LOCKED,
        )
        proc_rev.batch_accel_data = proc.batch_accel_data
        proc_rev.batch_mag_data = proc.batch_mag_data
        proc_rev._process_batch_data()
        rev = proc_rev.batch_results
        assert fwd is not None and rev is not None
        assert np.allclose(fwd["heading_deg"], 0.0)
        assert np.allclose(rev["heading_deg"], -180.0)
        assert fwd["pseudo_x"][-1] > 0 > rev["pseudo_x"][-1]  # north, then south

    def test_reversed_tag_turns_heading_and_flips_pitch(self) -> None:
        fwd, rev = _batch(TagForwardAxis.POS_X), _batch(TagForwardAxis.NEG_X)
        assert np.allclose(np.abs(_wrapped_diff(rev["heading_deg"], fwd["heading_deg"])), 180.0)
        assert np.allclose(rev["pseudo_x"], -fwd["pseudo_x"])
        assert np.allclose(rev["pseudo_y"], -fwd["pseudo_y"])
        assert np.allclose(rev["pitch_deg"], -fwd["pitch_deg"])
        assert np.allclose(rev["pitch_rad"], -fwd["pitch_rad"])
        assert np.allclose(rev["roll_deg"], fwd["roll_deg"])
        assert np.any(np.abs(fwd["pitch_deg"]) > 10.0)  # the comparison is not trivially zero


class TestStreaming:
    def _run(self, axis: TagForwardAxis) -> list[dict[str, Any]]:
        proc = StreamingProcessor(filt_len=5, freq=1, forward_axis=axis, **LOCKED)
        acc, mag = _sensors(60)
        out = []
        # accelerometer in 0.1 g units
        for a, m in zip((acc * 10.0).tolist(), mag.tolist(), strict=True):
            record = {"int aX": a[0], "int aY": a[1], "int aZ": a[2]}
            record |= {"int mX": m[0], "int mY": m[1], "int mZ": m[2], "Depth": 10.0}
            out.append(proc.process(record))
        return out

    def test_reversed_tag_turns_heading_and_flips_pitch(self) -> None:
        fwd, rev = self._run(TagForwardAxis.POS_X), self._run(TagForwardAxis.NEG_X)
        h_f = np.array([r["heading_degrees"] for r in fwd])
        h_r = np.array([r["heading_degrees"] for r in rev])
        assert np.allclose(np.abs(_wrapped_diff(h_r, h_f)), 180.0)
        p_f = np.array([r["pitch_degrees"] for r in fwd])
        p_r = np.array([r["pitch_degrees"] for r in rev])
        assert np.allclose(p_r, -p_f)
        assert np.any(np.abs(p_f) > 10.0)
        assert rev[-1]["pseudo_x"] == pytest.approx(-fwd[-1]["pseudo_x"])
        assert rev[-1]["pseudo_y"] == pytest.approx(-fwd[-1]["pseudo_y"])
