"""Fail-closed structural binding for final P4-B continuity evidence.

This module validates identities and digest relationships that Issue #295 requires in
one acceptance packet.  It deliberately cannot close Issue #295: cryptographic
verification, independent retention/retrieval, and final adjudication remain external
trust boundaries.  Synthetic fixtures may exercise this contract, but their PASS is
only a structural-schema result.
"""
from __future__ import annotations

import re
from typing import Any, Mapping

EXPECTED_REPOSITORY = "ndrorchestration/DGAF-Framework"
EXPECTED_HELPER_PATH = "experiments/pdmal_pilot/mode_t_strict_verifier.go"
EXPECTED_TLOCK_VERSION = "v1.2.0"
EXPECTED_TLOCK_SOURCE_COMMIT = "7b54141a9733fd6fa207587a11148280e6fb020d"
EXPECTED_GO_VERSION = "1.22.12"
EXPECTED_CONTINUITY_CLASS = "P4_B_MODE_T_STRICT_CONTINUITY_V1"
EXPECTED_PACKET_CLASS = "P4_B_MODE_T_FINAL_ACCEPTANCE_PACKET_V1"
EXPECTED_RETENTION_CLASS = "P6_INDEPENDENT_RETRIEVAL_REHASH_V1"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


class ContinuityAcceptanceError(ValueError):
    """Raised when a structural acceptance packet fails closed."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContinuityAcceptanceError(message)


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{label} must be non-empty")
    return value


def _sha256(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{label} must be lowercase SHA-256 hex",
    )
    return value


def _commit(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and _COMMIT_RE.fullmatch(value) is not None,
        f"{label} must be a full lowercase 40-character commit SHA",
    )
    return value


def _positive_decimal(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and value.isdecimal() and int(value) > 0,
        f"{label} must be a positive decimal string",
    )
    return value


def _require_exact_keys(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    _require(
        actual == expected,
        f"{label} keys changed; added={sorted(actual - expected)} "
        f"missing={sorted(expected - actual)}",
    )


def validate_structural_acceptance_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a complete identity graph without performing trust adjudication."""
    root = _mapping(packet, "packet")
    _require_exact_keys(
        root,
        {
            "schema_version",
            "evidence_class",
            "repository",
            "control_plane_sha",
            "helper",
            "continuity_report",
            "retention_retrieval",
            "adjudication",
            "freeze_established",
            "pilot_authorized",
            "empirical_n",
        },
        "packet",
    )
    _require(root["schema_version"] == 1, "unsupported packet schema")
    _require(root["evidence_class"] == EXPECTED_PACKET_CLASS, "unexpected packet class")
    _require(root["repository"] == EXPECTED_REPOSITORY, "unexpected repository")
    control_plane_sha = _commit(root["control_plane_sha"], "control-plane SHA")

    helper = _mapping(root["helper"], "helper")
    _require_exact_keys(
        helper,
        {
            "path",
            "source_blob_sha",
            "source_sha256",
            "binary_sha256",
            "tlock_version",
            "tlock_source_commit",
            "go_version",
            "target_os",
            "target_arch",
            "goamd64",
            "cgo_enabled",
        },
        "helper",
    )
    _require(helper["path"] == EXPECTED_HELPER_PATH, "unexpected helper path")
    source_blob_sha = _commit(helper["source_blob_sha"], "helper source blob SHA")
    source_sha256 = _sha256(helper["source_sha256"], "helper source SHA-256")
    binary_sha256 = _sha256(helper["binary_sha256"], "helper binary SHA-256")
    _require(helper["tlock_version"] == EXPECTED_TLOCK_VERSION, "unexpected tlock version")
    _require(
        helper["tlock_source_commit"] == EXPECTED_TLOCK_SOURCE_COMMIT,
        "unexpected tlock source commit",
    )
    _require(helper["go_version"] == EXPECTED_GO_VERSION, "unexpected Go version")
    _require(helper["target_os"] == "linux", "unexpected helper target OS")
    _require(helper["target_arch"] == "amd64", "unexpected helper target architecture")
    _require(helper["goamd64"] == "v1", "unexpected GOAMD64 target")
    _require(helper["cgo_enabled"] is False, "CGO must remain disabled")

    report = _mapping(root["continuity_report"], "continuity report")
    _require_exact_keys(
        report,
        {
            "report_sha256",
            "schema_version",
            "evidence_class",
            "status",
            "control_plane_sha",
            "github_run_id",
            "github_run_attempt",
            "tlock_version",
            "tlock_source_commit",
            "strict_chain_enforced",
            "ciphertext_sha256",
            "expected_plaintext_sha256",
            "plaintext_commitment_match",
            "plaintext_persisted",
            "plaintext_emitted",
            "empirical_data_collection",
            "freeze_established",
            "pilot_authorized",
            "empirical_n",
        },
        "continuity report",
    )
    report_sha256 = _sha256(report["report_sha256"], "continuity report SHA-256")
    _require(report["schema_version"] == 1, "unsupported continuity report schema")
    _require(report["evidence_class"] == EXPECTED_CONTINUITY_CLASS, "unexpected continuity class")
    _require(report["status"] == "PASS", "continuity report is not PASS")
    _require(
        _commit(report["control_plane_sha"], "report control-plane SHA")
        == control_plane_sha,
        "report control-plane SHA mismatch",
    )
    run_id = _positive_decimal(report["github_run_id"], "GitHub run ID")
    run_attempt = _positive_decimal(report["github_run_attempt"], "GitHub run attempt")
    _require(report["tlock_version"] == helper["tlock_version"], "report tlock version mismatch")
    _require(
        report["tlock_source_commit"] == helper["tlock_source_commit"],
        "report tlock source mismatch",
    )
    _require(report["strict_chain_enforced"] is True, "strict-chain enforcement missing")
    ciphertext_sha256 = _sha256(report["ciphertext_sha256"], "ciphertext SHA-256")
    expected_plaintext_sha256 = _sha256(
        report["expected_plaintext_sha256"],
        "expected plaintext commitment",
    )
    _require(report["plaintext_commitment_match"] is True, "plaintext commitment mismatch")
    _require(report["plaintext_persisted"] is False, "plaintext persistence is forbidden")
    _require(report["plaintext_emitted"] is False, "plaintext emission is forbidden")
    _require(report["empirical_data_collection"] is False, "empirical collection is forbidden")
    _require(report["freeze_established"] is False, "continuity report cannot establish freeze")
    _require(report["pilot_authorized"] is False, "continuity report cannot authorize pilot")
    _require(report["empirical_n"] == 0, "continuity report must preserve N=0")

    retention = _mapping(root["retention_retrieval"], "retention/retrieval")
    _require_exact_keys(
        retention,
        {
            "evidence_class",
            "retained_report_sha256",
            "retrieved_report_sha256",
            "retention_receipt_sha256",
            "retrieval_receipt_sha256",
            "sigstore_bundle_sha256",
            "trusted_root_sha256",
            "retention_location",
            "retrieval_actor",
            "producer_actor",
            "cryptographic_bundle_verified",
            "independent_retrieval_verified",
        },
        "retention/retrieval",
    )
    _require(retention["evidence_class"] == EXPECTED_RETENTION_CLASS, "unexpected retention class")
    retained_sha = _sha256(retention["retained_report_sha256"], "retained report SHA-256")
    retrieved_sha = _sha256(retention["retrieved_report_sha256"], "retrieved report SHA-256")
    _require(retained_sha == report_sha256, "retained report digest mismatch")
    _require(retrieved_sha == report_sha256, "retrieved report digest mismatch")
    _sha256(retention["retention_receipt_sha256"], "retention receipt SHA-256")
    _sha256(retention["retrieval_receipt_sha256"], "retrieval receipt SHA-256")
    bundle_sha256 = _sha256(retention["sigstore_bundle_sha256"], "Sigstore bundle SHA-256")
    trusted_root_sha256 = _sha256(retention["trusted_root_sha256"], "TrustedRoot SHA-256")
    _string(retention["retention_location"], "retention location")
    retrieval_actor = _string(retention["retrieval_actor"], "retrieval actor")
    producer_actor = _string(retention["producer_actor"], "producer actor")
    _require(retrieval_actor != producer_actor, "retrieval actor must differ from producer actor")
    _require(
        retention["cryptographic_bundle_verified"] is True,
        "cryptographic bundle verification missing",
    )
    _require(
        retention["independent_retrieval_verified"] is True,
        "independent retrieval verification missing",
    )

    adjudication = _mapping(root["adjudication"], "adjudication")
    _require_exact_keys(
        adjudication,
        {"status", "reviewer_identity", "record_sha256", "final_acceptance"},
        "adjudication",
    )
    _require(adjudication["status"] == "NOT_EXECUTED", "adjudication must remain external")
    _require(adjudication["reviewer_identity"] is None, "reviewer must not be pre-populated")
    _require(adjudication["record_sha256"] is None, "adjudication digest must not be pre-populated")
    _require(adjudication["final_acceptance"] is False, "final acceptance cannot be self-asserted")
    _require(root["freeze_established"] is False, "packet cannot establish freeze")
    _require(root["pilot_authorized"] is False, "packet cannot authorize pilot")
    _require(root["empirical_n"] == 0, "packet must preserve N=0")

    return {
        "schema_version": 1,
        "evidence_class": EXPECTED_PACKET_CLASS,
        "status": "PASS_STRUCTURAL_BINDING_ONLY",
        "repository": EXPECTED_REPOSITORY,
        "control_plane_sha": control_plane_sha,
        "helper_source_blob_sha": source_blob_sha,
        "helper_source_sha256": source_sha256,
        "helper_binary_sha256": binary_sha256,
        "continuity_report_sha256": report_sha256,
        "github_run_id": run_id,
        "github_run_attempt": run_attempt,
        "ciphertext_sha256": ciphertext_sha256,
        "expected_plaintext_sha256": expected_plaintext_sha256,
        "sigstore_bundle_sha256": bundle_sha256,
        "trusted_root_sha256": trusted_root_sha256,
        "independent_retrieval_digest_match": True,
        "final_independent_adjudication": "NOT_EXECUTED",
        "issue_295_closed": False,
        "p4_closed": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }
