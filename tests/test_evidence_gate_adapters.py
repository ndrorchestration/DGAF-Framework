import json

from components.evidence_gate import EvidenceAdmissionReason, admit_evidence
from components.evidence_gate_adapters import (
    LocalTestArtifact,
    local_test_artifact_to_gate_inputs,
    validated_track_a_operator_admission_to_gate_inputs,
)


def test_local_test_artifact_uses_generic_gate_contract():
    mapped = local_test_artifact_to_gate_inputs(
        LocalTestArtifact(
            artifact_id="pytest-run-1",
            test_name="test_widget",
            source_revision="abc123",
            runtime_identity="pytest-9.0",
            environment_identity="python-3.12",
            output_bytes=b'{"status":"passed"}\n',
        )
    )

    receipt = admit_evidence(
        mapped.evidence,
        mapped.target,
        mapped.provenance,
        mapped.claim_scope,
        evidence_bytes=mapped.evidence_bytes,
        expected_target=mapped.target,
        required_producer_class="LOCAL_TEST",
    )

    assert receipt.admitted is True
    assert receipt.reason_code is EvidenceAdmissionReason.ADMITTED
    assert receipt.authorization_effect == "NONE"
    assert receipt.evidence_class == "TESTED"
    assert "production_ready" in receipt.claim_ceiling


def track_a_record():
    return {
        "record_type": "TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "collection_execution_class": "OPERATOR_CODESPACE",
        "collection_authorization_commit_sha": "563152fdb254b8ee948a693c287126a8bf8314b8",
        "frozen_candidate_sha": "a" * 40,
        "frozen_candidate_tree_sha": "b" * 40,
        "python_version": "3.12.3",
        "requirements_lock_blob_sha": "c" * 40,
        "collection_execution_receipt_sha256": "d" * 64,
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "admission_status": "CONTENT_ADDRESSED_PENDING_DATASET_LOCK",
    }


def test_track_a_adapter_requires_prior_domain_validation():
    raw = (json.dumps(track_a_record(), sort_keys=True) + "\n").encode()
    try:
        validated_track_a_operator_admission_to_gate_inputs(
            raw,
            domain_validation_passed=False,
        )
    except ValueError as exc:
        assert "domain validation must pass" in str(exc)
    else:
        raise AssertionError("adapter must reject unvalidated Track A evidence")


def test_track_a_adapter_maps_validated_record_without_promoting_scientific_state():
    raw = (json.dumps(track_a_record(), sort_keys=True) + "\n").encode()
    mapped = validated_track_a_operator_admission_to_gate_inputs(
        raw,
        domain_validation_passed=True,
    )

    receipt = admit_evidence(
        mapped.evidence,
        mapped.target,
        mapped.provenance,
        mapped.claim_scope,
        evidence_bytes=mapped.evidence_bytes,
        expected_target=mapped.target,
        required_producer_class="OPERATOR_CODESPACE",
        receipt_checker=lambda e, t, p, c: p.receipt_identity == "d" * 64,
    )

    assert receipt.admitted is True
    assert receipt.evidence_class == "ATTESTED"
    assert receipt.authorization_effect == "NONE"
    assert "dataset_lock_established" in receipt.claim_ceiling
    assert "unblinding_authorized" in receipt.claim_ceiling
    assert "primary_analysis_authorized" in receipt.claim_ceiling
    assert "independently_validated" in receipt.claim_ceiling
    assert "canonical_dgaf_efficacy_established" in receipt.claim_ceiling
    assert "high_assurance_authorized" in receipt.claim_ceiling


def test_track_a_adapter_does_not_invent_github_actions_identity():
    raw = (json.dumps(track_a_record(), sort_keys=True) + "\n").encode()
    mapped = validated_track_a_operator_admission_to_gate_inputs(
        raw,
        domain_validation_passed=True,
    )

    assert mapped.provenance.provider_identity is None
    assert mapped.provenance.workflow_identity is None
    assert mapped.provenance.artifact_identity is None
