"""Tests for bounded exhaustive semantic-equivalence falsification."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_semantic_equivalence.py"

spec = importlib.util.spec_from_file_location("semantic_equivalence", MODULE_PATH)
assert spec and spec.loader
equivalence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(equivalence)


def test_enumeration_dimensions_are_explicit() -> None:
    report = equivalence.run()
    scope = report["enumeration_scope"]
    assert scope["action_states"] == 8
    assert scope["authority_states"] == 33
    assert scope["claim_states"] == 17
    assert scope["flow_states"] == 25
    assert scope["total_cases"] == 112200


def test_c3_and_dgaf_are_equivalent_on_current_enumerated_schema() -> None:
    report = equivalence.run()
    assert report["summary"]["difference_count"] == 0
    assert report["summary"]["parity_count"] == 112200
    assert report["summary"]["semantically_equivalent_on_enumerated_schema"] is True
    assert report["summary"]["strong_policy_allow_count"] == report["summary"]["dgaf_allow_count"]


def test_equivalence_result_preserves_claim_ceiling() -> None:
    report = equivalence.run()
    assert "SCIENTIFIC_N_INCREMENT_0" in report["claim_ceiling"]
    assert "INDEPENDENT_VALIDATION_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "STATE_OF_THE_ART_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "HIGH_ASSURANCE_NOT_AUTHORIZED" in report["claim_ceiling"]


def test_report_does_not_claim_architectural_equivalence() -> None:
    boundary = " ".join(equivalence.run()["interpretation_boundary"])
    assert "decision-function equivalence only" in boundary
    assert "not establish architectural equivalence" in boundary
