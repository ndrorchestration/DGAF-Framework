"""Tests for matched-semantics composition and recovery parity."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_recovery_composition_parity.py"

spec = importlib.util.spec_from_file_location("recovery_composition_parity", MODULE_PATH)
assert spec and spec.loader
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


def test_uses_merged_dgaf_reference_apis() -> None:
    report = benchmark.run()
    assert report["uses_merged_dgaf_reference_apis"] is True
    assert report["summary"]["cases"] == 11


def test_all_bounded_composition_and_recovery_cases_are_parity() -> None:
    report = benchmark.run()
    assert report["summary"]["parity_count"] == report["summary"]["cases"]
    assert report["summary"]["difference_count"] == 0
    assert all(row["parity"] for row in report["rows"])


def test_protected_egress_and_composition_denial_match() -> None:
    report = benchmark.run()
    rows = {row["case_id"]: row for row in report["rows"]}
    assert rows["COMPOSE_NOT_AUTHORIZED"]["c3"] == "DENY"
    assert rows["COMPOSE_NOT_AUTHORIZED"]["dgaf"] == "DENY"
    assert rows["COMPOSE_PROTECTED_EGRESS_BLOCKED"]["c3"] == "DENY"
    assert rows["COMPOSE_PROTECTED_EGRESS_BLOCKED"]["dgaf"] == "DENY"


def test_recovery_modes_match_for_partial_and_unknown_outcomes() -> None:
    report = benchmark.run()
    rows = {row["case_id"]: row for row in report["rows"]}
    assert rows["UNKNOWN_PROVIDER_OUTCOME"]["dgaf"]["recovery_mode"] == "RECONCILE"
    assert rows["PARTIAL_REVERSIBLE"]["dgaf"]["recovery_mode"] == "ROLLBACK"
    assert rows["PARTIAL_COMPENSATABLE"]["dgaf"]["recovery_mode"] == "COMPENSATE"
    assert rows["PARTIAL_IRREVERSIBLE"]["dgaf"]["recovery_mode"] == "CONTAIN_OR_ESCALATE"
    for case_id in (
        "UNKNOWN_PROVIDER_OUTCOME",
        "PARTIAL_REVERSIBLE",
        "PARTIAL_COMPENSATABLE",
        "PARTIAL_IRREVERSIBLE",
        "POSTCONDITION_FAILED",
        "SUCCESS",
    ):
        assert rows[case_id]["c3"] == rows[case_id]["dgaf"]


def test_unknown_retry_is_blocked_until_reconciled_for_both() -> None:
    report = benchmark.run()
    row = next(row for row in report["rows"] if row["case_id"] == "UNKNOWN_RETRY_RECONCILIATION")
    assert row["c3"]["retry"] == "RECONCILE_REQUIRED"
    assert row["dgaf"]["retry"] == "RECONCILE_REQUIRED"
    assert row["c3"]["after_reconcile_failed"] == "CLAIMED"
    assert row["dgaf"]["after_reconcile_failed"] == "CLAIMED"


def test_no_wrong_authority_or_stale_retry_continuation_in_cases() -> None:
    report = benchmark.run()
    summary = report["summary"]
    assert summary["wrong_authority_continuations_c3"] == 0
    assert summary["wrong_authority_continuations_dgaf"] == 0
    assert summary["stale_retry_continuations_c3"] == 0
    assert summary["stale_retry_continuations_dgaf"] == 0


def test_parity_is_falsification_not_equivalence_claim() -> None:
    report = benchmark.run()
    assert (
        report["falsification_outcome"]
        == "NO_UNIQUE_COMPOSITION_OR_RECOVERY_ADVANTAGE_IN_MATCHED_SEMANTICS_CASES"
    )
    boundary = " ".join(report["interpretation_boundary"])
    assert "not production incident evidence" in boundary
    assert "implementation complexity" in boundary
    assert "STATE_OF_THE_ART_NOT_ESTABLISHED" in report["claim_ceiling"]
