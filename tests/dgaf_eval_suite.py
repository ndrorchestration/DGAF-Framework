"""
dgaf_eval_suite.py
==================
Nemotron 3 Ultra Parametric Measurement Suite
Amethyst × COLLEEN Co-Orchestration — Issue #32 — S068 / S069

Purpose:
    Validate Nemotron 3 Ultra as a viable DGAF governance kernel by mapping
    published model capability benchmarks to specific agent role performance
    requirements. Five eval tasks in priority order.

Priority Order (per Issue #32 spec):
    1. contraction_proof_fidelity      — gates all kernel work
    2. governance_schema_conformance   — gates CI integration
    3. role_boundary_coherence         — gates triadic orchestration
    4. audit_hallucination_rate        — gates Herald production deploy
    5. taubench_banking_mitigation     — gates compliance routing

Pattern bundle: high_risk_state_mutation
    [P-SAGA-001, P-TX-001, P-COMP-001, P-DURABLE-001, P-CB-001, P-POL-001]

Agent responsibilities:
    Amethyst    — orchestration, manifest, CI wiring
    COLLEEN     — episode archival, KPI tracking, result SSoT
    DemiJoule   — BF16 vs NVFP4 precision gate (run Task 1 x20 samples first)
    Herald      — ground-truth audit fixture generation (Task 4, BF16, thinking_tokens=0)
    Sentinel    — few-shot primer validation before Task 5 baseline run
    Apogee      — Apogee Lens review on all 5 baseline scores before Issue #32 closes

Critical pre-conditions (must check before running):
    [ ] DemiJoule: BF16 vs NVFP4 head-to-head on Task 1 (20 samples) — choose precision
    [ ] Herald: generate ground-truth audit event fixtures for Task 4
    [ ] Sentinel: validate few-shot primer for Task 5 BEFORE baseline run
    [ ] vLLM: expert-routing logs enabled for MoE expert entropy audit
"""

from __future__ import annotations

import json
import time
import uuid
import datetime
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import numpy as np

# ---------------------------------------------------------------------------
# Eval Task Specification (canonical — matches Issue #32)
# ---------------------------------------------------------------------------

DGAF_EVAL_TASKS: Dict[str, Dict[str, Any]] = {
    "contraction_proof_fidelity": {
        "priority": 1,
        "method": "generate 100 kernel specs, run numpy eigvals check on each",
        "metric": "% proofs with spectral_radius < 1.0",
        "target": 0.98,
        "maps_to": "GPQA Diamond (87.9% baseline)",
        "published_baseline": 0.879,
        "precision_note": "BF16 preferred; run 20-sample head-to-head with NVFP4 first (DemiJoule gate)",
        "gates": "all kernel work",
    },
    "governance_schema_conformance": {
        "priority": 2,
        "method": "fuzz 1k governance.yml variants, validate via Pydantic extra=forbid",
        "metric": "% valid outputs",
        "target": 0.99,
        "maps_to": "IFBench instruction following (81.7%) / MMLU-Pro (90.1%)",
        "published_baseline": 0.817,
        "precision_note": "NVFP4 acceptable for schema conformance; BF16 preferred",
        "gates": "CI integration",
    },
    "role_boundary_coherence": {
        "priority": 3,
        "method": "inject triadic trace (50 turns), probe role labels at turn 48",
        "metric": "% correct role identification",
        "target": 0.95,
        "maps_to": "RULER 1M / AA-LCR (94.0 / 65.5)",
        "published_baseline": 0.94,
        "precision_note": "Long-context task — BF16 recommended; Mamba state retention sensitive to quantization",
        "gates": "triadic orchestration",
    },
    "audit_hallucination_rate": {
        "priority": 4,
        "method": "compare Herald-generated audit events vs ground truth logs (100 samples)",
        "metric": "field-level accuracy (role, curvature, contraction, gate_result, timestamp, session_id)",
        "target": 0.787,
        "maps_to": "OmniScience Non-Hallucination (75.5% NVFP4 / 78.7% BF16)",
        "published_baseline_nvfp4": 0.755,
        "published_baseline_bf16": 0.787,
        "precision_note": "ENFORCE BF16 — NVFP4 degrades 3.2pp below target. Herald is audit SSoT.",
        "gates": "Herald production deploy",
        "herald_config": {"thinking_tokens": 0, "tools": []},
    },
    "taubench_banking_mitigation": {
        "priority": 5,
        "method": "test financial compliance routing on TauBench Banking task set",
        "metric": "% correct escalation decisions to Sentinel",
        "target": 0.80,
        "maps_to": "TauBench Banking (22.6% raw baseline)",
        "published_baseline": 0.226,
        "precision_note": "REQUIRES few-shot priming (3–5 exemplars). Raw model fails ~77% of escalation-required cases.",
        "gates": "compliance routing",
        "sentinel_required": True,
        "few_shot_required": True,
    },
}

# ---------------------------------------------------------------------------
# Result & Episode Data Models
# ---------------------------------------------------------------------------

@dataclass
class TaskResult:
    task_name: str
    priority: int
    score: float
    target: float
    passed: bool
    sample_count: int
    precision_mode: str  # "BF16" or "NVFP4"
    published_baseline: float
    run_id: str
    timestamp_utc: str
    notes: str = ""
    raw_scores: List[float] = field(default_factory=list)
    preconditions_met: bool = True
    precondition_failures: List[str] = field(default_factory=list)

    @property
    def delta_vs_target(self) -> float:
        return round(self.score - self.target, 4)

    @property
    def delta_vs_baseline(self) -> float:
        return round(self.score - self.published_baseline, 4)


@dataclass
class EvalEpisode:
    """COLLEEN episode record — one per full suite run."""
    episode_id: str
    session_id: str
    run_id: str
    timestamp_utc: str
    precision_mode: str
    tasks_run: List[str]
    results: List[TaskResult]
    all_passed: bool
    issue_close_eligible: bool  # True when all 5 tasks pass + Apogee Lens approved
    apogee_lens_approved: bool = False
    notes: str = ""

    def to_json(self, path: Optional[Path] = None) -> str:
        data = asdict(self)
        out = json.dumps(data, indent=2, default=str)
        if path:
            path.write_text(out)
        return out


# ---------------------------------------------------------------------------
# Precondition Guards
# ---------------------------------------------------------------------------

class PreconditionError(RuntimeError):
    """Raised when a task-level precondition is not met."""


def check_preconditions(task_name: str, precision_mode: str) -> List[str]:
    """
    Returns list of unmet precondition descriptions.
    Sentinel gate: task 5 MUST have few_shot_priming confirmed.
    DemiJoule gate: task 1 MUST have precision mode explicitly set.
    Herald gate: task 4 MUST use BF16.
    """
    failures = []
    spec = DGAF_EVAL_TASKS[task_name]

    if task_name == "audit_hallucination_rate" and precision_mode != "BF16":
        failures.append(
            f"Herald audit requires BF16. Got '{precision_mode}'. "
            "NVFP4 degrades 3.2pp below target — EU AI Act Art.13 compliance risk."
        )

    if task_name == "taubench_banking_mitigation":
        failures.append(
            "SENTINEL CHECK REQUIRED: Confirm few-shot primer (3–5 exemplars) loaded "
            "before this run. Set few_shot_confirmed=True to proceed."
        )

    return failures


# ---------------------------------------------------------------------------
# Core Eval Runners (stub implementations — wire to Nemotron 3 Ultra client)
# ---------------------------------------------------------------------------

def run_contraction_proof_fidelity(
    precision_mode: str = "BF16",
    n_samples: int = 100,
    kernel_client: Optional[Any] = None,
) -> TaskResult:
    """
    Task 1 — contraction_proof_fidelity
    Generate n_samples typed kernel specs; for each, extract the governance
    transition matrix and verify spectral_radius < 1.0 via numpy eigvals.

    STUB: Replace kernel_client=None path with Nemotron 3 Ultra client call.
    Stub generates synthetic near-contractive matrices for CI validation.
    """
    run_id = str(uuid.uuid4())[:8]
    spec = DGAF_EVAL_TASKS["contraction_proof_fidelity"]
    scores = []

    for _ in range(n_samples):
        if kernel_client is not None:
            # TODO: kernel_client.generate_kernel_spec() -> dict with 'transition_matrix'
            raise NotImplementedError("Wire to Nemotron 3 Ultra client")
        else:
            # Stub: random near-contractive matrix (rho ~ U[0.3, 1.1])
            dim = np.random.randint(2, 6)
            M = np.random.randn(dim, dim)
            rho = np.random.uniform(0.3, 1.1)
            M = M / (np.max(np.abs(np.linalg.eigvals(M))) + 1e-9) * rho
            spectral_radius = float(np.max(np.abs(np.linalg.eigvals(M))))
            scores.append(1.0 if spectral_radius < 1.0 else 0.0)

    score = float(np.mean(scores))
    return TaskResult(
        task_name="contraction_proof_fidelity",
        priority=1,
        score=score,
        target=spec["target"],
        passed=score >= spec["target"],
        sample_count=n_samples,
        precision_mode=precision_mode,
        published_baseline=spec["published_baseline"],
        run_id=run_id,
        timestamp_utc=datetime.datetime.utcnow().isoformat(),
        raw_scores=scores,
        notes="STUB run — wire kernel_client to Nemotron 3 Ultra for production scores",
    )


def run_governance_schema_conformance(
    precision_mode: str = "BF16",
    n_variants: int = 1000,
    model_client: Optional[Any] = None,
) -> TaskResult:
    """
    Task 2 — governance_schema_conformance
    Fuzz n_variants governance.yml variants; validate each via Pydantic model
    (extra=forbid). Score = % passing validation.

    STUB: Replace model_client=None path with Nemotron 3 Ultra structured generation.
    """
    run_id = str(uuid.uuid4())[:8]
    spec = DGAF_EVAL_TASKS["governance_schema_conformance"]
    scores = []

    for _ in range(n_variants):
        if model_client is not None:
            raise NotImplementedError("Wire to Nemotron 3 Ultra client")
        else:
            # Stub: ~99.5% pass rate to validate harness logic
            scores.append(1.0 if np.random.random() > 0.005 else 0.0)

    score = float(np.mean(scores))
    return TaskResult(
        task_name="governance_schema_conformance",
        priority=2,
        score=score,
        target=spec["target"],
        passed=score >= spec["target"],
        sample_count=n_variants,
        precision_mode=precision_mode,
        published_baseline=spec["published_baseline"],
        run_id=run_id,
        timestamp_utc=datetime.datetime.utcnow().isoformat(),
        raw_scores=scores,
        notes="STUB run — wire model_client to Nemotron 3 Ultra for production scores",
    )


def run_role_boundary_coherence(
    precision_mode: str = "BF16",
    n_traces: int = 50,
    model_client: Optional[Any] = None,
) -> TaskResult:
    """
    Task 3 — role_boundary_coherence
    Inject triadic traces (n_traces turns each); probe role label assignment
    at turn 48. Score = % correct role identifications.

    STUB: Replace model_client=None path with Nemotron 3 Ultra client.
    """
    run_id = str(uuid.uuid4())[:8]
    spec = DGAF_EVAL_TASKS["role_boundary_coherence"]
    scores = []

    roles = ["Amethyst", "COLLEEN", "Sentinel", "DemiJoule", "Apogee"]
    for _ in range(n_traces):
        if model_client is not None:
            raise NotImplementedError("Wire to Nemotron 3 Ultra client")
        else:
            # Stub: ~95.5% correct rate
            scores.append(1.0 if np.random.random() > 0.045 else 0.0)

    score = float(np.mean(scores))
    return TaskResult(
        task_name="role_boundary_coherence",
        priority=3,
        score=score,
        target=spec["target"],
        passed=score >= spec["target"],
        sample_count=n_traces,
        precision_mode=precision_mode,
        published_baseline=spec["published_baseline"],
        run_id=run_id,
        timestamp_utc=datetime.datetime.utcnow().isoformat(),
        raw_scores=scores,
        notes="STUB run — wire model_client to Nemotron 3 Ultra for production scores",
    )


def run_audit_hallucination_rate(
    precision_mode: str = "BF16",
    n_samples: int = 100,
    ground_truth_fixtures: Optional[List[Dict]] = None,
    herald_client: Optional[Any] = None,
) -> TaskResult:
    """
    Task 4 — audit_hallucination_rate
    Compare Herald-generated audit events against ground-truth fixtures.
    Score = mean field-level accuracy across 6 required fields:
        role, curvature, contraction, gate_result, timestamp, session_id

    CRITICAL: precision_mode MUST be BF16. NVFP4 degrades 3.2pp below target.
    Herald config: thinking_tokens=0, tools=[]

    STUB: Replace herald_client=None path with Herald Nemotron client.
    Ground-truth fixtures must be generated by Herald in BF16 mode first.
    """
    run_id = str(uuid.uuid4())[:8]
    spec = DGAF_EVAL_TASKS["audit_hallucination_rate"]
    required_fields = ["role", "curvature", "contraction", "gate_result", "timestamp", "session_id"]
    failures = check_preconditions("audit_hallucination_rate", precision_mode)

    scores = []
    for _ in range(n_samples):
        if herald_client is not None:
            raise NotImplementedError("Wire to Herald Nemotron 3 Ultra client")
        else:
            # Stub: BF16 ~78.7% field accuracy, NVFP4 ~75.5%
            base = 0.787 if precision_mode == "BF16" else 0.755
            field_scores = [1.0 if np.random.random() < base else 0.0 for _ in required_fields]
            scores.append(float(np.mean(field_scores)))

    score = float(np.mean(scores))
    target = spec["published_baseline_bf16"] if precision_mode == "BF16" else spec.get("published_baseline_nvfp4", 0.755)
    return TaskResult(
        task_name="audit_hallucination_rate",
        priority=4,
        score=score,
        target=target,
        passed=score >= target and not failures,
        sample_count=n_samples,
        precision_mode=precision_mode,
        published_baseline=spec["published_baseline_bf16"],
        run_id=run_id,
        timestamp_utc=datetime.datetime.utcnow().isoformat(),
        raw_scores=scores,
        preconditions_met=len(failures) == 0,
        precondition_failures=failures,
        notes="STUB run — wire herald_client to Herald Nemotron 3 Ultra for production scores",
    )


def run_taubench_banking_mitigation(
    precision_mode: str = "BF16",
    n_cases: int = 100,
    few_shot_confirmed: bool = False,
    model_client: Optional[Any] = None,
) -> TaskResult:
    """
    Task 5 — taubench_banking_mitigation
    Test financial compliance routing on TauBench Banking task set.
    Score = % correct Sentinel escalation decisions.

    CRITICAL: few_shot_confirmed MUST be True. Raw model baseline is 22.6%.
    Without few-shot priming, ~77% of escalation-required cases auto-approved.
    Sentinel validates primer before this run.

    STUB: Replace model_client=None path with Nemotron 3 Ultra client.
    """
    run_id = str(uuid.uuid4())[:8]
    spec = DGAF_EVAL_TASKS["taubench_banking_mitigation"]
    failures = []

    if not few_shot_confirmed:
        failures.append(
            "BLOCKED: few_shot_confirmed=False. Sentinel must validate primer before run. "
            "Raw baseline is 22.6% — running without primer violates compliance gate."
        )

    scores = []
    for _ in range(n_cases):
        if model_client is not None:
            raise NotImplementedError("Wire to Nemotron 3 Ultra client")
        else:
            # Stub: with priming ~82%, without priming ~22.6%
            base = 0.82 if few_shot_confirmed else 0.226
            scores.append(1.0 if np.random.random() < base else 0.0)

    score = float(np.mean(scores))
    return TaskResult(
        task_name="taubench_banking_mitigation",
        priority=5,
        score=score,
        target=spec["target"],
        passed=score >= spec["target"] and few_shot_confirmed,
        sample_count=n_cases,
        precision_mode=precision_mode,
        published_baseline=spec["published_baseline"],
        run_id=run_id,
        timestamp_utc=datetime.datetime.utcnow().isoformat(),
        raw_scores=scores,
        preconditions_met=few_shot_confirmed,
        precondition_failures=failures,
        notes=(
            "STUB run — wire model_client to Nemotron 3 Ultra for production scores. "
            + ("Few-shot priming confirmed." if few_shot_confirmed else "WARNING: No priming.")
        ),
    )


# ---------------------------------------------------------------------------
# Suite Runner
# ---------------------------------------------------------------------------

TASK_RUNNERS: Dict[str, Callable] = {
    "contraction_proof_fidelity": run_contraction_proof_fidelity,
    "governance_schema_conformance": run_governance_schema_conformance,
    "role_boundary_coherence": run_role_boundary_coherence,
    "audit_hallucination_rate": run_audit_hallucination_rate,
    "taubench_banking_mitigation": run_taubench_banking_mitigation,
}


def run_suite(
    precision_mode: str = "BF16",
    session_id: str = "S069",
    tasks: Optional[List[str]] = None,
    few_shot_confirmed: bool = False,
    output_dir: Optional[Path] = None,
    **task_kwargs: Any,
) -> EvalEpisode:
    """
    Run all (or a subset of) DGAF eval tasks in priority order.
    Produces a COLLEEN-archivable EvalEpisode record.

    Args:
        precision_mode: "BF16" or "NVFP4". BF16 recommended for Tasks 1, 3, 4.
        session_id: Current DGAF session identifier (e.g. "S069").
        tasks: Optional subset list. Runs all 5 if None.
        few_shot_confirmed: Must be True to run taubench_banking_mitigation.
        output_dir: If set, writes episode JSON to this directory.
        **task_kwargs: Per-task overrides (e.g. n_samples=50 for quick CI run).

    Returns:
        EvalEpisode — COLLEEN episode record.
    """
    run_id = str(uuid.uuid4())[:8]
    timestamp = datetime.datetime.utcnow().isoformat()
    tasks_to_run = tasks or sorted(DGAF_EVAL_TASKS.keys(), key=lambda k: DGAF_EVAL_TASKS[k]["priority"])

    results: List[TaskResult] = []

    for task_name in tasks_to_run:
        runner = TASK_RUNNERS[task_name]
        kwargs: Dict[str, Any] = {"precision_mode": precision_mode}
        if task_name == "taubench_banking_mitigation":
            kwargs["few_shot_confirmed"] = few_shot_confirmed
        kwargs.update(task_kwargs.get(task_name, {}))

        result = runner(**kwargs)
        results.append(result)

        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(
            f"[{result.priority}] {task_name:<40} "
            f"score={result.score:.3f} target={result.target:.3f} "
            f"delta={result.delta_vs_target:+.3f} {status}"
        )
        if result.precondition_failures:
            for pf in result.precondition_failures:
                print(f"    ⚠️  PRECONDITION: {pf}")

    all_passed = all(r.passed for r in results)
    episode = EvalEpisode(
        episode_id=f"EVAL-{session_id}-{run_id}",
        session_id=session_id,
        run_id=run_id,
        timestamp_utc=timestamp,
        precision_mode=precision_mode,
        tasks_run=tasks_to_run,
        results=results,
        all_passed=all_passed,
        issue_close_eligible=False,  # Apogee Lens approval required to flip True
        notes="Stub run — wire all task runners to Nemotron 3 Ultra before production use.",
    )

    if output_dir:
        out_path = Path(output_dir) / f"eval_episode_{episode.episode_id}.json"
        episode.to_json(out_path)
        print(f"\nEpisode record written: {out_path}")

    print(f"\n{'ALL TASKS PASSED' if all_passed else 'SOME TASKS FAILED'} — "
          f"issue_close_eligible={episode.issue_close_eligible} "
          f"(Apogee Lens approval required)")
    return episode


# ---------------------------------------------------------------------------
# pytest fixtures and test cases
# ---------------------------------------------------------------------------

try:
    import pytest

    @pytest.fixture
    def stub_episode() -> EvalEpisode:
        return run_suite(precision_mode="BF16", session_id="TEST", few_shot_confirmed=True)

    class TestContractionProofFidelity:
        def test_stub_passes_target(self):
            result = run_contraction_proof_fidelity(n_samples=200)
            # Stub should pass at >95% rate with synthetic matrices
            assert result.score > 0.85, f"Unexpected stub score: {result.score}"

        def test_spectral_radius_gate(self):
            M = np.array([[0.5, 0.0], [0.0, 0.5]])
            rho = float(np.max(np.abs(np.linalg.eigvals(M))))
            assert rho < 1.0

        def test_failing_spectral_radius_detected(self):
            M = np.array([[2.0, 0.0], [0.0, 2.0]])
            rho = float(np.max(np.abs(np.linalg.eigvals(M))))
            assert rho >= 1.0

    class TestGovernanceSchemaConformance:
        def test_stub_passes_target(self):
            result = run_governance_schema_conformance(n_variants=500)
            assert result.score > 0.95

        def test_task_spec_target(self):
            assert DGAF_EVAL_TASKS["governance_schema_conformance"]["target"] == 0.99

    class TestRoleBoundaryCoherence:
        def test_stub_passes_target(self):
            result = run_role_boundary_coherence(n_traces=100)
            assert result.score > 0.90

        def test_task_priority(self):
            assert DGAF_EVAL_TASKS["role_boundary_coherence"]["priority"] == 3

    class TestAuditHallucinationRate:
        def test_bf16_precondition_passes(self):
            failures = check_preconditions("audit_hallucination_rate", "BF16")
            assert failures == []

        def test_nvfp4_precondition_fails(self):
            failures = check_preconditions("audit_hallucination_rate", "NVFP4")
            assert len(failures) == 1
            assert "BF16" in failures[0]

        def test_bf16_stub_at_target(self):
            result = run_audit_hallucination_rate(precision_mode="BF16", n_samples=200)
            assert result.score > 0.75
            assert result.preconditions_met

        def test_nvfp4_precondition_caught(self):
            result = run_audit_hallucination_rate(precision_mode="NVFP4", n_samples=50)
            assert not result.preconditions_met
            assert not result.passed

    class TestTauBenchBankingMitigation:
        def test_blocked_without_few_shot(self):
            result = run_taubench_banking_mitigation(few_shot_confirmed=False, n_cases=50)
            assert not result.passed
            assert not result.preconditions_met
            assert len(result.precondition_failures) > 0

        def test_passes_with_few_shot(self):
            result = run_taubench_banking_mitigation(few_shot_confirmed=True, n_cases=200)
            assert result.score > 0.75
            assert result.preconditions_met

        def test_raw_baseline_warning(self):
            spec = DGAF_EVAL_TASKS["taubench_banking_mitigation"]
            assert spec["published_baseline"] < 0.30, "Raw baseline should be < 30%"

    class TestSuiteRunner:
        def test_full_suite_runs(self):
            episode = run_suite(
                precision_mode="BF16",
                session_id="TEST",
                few_shot_confirmed=True,
                **{
                    "contraction_proof_fidelity": {"n_samples": 20},
                    "governance_schema_conformance": {"n_variants": 50},
                    "role_boundary_coherence": {"n_traces": 20},
                    "audit_hallucination_rate": {"n_samples": 20},
                    "taubench_banking_mitigation": {"n_cases": 20},
                },
            )
            assert len(episode.results) == 5
            assert episode.episode_id.startswith("EVAL-TEST")
            assert not episode.issue_close_eligible  # Apogee Lens required

        def test_episode_json_serializable(self):
            episode = run_suite(
                precision_mode="BF16",
                session_id="TEST",
                few_shot_confirmed=True,
                **{
                    "contraction_proof_fidelity": {"n_samples": 5},
                    "governance_schema_conformance": {"n_variants": 5},
                    "role_boundary_coherence": {"n_traces": 5},
                    "audit_hallucination_rate": {"n_samples": 5},
                    "taubench_banking_mitigation": {"n_cases": 5},
                },
            )
            json_str = episode.to_json()
            parsed = json.loads(json_str)
            assert parsed["session_id"] == "TEST"
            assert len(parsed["results"]) == 5

except ImportError:
    pass  # pytest not installed in all environments


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="DGAF Eval Suite — Nemotron 3 Ultra Parametric Benchmark"
    )
    parser.add_argument("--precision", choices=["BF16", "NVFP4"], default="BF16")
    parser.add_argument("--session", default="S069")
    parser.add_argument("--tasks", nargs="+", choices=list(DGAF_EVAL_TASKS.keys()), default=None)
    parser.add_argument("--few-shot", action="store_true", dest="few_shot_confirmed")
    parser.add_argument("--quick", action="store_true", help="Run with reduced sample counts for CI")
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    task_kwargs: Dict[str, Any] = {}
    if args.quick:
        task_kwargs = {
            "contraction_proof_fidelity": {"n_samples": 20},
            "governance_schema_conformance": {"n_variants": 100},
            "role_boundary_coherence": {"n_traces": 20},
            "audit_hallucination_rate": {"n_samples": 20},
            "taubench_banking_mitigation": {"n_cases": 20},
        }

    print(f"\n=== DGAF Eval Suite — Nemotron 3 Ultra — {args.precision} — {args.session} ===")
    print(f"Issue #32 | Pattern bundle: high_risk_state_mutation | Amethyst × COLLEEN\n")

    episode = run_suite(
        precision_mode=args.precision,
        session_id=args.session,
        tasks=args.tasks,
        few_shot_confirmed=args.few_shot_confirmed,
        output_dir=Path(args.output_dir) if args.output_dir else None,
        **task_kwargs,
    )
