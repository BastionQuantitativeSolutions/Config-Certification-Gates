"""Tests for the configuration validator."""

import pytest

from bastion_config_certification import validate_config
from bastion_config_certification.conflict import ConflictType


@pytest.fixture
def reference_config():
    return {
        "single_source_of_truth": True,
        "version": "1.0.0",
        "risk": {
            "base_risk_per_trade": 0.005,
            "max_risk_per_trade": 0.0075,
            "daily_drawdown_limit": 0.03,
        },
        "entry_thresholds": {
            "buy_threshold": 0.53,
            "sell_threshold": 0.47,
        },
        "symbols": ["EURUSD", "GBPUSD"],
        "timeframes": ["M1", "M5", "M15"],
    }


def test_valid_config(reference_config):
    result = validate_config(reference_config, reference_config, config_version="1.0.0")
    assert result.is_valid
    assert len(result.conflicts) == 0


def test_missing_required_section(reference_config):
    runtime = {k: v for k, v in reference_config.items() if k != "risk"}
    result = validate_config(runtime, reference_config, config_version="1.0.0")
    assert not result.is_valid
    assert any(c.conflict_type == ConflictType.MISSING_VALUE for c in result.conflicts)


def test_risk_drift(reference_config):
    runtime = reference_config.copy()
    runtime["risk"] = reference_config["risk"].copy()
    runtime["risk"]["base_risk_per_trade"] = 0.02  # 4x reference
    result = validate_config(runtime, reference_config, config_version="1.0.0")
    assert not result.is_valid
    assert any(c.conflict_type == ConflictType.INVALID_RANGE for c in result.conflicts)


def test_missing_single_source_of_truth_warning(reference_config):
    runtime = reference_config.copy()
    runtime["single_source_of_truth"] = False
    result = validate_config(runtime, reference_config, config_version="1.0.0")
    assert result.is_valid
    assert any("single_source_of_truth" in w for w in result.warnings)
