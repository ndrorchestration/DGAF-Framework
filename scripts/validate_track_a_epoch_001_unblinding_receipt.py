#!/usr/bin/env python3
"""Fail-closed validator for the Track A Epoch 001 unblinding receipt."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
EPOCH_ID = "TRACK_A_EPOCH_001"

UNBLIND_AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_UNBLINDING_AUTHORIZATION.json"
UNBLIND_RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_UNBLINDING_RECEIPT.json"
DATASET_RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_COLLECTION_RECEIPT.json"
PREREG_REL = "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json"
ANALYSIS_LOCK_REL = "docs/experiment/TRACK_A_EPOCH_001_ANALYSIS_LOCK.json"
ANALYSIS_REL = "experiments/pdmal_pilot/track_a_epoch_001_analysis.py"
REQUIREMENTS_REL = "experiments/pdmal_pilot/requirements-full-lock.txt"
UNBLIND_RECEIPT_PATH = ROOT / UNBLIND_RECEIPT_REL

UNBLIND_AUTH_COMMIT_SHA = "2e1981870a8455abed36fd72dcb3aaa35e2f9bff"
UNBLIND_AUTH_BLOB_SHA = "1e4d90181ca39b199baaa32f6487f679f6bf0e6e"
DATASET_LOCK_COMMIT_SHA = "fbf3e2da3be0a36c1102a69c996026e95c33cceb"
DATASET_LOCK_BLOB_SHA = "eb6b9325058fb104da85f8de6c26f2b2a748a1a9"
PREREG_BLOB_SHA = "52148950ff054a407c2e6b5cf36103695cf96474"
ANALYSIS_LOCK_BLOB_SHA = "ff9a37a0be7a75912dbe0ae34dd95893d41efafb"
ANALYSIS_BLOB_SHA = "76bc8e9604c5d7e039e324e73036f353dc8ea31f"
REQUIREMENTS_BLOB_SHA = "00c1f779e97030f9b25ae494642edb31b5b09de5"

COLLECTION_RUN_ID = 34262408225
PROTECTED_ARTIFACT_ID = 10070587302
PROTECTED_ARTIFACT_SHA256 = "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f"
PROTECTED_CIPHERTEXT_SHA256 = "15ba9d630cea0c26baca3ab50c33f7bcf10681a24293350b12acf3d4aeac4614"
PROTECTED_PLAINTEXT_TAR_SHA256 = "ec51a5451b63c5cbccfd83d01290f939d7a1832181af190c5fabd31fa806eb35"
CUSTODY_CERT_SHA256 = "cfa468d1091f2179cfe0c96ff000bfe45ae7c5bd1414146fbb99c77572dba707"
CUSTODY_PUBLIC_KEY_SHA256 = "5df195dec6352226cdf891ba3dcd35b1d5c89e6e5b2cc309bcde710f8fd7e5ee"
PRIVATE_KEY_PUBLIC_KEY_SHA256 = CUSTODY_PUBLIC_KEY_SHA256
MAPPING_SET_MANIFEST_SHA256 = "1995432b772309aa0b0b7d29b79287568e7fa3e38313de98a6f0068c38125ff2"
CUSTODY_RECORD_SHA256 = "7b492762a514d60d55ef0af2a83be72bd00f9c329c5c751893f7baa7eca60928"
MAPPING_MANIFEST_METHOD = "SHA256_OF_LF_JOINED_SORTED_SHA256_DOUBLESPACE_FILENAME_LINES_V1"
REGISTERED_TOPOLOGIES = ["complete", "pdmal", "random_regular", "ring", "small_world"]


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
    return subprocess.run(
        ["git", "cat-file", "-e", spec],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot load {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one JSON object")
    return value


def require_blob(head: str, rel: str, expected: str) -> None:
    if not git_object_exists(f"{head}:{rel}"):
        raise SystemExit(f"required source missing: {rel}")
    actual = git("rev-parse", f"{head}:{rel}")
    if actual != expected:
        raise SystemExit(f"required source drift: {rel}: {actual} != {expected}")


def validate_locked_preconditions(head: str) -> None:
    if not git_is_ancestor(UNBLIND_AUTH_COMMIT_SHA, head):
        raise SystemExit("unblinding receipt prohibited: authorization commit is not an ancestor")
    if not git_is_ancestor(DATASET_LOCK_COMMIT_SHA, head):
        raise SystemExit("unblinding receipt prohibited: dataset-lock commit is not an ancestor")

    require_blob(head, UNBLIND_AUTH_REL, UNBLIND_AUTH_BLOB_SHA)
    require_blob(head, DATASET_RECEIPT_REL, DATASET_LOCK_BLOB_SHA)
    require_blob(head, PREREG_REL, PREREG_BLOB_SHA)
    require_blob(head, ANALYSIS_LOCK_REL, ANALYSIS_LOCK_BLOB_SHA)
    require_blob(head, ANALYSIS_REL, ANALYSIS_BLOB_SHA)
    require_blob(head, REQUIREMENTS_REL, REQUIREMENTS_BLOB_SHA)

    auth_history = [x for x in git("log", "--format=%H", head, "--", UNBLIND_AUTH_REL).splitlines() if x]
    if auth_history != [UNBLIND_AUTH_COMMIT_SHA]:
        raise SystemExit(f"unblinding receipt prohibited: authorization history drift: {auth_history}")
    dataset_history = [x for x in git("log", "--format=%H", head, "--", DATASET_RECEIPT_REL).splitlines() if x]
    if dataset_history != [DATASET_LOCK_COMMIT_SHA]:
        raise SystemExit(f"unblinding receipt prohibited: dataset-lock history drift: {dataset_history}")

    auth = load_json(ROOT / UNBLIND_AUTH_REL)
    required_auth = {
        "record_type": "TRACK_A_EPOCH_001_UNBLINDING_AUTHORIZATION",
        "protocol_id": PROTOCOL_ID,
        "epoch_id": EPOCH_ID,
        "authorization_status": "AUTHORIZED",
        "authorization_scope": "TRACK_A_EPOCH_001_MAPPING_RELEASE_ONLY",
        "authorization_class": "HUMAN_REPOSITORY_OWNER_SAME_SYSTEM_NONINDEPENDENT",
        "independent_authorization": False,
        "key_release_authorized": True,
        "protected_artifact_decryption_authorized": True,
        "unblinding_authorized": True,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "outcome_aggregation_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "additional_scientific_n_increment": 0,
        "high_assurance_authorized": False,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    for key, expected in required_auth.items():
        if auth.get(key) != expected:
            raise SystemExit(f"unblinding receipt prohibited: authorization field {key!r} drift")

    paths = git("ls-tree", "-r", "--name-only", head).splitlines()
    forbidden_private_key_paths = [p for p in paths if "unblinding_private_key" in p.lower() or p.lower().endswith("private_key.pem")]
    if forbidden_private_key_paths:
        raise SystemExit(f"private key path must never be committed: {forbidden_private_key_paths}")


def expected_receipt(parent_sha: str) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_001_UNBLINDING_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch_id": EPOCH_ID,
        "receipt_parent_sha": parent_sha,
        "unblinding_authorization_commit_sha": UNBLIND_AUTH_COMMIT_SHA,
        "unblinding_authorization_blob_sha": UNBLIND_AUTH_BLOB_SHA,
        "dataset_lock_commit_sha": DATASET_LOCK_COMMIT_SHA,
        "dataset_lock_blob_sha": DATASET_LOCK_BLOB_SHA,
        "preregistration_blob_sha": PREREG_BLOB_SHA,
        "analysis_lock_blob_sha": ANALYSIS_LOCK_BLOB_SHA,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "requirements_lock_blob_sha": REQUIREMENTS_BLOB_SHA,
        "collection_run_id": COLLECTION_RUN_ID,
        "protected_artifact_id": PROTECTED_ARTIFACT_ID,
        "protected_artifact_archive_sha256": PROTECTED_ARTIFACT_SHA256,
        "protected_ciphertext_sha256": PROTECTED_CIPHERTEXT_SHA256,
        "protected_plaintext_tar_sha256": PROTECTED_PLAINTEXT_TAR_SHA256,
        "custody_certificate_sha256": CUSTODY_CERT_SHA256,
        "private_key_public_key_sha256": PRIVATE_KEY_PUBLIC_KEY_SHA256,
        "custody_certificate_public_key_sha256": CUSTODY_PUBLIC_KEY_SHA256,
        "mapping_set_manifest_method": MAPPING_MANIFEST_METHOD,
        "mapping_set_manifest_sha256": MAPPING_SET_MANIFEST_SHA256,
        "protected_custody_record_sha256": CUSTODY_RECORD_SHA256,
        "verification_class": "DEVELOPER_SAME_SYSTEM_NONINDEPENDENT",
        "decryption_status": "COMPLETE_VERIFIED",
        "mapping_file_count": 50,
        "mapping_sidecar_count": 50,
        "mapping_seed_first": 20270101,
        "mapping_seed_last": 20270150,
        "mapping_record_type": "TRACK_A_EPOCH_001_PROTECTED_TOPOLOGY_MAPPING",
        "mapping_schema_version": 2,
        "registered_topologies": REGISTERED_TOPOLOGIES,
        "mapping_sidecar_qc": "PASS",
        "mapping_bijection_qc": "PASS",
        "registered_topology_set_qc": "PASS",
        "public_dataset_topology_absence_flag_qc": "PASS",
        "protected_custody_class": "PROTECTED_SAME_SYSTEM_NONINDEPENDENT",
        "private_key_published": False,
        "mapping_values_published": False,
        "unblinding_complete": True,
        "outcome_mapping_join_performed": False,
        "outcome_values_inspected_for_unblinding_receipt": False,
        "outcome_aggregation_performed": False,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "additional_scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance_authorized": False,
    }


def validate_repository(*, expect_absent: bool) -> None:
    head = git("rev-parse", "HEAD")
    validate_locked_preconditions(head)

    if expect_absent:
        if UNBLIND_RECEIPT_PATH.exists():
            raise SystemExit("tooling mode requires unblinding receipt to remain absent")
        print("TRACK_A_EPOCH_001_UNBLINDING_RECEIPT_TOOLING_PASS")
        print("TRACK_A_UNBLINDING_AUTHORIZATION=ESTABLISHED")
        print("TRACK_A_UNBLINDING_EXECUTION=LOCAL_VERIFIED_NONINDEPENDENT_NOT_RECORDED")
        print("PRIMARY_ANALYSIS=NOT_AUTHORIZED")
        return

    if not UNBLIND_RECEIPT_PATH.exists():
        raise SystemExit("unblinding receipt is missing")

    parents = git("rev-list", "--parents", "-n", "1", head).split()
    if len(parents) != 2:
        raise SystemExit("unblinding receipt head must have exactly one parent")
    parent = parents[1]

    changed = sorted(
        x for x in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines() if x
    )
    if changed != [UNBLIND_RECEIPT_REL]:
        raise SystemExit(f"unblinding receipt head must change only {UNBLIND_RECEIPT_REL}; got {changed}")
    if git_object_exists(f"{parent}:{UNBLIND_RECEIPT_REL}"):
        raise SystemExit("unblinding receipt path unexpectedly existed at parent")

    history = [x for x in git("log", "--format=%H", "--", UNBLIND_RECEIPT_REL).splitlines() if x]
    if history != [head]:
        raise SystemExit(f"unblinding receipt must have exactly one history commit at HEAD; got {history}")

    actual = load_json(UNBLIND_RECEIPT_PATH)
    expected = expected_receipt(parent)
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        mismatched = sorted(k for k in set(actual) & set(expected) if actual[k] != expected[k])
        raise SystemExit(
            f"unblinding receipt mismatch: missing={missing} extra={extra} mismatched={mismatched}"
        )

    print("TRACK_A_EPOCH_001_UNBLINDING_RECEIPT_EVENT_SHAPE_PASS")
    print("TRACK_A_UNBLINDING_EXECUTION=PENDING_VALIDATED_RECEIPT_MERGE")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED")
    print("PRIMARY_ANALYSIS_RUN=FALSE")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-absent", action="store_true")
    args = parser.parse_args()
    validate_repository(expect_absent=args.expect_absent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
