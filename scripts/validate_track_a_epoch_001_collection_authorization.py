#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_PRECOLLECTION_PREFLIGHT.json"
)
FREEZE_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_MANIFEST.json"
)
CLOSURE_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_FINAL_CLOSURE_PACKET.json"
)
VERIFICATION_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_VERIFICATION_CLASSIFICATION.json"
)
AUTH_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION.json"
)

PREFLIGHT_PATH = ROOT / PREFLIGHT_REL
FREEZE_PATH = ROOT / FREEZE_REL
CLOSURE_PATH = ROOT / CLOSURE_REL
VERIFICATION_PATH = ROOT / VERIFICATION_REL
AUTH_PATH = ROOT / AUTH_REL

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
EPOCH_ID = "TRACK_A_EPOCH_001"
ALGORITHM_ID = "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
FROZEN_CANDIDATE_SHA = "961b9918002c4c68afac9c0fd5dd3e352e49b926"
FROZEN_CANDIDATE_TREE_SHA = "f20fa0ffee4b47872d84ce10cc9fd05e75c7306d"
PREFLIGHT_BLOB_SHA = "148cbd0e0717ca62efadfcce9227965abd838468"
FREEZE_MANIFEST_BLOB_SHA = "ae15c6282351c01bd13ace2423d273ba0dde8348"
CLOSURE_PACKET_BLOB_SHA = "c32d89385c29c9e5cd0a706630c1955fb3f5f1c8"
VERIFICATION_BLOB_SHA = "c67d09052faa7ae50de6eca57691ed50d906a951"
PREREG_MERGE_SHA = "26077b27ca336454148006e6daf4cd087005b421"
ANALYSIS_LOCK_MERGE_SHA = "e9ea59ad839aef33fbce10ed04c2157358c4326d"
ANALYSIS_BLOB_SHA = "76bc8e9604c5d7e039e324e73036f353dc8ea31f"
ANALYSIS_CONFIG_SHA256 = (
    "355b164f69e91405819f092d0721b7597b87b06de79394a0c451169410a5ab6d"
)
REQUIREMENTS_LOCK_BLOB_SHA = "00c1f779e97030f9b25ae494642edb31b5b09de5"

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

EXPECTED_PREFLIGHT = {
    "record_type": "TRACK_A_EPOCH_001_PRECOLLECTION_PREFLIGHT",
    "schema_version": 1,
    "protocol_id": PROTOCOL_ID,
    "candidate_sha": FROZEN_CANDIDATE_SHA,
    "candidate_tree_sha": FROZEN_CANDIDATE_TREE_SHA,
    "preregistration_merge_sha": PREREG_MERGE_SHA,
    "analysis_lock_merge_sha": ANALYSIS_LOCK_MERGE_SHA,
    "analysis_blob_sha": ANALYSIS_BLOB_SHA,
    "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
    "requirements_lock_blob_sha": REQUIREMENTS_LOCK_BLOB_SHA,
    "algorithm_id": ALGORITHM_ID,
    "matrix_cells_per_seed": 45,
    "expected_observations": 2250,
    "preflight_status": "PASS",
    "scientific_n_increment": 0,
    "collection_authorized": False,
    "unblinding_authorized": False,
    "high_assurance_authorized": False,
}

EXPECTED_FREEZE = {
    "record_type": "TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_MANIFEST",
    "schema_version": 1,
    "protocol_id": PROTOCOL_ID,
    "frozen_candidate_sha": FROZEN_CANDIDATE_SHA,
    "frozen_candidate_tree_sha": FROZEN_CANDIDATE_TREE_SHA,
    "preflight_blob_sha": PREFLIGHT_BLOB_SHA,
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
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def git_object_exists(spec: str) -> bool:
    return (
        subprocess.run(
            ["git", "cat-file", "-e", spec],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def git_blob(rev: str, path: str) -> str:
    return git("rev-parse", f"{rev}:{path}")


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


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
        mismatched = sorted(
            key for key in set(actual) & set(expected) if actual[key] != expected[key]
        )
        raise SystemExit(
            f"{label} mismatch: missing={missing} extra={extra} mismatched={mismatched}"
        )


def expected_authorization(authorization_parent_sha: str) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION",
        "schema_version": 2,
        "protocol_id": PROTOCOL_ID,
        "epoch_id": EPOCH_ID,
        "authorization_parent_sha": authorization_parent_sha,
        "frozen_candidate_sha": FROZEN_CANDIDATE_SHA,
        "frozen_candidate_tree_sha": FROZEN_CANDIDATE_TREE_SHA,
        "preflight_blob_sha": PREFLIGHT_BLOB_SHA,
        "freeze_manifest_blob_sha": FREEZE_MANIFEST_BLOB_SHA,
        "closure_packet_blob_sha": CLOSURE_PACKET_BLOB_SHA,
        "verification_classification_blob_sha": VERIFICATION_BLOB_SHA,
        "preregistration_merge_sha": PREREG_MERGE_SHA,
        "analysis_lock_merge_sha": ANALYSIS_LOCK_MERGE_SHA,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
        "requirements_lock_blob_sha": REQUIREMENTS_LOCK_BLOB_SHA,
        "algorithm_id": ALGORITHM_ID,
        "seed_start": 20270101,
        "seed_end": 20270150,
        "seed_count": 50,
        "expected_observations": 2250,
        "authorize_empirical_collection": True,
        "authorize_unblinding": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
    }


def validate_authorization_record(data: dict, authorization_parent_sha: str) -> None:
    require_exact_object(
        data,
        expected_authorization(authorization_parent_sha),
        "collection authorization",
    )


def validate_gate(
    *,
    head: str,
    path: str,
    local_path: Path,
    wanted_blob: str,
    expected: dict,
    label: str,
) -> str:
    actual_blob = git_blob(head, path)
    if actual_blob != wanted_blob:
        raise SystemExit(f"{label} blob drift: {actual_blob} != {wanted_blob}")
    require_exact_object(load_json(local_path), expected, label)
    history = [x for x in git("log", "--format=%H", "--", path).splitlines() if x]
    if len(history) != 1:
        raise SystemExit(f"{label} must have exactly one immutable history commit: {history}")
    if not git_is_ancestor(history[0], head):
        raise SystemExit(f"{label} commit is not an ancestor of authorization head")
    return history[0]


def validate_prerequisite_chain(head: str) -> None:
    if git("rev-parse", f"{FROZEN_CANDIDATE_SHA}^{{tree}}") != FROZEN_CANDIDATE_TREE_SHA:
        raise SystemExit("frozen candidate tree drift")
    if not git_is_ancestor(FROZEN_CANDIDATE_SHA, head):
        raise SystemExit("frozen candidate is not an ancestor of authorization head")

    preflight_commit = validate_gate(
        head=head,
        path=PREFLIGHT_REL,
        local_path=PREFLIGHT_PATH,
        wanted_blob=PREFLIGHT_BLOB_SHA,
        expected=EXPECTED_PREFLIGHT,
        label="preflight",
    )
    freeze_commit = validate_gate(
        head=head,
        path=FREEZE_REL,
        local_path=FREEZE_PATH,
        wanted_blob=FREEZE_MANIFEST_BLOB_SHA,
        expected=EXPECTED_FREEZE,
        label="freeze manifest",
    )
    closure_commit = validate_gate(
        head=head,
        path=CLOSURE_REL,
        local_path=CLOSURE_PATH,
        wanted_blob=CLOSURE_PACKET_BLOB_SHA,
        expected=EXPECTED_CLOSURE,
        label="closure packet",
    )
    verification_commit = validate_gate(
        head=head,
        path=VERIFICATION_REL,
        local_path=VERIFICATION_PATH,
        wanted_blob=VERIFICATION_BLOB_SHA,
        expected=EXPECTED_VERIFICATION,
        label="verification classification",
    )

    chain = (
        (FROZEN_CANDIDATE_SHA, preflight_commit, "candidate->preflight"),
        (preflight_commit, freeze_commit, "preflight->freeze"),
        (freeze_commit, closure_commit, "freeze->closure"),
        (closure_commit, verification_commit, "closure->verification"),
        (verification_commit, head, "verification->authorization-head"),
    )
    for ancestor, descendant, label in chain:
        if ancestor == descendant or not git_is_ancestor(ancestor, descendant):
            raise SystemExit(f"successor gate ordering violated: {label}")

    for path, wanted in EXPECTED_PROTECTED_SOURCE_BLOBS.items():
        if git_blob(FROZEN_CANDIDATE_SHA, path) != wanted:
            raise SystemExit(f"candidate protected source drift: {path}")
        if git_blob(head, path) != wanted:
            raise SystemExit(f"current protected source drift: {path}")


def validate_repository(*, expect_absent: bool) -> None:
    head = git("rev-parse", "HEAD")
    validate_prerequisite_chain(head)

    if expect_absent:
        if AUTH_PATH.exists():
            raise SystemExit("tooling mode requires collection authorization to remain absent")
        print("TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION_TOOLING_PASS")
        print("TRACK_A_EMPIRICAL_EXECUTION=NOT_AUTHORIZED")
        print("SCIENTIFIC_N_INCREMENT=0")
        return

    if not AUTH_PATH.exists():
        raise SystemExit("collection authorization is missing")

    parents = git("rev-list", "--parents", "-n", "1", head).split()
    if len(parents) != 2:
        raise SystemExit("authorization head must have exactly one parent")
    parent = parents[1]

    changed = sorted(
        x
        for x in git(
            "diff-tree", "--no-commit-id", "--name-only", "-r", head
        ).splitlines()
        if x
    )
    if changed != [AUTH_REL]:
        raise SystemExit(f"authorization head must change only {AUTH_REL}; got {changed}")
    if git_object_exists(f"{parent}:{AUTH_REL}"):
        raise SystemExit("authorization path unexpectedly existed at parent")

    history = [x for x in git("log", "--format=%H", "--", AUTH_REL).splitlines() if x]
    if history != [head]:
        raise SystemExit(
            f"authorization path must have exactly one history commit at HEAD; got {history}"
        )

    validate_authorization_record(load_json(AUTH_PATH), parent)

    print("TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION_EVENT_SHAPE_PASS")
    print("TRACK_A_COLLECTION_AUTHORIZATION=PENDING_VALIDATED_MERGE")
    print("TRACK_A_EMPIRICAL_EXECUTION=NOT_AUTHORIZED_ON_PR_HEAD")
    print("SCIENTIFIC_N_INCREMENT=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-absent", action="store_true")
    args = parser.parse_args()
    validate_repository(expect_absent=args.expect_absent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
