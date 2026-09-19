import copy
import json
from pathlib import Path

import pytest

from scripts.aoss_v0_6_acp_adapter import (\n    AdapterError,\n    classify_manifest,\n    normalize_manifest,\n)

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = ROOT / "tests/resources/aoss_v0_6_acp_fixture_bundle.json"
MANIFEST_PATH = ROOT / "registry/aoss_v0_6_acp_measurement_manifest_v1.json"

BUNDLE = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

PASS_CASES = {
    "normal_completion",
    "policy_denial",
    "unknown_capability_rejection",
    "handler_failure",
    "cancellation",
    "exact_budget_success",
    "budget_exhaustion",
    "suppressed_budget_exception_fail_closed",
    "missing_event",
    "reordered_exported_events",
    "duplicate_replayed_event",
    "stale_timestamp",
    "source_order_ambiguity",
    "missing_authority_evidence",
}


def case(name: str) -> dict:
    return copy.deepcopy(BUNDLE["cases"][name])


def test_freeze_parent_and_source_identity_are_exact() -> None:
    assert MANIFEST["freeze_parent"]["pr"] == 843
    assert MANIFEST["freeze_parent"]["commit"] == "bf7fa5c806b3b93e4b07a97c599a855d0a986459"
    assert MANIFEST["source_system"]["commit"] == "dbab7c1afafec524ce7c18157de2089cafe79c87"
    assert BUNDLE["source_identity"]["commit"] == MANIFEST["source_system"]["commit"]


@pytest.mark.parametrize("name", sorted(PASS_CASES))
def test_structurally_ingestible_fixtures_normalize_deterministically(name: str) -> None:
    first = normalize_manifest(case(name))
    second = normalize_manifest(case(name))
    assert first == second


def test_adapter_never_manufactures_missing_evidence() -> None:
    result = classify_manifest(case("normal_completion"))
    for event in result["events"]:
        assert event["authorization_state"] == "UNMEASURED"
        assert event["validation_state"] == "UNMEASURED"
        assert event["parent_event_id"] is None
        assert event["source_event_id"] is None
        assert event["durable_attestation"] == "NOT_ESTABLISHED"


def test_observer_ids_are_adapter_derived_and_replay_stable() -> None:
    left = classify_manifest(case("normal_completion"))
    right = classify_manifest(case("normal_completion"))
    assert left["normalized_digest"] == right["normalized_digest"]
    assert [event["observer_event_id"] for event in left["events"]] == [
        event["observer_event_id"] for event in right["events"]
    ]


def test_malformed_schema_fails_closed() -> None:
    with pytest.raises(AdapterError, match="schema mismatch"):
        normalize_manifest(case("malformed_manifest"))


def test_mismatched_run_id_fails_closed() -> None:
    with pytest.raises(AdapterError, match="run_id mismatch"):
        normalize_manifest(case("mismatched_run_id"))


def test_missing_event_remains_incomplete_not_invented() -> None:
    result = classify_manifest(case("missing_event"))
    assert result["terminal_event"] is None
    assert result["event_count"] == 1


def test_reordered_events_preserve_source_order_without_claiming_causality() -> None:
    result = classify_manifest(case("reordered_exported_events"))
    assert [event["event_kind"] for event in result["events"]] == [
        "task.completed",
        "task.started",
    ]
    assert result["parent_lineage_measured"] is False


def test_duplicate_replay_is_preserved_for_later_adversarial_detection() -> None:
    result = classify_manifest(case("duplicate_replayed_event"))
    assert [event["event_kind"] for event in result["events"]].count("task.started") == 2


def test_stale_timestamp_is_not_silently_rewritten() -> None:
    result = classify_manifest(case("stale_timestamp"))
    assert result["events"][0]["wall_time"].startswith("2025-01-01")


def test_missing_authority_evidence_stays_unmeasured_even_on_completion() -> None:
    result = classify_manifest(case("missing_authority_evidence"))
    assert result["terminal_event"] == "task.completed"
    assert result["has_unmeasured_authority"] is True
    assert result["has_unmeasured_validation"] is True


def test_fixture_bundle_is_apparatus_not_outcomes() -> None:
    assert BUNDLE["classification"] == "APPARATUS_FIXTURES_NOT_COLLECTED_OUTCOMES"


def test_manifest_contains_all_preregistered_episode_classes() -> None:
    assert set(MANIFEST["required_episode_classes"]) == set(BUNDLE["cases"])
