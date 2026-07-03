"""Pre-flight certification gate primitives.

A pre-flight gate blocks system launch until structural, config, data, and model
readiness checks pass. This module provides the framework; live thresholds and
broker checks are intentionally left to the caller.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List


class GateStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    CONDITIONAL = "CONDITIONAL"


@dataclass
class GateCheck:
    name: str
    status: GateStatus
    message: str


@dataclass
class PreflightCertification:
    """Composable pre-flight certification gate."""

    checks: List[GateCheck] = field(default_factory=list)

    def add_check(
        self,
        name: str,
        check_fn: Callable[[], tuple[GateStatus, str]],
    ) -> "PreflightCertification":
        """Run a check function and record the result."""
        status, message = check_fn()
        self.checks.append(GateCheck(name=name, status=status, message=message))
        return self

    @property
    def passed(self) -> bool:
        return all(c.status == GateStatus.PASS for c in self.checks)

    @property
    def failed(self) -> bool:
        return any(c.status == GateStatus.FAIL for c in self.checks)

    def summary(self) -> Dict[str, object]:
        return {
            "passed": self.passed,
            "failed": self.failed,
            "total": len(self.checks),
            "checks": [
                {"name": c.name, "status": c.status.value, "message": c.message}
                for c in self.checks
            ],
        }
