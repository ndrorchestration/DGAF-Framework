"""Side-effect-free Sigstore/Cosign verifier for DGAF Mode-T retention evidence.

This extracts the verification half of the existing #299 Rekor timing apparatus so
#323 does not need to trust caller-asserted Sigstore booleans. It verifies an existing
artifact+bundle with a checksum-pinned Cosign executable and exact certificate
identity/OIDC issuer, then normalizes only the metadata consumed by the retention
contract.

It never signs, requests OIDC, uploads to Rekor, or writes external evidence. A PASS
is cryptographic bundle/inclusion verification only; it does not prove durable
retention, temporal order, P4, freeze, authorization, or empirical execution.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Mapping

from mode_t_retention_contract import VerifiedTransparencyContext

EXPECTED_COSIGN_VERSION = "v3.1.3"
EXPECTED_COSIGN_LINUX_AMD64_SHA256 = (
    "4629c757b7618056f8ddd7e2625ae9fdd94c0372a65049520bc7d9df9efc7f71"
)
EXPECTED_OIDC_ISSUER = "https://token.actions.githubusercontent.com"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class SigstoreVerifierError(RuntimeError):
    """Raised when local Sigstore verification cannot be established exactly."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SigstoreVerifierError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    _require(path.is_file(), f"file missing: {path}")
    return sha256_bytes(path.read_bytes())


def _json_file(path: Path, label: str) -> Mapping[str, Any]:
    _require(path.is_file(), f"{label} missing")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SigstoreVerifierError(f"{label} is not valid UTF-8 JSON") from exc
    _require(isinstance(value, Mapping), f"{label} must be a JSON object")
    return value


def _run_cosign_verify(
    *,
    cosign: Path,
    artifact: Path,
    bundle: Path,
    certificate_identity: str,
    oidc_issuer: str,
    timeout_seconds: int,
) -> None:
    _require(timeout_seconds > 0, "timeout_seconds must be positive")
    _require(cosign.is_file(), "Cosign executable is missing")
    _require(artifact.is_file(), "artifact is missing")
    _require(bundle.is_file(), "Sigstore bundle is missing")
    _require(bool(certificate_identity), "certificate identity must be non-empty")
    _require(oidc_issuer == EXPECTED_OIDC_ISSUER, "unexpected certificate OIDC issuer")

    command = [
        str(cosign),
        "verify-blob",
        "--bundle",
        str(bundle),
        "--certificate-identity",
        certificate_identity,
        "--certificate-oidc-issuer",
        oidc_issuer,
        str(artifact),
    ]
    try:
        proc = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise SigstoreVerifierError("Cosign verification process failed") from exc
    if proc.returncode != 0:
        raise SigstoreVerifierError(
            f"Cosign verify-blob rejected artifact/bundle with exit code {proc.returncode}"
        )


def _first_tlog_entry(bundle: Mapping[str, Any]) -> Mapping[str, Any]:
    material = bundle.get("verificationMaterial")
    _require(isinstance(material, Mapping), "bundle missing verificationMaterial")
    entries = material.get("tlogEntries")
    _require(isinstance(entries, list) and len(entries) == 1, "bundle must contain exactly one transparency-log entry")
    entry = entries[0]
    _require(isinstance(entry, Mapping), "invalid transparency-log entry")
    return entry


def _nonnegative_integer(value: Any, label: str) -> int:
    _require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"{label} must be a non-negative integer")
    return value


def normalize_verified_bundle(
    *,
    artifact: Path,
    bundle: Path,
    certificate_identity: str,
    oidc_issuer: str = EXPECTED_OIDC_ISSUER,
) -> VerifiedTransparencyContext:
    """Normalize metadata only after external Cosign cryptographic verification passed."""
    artifact_sha = sha256_file(artifact)
    bundle_raw = bundle.read_bytes()
    bundle_sha = sha256_bytes(bundle_raw)
    parsed = _json_file(bundle, "Sigstore bundle")
    entry = _first_tlog_entry(parsed)

    log_index = _nonnegative_integer(entry.get("logIndex"), "logIndex")
    integrated_time = entry.get("integratedTime")
    if integrated_time is not None:
        integrated_time = _nonnegative_integer(integrated_time, "integratedTime")

    inclusion = entry.get("inclusionProof")
    promise = entry.get("inclusionPromise")
    _require(
        isinstance(inclusion, Mapping) or isinstance(promise, Mapping),
        "transparency entry has neither inclusion proof nor inclusion promise",
    )
    # Cosign verify-blob is the cryptographic source of truth for signature,
    # certificate chain/identity, SET/inclusion semantics, and artifact binding.
    # This parser does not independently reinterpret those cryptographic fields.
    log_id = entry.get("logId")
    if isinstance(log_id, Mapping):
        log_id = log_id.get("keyId")
    _require(isinstance(log_id, str) and bool(log_id), "transparency log identity missing")

    return VerifiedTransparencyContext(
        signature_verified=True,
        certificate_chain_verified=True,
        certificate_identity_verified=True,
        transparency_inclusion_verified=True,
        signed_entry_timestamp_verified=True,
        bundle_sha256=bundle_sha,
        log_entry_uuid=log_id,
        log_index=log_index,
        integrated_time_unix=integrated_time,
        verified_record_sha256=artifact_sha,
        certificate_identity=certificate_identity,
        oidc_issuer=oidc_issuer,
    )


def verify_sigstore_bundle(
    *,
    cosign: Path,
    expected_cosign_sha256: str,
    artifact: Path,
    bundle: Path,
    certificate_identity: str,
    oidc_issuer: str = EXPECTED_OIDC_ISSUER,
    timeout_seconds: int = 60,
) -> VerifiedTransparencyContext:
    """Verify existing bytes/bundle with pinned Cosign; perform no external write."""
    _require(
        _SHA256_RE.fullmatch(expected_cosign_sha256) is not None,
        "expected Cosign SHA-256 must be lowercase hex",
    )
    actual_cosign_sha = sha256_file(cosign)
    _require(
        actual_cosign_sha == expected_cosign_sha256,
        "Cosign executable SHA-256 does not match reviewed identity",
    )
    _run_cosign_verify(
        cosign=cosign,
        artifact=artifact,
        bundle=bundle,
        certificate_identity=certificate_identity,
        oidc_issuer=oidc_issuer,
        timeout_seconds=timeout_seconds,
    )
    return normalize_verified_bundle(
        artifact=artifact,
        bundle=bundle,
        certificate_identity=certificate_identity,
        oidc_issuer=oidc_issuer,
    )


def retention_safe_evidence(
    context: VerifiedTransparencyContext,
    *,
    cosign_sha256: str,
) -> dict[str, Any]:
    """Return non-secret evidence without claiming retention or temporal closure."""
    return {
        "sigstore_crypto_verified": True,
        "cosign_version_policy": EXPECTED_COSIGN_VERSION,
        "cosign_sha256": cosign_sha256,
        "bundle_sha256": context.bundle_sha256,
        "verified_record_sha256": context.verified_record_sha256,
        "certificate_identity": context.certificate_identity,
        "certificate_oidc_issuer": context.oidc_issuer,
        "log_entry_identity": context.log_entry_uuid,
        "log_index": context.log_index,
        "integrated_time_unix_metadata_only": context.integrated_time_unix,
        "external_write_performed_by_verifier": False,
        "oidc_token_requested_by_verifier": False,
        "real_external_retention_established": False,
        "temporal_order_verified": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }
