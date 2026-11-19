# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Configs written before a key was removed still load; the removed keys are ignored."""

from pathlib import Path

from biologger_sim.config import load_config

LEGACY_YAML = """\
mode: LAB
simulation:
  entities:
    - sim_id: sword_postfacto
      tag_id: RED001
      input_file: tag.csv
      depth_estimation:
        algorithm: acausal_interpolate
        interpolation_max_gap: 5.0
      dead_reckoning:
        track_model: fix_pinned
      ahrs:
        enabled: false
        algorithm: madgwick
        beta: 0.033
"""


def test_config_with_removed_ahrs_and_interpolation_max_gap_loads(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(LEGACY_YAML)
    config = load_config(path)
    entity = config.simulation.entities[0]
    assert entity.sim_id == "sword_postfacto"
    assert entity.dead_reckoning.track_model.value == "fix_pinned"
    assert entity.depth_estimation.algorithm.value == "acausal_interpolate"
    assert not hasattr(entity, "ahrs")
    assert not hasattr(entity.depth_estimation, "interpolation_max_gap")
