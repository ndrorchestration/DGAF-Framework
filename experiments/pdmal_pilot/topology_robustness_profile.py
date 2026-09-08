#!/usr/bin/env python3
"""Track A non-empirical topology-robustness structural probe.

This module reuses the historical numeric reference-update mechanics but emits
only structural identities and cryptographic hashes. It does not compute or
serialize efficacy endpoints.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

from harness_contract import TOPOLOGY_SPECS
from task_engine import PILOT_FAILURE_COUNTS, ConsensusTask
from topology_utils import graph_fingerprint

ROOT = Path(__file__).resolve().parents[2]
PROFILE_PATH = ROOT / "docs/governance/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1.json"
OUTPUT = ROOT / "test-artifacts/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1_PROBE.json"

PROFILE_ID = "PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1"
ALGORITHM_ID = "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
DIAGNOSTIC_SEEDS = (20261201, 20261202)
EXPECTED_TASK_ENGINE_BLOB = "90135e1c6dfccc3b56ffdc0dcb9eb50a0b2a5b05"
EXPECTED_HARNESS_BLOB = "bb97c54ddf087fef568b1b3c8f8df72c30dad11e"
FORBIDDEN_TOKENS = (
    "ffcr",
    "final_std",
    "consensus_success",
    "treatment_effect",
    "confidence_interval",
    "p_value",
    "governance_trace",
    "canonical_dgaf",
    "full_dgaf",
)


def _git_blob(path: str) -> str:
    return subprocess.check_output(
        ["git", "hash-object", path],
        cwd=ROOT,
        text=True,
    ).strip()


def _vector_hash(values: np.ndarray) -> str:
    canonical = np.asarray(values, dtype="<f8")
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


def _validate_profile() -> dict:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    assert profile["profile_id"] == PROFILE_ID
    assert profile["scientific_n_increment"] == 0
    assert profile["empirical_authorization"] is False
    assert profile["algorithm"]["public_id"] == ALGORITHM_ID
    assert profile["algorithm"]["alpha"] == 0.5
    assert profile["algorithm"]["public_condition_axis"] is False
    assert profile["algorithm"]["dgaf_semantic_gate_path"] is False
    assert profile["diagnostic_probe"]["seeds"] == list(DIAGNOSTIC_SEEDS)
    assert profile["diagnostic_probe"]["topologies"] == list(TOPOLOGY_SPECS)
    assert profile["diagnostic_probe"]["failure_counts"] == list(PILOT_FAILURE_COUNTS)
    assert profile["diagnostic_probe"]["expected_cells"] == (
        len(DIAGNOSTIC_SEEDS) * len(TOPOLOGY_SPECS) * len(PILOT_FAILURE_COUNTS)
    )
    assert _git_blob("experiments/pdmal_pilot/task_engine.py") == EXPECTED_TASK_ENGINE_BLOB
    assert _git_blob("experiments/pdmal_pilot/harness_contract.py") == EXPECTED_HARNESS_BLOB
    return profile


def run_probe(output: Path = OUTPUT) -> dict:
    profile = _validate_profile()
    records: list[dict] = []

    for seed in DIAGNOSTIC_SEEDS:
        for topology in TOPOLOGY_SPECS:
            for failure_count in PILOT_FAILURE_COUNTS:
                # Internal historical label is implementation reuse only and is
                # intentionally absent from the emitted artifact.
                task = ConsensusTask(
                    topology=topology,
                    failure_count=failure_count,
                    condition="null",
                )
                graph, initial_values_tuple, failure_nodes = task._build_trial_inputs(seed)
                initial_values = np.asarray(initial_values_tuple, dtype=float)

                phase_failed_sets = {
                    "pre_failure": set(),
                    "during_failure": set(failure_nodes),
                    "recovered": set(),
                }
                phase_hashes = {}
                for phase, failed in phase_failed_sets.items():
                    neighbors = task._active_neighbors(graph, failed)
                    updated = task._null_or_simple_update(initial_values, neighbors, 0.5)
                    phase_hashes[phase] = _vector_hash(updated)

                records.append(
                    {
                        "seed": seed,
                        "topology": topology,
                        "failure_count": failure_count,
                        "topology_fingerprint": graph_fingerprint(graph),
                        "failure_nodes": list(failure_nodes),
                        "initial_state_hash": _vector_hash(initial_values),
                        "phase_update_hashes": phase_hashes,
                    }
                )

    document = {
        "record_type": "PDMAL_TOPOLOGY_ROBUSTNESS_STRUCTURAL_PROBE",
        "schema_version": 1,
        "profile_id": PROFILE_ID,
        "algorithm_id": ALGORITHM_ID,
        "scientific_n_increment": 0,
        "empirical_authorization": False,
        "task_engine_blob_sha": EXPECTED_TASK_ENGINE_BLOB,
        "harness_blob_sha": EXPECTED_HARNESS_BLOB,
        "seeds": list(DIAGNOSTIC_SEEDS),
        "topologies": list(TOPOLOGY_SPECS),
        "failure_counts": list(PILOT_FAILURE_COUNTS),
        "expected_cells": profile["diagnostic_probe"]["expected_cells"],
        "completed_cells": len(records),
        "classification": "STRUCTURAL_HASH_ONLY_NONEMPIRICAL",
        "records": records,
    }

    raw = json.dumps(document, indent=2, sort_keys=True) + "\n"
    lowered = raw.lower()
    for token in FORBIDDEN_TOKENS:
        if token in lowered:
            raise RuntimeError(f"Track A probe emitted forbidden token: {token}")

    # Recovery restores the same neighbor structure used pre-failure when both
    # are evaluated from the same fixed initial state.
    assert all(
        record["phase_update_hashes"]["pre_failure"]
        == record["phase_update_hashes"]["recovered"]
        for record in records
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(raw, encoding="utf-8")
    return document


def main() -> int:
    document = run_probe()
    assert document["completed_cells"] == document["expected_cells"] == 90
    print(
        "PDMAL_TOPOLOGY_ROBUSTNESS_STRUCTURAL_PROBE_PASS "
        f"cells={document['completed_cells']} n_increment=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
