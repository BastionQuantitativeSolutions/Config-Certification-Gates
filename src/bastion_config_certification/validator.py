"""Configuration validator implementation.

This module validates a trading system's unified configuration against a set of
deterministic rules. It is a sanitized reference implementation: no live
thresholds, no broker logic, no model weights.
"""

from typing import Any, Dict, List

from .conflict import ConflictType, ConfigConflict, ValidationResult


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_config(
    config: Dict[str, Any],
    reference: Dict[str, Any],
    config_version: str = "unknown",
) -> ValidationResult:
    """Validate a runtime config against a reference schema/values.

    Args:
        config: The runtime configuration dictionary.
        reference: The authoritative reference dictionary.
        config_version: Semantic version or hash of the config under test.

    Returns:
        ValidationResult with all conflicts and warnings found.
    """
    conflicts: List[ConfigConflict] = []
    warnings: List[str] = []

    if not config.get("single_source_of_truth"):
        warnings.append("Config is NOT marked as single_source_of_truth!")

    # Required top-level sections
    required_sections = ["risk", "entry_thresholds", "symbols", "timeframes"]
    for section in required_sections:
        if section not in config:
            conflicts.append(
                ConfigConflict(
                    conflict_type=ConflictType.MISSING_VALUE,
                    file_path="runtime_config",
                    parameter_path=section,
                    expected_value="present",
                    actual_value="missing",
                    severity="CRITICAL",
                    message=f"Required section '{section}' is missing.",
                    resolution=f"Add the '{section}' section to the unified config.",
                )
            )

    # Value range checks against reference
    risk = config.get("risk", {})
    ref_risk = reference.get("risk", {})

    for key in ["base_risk_per_trade", "max_risk_per_trade", "daily_drawdown_limit"]:
        actual = risk.get(key)
        expected = ref_risk.get(key)
        if actual is None:
            conflicts.append(
                ConfigConflict(
                    conflict_type=ConflictType.MISSING_VALUE,
                    file_path="runtime_config",
                    parameter_path=f"risk.{key}",
                    expected_value=expected,
                    actual_value=None,
                    severity="HIGH",
                    message=f"Risk parameter '{key}' is missing.",
                    resolution=f"Set risk.{key} to the reference value.",
                )
            )
        elif expected is not None and _is_number(actual) and _is_number(expected):
            if actual > expected * 1.5 or actual < expected * 0.5:
                conflicts.append(
                    ConfigConflict(
                        conflict_type=ConflictType.INVALID_RANGE,
                        file_path="runtime_config",
                        parameter_path=f"risk.{key}",
                        expected_value=f"within 50% of {expected}",
                        actual_value=actual,
                        severity="HIGH",
                        message=f"Risk parameter '{key}' ({actual}) deviates from reference ({expected}).",
                        resolution="Review and align with the authorized risk envelope.",
                    )
                )

    # Drift check: any key in reference missing from runtime config
    def _check_drift(
        runtime: Dict[str, Any],
        auth: Dict[str, Any],
        path: str = "",
    ) -> None:
        for key, expected in auth.items():
            current_path = f"{path}.{key}" if path else key
            if key not in runtime:
                conflicts.append(
                    ConfigConflict(
                        conflict_type=ConflictType.DRIFT,
                        file_path="runtime_config",
                        parameter_path=current_path,
                        expected_value=expected,
                        actual_value="missing",
                        severity="MEDIUM",
                        message=f"Config drift: '{current_path}' exists in reference but not runtime.",
                        resolution="Re-sync runtime config with the unified reference.",
                    )
                )
            elif isinstance(expected, dict) and isinstance(runtime[key], dict):
                _check_drift(runtime[key], expected, current_path)

    _check_drift(config, reference)

    is_valid = not any(c.severity == "CRITICAL" for c in conflicts) and len(conflicts) == 0

    return ValidationResult(
        is_valid=is_valid,
        conflicts=conflicts,
        warnings=warnings,
        timestamp="",
        config_version=config_version,
    )
