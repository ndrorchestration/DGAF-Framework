"""Side-effect-free Sigstore/Cosign verifier for DGAF Mode-T retention evidence.

The public entry verifies an existing artifact+standardized Sigstore bundle with the
exact reviewed Cosign v3.1.3 Linux/amd64 binary, exact certificate/GitHub-workflow
identity, and an explicit predeclared TrustedRoot file. Ambient/default trust-material
acquisition is not accepted by this wrapper.

A matching TrustedRoot digest proves byte identity only. It does not prove that the
root or its TUF/bootstrap/update policy was independently approved. That governance
acceptance remains external and fail-closed.

This module never signs, requests OIDC, uploads to Rekor, or writes external evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Mapping

from mode_t_retention_contract import (
    EXPECTED_GITHUB_WORKFLOW_REF,
    EXPECTED_GITHUB_WORKFLOW_REPOSITORY,
    EXPECTED_OIDC_ISSUER,
    TransparencyExpectation,
    VerifiedTransparencyContext,
    verify_transparency_inclusion,
)

EXPECTED_COSIGN_VERSION = "v3.1.3"
EXPECTED_COSIGN_LINUX_AMD64_SHA256 = (
    "4629c757b7618056f8ddd7e2625ae9fdd94c0372a65049520bc7d9df9efc7f71"
)
_ALLOWED_BUNDLE_MEDIA_TYPES = frozenset(
    {
        "application/vnd.dev.sigstore.bundle.v0.3+json",
        "application/vnd.dev.sigstore.bundle+json;version=0.3",
    }
)
_UINT_DECIMAL_RE = re.compile(r"^(?:0|[1-9][0-9]*)$")


class SigstoreVerifierError(RuntimeError):
    """Raised when local Sigstore verification cannot be established exactly."""


@dataclass(frozen=True)
class VerifiedSigstoreRetention:
    """Cryptographically established retention input plus bounded normalized result."""

    transparency: VerifiedTransparencyContext
    retention_result: Mapping[str, Any]
    cosign_version: str
    cosign_sha256: str
    trusted_root_sha256: str


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


def _verify_cosign_binary(cosign: Path) -> str:
    actual = sha256_file(cosign)
    _require(
        actual == EXPECTED_COSIGN_LINUX_AMD64_SHA256,
        "Cosign executable SHA-256 does not match pinned v3.1.3 Linux/amd64 identity",
    )
    return actual


def _verify_trusted_root(
    *,
    trusted_root: Path,
    expectation: TransparencyExpectation,
) -> str:
    """Require explicit JSON trust material with exact predeclared byte identity."""
    _json_file(trusted_root, "Sigstore TrustedRoot")
    actual = sha256_file(trusted_root)
    _require(
        actual == expectation.trusted_root_sha256,
        "TrustedRoot SHA-256 does not match predeclared expectation",
    )
    return actual


def _run_cosign_verify(
    *,
    cosign: Path,
    artifact: Path,
    bundle: Path,
    trusted_root: Path,
    expectation: TransparencyExpectation,
    timeout_seconds: int,
) -> None:
    _require(timeout_seconds > 0, "timeout_seconds must be positive")
    _require(cosign.is_file(), "Cosign executable is missing")
    _require(artifact.is_file(), "artifact is missing")
    _require(bundle.is_file(), "Sigstore bundle is missing")
    _require(trusted_root.is_file(), "Sigstore TrustedRoot is missing")
    _require(bool(expectation.certificate_identity), "certificate identity must be non-empty")
    _require(
        expectation.oidc_issuer == EXPECTED_OIDC_ISSUER,
        "unexpected certificate OIDC issuer expectation",
    )
    _require(
        expectation.github_workflow_repository == EXPECTED_GITHUB_WORKFLOW_REPOSITORY,
        "unexpected GitHub workflow repository expectation",
    )
    _require(
        expectation.github_workflow_ref == EXPECTED_GITHUB_WORKFLOW_REF,
        "unexpected GitHub workflow ref expectation",
    )

    command = [
        str(cosign),
        "verify-blob",
        "--bundle",
        str(bundle),
        "--trusted-root",
        str(trusted_root),
        "--certificate-identity",
        expectation.certificate_identity,
        "--certificate-oidc-issuer",
        EXPECTED_OIDC_ISSUER,
        "--certificate-github-workflow-sha",
        expectation.github_workflow_sha,
        "--certificate-github-workflow-repository",
        EXPECTED_GITHUB_WORKFLOW_REPOSITORY,
        "--certificate-github-workflow-ref",
        EXPECTED_GITHUB_WORKFLOW_REF,
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


def _standardized_v03_bundle(bundle: Mapping[str, Any]) -> None:
    media_type = bundle.get("mediaType")
    _require(
        isinstance(media_type, str) and media_type in _ALLOWED_BUNDLE_MEDIA_TYPES,
        "Sigstore bundle must use the reviewed standardized v0.3 media type",
    )


def _first_tlog_entry(bundle: Mapping[str, Any]) -> Mapping[str, Any]:
    material = bundle.get("verificationMaterial")
    _require(isinstance(material, Mapping), "bundle missing verificationMaterial")
    entries = material.get("tlogEntries")
    _require(
        isinstance(entries, list) and len(entries) == 1,
        "bundle must contain exactly one transparency-log entry",
    )
    entry = entries[0]
    _require(isinstance(entry, Mapping), "invalid transparency-log entry")
    return entry


def _nonnegative_integer(value: Any, label: str) -> int:
    if isinstance(value, bool):
        raise SigstoreVerifierError(f"{label} must be a canonical non-negative integer")
    if isinstance(value, int):
        _require(value >= 0, f"{label} must be a canonical non-negative integer")
        return value
    if isinstance(value, str):
        _require(
            _UINT_DECIMAL_RE.fullmatch(value) is not None,
            f"{label} must be a canonical non-negative integer",
        )
        return int(value, 10)
    raise SigstoreVerifierError(f"{label} must be a canonical non-negative integer")


def _normalize_verified_bundle(
    *,
    artifact: Path,
    bundle: Path,
    trusted_root_sha256: str,
    expectation: TransparencyExpectation,
) -> VerifiedTransparencyContext:
    """Parse metadata only after private Cosign verification has succeeded."""
    artifact_sha = sha256_file(artifact)
    bundle_raw = bundle.read_bytes()
    bundle_sha = sha256_bytes(bundle_raw)
    parsed = _json_file(bundle, "Sigstore bundle")
    _standardized_v03_bundle(parsed)
    entry = _first_tlog_entry(parsed)

    log_index = _nonnegative_integer(entry.get("logIndex"), "logIndex")
    integrated_time = entry.get("integratedTime")
    if integrated_time is not None:
        integrated_time = _nonnegative_integer(integrated_time, "integratedTime")

    inclusion = entry.get("inclusionProof")
    _require(
        isinstance(inclusion, Mapping) and bool(inclusion),
        "reviewed retention evidence requires a transparency-log inclusion proof",
    )

    log_id = entry.get("logId")
    _require(isinstance(log_id, Mapping), "transparency log identity missing")
    log_id_key_id = log_id.get("keyId")
    _require(
        isinstance(log_id_key_id, str) and bool(log_id_key_id),
        "transparency log key identity missing",
    )

    return VerifiedTransparencyContext(
        signature_verified=True,
        certificate_chain_verified=True,
        certificate_identity_verified=True,
        transparency_inclusion_verified=True,
        signed_entry_timestamp_verified=True,
        bundle_sha256=bundle_sha,
        trusted_root_sha256=trusted_root_sha256,
        log_id_key_id=log_id_key_id,
        log_index=log_index,
        integrated_time_unix=integrated_time,
        verified_record_sha256=artifact_sha,
        certificate_identity=expectation.certificate_identity,
        oidc_issuer=EXPECTED_OIDC_ISSUER,
        github_workflow_sha=expectation.github_workflow_sha,
        github_workflow_repository=EXPECTED_GITHUB_WORKFLOW_REPOSITORY,
        github_workflow_ref=EXPECTED_GITHUB_WORKFLOW_REF,
    )


def verify_retention_record_with_sigstore(
    *,
    expectation: TransparencyExpectation,
    cosign: Path,
    artifact: Path,
    bundle: Path,
    trusted_root: Path,
    timeout_seconds: int = 60,
) -> VerifiedSigstoreRetention:
    """Cryptographically verify one predeclared DGAF retention record, read-only."""
    _require(isinstance(expectation, TransparencyExpectation), "expectation has wrong type")
    cosign_sha = _verify_cosign_binary(cosign)
    trusted_root_sha = _verify_trusted_root(
        trusted_root=trusted_root,
        expectation=expectation,
    )
    _run_cosign_verify(
        cosign=cosign,
        artifact=artifact,
        bundle=bundle,
        trusted_root=trusted_root,
        expectation=expectation,
        timeout_seconds=timeout_seconds,
    )
    context = _normalize_verified_bundle(
        artifact=artifact,
        bundle=bundle,
        trusted_root_sha256=trusted_root_sha,
        expectation=expectation,
    )
    retention = verify_transparency_inclusion(expectation, context)
    return VerifiedSigstoreRetention(
        transparency=context,
        retention_result=retention,
        cosign_version=EXPECTED_COSIGN_VERSION,
        cosign_sha256=cosign_sha,
        trusted_root_sha256=trusted_root_sha,
    )


def retention_safe_evidence(verified: VerifiedSigstoreRetention) -> dict[str, Any]:
    """Return non-secret evidence without claiming root approval or temporal closure."""
    _require(
        isinstance(verified, VerifiedSigstoreRetention),
        "verified Sigstore retention result required",
    )
    context = verified.transparency
    return {
        "sigstore_crypto_verified": True,
        "cosign_version_policy": verified.cosign_version,
        "cosign_sha256": verified.cosign_sha256,
        "trusted_root_sha256": verified.trusted_root_sha256,
        "trusted_root_explicit_and_digest_bound": True,
        "trusted_root_independently_approved": False,
        "bundle_sha256": context.bundle_sha256,
        "verified_record_sha256": context.verified_record_sha256,
        "certificate_identity": context.certificate_identity,
        "certificate_oidc_issuer": context.oidc_issuer,
        "github_workflow_sha": context.github_workflow_sha,
        "github_workflow_repository": context.github_workflow_repository,
        "github_workflow_ref": context.github_workflow_ref,
        "transparency_log_id_key_id": context.log_id_key_id,
        "log_index": context.log_index,
        "integrated_time_unix_metadata_only": context.integrated_time_unix,
        "cryptographic_inclusion_verified_by_this_module": True,
        "external_write_performed_by_verifier": False,
        "oidc_token_requested_by_verifier": False,
        "real_external_retention_established": False,
        "temporal_order_verified": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }
