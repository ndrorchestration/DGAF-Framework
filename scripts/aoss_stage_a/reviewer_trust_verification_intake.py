"""Non-promoting intake for external reviewer-trust verification findings.

This layer records externally supplied findings about reviewer attribution and
independence. It does not convert those findings into local verified trust,
local execution-admission acceptance, or collection readiness.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Mapping, NoReturn

from scripts.aoss_stage_a.external_admission_decision_intake import record_sha256

RECORD_TYPE = "AOSS_V0_6_STAGE_A_REVIEWER_TRUST_VERIFICATION_INTAKE"
STATUS = "EXTERNAL_TRUST_FINDINGS_UNADJUDICATED"
EXPECTED_CONTROLLER_ISSUE = 901
_FINDINGS = {"VERIFIED", "NOT_VERIFIED", "BLOCKED"}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ReviewerTrustVerificationIntakeError(ValueError):
    """Raised when reviewer-trust verification intake fails closed."""


def _fail(code: str) -> NoReturn:
    raise ReviewerTrustVerificationIntakeError(code)


def _nonempty(value: object, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(code)
    return value.strip()


def _sha256(value: object, code: str) -> str:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        _fail(code)
    return value


def _timestamp(value: object) -> str:
    timestamp = _nonempty(value, "TRUST_INTAKE_VERIFIED_AT_MISSING")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        _fail("TRUST_INTAKE_VERIFIED_AT_INVALID")
    if parsed.tzinfo is None:
        _fail("TRUST_INTAKE_VERIFIED_AT_NOT_OFFSET_AWARE")
    return timestamp


def _validate_reverification_packet(packet: Mapping[str, Any]) -> None:
    if packet.get("record_type") != "AOSS_V0_6_STAGE_A_EXTERNAL_EVIDENCE_REVERIFICATION_PACKET":
        _fail("TRUST_INTAKE_REVERIFICATION_PACKET_TYPE_MISMATCH")
    if packet.get("cryptographic_reverification") != "PASS_DECLARED_BYTES_MATCH_SHA256":
        _fail("TRUST_INTAKE_REVERIFICATION_NOT_PASS")
    if packet.get("reviewer_attribution_verified") is not False:
        _fail("TRUST_INTAKE_REVERIFICATION_ATTRIBUTION_PROMOTED")
    if packet.get("independence_verified") is not False:
        _fail("TRUST_INTAKE_REVERIFICATION_INDEPENDENCE_PROMOTED")
    if packet.get("local_adjudication") != "NOT_EXECUTED":
        _fail("TRUST_INTAKE_REVERIFICATION_LOCAL_ADJUDICATION_PREMATURE")
    if packet.get("execution_allowed") is not False:
        _fail("TRUST_INTAKE_REVERIFICATION_EXECUTION_PROMOTED")
    if packet.get("collection_execution_readiness") != "NOT_ESTABLISHED":
        _fail("TRUST_INTAKE_REVERIFICATION_READINESS_PROMOTED")
    if packet.get("scientific_n_increment") != 0:
        _fail("TRUST_INTAKE_REVERIFICATION_N_DRIFT")


def prepare_reviewer_trust_verification_intake(
    *,
    external_admission_intake: Mapping[str, Any],
    reverification_packet: Mapping[str, Any],
    verifier_identity: str,
    verified_at: str,
    verification_record_uri: str,
    verification_record_sha256: str,
    verification_method_summary: str,
    reviewer_attribution_finding: str,
    independence_finding: str,
) -> dict[str, object]:
    """Record external trust findings without local promotion."""

    _validate_reverification_packet(reverification_packet)

    verifier = _nonempty(verifier_identity, "TRUST_INTAKE_VERIFIER_IDENTITY_MISSING")
    timestamp = _timestamp(verified_at)
    record_uri = _nonempty(
        verification_record_uri,
        "TRUST_INTAKE_VERIFICATION_RECORD_URI_MISSING",
    )
    record_digest = _sha256(
        verification_record_sha256,
        "TRUST_INTAKE_VERIFICATION_RECORD_SHA_INVALID",
    )
    method = _nonempty(
        verification_method_summary,
        "TRUST_INTAKE_VERIFICATION_METHOD_MISSING",
    )

    findings = {
        "reviewer_attribution": reviewer_attribution_finding,
        "independence": independence_finding,
    }
    for finding in findings.values():
        if finding not in _FINDINGS:
            _fail("TRUST_INTAKE_FINDING_INVALID")

    attribution_evidence = reverification_packet.get("reviewer_attribution_evidence")
    if not isinstance(attribution_evidence, list) or not attribution_evidence:
        _fail("TRUST_INTAKE_ATTRIBUTION_EVIDENCE_MISSING")

    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": EXPECTED_CONTROLLER_ISSUE,
        "bindings": {
            "external_admission_intake_sha256": record_sha256(external_admission_intake),
            "reverification_packet_sha256": record_sha256(reverification_packet),
        },
        "external_verification": {
            "verifier_identity": verifier,
            "verified_at": timestamp,
            "verification_record_uri": record_uri,
            "verification_record_sha256": record_digest,
            "verification_method_summary": method,
            "findings": findings,
        },
        "attribution_evidence_count": len(attribution_evidence),
        "local_trust_state": {
            "reviewer_attribution_verified": False,
            "independence_verified": False,
        },
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


def validate_reviewer_trust_verification_intake(
    intake: Mapping[str, Any],
    *,
    external_admission_intake: Mapping[str, Any],
    reverification_packet: Mapping[str, Any],
) -> dict[str, object]:
    """Validate external findings while preserving local fail-closed state."""

    _validate_reverification_packet(reverification_packet)

    if intake.get("record_type") != RECORD_TYPE:
        _fail("TRUST_INTAKE_RECORD_TYPE_MISMATCH")
    if intake.get("status") != STATUS:
        _fail("TRUST_INTAKE_STATUS_MISMATCH")
    if intake.get("controller_issue") != EXPECTED_CONTROLLER_ISSUE:
        _fail("TRUST_INTAKE_CONTROLLER_MISMATCH")

    bindings = intake.get("bindings")
    if not isinstance(bindings, Mapping):
        _fail("TRUST_INTAKE_BINDINGS_MISSING")
    if bindings.get("external_admission_intake_sha256") != record_sha256(external_admission_intake):
        _fail("TRUST_INTAKE_EXTERNAL_ADMISSION_BINDING_MISMATCH")
    if bindings.get("reverification_packet_sha256") != record_sha256(reverification_packet):
        _fail("TRUST_INTAKE_REVERIFICATION_BINDING_MISMATCH")

    verification = intake.get("external_verification")
    if not isinstance(verification, Mapping):
        _fail("TRUST_INTAKE_EXTERNAL_VERIFICATION_MISSING")
    _nonempty(verification.get("verifier_identity"), "TRUST_INTAKE_VERIFIER_IDENTITY_MISSING")
    _timestamp(verification.get("verified_at"))
    _nonempty(
        verification.get("verification_record_uri"),
        "TRUST_INTAKE_VERIFICATION_RECORD_URI_MISSING",
    )
    _sha256(
        verification.get("verification_record_sha256"),
        "TRUST_INTAKE_VERIFICATION_RECORD_SHA_INVALID",
    )
    _nonempty(
        verification.get("verification_method_summary"),
        "TRUST_INTAKE_VERIFICATION_METHOD_MISSING",
    )

    findings = verification.get("findings")
    if not isinstance(findings, Mapping):
        _fail("TRUST_INTAKE_FINDINGS_MISSING")
    if set(findings) != {"reviewer_attribution", "independence"}:
        _fail("TRUST_INTAKE_FINDING_FIELDS_MISMATCH")
    for finding in findings.values():
        if finding not in _FINDINGS:
            _fail("TRUST_INTAKE_FINDING_INVALID")

    attribution_evidence = reverification_packet.get("reviewer_attribution_evidence")
    if not isinstance(attribution_evidence, list) or not attribution_evidence:
        _fail("TRUST_INTAKE_ATTRIBUTION_EVIDENCE_MISSING")
    if intake.get("attribution_evidence_count") != len(attribution_evidence):
        _fail("TRUST_INTAKE_ATTRIBUTION_EVIDENCE_COUNT_MISMATCH")

    if intake.get("local_trust_state") != {
        "reviewer_attribution_verified": False,
        "independence_verified": False,
    }:
        _fail("TRUST_INTAKE_LOCAL_TRUST_PROMOTION")

    boundary = {
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
        if intake.get(field) != expected:
            _fail(f"TRUST_INTAKE_BOUNDARY_DRIFT_{field.upper()}")

    return {
        "record_type": "AOSS_STAGE_A_REVIEWER_TRUST_VERIFICATION_INTAKE_REPORT",
        "intake_validation": "PASS_EXTERNAL_TRUST_FINDINGS_STRUCTURAL_ONLY",
        "external_findings": dict(findings),
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
