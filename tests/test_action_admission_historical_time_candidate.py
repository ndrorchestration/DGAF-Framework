"""Design-only historical signature timing: contract checks, not runtime proof."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry/action_admission_authority_contract.json"
SPEC = ROOT / "docs/governance/ACTION_ADMISSION_AUTHORITY_CONTRACT.md"


def candidate():
    document = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert document["status"] == "DESIGN_ONLY_NOT_RUNTIME_AUTHORITY"
    semantics = document["issuer_and_trust_anchor"]["candidate_operation_semantics"]
    assert semantics["status"] == "PROPOSED_NON_AUTHORIZING_REVIEW_REQUIRED"
    return semantics["candidate_historical_time_provenance"]


def test_backdated_self_assertion_does_not_prove_time():
    c = candidate()
    assert c["claimed_issued_at_establishes_signing_time"] is False
    assert c["missing_untrusted_or_conflicting_proof"] == "HISTORICAL_TIME_NOT_ESTABLISHED"


def test_payload_timestamp_is_not_signature_timestamp():
    c = candidate()
    assert c["timestamp_over_unsigned_payload_establishes_signature_existence"] is False
    assert c["proof_must_bind"] == "EXACT_SIGNATURE_BYTES_AND_ADMITTED_KEY_IDENTITY"


def test_proof_binds_existence_before_witness_not_exact_signing():
    c = candidate()
    assert c["historical_proof_could_support_only"] == "SIGNATURE_EXISTED_NO_LATER_THAN_TRUSTED_WITNESS_TIME"
    assert c["exact_signing_instant_from_proof_alone"] is False


def test_no_runtime_permissions_from_time_evidence():
    c = candidate()
    assert c["status"] == "PROPOSED_NON_AUTHORIZING_REVIEW_REQUIRED"
    assert c["time_proof_is_effect_authorization"] is False
    assert c["time_proof_is_postcondition_proof"] is False


def test_witness_and_event_time_requirements():
    c = candidate()
    assert set(c["required_claim_prerequisites"]) == {
        "TRUSTED_WITNESS_IDENTITY_AND_POLICY",
        "WITNESS_SIGNATURE_AND_IMPRINT_VERIFIED",
        "EXACT_SIGNED_RECEIPT_AND_KEY_IDENTITY_BOUND",
        "ELIGIBLE_EVENT_TIME_AND_KEY_USAGE_WINDOW",
        "RECONCILED_COMPROMISE_AND_REVOCATION_HISTORY",
    }


def test_document_is_explicitly_non_authorizing():
    text = SPEC.read_text(encoding="utf-8")
    assert "unsigned receipt payload" in text
    assert "not proof of the exact signing instant" in text
    assert "No runtime, provider, key, issued AAR" in text
