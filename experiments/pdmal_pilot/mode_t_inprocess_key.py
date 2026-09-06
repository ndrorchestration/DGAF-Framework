"""Attestation-gated in-process key lease for the bounded DGAF Mode-T lane.

The production entry point accepts a raw Confidential Space token, authenticates the
Google signing-key path, evaluates the exact PRE_EXECUTION claim contract, re-hashes
the normalized runtime identity, and only then generates operational key material.
It never accepts caller-assembled ``signature_verified`` or key-source dictionaries
as the production trust boundary.

Synthetic tests use a separate explicitly synthetic path. The raw key remains inside
an owned mutable bytearray and is never returned. Best-effort zeroization cannot prove
that Python/runtime internals made no transient copies. Real P4 acceptance therefore
still requires real TEE execution and independent leakage review.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
import os
import re
import secrets
from typing import Any, Mapping

from mode_t_confidential_space_attestation import (
    AttestationExpectation,
    PRE_EXECUTION,
    verify_confidential_space_attestation,
)
from mode_t_google_oidc_verifier import (
    PRODUCTION_TRANSPORT,
    SYNTHETIC_TRANSPORT,
    GoogleOIDCVerifier,
    VerifiedGoogleOIDCToken,
    verify_google_confidential_space_token,
)

KEY_BYTES = 32
FORBIDDEN_EXTERNAL_SECRET_ENV = (
    "PDMAL_BLINDING_KEY",
    "PDMAL_MODE_T_KEY",
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
BLIND_IDENTIFIER_DOMAIN = b"DGAF-MODE-T-BLIND-ID-V1\x00"
ORDER_TOKEN_DOMAIN = b"DGAF-MODE-T-ORDER-V1\x00"
KEY_COMMITMENT_DOMAIN = b"DGAF-MODE-T-KEY-COMMITMENT-V1\x00"


class ModeTKeyError(RuntimeError):
    """Raised when the in-process Mode-T key boundary fails closed."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ModeTKeyError(message)


def _require_sha256(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{label} must be lowercase SHA-256 hex",
    )
    return value


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _runtime_identity_sha256(runtime: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        dict(runtime),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_pre_execution_admission(
    admission: Mapping[str, Any],
) -> tuple[str, str, str]:
    _require(isinstance(admission, Mapping), "attestation admission must be an object")
    _require(admission.get("attestation_contract") == "PASS", "attestation contract is not PASS")
    _require(
        admission.get("attestation_phase") == PRE_EXECUTION,
        "Mode-T key generation requires PRE_EXECUTION attestation",
    )
    _require(admission.get("signature_verified") is True, "attestation signature is not verified")

    token_sha = _require_sha256(admission.get("token_sha256"), "token_sha256")
    consumption_sha = _require_sha256(
        admission.get("authorization_consumption_sha256"),
        "authorization_consumption_sha256",
    )
    binding_sha = _require_sha256(admission.get("binding_sha256"), "binding_sha256")
    _require(
        binding_sha == consumption_sha,
        "PRE_EXECUTION binding is not the authorization-consumption digest",
    )
    _require(
        admission.get("output_manifest_sha256") is None,
        "PRE_EXECUTION admission must not contain an output-manifest binding",
    )

    runtime_sha = _require_sha256(
        admission.get("runtime_identity_sha256"),
        "runtime_identity_sha256",
    )
    runtime = _require_mapping(admission.get("runtime_identity"), "runtime_identity")
    _require(
        _runtime_identity_sha256(runtime) == runtime_sha,
        "runtime identity digest does not match normalized runtime",
    )
    _require(runtime.get("software_identity") == "CONFIDENTIAL_SPACE", "attested software identity is not CONFIDENTIAL_SPACE")
    _require(runtime.get("hardware_model") == "GCP_INTEL_TDX", "attested hardware is not GCP_INTEL_TDX")
    _require(runtime.get("secure_boot") is True, "attested secure boot is not true")
    _require(runtime.get("debug_status") == "disabled-since-boot", "attested debug state is not production")
    _require(runtime.get("memory_monitoring") is False, "attested memory monitoring is not disabled")
    _require(runtime.get("restart_policy") == "Never", "attested restart policy is not Never")
    return token_sha, consumption_sha, runtime_sha


def _validate_verified_token(
    verified: VerifiedGoogleOIDCToken,
    *,
    token_sha256: str,
    production: bool,
) -> None:
    _require(
        isinstance(verified, VerifiedGoogleOIDCToken),
        "verified token must be a VerifiedGoogleOIDCToken",
    )
    _require(verified.token_context.signature_verified is True, "key-source token signature is not verified")
    _require(
        _require_sha256(verified.token_context.token_sha256, "verified token_sha256") == token_sha256,
        "verified token digest does not match PRE_EXECUTION token",
    )
    transport = verified.key_source.transport_authentication
    if production:
        _require(
            transport == PRODUCTION_TRANSPORT,
            "production Mode-T key generation requires authenticated production Google key source",
        )
    else:
        _require(
            transport == SYNTHETIC_TRANSPORT,
            "synthetic Mode-T key generation requires explicit synthetic key-source evidence",
        )


def _reject_external_secret_environment(environment: Mapping[str, str]) -> None:
    _require(isinstance(environment, Mapping), "environment must be a mapping")
    for name in FORBIDDEN_EXTERNAL_SECRET_ENV:
        if name in environment:
            raise ModeTKeyError(
                f"external operational-secret environment variable is forbidden: {name}"
            )


class ModeTKeyLease:
    """Non-serializable, best-effort-zeroized operational key capability."""

    __slots__ = (
        "_material",
        "_destroyed",
        "token_sha256",
        "authorization_consumption_sha256",
        "runtime_identity_sha256",
    )

    def __init__(
        self,
        material: bytearray,
        *,
        token_sha256: str,
        authorization_consumption_sha256: str,
        runtime_identity_sha256: str,
    ) -> None:
        if len(material) != KEY_BYTES:
            raise ModeTKeyError(f"Mode-T key must contain exactly {KEY_BYTES} bytes")
        self._material = material
        self._destroyed = False
        self.token_sha256 = token_sha256
        self.authorization_consumption_sha256 = authorization_consumption_sha256
        self.runtime_identity_sha256 = runtime_identity_sha256

    def __repr__(self) -> str:
        state = "destroyed" if self._destroyed else "active"
        return f"ModeTKeyLease(state={state}, material=<redacted>)"

    def __getstate__(self) -> None:
        raise TypeError("ModeTKeyLease serialization is prohibited")

    def __reduce__(self) -> None:
        raise TypeError("ModeTKeyLease serialization is prohibited")

    @property
    def destroyed(self) -> bool:
        return self._destroyed

    def _hmac(self, domain: bytes, message: bytes) -> bytes:
        if self._destroyed:
            raise ModeTKeyError("Mode-T key lease is destroyed")
        if not isinstance(message, bytes):
            raise ModeTKeyError("HMAC message must be bytes")
        return hmac.new(self._material, domain + message, hashlib.sha256).digest()

    def blind_identifier(self, clear_identifier: str) -> str:
        if not isinstance(clear_identifier, str) or not clear_identifier:
            raise ModeTKeyError("clear identifier must be a non-empty string")
        return self._hmac(BLIND_IDENTIFIER_DOMAIN, clear_identifier.encode("utf-8")).hex()

    def order_token(self, ordinal_material: bytes) -> str:
        return self._hmac(ORDER_TOKEN_DOMAIN, ordinal_material).hex()

    def key_commitment(self, commitment_nonce: bytes) -> str:
        if not isinstance(commitment_nonce, bytes) or len(commitment_nonce) < 16:
            raise ModeTKeyError("commitment nonce must contain at least 128 bits")
        return self._hmac(KEY_COMMITMENT_DOMAIN, commitment_nonce).hex()

    def destroy(self) -> None:
        if self._destroyed:
            return
        for index in range(len(self._material)):
            self._material[index] = 0
        self._destroyed = True

    def __enter__(self) -> "ModeTKeyLease":
        if self._destroyed:
            raise ModeTKeyError("cannot re-enter a destroyed Mode-T key lease")
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> bool:
        self.destroy()
        return False


@dataclass(frozen=True)
class ModeTKeyAcquisition:
    """One admitted PRE context plus its live key lease and retention-safe evidence."""

    lease: ModeTKeyLease
    pre_execution: Mapping[str, Any]
    token_evidence: Mapping[str, Any]

    def __getstate__(self) -> None:
        raise TypeError("ModeTKeyAcquisition serialization is prohibited")


def _acquire_from_verified(
    pre_execution_admission: Mapping[str, Any],
    verified: VerifiedGoogleOIDCToken,
    *,
    environment: Mapping[str, str] | None,
    production: bool,
) -> ModeTKeyLease:
    token_sha, consumption_sha, runtime_sha = _validate_pre_execution_admission(
        pre_execution_admission
    )
    _validate_verified_token(verified, token_sha256=token_sha, production=production)
    _reject_external_secret_environment(os.environ if environment is None else environment)
    generated = secrets.token_bytes(KEY_BYTES)
    _require(isinstance(generated, bytes), "CSPRNG did not return bytes")
    _require(len(generated) == KEY_BYTES, "CSPRNG returned an unexpected key length")
    return ModeTKeyLease(
        bytearray(generated),
        token_sha256=token_sha,
        authorization_consumption_sha256=consumption_sha,
        runtime_identity_sha256=runtime_sha,
    )


def admit_and_acquire_mode_t_key(
    token: str | bytes,
    expectation: AttestationExpectation,
    *,
    environment: Mapping[str, str] | None = None,
    verified_at_unix: int | None = None,
) -> ModeTKeyAcquisition:
    """Production entry: authenticate raw token, admit PRE claims, then generate key."""
    _require(expectation.phase == PRE_EXECUTION, "production key path requires PRE_EXECUTION expectation")
    verified = verify_google_confidential_space_token(
        token,
        verified_at_unix=verified_at_unix,
    )
    pre = verify_confidential_space_attestation(
        verified.claims,
        expectation,
        verified.token_context,
    )
    lease = _acquire_from_verified(
        pre,
        verified,
        environment=environment,
        production=True,
    )
    return ModeTKeyAcquisition(lease, pre, verified.evidence())


def admit_and_acquire_mode_t_key_synthetic(
    token: str | bytes,
    expectation: AttestationExpectation,
    *,
    verifier: GoogleOIDCVerifier,
    environment: Mapping[str, str] | None = None,
    verified_at_unix: int | None = None,
) -> ModeTKeyAcquisition:
    """Explicit synthetic test path using an injected synthetic verifier."""
    _require(expectation.phase == PRE_EXECUTION, "synthetic key path requires PRE_EXECUTION expectation")
    verified = verifier.verify(token, verified_at_unix=verified_at_unix)
    pre = verify_confidential_space_attestation(
        verified.claims,
        expectation,
        verified.token_context,
    )
    lease = _acquire_from_verified(
        pre,
        verified,
        environment=environment,
        production=False,
    )
    return ModeTKeyAcquisition(lease, pre, verified.evidence())


def acquire_mode_t_key_synthetic_from_verified(
    pre_execution_admission: Mapping[str, Any],
    verified: VerifiedGoogleOIDCToken,
    *,
    environment: Mapping[str, str] | None = None,
) -> ModeTKeyLease:
    """Test-only seam for adversarial mutation tests after normalization."""
    return _acquire_from_verified(
        pre_execution_admission,
        verified,
        environment=environment,
        production=False,
    )
