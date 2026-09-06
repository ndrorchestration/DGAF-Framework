"""Fail-closed claim contract for DGAF Mode-T Confidential Space admission.

This module evaluates claims only after a separate cryptographic token-signature
verification step has succeeded. It deliberately does not parse or validate JWT
signatures itself; callers must provide ``signature_verified=True`` only after an
independent verifier has authenticated the token.

Scientific boundary: engineering / synthetic admission checking only. Importing
or passing this module does not establish P4 custody, freeze, authorization, or
empirical evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping


GOOGLE_CLOUD_ATTESTATION_ISSUER = "https://confidentialcomputing.googleapis.com"
CONFIDENTIAL_SPACE_SWNAME = "CONFIDENTIAL_SPACE"
REQUIRED_HARDWARE_MODEL = "GCP_INTEL_TDX"
REQUIRED_DEBUG_STATUS = "disabled-since-boot"
REQUIRED_RESTART_POLICY = "Never"
REQUIRED_SUPPORT_ATTRIBUTE = "STABLE"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class AttestationContractError(ValueError):
    """Raised when a Mode-T attestation fails the admission contract."""


@dataclass(frozen=True)
class AttestationExpectation:
    """Exact non-secret values frozen before a candidate attestation is accepted."""

    image_digest: str
    authorization_consumption_sha256: str
    output_manifest_sha256: str
    expected_env: Mapping[str, str]
    expected_cmd_override: tuple[str, ...] = ()
    max_clock_skew_seconds: int = 60


@dataclass(frozen=True)
class VerifiedTokenContext:
    """Result metadata from the separate cryptographic token-verification layer."""

    signature_verified: bool
    token_sha256: str
    verified_at_unix: int


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AttestationContractError(message)


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _integer(value: Any, label: str) -> int:
    _require(isinstance(value, int) and not isinstance(value, bool), f"{label} must be an integer")
    return value


def _sha256(value: str, label: str) -> str:
    _require(isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None, f"{label} must be lowercase SHA-256 hex")
    return value


def _nonce_values(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        values = (value,)
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        values = tuple(value)
    else:
        raise AttestationContractError("eat_nonce must be a string or list of strings")
    for index, item in enumerate(values):
        _sha256(item, f"eat_nonce[{index}]")
    return values


def verify_confidential_space_attestation(
    claims: Mapping[str, Any],
    expectation: AttestationExpectation,
    token_context: VerifiedTokenContext,
) -> dict[str, Any]:
    """Verify the exact DGAF Mode-T Confidential Space claim contract.

    Returns a normalized non-secret evidence dictionary on success. Any missing,
    malformed, unexpected, stale, or mismatched security-critical value raises
    ``AttestationContractError``.
    """

    _require(token_context.signature_verified is True, "cryptographic token signature is not verified")
    token_sha256 = _sha256(token_context.token_sha256, "token_sha256")
    now = _integer(token_context.verified_at_unix, "verified_at_unix")

    _sha256(expectation.authorization_consumption_sha256, "authorization_consumption_sha256")
    _sha256(expectation.output_manifest_sha256, "output_manifest_sha256")
    _require(isinstance(expectation.image_digest, str) and expectation.image_digest, "image_digest must be non-empty")
    _require(expectation.max_clock_skew_seconds >= 0, "max_clock_skew_seconds must be non-negative")

    root = _mapping(claims, "claims")
    _require(root.get("iss") == GOOGLE_CLOUD_ATTESTATION_ISSUER, "unexpected attestation issuer")
    _require(root.get("swname") == CONFIDENTIAL_SPACE_SWNAME, "software identity is not CONFIDENTIAL_SPACE")
    _require(root.get("hwmodel") == REQUIRED_HARDWARE_MODEL, "hardware model is not GCP_INTEL_TDX")
    _require(root.get("dbgstat") == REQUIRED_DEBUG_STATUS, "debug status is not production disabled-since-boot")

    iat = _integer(root.get("iat"), "iat")
    nbf = _integer(root.get("nbf"), "nbf")
    exp = _integer(root.get("exp"), "exp")
    skew = expectation.max_clock_skew_seconds
    _require(iat <= now + skew, "attestation issued in the future beyond allowed skew")
    _require(nbf <= now + skew, "attestation not yet valid")
    _require(exp > now - skew, "attestation expired")
    _require(exp > iat, "attestation expiration must be after issue time")

    submods = _mapping(root.get("submods"), "submods")
    container = _mapping(submods.get("container"), "submods.container")
    confidential_space = _mapping(submods.get("confidential_space"), "submods.confidential_space")

    support_attributes = confidential_space.get("support_attributes")
    _require(
        isinstance(support_attributes, list) and all(isinstance(item, str) for item in support_attributes),
        "support_attributes must be a list of strings",
    )
    _require(REQUIRED_SUPPORT_ATTRIBUTE in support_attributes, "production image is not attested STABLE")

    _require(container.get("image_digest") == expectation.image_digest, "workload image digest mismatch")
    _require(container.get("restart_policy") == REQUIRED_RESTART_POLICY, "restart policy must be Never")

    cmd_override = container.get("cmd_override")
    _require(isinstance(cmd_override, list) and all(isinstance(item, str) for item in cmd_override), "cmd_override must be a list of strings")
    _require(tuple(cmd_override) == expectation.expected_cmd_override, "command override mismatch")

    env = _mapping(container.get("env"), "submods.container.env")
    _require(dict(env) == dict(expectation.expected_env), "explicit environment does not exactly match frozen non-secret inputs")

    env_override = _mapping(container.get("env_override"), "submods.container.env_override")
    _require(len(env_override) == 0, "environment overrides are not permitted")

    nonces = _nonce_values(root.get("eat_nonce"))
    _require(len(nonces) == 2, "exactly two attestation nonces are required")
    _require(len(set(nonces)) == 2, "attestation nonces must be unique")
    expected_nonces = {
        expectation.authorization_consumption_sha256,
        expectation.output_manifest_sha256,
    }
    _require(set(nonces) == expected_nonces, "attestation nonce binding mismatch")

    return {
        "attestation_contract": "PASS",
        "issuer": GOOGLE_CLOUD_ATTESTATION_ISSUER,
        "software_identity": CONFIDENTIAL_SPACE_SWNAME,
        "hardware_model": REQUIRED_HARDWARE_MODEL,
        "debug_status": REQUIRED_DEBUG_STATUS,
        "support_attribute": REQUIRED_SUPPORT_ATTRIBUTE,
        "image_digest": expectation.image_digest,
        "restart_policy": REQUIRED_RESTART_POLICY,
        "authorization_consumption_sha256": expectation.authorization_consumption_sha256,
        "output_manifest_sha256": expectation.output_manifest_sha256,
        "token_sha256": token_sha256,
        "signature_verified": True,
        "verified_at_unix": now,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_data_collection": False,
        "empirical_n": 0,
    }
