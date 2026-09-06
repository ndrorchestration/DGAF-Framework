"""Canonical admission-policy identity for DGAF Mode-T Confidential Space.

Issue #316 identified a trust-boundary gap: authenticating a Google-signed token
against a caller-supplied ``AttestationExpectation`` does not prove that the
expectation itself was the launch policy authorized before execution.

This module defines one canonical security-critical policy identity. Synthetic R/A/C
records may bind its SHA-256. Production use must additionally verify that C/policy
binding from an independently retained evidence source; a caller-supplied boolean or
digest is not accepted as a substitute for independent retention.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from mode_t_confidential_space_attestation import (
    AttestationExpectation,
    CONFIDENTIAL_SPACE_SWNAME,
    GOOGLE_CLOUD_ATTESTATION_ISSUER,
    GOOGLE_CLOUD_OEM_ID,
    PRE_EXECUTION,
    REQUIRED_ATTESTER_TCB,
    REQUIRED_DEBUG_STATUS,
    REQUIRED_HARDWARE_MODEL,
    REQUIRED_RESTART_POLICY,
    REQUIRED_SUPPORT_ATTRIBUTE,
)

POLICY_SCHEMA = "DGAF_MODE_T_CONFIDENTIAL_SPACE_ADMISSION_POLICY_V1"


class ModeTAdmissionPolicyError(ValueError):
    """Raised when an admission-policy identity is malformed or mismatched."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ModeTAdmissionPolicyError(message)


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        dict(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def canonical_admission_policy(expectation: AttestationExpectation) -> dict[str, Any]:
    """Return the security-critical launch policy independent of run-specific nonce C.

    ``binding_sha256`` is intentionally excluded because C does not exist when the
    launch policy is frozen. ``phase`` is fixed here to PRE_EXECUTION. POST must bind
    back to this same policy identity through the output manifest/two-phase lineage.
    """
    _require(
        isinstance(expectation, AttestationExpectation),
        "expectation must be AttestationExpectation",
    )
    _require(
        expectation.phase == PRE_EXECUTION,
        "canonical admission policy must be derived from PRE_EXECUTION expectation",
    )
    _require(
        isinstance(expectation.max_clock_skew_seconds, int)
        and not isinstance(expectation.max_clock_skew_seconds, bool)
        and expectation.max_clock_skew_seconds >= 0,
        "max_clock_skew_seconds must be a non-negative integer",
    )
    _require(bool(expectation.audience), "audience must be non-empty")
    _require(bool(expectation.subject), "subject must be non-empty")
    _require(bool(expectation.expected_service_accounts), "service-account set must be non-empty")
    _require(
        len(set(expectation.expected_service_accounts))
        == len(expectation.expected_service_accounts),
        "service-account set contains duplicates",
    )

    return {
        "policy_schema": POLICY_SCHEMA,
        "issuer": GOOGLE_CLOUD_ATTESTATION_ISSUER,
        "google_oem_id": GOOGLE_CLOUD_OEM_ID,
        "software_identity": CONFIDENTIAL_SPACE_SWNAME,
        "hardware_model": REQUIRED_HARDWARE_MODEL,
        "attester_tcb": list(REQUIRED_ATTESTER_TCB),
        "required_support_attribute": REQUIRED_SUPPORT_ATTRIBUTE,
        "secure_boot_required": True,
        "debug_status": REQUIRED_DEBUG_STATUS,
        "memory_monitoring_required": False,
        "restart_policy": REQUIRED_RESTART_POLICY,
        "audience": expectation.audience,
        "subject": expectation.subject,
        "service_accounts": sorted(expectation.expected_service_accounts),
        "workload_image_digest": expectation.image_digest,
        "container_args": list(expectation.expected_args),
        "command_override": list(expectation.expected_cmd_override),
        "explicit_non_secret_environment": dict(sorted(expectation.expected_env.items())),
        "environment_override_allowed": False,
        "max_clock_skew_seconds": expectation.max_clock_skew_seconds,
        "token_lifetime_policy": "SIGNED_IAT_NBF_EXP_REQUIRED_AND_CHECKED",
        "operational_secret_environment_allowed": False,
    }


def admission_policy_sha256(expectation: AttestationExpectation) -> str:
    return hashlib.sha256(canonical_json_bytes(canonical_admission_policy(expectation))).hexdigest()


def require_admission_policy_sha256(
    expectation: AttestationExpectation,
    expected_sha256: str,
) -> str:
    actual = admission_policy_sha256(expectation)
    if actual != expected_sha256:
        raise ModeTAdmissionPolicyError(
            "supplied PRE_EXECUTION expectation does not match pre-authorized admission policy"
        )
    return actual


def require_production_retained_policy_verifier() -> None:
    """Explicit fail-closed marker for the still-missing production trust source.

    The synthetic R/A/C model cannot satisfy independent retention. Production code
    must not turn a caller-provided mapping/digest/boolean into equivalent evidence.
    """
    raise ModeTAdmissionPolicyError(
        "production admission requires independently retained C/policy evidence verifier"
    )
