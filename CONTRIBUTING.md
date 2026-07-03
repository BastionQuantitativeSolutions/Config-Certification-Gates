# Contributing

Thank you for your interest in Bastion's open-source utilities.

## Scope

This repository publishes **configuration certification methodology**, not live trading parameters. Please do not submit PRs that:

- Expose real threshold values, model weights, or broker credentials.
- Add dependencies on proprietary or cloud-only services.
- Bypass deterministic validation for convenience.

## How to contribute

1. Open an issue describing the bug or enhancement.
2. Fork the repository and create a feature branch.
3. Add tests for any new functionality.
4. Run `pytest` and `ruff` locally.
5. Submit a PR referencing the issue.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
ruff check .
```

## Code style

- Python 3.10+ type hints.
- Max line length: 100.
- Deterministic, side-effect-free validation functions are preferred.
