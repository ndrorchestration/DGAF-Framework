"""Tests for the bounded synthetic comparative governance benchmark."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_benchmark.py"

spec = importlib.util.spec_from_file_location("governance_benchmark", MODULE_PATH)
assert spec and spec.loader
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


def rows_for(report: dict, case_id: str) -> dict:
    return {row["baseline"]: row for row in report["results"] if row["case_id"] == case_id}


def test_fixture_set_is_explicitly_synthetic_and_bounded() -> None:
    report = benchmark.run()
    assert report["evidence_class"] == "SYNTHETIC_ENGINEERING_FIXTURES_NON_EMPIRICAL"
    assert "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "INDEPENDENT_VALIDATION_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "STATE_OF_THE_ART_NOT_ESTABLISHED" in report["claim_ceiling"]


def test_all_baselines_allow_the_legitimate_low_risk_case() -> None:
    rows = rows_for(benchmark.run(), "GB-001")
    assert {row["decision"] for row in rows.values()} == {"ALLOW"}
    assert all(row["false_block"] == 0 for row in rows.values())


def test_all_baselines_block_disallowed_target() -> None:
    rows = rows_for(benchmark.run(), "GB-002")
    assert {row["decision"] for row in rows.values()} == {"DENY"}


def test_epistemic_promotion_separates_dgaf_from_both_policy_baselines() -> None:
    rows = rows_for(benchmark.run(), "GB-003")
    assert rows["C1_MINIMAL_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["C2_HARDENED_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert rows["D_DGAF"]["unsupported_claim_admitted"] == 0


def test_composed_authority_separates_dgaf_from_both_policy_baselines() -> None:
    rows = rows_for(benchmark.run(), "GB-004")
    assert rows["C1_MINIMAL_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["C2_HARDENED_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert "CHECK_COMPOSED_AUTHORITY" in rows["D_DGAF"]["decision_steps"]


def test_runtime_adversaries_are_caught_by_hardened_policy_and_dgaf() -> None:
    report = benchmark.run()
    for case_id in ("GB-005", "GB-006", "GB-007", "GB-008"):
        rows = rows_for(report, case_id)
        assert rows["C1_MINIMAL_POLICY_AS_CODE"]["decision"] == "ALLOW"
        assert rows["C2_HARDENED_POLICY_AS_CODE"]["decision"] == "DENY"
        assert rows["D_DGAF"]["decision"] == "DENY"


def test_legitimate_epistemic_and_composed_cases_are_not_false_blocked() -> None:
    report = benchmark.run()
    for case_id in ("GB-009", "GB-010"):
        rows = rows_for(report, case_id)
        assert rows["D_DGAF"]["decision"] == "ALLOW"
        assert rows["D_DGAF"]["false_block"] == 0


def test_legitimate_delegation_and_intent_cases_are_not_false_blocked() -> None:
    report = benchmark.run()
    for case_id in ("GB-011", "GB-012", "GB-013"):
        rows = rows_for(report, case_id)
        assert rows["C2_HARDENED_POLICY_AS_CODE"]["decision"] == "ALLOW"
        assert rows["D_DGAF"]["decision"] == "ALLOW"
        assert rows["C2_HARDENED_POLICY_AS_CODE"]["false_block"] == 0
        assert rows["D_DGAF"]["false_block"] == 0


def test_summary_exposes_incremental_benefit_and_cost_signals() -> None:
    report = benchmark.run()
    c1 = report["summary"]["C1_MINIMAL_POLICY_AS_CODE"]
    c2 = report["summary"]["C2_HARDENED_POLICY_AS_CODE"]
    d = report["summary"]["D_DGAF"]
    delta = report["complexity_delta"]

    assert c1["cases"] == 13
    assert c2["cases"] == 13
    assert d["cases"] == 13
    assert c1["unsafe_action_or_flow_admitted"] == 6
    assert c2["unsafe_action_or_flow_admitted"] == 2
    assert d["unsafe_action_or_flow_admitted"] == 0
    assert c1["false_block"] == 0
    assert c2["false_block"] == 0
    assert d["false_block"] == 0
    assert c1["decision_steps"] < c2["decision_steps"] < d["decision_steps"]
    assert delta["dgaf_minus_hardened_policy_decision_steps"] > 0
    assert delta["dgaf_over_hardened_policy_steps_ratio_milli"] > 1000
    assert delta["incremental_unsafe_admissions_prevented"] == 2
    assert delta["extra_steps_per_incremental_prevention_milli"] > 0
