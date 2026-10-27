"""Fail-closed numerical *evidence audit* for the four-node JiTCDDE fixture.

Same-author software custody, not an independent solver or pilot. Execution
success must never be confused with a validated numerical error tolerance.
Run with two local receipts:
  python -m tools.pdmal.early_window_receipt_audit nominal.json sensitivity.json

No SciPy, JiTCDDE, optional installs, topology comparisons, or network access.
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Mapping
from pathlib import Path

from tools.pdmal.early_window_oracle import initial_window_trajectory
from tools.pdmal.jitcdde_reference_probe import EXPECTED_FIXTURE_SHA256, GRID, INITIAL


def _phase_trace(data: object, name: str) -> tuple[tuple[float, ...], ...]:
    """Reject truncated, nonfinite, shifted, or malformed numerical trajectories."""
    if not isinstance(data, list) or len(data) != 41:
        raise ValueError(f"{name} must contain exactly 41 sampled states")
    states: list[tuple[float, ...]] = []
    for state in data:
        if not isinstance(state, (list, tuple)) or len(state) != len(INITIAL):
            raise ValueError(f"{name} has a wrong-dimension state")
        if any(type(value) not in (int, float) or not math.isfinite(value) for value in state):
            raise ValueError(f"{name} contains an invalid numerical value")
        states.append(tuple(float(value) for value in state))
    if max(abs(x - y) for x, y in zip(states[0], INITIAL)) > 1e-13:
        raise ValueError(f"{name} does not start from the fixed prescribed initial state")
    return tuple(states)


def _require_custody(payload: Mapping[str, object], name: str, *, nominal: bool) -> None:
    hash_field = "fixture_sha256" if nominal else "nominal_fixture_sha256"
    if payload.get(hash_field) != EXPECTED_FIXTURE_SHA256:
        raise ValueError(f"{name} fixture digest mismatch")
    if payload.get("scientific_n_increment") != 0:
        raise ValueError(f"{name} scientific N must remain zero")
    if payload.get("pilot_authorization") != "NOT_GRANTED":
        raise ValueError(f"{name} pilot is not authorized")
    if payload.get("independent_validation") != "NOT_ESTABLISHED":
        raise ValueError(f"{name} independent validation must not be asserted")


def audit_receipts(nominal: Mapping[str, object], sensitivity: Mapping[str, object]) -> dict[str, object]:
    """Audit numerical custody, full traces, and two first-window grid samples.

    No error threshold is set: these are measured residuals, not certification.
    """
    _require_custody(nominal, "nominal", nominal=True)
    _require_custody(sensitivity, "sensitivity", nominal=False)
    nominal_trace = _phase_trace(nominal.get("dde_trajectory_unwrapped_rad"), "nominal")
    variants = sensitivity.get("variants")
    if not isinstance(variants, list) or len(variants) != 3:
        raise ValueError("exactly three ordered bootstrap variants are required")
    expected_steps = (0.001, 0.0005, 0.00025)
    oracle = initial_window_trajectory(0.000625)
    assert len(oracle) == 65
    records: list[dict[str, object]] = []
    for variant, expected_step in zip(variants, expected_steps):
        if not isinstance(variant, dict) or type(variant.get("bootstrap_step_s")) not in (int, float):
            raise ValueError("bootstrap step is missing or invalid")
        if not math.isclose(variant["bootstrap_step_s"], expected_step, rel_tol=0, abs_tol=1e-14):
            raise ValueError("bootstrap sequence or declared step size changed")
        trace = _phase_trace(variant.get("complete_trajectory"), f"step={expected_step}")
        observed: dict[str, float] = {}
        for grid_index in (1, 2):
            oracle_index = round(grid_index * GRID / 0.000625)
            discrepancy = max(abs(a - b) for a, b in zip(trace[grid_index], oracle[oracle_index]))
            observed[f"t_{grid_index * GRID:.2f}_max_abs_phase_residual_rad"] = discrepancy
        records.append({"bootstrap_step_s": expected_step, **observed})
    if max(abs(x - y) for left, right in zip(nominal_trace, _phase_trace(variants[0]["complete_trajectory"], "first variant")) for x, y in zip(left, right)) > 1e-10:
        raise ValueError("nominal and first sensitivity trajectories disagree")
    t02 = [float(r["t_0.02_max_abs_phase_residual_rad"]) for r in records]
    t04 = [float(r["t_0.04_max_abs_phase_residual_rad"]) for r in records]
    return {
        "status": "EXECUTION_RECEIPT_AUDITED_NUMERICAL_ACCURACY_NOT_CERTIFIED",
        "disposition": "OBSERVED_EARLY_STARTUP_DISCREPANCY_REQUIRES_INDEPENDENT_REVIEW",
        "fixture_sha256": EXPECTED_FIXTURE_SHA256,
        "early_interval_end_s": 0.04,
        "model": "same-author analytic constant-history first-window ODE; not independent DDE solver",
        "first_window_residuals": records,
        "t_0p02_residual_halving_ratios": [t02[i] / t02[i + 1] for i in range(2)],
        "t_0p04_residual_halving_ratios": [t04[i] / t04[i + 1] for i in range(2)],
        "limitations": [
            "no preregistered or independently validated solver-accuracy tolerance",
            "early-window ODE only valid for t<=0.04 seconds",
            "shared same-author DDE model definition; no non-author scientific validation",
            "no comparative topology trials, pilot sample or DGAF efficacy result",
        ],
        "scientific_n_increment": 0,
        "pilot_authorization": "NOT_GRANTED",
        "independent_validation": "NOT_ESTABLISHED",
    }


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: python -m tools.pdmal.early_window_receipt_audit NOMINAL.json SENSITIVITY.json")
    nominal = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    sensitivity = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    print(json.dumps(audit_receipts(nominal, sensitivity), indent=2))


if __name__ == "__main__":
    main()
