"""Structural review of non-author DDE submissions; never numerical certification.

No external solver invocation, scientific-N change, authorization, or remote I/O.
This audits custody and shape, not the truth of independence declarations.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections.abc import Mapping
from pathlib import Path

EXPECTED_HASH = "9c54d2a437593ff226e19f8e6a655bf692af37fdcb0c77f12740598734bd1d15"
CLOSED = {
    "admission": "NON_ADMITTED_DDE_SOFTWARE_REPRODUCTION_ONLY",
    "scientific_n_increment": 0,
    "pilot_authorization": "NOT_GRANTED",
    "independent_validation": "NOT_ESTABLISHED",
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    "dgaf_v1_release": "HOLD",
}
CONCLUSIONS = {
    "REPRODUCED",
    "PARTIALLY REPRODUCED",
    "NOT REPRODUCED",
    "INDETERMINATE",
}


def _real_number(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def fixture_digest(fixture: Mapping[str, object]) -> str:
    """Canonical hash of the entire frozen author input, including solver defaults."""
    encoded = json.dumps(fixture, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def assess_submission(submission: Mapping[str, object], fixture: Mapping[str, object]) -> dict[str, object]:
    """Fail closed on missing/contradictory custody; report gaps without certifying."""
    errors: list[str] = []
    if fixture_digest(fixture) != EXPECTED_HASH:
        errors.append("FROZEN_FIXTURE_DIGEST_MISMATCH")
    if submission.get("canonical_fixture_sha256") != EXPECTED_HASH:
        errors.append("SUBMITTED_FIXTURE_DIGEST_MISMATCH")
    if submission.get("submission_state") != "SUBMITTED_FOR_EXTERNAL_REVIEW":
        errors.append("NOT_AN_ACTUAL_SUBMISSION")
    for key, value in CLOSED.items():
        if type(value) is int:
            valid = type(submission.get(key)) is int and submission[key] == value
        else:
            valid = submission.get(key) == value
        if not valid:
            errors.append("GOVERNANCE_BOUNDARY_" + key.upper())

    required_text = (
        "reviewer_id",
        "non_author_declaration",
        "reviewer_source_repository_or_archive",
        "reviewer_source_commit_or_sha256",
        "runtime_and_os",
        "external_dde_package_and_version",
        "dependency_manifest_and_hash",
        "numerical_solver_parameters",
        "history_and_discontinuity_method",
    )
    for field in required_text:
        if not _text(submission.get(field)):
            errors.append("MISSING_PROVENANCE_" + field.upper())
    for field in (
        "implementation_authored_independently_of_dgaf_solver",
        "physical_input_parity_confirmed",
        "author_comparison_performed_after_independent_run_freeze",
    ):
        if submission.get(field) is not True:
            errors.append("UNVERIFIED_DECLARATION_" + field.upper())

    obs = submission.get("observations")
    if not isinstance(obs, dict):
        obs = {}
        errors.append("OBSERVATIONS_MISSING")
    grid = [round(0.02 * i, 10) for i in range(41)]
    times = obs.get("timestamps_s")
    traces = obs.get("unwrapped_phases_rad")
    missing = obs.get("missing_timepoints_s")
    reasons = obs.get("missing_timepoint_reasons")
    if obs.get("expected_sample_count") != 41 or obs.get("expected_phase_dimension") != 4:
        errors.append("OBSERVATION_SCHEMA_MISMATCH")
    valid_times = isinstance(times, list) and all(_real_number(t) for t in times)
    valid_missing = isinstance(missing, list) and all(_real_number(t) for t in missing)
    if not valid_times or not valid_missing:
        errors.append("TIMESTAMP_LEDGER_MISSING_OR_INVALID")
        times, missing = [], []
    if len(times) != len(set(times)) or len(missing) != len(set(missing)):
        errors.append("DUPLICATE_TIMESTAMPS")
    if any(t not in grid for t in times + missing):
        errors.append("TIMESTAMP_OUTSIDE_GRID")
    if set(times) & set(missing) or set(times) | set(missing) != set(grid):
        errors.append("GRID_COVERAGE_LEDGER_INCOMPLETE")
    if not isinstance(traces, list) or len(traces) != len(times):
        errors.append("TRACE_LENGTH_MISMATCH")
    else:
        for state in traces:
            if not isinstance(state, list) or len(state) != 4:
                errors.append("PHASE_DIMENSION_MISMATCH")
                break
            if not all(_real_number(x) for x in state):
                errors.append("NONFINITE_PHASE")
                break
        if times and times[0] == 0 and traces and isinstance(traces[0], list):
            if len(traces[0]) == 4 and all(_real_number(x) for x in traces[0]):
                if max(abs(a - b) for a, b in zip(traces[0], fixture["initial_phases"])) > 1e-12:
                    errors.append("INITIAL_PHASE_MISMATCH")
    if missing and (not isinstance(reasons, dict) or any(not _text(reasons.get(str(t))) for t in missing)):
        errors.append("MISSING_SAMPLE_REASONS")
    if submission.get("conclusion") not in CONCLUSIONS:
        errors.append("CONCLUSION_UNSPECIFIED")
    for field in (
        "early_derivative_and_junction_checks",
        "timestep_tolerance_refinement",
        "raw_errors_and_negative_cases",
    ):
        if submission.get(field) is None:
            errors.append("MISSING_ANALYSIS_" + field.upper())
    signed = submission.get("per_time_signed_phase_residuals_rad")
    absolute = submission.get("per_time_max_abs_phase_residuals_rad")
    if not isinstance(signed, list) or len(signed) != len(times):
        errors.append("SIGNED_RESIDUAL_LEDGER_MISSING")
    elif any(not isinstance(row, list) or len(row) != 4 or not all(_real_number(x) for x in row) for row in signed):
        errors.append("SIGNED_RESIDUAL_VALUES_INVALID")
    if not isinstance(absolute, list) or len(absolute) != len(times):
        errors.append("ABS_RESIDUAL_LEDGER_MISSING")
    elif any(not _real_number(v) or v < 0 for v in absolute):
        errors.append("ABS_RESIDUAL_VALUES_INVALID")
    elif (
        isinstance(signed, list)
        and len(signed) == len(times)
        and all(isinstance(row, list) and len(row) == 4 and all(_real_number(x) for x in row) for row in signed)
    ):
        if any(abs(max(abs(x) for x in row) - value) > 1e-9 for row, value in zip(signed, absolute)):
            errors.append("RESIDUAL_INTERNAL_INCONSISTENCY")
    return {
        "status": "STRUCTURAL_REVIEW_READY" if not errors else "REJECTED_OR_INCOMPLETE",
        "errors": sorted(set(errors)),
        "covered_timepoints": len(times),
        "missing_timepoints": len(missing),
        "full_grid": not errors and len(times) == 41,
        "numerical_accuracy": "NOT_CERTIFIED",
        "external_independence": "DECLARATION_NOT_VERIFIED",
        "scientific_n_increment": 0,
        "pilot_authorization": "NOT_GRANTED",
        "independent_validation": "NOT_ESTABLISHED",
    }


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: python -m tools.pdmal.external_reproduction_receipt_gate " "FIXTURE.json REVIEWER_SUBMISSION.json"
        )
    fixture = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    submission = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    result = assess_submission(submission, fixture)
    print(json.dumps(result, indent=2))
    if result["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
