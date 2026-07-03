"""Configuration conflict data model."""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, List, Optional


class ConflictType(str, Enum):
    """Categories of configuration conflict."""

    THRESHOLD_MISMATCH = "threshold_mismatch"
    MISSING_VALUE = "missing_value"
    INVALID_RANGE = "invalid_range"
    DEPRECATED_USAGE = "deprecated_usage"
    DUPLICATE_CONFIG = "duplicate_config"
    DRIFT = "drift"


@dataclass
class ConfigConflict:
    """A single configuration conflict with actionable metadata."""

    conflict_type: ConflictType
    file_path: str
    parameter_path: str
    expected_value: Any
    actual_value: Any
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    message: str
    resolution: str = ""


@dataclass
class ValidationResult:
    """Outcome of a configuration validation run."""

    is_valid: bool
    conflicts: List[ConfigConflict]
    warnings: List[str]
    timestamp: str
    config_version: str

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()
