# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Record iteration and result collection that keep a long deployment in bounded memory.

A tag record held as a Python dict costs about 1 kB, so a 3.5 million row deployment held
whole as dicts (the input, then one result per row) needs well over 10 GB. These helpers
build the dicts a chunk at a time and keep results as columnar frames.
"""

from collections.abc import Iterator
from typing import Any, cast

import pandas as pd

CHUNK_ROWS = 100_000


def iter_records(df: pd.DataFrame, chunk_rows: int = CHUNK_ROWS) -> Iterator[dict[str, Any]]:
    """Yields the rows of ``df`` as ``df.to_dict("records")`` would, a chunk at a time."""
    for start in range(0, len(df), chunk_rows):
        for record in df.iloc[start : start + chunk_rows].to_dict("records"):
            yield cast("dict[str, Any]", record)


class ResultFrames:
    """Collects per-record result dicts into DataFrame chunks.

    ``frame()`` returns what ``pd.DataFrame(results)`` would for the same dicts, while only
    ``chunk_rows`` of them exist as dicts at any time.
    """

    def __init__(self, chunk_rows: int = CHUNK_ROWS) -> None:
        self.chunk_rows = chunk_rows
        self._pending: list[dict[str, Any]] = []
        self._frames: list[pd.DataFrame] = []
        self._count = 0

    def append(self, result: dict[str, Any]) -> None:
        self._pending.append(result)
        self._count += 1
        if len(self._pending) >= self.chunk_rows:
            self._flush()

    def _flush(self) -> None:
        if self._pending:
            self._frames.append(pd.DataFrame(self._pending))
            self._pending = []

    def __len__(self) -> int:
        return self._count

    def frame(self) -> pd.DataFrame:
        self._flush()
        if not self._frames:
            empty: pd.DataFrame = pd.DataFrame()
            return empty
        if len(self._frames) == 1:
            return self._frames[0]
        # A column that is all None in one chunk is object there; infer_objects restores the
        # dtype a single DataFrame of all the dicts would have.
        df: pd.DataFrame = pd.concat(self._frames, ignore_index=True, sort=False).infer_objects()
        self._frames = [df]
        return df
