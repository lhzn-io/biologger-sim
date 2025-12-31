# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""
Streaming utility functions for microsecond-precision datetime handling and Excel date conversion.
"""

__all__ = [
    "excel_date_to_datetime_ns",
    "format_datetime_iso8601_micro",
]

import datetime


def excel_date_to_datetime_ns(excel_date: float | int) -> tuple[datetime.datetime, int]:
    """
    Convert an Excel serial date (float) to a UTC datetime.datetime object and nanosecond remainder.
    Returns (datetime.datetime, nanosecond_remainder).
    """
    if not isinstance(excel_date, float | int):
        raise TypeError("excel_date must be a float or int")
    # Excel epoch is 1899-12-30
    base = datetime.datetime(1899, 12, 30, tzinfo=datetime.timezone.utc)
    total_seconds = excel_date * 86400.0
    int_seconds = int(total_seconds)
    microseconds = int((total_seconds - int_seconds) * 1_000_000)
    nanoseconds = round((total_seconds - int_seconds) * 1_000_000_000) % 1000
    dt = base + datetime.timedelta(seconds=int_seconds, microseconds=microseconds)
    return dt, nanoseconds


def format_datetime_iso8601_micro(dt: datetime.datetime) -> str:
    """
    Format a datetime.datetime object as ISO 8601 with microsecond precision and trailing Z.
    """
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
