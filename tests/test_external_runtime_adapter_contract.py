"""Tests for the provider-neutral external runtime ingress boundary."""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "registry/external_runtime_adapter_contract_v1.json"
FIXTURE_ROOT = REPO_ROOT / "tests/resources/external_runtime_adapter"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def valid_envelope() -> dict:
    return {
        "schema_version": "DGAF_EXTERNAL_RUNTIME_ENVELOPE_V1",
        "provider": {
            "provider_id": "synthetic-provider",
            "runtime_id": "synthetic-runtime",
            "adapter_id": "neutral-test-adapter",
            "adapter_version": "1.0.0",
        },
        "identity": {
            "event_id": "evt-001",
            "effect_id": "eff-001",
            "source_id": "src-001",
        },
        "evidence": {
            "evidence_class": "EXTERNAL_UNTRUSTED_OBSERVATION",
            "observed_at": "2026-09-17T14:00:00Z",
            "content_digest": "sha256:" + "1" * 64,
            "payload": {"claim": "synthetic"},
        },
        "provenance": {
            "producer_id": "synthetic-provider",
            "producer_run_id": "run-001",
            "source_bindings": ["src-001"],
        },
        "request": {
            "action_class": "NON_CONSEQUENTIAL_RECORD_INGRESS",
            "requested_transition": "RECORD_ONLY",
        },
        "assertions": {
            "verification_class": "EXTERNAL_PASS",
            "authority": {"status": "EXTERNAL_PROVIDER_APPROVED"},
        },
        "risk": {
            "consequence_class": "NOT_APPLICABLE",
            "reversibility": "NOT_APPLICABLE",
        },
    }


def test_contract_is_versioned_provider_neutral_and_non_authoritative() -> None:
    contract = load_contract()
    assert contract["version"] == "DGAF_EXTERNAL_RUNTIME_ENVELOPE_V1"
    assert contract["status"] == "NON_AUTHORITATIVE_INGRESS_CONTRACT"
    assert contract["authority_semantics"] == "PRESENTED_NOT_GRANTED"
    assert contract["exactly_once"] == "NOT_ESTABLISHED"
    assert contract["provider_specific_trust"] == "PROHIBITED"
    assert "record_id" not in contract["effect_identity_fields"]


def test_contract_rejection_taxonomy_is_stable() -> None:
    rejection_codes = set(load_contract()["rejection_codes"])
    assert {
        "DGAF_EXT_SCHEMA_UNSUPPORTED",
        "DGAF_EXT_REQUIRED_FIELD_MISSING",
        "DGAF_EXT_IDENTITY_MALFORMED",
        "DGAF_EXT_SOURCE_IDENTITY_INVALID",
        "DGAF_EXT_EVIDENCE_DIGEST_MISMATCH",
        "DGAF_EXT_PROVENANCE_INVALID",
        "DGAF_EXT_EVIDENCE_STALE",
        "DGAF_EXT_ACTION_CLASS_UNSUPPORTED",
        "DGAF_EXT_TRANSITION_UNSUPPORTED",
        "DGAF_EXT_AUTHORITY_MISMATCH",
        "DGAF_EXT_RISK_METADATA_REQUIRED",
        "DGAF_EXT_DUPLICATE_EFFECT",
        "DGAF_EXT_PROVIDER_SUBSTITUTION",
    } <= rejection_codes


def test_valid_envelope_is_admitted_only_as_non_authoritative_input() -> None:
    from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

    result = validate_external_runtime_envelope(
        valid_envelope(),
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    assert result["admitted"] is True
    assert result["result_version"] == "DGAF_EXTERNAL_RUNTIME_ADMISSION_V1"
    assert result["authority_status"] == "PRESENTED_NOT_GRANTED"
    assert result["record_id"].startswith("sha256:")
    assert result["effect_id"] == "eff-001"
    assert result["trust_class"] == "EXTERNAL_NON_AUTHORITATIVE_UNTIL_VALIDATED"
    assert result["external_assertions"]["verification_class"] == "EXTERNAL_PASS"
    assert result["external_assertions"]["authority"]["status"] == "EXTERNAL_PROVIDER_APPROVED"


@pytest.mark.parametrize(
    ("mutator", "expected_code"),
    [
        (
            lambda e: e["identity"].update(event_id="bad id with spaces"),
            "DGAF_EXT_IDENTITY_MALFORMED",
        ),
        (
            lambda e: e["evidence"].update(observed_at="2026-09-17T10:00:00Z"),
            "DGAF_EXT_EVIDENCE_STALE",
        ),
        (
            lambda e: e["assertions"].update(authority={"status": "DGAF_GRANTED"}),
            "DGAF_EXT_AUTHORITY_MISMATCH",
        ),
        (
            lambda e: e["request"].update(action_class="ARBITRARY_SHELL_EXECUTION"),
            "DGAF_EXT_ACTION_CLASS_UNSUPPORTED",
        ),
        (
            lambda e: e["provider"].update(provider_id="dgaf-authoritative-runtime"),
            "DGAF_EXT_PROVIDER_SUBSTITUTION",
        ),
        (
            lambda e: e["identity"].pop("source_id"),
            "DGAF_EXT_REQUIRED_FIELD_MISSING",
        ),
    ],
)
def test_invalid_envelopes_fail_closed(mutator, expected_code: str) -> None:
    from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

    envelope = valid_envelope()
    mutator(envelope)
    result = validate_external_runtime_envelope(
        envelope,
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    assert result["admitted"] is False
    assert result["reason_codes"][0] == expected_code
    assert result["authority_status"] == "PRESENTED_NOT_GRANTED"


def test_duplicate_effect_fails_closed_independent_of_event_identity() -> None:
    from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

    replay_envelope = valid_envelope()
    replay_envelope["identity"]["event_id"] = "evt-002"
    replay = validate_external_runtime_envelope(
        replay_envelope,
        seen_effect_ids={"eff-001"},
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    assert replay["admitted"] is False
    assert replay["reason_codes"] == ["DGAF_EXT_DUPLICATE_EFFECT"]


def test_unknown_required_risk_dimension_has_no_admissible_consequential_transition() -> None:
    from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

    envelope = valid_envelope()
    envelope["request"] = {
        "action_class": "CONSEQUENTIAL_ACTION_REQUEST",
        "requested_transition": "REQUEST_ACTION_ADMISSION",
    }
    envelope["risk"] = {"consequence_class": "UNKNOWN", "reversibility": "REVERSIBLE"}
    result = validate_external_runtime_envelope(
        envelope,
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    assert result["admitted"] is False
    assert result["reason_codes"] == ["DGAF_EXT_RISK_METADATA_REQUIRED"]


def test_provider_fixtures_preserve_neutral_semantics() -> None:
    from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

    valid = json.loads((FIXTURE_ROOT / "valid_envelope.json").read_text(encoding="utf-8"))
    substitution = json.loads(
        (FIXTURE_ROOT / "provider_substitution.json").read_text(encoding="utf-8")
    )
    accepted = validate_external_runtime_envelope(
        valid,
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    rejected = validate_external_runtime_envelope(
        substitution,
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    assert accepted["admitted"] is True
    assert accepted["authority_status"] == "PRESENTED_NOT_GRANTED"
    assert rejected["reason_codes"] == ["DGAF_EXT_PROVIDER_SUBSTITUTION"]
