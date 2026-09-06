"""In-process blinding-key lease for the bounded DGAF Mode-T admission lane.

The lease is deliberately separate from the current H/I pilot key-ingress path.
It may be created only from an already admitted Confidential Space attestation
result and refuses known externally injected operational-secret variables.

The raw key is kept in a mutable bytearray and is not returned to callers.
Callers receive only HMAC operations needed for blinded identifiers/scheduling.
Zeroization in Python is best-effort: interpreter/runtime copies outside this
buffer cannot be proven absent. Final P4 acceptance therefore still depends on
real TEE execution and independent leakage review.

Scientific boundary: engineering/synthetic only. This module does not establish
P4 custody, freeze, authorization, unblinding, or empirical evidence.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re
import secrets
from typing import Any, Mapping


KEY_BYTES = 32
FORBIDDEN_EXTERNAL_SECRET_ENV = (
    "PDMAL_BLINDING_KEY",
    "PDMAL_MODE_T_KEY",
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ModeTKeyError(RuntimeError):
    """Raised when the in-process Mode-T key boundary fails closed."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ModeTKeyError(message)


def _require_sha256(value: Any, label: str) -> str:
    _require(isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None, f"{label} must be lowercase SHA-256 hex")
    return value


def _validate_admission(admission: Mapping[str, Any]) -> tuple[str, str, str]:
    _require(isinstance(admission, Mapping), "attestation admission must be an object")
    _require(admission.get("attestation_contract") == "PASS", "attestation contract is not PASS")
    _require(admission.get("signature_verified") is True, "attestation signature is not verified")
    _require(admission.get("hardware_model") == "GCP_INTEL_TDX", "attested hardware is not GCP_INTEL_TDX")
    _require(admission.get("debug_status") == "disabled-since-boot", "attested debug state is not production")
    _require(admission.get("restart_policy") == "Never", "attested restart policy is not Never")
    token_sha = _require_sha256(admission.get("token_sha256"), "token_sha256")
    consumption_sha = _require_sha256(
        admission.get("authorization_consumption_sha256"), "authorization_consumption_sha256"
    )
    manifest_sha = _require_sha256(admission.get("output_manifest_sha256"), "output_manifest_sha256")
    return token_sha, consumption_sha, manifest_sha


def _reject_external_secret_environment(environment: Mapping[str, str]) -> None:
    for name in FORBIDDEN_EXTERNAL_SECRET_ENV:
        if name in environment:
            raise ModeTKeyError(f"external operational-secret environment variable is forbidden: {name}")


class ModeTKeyLease:
    """Attestation-bound, non-serializable, best-effort-zeroized key lease."""

    __slots__ = (
        "_material",
        "_destroyed",
        "token_sha256",
        "authorization_consumption_sha256",
        "output_manifest_sha256",
    )

    def __init__(
        self,
        material: bytearray,
        *,
        token_sha256: str,
        authorization_consumption_sha256: str,
        output_manifest_sha256: str,
    ) -> None:
        if len(material) != KEY_BYTES:
            raise ModeTKeyError(f"Mode-T key must contain exactly {KEY_BYTES} bytes")
        self._material = material
        self._destroyed = False
        self.token_sha256 = token_sha256
        self.authorization_consumption_sha256 = authorization_consumption_sha256
        self.output_manifest_sha256 = output_manifest_sha256

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

    def hmac_sha256(self, message: bytes) -> bytes:
        """Return HMAC-SHA256 without exposing the raw key to the caller."""
        if self._destroyed:
            raise ModeTKeyError("Mode-T key lease is destroyed")
        if not isinstance(message, bytes):
            raise ModeTKeyError("HMAC message must be bytes")
        return hmac.new(self._material, message, hashlib.sha256).digest()

    def destroy(self) -> None:
        """Best-effort overwrite of the owned mutable key buffer."""
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


def acquire_mode_t_key(
    admission: Mapping[str, Any],
    *,
    environment: Mapping[str, str] | None = None,
) -> ModeTKeyLease:
    """Generate a 256-bit operational key only after attestation admission.

    The entropy source is Python's ``secrets.token_bytes``, backed by the OS
    cryptographic randomness provider. Tests may monkeypatch that function, but
    production callers cannot supply an alternate entropy source through this
    API.
    """

    token_sha, consumption_sha, manifest_sha = _validate_admission(admission)
    _reject_external_secret_environment(os.environ if environment is None else environment)

    generated = secrets.token_bytes(KEY_BYTES)
    _require(isinstance(generated, bytes), "CSPRNG did not return bytes")
    _require(len(generated) == KEY_BYTES, "CSPRNG returned an unexpected key length")
    material = bytearray(generated)

    return ModeTKeyLease(
        material,
        token_sha256=token_sha,
        authorization_consumption_sha256=consumption_sha,
        output_manifest_sha256=manifest_sha,
    )
