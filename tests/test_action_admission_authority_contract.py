"""Contract tests for provider-neutral Action Admission authority semantics."""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "registry/action_admission_authority_contract.json"
SPEC_PATH = REPO_ROOT / "docs/governance/ACTION_ADMISSION_AUTHORITY_CONTRACT.md"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_authority_contract_is_versioned_and_non_authoritative() -> None:
    contract = load_contract()
    assert contract["version"] == "AAR_AUTHORITY_CONTRACT_V1"
    assert contract["status"] == "DESIGN_ONLY_NOT_RUNTIME_AUTHORITY"
    assert contract["provider_admission"] == "REQUIRED_BEFORE_RUNTIME_IMPLEMENTATION"


def test_replay_contract_claims_at_most_once_not_exactly_once() -> None:
    replay = load_contract()["replay"]
    assert replay["guarantee"] == "AT_MOST_ONCE_AUTHORIZED_EFFECT"
    assert replay["exactly_once"] == "NOT_ESTABLISHED"
    assert replay["required_atomic_operation"] == "CONSUME_ONCE"
    assert replay["authority_outcomes"] == ["CONSUMED", "REPLAY", "UNAVAILABLE", "CONFLICTED"]
    assert replay["fail_closed_outcomes"] == ["REPLAY", "UNAVAILABLE", "CONFLICTED"]
    assert replay["crash_after_consume_before_effect"] == "NO_AUTOMATIC_RETRY_MANUAL_RECOVERY_REQUIRED"

    # Record identity supports duplicate-record detection, but at-most-once effect
    # identity must not be defeatable by minting a fresh record_id for the same
    # authorized consequential effect.
    assert replay["record_identity_fields"] == [
        "version",
        "record_id",
        "action_class",
        "target",
        "policy_id",
        "authorization.authorization_id",
        "action_digest",
    ]
    assert replay["effect_identity_fields"] == [
        "version",
        "action_class",
        "target",
        "policy_id",
        "authorization.authorization_id",
        "action_digest",
    ]
    assert "record_id" not in replay["effect_identity_fields"]
    assert replay["consume_key"] == "EFFECT_IDENTITY"


def test_revocation_contract_is_commit_time_and_fail_closed() -> None:
    revocation = load_contract()["revocation"]
    assert revocation["authority_outcomes"] == ["ACTIVE", "REVOKED", "UNAVAILABLE", "CONFLICTED"]
    assert revocation["allow_outcomes"] == ["ACTIVE"]
    assert revocation["fail_closed_outcomes"] == ["REVOKED", "UNAVAILABLE", "CONFLICTED"]
    assert revocation["timing"] == "IMMEDIATELY_BEFORE_REPLAY_CONSUME_AND_SIDE_EFFECT"
    assert revocation["historical_receipts"] == "IMMUTABLE_NON_RETROACTIVE"


def test_issuer_and_trust_anchor_require_future_versioned_identity() -> None:
    trust = load_contract()["issuer_and_trust_anchor"]
    assert trust["aar_v1"] == "CURRENT_BOUNDED_NO_ISSUER_OR_KEY_IDENTITY"
    assert trust["future_record_version"] == "AAR_V2_REQUIRED_FOR_ISSUER_AND_KEY_IDENTITY"
    assert trust["trust_anchor_states"] == [
        "ACTIVE",
        "OVERLAP_VERIFY_ONLY",
        "RETIRED",
        "COMPROMISED",
        "UNAVAILABLE",
        "CONFLICTED",
    ]
    assert trust["verification_allow_states"] == ["ACTIVE", "OVERLAP_VERIFY_ONLY"]
    assert trust["verification_deny_states"] == ["RETIRED", "COMPROMISED", "UNAVAILABLE", "CONFLICTED"]
    assert trust["issuer_separation"] == "ISSUANCE_AUTHORITY_SEPARATE_FROM_REQUEST_PATH_VERIFICATION"


def test_commit_order_is_explicit_and_spec_disclaims_runtime_effect() -> None:
    contract = load_contract()
    assert contract["commit_order"] == [
        "STRUCTURAL_AND_ATTESTATION_VALIDATION",
        "COMMIT_TIME_REVOCATION_REVALIDATION",
        "ATOMIC_REPLAY_CONSUME",
        "PROTECTED_SIDE_EFFECT",
        "POSTCONDITION_AND_EXECUTION_RECEIPT",
    ]

    spec = SPEC_PATH.read_text(encoding="utf-8")
    assert "at-most-once" in spec.lower()
    assert "exactly-once is not established" in spec.lower()
    assert "does not admit a provider" in spec.lower()
    assert "record id" in spec.lower()
    assert "effect identity" in spec.lower()
    assert "PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0" in spec
