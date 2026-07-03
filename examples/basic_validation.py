"""Example: validate a unified trading config against a reference."""

from bastion_config_certification import validate_config

REFERENCE = {
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

RUNTIME = {
    "single_source_of_truth": True,
    "version": "1.0.1",
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

if __name__ == "__main__":
    result = validate_config(RUNTIME, REFERENCE, config_version="1.0.1")
    print(f"Valid: {result.is_valid}")
    print(f"Conflicts: {len(result.conflicts)}")
    for conflict in result.conflicts:
        print(f"  - {conflict.parameter_path}: {conflict.message}")
