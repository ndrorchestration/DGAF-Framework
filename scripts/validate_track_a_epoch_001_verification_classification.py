#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFICATION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_VERIFICATION_CLASSIFICATION.json"
CLOSURE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_FINAL_CLOSURE_PACKET.json"
FREEZE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_MANIFEST.json"
AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION.json"
VERIFICATION_PATH = ROOT / VERIFICATION_REL
CLOSURE_PATH = ROOT / CLOSURE_REL
FREEZE_PATH = ROOT / FREEZE_REL
AUTH_PATH = ROOT / AUTH_REL

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
FROZEN_CANDIDATE_SHA = "961b9918002c4c68afac9c0fd5dd3e352e49b926"
FROZEN_CANDIDATE_TREE_SHA = "f20fa0ffee4b47872d84ce10cc9fd05e75c7306d"
FREEZE_MANIFEST_BLOB_SHA = "ae15c6282351c01bd13ace2423d273ba0dde8348"
CLOSURE_PACKET_BLOB_SHA = "c32d89385c29c9e5cd0a706630c1955fb3f5f1c8"

EXPECTED_PROTECTED_SOURCE_BLOBS = {
    "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json": "52148950ff054a407c2e6b5cf36103695cf96474",
    "docs/experiment/TRACK_A_EPOCH_001_ANALYSIS_LOCK.json": "ff9a37a0be7a75912dbe0ae34dd95893d41efafb",
    "experiments/pdmal_pilot/track_a_epoch_001_analysis.py": "76bc8e9604c5d7e039e324e73036f353dc8ea31f",
    "experiments/pdmal_pilot/requirements-full-lock.txt": "00c1f779e97030f9b25ae494642edb31b5b09de5",
    "experiments/pdmal_pilot/task_engine.py": "90135e1c6dfccc3b56ffdc0dcb9eb50a0b2a5b05",
    "experiments/pdmal_pilot/harness_contract.py": "bb97c54ddf087fef568b1b3c8f8df72c30dad11e",
    "experiments/pdmal_pilot/topology_utils.py": "7ae92ba8a9ab964537e5dafa5e12de36b841391e",
    "experiments/pdmal_pilot/run_track_a_epoch_001.py": "d8ef6f31f49da82e4eaf5295bad024c3194f6d15",
}

EXPECTED_FREEZE = {
    "record_type": "TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_MANIFEST",
    "schema_version": 1,
    "protocol_id": PROTOCOL_ID,
    "frozen_candidate_sha": FROZEN_CANDIDATE_SHA,
    "frozen_candidate_tree_sha": FROZEN_CANDIDATE_TREE_SHA,
    "preflight_blob_sha": "148cbd0e0717ca62efadfcce9227965abd838468",
    "protected_source_blobs": EXPECTED_PROTECTED_SOURCE_BLOBS,
    "freeze_status": "ESTABLISHED",
    "scientific_n_increment": 0,
    "collection_authorized": False,
    "unblinding_authorized": False,
    "high_assurance_authorized": False,
}

EXPECTED_CLOSURE = {
    "record_type": "TRACK_A_EPOCH_001_FINAL_CLOSURE_PACKET",
    "schema_version": 1,
    "protocol_id": PROTOCOL_ID,
    "frozen_candidate_sha": FROZEN_CANDIDATE_SHA,
    "freeze_manifest_blob_sha": FREEZE_MANIFEST_BLOB_SHA,
    "open_blockers": [],
    "closure_status": "CLOSED_VERIFIED_FOR_AUTHORIZATION_REVIEW",
    "scientific_n_increment": 0,
    "collection_authorized": False,
    "unblinding_authorized": False,
    "high_assurance_authorized": False,
}

EXPECTED_VERIFICATION = {
    "record_type": "TRACK_A_EPOCH_001_VERIFICATION_CLASSIFICATION",
    "schema_version": 1,
    "protocol_id": PROTOCOL_ID,
    "frozen_candidate_sha": FROZEN_CANDIDATE_SHA,
    "closure_packet_blob_sha": CLOSURE_PACKET_BLOB_SHA,
    "verification_status": "PASS",
    "verification_class": "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT",
    "independent_verification": False,
    "same_system_custody": True,
    "scientific_n_increment": 0,
    "collection_authorized": False,
    "unblinding_authorized": False,
    "high_assurance_authorized": False,
}


def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False
    )
    if check and proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def git_object_exists(spec: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", spec], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
    ).returncode == 0


def git_blob(rev: str, path: str) -> str:
    return git("rev-parse", f"{rev}:{path}")


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot load {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one JSON object")
    return data


def require_exact_object(actual: dict, expected: dict, label: str) -> None:
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        mismatched = sorted(k for k in set(actual) & set(expected) if actual[k] != expected[k])
        raise SystemExit(
            f"{label} mismatch: missing={missing} extra={extra} mismatched={mismatched}"
        )


def validate_verification_record(data: dict) -> None:
    require_exact_object(data, EXPECTED_VERIFICATION, "verification classification")


def validate_chain(head: str) -> None:
    if git("rev-parse", f"{FROZEN_CANDIDATE_SHA}^{{tree}}") != FROZEN_CANDIDATE_TREE_SHA:
        raise SystemExit("frozen candidate tree drift")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", FROZEN_CANDIDATE_SHA, head],
        cwd=ROOT, check=False
    ).returncode != 0:
        raise SystemExit("frozen candidate is not an ancestor of verification head")

    if git_blob(head, FREEZE_REL) != FREEZE_MANIFEST_BLOB_SHA:
        raise SystemExit("freeze manifest blob drift")
    require_exact_object(load_json(FREEZE_PATH), EXPECTED_FREEZE, "freeze manifest")
    freeze_history = [x for x in git("log", "--format=%H", "--", FREEZE_REL).splitlines() if x]
    if len(freeze_history) != 1:
        raise SystemExit(f"freeze manifest history drift: {freeze_history}")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", freeze_history[0], head],
        cwd=ROOT, check=False
    ).returncode != 0:
        raise SystemExit("freeze commit is not an ancestor of verification head")

    if git_blob(head, CLOSURE_REL) != CLOSURE_PACKET_BLOB_SHA:
        raise SystemExit("closure packet blob drift")
    require_exact_object(load_json(CLOSURE_PATH), EXPECTED_CLOSURE, "closure packet")
    closure_history = [x for x in git("log", "--format=%H", "--", CLOSURE_REL).splitlines() if x]
    if len(closure_history) != 1:
        raise SystemExit(f"closure packet history drift: {closure_history}")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", closure_history[0], head],
        cwd=ROOT, check=False
    ).returncode != 0:
        raise SystemExit("closure commit is not an ancestor of verification head")

    for path, wanted in EXPECTED_PROTECTED_SOURCE_BLOBS.items():
        if git_blob(FROZEN_CANDIDATE_SHA, path) != wanted:
            raise SystemExit(f"candidate protected source drift: {path}")
        if git_blob(head, path) != wanted:
            raise SystemExit(f"current protected source drift: {path}")

    if AUTH_PATH.exists():
        raise SystemExit("collection authorization must remain absent")


def validate_repository(*, expect_absent: bool) -> None:
    head = git("rev-parse", "HEAD")
    validate_chain(head)

    if expect_absent:
        if VERIFICATION_PATH.exists():
            raise SystemExit("tooling mode requires verification classification to remain absent")
        print("TRACK_A_EPOCH_001_VERIFICATION_TOOLING_PASS_NONAUTHORIZING")
        print("TRACK_A_VERIFICATION=NOT_ESTABLISHED")
        print("TRACK_A_EMPIRICAL_EXECUTION=NOT_AUTHORIZED")
        print("SCIENTIFIC_N_INCREMENT=0")
        return

    if not VERIFICATION_PATH.exists():
        raise SystemExit("verification classification is missing")
    validate_verification_record(load_json(VERIFICATION_PATH))

    parents = git("rev-list", "--parents", "-n", "1", head).split()
    if len(parents) != 2:
        raise SystemExit("verification head must have exactly one parent")
    parent = parents[1]
    changed = sorted(
        x for x in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines() if x
    )
    if changed != [VERIFICATION_REL]:
        raise SystemExit(f"verification head must change only {VERIFICATION_REL}; got {changed}")
    if git_object_exists(f"{parent}:{VERIFICATION_REL}"):
        raise SystemExit("verification path unexpectedly existed at parent")
    history = [x for x in git("log", "--format=%H", "--", VERIFICATION_REL).splitlines() if x]
    if history != [head]:
        raise SystemExit(f"verification path must have exactly one history commit at HEAD; got {history}")

    data = load_json(VERIFICATION_PATH)
    if data["independent_verification"] is not False:
        raise SystemExit("same-system verification cannot claim independence")
    if data["same_system_custody"] is not True:
        raise SystemExit("same-system custody must be explicit")
    if data["verification_class"] != "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT":
        raise SystemExit("verification class exceeds supported evidence")

    print("TRACK_A_EPOCH_001_VERIFICATION_EVENT_PASS_NONAUTHORIZING")
    print("TRACK_A_VERIFICATION=PASS_DEVELOPER_SELF_ATTESTED_NONINDEPENDENT")
    print("TRACK_A_EMPIRICAL_EXECUTION=NOT_AUTHORIZED")
    print("SCIENTIFIC_N_INCREMENT=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-absent", action="store_true")
    args = parser.parse_args()
    validate_repository(expect_absent=args.expect_absent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
