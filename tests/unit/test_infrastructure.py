# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import pandas as pd
import pytest


def test_pytest_setup() -> None:
    """Basic test to verify pytest is working."""
    assert True


@pytest.mark.slow
def test_slow_marker() -> None:
    """Test that slow marker is registered."""
    assert True


@pytest.mark.requires_baseline
def test_baseline_marker() -> None:
    """Test that requires_baseline marker is registered."""
    assert True


def test_data_loading(load_stable_period_r_diagnostic: pd.DataFrame) -> None:
    """Verify that we can load the R diagnostic data."""
    df = load_stable_period_r_diagnostic
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    # Check for some expected columns from the 34-column schema
    expected_cols = ["DateTimeP", "Depth", "pitch_degrees", "roll_degrees"]
    for col in expected_cols:
        assert col in df.columns, f"Missing expected column: {col}"
