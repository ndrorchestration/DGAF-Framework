"""Closed-schema tests for the candidate matched HTTP effect contract."""

import copy
import json
from pathlib import Path

import pytest

from experiments.sbcf.matched_effect_contract import (
    effect_contract_digest,
    evaluate_effect_contract,
    validate_effect_contract,
)

FIXTURE = Path(__file__).parents[1] / "experiments" / "sbcf" / "fixtures" / "matched_http_effect_contract_v0.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_current_contract_is_candidate_and_not_ready():
    result = evaluate_effect_contract(load())
    assert not result.ready
    assert result.blockers == (
        "contract_not_frozen",
        "negative_observation_bound_unfrozen",
        "system_mapping_unfrozen:acs",
        "system_mapping_unfrozen:openshell",
        "system_mapping_unfrozen:sbcf",
    )


def test_candidate_digest_is_deterministic():
    contract = load()
    assert effect_contract_digest(contract) == effect_contract_digest(copy.deepcopy(contract))


def test_exact_case_set_is_required():
    contract = load()
    contract["cases"].pop()
    with pytest.raises(ValueError):
        validate_effect_contract(contract)


def test_case_semantics_cannot_be_silently_relabelled():
    contract = load()
    contract["cases"][1]["expected_decision"] = "ALLOW"
    with pytest.raises(ValueError, match="semantics changed"):
        validate_effect_contract(contract)


def test_effect_identity_fields_are_fixed():
    contract = load()
    contract["effect_identity_fields"].remove("body_sha256")
    with pytest.raises(ValueError, match="identity fields changed"):
        validate_effect_contract(contract)


@pytest.mark.parametrize("bound", [0, -1, True, 1.5, "1000"])
def test_negative_observation_bound_must_be_positive_integer_or_null(bound):
    contract = load()
    contract["witness"]["negative_observation_bound_ms"] = bound
    with pytest.raises(ValueError):
        validate_effect_contract(contract)


def test_frozen_label_cannot_hide_unresolved_negative_observation_bound():
    contract = load()
    contract["status"] = "FROZEN"
    for system_id in contract["system_mappings"]:
        contract["system_mappings"][system_id] = "FROZEN"

    result = evaluate_effect_contract(contract)

    assert not result.ready
    assert result.blockers == ("negative_observation_bound_unfrozen",)


def test_all_declared_prerequisites_can_make_structural_contract_ready():
    contract = load()
    contract["status"] = "FROZEN"
    contract["witness"]["negative_observation_bound_ms"] = 1000
    for system_id in contract["system_mappings"]:
        contract["system_mappings"][system_id] = "FROZEN"

    result = evaluate_effect_contract(contract)

    assert result.ready
    assert result.blockers == ()


def test_unresolved_acs_mapping_blocks_even_after_other_fields_freeze():
    contract = load()
    contract["status"] = "FROZEN"
    contract["witness"]["negative_observation_bound_ms"] = 1000
    contract["system_mappings"]["sbcf"] = "FROZEN"
    contract["system_mappings"]["openshell"] = "FROZEN"

    result = evaluate_effect_contract(contract)

    assert result.blockers == ("system_mapping_unfrozen:acs",)


def test_unknown_system_mapping_state_is_rejected():
    contract = load()
    contract["system_mappings"]["acs"] = "ASSUMED_EQUIVALENT"
    with pytest.raises(ValueError):
        validate_effect_contract(contract)


def test_unknown_top_level_field_is_rejected():
    contract = load()
    contract["efficacy_claim"] = "superior"
    with pytest.raises(ValueError):
        validate_effect_contract(contract)


def test_trial_id_is_bound_to_fixed_receiver_header():
    contract = load()
    assert contract["witness"]["trial_id_binding"] == {
        "kind": "FIXED_HEADER",
        "header_name": "X-SBCF-Trial-ID",
    }


@pytest.mark.parametrize(
    ("kind", "header"),
    [
        ("QUERY_PARAMETER", "X-SBCF-Trial-ID"),
        ("FIXED_HEADER", "X-Other-Trial-ID"),
    ],
)
def test_trial_id_binding_cannot_be_silently_relabelled(kind, header):
    contract = load()
    contract["witness"]["trial_id_binding"] = {
        "kind": kind,
        "header_name": header,
    }
    with pytest.raises(ValueError):
        validate_effect_contract(contract)
