"""Framework-neutral Assurance Profiles v0 primitives.

This module extracts reusable assurance mechanics from AOSS without importing
Stage-A comparator, endpoint, statistical, collection-authorization, or
scientific-promotion semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Mapping


class DerivationClass(str, Enum):
    DIRECT = "DIRECT"
    DERIVED = "DERIVED"
    UNMEASURED = "UNMEASURED"
    NOT_ESTABLISHED = "NOT_ESTABLISHED"


class PredicateStatus(str, Enum):
    BOUND = "BOUND"
    PASS = "PASS"
    BLOCKED = "BLOCKED"
    UNMEASURED = "UNMEASURED"
    NOT_ESTABLISHED = "NOT_ESTABLISHED"


class ReviewFinding(str, Enum):
    VERIFIED = "VERIFIED"
    NOT_VERIFIED = "NOT_VERIFIED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class SourceBinding:
    repository: str
    revision: str
    source_schema: str | None = None
    runtime_identity: str | None = None
    environment_identity: str | None = None
    executable_identity: str | None = None
    destination_identity: str | None = None

    def __post_init__(self) -> None:
        if not self.repository.strip():
            raise ValueError("repository must be non-empty")
        if not self.revision.strip():
            raise ValueError("revision must be non-empty")


@dataclass(frozen=True)
class MeasurementField:
    name: str
    derivation: DerivationClass
    value: Any = None
    source_field: str | None = None
    unit: str | None = None
    tolerance: str | None = None
    freshness_state: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("measurement field name must be non-empty")
        if self.derivation in {DerivationClass.UNMEASURED, DerivationClass.NOT_ESTABLISHED}:
            if self.value is not None:
                raise ValueError("unmeasured/not-established fields cannot carry a measured value")
        if self.derivation is DerivationClass.DIRECT and not self.source_field:
            raise ValueError("DIRECT measurement requires source_field")


@dataclass(frozen=True)
class MeasurementContract:
    source: SourceBinding
    fields: tuple[MeasurementField, ...]
    non_inference_rules: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.fields:
            raise ValueError("measurement contract requires at least one field")
        names = [field.name for field in self.fields]
        if len(set(names)) != len(names):
            raise ValueError("measurement field names must be unique")


@dataclass(frozen=True)
class ReplayContract:
    required_digest_roles: tuple[str, ...]
    required_verification_fields: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.required_digest_roles:
            raise ValueError("replay contract requires digest roles")
        if not self.required_verification_fields:
            raise ValueError("replay contract requires verification fields")


@dataclass(frozen=True)
class ReplayReceipt:
    source: SourceBinding
    digests: Mapping[str, str]
    verifications: Mapping[str, bool | None]
    replay_environment: Mapping[str, str]


@dataclass(frozen=True)
class ReadinessPredicate:
    predicate_id: str
    status: PredicateStatus
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.predicate_id.strip():
            raise ValueError("predicate_id must be non-empty")


@dataclass(frozen=True)
class ExternalReviewDisclosure:
    reviewer_identity: str
    relationship_disclosure: str
    independence_finding: ReviewFinding
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.reviewer_identity.strip():
            raise ValueError("reviewer_identity must be non-empty")
        if not self.relationship_disclosure.strip():
            raise ValueError("relationship_disclosure must be non-empty")


@dataclass(frozen=True)
class ExternalReviewReceipt:
    disclosure: ExternalReviewDisclosure
    source: SourceBinding
    finding: ReviewFinding
    retained_evidence_refs: tuple[str, ...] = ()
    local_acceptance_executed: bool = False
    authorization_effect: str = "NONE"


@dataclass(frozen=True)
class AssuranceProfile:
    profile_id: str
    measurement: MeasurementContract
    replay: ReplayContract
    readiness: tuple[ReadinessPredicate, ...]
    non_effects: tuple[str, ...] = (
        "NO_EXECUTION_AUTHORITY",
        "NO_SCIENTIFIC_N_INCREMENT",
        "NO_EFFICACY_EFFECT",
    )

    def __post_init__(self) -> None:
        if not self.profile_id.strip():
            raise ValueError("profile_id must be non-empty")
        if not self.readiness:
            raise ValueError("profile requires at least one readiness predicate")


@dataclass(frozen=True)
class AssuranceDecision:
    status: str
    reasons: tuple[str, ...]
    authorization_effect: str = "NONE"
    execution_effect: str = "NONE"
    scientific_n_increment: int = 0
    efficacy_effect: str = "NONE"

    @property
    def pass_(self) -> bool:
        return self.status == "PASS"

    def to_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def evaluate_replay(contract: ReplayContract, receipt: ReplayReceipt) -> AssuranceDecision:
    reasons: list[str] = []

    for role in contract.required_digest_roles:
        digest = receipt.digests.get(role)
        if digest is None:
            reasons.append(f"MISSING_DIGEST:{role}")
        elif len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            reasons.append(f"INVALID_DIGEST:{role}")

    for field in contract.required_verification_fields:
        value = receipt.verifications.get(field)
        if value is not True:
            reasons.append(f"VERIFICATION_NOT_TRUE:{field}")

    return AssuranceDecision(
        status="PASS" if not reasons else "BLOCKED",
        reasons=tuple(reasons),
    )


def evaluate_readiness(predicates: tuple[ReadinessPredicate, ...]) -> AssuranceDecision:
    reasons: list[str] = []
    for predicate in predicates:
        if predicate.status not in {PredicateStatus.BOUND, PredicateStatus.PASS}:
            reasons.append(f"READINESS_{predicate.status.value}:{predicate.predicate_id}")

    return AssuranceDecision(
        status="PASS" if not reasons else "BLOCKED",
        reasons=tuple(reasons),
    )


def evaluate_external_review(receipt: ExternalReviewReceipt) -> AssuranceDecision:
    reasons: list[str] = []

    if receipt.disclosure.independence_finding is not ReviewFinding.VERIFIED:
        reasons.append(f"INDEPENDENCE_{receipt.disclosure.independence_finding.value}")
    if receipt.finding is not ReviewFinding.VERIFIED:
        reasons.append(f"REVIEW_{receipt.finding.value}")
    if receipt.local_acceptance_executed:
        reasons.append("LOCAL_ACCEPTANCE_MUST_BE_SEPARATE")
    if receipt.authorization_effect != "NONE":
        reasons.append("EXTERNAL_REVIEW_CANNOT_GRANT_AUTHORIZATION")

    return AssuranceDecision(
        status="PASS" if not reasons else "BLOCKED",
        reasons=tuple(reasons),
    )
