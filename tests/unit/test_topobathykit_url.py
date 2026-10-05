# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Tests for the topobathykit URL setting and its one-release topobathysim fallbacks."""

import sys
import warnings
from typing import Any

import pytest

import biologger_sim.__main__ as cli
from biologger_sim.core.types import ProcessingMode, SimulationConfig
from biologger_sim.processors.streaming import StreamingProcessor


def _sim_config(**kwargs: Any) -> SimulationConfig:
    return SimulationConfig.model_validate({"input_file": "tag.csv", **kwargs})


class TestSimulationConfigUrl:
    def test_default_uses_internal_zone(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("error", FutureWarning)
            config = _sim_config()
        assert config.topobathykit_url == "http://garnet.internal:9595"

    def test_new_key(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("error", FutureWarning)
            config = _sim_config(topobathykit_url="http://localhost:9595")
        assert config.topobathykit_url == "http://localhost:9595"

    def test_legacy_key_still_works_with_warning(self) -> None:
        with pytest.warns(FutureWarning, match="topobathykit_url"):
            config = _sim_config(topobathysim_url="http://localhost:9595")
        assert config.topobathykit_url == "http://localhost:9595"

    def test_new_key_wins_over_legacy_key(self) -> None:
        with pytest.warns(FutureWarning):
            config = _sim_config(
                topobathykit_url="http://new:9595", topobathysim_url="http://old:9595"
            )
        assert config.topobathykit_url == "http://new:9595"


class _FakePipelineConfig:
    def __init__(self) -> None:
        self.mode = ProcessingMode.SIMULATION
        self.publish_zmq = True
        self.simulation = _sim_config(topobathykit_url="http://from-config:9595")


def _run_cli(monkeypatch: pytest.MonkeyPatch, *flags: str) -> _FakePipelineConfig:
    captured: dict[str, _FakePipelineConfig] = {}
    monkeypatch.setattr(cli, "load_config", lambda *_args, **_kwargs: _FakePipelineConfig())
    monkeypatch.setattr(
        cli,
        "run_simulation_mode",
        lambda pipeline_config, *_args: captured.setdefault("config", pipeline_config),
    )
    monkeypatch.setattr(sys, "argv", ["biologger-sim", "run", "--config", "x.yaml", *flags])
    cli.main()
    return captured["config"]


class TestCliUrlFlag:
    def test_no_flag_keeps_config_value(self, monkeypatch: pytest.MonkeyPatch) -> None:
        config = _run_cli(monkeypatch)
        assert config.simulation.topobathykit_url == "http://from-config:9595"

    def test_new_flag(self, monkeypatch: pytest.MonkeyPatch) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("error", FutureWarning)
            config = _run_cli(monkeypatch, "--topobathykit-url", "http://cli:9595")
        assert config.simulation.topobathykit_url == "http://cli:9595"

    def test_legacy_flag_still_works_with_warning(self, monkeypatch: pytest.MonkeyPatch) -> None:
        with pytest.warns(FutureWarning, match="--topobathykit-url"):
            config = _run_cli(monkeypatch, "--topobathysim-url", "http://legacy:9595")
        assert config.simulation.topobathykit_url == "http://legacy:9595"


def test_streaming_processor_receives_url() -> None:
    processor = StreamingProcessor(freq=1, topobathykit_url="http://garnet.internal:9595")
    assert processor.topobathykit_url == "http://garnet.internal:9595"
