# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Track bundle reproducibility: recipe files, fingerprint and the export path."""

import json
import math
import subprocess
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pytest

from biologger_sim.core import provenance as pv
from biologger_sim.core.georef import GeoFix, GeoReference
from biologger_sim.core.types import TrackModel
from biologger_sim.io import reproducibility as rp
from biologger_sim.io.track_export import bundle_from_results, track_meta_payload

T0 = 1660357807.999992
GEO = GeoReference(start=GeoFix(T0, 35.534425, -45.694675), end=GeoFix(T0 + 10, 35.5345, -45.6946))


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "sim"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "a.py").write_text("x = 1\n")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "-c", "user.name=t", "-c", "user.email=t@example.org", "add", ".")
    git(repo, "-c", "user.name=t", "-c", "user.email=t@example.org", "commit", "-qm", "init")
    return repo


def rows(n: int = 32) -> pd.DataFrame:
    s = np.arange(n) / 16.0
    df: pd.DataFrame = pd.DataFrame(
        {
            "timestamp": T0 + s,
            "pseudo_x": s * math.cos(math.radians(45.0)),
            "pseudo_y": s * math.sin(math.radians(45.0)),
            "Depth": 2.0 + 0.1 * s,
            "heading_degrees": np.full(n, 45.0),
            "pitch_degrees": np.full(n, -10.0),
            "roll_degrees": np.full(n, 3.0),
            "VeDBA": np.full(n, 0.5),
        }
    )
    return df


class TestCodeState:
    def test_clean_tree(self, tmp_path: Path) -> None:
        state = rp.code_state(make_repo(tmp_path))
        assert len(state["commit"]) == 40
        assert state["branch"] == "main"
        assert state["dirty"] is False
        assert state["patch"] == ""
        assert state["on_remote"] is False

    def test_dirty_tree_records_patch_and_untracked(self, tmp_path: Path) -> None:
        repo = make_repo(tmp_path)
        (repo / "src" / "a.py").write_text("x = 2\n")
        (repo / "src" / "b.py").write_text("y = 1\n")
        state = rp.code_state(repo)
        assert state["dirty"] is True
        assert "+x = 2" in state["patch"]
        assert list(state["untracked_src"]) == ["src/b.py"]

    def test_outside_git(self, tmp_path: Path) -> None:
        assert rp.code_state(tmp_path) == {"commit": None}


class TestFingerprint:
    def test_order_independent_and_sensitive(self) -> None:
        a = rp.fingerprint({"x": 1, "y": [1, 2]})
        assert a == rp.fingerprint({"y": [1, 2], "x": 1})
        assert a != rp.fingerprint({"x": 2, "y": [1, 2]})

    def test_sha256_file_streams(self, tmp_path: Path) -> None:
        p = tmp_path / "f.bin"
        p.write_bytes(b"a" * (3 << 20))
        import hashlib

        assert rp.sha256_file(p) == hashlib.sha256(p.read_bytes()).hexdigest()

    def test_deployment_row(self, tmp_path: Path) -> None:
        meta = tmp_path / "meta.csv"
        meta.write_text("tag_id,end_lat\nA,1.0\nB,2.0\n")
        assert rp.deployment_row(meta, "B") == {"tag_id": "B", "end_lat": "2.0"}
        assert rp.deployment_row(meta, "C") is None


class TestPipelineShape:
    def test_step_carries_method_version(self) -> None:
        s = pv.step("placement", "fix_pinned", {"scale": 1.5})
        assert s["version"] == pv.METHOD_VERSIONS["fix_pinned"]
        assert s["status"] == "applied"

    def test_unknown_method_has_no_version(self) -> None:
        with pytest.raises(KeyError):
            pv.step("placement", "not_a_method", {})

    def test_bad_status_rejected(self) -> None:
        with pytest.raises(ValueError, match="status"):
            pv.step("placement", "fix_pinned", {}, status="maybe")

    def test_non_finite_metric_is_null(self) -> None:
        assert pv.metric("end_fix_miss", float("nan"), "m")["value"] is None

    def test_open_params_any_shape(self) -> None:
        # A future method's params need no format change.
        s = pv.step("placement", "fix_pinned", {"nested": {"a": [1, 2]}, "flag": True})
        pv.validate([s], [])

    def test_validate_names_the_problem(self) -> None:
        with pytest.raises(ValueError, match=r"pipeline\[0\] lacks \['version'"):
            pv.validate([{"step": "x", "method": "y", "status": "applied", "params": {}}], [])
        with pytest.raises(ValueError, match=r"metrics\[0\] lacks \['unit'"):
            pv.validate([], [{"name": "m", "value": 1.0, "by": "x"}])

    def test_write_bundle_rejects_malformed_pipeline(self, tmp_path: Path) -> None:
        from biologger_sim.io.track_bundle import Provenance, write_bundle

        prov = Provenance(deployment_id="d", sim_id="s", pipeline=[{"step": "x"}])
        with pytest.raises(ValueError, match="pipeline"):
            write_bundle(tmp_path / "b", rows(), GEO, prov, 1.0)

    def test_find_step(self) -> None:
        a = pv.step("placement", "dead_reckoning", {})
        b = pv.step("placement", "fix_pinned", {})
        assert pv.find_step([a, b], "placement") is b
        assert pv.find_step([a], "current_correction") is None


class TestBundleRecipe:
    def export(self, tmp_path: Path, repo: Path, name: str, tag_bytes: bytes) -> dict[str, Any]:
        run_dir = tmp_path / f"run_{name}"
        run_dir.mkdir()
        (run_dir / "config.yaml").write_text("simulation: {}\n")
        tag = tmp_path / f"tag_{name}.csv"
        tag.write_bytes(tag_bytes)
        meta = tmp_path / "meta.csv"
        meta.write_text("tag_id,end_lat\nT1,35.5345\n")
        track_meta = track_meta_payload(
            sim_id="s",
            tag_id="T1",
            species=None,
            track_model_configured=TrackModel.FIX_PINNED,
            track_model_used=TrackModel.FIX_PINNED,
            heading_correction_deg=10.0,
            v_max=1.0,
            vedba_unit="m/s^2",
            repo_dir=repo,
            processor_record={
                "pipeline": [
                    pv.step("dead_reckoning", "odba_scaled", {"odba_speed_factor": 2.0}),
                    pv.step(
                        "current_correction",
                        "forcingkit",
                        {
                            "donor_used": "hycom",
                            "forcingkit_attrs": {"forcingkit_ocean_store_id": "s1"},
                        },
                    ),
                    pv.step("placement", "fix_pinned", {"scale": 2.0}),
                ],
                "metrics": [pv.metric("end_fix_miss", 0.0, "m")],
            },
            input_file=tag,
            meta_path=meta,
        )
        out = tmp_path / f"bundle_{name}"
        bundle_from_results(out, rows(), GEO, track_meta, run_dir)
        written: dict[str, Any] = json.loads((out / "track.json").read_text())
        return written

    def test_bundle_carries_recipe(self, tmp_path: Path) -> None:
        repo = make_repo(tmp_path)
        meta = self.export(tmp_path, repo, "a", b"tag data")
        r = meta["reproducibility"]
        assert r["complete"] is True
        assert r["sim_dirty"] is False
        assert r["files"] == {
            "config": "config.yaml",
            "environment": "environment.txt",
            "code_patch": None,
        }
        assert r["recipe"]["forcing"]["donor_used"] == "hycom"
        assert r["inputs"]["deployment_row"] == {"tag_id": "T1", "end_lat": "35.5345"}
        assert [s["step"] for s in meta["pipeline"]] == [
            "dead_reckoning",
            "current_correction",
            "placement",
        ]
        assert meta["pipeline"][2] == {
            "step": "placement",
            "method": "fix_pinned",
            "version": 1,
            "status": "applied",
            "params": {"scale": 2.0},
        }
        assert meta["metrics"] == [
            {"name": "end_fix_miss", "value": 0.0, "unit": "m", "by": "export-track"}
        ]
        bundle = tmp_path / "bundle_a"
        assert (bundle / "config.yaml").read_text() == "simulation: {}\n"
        assert (bundle / "environment.txt").read_text().startswith("# python ")
        assert not (bundle / "code.patch").exists()

    def test_same_recipe_same_fingerprint(self, tmp_path: Path) -> None:
        repo = make_repo(tmp_path)
        a = self.export(tmp_path, repo, "a", b"tag data")
        b = self.export(tmp_path, repo, "b", b"tag data")
        c = self.export(tmp_path, repo, "c", b"other tag data")
        assert a["run_id"] != b["run_id"]
        assert a["reproducibility"]["fingerprint"] == b["reproducibility"]["fingerprint"]
        assert a["reproducibility"]["fingerprint"] != c["reproducibility"]["fingerprint"]

    def test_dirty_tree_writes_patch_and_changes_fingerprint(self, tmp_path: Path) -> None:
        repo = make_repo(tmp_path)
        clean = self.export(tmp_path, repo, "a", b"tag data")
        (repo / "src" / "a.py").write_text("x = 3\n")
        dirty = self.export(tmp_path, repo, "b", b"tag data")
        assert dirty["reproducibility"]["files"]["code_patch"] == "code.patch"
        assert "+x = 3" in (tmp_path / "bundle_b" / "code.patch").read_text()
        assert clean["reproducibility"]["fingerprint"] != dirty["reproducibility"]["fingerprint"]
