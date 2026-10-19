"""Decision/effect evidence boundary for BKRC first slice."""

from copy import deepcopy

import pytest

from experiments.governance_benchmark import bkrc_first_slice as target


@pytest.fixture(scope="module")
def report():
    return target.run()


def test_historical_fixtures_remain_unchanged():
    before = target.digest(target.FIXTURES)
    modified = target.inputs()
    modified[0][2]["action"]["authorized"] = False
    assert target.digest(target.FIXTURES) == before


def test_positive_controls_and_two_negative_challenges(report):
    assert [x["id"] for x in report["cases"]] == list(target.CASES)
    assert [x["c3"] for x in report["cases"]] == list(target.EXPECTED)
    assert [x["synthetic_d"] for x in report["cases"]] == list(target.EXPECTED)
    assert report["c3_synthetic_d_parity"] == 4
    assert report["matches_operator_expectation"] == 4


def test_claim_positive_control_changes_exactly_one_field():
    items = target.inputs()
    allowed = deepcopy(items[2][2])
    denied = deepcopy(items[3][2])
    denied["claim"]["requested_status"] = allowed["claim"]["requested_status"]
    assert target.case_bytes(allowed) == target.case_bytes(denied)


@pytest.mark.parametrize("case_id", target.CASES)
def test_a_decision_does_not_prove_absence_of_effect(report, case_id):
    row = next(x for x in report["cases"] if x["id"] == case_id)
    assert row["dispatch_observed"] == "NOT_INSTRUMENTED"
    assert row["effect_observed"] == "NOT_INSTRUMENTED"
    assert row["enforcement_receipt"] is None
    assert row["non_dispatch_proven"] is False
    assert row["independent_oracle"] == "NOT_ESTABLISHED"


def test_immutable_sources_and_claim_ceilings(report):
    assert report["historical_fixture_sha256"] == target.digest(target.FIXTURES)
    assert report["historical_c3_rule_file_sha256"] == target.digest(target.RULES_PATH)
    assert len(report["historical_c3_canonical_sha256"]) == 64
    assert report["observed_effect_count"] == "NOT_MEASURED"
    assert report["independently_validated_cases"] == report["scientific_n_increment"] == 0
    assert report["independent_validation"] == "NOT_ESTABLISHED"
    assert report["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert report["high_assurance"] == "NOT_AUTHORIZED"


def test_deterministic_report(report):
    assert target.run() == report
    assert len(report["source_head"]) == 40
