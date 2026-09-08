#!/usr/bin/env python3
"""Fail-closed validator for the Track A Epoch 001 collection receipt/dataset lock."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION.json"
RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_COLLECTION_RECEIPT.json"
AUTH_PATH = ROOT / AUTH_REL
RECEIPT_PATH = ROOT / RECEIPT_REL

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
EPOCH_ID = "TRACK_A_EPOCH_001"
AUTHORIZATION_COMMIT_SHA = "659aaa4dea2dd42624747952f1a47f307e69a014"
AUTHORIZATION_BLOB_SHA = "10373d3f3c01e0a145d0fae51e81402ad33af90f"
EXECUTION_WRAPPER_COMMIT_SHA = "98e72e370897c0e0916f78245a040108ed278189"
COLLECTION_RUN_ID = 34262408225
COLLECTION_JOB_ID = 102183375896
PUBLIC_ARTIFACT_ID = 10070586413
PUBLIC_ARTIFACT_NAME = "track-a-epoch-001-public-blinded-482"
PUBLIC_ARTIFACT_SIZE = 83776
PUBLIC_ARTIFACT_SHA256 = "32851068cc61421f756041d0671681823b38c054f06e5082ed26c800bf296231"
PROTECTED_ARTIFACT_ID = 10070587302
PROTECTED_ARTIFACT_NAME = "track-a-epoch-001-protected-encrypted-482"
PROTECTED_ARTIFACT_SIZE = 136074
PROTECTED_ARTIFACT_SHA256 = "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f"
PROTECTED_CIPHERTEXT_SHA256 = "15ba9d630cea0c26baca3ab50c33f7bcf10681a24293350b12acf3d4aeac4614"
PROTECTED_PLAINTEXT_TAR_SHA256 = "ec51a5451b63c5cbccfd83d01290f939d7a1832181af190c5fabd31fa806eb35"
CUSTODY_CERT_SHA256 = "cfa468d1091f2179cfe0c96ff000bfe45ae7c5bd1414146fbb99c77572dba707"


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
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot load {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one JSON object")
    return value


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


def expected_receipt(receipt_parent_sha: str) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_001_COLLECTION_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch_id": EPOCH_ID,
        "receipt_parent_sha": receipt_parent_sha,
        "authorization_commit_sha": AUTHORIZATION_COMMIT_SHA,
        "authorization_blob_sha": AUTHORIZATION_BLOB_SHA,
        "execution_wrapper_commit_sha": EXECUTION_WRAPPER_COMMIT_SHA,
        "collection_run_id": COLLECTION_RUN_ID,
        "collection_job_id": COLLECTION_JOB_ID,
        "collection_status": "COMPLETE_BLINDED_RETAINED",
        "paired_seed_units": 50,
        "blinded_observations": 2250,
        "public_artifact_name": PUBLIC_ARTIFACT_NAME,
        "public_artifact_id": PUBLIC_ARTIFACT_ID,
        "public_artifact_size_bytes": PUBLIC_ARTIFACT_SIZE,
        "public_artifact_archive_sha256": PUBLIC_ARTIFACT_SHA256,
        "protected_artifact_name": PROTECTED_ARTIFACT_NAME,
        "protected_artifact_id": PROTECTED_ARTIFACT_ID,
        "protected_artifact_size_bytes": PROTECTED_ARTIFACT_SIZE,
        "protected_artifact_archive_sha256": PROTECTED_ARTIFACT_SHA256,
        "protected_ciphertext_sha256": PROTECTED_CIPHERTEXT_SHA256,
        "protected_plaintext_tar_sha256": PROTECTED_PLAINTEXT_TAR_SHA256,
        "custody_certificate_sha256": CUSTODY_CERT_SHA256,
        "public_sidecar_qc": "PASS",
        "manifest_structure_qc": "PASS",
        "protected_ciphertext_qc": "PASS",
        "dataset_lock_status": "ESTABLISHED",
        "external_private_custody": "ESTABLISHED_NONSHARED",
        "custody_class": "DEVELOPER_SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "private_key_published": False,
        "analysis_label_blinding_preserved": True,
        "outcome_values_inspected_for_receipt": False,
        "outcome_aggregation_performed": False,
        "primary_analysis_run": False,
        "unblinding_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def validate_authorization_state(head: str) -> None:
    if not git_object_exists(f"{head}:{AUTH_REL}"):
        raise SystemExit("collection receipt prohibited: authorization record missing")
    if git("rev-parse", f"{head}:{AUTH_REL}") != AUTHORIZATION_BLOB_SHA:
        raise SystemExit("collection receipt prohibited: authorization blob drift")
    history = [x for x in git("log", "--format=%H", head, "--", AUTH_REL).splitlines() if x]
    if history != [AUTHORIZATION_COMMIT_SHA]:
        raise SystemExit(f"collection receipt prohibited: authorization history drift: {history}")
    if not git_is_ancestor(AUTHORIZATION_COMMIT_SHA, head):
        raise SystemExit("collection receipt prohibited: authorization commit is not ancestor")


def validate_repository(*, expect_absent: bool) -> None:
    head = git("rev-parse", "HEAD")
    validate_authorization_state(head)

    if expect_absent:
        if RECEIPT_PATH.exists():
            raise SystemExit("tooling mode requires collection receipt to remain absent")
        print("TRACK_A_EPOCH_001_COLLECTION_RECEIPT_TOOLING_PASS")
        print("TRACK_A_DATASET_LOCK=NOT_ESTABLISHED_IN_REPOSITORY")
        print("TRACK_A_UNBLINDING=NOT_AUTHORIZED")
        return

    if not RECEIPT_PATH.exists():
        raise SystemExit("collection receipt is missing")

    parents = git("rev-list", "--parents", "-n", "1", head).split()
    if len(parents) != 2:
        raise SystemExit("collection receipt head must have exactly one parent")
    parent = parents[1]

    changed = sorted(
        x
        for x in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines()
        if x
    )
    if changed != [RECEIPT_REL]:
        raise SystemExit(f"collection receipt head must change only {RECEIPT_REL}; got {changed}")
    if git_object_exists(f"{parent}:{RECEIPT_REL}"):
        raise SystemExit("collection receipt path unexpectedly existed at parent")

    history = [x for x in git("log", "--format=%H", "--", RECEIPT_REL).splitlines() if x]
    if history != [head]:
        raise SystemExit(f"collection receipt must have exactly one history commit at HEAD; got {history}")

    require_exact_object(load_json(RECEIPT_PATH), expected_receipt(parent), "collection receipt")
    print("TRACK_A_EPOCH_001_COLLECTION_RECEIPT_EVENT_SHAPE_PASS")
    print("TRACK_A_DATASET_LOCK=PENDING_VALIDATED_MERGE")
    print("TRACK_A_UNBLINDING=NOT_AUTHORIZED")
    print("PRIMARY_ANALYSIS=NOT_RUN")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-absent", action="store_true")
    args = parser.parse_args()
    validate_repository(expect_absent=args.expect_absent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
