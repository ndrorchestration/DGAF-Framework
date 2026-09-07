#!/usr/bin/env python3
"""Non-empirical engineering diagnostic for the P-30 treatment-binding defect.

This module does not authorize, execute, or replace a scientific Solo/High-Assurance
experiment. It asks one bounded engineering question: once the previously missing
P-30 Apogee substrate is populated with an explicitly synthetic minimum-passing
fixture, can the remainder of the DGAF consensus treatment execute?

The fixture is deliberately fixed at 0.45 because that is the lowest passing
threshold in the already-designated P-30 S/A/B/C/D semantics. It is NOT an
observed, estimated, calibrated, or real Apogee confidence and must never be
reported as one.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from dgaf_tgl_adapter import ConsensusState, DGAF_TGLAdapter
from harness_contract import TOPOLOGY_SPECS, make_streams
from pdmaltgl_gate_binding import ApogeeAttestationState, build_apogee_hook
from pptl.triadic_governance_loop import GateResult
from task_engine import (
    AttemptStatus,
    CONSENSUS_ITERATIONS,
    FAILURE_INJECTION_ITERATION,
    FAILURE_RECOVERY_ITERATION,
    PILOT_FAILURE_COUNTS,
    SEED_RUNTIME_CEILING_SECONDS,
    ConsensusTask,
    ConsensusTrialResult,
)
from topology_utils import graph_fingerprint

DIAGNOSTIC_RECORD_TYPE = "DGAF_PDMAL_P30_REMEDIATION_ENGINEERING_DIAGNOSTIC"
DIAGNOSTIC_EPOCH = "SOLO-P30-DIAGNOSTIC-EPOCH-002"
P30_BINDING_ID = "SYNTHETIC_MINIMUM_PASSING_P30_FIXTURE_V1"
P30_FIXTURE_CONFIDENCE = 0.45
P30_FIXTURE_DESCRIPTION = (
    "Synthetic minimum-passing P-30 engineering diagnostic fixture; not a real Apogee confidence"
)
DIAGNOSTIC_SEEDS = (20260819, 20260820)


def _fixture_state() -> ApogeeAttestationState:
    return ApogeeAttestationState(
        confidence=P30_FIXTURE_CONFIDENCE,
        artifact_description=P30_FIXTURE_DESCRIPTION,
    )


def validate_fixture_contract() -> None:
    """Fail closed if the diagnostic fixture drifts from the preregistered boundary."""
    if P30_FIXTURE_CONFIDENCE != 0.45:
        raise RuntimeError("P-30 diagnostic fixture must remain exactly 0.45")
    state = _fixture_state()
    result = build_apogee_hook(state)("", {})
    if result is not GateResult.PASS or state.grade != "C":
        raise RuntimeError(
            f"P-30 diagnostic fixture contract failed: result={result!r}, grade={state.grade!r}"
        )


class P30FixtureConsensusTask(ConsensusTask):
    """ConsensusTask variant used only by the non-empirical remediation diagnostic."""

    def __init__(self, *, topology: str, failure_count: int) -> None:
        super().__init__(topology=topology, failure_count=failure_count, condition="dgaf")

    def _dgaf_update(
        self,
        *,
        seed: int,
        iteration: int,
        values: np.ndarray,
        graph,
        alive: tuple[bool, ...],
        active_neighbors: tuple[tuple[int, ...], ...],
        failure_history: tuple[tuple[int, ...], ...],
        failure_count_current: int,
        failure_count_total: int,
    ):
        adapter = DGAF_TGLAdapter(
            session_id=f"pdmAL-p30-diagnostic-{self.trial_key(seed, self.topology, self.condition, self.failure_count)}"
        )
        state = ConsensusState(
            seed_id=seed,
            iteration=iteration,
            agent_values=tuple(float(x) for x in values),
            alive=alive,
            original_neighbors=tuple(tuple(sorted(graph.neighbors(i))) for i in range(20)),
            active_neighbors=active_neighbors,
            failure_history=failure_history,
            failure_count_current=failure_count_current,
            failure_count_total=failure_count_total,
            current_final_std=float(np.std(values)),
            current_mean=float(np.mean(values)),
            runtime_budget_remaining_ms=int(SEED_RUNTIME_CEILING_SECONDS * 1000),
            protocol_id="PDMAL-P30-DIAGNOSTIC-EPOCH-002",
            apogee_state=_fixture_state(),
        )
        try:
            result = adapter.run_turn(state)
        except Exception as exc:
            return (
                values,
                AttemptStatus.FAILURE,
                f"dgaf-adapter-error:{type(exc).__name__}: {exc}",
                None,
            )
        governance_trace = result.audit.to_dict()
        governance_trace["decision"] = result.decision
        governance_trace["outcome"] = result.attempt_status.value
        if result.decision == "FAIL_CLOSED" or result.next_values is None:
            return values, AttemptStatus.FAILURE, "dgaf-fail-closed", governance_trace
        return np.asarray(result.next_values, dtype=float), AttemptStatus.SUCCESS, None, governance_trace


def _gate_failure_counts(result: ConsensusTrialResult) -> dict[str, int]:
    counts: dict[str, int] = {}
    for turn in result.governance_trace:
        for gate in turn.get("gate_records", []):
            gate_name = str(gate.get("gate_name", "UNKNOWN"))
            gate_result = str(gate.get("result", "UNKNOWN"))
            if gate_result in {"KILL", "KILL_REC", "SKIP"}:
                key = f"{gate_name}:{gate_result}"
                counts[key] = counts.get(key, 0) + 1
    return counts


def run_diagnostic(output: Path) -> dict[str, Any]:
    validate_fixture_contract()
    records: list[dict[str, Any]] = []
    total_success = 0
    total_failure = 0
    aggregate_gate_failures: dict[str, int] = {}

    for seed in DIAGNOSTIC_SEEDS:
        for topology in TOPOLOGY_SPECS:
            for failure_count in PILOT_FAILURE_COUNTS:
                task = P30FixtureConsensusTask(
                    topology=topology,
                    failure_count=failure_count,
                )
                result = task.run_detailed(seed=seed, attempt=1)
                success = result.attempt_status is AttemptStatus.SUCCESS
                total_success += int(success)
                total_failure += int(not success)
                failures = _gate_failure_counts(result)
                for key, count in failures.items():
                    aggregate_gate_failures[key] = aggregate_gate_failures.get(key, 0) + count
                records.append(
                    {
                        "seed": seed,
                        "topology": topology,
                        "failure_count": failure_count,
                        "attempt_status": result.attempt_status.value,
                        "iterations_completed": result.iterations_completed,
                        "deviation": result.deviation,
                        "consensus_success": result.consensus_success,
                        "final_std": result.final_std,
                        "topology_fingerprint": result.topology_fingerprint,
                        "gate_failures": failures,
                    }
                )

    document = {
        "record_type": DIAGNOSTIC_RECORD_TYPE,
        "classification": "NON_EMPIRICAL_ENGINEERING_DIAGNOSTIC",
        "diagnostic_epoch": DIAGNOSTIC_EPOCH,
        "scientific_n_increment": 0,
        "p30_binding_id": P30_BINDING_ID,
        "p30_fixture_confidence": P30_FIXTURE_CONFIDENCE,
        "p30_fixture_is_real_confidence": False,
        "p30_fixture_grade": "C",
        "seeds": list(DIAGNOSTIC_SEEDS),
        "topologies": list(TOPOLOGY_SPECS),
        "failure_counts": list(PILOT_FAILURE_COUNTS),
        "total_diagnostic_trials": len(records),
        "attempt_success_count": total_success,
        "attempt_failure_count": total_failure,
        "aggregate_gate_failures": dict(sorted(aggregate_gate_failures.items())),
        "records": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def main() -> int:
    output = Path("test-artifacts/p30_remediation_diagnostic.json")
    document = run_diagnostic(output)
    print(
        "P30_REMEDIATION_DIAGNOSTIC_COMPLETE: "
        f"trials={document['total_diagnostic_trials']} "
        f"attempt_success={document['attempt_success_count']} "
        f"attempt_failure={document['attempt_failure_count']}"
    )
    print("SCIENTIFIC_N_INCREMENT=0")
    print(f"artifact={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
