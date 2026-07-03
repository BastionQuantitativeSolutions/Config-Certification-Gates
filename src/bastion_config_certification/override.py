"""Manual override audit for safety-critical configuration changes."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


CONSENT_PHRASE = "RESUME NORMAL LIVE"


@dataclass
class OverrideRecord:
    """A permanent record of a manual override decision."""

    timestamp: str
    operator: str
    reason: str
    consent_phrase: str
    parameter_path: str
    previous_value: str
    new_value: str


class ManualOverrideAudit:
    """Enforce typed consent and immutable logging for manual overrides."""

    def __init__(self, records: Optional[List[OverrideRecord]] = None) -> None:
        self._records: List[OverrideRecord] = records or []

    def request_override(
        self,
        operator: str,
        reason: str,
        parameter_path: str,
        previous_value: str,
        new_value: str,
        consent_phrase: str,
    ) -> OverrideRecord:
        """Record an override only if the exact consent phrase is provided.

        Raises:
            ValueError: If the consent phrase does not match the required phrase.
        """
        if consent_phrase != CONSENT_PHRASE:
            raise ValueError(
                f"Override rejected. Typed consent must be exactly: {CONSENT_PHRASE!r}"
            )

        record = OverrideRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            operator=operator,
            reason=reason,
            consent_phrase=consent_phrase,
            parameter_path=parameter_path,
            previous_value=previous_value,
            new_value=new_value,
        )
        self._records.append(record)
        return record

    @property
    def records(self) -> List[OverrideRecord]:
        """Return an immutable view of override records."""
        return list(self._records)
