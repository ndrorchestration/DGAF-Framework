from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import mode_t_full_pilot_timing as full


def test_full_pilot_shape_is_exactly_50_by_180() -> None:
    assert full.PILOT_SEED_COUNT == 50
    assert full.component.expected_trials_per_seed() == 180
    assert full.expected_total_trials() == 9000


def test_complete_task_shape_executes_50_seeds_sequentially(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: list[int] = []

    monkeypatch.setattr(full.component, "expected_trials_per_seed", lambda: 180)

    def fake_measure(seed: int) -> float:
        observed.append(seed)
        return float(seed % 11) + 1.0

    monkeypatch.setattr(full.component, "measure_full_synthetic_matrix", fake_measure)

    result = full.measure_complete_task_shape(seed_base=1000)

    assert observed == list(range(1000, 1050))
    assert result["seed_count"] == 50
    assert result["trials_per_seed"] == 180
    assert result["total_trials"] == 9000
    assert result["execution_order"] == "sequential_seed_loop"
    assert result["per_seed_duration_statistics"]["sample_count"] == 50


def test_full_pilot_shape_rejects_partial_seed_count() -> None:
    with pytest.raises(ValueError, match="exactly 50"):
        full.measure_complete_task_shape(seed_base=1000, seed_count=49)


def test_full_pilot_shape_rejects_trial_shape_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(full.component, "expected_trials_per_seed", lambda: 179)
    with pytest.raises(RuntimeError, match="180 trials per seed"):
        full.measure_complete_task_shape(seed_base=1000)


def test_study_remains_not_w_eligible_after_full_task_measurement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(full.component, "expected_trials_per_seed", lambda: 180)

    def fake_complete(*, seed_base: int, seed_count: int = full.PILOT_SEED_COUNT) -> dict:
        assert seed_count == 50
        return {
            "seed_base": seed_base,
            "seed_count": 50,
            "trials_per_seed": 180,
            "total_trials": 9000,
            "execution_order": "sequential_seed_loop",
            "full_task_shape_duration_ms": 75000.0,
            "per_seed_duration_statistics": {
                "sample_count": 50,
                "min_ms": 1000.0,
                "p50_ms": 1500.0,
                "p95_ms": 1900.0,
                "max_ms": 2000.0,
                "mean_ms": 1500.0,
            },
        }

    monkeypatch.setattr(full, "measure_complete_task_shape", fake_complete)

    output = tmp_path / "full.json"
    artifact = full.run_study(output_path=output, repetitions=2)

    assert artifact["total_trials_per_repetition"] == 9000
    assert artifact["full_boundary_contiguous_timing_established"] is False
    assert artifact["complete_blinded_artifact_set_publication_timed"] is False
    assert artifact["accepted_independent_retention_timed"] is False
    assert artifact["external_transparency_timed"] is False
    assert artifact["coverage_complete"] is False
    assert artifact["w_proposal_eligible"] is False
    assert artifact["numeric_w_selected"] is False
    assert artifact["proposed_w_seconds"] is None
    assert artifact["empirical_data_collection"] is False
    assert artifact["protected_material_present"] is False
    assert artifact["pilot_authorized"] is False
    assert artifact["empirical_n"] == 0

    raw = output.read_bytes()
    sidecar = output.with_suffix(".json.sha256").read_text(encoding="utf-8")
    digest, name = sidecar.split()
    assert name == output.name
    assert digest == hashlib.sha256(raw).hexdigest()
    assert json.loads(raw)["epistemic_status"] == (
        "BOUNDED_FULL_TASK_SHAPE_NOT_COMPLETE_C_TO_L_TIMING"
    )


def test_repetition_bounds_fail_closed(tmp_path: Path) -> None:
    for invalid in (0, 11, True):
        with pytest.raises(ValueError):
            full.run_study(output_path=tmp_path / "x.json", repetitions=invalid)
