"""Opt-in JiTCDDE external-library probe for the fixed PDMAL-GR fixture.

NON-ADMITTED: Author-built adapter to a maintained DDE library, not a
non-author independent reproduction, pilot, comparison runner or efficacy
experiment. No dependency installation, implicit code execution or lock edits.

Optional usage after manual local installation of JiTCDDE:
  python -m tools.pdmal.jitcdde_reference_probe
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from importlib.metadata import version
from pathlib import Path

from tools.pdmal.delay_sandbox import simulate_delayed_kuramoto
from tools.pdmal.scipy_reference_probe import (
    COUPLING,
    DELAYS,
    FREQUENCIES,
    GRAPH,
    GRID,
    HORIZON,
    INITIAL,
)

FIXED_BOOTSTRAP_STEP = 0.001
ADAPTIVE_MAX_STEP = 0.01
EXPECTED_FIXTURE_SHA256 = "9c54d2a437593ff226e19f8e6a655bf692af37fdcb0c77f12740598734bd1d15"


def fixture_manifest() -> dict[str, object]:
    """Machine-readable fixed inputs. Directed delays are (receiver,sender)."""
    return {
        "schema": "pdmal-gr-jitcdde-fixture-v1",
        "graph": [list(pair) for pair in GRAPH],
        "initial_phases": list(INITIAL),
        "frequencies": list(FREQUENCIES),
        "directed_physical_delays": [[i, j, v] for (i, j), v in sorted(DELAYS.items())],
        "coupling": COUPLING,
        "horizon_s": HORIZON,
        "sample_grid_s": GRID,
        "bootstrap_step_s": FIXED_BOOTSTRAP_STEP,
        "adaptive_max_step_s": ADAPTIVE_MAX_STEP,
        "history": "constant phase vector for all t <= 0",
    }


def fixture_sha256() -> str:
    """Digest of a canonical physical fixture, distinct from the source code."""
    manifest = fixture_manifest()
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_fixture() -> int:
    """Reject accidental changes to this narrow, reproducible DDE fixture."""
    if len(INITIAL) != len(FREQUENCIES) or len(INITIAL) != 4:
        raise ValueError("reference fixture must have exactly four oscillator states")
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in (*INITIAL, *FREQUENCIES)):
        raise ValueError("reference phases and frequencies must be finite real scalars")
    if type(COUPLING) not in (int, float) or not math.isfinite(COUPLING) or COUPLING <= 0:
        raise ValueError("reference coupling must be finite and positive")
    if type(GRID) not in (int, float) or not math.isfinite(GRID) or GRID <= 0:
        raise ValueError("reference observation grid must be finite and positive")
    if type(HORIZON) not in (int, float) or not math.isfinite(HORIZON) or HORIZON <= GRID:
        raise ValueError("reference horizon must exceed grid")
    if type(FIXED_BOOTSTRAP_STEP) not in (int, float) or not math.isfinite(FIXED_BOOTSTRAP_STEP):
        raise ValueError("reference bootstrap step must be finite")
    if FIXED_BOOTSTRAP_STEP <= 0 or FIXED_BOOTSTRAP_STEP > GRID:
        raise ValueError("reference bootstrap step must be positive and no larger than grid")
    if type(ADAPTIVE_MAX_STEP) not in (int, float) or not math.isfinite(ADAPTIVE_MAX_STEP):
        raise ValueError("reference adaptive maximum step must be finite")
    if ADAPTIVE_MAX_STEP <= 0 or ADAPTIVE_MAX_STEP > GRID:
        raise ValueError("reference adaptive maximum step must be positive and no larger than grid")
    edge_set: set[tuple[int, int]] = set()
    for u, v in GRAPH:
        if type(u) is not int or type(v) is not int or u == v:
            raise ValueError("invalid reference graph")
        edge_set.add((min(u, v), max(u, v)))
    if len(edge_set) != len(GRAPH) or any(not 0 <= vertex < 4 for edge in edge_set for vertex in edge):
        raise ValueError("reference graph must be a simple four-node labeled graph")
    for key, delay in DELAYS.items():
        i, j = key
        if (min(i, j), max(i, j)) not in edge_set or type(delay) not in (float, int) or delay <= 0:
            raise ValueError("reference directed delay not on an edge or nonpositive")
        if not math.isclose(delay / GRID, round(delay / GRID), rel_tol=0, abs_tol=1e-9):
            raise ValueError("reference delay not aligned with grid")
    if not math.isclose(HORIZON / GRID, round(HORIZON / GRID), rel_tol=0, abs_tol=1e-9):
        raise ValueError("reference horizon does not align with grid")
    if not math.isclose(GRID / FIXED_BOOTSTRAP_STEP, round(GRID / FIXED_BOOTSTRAP_STEP), rel_tol=0, abs_tol=1e-9):
        raise ValueError("bootstrap step must divide the observation grid")
    if not math.isclose(max(DELAYS.values()) / GRID, round(max(DELAYS.values()) / GRID), rel_tol=0, abs_tol=1e-9):
        raise ValueError("bootstrap transition must occur on the observation grid")
    if fixture_sha256() != EXPECTED_FIXTURE_SHA256:
        raise ValueError("reference fixture identity changed; requires independent review and version bump")
    return round(HORIZON / GRID)


def build_symbolic_rhs(y, t, sin) -> list:
    """Pure expression builder: explicitly preserve directed sender/receiver keys."""
    neighbors: list[list[int]] = [[] for _ in INITIAL]
    for u, v in GRAPH:
        neighbors[u].append(v)
        neighbors[v].append(u)
    return [
        FREQUENCIES[i]
        + COUPLING
        / len(neighbors[i])
        * sum(sin((y(j, t - DELAYS[(i, j)]) if (i, j) in DELAYS else y(j)) - y(i)) for j in neighbors[i])
        for i in range(len(INITIAL))
    ]


def collect_reference_trajectory(solver, n_samples: int) -> tuple[tuple[float, ...], ...]:
    """Exercise the requested time grid without needing an installed solver.

    The caller supplies a compatible JiTCDDE object; tests use a fake one.
    Successful scheduling is not evidence of correct DDE integration.
    """
    if type(n_samples) is not int or n_samples < 1:
        raise ValueError("n_samples must be a positive integer")
    bootstrap_end = max(DELAYS.values())
    trace: list[tuple[float, ...]] = [INITIAL]
    for index in range(1, n_samples + 1):
        requested = round(index * GRID, 12)
        if requested <= bootstrap_end + 1e-12:
            state = solver.integrate_blindly(requested, step=FIXED_BOOTSTRAP_STEP)
        else:
            state = solver.integrate(requested)
        values = tuple(float(value) for value in state)
        if len(values) != len(INITIAL) or any(not math.isfinite(value) for value in values):
            raise ArithmeticError("JiTCDDE returned a nonfinite or invalid-dimension state")
        trace.append(values)
    return tuple(trace)


def run_probe() -> dict[str, object]:
    """Build a local JiTCDDE receipt. Never claim independent author review."""
    n_samples = validate_fixture()
    try:
        from jitcdde import jitcdde, t, y
        from symengine import sin
    except ImportError as exc:
        raise RuntimeError(
            "JiTCDDE and SymEngine are optional and unavailable; "
            "install them separately in an authorized no-cost environment"
        ) from exc

    solver = jitcdde(build_symbolic_rhs(y, t, sin), n=len(INITIAL), verbose=False)
    solver.set_integration_parameters(atol=1e-12, rtol=1e-10, first_step=0.001, max_step=ADAPTIVE_MAX_STEP)
    solver.constant_past(INITIAL, time=0.0)

    # Preserve every early sample; blind bootstrap resolution is unvalidated.
    trace = collect_reference_trajectory(solver, n_samples)

    reference_lags = {key: round(lag / GRID) for key, lag in DELAYS.items()}
    sandbox = simulate_delayed_kuramoto(
        GRAPH,
        INITIAL,
        FREQUENCIES,
        delays=reference_lags,
        coupling=COUPLING,
        dt=GRID,
        steps=n_samples,
    )
    per_time_errors = [
        max(abs(value - expected) for value, expected in zip(state, sandbox[index]))
        for index, state in enumerate(trace)
    ]
    manifest = fixture_manifest()
    root = Path(__file__).parent
    receipt = {
        "status": "AUTHOR_OPERATED_OPTIONAL_EXTERNAL_DDE_LIBRARY_PROBE",
        "admission": "NON_ADMITTED_NOT_NON_AUTHOR_INDEPENDENT_VALIDATION",
        "source_git_head": "RECORD_SEPARATELY_FROM_GITHUB",
        "python_version": sys.version.split()[0],
        "jitcdde_version": version("jitcdde"),
        "symengine_version": version("symengine"),
        "fixture": manifest,
        "fixture_sha256": fixture_sha256(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sandbox_sha256": hashlib.sha256((root / "delay_sandbox.py").read_bytes()).hexdigest(),
        "comparison_max_phase_error_rad": max(per_time_errors),
        "comparison_terminal_phase_error_rad": per_time_errors[-1],
        "comparison_grid_errors_rad": per_time_errors,
        "dde_trajectory_unwrapped_rad": trace,
        "discontinuity_policy": "blind fixed-step integration through maximum lag; adaptive thereafter",
        "limitations": [
            "blind bootstrap may introduce discretization errors near initial discontinuities",
            "optional JiTCDDE library has not been verified by a non-author",
            "single directed-delay fixture cannot validate global DDE accuracy or topology claims",
        ],
        "scientific_n_increment": 0,
        "pilot_authorization": "NOT_GRANTED",
        "independent_validation": "NOT_ESTABLISHED",
    }
    return receipt


def main() -> None:
    print(json.dumps(run_probe(), indent=2))


if __name__ == "__main__":
    main()
