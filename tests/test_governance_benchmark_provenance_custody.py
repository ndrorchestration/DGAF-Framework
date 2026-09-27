"""Tests for matched provenance-custody falsification."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_provenance_custody_parity.py"

spec = importlib.util.spec_from_file_location("provenance_custody_parity", MODULE_PATH)
assert spec and spec.loader
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


def test_base_artifacts_are_valid() -> None:
    report = benchmark.run()
    assert report["uses_merged_reference_transaction"] is True
    assert report["base_artifacts_valid"] is True


def test_all_mutations_are_detected_by_both() -> None:
    report = benchmark.run()
    assert report["summary"]["mutation_cases"] == 8
    assert report["summary"]["detected_mutations_c3"] == 8
    assert report["summary"]["detected_mutations_dgaf"] == 8
    assert all(row["c3_detected"] and row["dgaf_detected"] for row in report["rows"])


def test_detection_and_operator_review_counts_are_parity() -> None:
    report = benchmark.run()
    assert report["summary"]["parity_count"] == 8
    assert report["summary"]["difference_count"] == 0
    assert report["summary"]["operator_review_count_c3"] == 8
    assert report["summary"]["operator_review_count_dgaf"] == 8


def test_expected_provenance_links_are_covered() -> None:
    report = benchmark.run()
    case_ids = {row["case_id"] for row in report["rows"]}
    assert case_ids == {
        "ACTION_DIGEST",
        "AUTHORIZATION_ID",
        "WORKFLOW_ID",
        "INVOCATION_ID",
        "CAPABILITY_ID",
        "ADAPTER_IDENTITY",
        "EXECUTOR_IDENTITY",
        "PROVIDER_RECEIPT_ID",
    }


def test_parity_is_falsification_not_equivalence_claim() -> None:
    report = benchmark.run()
    assert report["falsification_outcome"] == "NO_UNIQUE_PROVENANCE_CUSTODY_ADVANTAGE_IN_MATCHED_CHECKS"
    boundary = " ".join(report["interpretation_boundary"])
    assert "durable storage" in boundary
    assert "independent custody" in boundary
    assert "STATE_OF_THE_ART_NOT_ESTABLISHED" in report["claim_ceiling"]
