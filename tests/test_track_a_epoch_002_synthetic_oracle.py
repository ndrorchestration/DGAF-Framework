from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts/run_track_a_epoch_002_synthetic_oracle.py"
ANALYSIS_PATH = ROOT / "experiments/pdmal_pilot/track_a_epoch_002_analysis.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_synthetic_oracle_fixture_has_exact_track_a_shape() -> None:
    runner = load_module(RUNNER_PATH, "synthetic_oracle_fixture_test")
    records = runner.build_records("positive_constant")

    assert len(records) == 2250
    keys = {
        (row["seed_id"], row["topology"], row["failure_count"]) for row in records
    }
    assert len(keys) == 2250
    assert all(row["algorithm_id"] == runner.ALGORITHM_ID for row in records)
    assert all(isinstance(row["ffcr_success"], bool) for row in records)


@pytest.mark.parametrize(
    ("scenario", "expected_estimate", "expected_classification"),
    [
        (
            "positive_constant",
            4.0 / 9.0,
            "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS",
        ),
        (
            "null_constant",
            0.0,
            "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED",
        ),
        (
            "negative_constant",
            -4.0 / 9.0,
            "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS",
        ),
        (
            "balanced_mixed",
            0.0,
            "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED",
        ),
    ],
)
def test_known_truth_is_recovered(
    scenario: str,
    expected_estimate: float,
    expected_classification: str,
) -> None:
    runner = load_module(RUNNER_PATH, f"synthetic_oracle_{scenario}")
    analysis = load_module(ANALYSIS_PATH, f"frozen_analysis_{scenario}")
    result = analysis.analyze(runner.build_records(scenario))

    assert result["estimate_pdmal_minus_random_regular"] == pytest.approx(
        expected_estimate,
        abs=1e-12,
    )
    assert result["classification"] == expected_classification
    runner.validate_oracle_result(scenario, result)


def test_primary_result_is_invariant_to_record_order_and_nuisance_topologies() -> None:
    runner = load_module(RUNNER_PATH, "synthetic_oracle_invariance")
    analysis = load_module(ANALYSIS_PATH, "frozen_analysis_invariance")

    baseline = analysis.analyze(runner.build_records("positive_constant"))
    reordered = analysis.analyze(
        list(reversed(runner.build_records("positive_constant")))
    )
    nuisance_inverted = analysis.analyze(
        runner.build_records("positive_constant", invert_nuisance=True)
    )

    assert runner.canonical_bytes(reordered) == runner.canonical_bytes(baseline)
    assert runner.canonical_bytes(nuisance_inverted) == runner.canonical_bytes(
        baseline
    )


def test_fail_closed_negative_controls_reject_malformed_synthetic_data() -> None:
    runner = load_module(RUNNER_PATH, "synthetic_oracle_negative_controls")
    analysis = load_module(ANALYSIS_PATH, "frozen_analysis_negative_controls")

    missing = runner.build_records("positive_constant")
    missing.pop()
    with pytest.raises(ValueError, match="expected exactly 2250 records"):
        analysis.analyze(missing)

    duplicate = runner.build_records("positive_constant")
    duplicate[-1] = dict(duplicate[0])
    with pytest.raises(ValueError, match="duplicate matrix cell"):
        analysis.analyze(duplicate)

    non_boolean = runner.build_records("positive_constant")
    non_boolean[0]["ffcr_success"] = 1
    with pytest.raises(ValueError, match="ffcr_success must be boolean"):
        analysis.analyze(non_boolean)

    wrong_algorithm = runner.build_records("positive_constant")
    wrong_algorithm[0]["algorithm_id"] = "SYNTHETIC_WRONG"
    with pytest.raises(ValueError, match="algorithm identity does not match"):
        analysis.analyze(wrong_algorithm)

    excluded = runner.build_records("positive_constant")
    excluded[0]["excluded"] = True
    with pytest.raises(ValueError, match="outcome exclusions are prohibited"):
        analysis.analyze(excluded)
