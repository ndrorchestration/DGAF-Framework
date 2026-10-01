"""Adapters that map domain evidence into the Evidence Gate v0 contract."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from .evidence_gate import (
    ClaimScope,
    EvidenceObject,
    EvidenceTarget,
    ProvenanceBinding,
)


@dataclass(frozen=True)
class EvidenceGateInputs:
    evidence: EvidenceObject
    target: EvidenceTarget
    provenance: ProvenanceBinding
    claim_scope: ClaimScope
    evidence_bytes: bytes


@dataclass(frozen=True)
class LocalTestArtifact:
    artifact_id: str
    test_name: str
    source_revision: str
    runtime_identity: str
    environment_identity: str
    output_bytes: bytes


def local_test_artifact_to_gate_inputs(
    artifact: LocalTestArtifact,
) -> EvidenceGateInputs:
    """Map a generic deterministic local-test artifact into Evidence Gate inputs."""
    if not isinstance(artifact, LocalTestArtifact):
        raise TypeError("artifact must be LocalTestArtifact")
    if not isinstance(artifact.output_bytes, bytes):
        raise TypeError("output_bytes must be bytes")

    scope_id = f"local-test:{artifact.test_name}"
    digest = hashlib.sha256(artifact.output_bytes).hexdigest()
    evidence = EvidenceObject(
        evidence_id=artifact.artifact_id,
        evidence_type="local-test-output",
        digest_algorithm="sha256",
        content_digest=digest,
        source_class="LOCAL_TEST",
    )
    target = EvidenceTarget(
        target_type="source_revision",
        target_id=artifact.source_revision,
        scope_id=scope_id,
        source_revision=artifact.source_revision,
        environment_identity=artifact.environment_identity,
    )
    provenance = ProvenanceBinding(
        producer_class="LOCAL_TEST",
        custody_class="SAME_SYSTEM",
        source_identity=artifact.source_revision,
        runtime_identity=artifact.runtime_identity,
        environment_identity=artifact.environment_identity,
    )
    claim_scope = ClaimScope(
        claim_id=f"test:{artifact.test_name}:passed-as-recorded",
        claim_class="deterministic-test",
        scope_id=scope_id,
        evidence_class="TESTED",
        limitations=("deterministic local test output only",),
        excluded_claims=(
            "production_ready",
            "independently_validated",
            "empirically_effective",
        ),
    )
    return EvidenceGateInputs(evidence, target, provenance, claim_scope, artifact.output_bytes)


def validated_track_a_operator_admission_to_gate_inputs(
    record_bytes: bytes,
    *,
    domain_validation_passed: bool,
) -> EvidenceGateInputs:
    """Map an already domain-validated Track A operator admission record.

    This adapter intentionally does not replace the Track A validator. Callers
    must supply domain_validation_passed=True only after the existing
    validate_track_a_epoch_002_operator_collection_admission.py evidence mode
    succeeds against the concrete receipt and retained archives.
    """
    if domain_validation_passed is not True:
        raise ValueError(
            "Track A domain validation must pass before Evidence Gate mapping"
        )
    if not isinstance(record_bytes, bytes):
        raise TypeError("record_bytes must be bytes")
    try:
        record: Any = json.loads(record_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("record_bytes must contain one UTF-8 JSON object") from exc
    if not isinstance(record, dict):
        raise ValueError("Track A admission record must be one JSON object")
    required = {
        "record_type",
        "protocol_id",
        "epoch",
        "collection_execution_class",
        "collection_authorization_commit_sha",
        "frozen_candidate_sha",
        "frozen_candidate_tree_sha",
        "python_version",
        "requirements_lock_blob_sha",
        "collection_execution_receipt_sha256",
        "custody_class",
        "independent_custody",
        "admission_status",
    }
    missing = sorted(required - set(record))
    if missing:
        raise ValueError(f"Track A admission record missing adapter fields: {missing}")
    if record["record_type"] != "TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION":
        raise ValueError("unexpected Track A record_type")

    scope_id = (
        f"{record['protocol_id']}:epoch:{record['epoch']}:"
        "operator-collection-provenance"
    )
    environment = (
        f"python:{record['python_version']}|requirements:{record['requirements_lock_blob_sha']}"
    )
    digest = hashlib.sha256(record_bytes).hexdigest()

    evidence = EvidenceObject(
        evidence_id=f"track-a-operator-admission:{digest}",
        evidence_type=record["record_type"],
        digest_algorithm="sha256",
        content_digest=digest,
        source_class=record["collection_execution_class"],
    )
    target = EvidenceTarget(
        target_type="frozen_candidate",
        target_id=record["frozen_candidate_sha"],
        scope_id=scope_id,
        source_revision=record["collection_authorization_commit_sha"],
        tree_identity=record["frozen_candidate_tree_sha"],
        environment_identity=environment,
    )
    provenance = ProvenanceBinding(
        producer_class=record["collection_execution_class"],
        custody_class=record["custody_class"],
        source_identity=record["collection_authorization_commit_sha"],
        environment_identity=environment,
        receipt_identity=record["collection_execution_receipt_sha256"],
    )
    claim_scope = ClaimScope(
        claim_id="track-a-epoch002:operator-collection-provenance-admitted",
        claim_class="provenance",
        scope_id=scope_id,
        evidence_class="ATTESTED",
        limitations=(
            "domain validator must already have accepted the concrete retained evidence",
            "same-system/non-independent provenance unless separately established otherwise",
        ),
        excluded_claims=(
            "dataset_lock_established",
            "unblinding_authorized",
            "primary_analysis_authorized",
            "independently_validated",
            "canonical_dgaf_efficacy_established",
            "high_assurance_authorized",
        ),
    )
    return EvidenceGateInputs(evidence, target, provenance, claim_scope, record_bytes)
