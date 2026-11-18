# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""What it takes to reproduce a track: code, environment, inputs and forcing.

A track bundle carries a ``reproducibility`` block and three files next to ``track.json``:

``config.yaml``
    The run's resolved configuration (after ``--set`` overrides), copied from the run directory.
``environment.txt``
    Python version, platform and every installed distribution as ``name==version``, sorted.
``code.patch``
    ``git diff HEAD`` of the simulator's tracked files, written only when the tree was dirty.
    Untracked source files are listed with their SHA-256 but not copied.

``fingerprint`` is the SHA-256 of a canonical JSON record of everything that determines the
track: the commit, the patch and untracked-file hashes, the environment, the config, the input
files' hashes, the deployment's metadata row and the ocean model's store identifiers. Two
bundles with the same fingerprint came from the same recipe; the fingerprint deliberately
excludes run IDs, times and paths.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import subprocess
import sys
from importlib import metadata
from pathlib import Path
from typing import Any

CONFIG_FILE = "config.yaml"
ENVIRONMENT_FILE = "environment.txt"
PATCH_FILE = "code.patch"

_CHUNK = 1 << 20


def sha256_file(path: Path) -> str:
    """Hex SHA-256 of a file's bytes, read in 1 MiB chunks (tag files run to gigabytes)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(_CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def environment_lines() -> list[str]:
    """Python, platform and installed distributions, one per line, sorted and deduplicated."""
    dists = sorted(
        {
            f"{(d.metadata['Name'] or '').lower()}=={d.version}"
            for d in metadata.distributions()
            if d.metadata["Name"]
        }
    )
    return [
        f"# python {sys.version.split()[0]} ({platform.python_implementation()})",
        f"# platform {platform.system()} {platform.machine()}",
        *dists,
    ]


def _git(repo_dir: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo_dir, capture_output=True, text=True, check=True
    ).stdout


def code_state(repo_dir: Path) -> dict[str, Any]:
    """Commit, branch, whether a remote has the commit, the diff and untracked source files.

    Returns ``{"commit": None}`` outside a git checkout.
    """
    try:
        commit = _git(repo_dir, "rev-parse", "HEAD").strip()
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None}
    branch = _git(repo_dir, "rev-parse", "--abbrev-ref", "HEAD").strip()
    on_remote = bool(_git(repo_dir, "branch", "-r", "--contains", commit).strip())
    patch = _git(repo_dir, "diff", "HEAD", "--binary")
    untracked = [
        p
        for p in _git(repo_dir, "ls-files", "--others", "--exclude-standard").splitlines()
        if p.startswith("src/")
    ]
    return {
        "commit": commit,
        "branch": branch,
        "on_remote": on_remote,
        "dirty": bool(patch.strip()) or bool(untracked),
        "patch": patch,
        "untracked_src": {p: sha256_file(repo_dir / p) for p in sorted(untracked)},
    }


def input_record(path: str | Path) -> dict[str, Any]:
    """Name, size and SHA-256 of an input file; ``sha256`` is None when it cannot be read."""
    p = Path(path)
    try:
        return {"name": p.name, "bytes": p.stat().st_size, "sha256": sha256_file(p)}
    except OSError:
        return {"name": p.name, "bytes": None, "sha256": None}


def deployment_row(meta_path: Path, tag_id: str) -> dict[str, str] | None:
    """The deployment's row of a ``biologger_meta.csv``, or None.

    The row, not the file's hash, goes into the fingerprint: editing another deployment's row
    does not change this track.
    """
    try:
        with open(meta_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if (row.get("tag_id") or row.get("id")) == tag_id:
                    return dict(row)
    except OSError:
        return None
    return None


def fingerprint(record: dict[str, Any]) -> str:
    """SHA-256 of ``record`` as canonical JSON (sorted keys, no whitespace)."""
    return sha256_text(json.dumps(record, sort_keys=True, separators=(",", ":"), default=str))


def write_recipe(
    bundle_dir: Path,
    run_dir: Path,
    code: dict[str, Any],
    environment: list[str],
    inputs: dict[str, Any],
    forcing: dict[str, Any] | None,
) -> dict[str, Any]:
    """Writes the recipe files into ``bundle_dir`` and returns the ``reproducibility`` block."""
    bundle_dir.mkdir(parents=True, exist_ok=True)
    env_text = "\n".join(environment) + "\n"
    (bundle_dir / ENVIRONMENT_FILE).write_text(env_text)
    env_sha = sha256_text(env_text)

    config_src = run_dir / CONFIG_FILE
    config_sha: str | None = None
    if config_src.exists():
        (bundle_dir / CONFIG_FILE).write_bytes(config_src.read_bytes())
        config_sha = sha256_file(config_src)

    patch = code.get("patch") or ""
    patch_sha = sha256_text(patch) if patch.strip() else None
    if patch_sha:
        (bundle_dir / PATCH_FILE).write_text(patch)
    elif (bundle_dir / PATCH_FILE).exists():
        (bundle_dir / PATCH_FILE).unlink()

    # Inputs enter the fingerprint by content: a file by its hash, the metadata row as is.
    recipe_inputs: dict[str, Any] = {
        key: (val.get("sha256") if isinstance(val, dict) and "sha256" in val else val)
        for key, val in inputs.items()
    }
    recipe: dict[str, Any] = {
        "sim_commit": code.get("commit"),
        "code_patch_sha256": patch_sha,
        "untracked_src": code.get("untracked_src") or {},
        "environment_sha256": env_sha,
        "config_sha256": config_sha,
        "inputs": recipe_inputs,
        "forcing": forcing,
    }
    files = {"config": CONFIG_FILE if config_sha else None, "environment": ENVIRONMENT_FILE}
    files["code_patch"] = PATCH_FILE if patch_sha else None
    return {
        "fingerprint": fingerprint(recipe),
        "complete": bool(code.get("commit")) and all(v is not None for v in recipe_inputs.values()),
        "sim_branch": code.get("branch"),
        "sim_commit_on_remote": code.get("on_remote"),
        "sim_dirty": code.get("dirty"),
        "recipe": recipe,
        "inputs": inputs,
        "files": files,
    }
