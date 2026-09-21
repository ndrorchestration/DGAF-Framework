"""Canonical candidate evidence for an observed AOSS Stage-A installed environment.

This module captures and validates reviewable environment evidence without
accepting the environment or changing collection readiness.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Mapping

from scripts.aoss_stage_a.runtime_binding import (
    EXPECTED_IMPLEMENTATION,
    EXPECTED_LOCK_SHA256,
    EXPECTED_VERSION,
    RuntimeFacts,
    inspect_runtime_facts,
)

RECORD_TYPE = "AOSS_V0_6_STAGE_A_INSTALLED_ENVIRONMENT_EVIDENCE_CANDIDATE"
STATUS = "OBSERVED_CANDIDATE_NOT_ACCEPTED"

_REQUIRED_EVIDENCE_FIELDS = {
    "interpreter_implementation",
    "interpreter_version",
    "dependency_lock_sha256",
    "platform_system",
    "platform_machine",
    "executable",
    "prefix",
    "base_prefix",
    "environment_observed_at",
}


class InstalledEnvironmentEvidenceError(ValueError):
    """Raised when candidate environment evidence is malformed or overclaims."""


def _fail(code: str) -> None:
    raise InstalledEnvironmentEvidenceError(code)


def _canonical_digest(evidence: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        dict(evidence),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def capture_installed_environment_evidence_candidate(
    *,
    observed_at: str,
    facts: RuntimeFacts | None = None,
) -> dict[str, object]:
    """Capture exact runtime facts as candidate evidence, never as acceptance."""

    observed = facts or inspect_runtime_facts()
    evidence = {
        "interpreter_implementation": observed.implementation,
        "interpreter_version": observed.version,
        "dependency_lock_sha256": EXPECTED_LOCK_SHA256,
        "platform_system": observed.platform_system,
        "platform_machine": observed.platform_machine,
        "executable": observed.executable,
        "prefix": observed.prefix,
        "base_prefix": observed.base_prefix,
        "environment_observed_at": observed_at,
    }
    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": 901,
        "evidence": evidence,
        "evidence_sha256": _canonical_digest(evidence),
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }


def validate_installed_environment_evidence_candidate(
    candidate: Mapping[str, Any],
) -> dict[str, object]:
    """Validate candidate bytes and exact runtime binding without accepting them."""

    if candidate.get("record_type") != RECORD_TYPE:
        _fail("ENVIRONMENT_EVIDENCE_RECORD_TYPE_MISMATCH")
    if candidate.get("status") != STATUS:
        _fail("ENVIRONMENT_EVIDENCE_STATUS_MUST_REMAIN_UNACCEPTED")
    if candidate.get("controller_issue") != 901:
        _fail("ENVIRONMENT_EVIDENCE_CONTROLLER_MISMATCH")

    evidence = candidate.get("evidence")
    if not isinstance(evidence, Mapping):
        _fail("ENVIRONMENT_EVIDENCE_OBJECT_MISSING")
    if set(evidence) != _REQUIRED_EVIDENCE_FIELDS:
        _fail("ENVIRONMENT_EVIDENCE_FIELD_SET_MISMATCH")

    if evidence.get("interpreter_implementation") != EXPECTED_IMPLEMENTATION:
        _fail("ENVIRONMENT_INTERPRETER_IMPLEMENTATION_MISMATCH")
    if evidence.get("interpreter_version") != EXPECTED_VERSION:
        _fail("ENVIRONMENT_INTERPRETER_VERSION_MISMATCH")
    if evidence.get("dependency_lock_sha256") != EXPECTED_LOCK_SHA256:
        _fail("ENVIRONMENT_DEPENDENCY_LOCK_MISMATCH")

    for field in (
        "platform_system",
        "platform_machine",
        "executable",
        "prefix",
        "base_prefix",
    ):
        value = evidence.get(field)
        if not isinstance(value, str) or not value:
            _fail(f"ENVIRONMENT_{field.upper()}_MISSING")

    timestamp = evidence.get("environment_observed_at")
    if not isinstance(timestamp, str) or not timestamp:
        _fail("ENVIRONMENT_OBSERVED_AT_MISSING")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        _fail("ENVIRONMENT_OBSERVED_AT_INVALID")
    if parsed.tzinfo is None:
        _fail("ENVIRONMENT_OBSERVED_AT_NOT_OFFSET_AWARE")

    expected_digest = _canonical_digest(evidence)
    if candidate.get("evidence_sha256") != expected_digest:
        _fail("ENVIRONMENT_EVIDENCE_DIGEST_MISMATCH")

    if candidate.get("installed_environment_acceptance") != "NOT_ESTABLISHED":
        _fail("ENVIRONMENT_ACCEPTANCE_PREMATURE")
    if candidate.get("source_driver_binding") != "NOT_ESTABLISHED":
        _fail("SOURCE_DRIVER_BINDING_PREMATURE")
    if candidate.get("execution_allowed") is not False:
        _fail("EXECUTION_PREMATURE")
    if candidate.get("collection_execution_readiness") != "NOT_ESTABLISHED":
        _fail("COLLECTION_READINESS_PREMATURE")
    if candidate.get("outcomes_generated") is not False:
        _fail("OUTCOME_GENERATION_PREMATURE")
    if candidate.get("scientific_n_increment") != 0:
        _fail("SCIENTIFIC_N_INCREMENT_INVALID")

    return {
        "record_type": "AOSS_STAGE_A_INSTALLED_ENVIRONMENT_EVIDENCE_CANDIDATE_REPORT",
        "candidate_validation": "PASS_OBSERVED_CANDIDATE_NOT_ACCEPTED",
        "evidence_sha256": expected_digest,
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
