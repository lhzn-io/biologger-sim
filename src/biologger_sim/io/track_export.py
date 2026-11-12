# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Track export: run-directory track metadata and back-filling bundles from finished runs.

Lab runs write ``<sim_id>_track_meta.json`` next to ``<sim_id>_output.csv`` (see
:func:`write_track_meta`) with the track model applied and the heading rotation, which the
output CSV alone cannot recover: a fix-pinned run saves the placed track and the corrected
heading, so the rotation that produced them is no longer observable. :func:`bundles_from_run`
turns a finished run into track bundles (:mod:`biologger_sim.io.track_bundle`), reading that
sidecar when present and otherwise falling back to the run's ``messages.log`` and to
:func:`apply_track_model`.
"""

from __future__ import annotations

import csv
import json
import logging
import re
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from biologger_sim.core.georef import GeoReference, georeference_from_row
from biologger_sim.core.species import max_sustained_speed
from biologger_sim.core.track_models import apply_track_model
from biologger_sim.core.types import TrackModel

from .track_bundle import (
    VEDBA_UNIT_LAB,
    VEDBA_UNIT_STREAMING,
    Provenance,
    git_state,
    sha256_file,
    write_bundle,
)

logger = logging.getLogger(__name__)

TRACK_META_SUFFIX = "_track_meta.json"

_LOG_TRACK_MODEL = re.compile(r"Track model: (\w+) \(configured (\w+)\)")
_LOG_HEADING = re.compile(r"Heading corrected by (-?[\d.]+) deg")

# Output columns the bundle needs; reading only these keeps a 2 GB output CSV in memory.
_BUNDLE_SOURCE_COLUMNS = [
    "timestamp",
    "pseudo_x",
    "pseudo_y",
    "Depth",
    "heading_degrees",
    "pitch_degrees",
    "roll_degrees",
    "VeDBA",
]


def write_track_meta(run_dir: Path, sim_id: str, payload: dict[str, Any]) -> Path:
    """Writes ``<sim_id>_track_meta.json`` in the run directory and returns its path."""
    path = run_dir / f"{sim_id}{TRACK_META_SUFFIX}"
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    return path


def track_meta_payload(
    *,
    sim_id: str,
    tag_id: str | None,
    species: str | None,
    track_model_configured: TrackModel,
    track_model_used: TrackModel,
    heading_correction_deg: float,
    v_max: float,
    vedba_unit: str,
    repo_dir: Path,
) -> dict[str, Any]:
    """The content of a run's ``<sim_id>_track_meta.json``."""
    commit, dirty = git_state(repo_dir)
    return {
        "sim_id": sim_id,
        "tag_id": tag_id,
        "species": species,
        "track_model_configured": track_model_configured.value,
        "track_model_used": track_model_used.value,
        "heading_correction_deg": heading_correction_deg,
        "v_max_m_s": v_max,
        "vedba_unit": vedba_unit,
        "sim_git_commit": commit,
        "sim_git_dirty": dirty,
    }


def resolve_meta_file(meta_file: str | Path, config_dir: Path) -> Path:
    """Resolves a config's ``meta_file`` the way ``run_lab_mode`` does.

    Absolute paths are used as is; a relative path is tried against ``config_dir`` first and
    then against the working directory.
    """
    path = Path(meta_file)
    if path.is_absolute():
        return path
    config_rel = (config_dir / path).resolve()
    return config_rel if config_rel.exists() else path.resolve()


def lookup_deployment(meta_path: Path, tag_id: str) -> tuple[GeoReference | None, str | None]:
    """Returns (georeference, species) for ``tag_id`` from a ``biologger_meta.csv``."""
    with open(meta_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (row.get("tag_id") or row.get("id")) == tag_id:
                return georeference_from_row(row), (row.get("species") or None)
    return None, None


def track_meta_from_log(log_path: Path) -> tuple[str | None, float | None]:
    """(track model used, heading correction in degrees) from a run's ``messages.log``.

    With several entities in one run the last match wins; callers with more than one entity
    should rely on the per-entity sidecar instead.
    """
    if not log_path.exists():
        return None, None
    used: str | None = None
    heading: float | None = None
    with open(log_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = _LOG_TRACK_MODEL.search(line)
            if m:
                used, heading = m.group(1), None
                continue
            m = _LOG_HEADING.search(line)
            if m:
                heading = float(m.group(1))
    return used, heading


def _vedba_unit(config: dict[str, Any], entity: dict[str, Any]) -> str:
    lab = str(config.get("mode", "")).upper() == "LAB" or bool(entity.get("strict_r_parity"))
    return VEDBA_UNIT_LAB if lab else VEDBA_UNIT_STREAMING


def bundles_from_run(
    run_dir: Path,
    out_dir: Path | None = None,
    rate_hz: float = 1.0,
    config_dir: Path = Path("config"),
    repo_dir: Path = Path("."),
) -> list[Path]:
    """Writes a track bundle for each entity of a finished run that left an output CSV.

    ``out_dir`` defaults to ``<run_dir>/track``; with more than one entity each bundle goes
    in a ``<sim_id>`` subdirectory. ``meta_file`` in the run's ``config.yaml`` is resolved
    relative to ``config_dir`` (the repository's ``config/``), as the original config was.
    Returns the bundle directories written.
    """
    config_path = run_dir / "config.yaml"
    config = yaml.safe_load(config_path.read_text())
    sim = config.get("simulation", {})
    entities = sim.get("entities", [])
    base = out_dir if out_dir is not None else run_dir / "track"
    written: list[Path] = []

    for entity in entities:
        sim_id = entity["sim_id"]
        tag_id = entity.get("tag_id") or sim_id
        csv_path = run_dir / f"{sim_id}_output.csv"
        if not csv_path.exists():
            logger.warning(f"{run_dir.name}: no {csv_path.name}; skipping {sim_id}")
            continue

        meta_file = entity.get("metadata_file") or sim.get("meta_file")
        georef: GeoReference | None = None
        species: str | None = None
        if meta_file:
            georef, species = lookup_deployment(resolve_meta_file(meta_file, config_dir), tag_id)
        if georef is None:
            logger.warning(f"{sim_id}: no start fix for {tag_id}; bundle will have no lat/lon")

        header = pd.read_csv(csv_path, nrows=0).columns
        rows = pd.read_csv(csv_path, usecols=[c for c in _BUNDLE_SOURCE_COLUMNS if c in header])

        dr = entity.get("dead_reckoning") or {}
        configured = TrackModel(dr.get("track_model", TrackModel.DEAD_RECKONING.value))
        notes: list[str] = []
        sidecar_path = run_dir / f"{sim_id}{TRACK_META_SUFFIX}"
        sidecar = json.loads(sidecar_path.read_text()) if sidecar_path.exists() else None

        if sidecar is not None:
            used = sidecar["track_model_used"]
            heading = sidecar["heading_correction_deg"]
            heading_source = "run"
            commit, dirty = sidecar.get("sim_git_commit"), sidecar.get("sim_git_dirty")
            species = sidecar.get("species") or species
        else:
            commit, dirty = None, None
            notes.append("Back-filled from an output CSV; the sim commit at run time is unknown.")
            # Recompute the fallback: a model that needs an end fix degrades to dead
            # reckoning without one.
            t = rows["timestamp"].to_numpy(dtype=float)
            _, _, used_model = apply_track_model(
                configured,
                t,
                rows["pseudo_x"].to_numpy(dtype=float),
                rows["pseudo_y"].to_numpy(dtype=float),
                georef,
            )
            used = used_model.value
            log_used, log_heading = track_meta_from_log(run_dir / "messages.log")
            if log_used is not None and log_used != used and len(entities) == 1:
                notes.append(f"messages.log reports track model {log_used}; using it.")
                used = log_used
            if used != TrackModel.FIX_PINNED.value:
                heading, heading_source = 0.0, "model"  # only pinning rotates the heading
            elif log_heading is not None and len(entities) == 1:
                heading, heading_source = log_heading, "messages.log"
            else:
                # The output CSV holds the pinned track and corrected heading, so the
                # rotation between them and the raw track cannot be recovered from it.
                heading, heading_source = None, None
                notes.append("Heading correction not recorded for this run.")

        provenance = Provenance(
            deployment_id=tag_id,
            sim_id=sim_id,
            run_id=run_dir.name,
            source="from-run",
            sim_git_commit=commit,
            sim_git_dirty=dirty,
            config_file=str(config_path.name),
            config_sha256=sha256_file(config_path),
            species=species,
            track_model_configured=configured.value,
            track_model_used=used,
            heading_correction_deg=heading,
            heading_correction_source=heading_source,
            v_max_m_s=(sidecar or {}).get("v_max_m_s")
            or max_sustained_speed(species, dr.get("max_sustained_speed_m_s")),
            vedba_unit=_vedba_unit(config, entity),
            notes=notes,
        )
        dest = base / sim_id if len(entities) > 1 else base
        meta = write_bundle(dest, rows, georef, provenance, rate_hz)
        logger.info(f"{sim_id}: wrote {meta['count']} samples at {rate_hz} Hz to {dest}")
        written.append(dest)
    return written


def bundle_from_results(
    out_dir: Path,
    result_df: pd.DataFrame,
    georef: GeoReference | None,
    track_meta: dict[str, Any],
    run_dir: Path,
    rate_hz: float = 1.0,
) -> dict[str, Any]:
    """Writes a bundle from in-memory pipeline results and the run's track metadata."""
    config_path = run_dir / "config.yaml"
    provenance = Provenance(
        deployment_id=track_meta.get("tag_id") or track_meta["sim_id"],
        sim_id=track_meta["sim_id"],
        run_id=run_dir.name,
        source="pipeline",
        sim_git_commit=track_meta.get("sim_git_commit"),
        sim_git_dirty=track_meta.get("sim_git_dirty"),
        config_file=config_path.name if config_path.exists() else None,
        config_sha256=sha256_file(config_path) if config_path.exists() else None,
        species=track_meta.get("species"),
        track_model_configured=track_meta.get("track_model_configured"),
        track_model_used=track_meta.get("track_model_used"),
        heading_correction_deg=track_meta.get("heading_correction_deg"),
        heading_correction_source="run",
        v_max_m_s=track_meta.get("v_max_m_s"),
        vedba_unit=track_meta.get("vedba_unit", VEDBA_UNIT_LAB),
    )
    cols = [c for c in _BUNDLE_SOURCE_COLUMNS if c in result_df]
    return write_bundle(out_dir, result_df[cols], georef, provenance, rate_hz)
