"""Non-promoting intake for externally supplied AOSS Stage-A admission decisions.

This module validates attribution, exact candidate binding, and decision syntax.
It deliberately does not convert an external decision into local acceptance,
execution permission, or collection readiness.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from typing import Any, Mapping, NoReturn

from scripts.aoss_stage_a.execution_identity_candidate import (
    record_sha256 as execution_identity_record_sha256,
    validate_execution_identity_candidate,
)
from scripts.aoss_stage_a.installed_environment_evidence import (
    validate_installed_environment_evidence_candidate,
)

RECORD_TYPE = "AOSS_V0_6_STAGE_A_EXTERNAL_ADMISSION_DECISION_INTAKE"
STATUS = "EXTERNAL_DECISION_UNVERIFIED_NOT_ADJUDICATED"
EXPECTED_CONTROLLER_ISSUE = 901
_DECISIONS = {"ACCEPT", "REJECT", "BLOCKED"}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ExternalAdmissionDecisionIntakeError(ValueError):
    """Raised when an external admission-decision intake fails closed."""


def _fail(code: str) -> NoReturn:
    raise ExternalAdmissionDecisionIntakeError(code)


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(
            dict(value),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        + "\n"
    ).encode("utf-8")


def record_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _require_nonempty(value: object, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(code)
    return value.strip()


def _require_sha256(value: object, code: str) -> str:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        _fail(code)
    return value


def _require_timestamp(value: object) -> str:
    timestamp = _require_nonempty(value, "EXTERNAL_DECISION_REVIEWED_AT_MISSING")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        _fail("EXTERNAL_DECISION_REVIEWED_AT_INVALID")
    if parsed.tzinfo is None:
        _fail("EXTERNAL_DECISION_REVIEWED_AT_NOT_OFFSET_AWARE")
    return timestamp


def prepare_external_admission_decision_intake(
    *,
    environment_candidate: Mapping[str, Any],
    execution_identity_candidate: Mapping[str, Any],
    reviewer_identity: str,
    reviewed_at: str,
    external_record_uri: str,
    external_record_sha256: str,
    independence_claimed: bool,
    independence_basis: str | None,
    installed_environment_decision: str,
    source_driver_executable_decision: str,
    destination_attempt_decision: str,
) -> dict[str, object]:
    """Prepare an unverified external-decision intake without local promotion."""

    environment_report = validate_installed_environment_evidence_candidate(
        environment_candidate
    )
    execution_report = validate_execution_identity_candidate(
        execution_identity_candidate
    )

    reviewer = _require_nonempty(
        reviewer_identity,
        "EXTERNAL_DECISION_REVIEWER_IDENTITY_MISSING",
    )
    timestamp = _require_timestamp(reviewed_at)
    record_uri = _require_nonempty(
        external_record_uri,
        "EXTERNAL_DECISION_RECORD_URI_MISSING",
    )
    external_digest = _require_sha256(
        external_record_sha256,
        "EXTERNAL_DECISION_RECORD_SHA_INVALID",
    )

    if not isinstance(independence_claimed, bool):
        _fail("EXTERNAL_DECISION_INDEPENDENCE_CLAIM_INVALID")
    if independence_claimed:
        _require_nonempty(
            independence_basis,
            "EXTERNAL_DECISION_INDEPENDENCE_BASIS_MISSING",
        )
    elif independence_basis is not None and (
        not isinstance(independence_basis, str) or not independence_basis.strip()
    ):
        _fail("EXTERNAL_DECISION_INDEPENDENCE_BASIS_INVALID")

    decisions = {
        "installed_environment": installed_environment_decision,
        "source_driver_executable": source_driver_executable_decision,
        "destination_attempt": destination_attempt_decision,
    }
    for value in decisions.values():
        if value not in _DECISIONS:
            _fail("EXTERNAL_DECISION_DISPOSITION_INVALID")

    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": EXPECTED_CONTROLLER_ISSUE,
        "candidate_bindings": {
            "environment_candidate_record_sha256": record_sha256(
                environment_candidate
            ),
            "environment_evidence_sha256": environment_report["evidence_sha256"],
            "execution_identity_candidate_record_sha256": execution_report[
                "candidate_record_sha256"
            ],
        },
        "external_review": {
            "reviewer_identity": reviewer,
            "reviewed_at": timestamp,
            "external_record_uri": record_uri,
            "external_record_sha256": external_digest,
            "independence_claimed": independence_claimed,
            "independence_basis": independence_basis,
        },
        "external_decisions": decisions,
        "local_adjudication": {
            "status": "NOT_EXECUTED",
            "decision_record_sha256": None,
        },
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }


def validate_external_admission_decision_intake(
    intake: Mapping[str, Any],
    *,
    environment_candidate: Mapping[str, Any],
    execution_identity_candidate: Mapping[str, Any],
) -> dict[str, object]:
    """Validate an external decision as intake evidence, never as local acceptance."""

    environment_report = validate_installed_environment_evidence_candidate(
        environment_candidate
    )
    execution_report = validate_execution_identity_candidate(
        execution_identity_candidate
    )

    if intake.get("record_type") != RECORD_TYPE:
        _fail("EXTERNAL_DECISION_RECORD_TYPE_MISMATCH")
    if intake.get("status") != STATUS:
        _fail("EXTERNAL_DECISION_STATUS_MISMATCH")
    if intake.get("controller_issue") != EXPECTED_CONTROLLER_ISSUE:
        _fail("EXTERNAL_DECISION_CONTROLLER_MISMATCH")

    bindings = intake.get("candidate_bindings")
    if not isinstance(bindings, Mapping):
        _fail("EXTERNAL_DECISION_CANDIDATE_BINDINGS_MISSING")
    expected_environment_record_sha = record_sha256(environment_candidate)
    if bindings.get("environment_candidate_record_sha256") != expected_environment_record_sha:
        _fail("EXTERNAL_DECISION_ENVIRONMENT_CANDIDATE_SHA_MISMATCH")
    if bindings.get("environment_evidence_sha256") != environment_report["evidence_sha256"]:
        _fail("EXTERNAL_DECISION_ENVIRONMENT_EVIDENCE_SHA_MISMATCH")
    if bindings.get("execution_identity_candidate_record_sha256") != execution_report[
        "candidate_record_sha256"
    ]:
        _fail("EXTERNAL_DECISION_EXECUTION_IDENTITY_SHA_MISMATCH")

    review = intake.get("external_review")
    if not isinstance(review, Mapping):
        _fail("EXTERNAL_DECISION_REVIEW_MISSING")
    _require_nonempty(
        review.get("reviewer_identity"),
        "EXTERNAL_DECISION_REVIEWER_IDENTITY_MISSING",
    )
    _require_timestamp(review.get("reviewed_at"))
    _require_nonempty(
        review.get("external_record_uri"),
        "EXTERNAL_DECISION_RECORD_URI_MISSING",
    )
    _require_sha256(
        review.get("external_record_sha256"),
        "EXTERNAL_DECISION_RECORD_SHA_INVALID",
    )

    independence_claimed = review.get("independence_claimed")
    if not isinstance(independence_claimed, bool):
        _fail("EXTERNAL_DECISION_INDEPENDENCE_CLAIM_INVALID")
    independence_basis = review.get("independence_basis")
    if independence_claimed:
        _require_nonempty(
            independence_basis,
            "EXTERNAL_DECISION_INDEPENDENCE_BASIS_MISSING",
        )
    elif independence_basis is not None and (
        not isinstance(independence_basis, str) or not independence_basis.strip()
    ):
        _fail("EXTERNAL_DECISION_INDEPENDENCE_BASIS_INVALID")

    decisions = intake.get("external_decisions")
    if not isinstance(decisions, Mapping):
        _fail("EXTERNAL_DECISIONS_MISSING")
    if set(decisions) != {
        "installed_environment",
        "source_driver_executable",
        "destination_attempt",
    }:
        _fail("EXTERNAL_DECISION_FIELDS_MISMATCH")
    for value in decisions.values():
        if value not in _DECISIONS:
            _fail("EXTERNAL_DECISION_DISPOSITION_INVALID")

    if intake.get("local_adjudication") != {
        "status": "NOT_EXECUTED",
        "decision_record_sha256": None,
    }:
        _fail("EXTERNAL_DECISION_LOCAL_ADJUDICATION_PREMATURE")

    boundary = {
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
            _fail(f"EXTERNAL_DECISION_BOUNDARY_DRIFT_{field.upper()}")

    return {
        "record_type": "AOSS_STAGE_A_EXTERNAL_ADMISSION_DECISION_INTAKE_REPORT",
        "intake_validation": "PASS_EXTERNAL_DECISION_STRUCTURAL_ONLY",
        "intake_record_sha256": record_sha256(intake),
        "external_decisions": dict(decisions),
        "reviewer_attribution_verified": False,
        "independence_verified": False,
        "external_record_retrieved": False,
        "cryptographic_reverification": "NOT_EXECUTED",
        "local_adjudication": "NOT_EXECUTED",
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
