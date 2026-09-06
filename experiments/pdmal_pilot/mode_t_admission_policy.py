"""Canonical admission-policy identity for DGAF Mode-T Confidential Space.

Issue #316 identified a trust-boundary gap: authenticating a Google-signed token
against a caller-supplied ``AttestationExpectation`` does not prove that the
expectation itself was the launch policy authorized before execution.

This module defines one canonical security-critical policy identity. Synthetic R/A/C
records bind its SHA-256 and the synthetic key path verifies that binding before token
admission/key generation. Production remains fail-closed until an independently
retained C/policy evidence verifier exists; caller-supplied booleans/digests do not
substitute for that trust source.
"""
from __future__ import annotations

import hashlib
import json
import re
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
from mode_t_google_oidc_verifier import GoogleOIDCVerifier
from mode_t_inprocess_key import (
    ModeTKeyAcquisition,
    admit_and_acquire_mode_t_key_synthetic,
)

POLICY_SCHEMA = "DGAF_MODE_T_CONFIDENTIAL_SPACE_ADMISSION_POLICY_V1"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ModeTAdmissionPolicyError(ValueError):
    """Raised when an admission-policy identity is malformed or mismatched."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ModeTAdmissionPolicyError(message)


def _sha(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{label} must be lowercase SHA-256 hex",
    )
    return value


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        dict(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def canonical_admission_policy(expectation: AttestationExpectation) -> dict[str, Any]:
    """Return security-critical launch policy independent of run-specific nonce C."""
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
    _sha(expected_sha256, "expected admission_policy_sha256")
    actual = admission_policy_sha256(expectation)
    if actual != expected_sha256:
        raise ModeTAdmissionPolicyError(
            "supplied PRE_EXECUTION expectation does not match pre-authorized admission policy"
        )
    return actual


def _verify_synthetic_consumption_record(
    consumption: Mapping[str, Any],
) -> tuple[str, str]:
    _require(isinstance(consumption, Mapping), "consumption evidence must be an object")
    data = dict(consumption)
    claimed = _sha(
        data.pop("consumption_evidence_sha256", None),
        "consumption_evidence_sha256",
    )
    actual = hashlib.sha256(canonical_json_bytes(data)).hexdigest()
    _require(actual == claimed, "synthetic C digest does not match record")
    _require(
        data.get("record_type") == "PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION",
        "wrong consumption record type",
    )
    _require(
        data.get("status") == "CONSUMED_PRE_SECRET_SYNTHETIC",
        "consumption record is not the synthetic pre-secret state",
    )
    _require(data.get("synthetic_only") is True, "consumption record must be synthetic")
    _require(
        data.get("retention_status")
        == "SYNTHETIC_MODEL_ONLY_NOT_INDEPENDENTLY_RETAINED",
        "synthetic C retention marker is missing or promoted",
    )
    return claimed, _sha(data.get("admission_policy_sha256"), "admission_policy_sha256")


def admit_and_acquire_mode_t_key_synthetic_policy_bound(
    token: str | bytes,
    expectation: AttestationExpectation,
    consumption: Mapping[str, Any],
    *,
    verifier: GoogleOIDCVerifier,
    environment: Mapping[str, str] | None = None,
    verified_at_unix: int | None = None,
) -> ModeTKeyAcquisition:
    """Synthetic-only gate proving C binds the exact supplied PRE launch policy."""
    c_sha, policy_sha = _verify_synthetic_consumption_record(consumption)
    _require(
        expectation.phase == PRE_EXECUTION,
        "policy-bound synthetic key path requires PRE_EXECUTION expectation",
    )
    _require(
        expectation.binding_sha256 == c_sha,
        "PRE_EXECUTION expectation does not bind the exact synthetic C record",
    )
    require_admission_policy_sha256(expectation, policy_sha)
    return admit_and_acquire_mode_t_key_synthetic(
        token,
        expectation,
        verifier=verifier,
        environment=environment,
        verified_at_unix=verified_at_unix,
    )


def require_production_retained_policy_verifier() -> None:
    """Fail closed until independent C/policy retention is a real trust source."""
    raise ModeTAdmissionPolicyError(
        "production admission requires independently retained C/policy evidence verifier"
    )
