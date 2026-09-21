"""Structural packet for AOSS Stage-A installed-environment acceptance review.

This module binds a validated environment-evidence candidate to an exact review
packet. It deliberately cannot accept the environment: adjudication remains a
separate trust boundary.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping, NoReturn

from scripts.aoss_stage_a.installed_environment_evidence import (
    validate_installed_environment_evidence_candidate,
)

RECORD_TYPE = "AOSS_V0_6_STAGE_A_INSTALLED_ENVIRONMENT_ACCEPTANCE_PACKET"
STATUS = "PREPARED_FOR_EXTERNAL_REVIEW_NOT_ACCEPTED"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class InstalledEnvironmentAcceptancePacketError(ValueError):
    """Raised when an environment-acceptance packet fails closed."""


def _fail(code: str) -> NoReturn:
    raise InstalledEnvironmentAcceptancePacketError(code)


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


def candidate_record_sha256(candidate: Mapping[str, Any]) -> str:
    """Return the deterministic digest of the complete candidate record."""

    return hashlib.sha256(_canonical_bytes(candidate)).hexdigest()


def prepare_installed_environment_acceptance_packet(
    *,
    candidate: Mapping[str, Any],
    candidate_source_ref: str,
) -> dict[str, object]:
    """Prepare a packet for external review without performing adjudication."""

    candidate_report = validate_installed_environment_evidence_candidate(candidate)
    source_ref = candidate_source_ref.strip()
    if not source_ref:
        _fail("ENVIRONMENT_ACCEPTANCE_SOURCE_REF_MISSING")

    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": 901,
        "candidate_source_ref": source_ref,
        "candidate_record_sha256": candidate_record_sha256(candidate),
        "candidate_evidence_sha256": candidate_report["evidence_sha256"],
        "adjudication": {
            "status": "NOT_EXECUTED",
            "reviewer_identity": None,
            "reviewed_at": None,
            "decision_record_sha256": None,
            "installed_environment_acceptance": "NOT_ESTABLISHED",
        },
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }


def validate_installed_environment_acceptance_packet(
    packet: Mapping[str, Any],
    *,
    candidate: Mapping[str, Any],
) -> dict[str, object]:
    """Validate structural binding while forbidding self-acceptance."""

    candidate_report = validate_installed_environment_evidence_candidate(candidate)

    if packet.get("record_type") != RECORD_TYPE:
        _fail("ENVIRONMENT_ACCEPTANCE_PACKET_TYPE_MISMATCH")
    if packet.get("status") != STATUS:
        _fail("ENVIRONMENT_ACCEPTANCE_PACKET_STATUS_MISMATCH")
    if packet.get("controller_issue") != 901:
        _fail("ENVIRONMENT_ACCEPTANCE_PACKET_CONTROLLER_MISMATCH")

    source_ref = packet.get("candidate_source_ref")
    if not isinstance(source_ref, str) or not source_ref.strip():
        _fail("ENVIRONMENT_ACCEPTANCE_SOURCE_REF_MISSING")

    expected_record_sha = candidate_record_sha256(candidate)
    record_sha = packet.get("candidate_record_sha256")
    if not isinstance(record_sha, str) or _SHA256_RE.fullmatch(record_sha) is None:
        _fail("ENVIRONMENT_ACCEPTANCE_CANDIDATE_RECORD_SHA_INVALID")
    if record_sha != expected_record_sha:
        _fail("ENVIRONMENT_ACCEPTANCE_CANDIDATE_RECORD_SHA_MISMATCH")

    evidence_sha = packet.get("candidate_evidence_sha256")
    if not isinstance(evidence_sha, str) or _SHA256_RE.fullmatch(evidence_sha) is None:
        _fail("ENVIRONMENT_ACCEPTANCE_EVIDENCE_SHA_INVALID")
    if evidence_sha != candidate_report["evidence_sha256"]:
        _fail("ENVIRONMENT_ACCEPTANCE_EVIDENCE_SHA_MISMATCH")

    adjudication = packet.get("adjudication")
    if not isinstance(adjudication, Mapping):
        _fail("ENVIRONMENT_ACCEPTANCE_ADJUDICATION_MISSING")
    if set(adjudication) != {
        "status",
        "reviewer_identity",
        "reviewed_at",
        "decision_record_sha256",
        "installed_environment_acceptance",
    }:
        _fail("ENVIRONMENT_ACCEPTANCE_ADJUDICATION_FIELDS_MISMATCH")
    if adjudication.get("status") != "NOT_EXECUTED":
        _fail("ENVIRONMENT_ACCEPTANCE_ADJUDICATION_MUST_REMAIN_EXTERNAL")
    if adjudication.get("reviewer_identity") is not None:
        _fail("ENVIRONMENT_ACCEPTANCE_REVIEWER_PREPOPULATED")
    if adjudication.get("reviewed_at") is not None:
        _fail("ENVIRONMENT_ACCEPTANCE_REVIEW_TIME_PREPOPULATED")
    if adjudication.get("decision_record_sha256") is not None:
        _fail("ENVIRONMENT_ACCEPTANCE_DECISION_DIGEST_PREPOPULATED")
    if adjudication.get("installed_environment_acceptance") != "NOT_ESTABLISHED":
        _fail("ENVIRONMENT_ACCEPTANCE_PREMATURE")

    expected_boundary = {
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }
    for field, expected in expected_boundary.items():
        if packet.get(field) != expected:
            _fail(f"ENVIRONMENT_ACCEPTANCE_BOUNDARY_DRIFT_{field.upper()}")

    return {
        "record_type": "AOSS_STAGE_A_INSTALLED_ENVIRONMENT_ACCEPTANCE_PACKET_REPORT",
        "packet_validation": "PASS_STRUCTURAL_BINDING_ONLY",
        "candidate_record_sha256": expected_record_sha,
        "candidate_evidence_sha256": evidence_sha,
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "external_adjudication": "NOT_EXECUTED",
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
