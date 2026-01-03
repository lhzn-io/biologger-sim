# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from pathlib import Path

import pyarrow.feather as feather

from biologger_sim.io.converter import calculate_src_hash, convert_csv_to_feather


def test_calculate_src_hash(tmp_path: Path) -> None:
    """Test MD5 hash calculation of a directory."""
    # Create a dummy file
    d = tmp_path / "src"
    d.mkdir()
    p = d / "hello.py"
    p.write_text("print('hello')")

    hash1 = calculate_src_hash(d)
    assert hash1 != "unknown"

    # Modify file
    p.write_text("print('world')")
    hash2 = calculate_src_hash(d)
    assert hash1 != hash2


def test_convert_csv_to_feather(tmp_path: Path) -> None:
    """Test conversion from CSV to Feather."""
    # Create a dummy CSV
    csv_path = tmp_path / "test.csv"

    # Create a CSV with header comments (Little Leonardo style)
    content = """
; Header Comment 1
; Header Comment 2
Date,Time,Depth,Temp
2025-01-01,12:00:00,10.5,20.0
2025-01-01,12:00:01,10.6,20.1
"""
    csv_path.write_text(content.strip())

    output_path = tmp_path / "test.feather"

    # Run conversion
    result_path = convert_csv_to_feather(csv_path, output_path)

    assert result_path.exists()
    assert result_path == output_path

    # Verify content
    df = feather.read_feather(output_path)
    assert len(df) == 2
    assert "Depth" in df.columns
    assert df.iloc[0]["Depth"] == 10.5

    # Verify metadata
    table = feather.read_table(output_path)
    metadata = table.schema.metadata
    assert metadata is not None
    # Check for header comments (keys are bytes in pyarrow metadata)
    assert b"header_comment_1" in metadata
    assert b"source_file" in metadata


def test_convert_csv_to_feather_auto_output(tmp_path: Path) -> None:
    """Test conversion with automatic output path generation."""
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("A,B\n1,2")

    result_path = convert_csv_to_feather(csv_path)

    expected_path = tmp_path / "data.feather"
    assert result_path == expected_path
    assert result_path.exists()
