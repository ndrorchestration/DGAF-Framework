#!/usr/bin/env python3
"""Fail-closed validator for Track A Epoch 001 primary-analysis authorization."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
EPOCH_ID = "TRACK_A_EPOCH_001"

RECEIPT_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_UNBLINDED_INPUT_RECEIPT.json"
)
AUTH_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_PRIMARY_ANALYSIS_AUTHORIZATION.json"
)
PRIMARY_RESULT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_PRIMARY_RESULT.json"
UNBLINDING_AUTH_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_UNBLINDING_AUTHORIZATION.json"
)
RECEIPT_VALIDATOR_REL = "scripts/validate_track_a_epoch_001_unblinded_input_receipt.py"
ANALYSIS_LOCK_REL = "docs/experiment/TRACK_A_EPOCH_001_ANALYSIS_LOCK.json"
ANALYSIS_REL = "experiments/pdmal_pilot/track_a_epoch_001_analysis.py"
PREREG_REL = (
    "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json"
)
REQUIREMENTS_REL = "experiments/pdmal_pilot/requirements-full-lock.txt"

AUTH_PATH = ROOT / AUTH_REL
RECEIPT_PATH = ROOT / RECEIPT_REL

UNBLINDING_AUTH_SHA = "2e1981870a8455abed36fd72dcb3aaa35e2f9bff"
UNBLINDING_AUTH_BLOB_SHA = "1e4d90181ca39b199baaa32f6487f679f6bf0e6e"
RECEIPT_TOOLING_MERGE_SHA = "f36d746f603f95d14098322792bec074b21b54cb"
RECEIPT_VALIDATOR_BLOB_SHA = "80ef872280713193ba4fbae4299c6558fe43d7c1"
ANALYSIS_LOCK_BLOB_SHA = "ff9a37a0be7a75912dbe0ae34dd95893d41efafb"
ANALYSIS_BLOB_SHA = "76bc8e9604c5d7e039e324e73036f353dc8ea31f"
ANALYSIS_CONFIG_SHA256 = (
    "355b164f69e91405819f092d0721b7597b87b06de79394a0c451169410a5ab6d"
)
PREREG_BLOB_SHA = "52148950ff054a407c2e6b5cf36103695cf96474"
REQUIREMENTS_BLOB_SHA = "00c1f779e97030f9b25ae494642edb31b5b09de5"
MATERIALIZER_MERGE_SHA = "f92c251bb8fcf068c644db04ae9d2f855c382caa"
MATERIALIZER_BLOB_SHA = "d4dd3551dda6413ee4d0b195c6d726e17cb2481a"
PUBLIC_ARTIFACT_ID = 10070586413
PUBLIC_ARCHIVE_SHA256 = (
    "32851068cc61421f756041d0671681823b38c054f06e5082ed26c800bf296231"
)
PROTECTED_ARTIFACT_ID = 10070587302
PROTECTED_ARCHIVE_SHA256 = (
    "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Track A primary-analysis authorization refused: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot load {path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value


def require_blob(head: str, rel: str, expected: str) -> None:
    require(git_object_exists(f"{head}:{rel}"), f"required source missing: {rel}")
    actual = git("rev-parse", f"{head}:{rel}")
    require(actual == expected, f"required source drift: {rel}: {actual} != {expected}")


def validate_static_chain(head: str) -> None:
    require(
        git_is_ancestor(UNBLINDING_AUTH_SHA, head),
        "accepted unblinding authorization is not an ancestor",
    )
    require(
        git_is_ancestor(RECEIPT_TOOLING_MERGE_SHA, head),
        "accepted receipt tooling is not an ancestor",
    )
    require_blob(head, UNBLINDING_AUTH_REL, UNBLINDING_AUTH_BLOB_SHA)
    require_blob(head, RECEIPT_VALIDATOR_REL, RECEIPT_VALIDATOR_BLOB_SHA)
    require_blob(head, ANALYSIS_LOCK_REL, ANALYSIS_LOCK_BLOB_SHA)
    require_blob(head, ANALYSIS_REL, ANALYSIS_BLOB_SHA)
    require_blob(head, PREREG_REL, PREREG_BLOB_SHA)
    require_blob(head, REQUIREMENTS_REL, REQUIREMENTS_BLOB_SHA)

    analysis_lock = load_json(ROOT / ANALYSIS_LOCK_REL)
    require(
        analysis_lock.get("status") == "ANALYSIS_IMPLEMENTATION_LOCKED_NONEMPIRICAL",
        "analysis lock status drift",
    )
    require(
        analysis_lock.get("analysis_blob_sha") == ANALYSIS_BLOB_SHA,
        "analysis lock no longer binds the accepted analysis blob",
    )
    require(
        analysis_lock.get("analysis_config_sha256") == ANALYSIS_CONFIG_SHA256,
        "analysis configuration digest drift",
    )
    primary = analysis_lock.get("primary_contract")
    require(isinstance(primary, dict), "analysis lock primary_contract missing")
    expected_primary = {
        "seed_count": 50,
        "expected_total_records": 2250,
        "endpoint": "ffcr_success",
        "primary_topology": "pdmal",
        "primary_comparator": "random_regular",
        "estimand": "mean_seed_paired_pdmal_minus_random_regular_ffcr",
        "bootstrap": "paired_seed_effects_percentile",
        "bootstrap_resamples": 10000,
        "bootstrap_seed": 20270151,
        "alpha": 0.05,
        "confirmatory_test_count": 1,
    }
    require(primary == expected_primary, "locked primary analysis contract drift")


def validate_receipt_at(parent: str) -> tuple[str, str, dict[str, Any]]:
    require(
        git_object_exists(f"{parent}:{RECEIPT_REL}"),
        "unblinded-input receipt is not established at authorization parent",
    )
    receipt_history = [
        item
        for item in git("log", "--format=%H", parent, "--", RECEIPT_REL).splitlines()
        if item
    ]
    require(
        len(receipt_history) == 1,
        f"unblinded-input receipt history must contain exactly one commit: {receipt_history}",
    )
    receipt_commit = receipt_history[0]
    require(
        git_is_ancestor(receipt_commit, parent),
        "unblinded-input receipt commit is not an ancestor of authorization parent",
    )

    receipt_commit_shape = git(
        "rev-list", "--parents", "-n", "1", receipt_commit
    ).split()
    require(
        len(receipt_commit_shape) == 2,
        "unblinded-input receipt commit must have exactly one parent",
    )
    receipt_parent = receipt_commit_shape[1]
    changed = sorted(
        item
        for item in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            receipt_commit,
        ).splitlines()
        if item
    )
    require(
        changed == [RECEIPT_REL],
        f"unblinded-input receipt commit changed unexpected files: {changed}",
    )
    require(
        not git_object_exists(f"{receipt_parent}:{RECEIPT_REL}"),
        "unblinded-input receipt path existed before its immutable event",
    )

    receipt_blob = git("rev-parse", f"{parent}:{RECEIPT_REL}")
    receipt = load_json(RECEIPT_PATH)
    expected_fields = {
        "record_type": "TRACK_A_EPOCH_001_UNBLINDED_INPUT_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "receipt_parent_sha": receipt_parent,
        "materializer_merge_sha": MATERIALIZER_MERGE_SHA,
        "materializer_blob_sha": MATERIALIZER_BLOB_SHA,
        "unblinding_authorization_sha": UNBLINDING_AUTH_SHA,
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
    for key, expected in expected_fields.items():
        require(receipt.get(key) == expected, f"unblinded-input receipt field drift: {key}")

    for key in ("materialized_input_sha256", "materialized_input_sidecar_sha256"):
        value = receipt.get(key)
        require(
            isinstance(value, str) and SHA256_RE.fullmatch(value) is not None,
            f"unblinded-input receipt {key} is malformed",
        )
    require(
        receipt["materialized_input_sha256"]
        != receipt["materialized_input_sidecar_sha256"],
        "materialized input and sidecar digests must be distinct",
    )
    require(
        receipt.get("durable_retention_type")
        in {"GITHUB_ACTIONS_ARTIFACT", "GITHUB_RELEASE_ASSET", "LOCAL_CUSTODY_ARCHIVE"},
        "unblinded-input receipt durable retention type is unsupported",
    )
    retention_id = receipt.get("durable_retention_id")
    require(
        isinstance(retention_id, str) and bool(retention_id.strip()),
        "unblinded-input receipt durable retention identity is missing",
    )
    return receipt_commit, receipt_blob, receipt


def expected_authorization(
    parent_sha: str,
    receipt_commit_sha: str,
    receipt_blob_sha: str,
    receipt: dict[str, Any],
) -> dict[str, Any]:
    return {
        "record_type": "TRACK_A_EPOCH_001_PRIMARY_ANALYSIS_AUTHORIZATION",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch_id": EPOCH_ID,
        "authorization_parent_sha": parent_sha,
        "unblinded_input_receipt_commit_sha": receipt_commit_sha,
        "unblinded_input_receipt_blob_sha": receipt_blob_sha,
        "materialized_input_sha256": receipt["materialized_input_sha256"],
        "materialized_input_sidecar_sha256": receipt[
            "materialized_input_sidecar_sha256"
        ],
        "durable_retention_type": receipt["durable_retention_type"],
        "durable_retention_id": receipt["durable_retention_id"],
        "preregistration_blob_sha": PREREG_BLOB_SHA,
        "analysis_lock_blob_sha": ANALYSIS_LOCK_BLOB_SHA,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
        "requirements_lock_blob_sha": REQUIREMENTS_BLOB_SHA,
        "paired_seed_units": 50,
        "record_count": 2250,
        "authorization_status": "AUTHORIZED",
        "authorization_scope": "TRACK_A_EPOCH_001_LOCKED_PRIMARY_ANALYSIS_ONLY",
        "authorization_class": "HUMAN_REPOSITORY_OWNER_SAME_SYSTEM_NONINDEPENDENT",
        "independent_authorization": False,
        "unblinded_input_receipt_verified": True,
        "analysis_lock_verified": True,
        "primary_analysis_authorized": True,
        "primary_analysis_run": False,
        "outcome_aggregation_authorized": True,
        "outcome_aggregation_scope": "LOCKED_PRIMARY_ANALYSIS_ONLY",
        "exploratory_analysis_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "additional_scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance_authorized": False,
    }


def validate_repository(*, expect_absent: bool) -> None:
    head = git("rev-parse", "HEAD")
    validate_static_chain(head)

    if expect_absent:
        require(
            not RECEIPT_PATH.exists(),
            "tooling mode requires unblinded-input receipt to remain absent",
        )
        require(
            not AUTH_PATH.exists(),
            "tooling mode requires primary-analysis authorization to remain absent",
        )
        require(
            not (ROOT / PRIMARY_RESULT_REL).exists(),
            "tooling mode prohibits a primary result artifact",
        )
        print("TRACK_A_EPOCH_001_PRIMARY_ANALYSIS_AUTHORIZATION_TOOLING=PASS")
        print("UNBLINDED_INPUT_RECEIPT=NOT_ESTABLISHED")
        print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
        print("SCIENTIFIC_N_INCREMENT=0")
        return

    require(AUTH_PATH.exists(), "primary-analysis authorization file is absent")
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    require(
        len(parents) == 2,
        "primary-analysis authorization head must have exactly one parent",
    )
    parent = parents[1]

    changed = sorted(
        item
        for item in git(
            "diff-tree", "--no-commit-id", "--name-only", "-r", head
        ).splitlines()
        if item
    )
    require(
        changed == [AUTH_REL],
        f"primary-analysis authorization head changed unexpected files: {changed}",
    )
    require(
        not git_object_exists(f"{parent}:{AUTH_REL}"),
        "primary-analysis authorization path existed at parent",
    )
    history = [
        item for item in git("log", "--format=%H", "--", AUTH_REL).splitlines() if item
    ]
    require(
        history == [head],
        f"primary-analysis authorization must have one history commit at HEAD: {history}",
    )
    require(
        not (ROOT / PRIMARY_RESULT_REL).exists(),
        "primary result must remain absent during authorization",
    )

    receipt_commit, receipt_blob, receipt = validate_receipt_at(parent)
    actual = load_json(AUTH_PATH)
    expected = expected_authorization(parent, receipt_commit, receipt_blob, receipt)
    require(
        actual == expected,
        "primary-analysis authorization JSON does not exactly match the locked contract",
    )

    print("TRACK_A_EPOCH_001_PRIMARY_ANALYSIS_AUTHORIZATION_EVENT_SHAPE=PASS")
    print("PRIMARY_ANALYSIS=PENDING_VALIDATED_MERGE")
    print("PRIMARY_ANALYSIS_RUN=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-absent", action="store_true")
    args = parser.parse_args()
    validate_repository(expect_absent=args.expect_absent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
