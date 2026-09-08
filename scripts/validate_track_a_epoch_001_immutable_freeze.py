#!/usr/bin/env python3
"""Fail-closed validator for the Track A Epoch 001 immutable-freeze event.

Tooling mode proves the freeze remains absent. Freeze mode validates a future
one-file freeze commit against the already-merged runner predicate.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_MANIFEST.json"
PREFLIGHT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_PRECOLLECTION_PREFLIGHT.json"
CLOSURE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_FINAL_CLOSURE_PACKET.json"
VERIFICATION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_VERIFICATION_CLASSIFICATION.json"
AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION.json"
FREEZE_PATH = ROOT / FREEZE_REL

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
CANDIDATE_SHA = "961b9918002c4c68afac9c0fd5dd3e352e49b926"
CANDIDATE_TREE_SHA = "f20fa0ffee4b47872d84ce10cc9fd05e75c7306d"
PREFLIGHT_BLOB_SHA = "148cbd0e0717ca62efadfcce9227965abd838468"
PROTECTED_SOURCE_BLOBS = {
    "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json": "52148950ff054a407c2e6b5cf36103695cf96474",
    "docs/experiment/TRACK_A_EPOCH_001_ANALYSIS_LOCK.json": "ff9a37a0be7a75912dbe0ae34dd95893d41efafb",
    "experiments/pdmal_pilot/track_a_epoch_001_analysis.py": "76bc8e9604c5d7e039e324e73036f353dc8ea31f",
    "experiments/pdmal_pilot/requirements-full-lock.txt": "00c1f779e97030f9b25ae494642edb31b5b09de5",
    "experiments/pdmal_pilot/task_engine.py": "90135e1c6dfccc3b56ffdc0dcb9eb50a0b2a5b05",
    "experiments/pdmal_pilot/harness_contract.py": "bb97c54ddf087fef568b1b3c8f8df72c30dad11e",
    "experiments/pdmal_pilot/topology_utils.py": "7ae92ba8a9ab964537e5dafa5e12de36b841391e",
    "experiments/pdmal_pilot/run_track_a_epoch_001.py": "d8ef6f31f49da82e4eaf5295bad024c3194f6d15",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def path_history(path: str, revision: str = "HEAD") -> tuple[str, ...]:
    output = git("log", "--format=%H", revision, "--", path)
    return tuple(line for line in output.splitlines() if line)


def expected_freeze() -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_MANIFEST",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "frozen_candidate_sha": CANDIDATE_SHA,
        "frozen_candidate_tree_sha": CANDIDATE_TREE_SHA,
        "preflight_blob_sha": PREFLIGHT_BLOB_SHA,
        "protected_source_blobs": PROTECTED_SOURCE_BLOBS,
        "freeze_status": "ESTABLISHED",
        "scientific_n_increment": 0,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "high_assurance_authorized": False,
    }


def require_exact_record(data: dict) -> None:
    expected = expected_freeze()
    if data != expected:
        missing = sorted(set(expected) - set(data))
        extra = sorted(set(data) - set(expected))
        mismatched = sorted(k for k in set(expected) & set(data) if data[k] != expected[k])
        raise SystemExit(
            "FREEZE_FAIL: manifest mismatch "
            f"missing={missing} extra={extra} mismatched={mismatched}"
        )


def validate_common_prerequisites() -> None:
    if git("rev-parse", f"{CANDIDATE_SHA}^{{tree}}") != CANDIDATE_TREE_SHA:
        raise SystemExit("FREEZE_FAIL: stabilized candidate tree drift")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", CANDIDATE_SHA, "HEAD"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode != 0:
        raise SystemExit("FREEZE_FAIL: stabilized candidate is not an ancestor of HEAD")

    preflight_actual = git("rev-parse", f"HEAD:{PREFLIGHT_REL}")
    if preflight_actual != PREFLIGHT_BLOB_SHA:
        raise SystemExit(
            f"FREEZE_FAIL: preflight blob drift {preflight_actual} != {PREFLIGHT_BLOB_SHA}"
        )
    history = path_history(PREFLIGHT_REL)
    if len(history) != 1:
        raise SystemExit(f"FREEZE_FAIL: preflight history must be immutable; history={list(history)}")

    for path, expected in PROTECTED_SOURCE_BLOBS.items():
        candidate_blob = git("rev-parse", f"{CANDIDATE_SHA}:{path}")
        current_blob = git("rev-parse", f"HEAD:{path}")
        if candidate_blob != expected or current_blob != expected:
            raise SystemExit(
                f"FREEZE_FAIL: protected source drift {path}: "
                f"candidate={candidate_blob} current={current_blob} expected={expected}"
            )

    downstream = [p for p in (CLOSURE_REL, VERIFICATION_REL, AUTH_REL) if (ROOT / p).exists()]
    if downstream:
        raise SystemExit(f"FREEZE_FAIL: downstream gates must remain absent: {downstream}")


def validate_tooling_only() -> None:
    validate_common_prerequisites()
    if FREEZE_PATH.exists():
        raise SystemExit("FREEZE_FAIL: tooling-only validation requires freeze manifest absent")
    print("TRACK_A_EPOCH_001_FREEZE_TOOLING_PASS_FREEZE_ABSENT")
    print("TRACK_A_FREEZE=NOT_ESTABLISHED")
    print("TRACK_A_EMPIRICAL_EXECUTION=NOT_AUTHORIZED")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_freeze_event() -> None:
    validate_common_prerequisites()
    if not FREEZE_PATH.exists():
        raise SystemExit("FREEZE_FAIL: freeze manifest absent")
    try:
        data = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FREEZE_FAIL: invalid freeze manifest: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("FREEZE_FAIL: freeze manifest must be a JSON object")
    require_exact_record(data)

    parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()[1:]
    if len(parents) != 1:
        raise SystemExit(f"FREEZE_FAIL: freeze head must have exactly one parent; parents={parents}")
    parent = parents[0]
    changed = tuple(
        line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines() if line
    )
    if changed != (FREEZE_REL,):
        raise SystemExit(f"FREEZE_FAIL: freeze commit must change exactly one file; changed={changed}")
    if subprocess.run(
        ["git", "cat-file", "-e", f"{parent}:{FREEZE_REL}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0:
        raise SystemExit("FREEZE_FAIL: freeze manifest already existed at parent")
    history = path_history(FREEZE_REL)
    if len(history) != 1 or history[0] != git("rev-parse", "HEAD"):
        raise SystemExit(f"FREEZE_FAIL: freeze path must have exactly one history commit; history={list(history)}")

    print("TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_PASS_NONAUTHORIZING")
    print(f"FROZEN_CANDIDATE_SHA={CANDIDATE_SHA}")
    print("TRACK_A_FREEZE=ESTABLISHED")
    print("TRACK_A_EMPIRICAL_EXECUTION=NOT_AUTHORIZED")
    print("SCIENTIFIC_N_INCREMENT=0")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-absent", action="store_true")
    args = parser.parse_args(argv)
    if args.expect_absent:
        validate_tooling_only()
    else:
        validate_freeze_event()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
