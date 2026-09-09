#!/usr/bin/env python3
"""Fail-closed validator for Track A Epoch 001 unblinding authorization."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
EPOCH_ID = "TRACK_A_EPOCH_001"

RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_COLLECTION_RECEIPT.json"
AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_UNBLINDING_AUTHORIZATION.json"
PREREG_REL = "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json"
ANALYSIS_LOCK_REL = "docs/experiment/TRACK_A_EPOCH_001_ANALYSIS_LOCK.json"
ANALYSIS_REL = "experiments/pdmal_pilot/track_a_epoch_001_analysis.py"
REQUIREMENTS_REL = "experiments/pdmal_pilot/requirements-full-lock.txt"
AUTH_PATH = ROOT / AUTH_REL

DATASET_LOCK_COMMIT_SHA = "fbf3e2da3be0a36c1102a69c996026e95c33cceb"
DATASET_LOCK_BLOB_SHA = "eb6b9325058fb104da85f8de6c26f2b2a748a1a9"
PREREG_BLOB_SHA = "52148950ff054a407c2e6b5cf36103695cf96474"
ANALYSIS_LOCK_BLOB_SHA = "ff9a37a0be7a75912dbe0ae34dd95893d41efafb"
ANALYSIS_BLOB_SHA = "76bc8e9604c5d7e039e324e73036f353dc8ea31f"
REQUIREMENTS_BLOB_SHA = "00c1f779e97030f9b25ae494642edb31b5b09de5"
COLLECTION_RUN_ID = 34262408225
PUBLIC_ARTIFACT_ID = 10070586413
PUBLIC_ARTIFACT_SHA256 = "32851068cc61421f756041d0671681823b38c054f06e5082ed26c800bf296231"
PROTECTED_ARTIFACT_ID = 10070587302
PROTECTED_ARTIFACT_SHA256 = "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f"
PROTECTED_CIPHERTEXT_SHA256 = "15ba9d630cea0c26baca3ab50c33f7bcf10681a24293350b12acf3d4aeac4614"
PROTECTED_PLAINTEXT_TAR_SHA256 = "ec51a5451b63c5cbccfd83d01290f939d7a1832181af190c5fabd31fa806eb35"
CUSTODY_CERT_SHA256 = "cfa468d1091f2179cfe0c96ff000bfe45ae7c5bd1414146fbb99c77572dba707"


def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if check and proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def git_object_exists(spec: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", spec], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    ).returncode == 0


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
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
    if not git_is_ancestor(DATASET_LOCK_COMMIT_SHA, head):
        raise SystemExit("unblinding prohibited: dataset-lock commit is not an ancestor")
    require_blob(head, RECEIPT_REL, DATASET_LOCK_BLOB_SHA)
    receipt_history = [x for x in git("log", "--format=%H", head, "--", RECEIPT_REL).splitlines() if x]
    if receipt_history != [DATASET_LOCK_COMMIT_SHA]:
        raise SystemExit(f"unblinding prohibited: receipt history drift: {receipt_history}")

    receipt = load_json(ROOT / RECEIPT_REL)
    required_receipt = {
        "record_type": "TRACK_A_EPOCH_001_COLLECTION_RECEIPT",
        "protocol_id": PROTOCOL_ID,
        "epoch_id": EPOCH_ID,
        "collection_run_id": COLLECTION_RUN_ID,
        "paired_seed_units": 50,
        "blinded_observations": 2250,
        "public_artifact_id": PUBLIC_ARTIFACT_ID,
        "public_artifact_archive_sha256": PUBLIC_ARTIFACT_SHA256,
        "protected_artifact_id": PROTECTED_ARTIFACT_ID,
        "protected_artifact_archive_sha256": PROTECTED_ARTIFACT_SHA256,
        "protected_ciphertext_sha256": PROTECTED_CIPHERTEXT_SHA256,
        "protected_plaintext_tar_sha256": PROTECTED_PLAINTEXT_TAR_SHA256,
        "custody_certificate_sha256": CUSTODY_CERT_SHA256,
        "dataset_lock_status": "ESTABLISHED",
        "analysis_label_blinding_preserved": True,
        "primary_analysis_run": False,
        "unblinding_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    for key, expected in required_receipt.items():
        if receipt.get(key) != expected:
            raise SystemExit(f"unblinding prohibited: receipt field {key!r} drift")

    require_blob(head, PREREG_REL, PREREG_BLOB_SHA)
    require_blob(head, ANALYSIS_LOCK_REL, ANALYSIS_LOCK_BLOB_SHA)
    require_blob(head, ANALYSIS_REL, ANALYSIS_BLOB_SHA)
    require_blob(head, REQUIREMENTS_REL, REQUIREMENTS_BLOB_SHA)

    analysis_lock = load_json(ROOT / ANALYSIS_LOCK_REL)
    if analysis_lock.get("status") != "ANALYSIS_IMPLEMENTATION_LOCKED_NONEMPIRICAL":
        raise SystemExit("unblinding prohibited: analysis lock status drift")
    if analysis_lock.get("analysis_blob_sha") != ANALYSIS_BLOB_SHA:
        raise SystemExit("unblinding prohibited: locked analysis identity drift")
    if analysis_lock.get("boundaries", {}).get("unblinding_authorized") is not False:
        raise SystemExit("unblinding prohibited: pre-existing analysis lock unexpectedly authorizes unblinding")


def expected_authorization(parent_sha: str) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_001_UNBLINDING_AUTHORIZATION",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch_id": EPOCH_ID,
        "authorization_parent_sha": parent_sha,
        "dataset_lock_commit_sha": DATASET_LOCK_COMMIT_SHA,
        "dataset_lock_blob_sha": DATASET_LOCK_BLOB_SHA,
        "preregistration_blob_sha": PREREG_BLOB_SHA,
        "analysis_lock_blob_sha": ANALYSIS_LOCK_BLOB_SHA,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "requirements_lock_blob_sha": REQUIREMENTS_BLOB_SHA,
        "collection_run_id": COLLECTION_RUN_ID,
        "public_artifact_id": PUBLIC_ARTIFACT_ID,
        "public_artifact_archive_sha256": PUBLIC_ARTIFACT_SHA256,
        "protected_artifact_id": PROTECTED_ARTIFACT_ID,
        "protected_artifact_archive_sha256": PROTECTED_ARTIFACT_SHA256,
        "protected_ciphertext_sha256": PROTECTED_CIPHERTEXT_SHA256,
        "protected_plaintext_tar_sha256": PROTECTED_PLAINTEXT_TAR_SHA256,
        "custody_certificate_sha256": CUSTODY_CERT_SHA256,
        "authorization_status": "AUTHORIZED",
        "authorization_scope": "TRACK_A_EPOCH_001_MAPPING_RELEASE_ONLY",
        "authorization_class": "HUMAN_REPOSITORY_OWNER_SAME_SYSTEM_NONINDEPENDENT",
        "independent_authorization": False,
        "dataset_lock_verified": True,
        "analysis_lock_verified": True,
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


def validate_repository(*, expect_absent: bool) -> None:
    head = git("rev-parse", "HEAD")
    validate_locked_preconditions(head)

    if expect_absent:
        if AUTH_PATH.exists():
            raise SystemExit("tooling mode requires unblinding authorization to remain absent")
        print("TRACK_A_EPOCH_001_UNBLINDING_AUTHORIZATION_TOOLING_PASS")
        print("TRACK_A_DATASET_LOCK=ESTABLISHED")
        print("TRACK_A_UNBLINDING=NOT_AUTHORIZED")
        print("PRIMARY_ANALYSIS=NOT_RUN")
        return

    if not AUTH_PATH.exists():
        raise SystemExit("unblinding authorization is missing")

    parents = git("rev-list", "--parents", "-n", "1", head).split()
    if len(parents) != 2:
        raise SystemExit("unblinding authorization head must have exactly one parent")
    parent = parents[1]

    changed = sorted(
        x for x in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines() if x
    )
    if changed != [AUTH_REL]:
        raise SystemExit(f"unblinding authorization head must change only {AUTH_REL}; got {changed}")
    if git_object_exists(f"{parent}:{AUTH_REL}"):
        raise SystemExit("unblinding authorization path unexpectedly existed at parent")
    history = [x for x in git("log", "--format=%H", "--", AUTH_REL).splitlines() if x]
    if history != [head]:
        raise SystemExit(f"unblinding authorization must have exactly one history commit at HEAD; got {history}")

    actual = load_json(AUTH_PATH)
    expected = expected_authorization(parent)
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        mismatched = sorted(k for k in set(actual) & set(expected) if actual[k] != expected[k])
        raise SystemExit(
            f"unblinding authorization mismatch: missing={missing} extra={extra} mismatched={mismatched}"
        )

    print("TRACK_A_EPOCH_001_UNBLINDING_AUTHORIZATION_EVENT_SHAPE_PASS")
    print("TRACK_A_UNBLINDING=PENDING_VALIDATED_MERGE")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-absent", action="store_true")
    args = parser.parse_args()
    validate_repository(expect_absent=args.expect_absent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
