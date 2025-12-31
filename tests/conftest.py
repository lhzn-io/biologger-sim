# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from collections.abc import Callable
from pathlib import Path

import pandas as pd
import pytest

# Constants for validation
ORIENTATION_TOLERANCE_DEG = 0.01
RELATIVE_TOLERANCE = 0.001


@pytest.fixture(scope="session")
def test_data_root() -> Path:
    """Returns the root directory of the test datasets."""
    # Use local tests/data directory
    path = Path(__file__).parent / "data"
    if not path.exists():
        # Fallback or warning if running in a different environment
        print(f"WARNING: Test data path {path} does not exist.")
    return path


@pytest.fixture(scope="session")
def metadata_path(test_data_root: Path) -> Path:
    """Returns the path to the metadata CSV."""
    path = test_data_root / "biologger_meta.csv"
    if not path.exists():
        # Fallback to project root if not found in datasets
        path = Path("biologger_meta.csv")
    return path


@pytest.fixture(scope="session")
def stable_period_path(test_data_root: Path) -> Path:
    return test_data_root / "stable_period"


@pytest.fixture(scope="session")
def attachment_angle_validation_path(test_data_root: Path) -> Path:
    return test_data_root / "attachment_angle_validation"


@pytest.fixture(scope="session")
def early_deployment_path(test_data_root: Path) -> Path:
    return test_data_root / "early_deployment"


@pytest.fixture(scope="session")
def load_stable_period_r_diagnostic(stable_period_path: Path) -> pd.DataFrame:
    """Loads the R diagnostic CSV for the stable period."""
    csv_path = stable_period_path / "RED001_20220812_19A0564_stable_period-R-diagnostic.csv"
    if not csv_path.exists():
        pytest.skip(f"R diagnostic file not found: {csv_path}")
    return pd.read_csv(csv_path)


@pytest.fixture(scope="session")
def load_attachment_angle_r_diagnostic(attachment_angle_validation_path: Path) -> pd.DataFrame:
    """Loads the R diagnostic CSV for the attachment angle validation."""
    csv_path = (
        attachment_angle_validation_path / "RED001_20220812_19A0564-buffer-sized-R-diagnostic.csv"
    )
    if not csv_path.exists():
        pytest.skip(f"R diagnostic file not found: {csv_path}")
    return pd.read_csv(csv_path)


@pytest.fixture
def assert_series_close() -> Callable[..., None]:
    """Fixture that returns a helper function to compare two pandas Series."""

    def _assert(
        actual: pd.Series,
        expected: pd.Series,
        abs_tol: float | None = None,
        rel_tol: float | None = None,
        name: str = "Series",
    ) -> None:
        try:
            pd.testing.assert_series_equal(
                actual,
                expected,
                check_names=False,
                rtol=rel_tol or RELATIVE_TOLERANCE,
                atol=abs_tol or 0,
            )
        except AssertionError as e:
            raise AssertionError(f"{name} mismatch: {e}") from e

    return _assert
