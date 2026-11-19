# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Chunked record iteration and result collection match the whole-list versions."""

from typing import Any, cast

import numpy as np
import pandas as pd
import pytest

from biologger_sim.io.records import ResultFrames, iter_records


def _input() -> pd.DataFrame:
    n = 23
    df: pd.DataFrame = pd.DataFrame(
        {
            "timestamp": np.arange(n, dtype=np.float64) / 16,
            "X_Accel_raw": np.linspace(-1, 1, n),
            "Depth": np.where(np.arange(n) % 5 == 0, np.nan, np.arange(n) * 0.5),
            "count": np.arange(n),
            "tag": ["a"] * n,
        }
    )
    return df


def _results() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for i in range(23):
        r: dict[str, Any] = {"timestamp": float(i), "pitch_degrees": np.float64(i * 0.1)}
        if i >= 4:  # a column that appears late, as heading does
            r["heading_degrees"] = np.float64(i)
        r["clock_drift_sec"] = None if i < 10 else float(i)  # all None in the first chunks
        r["flag"] = bool(i % 2)
        out.append(r)
    return out


@pytest.mark.parametrize("chunk", [1, 4, 7, 23, 100])
def test_iter_records_matches_to_dict(chunk: int) -> None:
    df = _input()
    got = list(iter_records(df, chunk_rows=chunk))
    want = cast("list[dict[str, Any]]", df.to_dict("records"))
    assert len(got) == len(want)
    for g, w in zip(got, want, strict=True):
        assert g.keys() == w.keys()
        for k in w:
            assert type(g[k]) is type(w[k])
            assert g[k] == w[k] or (np.isnan(g[k]) and np.isnan(w[k]))


@pytest.mark.parametrize("chunk", [1, 4, 7, 23, 100])
def test_result_frames_match_one_dataframe(chunk: int) -> None:
    results = _results()
    frames = ResultFrames(chunk_rows=chunk)
    for r in results:
        frames.append(r)
    assert len(frames) == len(results)
    pd.testing.assert_frame_equal(frames.frame(), pd.DataFrame(results))
    # frame() can be called again
    pd.testing.assert_frame_equal(frames.frame(), pd.DataFrame(results))


def test_empty() -> None:
    frames = ResultFrames()
    assert not frames
    assert frames.frame().empty
    assert list(iter_records(pd.DataFrame())) == []
