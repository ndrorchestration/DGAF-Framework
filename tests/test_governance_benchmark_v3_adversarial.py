"""Shared type-envelope behavior over deterministic operator-generated inputs."""

import pytest

from experiments.governance_benchmark.v3.characterize import characterize
from experiments.governance_benchmark.v3.input_envelope import (
    REJECTED,
    evaluate_all,
    validate,
)
from experiments.governance_benchmark.v3.probe_cases_v1 import cases

CASES = cases()


@pytest.mark.parametrize("index", range(370))
def test_each_case_has_no_partial_policy_call_on_rejected_envelope(index):
    case = CASES[index]
    checked = validate(case)
    calls = []

    def trap(input_data):
        calls.append(input_data)
        return "ALLOW", ["C1"]

    result = evaluate_all(case, {"C1": trap, "C2": trap, "D": trap, "C3": trap, "OPA": trap})
    if checked.status == REJECTED:
        assert calls == []
        assert all(decision == "NOT_EVALUATED" for decision in result["policy_results"].values())
    else:
        assert len(calls) == 5
        assert all(decision == "ALLOW" for decision in result["policy_results"].values())


def test_the_370_case_matrix_preserves_original_inputs_and_denominators():
    report = characterize(CASES)
    assert report["summary"]["cases"] == 370
    assert report["summary"]["admitted"] + report["summary"]["input_rejected"] == 370
    assert report["summary"]["input_rejected"] > 300
    assert all(
        value == "NOT_EVALUATED"
        for item in report["results"]
        if item["input_state"] == REJECTED
        for value in item["policy_results"].values()
    )
    assert report["scientific_n_increment"] == 0
