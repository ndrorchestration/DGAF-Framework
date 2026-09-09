#!/usr/bin/env python3
"""Validate the immutable Track A Epoch 001 unblinded-input receipt event."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_UNBLINDED_INPUT_RECEIPT.json"
MATERIALIZER_REL = "scripts/materialize_track_a_epoch_001_unblinded_input.py"
MATERIALIZER_MERGE_SHA = "f92c251bb8fcf068c644db04ae9d2f855c382caa"
MATERIALIZER_BLOB_SHA = "d4dd3551dda6413ee4d0b195c6d726e17cb2481a"
UNBLINDING_AUTH_SHA = "2e1981870a8455abed36fd72dcb3aaa35e2f9bff"
COLLECTION_RUN_ID = 34262408225
PUBLIC_ARTIFACT_ID = 10070586413
PUBLIC_ARCHIVE_SHA256 = "32851068cc61421f756041d0671681823b38c054f06e5082ed26c800bf296231"
PROTECTED_ARTIFACT_ID = 10070587302
PROTECTED_ARCHIVE_SHA256 = "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f"
PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Track A unblinded-input receipt validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def exact_keys() -> set[str]:
    return {
        "record_type",
        "schema_version",
        "protocol_id",
        "receipt_parent_sha",
        "materializer_merge_sha",
        "materializer_blob_sha",
        "unblinding_authorization_sha",
        "collection_run_id",
        "public_artifact_id",
        "public_artifact_archive_sha256",
        "protected_artifact_id",
        "protected_artifact_archive_sha256",
        "materialized_input_sha256",
        "materialized_input_sidecar_sha256",
        "durable_retention_type",
        "durable_retention_id",
        "paired_seed_units",
        "record_count",
        "structure_validation",
        "custody_class",
        "independent_custody",
        "private_key_published",
        "primary_analysis_authorized",
        "primary_analysis_run",
        "outcome_aggregation_performed",
        "historical_pooling_allowed",
        "epoch_004_substitution_allowed",
        "high_assurance_authorized",
        "canonical_dgaf_efficacy",
    }


def validate_common() -> None:
    head = git("rev-parse", "HEAD")
    require(git("merge-base", "--is-ancestor", MATERIALIZER_MERGE_SHA, head) == "", "materializer merge is not an ancestor")
    require(git("rev-parse", f"{MATERIALIZER_MERGE_SHA}:{MATERIALIZER_REL}") == MATERIALIZER_BLOB_SHA, "materializer blob mismatch at accepted merge")
    require(git("rev-parse", f"HEAD:{MATERIALIZER_REL}") == MATERIALIZER_BLOB_SHA, "materializer blob drifted after accepted merge")


def validate_receipt_event() -> None:
    validate_common()
    path = Path(RECEIPT_REL)
    require(path.is_file(), "receipt file is absent")
    head = git("rev-parse", "HEAD")
    parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()
    require(len(parents) == 2, "receipt event must have exactly one parent")
    parent = parents[1]
    changed = [line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines() if line]
    require(changed == [RECEIPT_REL], "receipt event must change exactly the receipt file")
    require(subprocess.run(["git", "cat-file", "-e", f"{parent}:{RECEIPT_REL}"], check=False).returncode != 0, "receipt path existed at parent")
    history = [line for line in git("log", "--format=%H", "--", RECEIPT_REL).splitlines() if line]
    require(history == [head], "receipt path must have exactly one history commit at HEAD")

    doc = load_json(path)
    require(set(doc) == exact_keys(), "receipt schema has missing or extra fields")
    expected = {
        "record_type": "TRACK_A_EPOCH_001_UNBLINDED_INPUT_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "receipt_parent_sha": parent,
        "materializer_merge_sha": MATERIALIZER_MERGE_SHA,
        "materializer_blob_sha": MATERIALIZER_BLOB_SHA,
        "unblinding_authorization_sha": UNBLINDING_AUTH_SHA,
        "collection_run_id": COLLECTION_RUN_ID,
        "public_artifact_id": PUBLIC_ARTIFACT_ID,
        "public_artifact_archive_sha256": PUBLIC_ARCHIVE_SHA256,
        "protected_artifact_id": PROTECTED_ARTIFACT_ID,
        "protected_artifact_archive_sha256": PROTECTED_ARCHIVE_SHA256,
        "paired_seed_units": 50,
        "record_count": 2250,
        "structure_validation": "PASS",
        "custody_class": "HUMAN_REPOSITORY_OWNER_SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "private_key_published": False,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "outcome_aggregation_performed": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    for key, value in expected.items():
        require(doc.get(key) == value, f"receipt field mismatch: {key}")
    require(isinstance(doc["materialized_input_sha256"], str) and SHA256_RE.fullmatch(doc["materialized_input_sha256"]) is not None, "materialized input SHA-256 malformed")
    require(isinstance(doc["materialized_input_sidecar_sha256"], str) and SHA256_RE.fullmatch(doc["materialized_input_sidecar_sha256"]) is not None, "sidecar SHA-256 malformed")
    require(doc["materialized_input_sha256"] != doc["materialized_input_sidecar_sha256"], "input and sidecar digests must be distinct")
    require(isinstance(doc["durable_retention_type"], str) and doc["durable_retention_type"] in {"GITHUB_ACTIONS_ARTIFACT", "GITHUB_RELEASE_ASSET", "LOCAL_CUSTODY_ARCHIVE"}, "unsupported durable retention type")
    require(isinstance(doc["durable_retention_id"], str) and bool(doc["durable_retention_id"].strip()), "durable retention identity is required")
    require("PRIVATE" not in doc["durable_retention_id"].upper(), "durable retention identity must not encode private-key material")
    print("TRACK_A_EPOCH_001_UNBLINDED_INPUT_RECEIPT=PASS")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
    print("OUTCOME_AGGREGATION=NOT_PERFORMED")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")


def validate_expect_absent() -> None:
    validate_common()
    require(not Path(RECEIPT_REL).exists(), "receipt must remain absent in tooling mode")
    print("TRACK_A_EPOCH_001_UNBLINDED_INPUT_RECEIPT=NOT_ESTABLISHED")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-absent", action="store_true")
    args = parser.parse_args()
    if args.expect_absent:
        validate_expect_absent()
    else:
        validate_receipt_event()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
