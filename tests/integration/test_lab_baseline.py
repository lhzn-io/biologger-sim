# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pytest

from biologger_sim.io.data_loader import load_and_filter_data
from biologger_sim.processors.lab import PostFactoProcessor


@pytest.mark.slow
@pytest.mark.requires_baseline
def test_lab_pipeline_vs_r_baseline(
    stable_period_path: Path,
    metadata_path: Path,
    load_stable_period_r_diagnostic: pd.DataFrame,
    assert_series_close: Callable[..., None],
) -> None:
    # Load input data
    input_csv = stable_period_path / "RED001_20220812_19A0564_stable_period.csv"
    if not input_csv.exists():
        pytest.skip(f"Input file not found: {input_csv}")

    # Load and filter data using metadata
    # Tag ID in metadata is RED001_20220812
    try:
        input_df = load_and_filter_data(input_csv, metadata_path, "RED001_20220812")
    except Exception as e:
        pytest.fail(f"Failed to load and filter data: {e}")

    # Load R baseline
    r_df = load_stable_period_r_diagnostic

    # Initialize processor
    # We use r_exact_mode=True to compute calibration from the data, matching R's batch approach
    processor = PostFactoProcessor(
        filt_len=48,  # Standard 3s @ 16Hz
        freq=16,
        r_exact_mode=True,
        compute_attachment_angles=True,
        compute_mag_offsets=True,
        debug_level=0,
    )

    # Pass 1: Collect calibration data
    records = input_df.to_dict("records")

    for record in records:
        processor.process(cast(dict[str, Any], record))

    # Compute calibration
    processor.calibrate_from_batch_data()

    # Reset for Pass 2
    processor.reset()

    # Pass 2: Process and collect results
    results = []
    for record in records:
        res = processor.process(cast(dict[str, Any], record))
        results.append(res)

    result_df = pd.DataFrame(results)

    # Compare columns
    # We skip the first few rows (filter warmup) for strict comparison
    start_idx = 50

    # Pitch
    assert_series_close(
        result_df["pitch_degrees"].iloc[start_idx:],
        r_df["pitch_degrees"].iloc[start_idx:],
        abs_tol=0.1,
        name="Pitch",
    )

    # Roll
    assert_series_close(
        result_df["roll_degrees"].iloc[start_idx:],
        r_df["roll_degrees"].iloc[start_idx:],
        abs_tol=0.1,
        name="Roll",
    )

    # Static Acceleration X
    assert_series_close(
        result_df["X_Static"].iloc[start_idx:],
        r_df["X_Static"].iloc[start_idx:],
        abs_tol=0.05,
        name="X_Static",
    )

    # ODBA
    assert_series_close(
        result_df["ODBA"].iloc[start_idx:], r_df["ODBA"].iloc[start_idx:], abs_tol=0.05, name="ODBA"
    )
