"""Tests for bounded two-factor governance interactions."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_interactions.py"

spec = importlib.util.spec_from_file_location("governance_interactions", MODULE_PATH)
assert spec and spec.loader
interactions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(interactions)


def test_interaction_suite_is_bounded_and_non_promoting() -> None:
    report = interactions.run_interactions()
    assert report["interaction_count"] == 7
    assert report["evidence_class"] == "SYNTHETIC_TWO_FACTOR_ENGINEERING_EVIDENCE"
    assert "NO_EMERGENT_ROBUSTNESS_CLAIM" in report["claim_ceiling"]


def test_every_interaction_matches_declared_expectation() -> None:
    report = interactions.run_interactions()
    assert report["all_pass"] is True
    assert all(row["pass"] for row in report["rows"])


def test_authority_interactions_are_not_unique_dgaf_credit() -> None:
    report = interactions.run_interactions()
    rows = [
        row for row in report["rows"] if all(field.startswith("authority_context.") for field in row["mutated_fields"])
    ]
    assert rows
    for row in rows:
        if row["baseline"] == "C1_MINIMAL_POLICY_AS_CODE":
            assert row["decision"] == "ALLOW"
        else:
            assert row["decision"] == "DENY"


def test_claim_and_flow_interactions_remain_dgaf_incremental_scope() -> None:
    report = interactions.run_interactions()
    rows = [
        row for row in report["rows"] if any(field.startswith(("claim.", "flow.")) for field in row["mutated_fields"])
    ]
    assert rows
    for row in rows:
        if row["baseline"] == "D_DGAF":
            assert row["decision"] == "DENY"
        else:
            assert row["decision"] == "ALLOW"
