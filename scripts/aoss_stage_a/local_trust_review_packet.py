"""Inert local trust-review packet for AOSS Stage-A admission evidence.

This module prepares review material for local verification of reviewer
attribution and independence. It binds exact upstream records and retained
evidence identities, but it cannot execute the review or promote trust,
execution authority, collection readiness, or scientific N.
"""

from __future__ import annotations

import re
from typing import Any, Mapping, NoReturn, Sequence

from scripts.aoss_stage_a.external_admission_decision_intake import record_sha256
from scripts.aoss_stage_a.local_adjudication_candidate import (
    validate_local_adjudication_candidate,
)

RECORD_TYPE = "AOSS_V0_6_STAGE_A_LOCAL_TRUST_REVIEW_PACKET"
STATUS = "REVIEW_MATERIAL_RETAINED_NOT_ADJUDICATED"
EXPECTED_CONTROLLER_ISSUE = 901
_REQUIRED_ROLES = {"reviewer_attribution", "independence"}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class LocalTrustReviewPacketError(ValueError):
    """Raised when local trust-review material fails closed."""


def _fail(code: str) -> NoReturn:
    raise LocalTrustReviewPacketError(code)


def _nonempty(value: object, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(code)
    return value.strip()


def _sha256(value: object, code: str) -> str:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        _fail(code)
    return value


def _retained_evidence(
    evidence: Sequence[tuple[str, str, str]],
) -> list[dict[str, str]]:
    if len(evidence) != len(_REQUIRED_ROLES):
        _fail("LOCAL_TRUST_REVIEW_EVIDENCE_COUNT_INVALID")

    seen: set[str] = set()
    records: list[dict[str, str]] = []
    for role, source_uri, digest in evidence:
        if role not in _REQUIRED_ROLES:
            _fail("LOCAL_TRUST_REVIEW_EVIDENCE_ROLE_INVALID")
        if role in seen:
            _fail("LOCAL_TRUST_REVIEW_EVIDENCE_ROLE_DUPLICATE")
        seen.add(role)
        records.append(
            {
                "role": role,
                "source_uri": _nonempty(
                    source_uri,
                    "LOCAL_TRUST_REVIEW_EVIDENCE_URI_MISSING",
                ),
                "sha256": _sha256(
                    digest,
                    "LOCAL_TRUST_REVIEW_EVIDENCE_SHA_INVALID",
                ),
            }
        )

    if seen != _REQUIRED_ROLES:
        _fail("LOCAL_TRUST_REVIEW_EVIDENCE_ROLE_MISSING")
    return sorted(records, key=lambda item: item["role"])


def prepare_local_trust_review_packet(
    *,
    external_admission_intake: Mapping[str, Any],
    reverification_packet: Mapping[str, Any],
    reviewer_trust_intake: Mapping[str, Any],
    local_adjudication_candidate: Mapping[str, Any],
    retained_evidence: Sequence[tuple[str, str, str]],
) -> dict[str, object]:
    """Prepare retained local review material without executing adjudication."""

    report = validate_local_adjudication_candidate(
        local_adjudication_candidate,
        external_admission_intake=external_admission_intake,
        reverification_packet=reverification_packet,
        reviewer_trust_intake=reviewer_trust_intake,
    )
    if report["effective_disposition"] != "BLOCKED":
        _fail("LOCAL_TRUST_REVIEW_UPSTREAM_NOT_BLOCKED")

    evidence = _retained_evidence(retained_evidence)

    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": EXPECTED_CONTROLLER_ISSUE,
        "bindings": {
            "reviewer_trust_intake_sha256": record_sha256(reviewer_trust_intake),
            "local_adjudication_candidate_sha256": record_sha256(
                local_adjudication_candidate
            ),
        },
        "retained_evidence": evidence,
        "review_state": {
            "classification": "NOT_EXECUTED",
            "reviewer_identity": None,
            "reviewed_at": None,
            "fresh_cryptographic_verification": False,
            "reviewer_attribution_verified": False,
            "independence_verified": False,
        },
        "upstream_effective_disposition": "BLOCKED",
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }


def validate_local_trust_review_packet(
    packet: Mapping[str, Any],
    *,
    external_admission_intake: Mapping[str, Any],
    reverification_packet: Mapping[str, Any],
    reviewer_trust_intake: Mapping[str, Any],
    local_adjudication_candidate: Mapping[str, Any],
    retained_evidence: Sequence[tuple[str, str, str]],
) -> dict[str, object]:
    """Validate exact review material while requiring review state to stay inert."""

    report = validate_local_adjudication_candidate(
        local_adjudication_candidate,
        external_admission_intake=external_admission_intake,
        reverification_packet=reverification_packet,
        reviewer_trust_intake=reviewer_trust_intake,
    )
    if report["effective_disposition"] != "BLOCKED":
        _fail("LOCAL_TRUST_REVIEW_UPSTREAM_NOT_BLOCKED")

    if packet.get("record_type") != RECORD_TYPE:
        _fail("LOCAL_TRUST_REVIEW_RECORD_TYPE_MISMATCH")
    if packet.get("status") != STATUS:
        _fail("LOCAL_TRUST_REVIEW_STATUS_MISMATCH")
    if packet.get("controller_issue") != EXPECTED_CONTROLLER_ISSUE:
        _fail("LOCAL_TRUST_REVIEW_CONTROLLER_MISMATCH")

    bindings = packet.get("bindings")
    expected_bindings = {
        "reviewer_trust_intake_sha256": record_sha256(reviewer_trust_intake),
        "local_adjudication_candidate_sha256": record_sha256(
            local_adjudication_candidate
        ),
    }
    if not isinstance(bindings, Mapping) or dict(bindings) != expected_bindings:
        _fail("LOCAL_TRUST_REVIEW_BINDING_MISMATCH")

    expected_evidence = _retained_evidence(retained_evidence)
    if packet.get("retained_evidence") != expected_evidence:
        _fail("LOCAL_TRUST_REVIEW_EVIDENCE_MISMATCH")

    expected_review_state = {
        "classification": "NOT_EXECUTED",
        "reviewer_identity": None,
        "reviewed_at": None,
        "fresh_cryptographic_verification": False,
        "reviewer_attribution_verified": False,
        "independence_verified": False,
    }
    if packet.get("review_state") != expected_review_state:
        _fail("LOCAL_TRUST_REVIEW_PREMATURE_ADJUDICATION")

    boundary = {
        "upstream_effective_disposition": "BLOCKED",
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }
    for field, expected in boundary.items():
        if packet.get(field) != expected:
            _fail(f"LOCAL_TRUST_REVIEW_BOUNDARY_DRIFT_{field.upper()}")

    return {
        "record_type": "AOSS_STAGE_A_LOCAL_TRUST_REVIEW_PACKET_REPORT",
        "packet_validation": "PASS_REVIEW_MATERIAL_INERT",
        "retained_evidence_roles": sorted(_REQUIRED_ROLES),
        "review_classification": "NOT_EXECUTED",
        "reviewer_attribution_verified": False,
        "independence_verified": False,
        "effective_disposition": "BLOCKED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
