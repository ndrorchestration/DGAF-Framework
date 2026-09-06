"""Policy-bound synthetic key-acquisition bridge for the DGAF Mode-T lane.

This module closes a synthetic integration seam: callers must not be able to verify a
synthetic C/policy binding as an optional side step and then bypass it by directly
calling the synthetic key-acquisition primitive.

The bridge verifies the C seal, requires PRE to bind the exact C digest, verifies the
canonical static admission-policy digest carried by C, and only then enters the
existing synthetic OIDC/attestation/key path.

It is intentionally synthetic-only. It does not implement the independently retained
production C/policy evidence source required by issue #316 and cannot establish P4,
freeze, pilot authorization, or empirical execution.
"""
from __future__ import annotations

import re
from typing import Any, Mapping

from mode_t_admission_policy import (
    AdmissionPolicyError,
    verify_synthetic_consumption_policy_binding,
)
from mode_t_confidential_space_attestation import AttestationExpectation, PRE_EXECUTION
from mode_t_google_oidc_verifier import GoogleOIDCVerifier
from mode_t_inprocess_key import ModeTKeyAcquisition, admit_and_acquire_mode_t_key_synthetic
from mode_t_integrated_lifecycle import canonical_sha256

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AdmissionPolicyError(message)


def _verified_consumption_sha256(consumption: Mapping[str, Any]) -> str:
    _require(isinstance(consumption, Mapping), "consumption must be an object")
    sealed = dict(consumption)
    claimed = sealed.pop("consumption_evidence_sha256", None)
    _require(
        isinstance(claimed, str) and _SHA256_RE.fullmatch(claimed) is not None,
        "consumption_evidence_sha256 is invalid",
    )
    _require(
        canonical_sha256(sealed) == claimed,
        "consumption_evidence_sha256 does not match C record",
    )
    return claimed


def admit_and_acquire_mode_t_key_synthetic_from_consumption(
    token: str | bytes,
    expectation: AttestationExpectation,
    consumption: Mapping[str, Any],
    *,
    verifier: GoogleOIDCVerifier,
    environment: Mapping[str, str] | None = None,
    verified_at_unix: int | None = None,
) -> ModeTKeyAcquisition:
    """Require exact sealed synthetic C/policy binding before synthetic key generation."""
    _require(
        isinstance(expectation, AttestationExpectation),
        "expectation has wrong type",
    )
    _require(
        expectation.phase == PRE_EXECUTION,
        "policy-bound synthetic key path requires PRE_EXECUTION expectation",
    )
    c_sha = _verified_consumption_sha256(consumption)
    _require(
        expectation.binding_sha256 == c_sha,
        "PRE expectation does not bind the exact synthetic C record",
    )
    verify_synthetic_consumption_policy_binding(consumption, expectation)
    acquisition = admit_and_acquire_mode_t_key_synthetic(
        token,
        expectation,
        verifier=verifier,
        environment=environment,
        verified_at_unix=verified_at_unix,
    )
    _require(
        acquisition.lease.authorization_consumption_sha256 == c_sha,
        "key lease does not bind the exact synthetic C record",
    )
    return acquisition
