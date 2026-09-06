"""Canonical static admission-policy identity for the bounded DGAF Mode-T lane.

This module separates the *static security policy* from per-phase attestation bindings.
PRE/POST phase and nonce/binding digests deliberately do not change the policy identity;
audience, VM subject, service accounts, image identity, argv/environment expectations,
security profile, restart policy, and clock-skew policy do.

The current v1 identity is engineering/synthetic evidence only. A signed-token lifetime
upper-bound policy is still under review, and independently retained production R/A/C
verification does not yet exist. Therefore a matching digest cannot establish P4,
freeze, pilot authorization, or real admission by itself.
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
    REQUIRED_ATTESTER_TCB,
    REQUIRED_DEBUG_STATUS,
    REQUIRED_HARDWARE_MODEL,
    REQUIRED_RESTART_POLICY,
    REQUIRED_SUPPORT_ATTRIBUTE,
)

POLICY_SCHEMA = "dgaf-mode-t-admission-policy-v1"
TOKEN_LIFETIME_POLICY = "OPEN_REVIEW_NOT_PRODUCTION_COMPLETE"
SYNTHETIC_RETENTION_STATUS = "SYNTHETIC_MODEL_ONLY_NOT_INDEPENDENTLY_RETAINED"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_IMAGE_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class AdmissionPolicyError(ValueError):
    """Raised when an admission policy or policy-bound synthetic C fails closed."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AdmissionPolicyError(message)


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        dict(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def _strings(values: Any, label: str, *, nonempty: bool = False) -> list[str]:
    _require(isinstance(values, (tuple, list)), f"{label} must be a list/tuple")
    result = list(values)
    if nonempty:
        _require(bool(result), f"{label} must be non-empty")
    _require(all(isinstance(item, str) for item in result), f"{label} must contain strings")
    return result


def admission_policy_identity(expectation: AttestationExpectation) -> dict[str, Any]:
    """Return the canonical static policy preimage for one reviewed expectation.

    ``phase`` and ``binding_sha256`` are intentionally excluded because PRE binds C and
    POST binds the output manifest while both phases must share one static admission
    policy. The exact expectation values themselves remain fully security-sensitive.
    """
    _require(isinstance(expectation, AttestationExpectation), "expectation has wrong type")
    _require(isinstance(expectation.audience, str) and bool(expectation.audience), "audience must be non-empty")
    _require(len(expectation.audience.encode("utf-8")) <= 512, "audience exceeds Google token limit")
    _require(isinstance(expectation.subject, str) and bool(expectation.subject), "subject must be non-empty")

    accounts = _strings(expectation.expected_service_accounts, "expected_service_accounts", nonempty=True)
    _require(len(set(accounts)) == len(accounts), "expected service accounts must be unique")
    args = _strings(expectation.expected_args, "expected_args")
    cmd_override = _strings(expectation.expected_cmd_override, "expected_cmd_override")

    _require(
        isinstance(expectation.image_digest, str)
        and _IMAGE_DIGEST_RE.fullmatch(expectation.image_digest) is not None,
        "image_digest must be sha256:<lowercase-hex>",
    )
    _require(
        isinstance(expectation.max_clock_skew_seconds, int)
        and not isinstance(expectation.max_clock_skew_seconds, bool)
        and expectation.max_clock_skew_seconds >= 0,
        "max_clock_skew_seconds must be a non-negative integer",
    )

    _require(isinstance(expectation.expected_env, Mapping), "expected_env must be an object")
    env = dict(expectation.expected_env)
    _require(
        all(isinstance(key, str) and isinstance(value, str) for key, value in env.items()),
        "expected_env keys and values must be strings",
    )

    return {
        "schema_version": POLICY_SCHEMA,
        "issuer": GOOGLE_CLOUD_ATTESTATION_ISSUER,
        "oemid": GOOGLE_CLOUD_OEM_ID,
        "audience": expectation.audience,
        "subject": expectation.subject,
        "google_service_accounts": sorted(accounts),
        "software_identity": CONFIDENTIAL_SPACE_SWNAME,
        "hardware_model": REQUIRED_HARDWARE_MODEL,
        "attester_tcb": list(REQUIRED_ATTESTER_TCB),
        "secure_boot_required": True,
        "debug_status": REQUIRED_DEBUG_STATUS,
        "required_support_attribute": REQUIRED_SUPPORT_ATTRIBUTE,
        "memory_monitoring_required": False,
        "container": {
            "image_digest": expectation.image_digest,
            "args": args,
            "cmd_override": cmd_override,
            "env": env,
            "env_override": {},
            "restart_policy": REQUIRED_RESTART_POLICY,
        },
        "max_clock_skew_seconds": expectation.max_clock_skew_seconds,
        "token_lifetime_upper_bound_seconds": None,
        "token_lifetime_policy": TOKEN_LIFETIME_POLICY,
        "production_policy_complete": False,
    }


def admission_policy_sha256(expectation: AttestationExpectation) -> str:
    """Hash the canonical static policy identity."""
    return hashlib.sha256(_canonical_bytes(admission_policy_identity(expectation))).hexdigest()


def verify_synthetic_consumption_policy_binding(
    consumption: Mapping[str, Any],
    expectation: AttestationExpectation,
) -> dict[str, Any]:
    """Prove a synthetic C carries the exact policy digest expected by the caller.

    This explicitly rejects promotion to production because the synthetic C is not
    independently retained and the v1 token-lifetime policy remains open review.
    """
    _require(isinstance(consumption, Mapping), "consumption must be an object")
    claimed = consumption.get("admission_policy_sha256")
    _require(
        isinstance(claimed, str) and _SHA256_RE.fullmatch(claimed) is not None,
        "consumption admission_policy_sha256 is invalid",
    )
    expected = admission_policy_sha256(expectation)
    _require(claimed == expected, "consumption is bound to a different admission policy")
    _require(consumption.get("synthetic_only") is True, "synthetic policy binding requires synthetic C")
    _require(
        consumption.get("retention_status") == SYNTHETIC_RETENTION_STATUS,
        "unexpected synthetic C retention status",
    )
    return {
        "admission_policy_binding": "PASS_SYNTHETIC_ONLY",
        "admission_policy_sha256": expected,
        "independent_retention_verified": False,
        "production_policy_complete": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }
