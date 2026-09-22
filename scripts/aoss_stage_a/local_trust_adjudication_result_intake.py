"""Non-promoting local trust adjudication-result intake for AOSS Stage A.

The intake retains an eventual local review result and binds it to the inert
review packet. It records reported findings but cannot promote reviewer
attribution, independence, execution authority, collection readiness, or
scientific N.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Mapping, NoReturn

from scripts.aoss_stage_a.external_admission_decision_intake import record_sha256
from scripts.aoss_stage_a.local_trust_review_packet import (
    validate_local_trust_review_packet,
)

RECORD_TYPE = "AOSS_V0_6_STAGE_A_LOCAL_TRUST_ADJUDICATION_RESULT_INTAKE"
STATUS = "LOCAL_REVIEW_RESULT_RECORDED_NO_TRUST_PROMOTION"
EXPECTED_CONTROLLER_ISSUE = 901
_ALLOWED_FINDINGS = {"VERIFIED", "NOT_VERIFIED", "BLOCKED"}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class LocalTrustAdjudicationResultIntakeError(ValueError):
    """Raised when a local trust adjudication-result intake fails closed."""


def _fail(code: str) -> NoReturn:
    raise LocalTrustAdjudicationResultIntakeError(code)


def _nonempty(value: object, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(code)
    return value.strip()


def _timestamp(value: object) -> str:
    timestamp = _nonempty(
        value,
        "LOCAL_TRUST_ADJUDICATION_RESULT_REVIEWED_AT_MISSING",
    )
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_REVIEWED_AT_INVALID")
    if parsed.tzinfo is None:
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_REVIEWED_AT_NOT_OFFSET_AWARE")
    return timestamp


def _digest(value: object) -> str:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_SHA256_INVALID")
    return value


def _finding(value: object, field: str) -> str:
    if value not in _ALLOWED_FINDINGS:
        _fail(f"LOCAL_TRUST_ADJUDICATION_RESULT_{field.upper()}_INVALID")
    return str(value)


def prepare_local_trust_adjudication_result_intake(
    *,
    review_packet: Mapping[str, Any],
    external_admission_intake: Mapping[str, Any],
    reverification_packet: Mapping[str, Any],
    reviewer_trust_intake: Mapping[str, Any],
    local_adjudication_candidate: Mapping[str, Any],
    retained_evidence: list[tuple[str, str, str]],
    reviewer_identity: str,
    reviewed_at: str,
    decision_record_uri: str,
    decision_record_sha256: str,
    fresh_cryptographic_verification_reported: bool,
    reviewer_attribution_finding: str,
    independence_finding: str,
) -> dict[str, object]:
    """Record a local review result without turning it into accepted trust."""

    packet_report = validate_local_trust_review_packet(
        review_packet,
        external_admission_intake=external_admission_intake,
        reverification_packet=reverification_packet,
        reviewer_trust_intake=reviewer_trust_intake,
        local_adjudication_candidate=local_adjudication_candidate,
        retained_evidence=retained_evidence,
    )
    if packet_report["review_classification"] != "NOT_EXECUTED":
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_REVIEW_PACKET_ALREADY_EXECUTED")

    reviewer = _nonempty(
        reviewer_identity,
        "LOCAL_TRUST_ADJUDICATION_RESULT_REVIEWER_IDENTITY_MISSING",
    )
    timestamp = _timestamp(reviewed_at)
    record_uri = _nonempty(
        decision_record_uri,
        "LOCAL_TRUST_ADJUDICATION_RESULT_URI_MISSING",
    )
    record_digest = _digest(decision_record_sha256)
    attribution = _finding(reviewer_attribution_finding, "reviewer_attribution")
    independence = _finding(independence_finding, "independence")

    if not isinstance(fresh_cryptographic_verification_reported, bool):
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_FRESH_CRYPTO_FLAG_INVALID")

    reported_outcome = (
        "POSITIVE_REVIEW_REPORTED"
        if (fresh_cryptographic_verification_reported and attribution == "VERIFIED" and independence == "VERIFIED")
        else "NON_POSITIVE_REVIEW_REPORTED"
    )

    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": EXPECTED_CONTROLLER_ISSUE,
        "bindings": {
            "local_trust_review_packet_sha256": record_sha256(review_packet),
        },
        "reported_review": {
            "reviewer_identity": reviewer,
            "reviewed_at": timestamp,
            "decision_record_uri": record_uri,
            "decision_record_sha256": record_digest,
            "fresh_cryptographic_verification_reported": (fresh_cryptographic_verification_reported),
            "findings": {
                "reviewer_attribution": attribution,
                "independence": independence,
            },
            "reported_outcome": reported_outcome,
        },
        "trust_promotion": "NOT_EXECUTED",
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


def validate_local_trust_adjudication_result_intake(
    intake: Mapping[str, Any],
    *,
    review_packet: Mapping[str, Any],
    external_admission_intake: Mapping[str, Any],
    reverification_packet: Mapping[str, Any],
    reviewer_trust_intake: Mapping[str, Any],
    local_adjudication_candidate: Mapping[str, Any],
    retained_evidence: list[tuple[str, str, str]],
) -> dict[str, object]:
    """Validate a retained local result while preserving non-promotion."""

    validate_local_trust_review_packet(
        review_packet,
        external_admission_intake=external_admission_intake,
        reverification_packet=reverification_packet,
        reviewer_trust_intake=reviewer_trust_intake,
        local_adjudication_candidate=local_adjudication_candidate,
        retained_evidence=retained_evidence,
    )

    if intake.get("record_type") != RECORD_TYPE:
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_RECORD_TYPE_MISMATCH")
    if intake.get("status") != STATUS:
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_STATUS_MISMATCH")
    if intake.get("controller_issue") != EXPECTED_CONTROLLER_ISSUE:
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_CONTROLLER_MISMATCH")

    expected_bindings = {
        "local_trust_review_packet_sha256": record_sha256(review_packet),
    }
    bindings = intake.get("bindings")
    if not isinstance(bindings, Mapping) or dict(bindings) != expected_bindings:
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_BINDING_MISMATCH")

    reported = intake.get("reported_review")
    if not isinstance(reported, Mapping):
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_REPORTED_REVIEW_MISSING")
    _nonempty(
        reported.get("reviewer_identity"),
        "LOCAL_TRUST_ADJUDICATION_RESULT_REVIEWER_IDENTITY_MISSING",
    )
    _timestamp(reported.get("reviewed_at"))
    _nonempty(
        reported.get("decision_record_uri"),
        "LOCAL_TRUST_ADJUDICATION_RESULT_URI_MISSING",
    )
    _digest(reported.get("decision_record_sha256"))

    fresh = reported.get("fresh_cryptographic_verification_reported")
    if not isinstance(fresh, bool):
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_FRESH_CRYPTO_FLAG_INVALID")

    findings = reported.get("findings")
    if not isinstance(findings, Mapping):
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_FINDINGS_MISSING")
    attribution = _finding(findings.get("reviewer_attribution"), "reviewer_attribution")
    independence = _finding(findings.get("independence"), "independence")

    expected_reported_outcome = (
        "POSITIVE_REVIEW_REPORTED"
        if fresh and attribution == "VERIFIED" and independence == "VERIFIED"
        else "NON_POSITIVE_REVIEW_REPORTED"
    )
    if reported.get("reported_outcome") != expected_reported_outcome:
        _fail("LOCAL_TRUST_ADJUDICATION_RESULT_OUTCOME_MISMATCH")

    boundary = {
        "trust_promotion": "NOT_EXECUTED",
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
        if intake.get(field) != expected:
            _fail(f"LOCAL_TRUST_ADJUDICATION_RESULT_BOUNDARY_DRIFT_{field.upper()}")

    return {
        "record_type": "AOSS_STAGE_A_LOCAL_TRUST_ADJUDICATION_RESULT_INTAKE_REPORT",
        "intake_validation": "PASS_RECORDED_NO_TRUST_PROMOTION",
        "reported_outcome": expected_reported_outcome,
        "trust_promotion": "NOT_EXECUTED",
        "reviewer_attribution_verified": False,
        "independence_verified": False,
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
