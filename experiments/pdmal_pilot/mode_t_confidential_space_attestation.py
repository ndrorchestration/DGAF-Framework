"""Fail-closed claim contract for DGAF Mode-T Confidential Space admission.

This module evaluates claims only after a separate cryptographic token-signature
verification step has succeeded. It deliberately does not parse or validate JWT
signatures itself; callers must provide ``signature_verified=True`` only after an
independent verifier has authenticated the token.

The lifecycle has two non-interchangeable attestation phases:

* PRE_EXECUTION binds the admitted runtime to the already-consumed authorization
  record C and is the only phase that may gate operational-key generation.
* POST_EXECUTION binds the same admitted runtime identity to the final blinded
  output/evidence manifest after that manifest exists.

Scientific boundary: engineering / synthetic admission checking only. Importing
or passing this module does not establish P4 custody, freeze, authorization, or
empirical evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping


GOOGLE_CLOUD_ATTESTATION_ISSUER = "https://confidentialcomputing.googleapis.com"
CONFIDENTIAL_SPACE_SWNAME = "CONFIDENTIAL_SPACE"
REQUIRED_HARDWARE_MODEL = "GCP_INTEL_TDX"
REQUIRED_ATTESTER_TCB = ("INTEL",)
REQUIRED_DEBUG_STATUS = "disabled-since-boot"
REQUIRED_RESTART_POLICY = "Never"
REQUIRED_SUPPORT_ATTRIBUTE = "STABLE"
PRE_EXECUTION = "PRE_EXECUTION"
POST_EXECUTION = "POST_EXECUTION"
ATTESTATION_PHASES = frozenset({PRE_EXECUTION, POST_EXECUTION})
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_IMAGE_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class AttestationContractError(ValueError):
    """Raised when a Mode-T attestation fails the admission contract."""


@dataclass(frozen=True)
class AttestationExpectation:
    """Exact non-secret values frozen before one attestation is accepted."""

    phase: str
    audience: str
    image_digest: str
    binding_sha256: str
    expected_args: tuple[str, ...]
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
    _require(
        isinstance(value, int) and not isinstance(value, bool),
        f"{label} must be an integer",
    )
    return value


def _sha256(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{label} must be lowercase SHA-256 hex",
    )
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


def _runtime_identity_sha256(runtime_identity: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        runtime_identity,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def verify_confidential_space_attestation(
    claims: Mapping[str, Any],
    expectation: AttestationExpectation,
    token_context: VerifiedTokenContext,
) -> dict[str, Any]:
    """Verify one exact DGAF Mode-T Confidential Space attestation phase.

    Returns normalized non-secret evidence on success. Any missing, malformed,
    stale, or mismatched security-critical value raises
    ``AttestationContractError``.
    """

    _require(
        token_context.signature_verified is True,
        "cryptographic token signature is not verified",
    )
    token_sha256 = _sha256(token_context.token_sha256, "token_sha256")
    now = _integer(token_context.verified_at_unix, "verified_at_unix")

    _require(
        expectation.phase in ATTESTATION_PHASES,
        "attestation phase must be PRE_EXECUTION or POST_EXECUTION",
    )
    _require(
        isinstance(expectation.audience, str) and bool(expectation.audience),
        "attestation audience must be non-empty",
    )
    _require(
        isinstance(expectation.image_digest, str)
        and _IMAGE_DIGEST_RE.fullmatch(expectation.image_digest) is not None,
        "image_digest must be sha256:<lowercase-hex>",
    )
    binding_sha256 = _sha256(expectation.binding_sha256, "binding_sha256")
    _require(
        expectation.max_clock_skew_seconds >= 0,
        "max_clock_skew_seconds must be non-negative",
    )

    root = _mapping(claims, "claims")
    _require(
        root.get("iss") == GOOGLE_CLOUD_ATTESTATION_ISSUER,
        "unexpected attestation issuer",
    )
    _require(root.get("aud") == expectation.audience, "attestation audience mismatch")
    _require(
        root.get("swname") == CONFIDENTIAL_SPACE_SWNAME,
        "software identity is not CONFIDENTIAL_SPACE",
    )
    _require(
        root.get("hwmodel") == REQUIRED_HARDWARE_MODEL,
        "hardware model is not GCP_INTEL_TDX",
    )
    _require(
        root.get("attester_tcb") == list(REQUIRED_ATTESTER_TCB),
        "TDX attester_tcb must be exactly ['INTEL']",
    )
    _require(root.get("secboot") is True, "secure boot is not attested true")
    _require(
        root.get("dbgstat") == REQUIRED_DEBUG_STATUS,
        "debug status is not production disabled-since-boot",
    )

    iat = _integer(root.get("iat"), "iat")
    nbf = _integer(root.get("nbf"), "nbf")
    exp = _integer(root.get("exp"), "exp")
    skew = expectation.max_clock_skew_seconds
    _require(iat <= now + skew, "attestation issued in the future beyond allowed skew")
    _require(nbf <= now + skew, "attestation not yet valid")
    _require(exp > now - skew, "attestation expired")
    _require(exp > iat, "attestation expiration must be after issue time")
    _require(exp > nbf, "attestation expiration must be after not-before time")

    submods = _mapping(root.get("submods"), "submods")
    container = _mapping(submods.get("container"), "submods.container")
    confidential_space = _mapping(
        submods.get("confidential_space"),
        "submods.confidential_space",
    )

    support_attributes = confidential_space.get("support_attributes")
    _require(
        isinstance(support_attributes, list)
        and all(isinstance(item, str) for item in support_attributes),
        "support_attributes must be a list of strings",
    )
    _require(
        REQUIRED_SUPPORT_ATTRIBUTE in support_attributes,
        "production image is not attested STABLE",
    )

    monitoring = _mapping(
        confidential_space.get("monitoring_enabled"),
        "submods.confidential_space.monitoring_enabled",
    )
    _require(
        dict(monitoring) == {"memory": False},
        "Confidential Space memory monitoring must be exactly disabled",
    )

    _require(
        container.get("image_digest") == expectation.image_digest,
        "workload image digest mismatch",
    )
    _require(
        container.get("restart_policy") == REQUIRED_RESTART_POLICY,
        "restart policy must be Never",
    )

    args = container.get("args")
    _require(
        isinstance(args, list) and all(isinstance(item, str) for item in args),
        "container args must be a list of strings",
    )
    _require(tuple(args) == expectation.expected_args, "container args mismatch")

    cmd_override = container.get("cmd_override")
    _require(
        isinstance(cmd_override, list)
        and all(isinstance(item, str) for item in cmd_override),
        "cmd_override must be a list of strings",
    )
    _require(
        tuple(cmd_override) == expectation.expected_cmd_override,
        "command override mismatch",
    )

    env = _mapping(container.get("env"), "submods.container.env")
    _require(
        dict(env) == dict(expectation.expected_env),
        "explicit environment does not exactly match frozen non-secret inputs",
    )

    env_override = _mapping(
        container.get("env_override"),
        "submods.container.env_override",
    )
    _require(len(env_override) == 0, "environment overrides are not permitted")

    nonces = _nonce_values(root.get("eat_nonce"))
    _require(len(nonces) == 1, "exactly one phase-specific attestation nonce is required")
    _require(nonces[0] == binding_sha256, "attestation nonce binding mismatch")

    runtime_identity = {
        "audience": expectation.audience,
        "software_identity": CONFIDENTIAL_SPACE_SWNAME,
        "hardware_model": REQUIRED_HARDWARE_MODEL,
        "attester_tcb": list(REQUIRED_ATTESTER_TCB),
        "secure_boot": True,
        "debug_status": REQUIRED_DEBUG_STATUS,
        "support_attribute": REQUIRED_SUPPORT_ATTRIBUTE,
        "memory_monitoring": False,
        "image_digest": expectation.image_digest,
        "container_args": list(expectation.expected_args),
        "command_override": list(expectation.expected_cmd_override),
        "environment": dict(expectation.expected_env),
        "environment_override": {},
        "restart_policy": REQUIRED_RESTART_POLICY,
    }
    runtime_identity_sha256 = _runtime_identity_sha256(runtime_identity)

    result = {
        "attestation_contract": "PASS",
        "attestation_phase": expectation.phase,
        "issuer": GOOGLE_CLOUD_ATTESTATION_ISSUER,
        "runtime_identity": runtime_identity,
        "runtime_identity_sha256": runtime_identity_sha256,
        "binding_sha256": binding_sha256,
        "token_sha256": token_sha256,
        "signature_verified": True,
        "issued_at_unix": iat,
        "verified_at_unix": now,
        "authorization_consumption_sha256": None,
        "output_manifest_sha256": None,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_data_collection": False,
        "empirical_n": 0,
    }
    if expectation.phase == PRE_EXECUTION:
        result["authorization_consumption_sha256"] = binding_sha256
    else:
        result["output_manifest_sha256"] = binding_sha256
    return result


def verify_two_phase_attestation_binding(
    pre_execution: Mapping[str, Any],
    post_execution: Mapping[str, Any],
    *,
    authorization_consumption_sha256: str,
    output_manifest_sha256: str,
) -> dict[str, Any]:
    """Bind two independently verified tokens to one admitted runtime lineage."""

    expected_c = _sha256(
        authorization_consumption_sha256,
        "authorization_consumption_sha256",
    )
    expected_manifest = _sha256(output_manifest_sha256, "output_manifest_sha256")

    pre = _mapping(pre_execution, "pre_execution")
    post = _mapping(post_execution, "post_execution")
    _require(pre.get("attestation_contract") == "PASS", "pre-execution attestation is not PASS")
    _require(post.get("attestation_contract") == "PASS", "post-execution attestation is not PASS")
    _require(pre.get("signature_verified") is True, "pre-execution signature is not verified")
    _require(post.get("signature_verified") is True, "post-execution signature is not verified")
    _require(pre.get("attestation_phase") == PRE_EXECUTION, "first token is not PRE_EXECUTION")
    _require(post.get("attestation_phase") == POST_EXECUTION, "second token is not POST_EXECUTION")
    _require(
        pre.get("authorization_consumption_sha256") == expected_c,
        "pre-execution C binding mismatch",
    )
    _require(
        post.get("output_manifest_sha256") == expected_manifest,
        "post-execution manifest binding mismatch",
    )
    _require(
        pre.get("runtime_identity_sha256") == post.get("runtime_identity_sha256"),
        "pre/post runtime identity mismatch",
    )

    pre_token = _sha256(pre.get("token_sha256"), "pre token_sha256")
    post_token = _sha256(post.get("token_sha256"), "post token_sha256")
    _require(pre_token != post_token, "pre/post attestation tokens must be distinct")

    pre_iat = _integer(pre.get("issued_at_unix"), "pre issued_at_unix")
    post_iat = _integer(post.get("issued_at_unix"), "post issued_at_unix")
    _require(post_iat >= pre_iat, "post-execution token predates pre-execution token")

    return {
        "two_phase_attestation_binding": "PASS",
        "runtime_identity_sha256": pre.get("runtime_identity_sha256"),
        "authorization_consumption_sha256": expected_c,
        "output_manifest_sha256": expected_manifest,
        "pre_execution_token_sha256": pre_token,
        "post_execution_token_sha256": post_token,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_data_collection": False,
        "empirical_n": 0,
    }
