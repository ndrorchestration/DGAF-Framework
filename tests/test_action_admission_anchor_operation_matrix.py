"""Candidate AAR issuer trust-anchor state/operation distinction (design only)."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "registry/action_admission_authority_contract.json"
SPEC = ROOT / "docs/governance/ACTION_ADMISSION_AUTHORITY_CONTRACT.md"

STATES = (
    "ACTIVE",
    "OVERLAP_VERIFY_ONLY",
    "RETIRED",
    "COMPROMISED",
    "UNAVAILABLE",
    "CONFLICTED",
)
OPERATIONS = (
    "VERIFY_HISTORICAL_SIGNATURE",
    "ISSUE_NEW_ATTESTATION",
    "ADMIT_NEW_PROTECTED_EFFECT",
)


def matrix():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))["issuer_and_trust_anchor"]["candidate_operation_semantics"]


def test_additive_design_not_new_runtime_permission():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert data["status"] == "DESIGN_ONLY_NOT_RUNTIME_AUTHORITY"
    assert data["issuer_and_trust_anchor"]["aar_v1"] == ("CURRENT_BOUNDED_NO_ISSUER_OR_KEY_IDENTITY")
    assert matrix()["status"] == "PROPOSED_NON_AUTHORIZING_REVIEW_REQUIRED"
    assert matrix()["required_record_version"] == "AAR_V2"
    assert matrix()["effect_authority_from_signature_alone"] is False


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("state", STATES)
def test_operation_specific_necessary_key_state(operation, state):
    allowed = {"ACTIVE", "OVERLAP_VERIFY_ONLY"} if operation == "VERIFY_HISTORICAL_SIGNATURE" else {"ACTIVE"}
    value = matrix()["allowed_anchor_states_by_operation"][operation]
    assert set(value) == allowed
    assert (state in value) == (state in allowed)


def test_no_issuance_from_verification_state():
    m = matrix()["allowed_anchor_states_by_operation"]
    assert "OVERLAP_VERIFY_ONLY" in m["VERIFY_HISTORICAL_SIGNATURE"]
    assert "OVERLAP_VERIFY_ONLY" not in m["ISSUE_NEW_ATTESTATION"]
    assert "OVERLAP_VERIFY_ONLY" not in m["ADMIT_NEW_PROTECTED_EFFECT"]


def test_external_trust_identity_and_runtime_remaining_gates_are_explicit():
    m = matrix()
    assert m["anchor_identity_source"] == "ADMITTED_TRUST_REGISTRY_NOT_RECEIPT_OR_REQUEST"
    assert m["issuance_principal"] == "INDEPENDENTLY_AUTHORIZED_ISSUER_REQUIRED"
    assert m["effect_admission_requires"] == [
        "VALID_TYPED_INPUT",
        "FRESH_SCOPE_LIMITED_AUTHORIZATION",
        "COMMIT_TIME_REVOCATION_CHECK",
        "ATOMIC_EFFECT_IDENTITY_CONSUME",
        "TRUSTED_EFFECT_GATE",
    ]
    assert m["historical_verification_is_effect_authorization"] is False
    assert m["historical_verification_is_postcondition_proof"] is False


def test_non_authorizing_docs_have_operation_and_claim_limits():
    content = SPEC.read_text(encoding="utf-8")
    for name in OPERATIONS:
        assert name in content
    assert "OVERLAP_VERIFY_ONLY" in content
    assert "does not authorize a fresh protected action" in " ".join(content.split())
    assert "The proposed operation matrix is design-only" in content
