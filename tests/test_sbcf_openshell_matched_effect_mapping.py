"""Closed-schema tests for the pinned OpenShell matched-effect candidate."""

import json
from pathlib import Path

import pytest
from experiments.sbcf.matched_effect_contract import effect_contract_digest
from experiments.sbcf.openshell_matched_effect_mapping import (
    evaluate_openshell_mapping,
    validate_openshell_mapping,
)

FIXTURE_ROOT = Path(__file__).parents[1] / "experiments" / "sbcf" / "fixtures"
FIXTURE = FIXTURE_ROOT / "openshell_matched_http_mapping_v0.json"
EFFECT_FIXTURE = FIXTURE_ROOT / "matched_http_effect_contract_v0.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_current_openshell_mapping_is_partial_and_not_ready():
    result = evaluate_openshell_mapping(load())
    assert not result.complete
    assert "openshell_receiver_unmatched" in result.blockers
    assert (
        "openshell_case_blocked:control_plane_unavailable:" "candidate_expected_deny_observed_allow"
    ) in result.blockers


def test_host_method_and_revocation_candidates_remain_receiver_blocked():
    records = {record["id"]: record for record in load()["cases"]}
    for case_id in ("exact_allow", "adjacent_host", "adjacent_method", "revoked_authority"):
        assert records[case_id]["blocker"] == "external_receiver_identity_not_matched"
    assert records["control_plane_unavailable"] == {
        "id": "control_plane_unavailable",
        "mapping_state": "OBSERVED_SEMANTIC_MISMATCH",
        "system_decision": "ALLOW",
        "blocker": "candidate_expected_deny_observed_allow",
    }


def test_mapping_is_bound_to_current_effect_contract_without_freezing_parent():
    mapping = load()
    effect = json.loads(EFFECT_FIXTURE.read_text(encoding="utf-8"))
    assert mapping["effect_contract_digest"] == effect_contract_digest(effect)
    assert effect["system_mappings"]["openshell"] == "CANDIDATE_ENFORCED_RUNTIME"


def test_pinned_upstream_identity_cannot_drift():
    mapping = load()
    mapping["upstream"]["commit"] = "main"
    with pytest.raises(ValueError, match="upstream identity changed"):
        validate_openshell_mapping(mapping)


def test_public_baseline_receiver_cannot_be_silently_declared_matched():
    mapping = load()
    mapping["baseline_receiver"]["matches_common_receiver"] = True
    mapping["baseline_receiver"]["blocker"] = None
    with pytest.raises(ValueError, match="receiver semantics changed"):
        validate_openshell_mapping(mapping)


def test_control_plane_semantic_mismatch_cannot_be_silently_relabelled():
    mapping = load()
    record = next(item for item in mapping["cases"] if item["id"] == "control_plane_unavailable")
    record["mapping_state"] = "EXECUTABLE_CANDIDATE_UNMATCHED_RECEIVER"
    record["system_decision"] = "DENY"
    record["blocker"] = "external_receiver_identity_not_matched"
    with pytest.raises(ValueError, match="case semantics changed"):
        validate_openshell_mapping(mapping)


def test_frozen_label_cannot_hide_receiver_or_case_blockers():
    mapping = load()
    mapping["status"] = "FROZEN"
    result = evaluate_openshell_mapping(mapping)
    assert not result.complete
    assert "openshell_receiver_unmatched" in result.blockers
    assert any(blocker.startswith("openshell_case_blocked:") for blocker in result.blockers)
