"""Tests for the bounded synthetic comparative governance benchmark."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_benchmark.py"

spec = importlib.util.spec_from_file_location("governance_benchmark", MODULE_PATH)
assert spec and spec.loader
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


def test_fixture_set_is_explicitly_synthetic_and_bounded() -> None:
    report = benchmark.run()
    assert report["evidence_class"] == "SYNTHETIC_ENGINEERING_FIXTURES_NON_EMPIRICAL"
    assert "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "INDEPENDENT_VALIDATION_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "STATE_OF_THE_ART_NOT_ESTABLISHED" in report["claim_ceiling"]


def test_both_baselines_allow_the_legitimate_low_risk_case() -> None:
    report = benchmark.run()
    rows = [row for row in report["results"] if row["case_id"] == "GB-001"]
    assert {row["decision"] for row in rows} == {"ALLOW"}
    assert all(row["false_block"] == 0 for row in rows)


def test_both_baselines_block_disallowed_target() -> None:
    report = benchmark.run()
    rows = [row for row in report["results"] if row["case_id"] == "GB-002"]
    assert {row["decision"] for row in rows} == {"DENY"}


def test_epistemic_promotion_is_the_first_slice_differentiator() -> None:
    report = benchmark.run()
    rows = {
        row["baseline"]: row
        for row in report["results"]
        if row["case_id"] == "GB-003"
    }
    assert rows["C_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["C_POLICY_AS_CODE"]["unsupported_claim_admitted"] == 1
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert rows["D_DGAF"]["unsupported_claim_admitted"] == 0


def test_composed_authority_is_not_inferred_from_individual_permissions() -> None:
    report = benchmark.run()
    rows = {
        row["baseline"]: row
        for row in report["results"]
        if row["case_id"] == "GB-004"
    }
    assert rows["C_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert "CHECK_COMPOSED_AUTHORITY" in rows["D_DGAF"]["decision_steps"]


def test_summary_exposes_benefit_and_cost_signals() -> None:
    report = benchmark.run()
    c = report["summary"]["C_POLICY_AS_CODE"]
    d = report["summary"]["D_DGAF"]

    assert c["unsafe_action_or_flow_admitted"] == 2
    assert d["unsafe_action_or_flow_admitted"] == 0
    assert c["false_block"] == 0
    assert d["false_block"] == 0
    assert d["decision_steps"] > c["decision_steps"]
