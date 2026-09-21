"""Cryptographic custody/reverification for AOSS Stage-A external admission evidence.

This module can establish only that supplied bytes match declared SHA-256
identities. It cannot verify reviewer identity or independence, perform local
governance adjudication, accept execution identities, or enable collection.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from typing import Any, Mapping, NoReturn, Sequence

from scripts.aoss_stage_a.external_admission_decision_intake import (
    record_sha256,
    validate_external_admission_decision_intake,
)

RECORD_TYPE = "AOSS_V0_6_STAGE_A_EXTERNAL_EVIDENCE_REVERIFICATION_PACKET"
STATUS = "CRYPTOGRAPHIC_BYTES_MATCHED_NO_TRUST_PROMOTION"
EXPECTED_CONTROLLER_ISSUE = 901
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ExternalEvidenceReverificationError(ValueError):
    """Raised when external evidence reverification fails closed."""


def _fail(code: str) -> NoReturn:
    raise ExternalEvidenceReverificationError(code)


def _nonempty(value: object, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(code)
    return value.strip()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_sha256(value: object, code: str) -> str:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        _fail(code)
    return value


def _timestamp(value: object) -> str:
    timestamp = _nonempty(value, "REVERIFICATION_RETRIEVED_AT_MISSING")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        _fail("REVERIFICATION_RETRIEVED_AT_INVALID")
    if parsed.tzinfo is None:
        _fail("REVERIFICATION_RETRIEVED_AT_NOT_OFFSET_AWARE")
    return timestamp


def _validated_intake_review(
    intake: Mapping[str, Any],
    *,
    environment_candidate: Mapping[str, Any],
    execution_identity_candidate: Mapping[str, Any],
) -> Mapping[str, Any]:
    validate_external_admission_decision_intake(
        intake,
        environment_candidate=environment_candidate,
        execution_identity_candidate=execution_identity_candidate,
    )
    review = intake.get("external_review")
    if not isinstance(review, Mapping):
        _fail("REVERIFICATION_EXTERNAL_REVIEW_MISSING")
    return review


def _verify_attribution_artifacts(
    artifacts: Sequence[tuple[str, str, str, bytes]],
) -> list[dict[str, object]]:
    if not artifacts:
        _fail("REVERIFICATION_ATTRIBUTION_EVIDENCE_REQUIRED")

    seen: set[str] = set()
    records: list[dict[str, object]] = []
    for artifact_id, source_uri, declared_sha256, content in artifacts:
        identifier = _nonempty(artifact_id, "REVERIFICATION_ATTRIBUTION_ARTIFACT_ID_MISSING")
        if identifier in seen:
            _fail("REVERIFICATION_ATTRIBUTION_ARTIFACT_ID_DUPLICATE")
        seen.add(identifier)

        uri = _nonempty(source_uri, "REVERIFICATION_ATTRIBUTION_ARTIFACT_URI_MISSING")
        declared = _require_sha256(
            declared_sha256,
            "REVERIFICATION_ATTRIBUTION_DECLARED_SHA_INVALID",
        )
        if not isinstance(content, bytes) or not content:
            _fail("REVERIFICATION_ATTRIBUTION_ARTIFACT_BYTES_MISSING")

        observed = _sha256_bytes(content)
        if observed != declared:
            _fail("REVERIFICATION_ATTRIBUTION_SHA_MISMATCH")

        records.append(
            {
                "artifact_id": identifier,
                "source_uri": uri,
                "declared_sha256": declared,
                "observed_sha256": observed,
                "byte_length": len(content),
                "digest_match": True,
            }
        )
    return records


def prepare_external_evidence_reverification_packet(
    *,
    intake: Mapping[str, Any],
    environment_candidate: Mapping[str, Any],
    execution_identity_candidate: Mapping[str, Any],
    retrieval_source_uri: str,
    retrieved_at: str,
    external_record_bytes: bytes,
    attribution_artifacts: Sequence[tuple[str, str, str, bytes]],
) -> dict[str, object]:
    """Build a hash-matched evidence packet without promoting trust state."""

    review = _validated_intake_review(
        intake,
        environment_candidate=environment_candidate,
        execution_identity_candidate=execution_identity_candidate,
    )

    declared_uri = _nonempty(
        review.get("external_record_uri"),
        "REVERIFICATION_EXTERNAL_RECORD_URI_MISSING",
    )
    requested_uri = _nonempty(
        retrieval_source_uri,
        "REVERIFICATION_RETRIEVAL_SOURCE_URI_MISSING",
    )
    if requested_uri != declared_uri:
        _fail("REVERIFICATION_RETRIEVAL_SOURCE_URI_MISMATCH")

    declared_sha = _require_sha256(
        review.get("external_record_sha256"),
        "REVERIFICATION_EXTERNAL_RECORD_DECLARED_SHA_INVALID",
    )
    if not isinstance(external_record_bytes, bytes) or not external_record_bytes:
        _fail("REVERIFICATION_EXTERNAL_RECORD_BYTES_MISSING")
    observed_sha = _sha256_bytes(external_record_bytes)
    if observed_sha != declared_sha:
        _fail("REVERIFICATION_EXTERNAL_RECORD_SHA_MISMATCH")

    attribution_records = _verify_attribution_artifacts(attribution_artifacts)

    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": EXPECTED_CONTROLLER_ISSUE,
        "intake_record_sha256": record_sha256(intake),
        "retrieval": {
            "source_uri": declared_uri,
            "retrieved_at": _timestamp(retrieved_at),
            "external_record_declared_sha256": declared_sha,
            "external_record_observed_sha256": observed_sha,
            "external_record_byte_length": len(external_record_bytes),
            "external_record_digest_match": True,
        },
        "reviewer_attribution_evidence": attribution_records,
        "attribution_binding": "PACKET_DECLARATION_NOT_TRUST_ANCHOR",
        "external_record_retrieved": True,
        "attribution_evidence_retrieved": True,
        "cryptographic_reverification": "PASS_DECLARED_BYTES_MATCH_SHA256",
        "reviewer_attribution_verified": False,
        "independence_verified": False,
        "local_adjudication": "NOT_EXECUTED",
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }


def validate_external_evidence_reverification_packet(
    packet: Mapping[str, Any],
    *,
    intake: Mapping[str, Any],
    environment_candidate: Mapping[str, Any],
    execution_identity_candidate: Mapping[str, Any],
    external_record_bytes: bytes,
    attribution_artifacts: Sequence[tuple[str, str, str, bytes]],
) -> dict[str, object]:
    """Recompute packet digests and preserve the non-promotion boundary."""

    review = _validated_intake_review(
        intake,
        environment_candidate=environment_candidate,
        execution_identity_candidate=execution_identity_candidate,
    )

    if packet.get("record_type") != RECORD_TYPE:
        _fail("REVERIFICATION_PACKET_TYPE_MISMATCH")
    if packet.get("status") != STATUS:
        _fail("REVERIFICATION_PACKET_STATUS_MISMATCH")
    if packet.get("controller_issue") != EXPECTED_CONTROLLER_ISSUE:
        _fail("REVERIFICATION_CONTROLLER_MISMATCH")
    if packet.get("intake_record_sha256") != record_sha256(intake):
        _fail("REVERIFICATION_INTAKE_SHA_MISMATCH")

    retrieval = packet.get("retrieval")
    if not isinstance(retrieval, Mapping):
        _fail("REVERIFICATION_RETRIEVAL_RECORD_MISSING")
    declared_uri = _nonempty(
        review.get("external_record_uri"),
        "REVERIFICATION_EXTERNAL_RECORD_URI_MISSING",
    )
    if retrieval.get("source_uri") != declared_uri:
        _fail("REVERIFICATION_RETRIEVAL_SOURCE_URI_MISMATCH")
    _timestamp(retrieval.get("retrieved_at"))

    declared_sha = _require_sha256(
        review.get("external_record_sha256"),
        "REVERIFICATION_EXTERNAL_RECORD_DECLARED_SHA_INVALID",
    )
    if not isinstance(external_record_bytes, bytes) or not external_record_bytes:
        _fail("REVERIFICATION_EXTERNAL_RECORD_BYTES_MISSING")
    observed_sha = _sha256_bytes(external_record_bytes)
    if observed_sha != declared_sha:
        _fail("REVERIFICATION_EXTERNAL_RECORD_SHA_MISMATCH")
    if retrieval.get("external_record_declared_sha256") != declared_sha:
        _fail("REVERIFICATION_PACKET_DECLARED_SHA_MISMATCH")
    if retrieval.get("external_record_observed_sha256") != observed_sha:
        _fail("REVERIFICATION_PACKET_OBSERVED_SHA_MISMATCH")
    if retrieval.get("external_record_byte_length") != len(external_record_bytes):
        _fail("REVERIFICATION_PACKET_BYTE_LENGTH_MISMATCH")
    if retrieval.get("external_record_digest_match") is not True:
        _fail("REVERIFICATION_PACKET_DIGEST_MATCH_INVALID")

    expected_attribution = _verify_attribution_artifacts(attribution_artifacts)
    if packet.get("reviewer_attribution_evidence") != expected_attribution:
        _fail("REVERIFICATION_ATTRIBUTION_EVIDENCE_MISMATCH")
    if packet.get("attribution_binding") != "PACKET_DECLARATION_NOT_TRUST_ANCHOR":
        _fail("REVERIFICATION_ATTRIBUTION_BINDING_OVERCLAIM")

    boundary = {
        "external_record_retrieved": True,
        "attribution_evidence_retrieved": True,
        "cryptographic_reverification": "PASS_DECLARED_BYTES_MATCH_SHA256",
        "reviewer_attribution_verified": False,
        "independence_verified": False,
        "local_adjudication": "NOT_EXECUTED",
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
            _fail(f"REVERIFICATION_BOUNDARY_DRIFT_{field.upper()}")

    return {
        "record_type": "AOSS_STAGE_A_EXTERNAL_EVIDENCE_REVERIFICATION_REPORT",
        "reverification": "PASS_DECLARED_BYTES_MATCH_SHA256",
        "intake_record_sha256": record_sha256(intake),
        "external_record_retrieved": True,
        "attribution_evidence_retrieved": True,
        "reviewer_attribution_verified": False,
        "independence_verified": False,
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
