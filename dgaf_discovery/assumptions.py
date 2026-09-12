from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class EvidenceValidityClass(str, Enum):
    IMMUTABLE = "IMMUTABLE"
    VERSION_BOUND = "VERSION_BOUND"
    CONFIGURATION_BOUND = "CONFIGURATION_BOUND"
    ENVIRONMENT_BOUND = "ENVIRONMENT_BOUND"
    TEMPORAL = "TEMPORAL"


@dataclass(frozen=True)
class AssumptionRecord:
    assumption_id: str
    statement: str
    evidence_refs: tuple[str, ...]
    validity_class: EvidenceValidityClass
    invalidation_triggers: tuple[str, ...]
    falsification_test: str
    revalidate_after: str | None = None
    authoritative_effect: str = "NONE"


@dataclass(frozen=True)
class ExpiryAssessment:
    expired: bool
    reasons: tuple[str, ...]


def _parse_deadline(value: str) -> datetime:
    deadline = datetime.fromisoformat(value)
    if deadline.tzinfo is None:
        raise ValueError("revalidate_after must be timezone-aware")
    return deadline


def validate_assumption(record: AssumptionRecord) -> None:
    errors: list[str] = []
    if not record.assumption_id.strip():
        errors.append("assumption_id is required")
    if not record.statement.strip():
        errors.append("statement is required")
    if not record.evidence_refs:
        errors.append("at least one evidence_ref is required")
    if not record.falsification_test.strip():
        errors.append("falsification_test is required")
    if record.authoritative_effect != "NONE":
        errors.append("assumption records cannot have authoritative effect")
    if not isinstance(record.validity_class, EvidenceValidityClass):
        errors.append("validity_class must be EvidenceValidityClass")
    trigger_bound = {
        EvidenceValidityClass.VERSION_BOUND,
        EvidenceValidityClass.CONFIGURATION_BOUND,
        EvidenceValidityClass.ENVIRONMENT_BOUND,
    }
    if record.validity_class in trigger_bound and not record.invalidation_triggers:
        errors.append("trigger-bound assumptions require at least one invalidation_trigger")
    if record.validity_class is EvidenceValidityClass.TEMPORAL:
        if record.revalidate_after is None:
            errors.append("temporal assumptions require revalidate_after")
        else:
            try:
                _parse_deadline(record.revalidate_after)
            except ValueError as exc:
                errors.append(str(exc))
    elif record.revalidate_after is not None:
        errors.append("revalidate_after is only valid for TEMPORAL evidence")
    if errors:
        raise ValueError("; ".join(errors))


def assess_expiry(
    record: AssumptionRecord,
    observed_triggers: set[str],
    now: datetime | None = None,
) -> ExpiryAssessment:
    validate_assumption(record)
    reasons: list[str] = []
    if record.validity_class is not EvidenceValidityClass.IMMUTABLE:
        reasons.extend(trigger for trigger in record.invalidation_triggers if trigger in observed_triggers)
    if record.validity_class is EvidenceValidityClass.TEMPORAL:
        current = now or datetime.now(timezone.utc)
        deadline = _parse_deadline(record.revalidate_after or "")
        if current >= deadline:
            reasons.append("revalidation_deadline_reached")
    return ExpiryAssessment(expired=bool(reasons), reasons=tuple(reasons))
