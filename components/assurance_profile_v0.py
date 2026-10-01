"""Framework-neutral Assurance Profile v0 evaluator.

This module evaluates a declared assurance profile across six independent
dimensions. It is deliberately non-authorizing and non-certifying.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional

ASSURANCE_PROFILE_SCHEMA_VERSION = "assurance-profile.v0-candidate"
AUTHORIZATION_EFFECT_NONE = "NONE"
CERTIFICATION_EFFECT_NONE = "NONE"


class DimensionStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class IndependenceClass(str, Enum):
    SAME_SYSTEM = "SAME_SYSTEM"
    INDEPENDENT_VERIFIED = "INDEPENDENT_VERIFIED"
    INDEPENDENT_UNVERIFIED = "INDEPENDENT_UNVERIFIED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class DimensionAssessment:
    status: DimensionStatus
    required: bool
    evidence_refs: tuple[str, ...] = ()
    limitation: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, DimensionStatus):
            raise ValueError("status must be DimensionStatus")
        if self.required and self.status is DimensionStatus.NOT_APPLICABLE:
            raise ValueError("required dimensions cannot be NOT_APPLICABLE")


@dataclass(frozen=True)
class AssuranceProfileInput:
    profile_id: str
    profile_version: str
    target_system: str
    source_identity: str
    runtime_identity: str
    environment_identity: str
    material_source_manifest_ref: Optional[str]
    measurement_apparatus: DimensionAssessment
    runtime_source_environment_binding: DimensionAssessment
    authorization_decision_separation: DimensionAssessment
    custody_replay_integrity: DimensionAssessment
    readiness_preflight: DimensionAssessment
    trust_independence_review: DimensionAssessment
    independence_class: IndependenceClass
    claim_ceiling: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "profile_id",
            "profile_version",
            "target_system",
            "source_identity",
            "runtime_identity",
            "environment_identity",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must not be blank")
        if not isinstance(self.independence_class, IndependenceClass):
            raise ValueError("independence_class must be IndependenceClass")


@dataclass(frozen=True)
class AssuranceProfileReceipt:
    passed: bool
    profile_id: str
    profile_version: str
    target_system: str
    dimension_statuses: Mapping[str, str]
    unresolved_blockers: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    independence_class: IndependenceClass
    claim_ceiling: tuple[str, ...]
    authorization_effect: str = AUTHORIZATION_EFFECT_NONE
    certification_effect: str = CERTIFICATION_EFFECT_NONE
    schema_version: str = ASSURANCE_PROFILE_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.authorization_effect != AUTHORIZATION_EFFECT_NONE:
            raise ValueError("Assurance Profile never grants authorization")
        if self.certification_effect != CERTIFICATION_EFFECT_NONE:
            raise ValueError("Assurance Profile never grants certification")


_DIMENSIONS = (
    ("measurement_apparatus", "measurement/apparatus"),
    (
        "runtime_source_environment_binding",
        "runtime/source/environment binding",
    ),
    (
        "authorization_decision_separation",
        "authorization/decision separation",
    ),
    ("custody_replay_integrity", "custody/replay/integrity"),
    ("readiness_preflight", "readiness/preflight"),
    ("trust_independence_review", "trust/independence review"),
)


def evaluate_assurance_profile(profile: AssuranceProfileInput) -> AssuranceProfileReceipt:
    """Evaluate required profile dimensions without authorizing any action."""

    if not isinstance(profile, AssuranceProfileInput):
        raise TypeError("profile must be AssuranceProfileInput")

    statuses: dict[str, str] = {}
    blockers: list[str] = []
    evidence_refs: list[str] = []

    for attribute_name, display_name in _DIMENSIONS:
        assessment = getattr(profile, attribute_name)
        if not isinstance(assessment, DimensionAssessment):
            raise TypeError(f"{attribute_name} must be DimensionAssessment")

        statuses[display_name] = assessment.status.value
        evidence_refs.extend(assessment.evidence_refs)

        if assessment.required and assessment.status is not DimensionStatus.PASS:
            blockers.append(f"{display_name}:{assessment.status.value}")

    if (
        profile.trust_independence_review.required
        and profile.independence_class
        in (IndependenceClass.UNKNOWN, IndependenceClass.INDEPENDENT_UNVERIFIED)
    ):
        blockers.append(f"independence:{profile.independence_class.value}")

    return AssuranceProfileReceipt(
        passed=not blockers,
        profile_id=profile.profile_id,
        profile_version=profile.profile_version,
        target_system=profile.target_system,
        dimension_statuses=statuses,
        unresolved_blockers=tuple(blockers),
        evidence_refs=tuple(dict.fromkeys(evidence_refs)),
        independence_class=profile.independence_class,
        claim_ceiling=profile.claim_ceiling,
    )
