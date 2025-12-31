# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import hashlib
import subprocess
import warnings
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather

from biologger_sim.core.datetime_utils import excel_date_to_datetime_ns


def get_git_revision_hash() -> str:
    """Returns the current git commit hash."""
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip()
    except Exception:
        return "unknown"


def calculate_src_hash(src_dir: Path) -> str:
    """Calculates MD5 hash of all files in the src directory."""
    md5 = hashlib.md5()
    if not src_dir.exists():
        return "unknown"

    for p in sorted(src_dir.rglob("*")):
        if p.is_file() and not p.name.endswith(".pyc") and "__pycache__" not in p.parts:
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5.update(chunk)
    return md5.hexdigest()


def convert_csv_to_feather(
    input_path: Path, output_path: Path | None = None, metadata: dict[str, str] | None = None
) -> Path:
    """
    Converts a CSV file to Feather format with metadata.

    Args:
        input_path: Path to the input CSV file.
        output_path: Path to the output Feather file. If None, uses input filename with
            .feather extension.
        metadata: Dictionary of metadata to store in the Feather file.

    Returns:
        Path to the generated Feather file.
    """
    if output_path is None:
        output_path = input_path.with_suffix(".feather")

    # Load CSV with robust handling for biologger formats
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=pd.errors.ParserWarning)
            df = pd.read_csv(
                input_path,
                comment=";",
                index_col=False,
                engine="python",
                on_bad_lines="skip",  # Skip bad lines (e.g. events with extra commas)
            )
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV: {e}") from e

    # Ensure DateTimeP exists and is datetime
    if "DateTimeP" not in df.columns:
        if "Date" in df.columns:
            # Excel serial date conversion using high-precision utility
            def safe_excel_to_datetime(x: Any) -> Any:
                if pd.isna(x) or x is None or x == "":
                    return pd.NaT
                try:
                    return excel_date_to_datetime_ns(float(x))[0]
                except (ValueError, TypeError):
                    return pd.NaT

            df["DateTimeP"] = df["Date"].apply(safe_excel_to_datetime)
    elif not pd.api.types.is_datetime64_any_dtype(df["DateTimeP"]):
        df["DateTimeP"] = pd.to_datetime(df["DateTimeP"])

    # Prepare metadata
    if metadata is None:
        metadata = {}

    # Extract header comments from CSV for metadata
    try:
        header_comments = []
        with open(input_path, encoding="utf-8", errors="ignore") as f:
            for _ in range(10):  # Check first 10 lines
                line = f.readline()
                if line.strip().startswith(";"):
                    header_comments.append(line.strip())
                elif not line.strip():
                    continue
                else:
                    break

        for i, comment in enumerate(header_comments):
            metadata[f"header_comment_{i + 1}"] = comment
    except Exception as e:
        print(f"Warning: Failed to extract header comments: {e}")

    # Add provenance metadata
    metadata["source_file"] = str(input_path)
    metadata["conversion_timestamp"] = pd.Timestamp.now().isoformat()
    metadata["git_commit"] = get_git_revision_hash()

    # Convert metadata to bytes for PyArrow
    arrow_metadata = {k: v.encode("utf-8") for k, v in metadata.items()}

    # Create Table
    table = pa.Table.from_pandas(df)

    # Attach metadata
    # Note: from_pandas preserves index metadata, we want to add our custom metadata
    # We need to merge existing metadata (if any) with ours
    existing_metadata = table.schema.metadata or {}
    combined_metadata = {**existing_metadata, **arrow_metadata}

    table = table.replace_schema_metadata(combined_metadata)

    # Write Feather
    feather.write_feather(table, output_path)

    return output_path
