"""Tests for the neutral configuration-scaling falsification model."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_configuration_scaling.py"

spec = importlib.util.spec_from_file_location("configuration_scaling", MODULE_PATH)
assert spec and spec.loader
scaling = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scaling)


def test_both_architectures_get_reusable_abstractions() -> None:
    report = scaling.run()
    assert report["semantic_control_count"] == 12
    for row in report["rows"]:
        assert row["c3"]["shared_semantic_modules"] == 12
        assert row["dgaf"]["shared_semantic_modules"] == 12
        assert row["c3"]["scope_bindings"] == row["scope_count"]
        assert row["dgaf"]["scope_bindings"] == row["scope_count"]


def test_semantic_update_remains_constant_for_both() -> None:
    report = scaling.run()
    assert report["summary"]["c3_update_artifacts_touched"] == [1]
    assert report["summary"]["dgaf_update_artifacts_touched"] == [1]
    assert report["summary"]["semantic_update_growth"] == "CONSTANT_FOR_BOTH"


def test_scope_binding_growth_is_linear_for_both() -> None:
    report = scaling.run()
    assert report["scope_counts"] == [1, 8, 64, 512]
    assert report["summary"]["scope_binding_growth"] == "LINEAR_FOR_BOTH"
    for row in report["rows"]:
        assert row["c3"]["scope_bindings"] == row["dgaf"]["scope_bindings"]


def test_neutral_reuse_model_records_parity_as_falsification() -> None:
    report = scaling.run()
    assert report["summary"]["structural_scaling_parity"] is True
    assert report["falsification_outcome"] == "NO_UNIQUE_CONFIGURATION_SCALING_ADVANTAGE_IN_NEUTRAL_REUSE_MODEL"


def test_byte_size_is_explicitly_non_authoritative() -> None:
    report = scaling.run()
    boundary = " ".join(report["interpretation_boundary"])
    assert "must not be treated as burden scores" in boundary
    assert "STATE_OF_THE_ART_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED" in report["claim_ceiling"]
    assert "INDEPENDENT_VALIDATION_NOT_ESTABLISHED" in report["claim_ceiling"]
