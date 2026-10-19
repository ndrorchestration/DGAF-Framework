"""Closed-schema tests for the pinned ACS matched-effect candidate mapping."""

import copy
import json
from pathlib import Path

import pytest

from experiments.sbcf.acs_matched_effect_mapping import (
    evaluate_acs_mapping,
    validate_acs_mapping,
)
from experiments.sbcf.matched_effect_contract import effect_contract_digest

FIXTURE_ROOT = Path(__file__).parents[1] / "experiments" / "sbcf" / "fixtures"
FIXTURE = FIXTURE_ROOT / "acs_matched_http_mapping_v0.json"
EFFECT_FIXTURE = FIXTURE_ROOT / "matched_http_effect_contract_v0.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_current_acs_mapping_is_partial_and_not_ready():
    result = evaluate_acs_mapping(load())
    assert not result.complete
    assert "acs_case_blocked:adjacent_method:acs_stock_egress_does_not_bind_http_method" in result.blockers
    assert (
        "acs_case_blocked:revoked_authority:" "acs_reference_mapping_has_no_frozen_authority_revocation_semantics"
    ) in result.blockers
    assert (
        "acs_case_blocked:control_plane_unavailable:" "acs_failure_posture_not_frozen_to_deny_for_matched_fixture"
    ) in result.blockers


def test_only_host_cases_are_executable_candidates():
    records = {record["id"]: record for record in load()["cases"]}
    assert records["exact_allow"]["mapping_state"] == "EXECUTABLE_CANDIDATE"
    assert records["exact_allow"]["system_decision"] == "ALLOW"
    assert records["adjacent_host"]["mapping_state"] == "EXECUTABLE_CANDIDATE"
    assert records["adjacent_host"]["system_decision"] == "DENY"
    for case_id in ("adjacent_method", "revoked_authority", "control_plane_unavailable"):
        assert records[case_id]["mapping_state"] == "UNRESOLVED"


def test_candidate_overlay_is_explicit_and_not_frozen():
    overlay = load()["policy_overlay"]
    assert overlay == {
        "kind": "CANDIDATE_BENCHMARK_FIXTURE_OVERLAY",
        "base_file": "reference-implementations/agt/policy/lib/data.json",
        "egress_allowlist": ["127.0.0.1"],
        "frozen": False,
    }


def test_pinned_upstream_identity_cannot_drift():
    mapping = load()
    mapping["upstream"]["commit"] = "main"
    with pytest.raises(ValueError, match="upstream identity changed"):
        validate_acs_mapping(mapping)


def test_effect_contract_digest_cannot_drift():
    mapping = load()
    mapping["effect_contract_digest"] = "sha256:" + "0" * 64
    with pytest.raises(ValueError, match="effect contract digest changed"):
        validate_acs_mapping(mapping)


def test_unresolved_case_cannot_be_silently_declared_mapped():
    mapping = load()
    record = next(item for item in mapping["cases"] if item["id"] == "adjacent_method")
    record["mapping_state"] = "EXECUTABLE_CANDIDATE"
    record["system_decision"] = "DENY"
    record["blocker"] = None
    with pytest.raises(ValueError, match="case semantics changed"):
        validate_acs_mapping(mapping)


def test_frozen_label_cannot_hide_case_blockers():
    mapping = load()
    mapping["status"] = "FROZEN"
    mapping["policy_overlay"]["frozen"] = True
    result = evaluate_acs_mapping(mapping)
    assert not result.complete
    assert any(blocker.startswith("acs_case_blocked:") for blocker in result.blockers)


def test_fixture_is_copy_stable():
    mapping = load()
    validate_acs_mapping(copy.deepcopy(mapping))


def test_mapping_is_bound_to_current_effect_contract_without_resolving_acs():
    mapping = load()
    effect_contract = json.loads(EFFECT_FIXTURE.read_text(encoding="utf-8"))
    assert mapping["effect_contract_digest"] == effect_contract_digest(effect_contract)
    assert effect_contract["system_mappings"]["acs"] == "UNRESOLVED"
