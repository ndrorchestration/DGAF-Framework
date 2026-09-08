#!/usr/bin/env python3
"""Non-empirical topology/decision-path diagnostic after canonical Epoch 004.

This diagnostic is hypothesis-generating only. It emits governance decision
frequencies and sparse-neighbor structure, never FFCR, final consensus outcomes,
treatment effects, confidence intervals, or efficacy classifications.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from run_canonical_epoch_004 import CanonicalEpoch004Task
from canonical_profile_tgl_diagnostic import load_and_validate_qualification
from task_engine import (
    CONSENSUS_ITERATIONS,
    FAILURE_INJECTION_ITERATION,
    FAILURE_RECOVERY_ITERATION,
    PILOT_FAILURE_COUNTS,
)
from harness_contract import TOPOLOGY_SPECS

DIAGNOSTIC_ID = "DGAF-CANONICAL-TOPOLOGY-MECHANISM-DIAGNOSTIC-V1"
DIAGNOSTIC_SEEDS = (20261101, 20261102)
FORBIDDEN_OUTPUT_KEYS = {
    "ffcr_success",
    "primary_outcome",
    "secondary_outcomes",
    "final_std",
    "consensus_success",
    "effect",
    "confidence_interval",
    "p_value",
}


def _zero_neighbor_turn_count(task: CanonicalEpoch004Task, seed: int) -> tuple[int, int]:
    graph, _initial_values, failure_nodes = task._build_trial_inputs(seed)
    failed: set[int] = set()
    zero_node_turns = 0
    turns_with_any_zero_neighbor = 0
    for iteration in range(CONSENSUS_ITERATIONS):
        if iteration == FAILURE_INJECTION_ITERATION:
            failed = set(failure_nodes)
        elif iteration == FAILURE_RECOVERY_ITERATION:
            failed = set()
        active = task._active_neighbors(graph, failed)
        count = sum(1 for neighbors in active if not neighbors)
        zero_node_turns += count
        turns_with_any_zero_neighbor += int(count > 0)
    return zero_node_turns, turns_with_any_zero_neighbor


def _trace_summary(trace: tuple[dict, ...]) -> dict:
    decisions = Counter()
    gate_results = Counter()
    final_statuses = Counter()
    malformed_turns = 0
    for turn in trace:
        decision = turn.get("decision")
        if isinstance(decision, str):
            decisions[decision] += 1
        else:
            malformed_turns += 1
        status = turn.get("final_status")
        if isinstance(status, str):
            final_statuses[status] += 1
        gates = turn.get("gates")
        if not isinstance(gates, list):
            malformed_turns += 1
            continue
        for gate in gates:
            step = gate.get("step")
            result = gate.get("result")
            if isinstance(step, int) and isinstance(result, str):
                gate_results[f"step{step}:{result}"] += 1
    return {
        "decision_counts": dict(sorted(decisions.items())),
        "final_status_counts": dict(sorted(final_statuses.items())),
        "gate_result_counts": dict(sorted(gate_results.items())),
        "governance_turn_count": len(trace),
        "malformed_turn_count": malformed_turns,
    }


def run(output: Path) -> dict:
    qualification = load_and_validate_qualification()
    records = []
    aggregate_decisions: Counter[str] = Counter()
    aggregate_zero_neighbor_node_turns = 0
    aggregate_turns_with_zero_neighbor = 0

    for seed in DIAGNOSTIC_SEEDS:
        for topology in TOPOLOGY_SPECS:
            for failure_count in PILOT_FAILURE_COUNTS:
                task = CanonicalEpoch004Task(
                    topology=topology,
                    failure_count=failure_count,
                    qualification_bytes=qualification,
                )
                result = task.run_detailed(seed=seed, attempt=1)
                summary = _trace_summary(result.governance_trace)
                zero_node_turns, turns_with_zero = _zero_neighbor_turn_count(task, seed)
                aggregate_decisions.update(summary["decision_counts"])
                aggregate_zero_neighbor_node_turns += zero_node_turns
                aggregate_turns_with_zero_neighbor += turns_with_zero
                records.append(
                    {
                        "seed": seed,
                        "topology": topology,
                        "failure_count": failure_count,
                        "execution_completed_turns": summary["governance_turn_count"],
                        "decision_counts": summary["decision_counts"],
                        "final_status_counts": summary["final_status_counts"],
                        "gate_result_counts": summary["gate_result_counts"],
                        "malformed_turn_count": summary["malformed_turn_count"],
                        "zero_active_neighbor_node_turns": zero_node_turns,
                        "turns_with_any_zero_active_neighbor": turns_with_zero,
                    }
                )

    document = {
        "record_type": "DGAF_CANONICAL_TOPOLOGY_MECHANISM_DIAGNOSTIC",
        "schema_version": 1,
        "diagnostic_id": DIAGNOSTIC_ID,
        "classification": "POST_PRIMARY_NONEMPIRICAL_MECHANISM_DIAGNOSTIC",
        "scientific_n_increment": 0,
        "empirical_authorization": False,
        "primary_result_unchanged": "EVIDENCE_AGAINST_DIRECTIONAL_DGAF",
        "seeds": list(DIAGNOSTIC_SEEDS),
        "topologies": list(TOPOLOGY_SPECS),
        "failure_counts": list(PILOT_FAILURE_COUNTS),
        "trial_count": len(records),
        "aggregate_decision_counts": dict(sorted(aggregate_decisions.items())),
        "aggregate_zero_active_neighbor_node_turns": aggregate_zero_neighbor_node_turns,
        "aggregate_turns_with_any_zero_active_neighbor": aggregate_turns_with_zero_neighbor,
        "records": records,
        "interpretation": "TRACE_ONLY_HYPOTHESIS_GENERATING_NO_EFFICACY_INFERENCE",
    }
    raw = json.dumps(document, indent=2, sort_keys=True) + "\n"
    lowered = raw.lower()
    for key in FORBIDDEN_OUTPUT_KEYS:
        if key.lower() in lowered:
            raise RuntimeError(f"diagnostic output contains forbidden efficacy field token: {key}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(raw, encoding="utf-8")
    return document


def main() -> int:
    output = Path("test-artifacts/CANONICAL_TOPOLOGY_MECHANISM_DIAGNOSTIC.json")
    doc = run(output)
    if doc["trial_count"] != 90:
        raise SystemExit("diagnostic must contain exactly 90 cells")
    if any(r["malformed_turn_count"] for r in doc["records"]):
        raise SystemExit("diagnostic contains malformed governance traces")
    print(
        "TOPOLOGY_MECHANISM_DIAGNOSTIC_PASS "
        f"trials={doc['trial_count']} decisions={doc['aggregate_decision_counts']} "
        f"zero_neighbor_turns={doc['aggregate_turns_with_any_zero_active_neighbor']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
