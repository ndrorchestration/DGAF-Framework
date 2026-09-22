"""Blocked local-adjudication candidate for AOSS Stage-A admission evidence.

This module binds accepted external-admission, cryptographic reverification, and
reviewer-trust intake records into a local adjudication candidate. It does not
establish local reviewer trust, accept execution identities, enable collection,
or increment scientific N.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, NoReturn

from scripts.aoss_stage_a.external_admission_decision_intake import record_sha256
from scripts.aoss_stage_a.reviewer_trust_verification_intake import (
    validate_reviewer_trust_verification_intake,
)

RECORD_TYPE = "AOSS_V0_6_STAGE_A_LOCAL_ADJUDICATION_CANDIDATE"
STATUS = "BLOCKED_PENDING_LOCAL_TRUST_VERIFICATION"
EXPECTED_CONTROLLER_ISSUE = 901
_REQUESTED_DISPOSITIONS = {"ACCEPT", "REJECT", "BLOCKED"}


class LocalAdjudicationCandidateError(ValueError):
    """Raised when the local-adjudication candidate fails closed."""


def _fail(code: str) -> NoReturn:
    raise LocalAdjudicationCandidateError(code)


def _nonempty(value: object, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(code)
    return value.strip()


def _timestamp(value: object) -> str:
    timestamp = _nonempty(value, "LOCAL_ADJUDICATION_TIMESTAMP_MISSING")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        _fail("LOCAL_ADJUDICATION_TIMESTAMP_INVALID")
    if parsed.tzinfo is None:
        _fail("LOCAL_ADJUDICATION_TIMESTAMP_NOT_OFFSET_AWARE")
    return timestamp


def _derive_blockers(
    trust_intake: Mapping[str, Any],
) -> list[str]:
    verification = trust_intake.get("external_verification")
    if not isinstance(verification, Mapping):
        _fail("LOCAL_ADJUDICATION_EXTERNAL_VERIFICATION_MISSING")

    findings = verification.get("findings")
    if not isinstance(findings, Mapping):
        _fail("LOCAL_ADJUDICATION_EXTERNAL_FINDINGS_MISSING")

    blockers: list[str] = []
    if findings.get("reviewer_attribution") != "VERIFIED":
        blockers.append("EXTERNAL_REVIEWER_ATTRIBUTION_NOT_VERIFIED")
    if findings.get("independence") != "VERIFIED":
        blockers.append("EXTERNAL_INDEPENDENCE_NOT_VERIFIED")

    local_trust = trust_intake.get("local_trust_state")
    if not isinstance(local_trust, Mapping):
        _fail("LOCAL_ADJUDICATION_LOCAL_TRUST_STATE_MISSING")
    if local_trust.get("reviewer_attribution_verified") is not True:
        blockers.append("LOCAL_REVIEWER_ATTRIBUTION_NOT_VERIFIED")
    if local_trust.get("independence_verified") is not True:
        blockers.append("LOCAL_INDEPENDENCE_NOT_VERIFIED")

    return blockers


def prepare_local_adjudication_candidate(
    *,
    external_admission_intake: Mapping[str, Any],
    reverification_packet: Mapping[str, Any],
    reviewer_trust_intake: Mapping[str, Any],
    adjudicator_identity: str,
    adjudicated_at: str,
    requested_disposition: str,
) -> dict[str, object]:
    """Prepare a blocked local adjudication candidate without promotion."""

    validate_reviewer_trust_verification_intake(
        reviewer_trust_intake,
        external_admission_intake=external_admission_intake,
        reverification_packet=reverification_packet,
    )

    adjudicator = _nonempty(
        adjudicator_identity,
        "LOCAL_ADJUDICATION_ADJUDICATOR_IDENTITY_MISSING",
    )
    timestamp = _timestamp(adjudicated_at)
    if requested_disposition not in _REQUESTED_DISPOSITIONS:
        _fail("LOCAL_ADJUDICATION_REQUESTED_DISPOSITION_INVALID")

    blockers = _derive_blockers(reviewer_trust_intake)
    if not blockers:
        _fail("LOCAL_ADJUDICATION_UNBLOCKED_PATH_NOT_IMPLEMENTED")

    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": EXPECTED_CONTROLLER_ISSUE,
        "bindings": {
            "external_admission_intake_sha256": record_sha256(external_admission_intake),
            "reverification_packet_sha256": record_sha256(reverification_packet),
            "reviewer_trust_intake_sha256": record_sha256(reviewer_trust_intake),
        },
        "local_adjudication": {
            "adjudicator_identity": adjudicator,
            "adjudicated_at": timestamp,
            "requested_disposition": requested_disposition,
            "effective_disposition": "BLOCKED",
            "blockers": blockers,
        },
        "reviewer_attribution_verified": False,
        "independence_verified": False,
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }


def validate_local_adjudication_candidate(
    candidate: Mapping[str, Any],
    *,
    external_admission_intake: Mapping[str, Any],
    reverification_packet: Mapping[str, Any],
    reviewer_trust_intake: Mapping[str, Any],
) -> dict[str, object]:
    """Validate blocked local adjudication candidate and preserve fail-closed state."""

    validate_reviewer_trust_verification_intake(
        reviewer_trust_intake,
        external_admission_intake=external_admission_intake,
        reverification_packet=reverification_packet,
    )

    if candidate.get("record_type") != RECORD_TYPE:
        _fail("LOCAL_ADJUDICATION_RECORD_TYPE_MISMATCH")
    if candidate.get("status") != STATUS:
        _fail("LOCAL_ADJUDICATION_STATUS_MISMATCH")
    if candidate.get("controller_issue") != EXPECTED_CONTROLLER_ISSUE:
        _fail("LOCAL_ADJUDICATION_CONTROLLER_MISMATCH")

    bindings = candidate.get("bindings")
    if not isinstance(bindings, Mapping):
        _fail("LOCAL_ADJUDICATION_BINDINGS_MISSING")
    expected_bindings = {
        "external_admission_intake_sha256": record_sha256(external_admission_intake),
        "reverification_packet_sha256": record_sha256(reverification_packet),
        "reviewer_trust_intake_sha256": record_sha256(reviewer_trust_intake),
    }
    if dict(bindings) != expected_bindings:
        _fail("LOCAL_ADJUDICATION_BINDING_MISMATCH")

    adjudication = candidate.get("local_adjudication")
    if not isinstance(adjudication, Mapping):
        _fail("LOCAL_ADJUDICATION_RECORD_MISSING")
    _nonempty(
        adjudication.get("adjudicator_identity"),
        "LOCAL_ADJUDICATION_ADJUDICATOR_IDENTITY_MISSING",
    )
    _timestamp(adjudication.get("adjudicated_at"))
    if adjudication.get("requested_disposition") not in _REQUESTED_DISPOSITIONS:
        _fail("LOCAL_ADJUDICATION_REQUESTED_DISPOSITION_INVALID")
    if adjudication.get("effective_disposition") != "BLOCKED":
        _fail("LOCAL_ADJUDICATION_EFFECTIVE_DISPOSITION_PROMOTED")

    expected_blockers = _derive_blockers(reviewer_trust_intake)
    if not expected_blockers:
        _fail("LOCAL_ADJUDICATION_UNBLOCKED_PATH_NOT_IMPLEMENTED")
    if adjudication.get("blockers") != expected_blockers:
        _fail("LOCAL_ADJUDICATION_BLOCKERS_MISMATCH")

    boundary = {
        "reviewer_attribution_verified": False,
        "independence_verified": False,
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
        if candidate.get(field) != expected:
            _fail(f"LOCAL_ADJUDICATION_BOUNDARY_DRIFT_{field.upper()}")

    return {
        "record_type": "AOSS_STAGE_A_LOCAL_ADJUDICATION_CANDIDATE_REPORT",
        "candidate_validation": "PASS_BLOCKED_LOCAL_ADJUDICATION_CANDIDATE",
        "effective_disposition": "BLOCKED",
        "blockers": expected_blockers,
        "reviewer_attribution_verified": False,
        "independence_verified": False,
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
