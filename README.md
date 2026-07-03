# Config-Certification-Gates

Deterministic configuration certification gates for algorithmic trading systems.

## What it is

This repository contains the sanitized reference implementation of the config
certification pattern used by Cavalier:

- **Single source of truth enforcement** — warn when a config is not explicitly
  marked as authoritative.
- **Structured conflict reporting** — every mismatch carries a severity, path,
  expected/actual value, and resolution hint.
- **Range validation** — detect when runtime risk parameters drift outside the
  authorized envelope.
- **Config drift detection** — recursively compare runtime config against a
  reference manifest.
- **Manual override audit** — require an exact typed consent phrase and produce
  a permanent, timestamped record.
- **Pre-flight certification gate** — compose readiness checks before allowing
  a system launch.

## What it is not

This repo does **not** contain:

- Live threshold values for any trading system.
- Broker integration logic.
- Model weights or signal parameters.
- Real account credentials.

## Installation

```bash
pip install bastion-config-certification
```

Or install from source:

```bash
git clone https://github.com/BastionQuantitativeSolutions/Config-Certification-Gates.git
cd Config-Certification-Gates
pip install -e ".[dev]"
```

## Quick start

```python
from bastion_config_certification import validate_config

reference = {
    "single_source_of_truth": True,
    "risk": {
        "base_risk_per_trade": 0.005,
        "max_risk_per_trade": 0.0075,
    },
    "entry_thresholds": {"buy_threshold": 0.53, "sell_threshold": 0.47},
    "symbols": ["EURUSD", "GBPUSD"],
    "timeframes": ["M1", "M5"],
}

runtime = {
    "single_source_of_truth": True,
    "risk": {
        "base_risk_per_trade": 0.005,
        "max_risk_per_trade": 0.015,  # drift!
    },
    "entry_thresholds": {"buy_threshold": 0.53, "sell_threshold": 0.47},
    "symbols": ["EURUSD", "GBPUSD"],
    "timeframes": ["M1", "M5"],
}

result = validate_config(runtime, reference, config_version="1.0.1")
print(result.is_valid)  # False
for c in result.conflicts:
    print(c.parameter_path, c.message)
```

## Manual override audit

```python
from bastion_config_certification import ManualOverrideAudit

audit = ManualOverrideAudit()
audit.request_override(
    operator="operator_1",
    reason="Emergency launch after certification warning",
    parameter_path="risk.max_risk_per_trade",
    previous_value="0.0075",
    new_value="0.015",
    consent_phrase="RESUME NORMAL LIVE",
)

for record in audit.records:
    print(record.timestamp, record.operator, record.reason)
```

## Repository structure

```
Config-Certification-Gates/
├── src/bastion_config_certification/
│   ├── __init__.py
│   ├── conflict.py          # ConflictType, ConfigConflict, ValidationResult
│   ├── validator.py         # validate_config()
│   ├── override.py          # ManualOverrideAudit
│   └── preflight.py         # PreflightCertification gate
├── tests/
├── examples/
├── .github/workflows/ci.yml
├── pyproject.toml
├── LICENSE
├── CHANGELOG.md
└── CONTRIBUTING.md
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## License

MIT — see [LICENSE](LICENSE).

---

_For the broader validation framework, see_
[BastionQuantitativeSolutions/Validation-Framework](https://github.com/BastionQuantitativeSolutions/Validation-Framework).
