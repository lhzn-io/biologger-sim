# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class BiologgerProcessor(ABC):
    """
    Abstract base interface for biologger data processors.

    This interface defines the standard contract that all biologger processing
    pipelines should implement, enabling consistent usage patterns across
    batch, streaming, and adaptive sensor fusion processors.

    Design Principles:
    - Unified processing interface via process() method
    - Standardized configuration and state management
    - Consistent performance monitoring and telemetry
    - Flexible input/output for different data types
    - Runtime reconfiguration support
    """

    @abstractmethod
    def process(self, data: dict[str, Any] | np.ndarray) -> dict[str, Any]:
        """
        Process input data through the pipeline.

        This is the main processing method that all processors must implement.
        The input format is flexible to support different processor types:
        - Streaming: Dict with sensor records (accel, mag, depth, etc.)
        - Adaptive: np.ndarray with accelerometer samples
        - Batch: Dict with full dataset parameters

        Args:
            data: Input data - format depends on processor type

        Returns:
            Dict containing processed results and metadata

        Raises:
            ProcessingError: If processing fails due to invalid input or internal error
        """

    @abstractmethod
    def reset(self) -> None:
        """
        Reset processor to initial state.

        Clears all internal buffers, calibration state, and accumulated
        statistics while preserving configuration settings.
        """

    @abstractmethod
    def get_performance_summary(self) -> dict[str, Any]:
        """
        Get comprehensive performance metrics and telemetry.

        Returns:
            Dict containing timing statistics, throughput metrics,
            algorithm performance, and diagnostic information
        """

    @abstractmethod
    def update_config(self, config_updates: dict[str, Any]) -> None:
        """
        Update processor configuration at runtime.

        Args:
            config_updates: Dictionary of configuration parameters to update

        Raises:
            ConfigurationError: If configuration update is invalid
        """

    @abstractmethod
    def get_current_state(self) -> dict[str, Any]:
        """
        Get current processor state and internal parameters.

        Returns:
            Dict containing current state information, calibration status,
            buffer contents, and algorithm-specific diagnostics
        """

    def get_output_schema(self) -> list[str]:
        """
        Get list of output field names produced by process().

        Default implementation returns empty list. Processors should
        override this to provide schema information for output validation.

        Returns:
            List of string field names in process() output
        """
        return []

    def validate_input(self, data: dict[str, Any] | np.ndarray) -> bool:
        """
        Validate input data format and content.

        Default implementation always returns True. Processors can
        override this for custom validation logic.

        Args:
            data: Input data to validate

        Returns:
            True if input is valid, False otherwise
        """
        return True

    def get_processor_info(self) -> dict[str, Any]:
        """
        Get processor metadata and capabilities.

        Returns:
            Dict containing processor type, version, supported features,
            and configuration parameters
        """
        return {
            "processor_type": self.__class__.__name__,
            "version": getattr(self, "version", "1.0.0"),
            "supports_realtime": getattr(self, "supports_realtime", False),
            "supports_batch": getattr(self, "supports_batch", False),
            "required_sensors": getattr(self, "required_sensors", []),
        }


class ProcessingError(Exception):
    """Exception raised during data processing."""


class ConfigurationError(Exception):
    """Exception raised for invalid configuration updates."""
