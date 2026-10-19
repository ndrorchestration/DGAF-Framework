"""Closed-schema tests for prospective matched HTTP effect contract v1."""

import copy
import json
from pathlib import Path

import pytest

from experiments.sbcf.matched_effect_contract_v1 import (
    effect_contract_v1_digest,
    evaluate_effect_contract_v1,
    validate_effect_contract_v1,
)

FIXTURE = Path(__file__).parents[1] / "experiments" / "sbcf" / "fixtures" / "matched_http_effect_contract_v1.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_v1_is_prospective_and_not_ready():
    result = evaluate_effect_contract_v1(load())
    assert not result.ready
    assert result.blockers == (
        "contract_not_frozen",
        "failure_posture_not_frozen",
        "failure_posture_unresolved:acs",
        "failure_posture_unresolved:openshell",
        "failure_posture_unresolved:sbcf",
        "negative_observation_bound_unfrozen",
        "receiver_custody_unfrozen",
        "system_mapping_unfrozen:acs",
        "system_mapping_unfrozen:openshell",
        "system_mapping_unfrozen:sbcf",
    )


def test_v1_digest_is_deterministic():
    contract = load()
    assert effect_contract_v1_digest(contract) == effect_contract_v1_digest(copy.deepcopy(contract))


def test_control_plane_case_has_no_universal_expected_outcome():
    record = next(item for item in load()["cases"] if item["id"] == "control_plane_unavailable")
    assert record["scoring_mode"] == "STRATIFIED_FAILURE_POSTURE"
    assert record["expected_decision"] is None
    assert record["expected_effect"] is None


def test_normative_cases_remain_normative():
    records = {item["id"]: item for item in load()["cases"]}
    for case_id in ("exact_allow", "adjacent_host", "adjacent_method", "revoked_authority"):
        assert records[case_id]["scoring_mode"] == "NORMATIVE"


def test_v1_refuses_posthoc_normative_target():
    contract = load()
    contract["failure_posture"]["normative_target"] = "FAIL_CLOSED_DENY"
    with pytest.raises(ValueError, match="must not define a normative target"):
        validate_effect_contract_v1(contract)


def test_v1_refuses_failure_case_efficacy_scoring():
    contract = load()
    contract["failure_posture"]["efficacy_scoring"] = "INCLUDE"
    with pytest.raises(ValueError, match="scoring rule changed"):
        validate_effect_contract_v1(contract)


def test_receiver_custody_is_explicit_freeze_gate():
    contract = load()
    contract["witness"]["receiver_custody"]["independent_operator_required"] = False
    with pytest.raises(ValueError, match="independent operator"):
        validate_effect_contract_v1(contract)


def test_failure_posture_vocabulary_is_closed():
    contract = load()
    contract["failure_posture"]["system_postures"]["openshell"] = "STALE_POLICY_ALLOW"
    with pytest.raises(ValueError, match="invalid system failure posture"):
        validate_effect_contract_v1(contract)


def test_structural_ready_requires_frozen_system_postures():
    contract = load()
    contract["status"] = "FROZEN"
    contract["witness"]["negative_observation_bound_ms"] = 1000
    contract["witness"]["receiver_custody"]["status"] = "FROZEN"
    for system_id in contract["system_mappings"]:
        contract["system_mappings"][system_id] = "FROZEN"
    contract["failure_posture"]["status"] = "FROZEN"
    contract["failure_posture"]["system_postures"] = {
        "sbcf": "FAIL_CLOSED_DENY",
        "acs": "FAIL_CLOSED_DENY",
        "openshell": "LAST_KNOWN_GOOD",
    }

    result = evaluate_effect_contract_v1(contract)

    assert result.ready
    assert result.blockers == ()


def test_v1_does_not_mutate_v0_schema_identity():
    contract = load()
    contract["schema_version"] = "sbcf-matched-http-effect-v0"
    with pytest.raises(ValueError, match="unsupported matched effect v1 version"):
        validate_effect_contract_v1(contract)


def test_unknown_top_level_field_is_rejected():
    contract = load()
    contract["efficacy_claim"] = "superior"
    with pytest.raises(ValueError):
        validate_effect_contract_v1(contract)
