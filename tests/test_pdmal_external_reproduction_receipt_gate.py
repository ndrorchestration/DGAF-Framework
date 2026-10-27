"""Negative/positive structural contracts; never independent DDE validation."""

import copy
import json
from pathlib import Path

from tools.pdmal.external_reproduction_receipt_gate import (
    EXPECTED_HASH,
    assess_submission,
    fixture_digest,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "docs/experiment/PDMAL_DDE_EXTERNAL_REPLICATION_FIXTURE_V1.json").read_text())
TEMPLATE = json.loads((ROOT / "docs/experiment/PDMAL_DDE_NONAUTHOR_RETURN_TEMPLATE_V1.json").read_text())


def submission():
    """Synthetic complete-shaped receipt, explicitly NOT a real reviewer result."""
    result = copy.deepcopy(TEMPLATE)
    result.update(
        {
            "submission_state": "SUBMITTED_FOR_EXTERNAL_REVIEW",
            "reviewer_id": "synthetic-test-only",
            "non_author_declaration": "fixture test, not an external person",
            "reviewer_source_repository_or_archive": "synthetic-fixture-only",
            "reviewer_source_commit_or_sha256": "synthetic-no-source",
            "implementation_authored_independently_of_dgaf_solver": True,
            "physical_input_parity_confirmed": True,
            "runtime_and_os": "synthetic-test-only",
            "external_dde_package_and_version": "synthetic-test-only",
            "dependency_manifest_and_hash": "synthetic-test-only",
            "numerical_solver_parameters": "synthetic-test-only",
            "history_and_discontinuity_method": "synthetic-test-only",
            "author_comparison_performed_after_independent_run_freeze": True,
            "early_derivative_and_junction_checks": {},
            "timestep_tolerance_refinement": {},
            "raw_errors_and_negative_cases": {},
            "conclusion": "INDETERMINATE",
        }
    )
    result["observations"].update(
        {
            "timestamps_s": [round(i * 0.02, 10) for i in range(41)],
            "unwrapped_phases_rad": [list(FIXTURE["initial_phases"]) for _ in range(41)],
            "missing_timepoints_s": [],
            "missing_timepoint_reasons": {},
        }
    )
    result["per_time_signed_phase_residuals_rad"] = [[0.0] * 4 for _ in range(41)]
    result["per_time_max_abs_phase_residuals_rad"] = [0.0] * 41
    return result


def assess(data, fixture=FIXTURE):
    return assess_submission(data, fixture)


def test_frozen_fixture_digest():
    assert fixture_digest(FIXTURE) == EXPECTED_HASH


def test_unsubmitted_template_fails_closed():
    result = assess(TEMPLATE)
    assert result["status"] == "REJECTED_OR_INCOMPLETE"
    assert "NOT_AN_ACTUAL_SUBMISSION" in result["errors"]


def test_synthetic_complete_structure_not_certified():
    result = assess(submission())
    assert result["status"] == "STRUCTURAL_REVIEW_READY"
    assert result["numerical_accuracy"] == "NOT_CERTIFIED"
    assert result["external_independence"] == "DECLARATION_NOT_VERIFIED"
    assert result["scientific_n_increment"] == 0


def test_tampered_fixture_rejected():
    modified = copy.deepcopy(FIXTURE)
    modified["coupling"] = 2.0
    assert "FROZEN_FIXTURE_DIGEST_MISMATCH" in assess(submission(), modified)["errors"]


def test_governance_escalation_rejected():
    data = submission()
    data["pilot_authorization"] = "GRANTED"
    assert "GOVERNANCE_BOUNDARY_PILOT_AUTHORIZATION" in assess(data)["errors"]


def test_truncated_samples_not_full_grid():
    data = submission()
    data["observations"]["timestamps_s"].pop()
    data["observations"]["unwrapped_phases_rad"].pop()
    data["per_time_signed_phase_residuals_rad"].pop()
    data["per_time_max_abs_phase_residuals_rad"].pop()
    assert "GRID_COVERAGE_LEDGER_INCOMPLETE" in assess(data)["errors"]


def test_missing_early_sample_with_ledger_is_partial():
    data = submission()
    data["observations"]["timestamps_s"].pop(1)
    data["observations"]["unwrapped_phases_rad"].pop(1)
    data["observations"]["missing_timepoints_s"] = [0.02]
    data["observations"]["missing_timepoint_reasons"] = {"0.02": "solver advanced"}
    data["per_time_signed_phase_residuals_rad"].pop(1)
    data["per_time_max_abs_phase_residuals_rad"].pop(1)
    outcome = assess(data)
    assert outcome["status"] == "STRUCTURAL_REVIEW_READY"
    assert outcome["full_grid"] is False
    assert outcome["numerical_accuracy"] == "NOT_CERTIFIED"


def test_nan_phase_rejected():
    data = submission()
    data["observations"]["unwrapped_phases_rad"][3][2] = float("nan")
    assert "NONFINITE_PHASE" in assess(data)["errors"]


def test_wrong_initial_state_rejected():
    data = submission()
    data["observations"]["unwrapped_phases_rad"][0][0] += 0.1
    assert "INITIAL_PHASE_MISMATCH" in assess(data)["errors"]


def test_residual_mismatch_rejected():
    data = submission()
    data["per_time_signed_phase_residuals_rad"][2][1] = 0.5
    assert "RESIDUAL_INTERNAL_INCONSISTENCY" in assess(data)["errors"]


def test_nonfinite_timestamp_rejected():
    data = submission()
    data["observations"]["timestamps_s"][2] = float("inf")
    assert "TIMESTAMP_LEDGER_MISSING_OR_INVALID" in assess(data)["errors"]


def test_truthy_int_is_not_boolean_authorization():
    data = submission()
    data["scientific_n_increment"] = False
    assert "GOVERNANCE_BOUNDARY_SCIENTIFIC_N_INCREMENT" in assess(data)["errors"]


def test_shuffled_full_grid_rejected():
    data = submission()
    times = data["observations"]["timestamps_s"]
    traces = data["observations"]["unwrapped_phases_rad"]
    times[1], times[2] = times[2], times[1]
    traces[1], traces[2] = traces[2], traces[1]
    assert "TIMESTAMP_ORDER_INVALID" in assess(data)["errors"]


def test_shuffled_missing_ledger_rejected():
    data = submission()
    for index in (1, 2):
        data["observations"]["timestamps_s"].pop(1)
        data["observations"]["unwrapped_phases_rad"].pop(1)
        data["per_time_signed_phase_residuals_rad"].pop(1)
        data["per_time_max_abs_phase_residuals_rad"].pop(1)
    data["observations"]["missing_timepoints_s"] = [0.04, 0.02]
    data["observations"]["missing_timepoint_reasons"] = {"0.02": "missing", "0.04": "missing"}
    assert "TIMESTAMP_ORDER_INVALID" in assess(data)["errors"]
