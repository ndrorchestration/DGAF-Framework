import json

from components.evidence_gate import (
    ClaimScope,
    EvidenceObject,
    EvidenceTarget,
    ProvenanceBinding,
    admit_evidence,
)
from components.evidence_gate_serialization import evidence_admission_receipt_to_dict


def test_evidence_receipt_serialization_is_json_safe_and_preserves_ceiling():
    payload_bytes = b'{"status":"passed"}\n'
    import hashlib

    digest = hashlib.sha256(payload_bytes).hexdigest()
    evidence = EvidenceObject(
        evidence_id="ev-json-1",
        evidence_type="test-result",
        digest_algorithm="sha256",
        content_digest=digest,
        source_class="LOCAL_TEST",
    )
    target = EvidenceTarget(
        target_type="source_revision",
        target_id="abc123",
        scope_id="unit-test:test_widget",
        source_revision="abc123",
    )
    provenance = ProvenanceBinding(
        producer_class="LOCAL_TEST",
        custody_class="SAME_SYSTEM",
        source_identity="abc123",
    )
    claim = ClaimScope(
        claim_id="claim-json-1",
        claim_class="deterministic-test",
        scope_id="unit-test:test_widget",
        evidence_class="TESTED",
        excluded_claims=("production_ready", "independently_validated"),
    )

    receipt = admit_evidence(
        evidence,
        target,
        provenance,
        claim,
        evidence_bytes=payload_bytes,
        expected_target=target,
        required_producer_class="LOCAL_TEST",
    )
    payload = evidence_admission_receipt_to_dict(receipt)

    assert payload["admitted"] is True
    assert payload["reason_code"] == "ADMITTED"
    assert payload["authorization_effect"] == "NONE"
    assert payload["claim"]["ceiling"] == ["production_ready", "independently_validated"]
    assert payload["checks"]["digest"] is True
    assert json.loads(json.dumps(payload))["schema_version"].endswith("v0-candidate")
