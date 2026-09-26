"""Tests for bounded cross-domain governance interactions."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_cross_domain.py"

spec = importlib.util.spec_from_file_location("governance_cross_domain", MODULE_PATH)
assert spec and spec.loader
cross_domain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cross_domain)


def test_cross_domain_suite_is_bounded_and_non_promoting() -> None:
    report = cross_domain.run_cross_domain_interactions()
    assert report["interaction_count"] == 6
    assert report["evidence_class"] == "SYNTHETIC_CROSS_DOMAIN_ENGINEERING_EVIDENCE"
    assert "NO_GENERAL_COMPOSITIONAL_ROBUSTNESS_CLAIM" in report["claim_ceiling"]


def test_every_cross_domain_interaction_matches_declared_expectation() -> None:
    report = cross_domain.run_cross_domain_interactions()
    assert report["all_pass"] is True
    assert all(row["pass"] for row in report["rows"])


def test_hardened_policy_gets_credit_when_authority_domain_already_blocks() -> None:
    report = cross_domain.run_cross_domain_interactions()
    rows = [
        row for row in report["rows"] if any(field.startswith("authority_context.") for field in row["mutated_fields"])
    ]
    assert rows
    for row in rows:
        if row["baseline"] == "C1_MINIMAL_POLICY_AS_CODE":
            assert row["decision"] == "ALLOW"
        else:
            assert row["decision"] == "DENY"


def test_claim_flow_cross_domain_cases_isolate_dgaf_increment() -> None:
    report = cross_domain.run_cross_domain_interactions()
    rows = [
        row
        for row in report["rows"]
        if not any(field.startswith("authority_context.") for field in row["mutated_fields"])
    ]
    assert rows
    for row in rows:
        if row["baseline"] == "D_DGAF":
            assert row["decision"] == "DENY"
        else:
            assert row["decision"] == "ALLOW"
