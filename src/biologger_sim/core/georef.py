# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""Georeferencing for tag deployments: position fixes and a local north/east frame.

Positions in the simulator are north and east metres from an origin (the start fix). This
module holds the fixes read from ``biologger_meta.csv`` and converts between that local frame
and latitude/longitude with an equirectangular approximation, which is accurate to well under
0.1 % over the tens of kilometres a deployment covers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone

EARTH_RADIUS_M = 6371000.0

# Metadata time formats seen in biologger_meta.csv: ISO 8601 for start_location_time,
# spreadsheet style (m/d/yy H:M) for time_start_utc and time_end_utc.
_TIME_FORMATS = ("%m/%d/%y %H:%M", "%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M")


def parse_utc(value: str | None) -> float | None:
    """Parses a metadata timestamp as UTC and returns Unix seconds, or None if empty."""
    if value is None:
        return None
    text = value.strip()
    if not text or text.upper() in ("NA", "TBD", "N/A"):
        return None
    try:
        iso = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if iso.tzinfo is None:
            iso = iso.replace(tzinfo=timezone.utc)
        return iso.timestamp()
    except ValueError:
        pass
    for fmt in _TIME_FORMATS:
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc).timestamp()
        except ValueError:
            continue
    return None


def parse_float(value: str | None) -> float | None:
    """Parses an optional float field; empty, NA and non-numeric values give None."""
    if value is None or not value.strip():
        return None
    try:
        return float(value)
    except ValueError:
        return None


@dataclass(frozen=True)
class GeoFix:
    """A known position of the animal at a time (Unix seconds, UTC)."""

    t: float
    lat: float
    lon: float


@dataclass(frozen=True)
class GeoReference:
    """Origin and position fixes for one deployment.

    The origin is the start fix. ``end`` is None when only a deployment position is known.
    """

    start: GeoFix
    end: GeoFix | None = None

    @property
    def origin(self) -> tuple[float, float]:
        return (self.start.lat, self.start.lon)

    def to_ne(self, lat: float, lon: float) -> tuple[float, float]:
        """Latitude/longitude to (north, east) metres from the origin."""
        north = math.radians(lat - self.start.lat) * EARTH_RADIUS_M
        east = (
            math.radians(lon - self.start.lon)
            * EARTH_RADIUS_M
            * math.cos(math.radians(self.start.lat))
        )
        return north, east

    def to_latlon(self, north: float, east: float) -> tuple[float, float]:
        """(north, east) metres from the origin to latitude/longitude."""
        lat = self.start.lat + math.degrees(north / EARTH_RADIUS_M)
        cos_lat = math.cos(math.radians(self.start.lat))
        lon = self.start.lon + (
            0.0 if abs(cos_lat) < 1e-9 else math.degrees(east / (EARTH_RADIUS_M * cos_lat))
        )
        return lat, lon

    def end_ne(self) -> tuple[float, float] | None:
        """The end fix in (north, east) metres, or None without an end fix."""
        if self.end is None:
            return None
        return self.to_ne(self.end.lat, self.end.lon)


def georeference_from_row(row: dict[str, str]) -> GeoReference | None:
    """Builds a GeoReference from one biologger_meta.csv row, or None without a start fix.

    The start time is ``start_location_time`` (the fix itself), falling back to
    ``time_start_utc``; the end fix uses ``end_lat``/``end_lon`` at ``time_end_utc``.
    """
    lat = parse_float(row.get("start_lat") or row.get("lat"))
    lon = parse_float(row.get("start_lon") or row.get("lon"))
    t0 = parse_utc(row.get("start_location_time")) or parse_utc(row.get("time_start_utc"))
    if lat is None or lon is None or t0 is None or (lat == 0.0 and lon == 0.0):
        return None
    start = GeoFix(t0, lat, lon)

    end_lat = parse_float(row.get("end_lat"))
    end_lon = parse_float(row.get("end_lon"))
    t1 = parse_utc(row.get("time_end_utc"))
    end = None
    if end_lat is not None and end_lon is not None and t1 is not None and t1 > t0:
        end = GeoFix(t1, end_lat, end_lon)
    return GeoReference(start=start, end=end)
