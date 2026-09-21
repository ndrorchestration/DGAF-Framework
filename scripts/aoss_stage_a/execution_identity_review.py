"""Prepare AOSS Stage-A execution-identity material for external review.

The accepted source-driver and executable/destination records are intentionally
non-collecting proposals. This module binds their exact bytes and proves why
they are not yet admissible execution identities. It cannot accept replacement
identities or authorize collection.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, NoReturn

from scripts.aoss_stage_a.executable_destination_binding import (
    EXPECTED_ATTEMPT_IDENTITY,
    EXPECTED_DESTINATION_IDENTITY,
    EXPECTED_EXECUTABLE_IDENTITY,
    validate_proposed_executable_destination_binding,
)
from scripts.aoss_stage_a.source_driver_binding import (
    validate_unaccepted_source_driver_binding,
)

RECORD_TYPE = "AOSS_V0_6_STAGE_A_EXECUTION_IDENTITY_REVIEW_PACKET"
STATUS = "PREPARED_BLOCKED_PENDING_REAL_IDENTITIES_AND_EXTERNAL_ADJUDICATION"
_BLOCKERS = (
    "SOURCE_DRIVER_ACCEPTANCE_REQUIRED",
    "REAL_EXECUTABLE_IDENTITY_REQUIRED",
    "REAL_DESTINATION_IDENTITY_REQUIRED",
    "REAL_ATTEMPT_IDENTITY_REQUIRED",
    "EXTERNAL_ADJUDICATION_REQUIRED",
)


class ExecutionIdentityReviewPacketError(ValueError):
    """Raised when the review packet drifts or overclaims."""


def _fail(code: str) -> NoReturn:
    raise ExecutionIdentityReviewPacketError(code)


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


def prepare_execution_identity_review_packet(
    *,
    source_driver_binding: Mapping[str, Any],
    executable_destination_binding: Mapping[str, Any],
    source_driver_ref: str,
    executable_destination_ref: str,
) -> dict[str, object]:
    """Bind the current proposal records while preserving their blockers."""

    source_report = validate_unaccepted_source_driver_binding(source_driver_binding)
    identity_report = validate_proposed_executable_destination_binding(
        executable_destination_binding
    )

    if not source_driver_ref.strip():
        _fail("SOURCE_DRIVER_REVIEW_REF_MISSING")
    if not executable_destination_ref.strip():
        _fail("EXECUTABLE_DESTINATION_REVIEW_REF_MISSING")

    if source_report["source_driver_binding"] != "NOT_ESTABLISHED":
        _fail("SOURCE_DRIVER_ACCEPTANCE_PREMATURE")
    if executable_destination_binding.get("executable_identity") != EXPECTED_EXECUTABLE_IDENTITY:
        _fail("EXECUTABLE_PROVENANCE_PLACEHOLDER_DRIFT")
    if executable_destination_binding.get("destination_identity") != EXPECTED_DESTINATION_IDENTITY:
        _fail("DESTINATION_FIXTURE_DRIFT")
    if executable_destination_binding.get("attempt_identity") != EXPECTED_ATTEMPT_IDENTITY:
        _fail("ATTEMPT_FIXTURE_DRIFT")

    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": 901,
        "source_driver": {
            "ref": source_driver_ref.strip(),
            "record_sha256": record_sha256(source_driver_binding),
            "acceptance": "NOT_ESTABLISHED",
        },
        "executable_destination": {
            "ref": executable_destination_ref.strip(),
            "record_sha256": record_sha256(executable_destination_binding),
            "executable_identity_class": "SOURCE_MODULE_PROVENANCE_ONLY",
            "destination_identity_class": "SYNTHETIC_FIXTURE_ONLY",
            "attempt_identity_class": "SYNTHETIC_FIXTURE_ONLY",
            "executable_acceptance": identity_report["executable_acceptance"],
            "destination_acceptance": identity_report["destination_acceptance"],
        },
        "replacement_identity_requirements": {
            "executable": "REAL_EXECUTABLE_IDENTITY_REQUIRED",
            "destination": "REAL_DESTINATION_IDENTITY_REQUIRED",
            "attempt": "REAL_ATTEMPT_IDENTITY_REQUIRED",
        },
        "adjudication": {
            "status": "NOT_EXECUTED",
            "reviewer_identity": None,
            "reviewed_at": None,
            "decision_record_sha256": None,
        },
        "blockers": list(_BLOCKERS),
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }


def validate_execution_identity_review_packet(
    packet: Mapping[str, Any],
    *,
    source_driver_binding: Mapping[str, Any],
    executable_destination_binding: Mapping[str, Any],
) -> dict[str, object]:
    """Validate exact proposal binding and the fail-closed review boundary."""

    validate_unaccepted_source_driver_binding(source_driver_binding)
    validate_proposed_executable_destination_binding(executable_destination_binding)

    if packet.get("record_type") != RECORD_TYPE:
        _fail("EXECUTION_IDENTITY_REVIEW_PACKET_TYPE_MISMATCH")
    if packet.get("status") != STATUS:
        _fail("EXECUTION_IDENTITY_REVIEW_PACKET_STATUS_MISMATCH")
    if packet.get("controller_issue") != 901:
        _fail("EXECUTION_IDENTITY_REVIEW_CONTROLLER_MISMATCH")

    source = packet.get("source_driver")
    if not isinstance(source, Mapping):
        _fail("SOURCE_DRIVER_REVIEW_BINDING_MISSING")
    if source.get("record_sha256") != record_sha256(source_driver_binding):
        _fail("SOURCE_DRIVER_REVIEW_DIGEST_MISMATCH")
    if source.get("acceptance") != "NOT_ESTABLISHED":
        _fail("SOURCE_DRIVER_ACCEPTANCE_PREMATURE")

    identities = packet.get("executable_destination")
    if not isinstance(identities, Mapping):
        _fail("EXECUTABLE_DESTINATION_REVIEW_BINDING_MISSING")
    if identities.get("record_sha256") != record_sha256(executable_destination_binding):
        _fail("EXECUTABLE_DESTINATION_REVIEW_DIGEST_MISMATCH")
    if identities.get("executable_identity_class") != "SOURCE_MODULE_PROVENANCE_ONLY":
        _fail("EXECUTABLE_IDENTITY_CLASS_OVERCLAIM")
    if identities.get("destination_identity_class") != "SYNTHETIC_FIXTURE_ONLY":
        _fail("DESTINATION_IDENTITY_CLASS_OVERCLAIM")
    if identities.get("attempt_identity_class") != "SYNTHETIC_FIXTURE_ONLY":
        _fail("ATTEMPT_IDENTITY_CLASS_OVERCLAIM")
    if identities.get("executable_acceptance") != "NOT_ESTABLISHED":
        _fail("EXECUTABLE_ACCEPTANCE_PREMATURE")
    if identities.get("destination_acceptance") != "NOT_ESTABLISHED":
        _fail("DESTINATION_ACCEPTANCE_PREMATURE")

    requirements = packet.get("replacement_identity_requirements")
    if requirements != {
        "executable": "REAL_EXECUTABLE_IDENTITY_REQUIRED",
        "destination": "REAL_DESTINATION_IDENTITY_REQUIRED",
        "attempt": "REAL_ATTEMPT_IDENTITY_REQUIRED",
    }:
        _fail("REPLACEMENT_IDENTITY_REQUIREMENTS_DRIFT")

    adjudication = packet.get("adjudication")
    if adjudication != {
        "status": "NOT_EXECUTED",
        "reviewer_identity": None,
        "reviewed_at": None,
        "decision_record_sha256": None,
    }:
        _fail("EXECUTION_IDENTITY_ADJUDICATION_PREMATURE")

    if packet.get("blockers") != list(_BLOCKERS):
        _fail("EXECUTION_IDENTITY_BLOCKER_SET_DRIFT")
    if packet.get("execution_allowed") is not False:
        _fail("EXECUTION_PREMATURE")
    if packet.get("collection_execution_readiness") != "NOT_ESTABLISHED":
        _fail("COLLECTION_READINESS_PREMATURE")
    if packet.get("outcomes_generated") is not False:
        _fail("OUTCOME_GENERATION_PREMATURE")
    if packet.get("scientific_n_increment") != 0:
        _fail("SCIENTIFIC_N_INCREMENT_INVALID")

    return {
        "record_type": "AOSS_STAGE_A_EXECUTION_IDENTITY_REVIEW_PACKET_REPORT",
        "packet_validation": "PASS_BLOCKED_REVIEW_PACKET",
        "blockers": list(_BLOCKERS),
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "external_adjudication": "NOT_EXECUTED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
