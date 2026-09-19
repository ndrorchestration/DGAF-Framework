#!/usr/bin/env python3
"""Synthetic known-truth oracle for the frozen Track A Epoch 002 analysis.

This runner never consumes protected or empirical Track A material. It generates
only deterministic synthetic records with planted outcomes, invokes the exact
frozen analysis module, verifies known-answer and fail-closed behavior, and emits
non-empirical evidence artifacts.

It is not the authorized empirical primary analysis and cannot change scientific
or governance state.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUN_DEFINITION_REL = "docs/experiment/TRACK_A_EPOCH_002_SYNTHETIC_ORACLE_RUN.json"
ANALYSIS_REL = "experiments/pdmal_pilot/track_a_epoch_002_analysis.py"
REQUIREMENTS_REL = "experiments/pdmal_pilot/requirements-full-lock.txt"

CLASSIFICATION = "SYNTHETIC_ENGINEERING_ASSURANCE_ONLY"
EXPECTED_ANALYSIS_BLOB = "d4495f7cdf211b974039ec0e66292dc62ea0881f"
EXPECTED_ANALYSIS_CONFIG = "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
EXPECTED_REQUIREMENTS_BLOB = "00c1f779e97030f9b25ae494642edb31b5b09de5"
EXPECTED_PYTHON = "3.12.0"
EXPECTED_NUMPY = "2.5.1"

INPUT_MANIFEST_NAME = "TRACK_A_EPOCH_002_SYNTHETIC_ORACLE_INPUT_MANIFEST.json"
RESULT_NAME = "TRACK_A_EPOCH_002_SYNTHETIC_ORACLE_RESULT.json"

SEEDS = tuple(range(20270201, 20270251))
TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)
ALGORITHM_ID = "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"


def fail(message: str) -> None:
    raise SystemExit(f"TRACK_A_EPOCH_002_SYNTHETIC_ORACLE_FAIL: {message}")


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob(relpath: str) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relpath}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        fail(f"cannot resolve frozen blob for {relpath}: {completed.stderr.strip()}")
    return completed.stdout.strip()


def source_sha() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        fail("cannot resolve source HEAD")
    return completed.stdout.strip()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"{path} must contain a JSON object")
    return value


def load_analysis() -> Any:
    path = ROOT / ANALYSIS_REL
    spec = importlib.util.spec_from_file_location("track_a_epoch_002_synthetic_oracle_analysis", path)
    if spec is None or spec.loader is None:
        fail("cannot load frozen analysis module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_run_definition(definition: dict[str, Any]) -> None:
    if definition.get("classification") != CLASSIFICATION:
        fail("run-definition classification drift")
    if definition.get("execution_scope") != "FROZEN_ANALYSIS_KNOWN_TRUTH_ORACLE_ONLY":
        fail("run-definition execution scope drift")
    state = definition.get("state_effect")
    if not isinstance(state, dict):
        fail("run-definition state_effect is malformed")
    expected_state = {
        "empirical_data_used": False,
        "protected_material_used": False,
        "real_primary_analysis_performed": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
    }
    if state != expected_state:
        fail("run-definition scientific/governance boundary drift")

    matrix = definition.get("matrix")
    if not isinstance(matrix, dict):
        fail("run-definition matrix is malformed")
    required_matrix = {
        "seed_count": 50,
        "records_per_seed": 45,
        "total_records_per_scenario": 2250,
        "algorithm_id": ALGORITHM_ID,
    }
    for key, expected in required_matrix.items():
        if matrix.get(key) != expected:
            fail(f"run-definition matrix drift: {key}")

    bindings = definition.get("bindings")
    if not isinstance(bindings, dict):
        fail("run-definition bindings are malformed")
    expected_bindings = {
        "analysis_path": ANALYSIS_REL,
        "analysis_blob_sha": EXPECTED_ANALYSIS_BLOB,
        "analysis_config_sha256": EXPECTED_ANALYSIS_CONFIG,
        "requirements_lock_path": REQUIREMENTS_REL,
        "requirements_lock_blob_sha": EXPECTED_REQUIREMENTS_BLOB,
        "python_version": EXPECTED_PYTHON,
        "numpy_version": EXPECTED_NUMPY,
    }
    for key, expected in expected_bindings.items():
        if bindings.get(key) != expected:
            fail(f"run-definition binding drift: {key}")


def validate_frozen_environment(analysis: Any) -> dict[str, str]:
    if git_blob(ANALYSIS_REL) != EXPECTED_ANALYSIS_BLOB:
        fail("frozen analysis blob drift")
    if git_blob(REQUIREMENTS_REL) != EXPECTED_REQUIREMENTS_BLOB:
        fail("frozen requirements blob drift")
    if analysis.analysis_config_sha256() != EXPECTED_ANALYSIS_CONFIG:
        fail("frozen analysis configuration drift")
    actual_python = platform.python_version()
    actual_numpy = np.__version__
    if actual_python != EXPECTED_PYTHON:
        fail(f"Python mismatch: expected {EXPECTED_PYTHON}, got {actual_python}")
    if actual_numpy != EXPECTED_NUMPY:
        fail(f"NumPy mismatch: expected {EXPECTED_NUMPY}, got {actual_numpy}")
    return {"python": actual_python, "numpy": actual_numpy}


def success_counts(scenario: str, seed_index: int) -> tuple[int, int]:
    if scenario == "positive_constant":
        return 8, 4
    if scenario == "null_constant":
        return 5, 5
    if scenario == "negative_constant":
        return 3, 7
    if scenario == "balanced_mixed":
        return (6, 5) if seed_index < 25 else (5, 6)
    raise ValueError(f"unknown synthetic scenario: {scenario}")


def build_records(
    scenario: str,
    *,
    invert_nuisance: bool = False,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for seed_index, seed in enumerate(SEEDS):
        pdmal_count, rr_count = success_counts(scenario, seed_index)
        for topology_index, topology in enumerate(TOPOLOGIES):
            for failure_index, failure_count in enumerate(FAILURE_COUNTS):
                if topology == "pdmal":
                    success = failure_index < pdmal_count
                elif topology == "random_regular":
                    success = failure_index < rr_count
                else:
                    success = ((seed_index + topology_index + failure_index) % 3) == 0
                    if invert_nuisance:
                        success = not success
                records.append(
                    {
                        "seed_id": seed,
                        "topology": topology,
                        "failure_count": failure_count,
                        "ffcr_success": bool(success),
                        "algorithm_id": ALGORITHM_ID,
                        "excluded": False,
                    }
                )
    if len(records) != 2250:
        fail(f"synthetic fixture shape drift: {len(records)} records")
    return records


def result_digest(result: dict[str, Any]) -> str:
    return sha256_bytes(canonical_bytes(result))


def run_analysis(analysis: Any, records: list[dict[str, object]]) -> tuple[dict[str, Any], float]:
    started = time.perf_counter()
    result = analysis.analyze(records)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    if not isinstance(result, dict):
        fail("frozen analysis returned a non-object result")
    return result, elapsed_ms


def assert_close(actual: float, expected: float, label: str) -> None:
    if abs(float(actual) - expected) > 1e-12:
        fail(f"{label} mismatch: expected {expected}, got {actual}")


def validate_oracle_result(scenario: str, result: dict[str, Any]) -> None:
    estimate = float(result["estimate_pdmal_minus_random_regular"])
    low, high = (float(x) for x in result["two_sided_95pct_percentile_ci"])
    classification = result["classification"]

    expected_class = {
        "positive_constant": "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS",
        "null_constant": "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED",
        "negative_constant": "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS",
        "balanced_mixed": "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED",
    }[scenario]
    expected_estimate = {
        "positive_constant": 4.0 / 9.0,
        "null_constant": 0.0,
        "negative_constant": -4.0 / 9.0,
        "balanced_mixed": 0.0,
    }[scenario]

    assert_close(estimate, expected_estimate, f"{scenario} estimate")
    if classification != expected_class:
        fail(
            f"{scenario} classification mismatch: expected {expected_class}, "
            f"got {classification}"
        )

    if scenario in {"positive_constant", "negative_constant"}:
        assert_close(low, expected_estimate, f"{scenario} CI lower")
        assert_close(high, expected_estimate, f"{scenario} CI upper")
    elif scenario == "null_constant":
        assert_close(low, 0.0, "null_constant CI lower")
        assert_close(high, 0.0, "null_constant CI upper")
    elif not (low < 0.0 < high):
        fail(f"balanced_mixed CI must straddle zero, got [{low}, {high}]")

    if result.get("paired_seed_count") != 50:
        fail(f"{scenario} paired-seed count drift")
    if result.get("bootstrap_resamples") != 10000:
        fail(f"{scenario} bootstrap-resample count drift")
    if result.get("bootstrap_seed") != 20270251:
        fail(f"{scenario} bootstrap seed drift")
    if result.get("alpha") != 0.05:
        fail(f"{scenario} alpha drift")
    if result.get("canonical_dgaf_efficacy") != "NOT_ESTABLISHED":
        fail(f"{scenario} attempted efficacy promotion")
    if result.get("high_assurance") != "NOT_AUTHORIZED_N0":
        fail(f"{scenario} attempted High-Assurance promotion")


def negative_control(
    analysis: Any,
    name: str,
    mutate: Callable[[list[dict[str, object]]], None],
    expected_fragment: str,
) -> dict[str, str]:
    records = [dict(row) for row in build_records("positive_constant")]
    mutate(records)
    try:
        analysis.analyze(records)
    except ValueError as exc:
        message = str(exc)
        if expected_fragment not in message:
            fail(
                f"negative control {name} rejected for unexpected reason: {message}"
            )
        return {"status": "PASS_REJECTED", "reason": message}
    fail(f"negative control {name} was not rejected")


def write_artifact(path: Path, value: dict[str, Any]) -> str:
    raw = canonical_bytes(value)
    path.write_bytes(raw)
    digest = sha256_bytes(raw)
    path.with_suffix(path.suffix + ".sha256").write_text(
        f"{digest}  {path.name}\n",
        encoding="ascii",
    )
    return digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    definition_path = ROOT / RUN_DEFINITION_REL
    definition = load_json(definition_path)
    validate_run_definition(definition)

    analysis = load_analysis()
    environment = validate_frozen_environment(analysis)
    head = source_sha()

    scenario_summaries: dict[str, Any] = {}
    input_manifest_entries: dict[str, Any] = {}
    for scenario in (
        "positive_constant",
        "null_constant",
        "negative_constant",
        "balanced_mixed",
    ):
        records = build_records(scenario)
        input_sha = sha256_bytes(canonical_bytes(records))
        first, first_ms = run_analysis(analysis, records)
        second, second_ms = run_analysis(analysis, records)
        validate_oracle_result(scenario, first)
        validate_oracle_result(scenario, second)
        if canonical_bytes(first) != canonical_bytes(second):
            fail(f"{scenario} deterministic replay drift")

        scenario_summaries[scenario] = {
            "status": "PASS",
            "record_count": len(records),
            "input_sha256": input_sha,
            "analysis_result_sha256": result_digest(first),
            "estimate": first["estimate_pdmal_minus_random_regular"],
            "two_sided_95pct_percentile_ci": first[
                "two_sided_95pct_percentile_ci"
            ],
            "classification": first["classification"],
            "first_runtime_ms": first_ms,
            "replay_runtime_ms": second_ms,
            "deterministic_replay_equal": True,
        }
        input_manifest_entries[scenario] = {
            "record_count": len(records),
            "sha256": input_sha,
        }

    positive = build_records("positive_constant")
    positive_result, _ = run_analysis(analysis, positive)

    reversed_result, _ = run_analysis(analysis, list(reversed(positive)))
    if canonical_bytes(reversed_result) != canonical_bytes(positive_result):
        fail("record-order invariance failed")

    nuisance_result, _ = run_analysis(
        analysis,
        build_records("positive_constant", invert_nuisance=True),
    )
    if canonical_bytes(nuisance_result) != canonical_bytes(positive_result):
        fail("nonprimary-topology outcome invariance failed")

    controls = {
        "missing_matrix_cell": negative_control(
            analysis,
            "missing_matrix_cell",
            lambda rows: rows.pop(),
            "expected exactly 2250 records",
        ),
        "duplicate_matrix_cell": negative_control(
            analysis,
            "duplicate_matrix_cell",
            lambda rows: rows.__setitem__(-1, dict(rows[0])),
            "duplicate matrix cell",
        ),
        "non_boolean_endpoint": negative_control(
            analysis,
            "non_boolean_endpoint",
            lambda rows: rows[0].__setitem__("ffcr_success", 1),
            "ffcr_success must be boolean",
        ),
        "wrong_algorithm_identity": negative_control(
            analysis,
            "wrong_algorithm_identity",
            lambda rows: rows[0].__setitem__("algorithm_id", "SYNTHETIC_WRONG"),
            "algorithm identity does not match",
        ),
        "outcome_exclusion_attempt": negative_control(
            analysis,
            "outcome_exclusion_attempt",
            lambda rows: rows[0].__setitem__("excluded", True),
            "outcome exclusions are prohibited",
        ),
    }

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    run_definition_sha256 = sha256_bytes(definition_path.read_bytes())
    input_manifest = {
        "record_type": "TRACK_A_EPOCH_002_SYNTHETIC_ORACLE_INPUT_MANIFEST",
        "schema_version": 1,
        "classification": CLASSIFICATION,
        "source_sha": head,
        "run_definition_sha256": run_definition_sha256,
        "generator_path": "scripts/run_track_a_epoch_002_synthetic_oracle.py",
        "scenario_inputs": input_manifest_entries,
        "empirical_data_used": False,
        "protected_material_used": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    input_manifest_digest = write_artifact(
        output_dir / INPUT_MANIFEST_NAME,
        input_manifest,
    )

    result = {
        "record_type": "TRACK_A_EPOCH_002_SYNTHETIC_ORACLE_RESULT",
        "schema_version": 1,
        "classification": CLASSIFICATION,
        "source_sha": head,
        "run_definition_sha256": run_definition_sha256,
        "input_manifest_sha256": input_manifest_digest,
        "frozen_bindings": {
            "analysis_blob_sha": EXPECTED_ANALYSIS_BLOB,
            "analysis_config_sha256": EXPECTED_ANALYSIS_CONFIG,
            "requirements_lock_blob_sha": EXPECTED_REQUIREMENTS_BLOB,
        },
        "environment": environment,
        "scenarios": scenario_summaries,
        "invariance_checks": {
            "record_order_invariance": "PASS",
            "nonprimary_topology_outcome_invariance": "PASS",
            "deterministic_replay": "PASS",
        },
        "negative_controls": controls,
        "measurements": {
            "scenario_count": 4,
            "records_per_scenario": 2250,
            "synthetic_records_exercised_in_oracle_scenarios": 9000,
            "negative_controls_required": 5,
            "negative_controls_rejected": sum(
                1 for item in controls.values() if item["status"] == "PASS_REJECTED"
            ),
        },
        "empirical_data_used": False,
        "protected_material_used": False,
        "real_primary_analysis_performed": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
        "claim_ceiling": "ENGINEERING_ASSURANCE_OF_THE_FROZEN_ANALYSIS_CODE_PATH_ONLY",
    }

    write_artifact(output_dir / RESULT_NAME, result)

    print("TRACK_A_EPOCH_002_SYNTHETIC_ORACLE=PASS")
    print("CLASSIFICATION=SYNTHETIC_ENGINEERING_ASSURANCE_ONLY")
    print("SCENARIOS=4")
    print("SYNTHETIC_RECORDS_EXERCISED=9000")
    print("NEGATIVE_CONTROLS_REJECTED=5")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("REAL_PRIMARY_ANALYSIS_PERFORMED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
