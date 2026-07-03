"""Tests for pre-flight certification gate."""

from bastion_config_certification import PreflightCertification
from bastion_config_certification.preflight import GateStatus


def test_preflight_passes_when_all_checks_pass():
    gate = PreflightCertification()
    gate.add_check("structure", lambda: (GateStatus.PASS, "OK"))
    gate.add_check("config", lambda: (GateStatus.PASS, "OK"))
    assert gate.passed
    assert not gate.failed
    assert gate.summary()["total"] == 2


def test_preflight_fails_on_any_failure():
    gate = PreflightCertification()
    gate.add_check("structure", lambda: (GateStatus.PASS, "OK"))
    gate.add_check("mt5", lambda: (GateStatus.FAIL, "No connection"))
    assert not gate.passed
    assert gate.failed
