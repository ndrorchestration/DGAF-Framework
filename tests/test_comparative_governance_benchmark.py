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
    assert "not representative of all policy-as-code systems" in report["baseline_limitations"]["C_POLICY_AS_CODE"]


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
    rows = rows_for(benchmark.run(), "GB-003")
    assert rows["C_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["C_POLICY_AS_CODE"]["unsupported_claim_admitted"] == 1
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert rows["D_DGAF"]["unsupported_claim_admitted"] == 0


def test_composed_authority_is_not_inferred_from_individual_permissions() -> None:
    rows = rows_for(benchmark.run(), "GB-004")
    assert rows["C_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert "CHECK_COMPOSED_AUTHORITY" in rows["D_DGAF"]["decision_steps"]


def test_confused_deputy_is_blocked_by_delegated_requester_guard() -> None:
    rows = rows_for(benchmark.run(), "GB-005")
    assert rows["C_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert "CHECK_DELEGATED_REQUESTER" in rows["D_DGAF"]["decision_steps"]


def test_token_replay_is_blocked() -> None:
    rows = rows_for(benchmark.run(), "GB-006")
    assert rows["C_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert "CHECK_REPLAY" in rows["D_DGAF"]["decision_steps"]


def test_prompt_injection_cannot_change_authorized_intent() -> None:
    rows = rows_for(benchmark.run(), "GB-007")
    assert rows["C_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert "CHECK_INTENT_BINDING" in rows["D_DGAF"]["decision_steps"]


def test_compromised_subagent_fails_workload_attestation() -> None:
    rows = rows_for(benchmark.run(), "GB-008")
    assert rows["C_POLICY_AS_CODE"]["decision"] == "ALLOW"
    assert rows["D_DGAF"]["decision"] == "DENY"
    assert "CHECK_WORKLOAD_ATTESTATION" in rows["D_DGAF"]["decision_steps"]


def test_summary_exposes_benefit_and_cost_signals() -> None:
    report = benchmark.run()
    c = report["summary"]["C_POLICY_AS_CODE"]
    d = report["summary"]["D_DGAF"]

    assert c["cases"] == 8
    assert d["cases"] == 8
    assert c["unsafe_action_or_flow_admitted"] == 6
    assert d["unsafe_action_or_flow_admitted"] == 0
    assert c["false_block"] == 0
    assert d["false_block"] == 0
    assert d["decision_steps"] > c["decision_steps"]
