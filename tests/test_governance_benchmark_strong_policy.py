"""Tests for the strong policy-as-code falsification comparator."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_strong_policy_comparator.py"

spec = importlib.util.spec_from_file_location("strong_policy_comparator", MODULE_PATH)
assert spec and spec.loader
comparator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comparator)


def test_ruleset_is_frozen_and_machine_identified() -> None:
    report = comparator.run()
    assert report["rules_frozen_before_result_inspection"] is True
    assert report["ruleset_version"] == "C3_STRONG_POLICY_AS_CODE_V1"
    assert len(report["ruleset_sha256"]) == 64
    assert report["configuration_complexity"]["rule_count"] == 12
    assert report["configuration_complexity"]["canonical_policy_bytes"] > 0


def test_strong_policy_reproduces_dgaf_decisions_on_current_fixed_fixtures() -> None:
    report = comparator.run()
    assert report["summary"]["cases"] == 13
    assert report["summary"]["parity_count"] == 13
    assert report["summary"]["difference_count"] == 0
    assert report["falsification_outcome"] == "PARITY_ON_CURRENT_FIXED_FIXTURES"
    assert all(row["parity"] for row in report["results"])


def test_parity_preserves_correctness_and_false_block_accounting() -> None:
    report = comparator.run()
    summary = report["summary"]
    assert summary["strong_policy_task_correct"] == 13
    assert summary["dgaf_task_correct"] == 13
    assert summary["strong_policy_false_blocks"] == 0
    assert summary["dgaf_false_blocks"] == 0


def test_parity_is_recorded_as_falsification_not_superiority() -> None:
    report = comparator.run()
    boundary = " ".join(report["interpretation_boundary"])
    assert "weakens any claim" in boundary
    assert "does not show architectural equivalence" in boundary
    assert "STATE_OF_THE_ART_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "INDEPENDENT_VALIDATION_NOT_ESTABLISHED" in report["claim_ceiling"]


def test_rules_cover_claim_and_flow_fields_not_only_runtime_authority() -> None:
    policy = comparator.load_rules()
    encoded = str(policy["rules"])
    assert "claim.evidence_present" in encoded
    assert "claim.verification_class" in encoded
    assert "flow.provenance_known" in encoded
    assert "flow.composition_authorized" in encoded
