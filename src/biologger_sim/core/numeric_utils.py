# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import logging
from typing import Any


def safe_float(
    val: Any, field_name: str = "unknown", debug_level: int = 0, record_count: int | None = None
) -> float:
    """Safely convert value to float, returning NaN for invalid values."""
    try:
        if val == "" or val is None:
            if debug_level >= 2:
                logging.getLogger(__name__).debug(
                    f"[safe_float] Record {record_count}, Field '{field_name}': "
                    "Empty/None value -> NaN"
                )
            return float("nan")
        result = float(val)
        if result != result:
            if debug_level >= 2:
                logging.getLogger(__name__).debug(
                    f"[safe_float] Record {record_count}, Field '{field_name}': "
                    f"Value '{val}' resulted in NaN"
                )
            return float("nan")
        return result
    except (ValueError, TypeError) as e:
        if debug_level >= 2:
            logging.getLogger(__name__).warning(
                f"[safe_float] Record {record_count}, Field '{field_name}': "
                f"Failed to convert '{val}' to float: {e} -> NaN"
            )
        return float("nan")
    except Exception as e:
        if debug_level >= 2:
            logging.getLogger(__name__).error(
                f"[safe_float] Record {record_count}, Field '{field_name}': "
                f"Unexpected error converting '{val}': {e} -> NaN"
            )
        return float("nan")
