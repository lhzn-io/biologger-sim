# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from pathlib import Path

import pandas as pd
import pytest

from biologger_sim.io.converter import read_tag_csv

# The shape of a Wildlife Computers MK10 export: comment lines, a header of 6 names, event rows that
# fill all 6 fields, and sensor rows with one more (the wet/dry label).
MK10 = """; SN 00X0000
; Records 0 to 5 of 6
Date,Depth,"int aX","Wet / Dry Threshold",Events
44784.150000,,,,11-Aug-2022 03:36 Data sampling started
44784.150000,,,80.00,11-Aug-2022 03:36 Conductivity Threshold: 80
44784.150001,0.00,0.20,,,Dry
44784.150002,,0.10,,,Dry
44784.150003,1.50,-0.40,,,Wet
44784.150004,,,,11-Aug-2022 03:37 an event, with, commas
"""


@pytest.fixture
def mk10(tmp_path: Path) -> Path:
    path = tmp_path / "tag.csv"
    path.write_text(MK10)
    return path


def test_sensor_rows_with_a_trailing_label_are_kept(mk10: Path) -> None:
    df = read_tag_csv(mk10)
    assert list(df.columns) == ["Date", "Depth", "int aX", "Wet / Dry Threshold", "Events"]
    # Two event rows and three sensor rows; the event with commas in its text is skipped.
    assert len(df) == 5
    assert df["int aX"].tolist()[2:] == [0.20, 0.10, -0.40]
    assert df["Depth"].iloc[4] == 1.50
    assert df["Events"].iloc[0] == "11-Aug-2022 03:36 Data sampling started"
    assert df["Wet / Dry Threshold"].iloc[1] == 80.0
    assert pd.isna(df["Events"].iloc[2])


def test_a_file_without_the_trailing_label(tmp_path: Path) -> None:
    path = tmp_path / "plain.csv"
    path.write_text("Date,Depth\n44784.15,0.5\n44784.16,0.7\n")
    df = read_tag_csv(path)
    assert list(df.columns) == ["Date", "Depth"] and df["Depth"].tolist() == [0.5, 0.7]
