#!/usr/bin/env python3
"""Fail-closed validator for Track A Epoch 001 precollection preflight.

This validates candidate stabilization and precollection readiness only.
It does not establish freeze or authorize empirical collection.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_001_RUNNER_CONTRACT.json"
PREFLIGHT_PATH = ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_PRECOLLECTION_PREFLIGHT.json"
DOWNSTREAM = (
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_MANIFEST.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_FINAL_CLOSURE_PACKET.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_VERIFICATION_CLASSIFICATION.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION.json",
)
SOURCE_PATHS = {
    "preregistration_blob_sha": "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json",
    "analysis_lock_blob_sha": "docs/experiment/TRACK_A_EPOCH_001_ANALYSIS_LOCK.json",
    "analysis_blob_sha": "experiments/pdmal_pilot/track_a_epoch_001_analysis.py",
    "requirements_lock_blob_sha": "experiments/pdmal_pilot/requirements-full-lock.txt",
    "task_engine_blob_sha": "experiments/pdmal_pilot/task_engine.py",
    "harness_contract_blob_sha": "experiments/pdmal_pilot/harness_contract.py",
    "topology_utils_blob_sha": "experiments/pdmal_pilot/topology_utils.py",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def is_ancestor(ancestor: str, descendant: str = "HEAD") -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def load_object(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PREFLIGHT_FAIL: invalid or missing {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"PREFLIGHT_FAIL: {label} must be a JSON object")
    return value


def expected_record(contract: dict, candidate_sha: str, candidate_tree_sha: str) -> dict:
    bindings = contract["source_bindings"]
    matrix = contract["matrix"]
    return {
        "record_type": "TRACK_A_EPOCH_001_PRECOLLECTION_PREFLIGHT",
        "schema_version": 1,
        "protocol_id": contract["protocol_id"],
        "candidate_sha": candidate_sha,
        "candidate_tree_sha": candidate_tree_sha,
        "preregistration_merge_sha": bindings["preregistration_merge_sha"],
        "analysis_lock_merge_sha": bindings["analysis_lock_merge_sha"],
        "analysis_blob_sha": bindings["analysis_blob_sha"],
        "analysis_config_sha256": bindings["analysis_config_sha256"],
        "requirements_lock_blob_sha": bindings["requirements_lock_blob_sha"],
        "algorithm_id": contract["algorithm_id"],
        "matrix_cells_per_seed": matrix["cells_per_seed"],
        "expected_observations": matrix["expected_total_observations"],
        "preflight_status": "PASS",
        "scientific_n_increment": 0,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "high_assurance_authorized": False,
    }


def validate_record(record: dict, contract: dict, candidate_sha: str, candidate_tree_sha: str) -> None:
    expected = expected_record(contract, candidate_sha, candidate_tree_sha)
    if record != expected:
        missing = sorted(set(expected) - set(record))
        extra = sorted(set(record) - set(expected))
        mismatched = sorted(k for k in set(expected) & set(record) if expected[k] != record[k])
        raise SystemExit(
            f"PREFLIGHT_FAIL: record mismatch missing={missing} extra={extra} mismatched={mismatched}"
        )
    if not HEX40.fullmatch(record["candidate_sha"]):
        raise SystemExit("PREFLIGHT_FAIL: malformed candidate SHA")
    if not HEX40.fullmatch(record["candidate_tree_sha"]):
        raise SystemExit("PREFLIGHT_FAIL: malformed candidate tree SHA")
    if not HEX64.fullmatch(record["analysis_config_sha256"]):
        raise SystemExit("PREFLIGHT_FAIL: malformed analysis config SHA-256")


def validate_git_bindings(record: dict, contract: dict, expected_candidate_sha: str | None) -> None:
    candidate_sha = record["candidate_sha"]
    candidate_tree = record["candidate_tree_sha"]
    if expected_candidate_sha is not None and candidate_sha != expected_candidate_sha.lower():
        raise SystemExit(
            f"PREFLIGHT_FAIL: candidate must equal exact PR base {expected_candidate_sha}; got {candidate_sha}"
        )
    if git("rev-parse", f"{candidate_sha}^{{tree}}") != candidate_tree:
        raise SystemExit("PREFLIGHT_FAIL: candidate tree does not match Git")
    if not is_ancestor(candidate_sha):
        raise SystemExit("PREFLIGHT_FAIL: candidate is not an ancestor of preflight HEAD")

    bindings = contract["source_bindings"]
    for key, path in SOURCE_PATHS.items():
        actual = git("rev-parse", f"{candidate_sha}:{path}")
        expected = bindings[key]
        if actual != expected:
            raise SystemExit(f"PREFLIGHT_FAIL: candidate source drift {path}: {actual} != {expected}")

    prereg_merge = bindings["preregistration_merge_sha"]
    analysis_merge = bindings["analysis_lock_merge_sha"]
    if not is_ancestor(prereg_merge, candidate_sha):
        raise SystemExit("PREFLIGHT_FAIL: preregistration merge is not in candidate ancestry")
    if not is_ancestor(analysis_merge, candidate_sha):
        raise SystemExit("PREFLIGHT_FAIL: analysis-lock merge is not in candidate ancestry")


def validate_contract_boundary(contract: dict) -> None:
    if contract.get("schema_version") != 2:
        raise SystemExit("PREFLIGHT_FAIL: runner contract schema_version != 2")
    if contract.get("next_gate") != "CANDIDATE_STABILIZATION_AND_PRECOLLECTION_PREFLIGHT":
        raise SystemExit("PREFLIGHT_FAIL: runner contract next gate drift")
    if contract.get("track_a_freeze") != "NOT_ESTABLISHED":
        raise SystemExit("PREFLIGHT_FAIL: runner contract unexpectedly establishes freeze")
    if contract.get("track_a_empirical_execution") != "NOT_AUTHORIZED":
        raise SystemExit("PREFLIGHT_FAIL: runner contract unexpectedly authorizes execution")
    if contract.get("scientific_n_increment") != 0:
        raise SystemExit("PREFLIGHT_FAIL: runner contract increments scientific N")
    if contract.get("authorization", {}).get("collection_authorized") is not False:
        raise SystemExit("PREFLIGHT_FAIL: collection authorization must remain false")


def validate_downstream_absence() -> None:
    present = [str(path.relative_to(ROOT)) for path in DOWNSTREAM if path.exists()]
    if present:
        raise SystemExit(f"PREFLIGHT_FAIL: downstream successor gates must remain absent: {present}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-candidate-sha", default=None)
    args = parser.parse_args(argv)

    contract = load_object(CONTRACT_PATH, "runner contract")
    record = load_object(PREFLIGHT_PATH, "preflight record")
    validate_contract_boundary(contract)

    if args.expected_candidate_sha is not None:
        expected_candidate_sha = args.expected_candidate_sha.lower()
        if not HEX40.fullmatch(expected_candidate_sha):
            raise SystemExit("PREFLIGHT_FAIL: malformed expected candidate SHA")
        try:
            expected_candidate_tree = git("rev-parse", f"{expected_candidate_sha}^{{tree}}")
        except subprocess.CalledProcessError as exc:
            raise SystemExit("PREFLIGHT_FAIL: expected candidate does not resolve in Git") from exc
    else:
        expected_candidate_sha = record.get("candidate_sha", "")
        expected_candidate_tree = record.get("candidate_tree_sha", "")

    validate_record(record, contract, expected_candidate_sha, expected_candidate_tree)
    validate_git_bindings(record, contract, args.expected_candidate_sha)
    validate_downstream_absence()

    print("TRACK_A_EPOCH_001_PRECOLLECTION_PREFLIGHT_PASS_NONAUTHORIZING")
    print(f"CANDIDATE_SHA={record['candidate_sha']}")
    print(f"CANDIDATE_TREE_SHA={record['candidate_tree_sha']}")
    print("TRACK_A_FREEZE=NOT_ESTABLISHED")
    print("TRACK_A_EMPIRICAL_EXECUTION=NOT_AUTHORIZED")
    print("SCIENTIFIC_N_INCREMENT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
