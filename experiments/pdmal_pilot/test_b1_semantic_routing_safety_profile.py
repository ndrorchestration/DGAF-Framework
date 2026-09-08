from copy import deepcopy

import pytest

from experiments.pdmal_pilot.b1_semantic_routing_safety_profile import (
    evaluate_record,
    registered_fixtures,
    run_registered_fixtures,
)


def _by_id():
    return {item["record_id"]: item for item in run_registered_fixtures()}


def test_registered_fixtures_cover_required_source_paths() -> None:
    results = _by_id()
    assert set(results) == {
        "clean-governance",
        "ambiguous-mixed",
        "adversarial",
        "low-confidence-balanced",
        "deontic-forbidden",
    }

    assert results["clean-governance"]["kappa_category"] == "governance_clear"
    assert results["clean-governance"]["classification"] == "PASS"

    assert results["ambiguous-mixed"]["kappa_category"] == "ambiguous"

    assert results["adversarial"]["kappa_category"] == "adversarial"
    assert results["adversarial"]["kappa_policy"] == "apply_strong"
    assert results["adversarial"]["classification"] == "BLOCK"

    assert results["low-confidence-balanced"]["kappa_policy"] == "fallback_balanced"
    assert "risk_warn" in results["low-confidence-balanced"]["sentinel_risks"]
    assert results["low-confidence-balanced"]["classification"] == "REVIEW"

    assert results["deontic-forbidden"]["deontic_gate"]["gate"] == "forbidden"
    assert results["deontic-forbidden"]["kappa_policy"] == "apply_strong"
    assert "risk_block" in results["deontic-forbidden"]["sentinel_risks"]
    assert results["deontic-forbidden"]["classification"] == "BLOCK"


def test_outputs_are_nonempirical_and_claim_bounded() -> None:
    for result in run_registered_fixtures():
        assert result["scientific_n_increment"] == 0
        assert result["empirical_execution_authorized"] is False
        assert result["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"


@pytest.mark.parametrize("mutation", ["missing", "extra", "bad_score", "bad_deontic", "deontic_mismatch"])
def test_schema_or_semantic_drift_fails_closed(mutation: str) -> None:
    record = deepcopy(registered_fixtures()[0])
    if mutation == "missing":
        record.pop("entropy_score")
    elif mutation == "extra":
        record["unexpected"] = True
    elif mutation == "bad_score":
        record["scores"]["accuracy"] = 2.0
    elif mutation == "bad_deontic":
        record["deontic"] = "unknown"
    elif mutation == "deontic_mismatch":
        record["deontic"] = "permitted"
    with pytest.raises(ValueError):
        evaluate_record(record)


def test_demijoule_current_source_limitation_is_observable() -> None:
    decisions = {result["demijoule_decision"] for result in run_registered_fixtures()}
    assert "reprompt" not in decisions
    assert decisions <= {"pass", "kill"}
