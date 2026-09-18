from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/summarize_synthetic_assurance_cascade.py"


def load_module():
    spec = importlib.util.spec_from_file_location("synthetic_assurance_summary", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def full_fixture() -> dict:
    return {
        "evidence_class": "P4_MODE_T_SYNTHETIC_FULL_PILOT_TASK_TIMING_V1",
        "total_trials_per_repetition": 9000,
        "synthetic_seed_count_per_repetition": 50,
        "trials_per_seed": 180,
        "empirical_data_collection": False,
        "protected_material_present": False,
        "pilot_authorized": False,
        "empirical_n": 0,
        "full_task_shape_duration_statistics": {
            "sample_count": 1,
            "min_ms": 1.0,
            "p50_ms": 1.0,
            "p95_ms": 1.0,
            "max_ms": 1.0,
            "mean_ms": 1.0,
        },
    }


def partial_fixture() -> dict:
    return {
        "evidence_class": "P4_MODE_T_SYNTHETIC_TIMING_PARTIAL_V1",
        "empirical_data_collection": False,
        "pilot_authorized": False,
        "numeric_w_selected": False,
        "w_proposal_eligible": False,
        "stages": {
            "full_synthetic_matrix_timing": {
                "status": "PASS",
                "trials_per_repetition": 180,
                "statistics": {"sample_count": 1},
            },
            "locked_primary_analysis_timing": {
                "status": "PASS",
                "synthetic_seed_count": 50,
                "statistics": {"sample_count": 1},
            },
            "synthetic_timelock_encryption_timing": {"status": "NOT_EXECUTED"},
            "external_transparency_retention_timing": {"status": "NOT_EXECUTED"},
            "artifact_publication_retention_timing": {"status": "NOT_EXECUTED"},
        },
    }


def weighted_fixture() -> dict:
    return {
        "epistemic_classification": {
            "track_a_state_effect": "NONE",
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
        "protocol": {
            "total_trials": 480,
            "calibration_trials": 240,
            "heldout_trials": 240,
        },
        "variance_restoration": {"total_trials": 480, "fraction": 1.0},
        "heldout_detector_summary": {"detector": {"mean_tpr": 0.5}},
    }


def test_build_summary_preserves_nonempirical_boundary() -> None:
    module = load_module()
    summary = module.build_summary(
        full_fixture(),
        partial_fixture(),
        weighted_fixture(),
        {"tests": 100, "failures": 0, "errors": 0, "skipped": 2},
    )

    assert summary["classification"] == "SYNTHETIC_ENGINEERING_ASSURANCE_ONLY"
    assert summary["empirical_data_used"] is False
    assert summary["protected_material_used"] is False
    assert summary["real_materialization_performed"] is False
    assert summary["real_primary_analysis_performed"] is False
    assert summary["scientific_n_increment"] == 0
    assert summary["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert summary["measurements"]["full_pilot_shape"]["total_trials"] == 9000
    assert summary["measurements"]["weighted_forman_falsification"]["total_trials"] == 480


def test_summary_rejects_empirical_promotion() -> None:
    module = load_module()
    full = full_fixture()
    full["empirical_n"] = 1

    with pytest.raises(ValueError, match="empirical N=0"):
        module.build_summary(
            full,
            partial_fixture(),
            weighted_fixture(),
            {"tests": 1, "failures": 0, "errors": 0, "skipped": 0},
        )


def test_summary_rejects_failed_junit_evidence() -> None:
    module = load_module()

    with pytest.raises(ValueError, match="failures/errors"):
        module.build_summary(
            full_fixture(),
            partial_fixture(),
            weighted_fixture(),
            {"tests": 1, "failures": 1, "errors": 0, "skipped": 0},
        )


def test_weighted_forman_split_must_remain_preregistered() -> None:
    module = load_module()
    weighted = weighted_fixture()
    weighted["protocol"]["heldout_trials"] = 239

    with pytest.raises(ValueError, match="split drifted"):
        module.build_summary(
            full_fixture(),
            partial_fixture(),
            weighted,
            {"tests": 1, "failures": 0, "errors": 0, "skipped": 0},
        )
