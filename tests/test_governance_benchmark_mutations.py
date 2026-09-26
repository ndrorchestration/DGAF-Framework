"""Tests for deterministic governance-benchmark mutations."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_mutations.py"

spec = importlib.util.spec_from_file_location("governance_mutations", MODULE_PATH)
assert spec and spec.loader
mutations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutations)


def test_mutation_suite_has_bounded_non_random_scope() -> None:
    report = mutations.run_mutations()
    assert report["mutation_count"] == 10
    assert report["evidence_class"] == "SYNTHETIC_METAMORPHIC_ENGINEERING_EVIDENCE"
    assert "STATE_OF_THE_ART_NOT_ESTABLISHED" in report["claim_ceiling"]


def test_every_mutation_matches_its_metamorphic_expectation() -> None:
    report = mutations.run_mutations()
    assert report["all_pass"] is True
    assert all(row["pass"] for row in report["rows"])


def test_authority_mutations_are_caught_without_crediting_minimal_policy() -> None:
    report = mutations.run_mutations()
    rows = [row for row in report["rows"] if row["mutated_field"].startswith("authority_context.")]
    assert rows
    for row in rows:
        if row["baseline"] == "C1_MINIMAL_POLICY_AS_CODE":
            assert row["decision"] == "ALLOW"
        else:
            assert row["decision"] == "DENY"


def test_epistemic_and_flow_mutations_isolate_dgaf_increment() -> None:
    report = mutations.run_mutations()
    rows = [
        row
        for row in report["rows"]
        if row["mutated_field"].startswith(("claim.", "flow."))
    ]
    assert rows
    for row in rows:
        if row["baseline"] == "D_DGAF":
            assert row["decision"] == "DENY"
        else:
            assert row["decision"] == "ALLOW"
