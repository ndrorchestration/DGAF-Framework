from pathlib import Path

from evaluations.contraction_proof_fidelity import (
    DEFAULT_FIXTURE,
    TARGET,
    evaluate,
    load_fixture,
)


def test_contraction_fixture_is_canonical_and_complete():
    fixture = load_fixture(DEFAULT_FIXTURE)
    assert fixture["evidence_class"] == "SYNTHETIC"
    assert len(fixture["cases"]) == 100
    assert sum(case["expected_contraction"] for case in fixture["cases"]) == 50
    assert sum(not case["expected_contraction"] for case in fixture["cases"]) == 50


def test_contraction_fidelity_reproduces_analytic_expectations():
    result = evaluate(DEFAULT_FIXTURE)
    assert result["sample_count"] == 100
    assert result["correct_count"] == 100
    assert result["score"] == 1.0
    assert result["target"] == TARGET == 0.98
    assert result["passed"] is True
    assert result["failure_analysis"] == []
