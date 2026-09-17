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
        "version": "EXTERNAL_RUNTIME_ENVELOPE_V1",
        "provider_identity": "synthetic-runtime",
        "provider_display_name": "Synthetic Runtime",
        "event_id": "evt-001",
        "effect_id": "eff-001",
        "source_id": "src-001",
        "evidence": {
            "observed_at": "2026-09-17T14:00:00Z",
            "class": "EXTERNAL_UNTRUSTED_OBSERVATION",
            "digest": "sha256:" + "1" * 64,
        },
        "provenance": {
            "producer": "synthetic-runtime",
            "binding": "sha256:" + "2" * 64,
        },
        "requested_action_class": "NON_CONSEQUENTIAL_RECORD_INGRESS",
        "verification_assertion": "EXTERNAL_PASS",
        "authority_presented": "EXTERNAL_PROVIDER_APPROVED",
        "consequence": "LOW",
        "reversibility": "REVERSIBLE",
    }


def test_contract_is_versioned_provider_neutral_and_non_authoritative() -> None:
    contract = load_contract()
    assert contract["version"] == "EXTERNAL_RUNTIME_ENVELOPE_V1"
    assert contract["status"] == "NON_AUTHORITATIVE_INGRESS_CONTRACT"
    assert contract["authority_semantics"] == "PRESENTED_NOT_GRANTED"
    assert contract["exactly_once"] == "NOT_ESTABLISHED"
    assert contract["provider_specific_trust"] == "PROHIBITED"
    assert "record_id" not in contract["effect_identity_fields"]


def test_contract_rejection_taxonomy_is_stable() -> None:
    rejection_codes = set(load_contract()["rejection_codes"])
    assert {
        "MALFORMED_IDENTITY",
        "STALE_EVIDENCE",
        "DUPLICATE_EFFECT",
        "AUTHORITY_MISMATCH",
        "UNSUPPORTED_ACTION_CLASS",
        "PROVIDER_SUBSTITUTION",
        "MISSING_REQUIRED_FIELD",
        "UNKNOWN_REQUIRED_DIMENSION",
    } <= rejection_codes


def test_valid_envelope_is_admitted_only_as_non_authoritative_input() -> None:
    from dgaf.external_runtime_adapter import validate_external_runtime_envelope

    result = validate_external_runtime_envelope(
        valid_envelope(),
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    assert result["decision"] == "ADMITTED_AS_NON_AUTHORITATIVE_INPUT"
    assert result["authority_effect"] == "NONE"
    assert result["record_identity"].startswith("sha256:")
    assert result["effect_identity"].startswith("sha256:")
    assert result["normalized_envelope"]["authority_presented"] == "EXTERNAL_PROVIDER_APPROVED"
    assert result["normalized_envelope"]["verification_assertion"] == "EXTERNAL_PASS"


@pytest.mark.parametrize(
    ("mutator", "expected_code"),
    [
        (lambda e: e.update(event_id="bad id with spaces"), "MALFORMED_IDENTITY"),
        (
            lambda e: e["evidence"].update(observed_at="2026-09-17T10:00:00Z"),
            "STALE_EVIDENCE",
        ),
        (
            lambda e: e.update(authority_presented="DGAF_GRANTED"),
            "AUTHORITY_MISMATCH",
        ),
        (
            lambda e: e.update(requested_action_class="ARBITRARY_SHELL_EXECUTION"),
            "UNSUPPORTED_ACTION_CLASS",
        ),
        (
            lambda e: e.update(provider_identity="dgaf-authoritative-runtime"),
            "PROVIDER_SUBSTITUTION",
        ),
        (lambda e: e.pop("source_id"), "MISSING_REQUIRED_FIELD"),
    ],
)
def test_invalid_envelopes_fail_closed(mutator, expected_code: str) -> None:
    from dgaf.external_runtime_adapter import validate_external_runtime_envelope

    envelope = valid_envelope()
    mutator(envelope)
    result = validate_external_runtime_envelope(
        envelope,
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    assert result["decision"] == "REJECTED"
    assert result["rejection_code"] == expected_code
    assert result["authority_effect"] == "NONE"


def test_duplicate_effect_fails_closed_independent_of_record_identity() -> None:
    from dgaf.external_runtime_adapter import validate_external_runtime_envelope

    first = validate_external_runtime_envelope(
        valid_envelope(),
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    replay_envelope = valid_envelope()
    replay_envelope["event_id"] = "evt-002"
    replay = validate_external_runtime_envelope(
        replay_envelope,
        seen_effect_ids={first["effect_identity"]},
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    assert replay["decision"] == "REJECTED"
    assert replay["rejection_code"] == "DUPLICATE_EFFECT"


def test_unknown_required_dimension_has_no_admissible_transition() -> None:
    from dgaf.external_runtime_adapter import validate_external_runtime_envelope

    envelope = valid_envelope()
    envelope["requested_action_class"] = "CONSEQUENTIAL_ACTION_REQUEST"
    envelope["consequence"] = "UNKNOWN"
    result = validate_external_runtime_envelope(
        envelope,
        now=datetime(2026, 9, 17, 14, 5, tzinfo=timezone.utc),
    )
    assert result["decision"] == "REJECTED"
    assert result["rejection_code"] == "UNKNOWN_REQUIRED_DIMENSION"


def test_provider_fixtures_preserve_neutral_semantics() -> None:
    from dgaf.external_runtime_adapter import validate_external_runtime_envelope

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
    assert accepted["decision"] == "ADMITTED_AS_NON_AUTHORITATIVE_INPUT"
    assert accepted["authority_effect"] == "NONE"
    assert rejected["rejection_code"] == "PROVIDER_SUBSTITUTION"
