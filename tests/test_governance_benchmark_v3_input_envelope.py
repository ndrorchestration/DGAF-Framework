"""Candidate V3 shared envelope: no frozen comparator rewriting or scientific inference."""

import copy
import json
from pathlib import Path

import pytest

from experiments.governance_benchmark.v3.characterize import characterize, comparators
from experiments.governance_benchmark.v3.input_envelope import (
    REJECTED,
    contract_sha256,
    evaluate_all,
    validate,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "experiments/governance_benchmark/fixtures_v1.json"
AXES = ("authorized", "tool_allowed", "target_allowed")


def positive():
    return {
        "action": {"authorized": True, "tool_allowed": True, "target_allowed": True},
        "authority_context": None,
        "claim": None,
        "flow": None,
    }


def test_all_13_historical_fixtures_are_accepted_before_policy_evaluation():
    cases = json.loads(FIXTURES.read_text())["cases"]
    assert len(cases) == 13
    assert all(validate(case).status == "ADMITTED_FOR_COMPARISON" for case in cases)
    report = characterize(cases)
    assert report["summary"] == {
        "cases": 13,
        "admitted": 13,
        "input_rejected": 0,
        "four_way_parity_on_admitted": 7,
    }
    assert report["scientific_n_increment"] == 0
    assert report["real_opa_executed"] is False
    assert len(contract_sha256()) == 64


def test_historical_model_c3_disagreement_is_not_erased():
    report = characterize(json.loads(FIXTURES.read_text())["cases"])
    assert all(
        row["policy_results"]["D_SYNTHETIC_HISTORICAL"] == row["policy_results"]["C3_HISTORICAL"]
        for row in report["results"]
    )


@pytest.mark.parametrize("bad", [1, 0, -1, 1.2, "true", [], {}, None, "True"])
@pytest.mark.parametrize("axis", AXES)
def test_bad_action_predicate_never_invokes_any_policy(bad, axis):
    case = positive()
    case["action"][axis] = bad
    called = []

    def would_have_allowed(payload):
        called.append(payload)
        return "ALLOW", ["NEVER"]

    policies = {name: would_have_allowed for name in ("C1", "C2", "D", "C3", "OPA")}
    result = evaluate_all(case, policies)
    assert result["input_state"] == REJECTED
    assert result["policy_results"] == dict.fromkeys(policies, "NOT_EVALUATED")
    assert called == []


@pytest.mark.parametrize("bad", [None, [], 1, True, "x", {"authorized": 1}])
def test_nonobject_or_incomplete_action_fails_typed(bad):
    case = positive()
    case["action"] = bad
    assert validate(case).status == REJECTED


@pytest.mark.parametrize("domain", ["authority_context", "claim", "flow"])
@pytest.mark.parametrize("bad", [True, [], 1, "bad", {}, {"unexpected": True}])
def test_supplied_optional_domain_must_be_complete_typed_object(domain, bad):
    case = positive()
    case[domain] = bad
    assert validate(case).status == REJECTED


def test_all_three_optional_domains_may_be_absent_or_null():
    case = {"action": positive()["action"]}
    assert validate(case).status == "ADMITTED_FOR_COMPARISON"
    out = validate(case).admitted
    assert out is not None
    assert out["claim"] is None and out["flow"] is None and out["authority_context"] is None


def test_complete_positive_optional_domain_continues_to_policy():
    case = {
        **positive(),
        "authority_context": {
            "delegated_requester_authorized": True,
            "token_replay_detected": False,
            "request_bound_to_authorized_intent": True,
            "workload_attested": True,
            "child_scope_subset": True,
        },
        "claim": {
            "evidence_present": True,
            "evidence_fresh": True,
            "requested_status": "SAME_SYSTEM_NONINDEPENDENT",
            "verification_class": "SAME_SYSTEM_NONINDEPENDENT",
        },
        "flow": {
            "provenance_known": True,
            "source_classification": "PUBLIC",
            "destination_class": "INTERNAL",
            "composition_authorized": False,
        },
    }
    report = evaluate_all(case, comparators())
    assert report["input_state"] == "ADMITTED_FOR_COMPARISON"
    assert all(x == "ALLOW" for x in report["policy_results"].values())


def test_input_is_not_mutated():
    case = positive()
    original = copy.deepcopy(case)
    assert validate(case).status == "ADMITTED_FOR_COMPARISON"
    assert case == original
    normalized = validate(case).admitted
    assert normalized is not case and normalized["action"] is not case["action"]


@pytest.mark.parametrize(
    "case",
    [
        {**positive(), "extra_authority": True},
        {**positive(), "action": {**positive()["action"], "trusted": True}},
        {**positive(), "claim": {"evidence_present": True}},
        {1: "nonjsonkey", **positive()},
        {**positive(), "action": {1: True, **positive()["action"]}},
    ],
)
def test_unknown_and_nonstring_mapping_keys_return_typed_rejection(case):
    assert validate(case).status == REJECTED


@pytest.mark.parametrize("bad", [None, [], True, "text", 1, 2.0])
def test_nonobject_root_never_executes_comparator(bad):
    assert evaluate_all(bad, {"OPA": lambda _: ("ALLOW", [])})["policy_results"]["OPA"] == "NOT_EVALUATED"


def test_invalid_input_report_is_explicitly_not_a_policy_deny():
    result = characterize([{**positive(), "action": {**positive()["action"], "authorized": 1}}])
    assert result["summary"]["input_rejected"] == 1
    assert result["summary"]["admitted"] == 0
    assert result["results"][0]["policy_results"]["D_SYNTHETIC_HISTORICAL"] == "NOT_EVALUATED"


def test_four_way_positive_and_denial_controls():
    admitted = characterize(
        [
            positive(),
            {**positive(), "action": {**positive()["action"], "authorized": False}},
        ]
    )
    assert [row["policy_results"]["D_SYNTHETIC_HISTORICAL"] for row in admitted["results"]] == ["ALLOW", "DENY"]
    assert admitted["summary"]["four_way_parity_on_admitted"] == 2
