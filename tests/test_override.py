"""Tests for manual override audit."""

import pytest

from bastion_config_certification import ManualOverrideAudit
from bastion_config_certification.override import CONSENT_PHRASE


def test_override_requires_exact_consent():
    audit = ManualOverrideAudit()
    with pytest.raises(ValueError):
        audit.request_override(
            operator="operator_1",
            reason="Emergency launch",
            parameter_path="risk.base_risk_per_trade",
            previous_value="0.005",
            new_value="0.01",
            consent_phrase="resume normal live",  # wrong case
        )


def test_override_records_with_exact_consent():
    audit = ManualOverrideAudit()
    record = audit.request_override(
        operator="operator_1",
        reason="Emergency launch",
        parameter_path="risk.base_risk_per_trade",
        previous_value="0.005",
        new_value="0.01",
        consent_phrase=CONSENT_PHRASE,
    )
    assert record.operator == "operator_1"
    assert record.consent_phrase == CONSENT_PHRASE
    assert len(audit.records) == 1
