#!/usr/bin/env python3
"""Prepare the exact Epoch 002 operator dataset-lock receipt repository delta."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def fail(message: str) -> NoReturn:
    raise SystemExit(
        f"TRACK_A_EPOCH_002_OPERATOR_DATASET_LOCK_RECEIPT_PREP_FAIL: {message}"
    )


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


dataset_lock = load_module(
    SCRIPTS / "validate_track_a_epoch_002_dataset_lock.py",
    "epoch_002_dataset_lock_for_operator_receipt_preparer",
)


def git(*args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and completed.returncode != 0:
        fail(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def path_history(path: str) -> list[str]:
    return [line for line in git("log", "--format=%H", "--", path).splitlines() if line]


def require_clean_repository() -> None:
    status = git("status", "--porcelain", "--untracked-files=all")
    if status:
        fail("clean repository required before preparing operator dataset-lock receipt")


def require_admitted_evidence() -> tuple[Path, Path]:
    evidence_path = ROOT / dataset_lock.OPERATOR_EVIDENCE_REL
    ledger_path = ROOT / dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL
    if not evidence_path.is_file() or not ledger_path.is_file():
        fail("admitted operator evidence and pre-lock ledger are required")
    return evidence_path, ledger_path


def require_receipt_absent() -> Path:
    receipt_path = ROOT / dataset_lock.RECEIPT_REL
    if receipt_path.exists():
        fail("receipt already exists in the working tree")
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{dataset_lock.RECEIPT_REL}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode == 0:
        fail("receipt already exists in HEAD")
    return receipt_path


def derive_evidence_admission_commit() -> str:
    evidence_history = path_history(dataset_lock.OPERATOR_EVIDENCE_REL)
    ledger_history = path_history(dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL)
    if (
        len(evidence_history) != 1
        or len(ledger_history) != 1
        or evidence_history != ledger_history
    ):
        fail("operator evidence and pre-lock ledger must share one immutable admission event")
    admission_commit = evidence_history[0]
    head = git("rev-parse", "HEAD")
    if not git_is_ancestor(admission_commit, head):
        fail("operator evidence admission commit is not an ancestor of HEAD")
    changed = sorted(
        line
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            admission_commit,
        ).splitlines()
        if line
    )
    expected = sorted(
        [
            dataset_lock.OPERATOR_EVIDENCE_REL,
            dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL,
        ]
    )
    if changed != expected:
        fail(
            "operator evidence admission commit must change exactly the two canonical "
            f"evidence files; got {changed}"
        )
    return admission_commit


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def verify_exact_delta() -> None:
    actual = [
        line
        for line in git("status", "--porcelain", "--untracked-files=all").splitlines()
        if line
    ]
    expected = [f"?? {dataset_lock.RECEIPT_REL}"]
    if actual != expected:
        fail(f"repository delta must contain exactly the receipt file; got {actual}")


def prepare(
    *,
    write: bool = False,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    evidence_path, ledger_path = require_admitted_evidence()
    receipt_path = require_receipt_absent()
    require_clean_repository()

    evidence, validated_sha = dataset_lock.validate_evidence_file(evidence_path)
    if evidence.get("evidence_execution_class") != "OPERATOR_CODESPACE":
        fail("operator receipt requires OPERATOR_CODESPACE evidence")
    if evidence.get("collection_execution_class") != "OPERATOR_CODESPACE":
        fail("operator receipt requires OPERATOR_CODESPACE collection provenance")
    dataset_lock.validate_pre_lock_ledger(ledger_path, evidence)

    evidence_sha256 = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    if validated_sha != evidence_sha256:
        fail("validated evidence SHA-256 does not match repository bytes")
    admission_commit = derive_evidence_admission_commit()
    generated_at = generated_at_utc or utc_now()
    receipt = dataset_lock.expected_operator_receipt(
        evidence,
        evidence_sha256,
        evidence_admission_commit_sha=admission_commit,
        generated_at_utc=generated_at,
    )
    dataset_lock.validate_operator_receipt_object(
        receipt,
        evidence,
        evidence_sha256,
        admission_commit,
    )

    if not write:
        print(
            "TRACK_A_EPOCH_002_OPERATOR_DATASET_LOCK_RECEIPT_PREPARER="
            "PASS_DRY_RUN_NOT_WRITTEN"
        )
        print(f"EVIDENCE_ADMISSION_COMMIT={admission_commit}")
        print(f"EVIDENCE_SHA256={evidence_sha256}")
        print(f"RECEIPT_DESTINATION={receipt_path}")
        return receipt

    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        receipt_path.write_bytes(dataset_lock.canonical_json_bytes(receipt))
        verify_exact_delta()
        persisted = dataset_lock.load_object(receipt_path, "dataset-lock receipt")
        dataset_lock.validate_operator_receipt_object(
            persisted,
            evidence,
            evidence_sha256,
            admission_commit,
        )
    except BaseException:
        receipt_path.unlink(missing_ok=True)
        raise

    print(
        "TRACK_A_EPOCH_002_OPERATOR_DATASET_LOCK_RECEIPT_PREPARER="
        "PASS_NONAUTHORIZING_DELTA_PREPARED"
    )
    print(f"EVIDENCE_ADMISSION_COMMIT={admission_commit}")
    print(f"EVIDENCE_SHA256={evidence_sha256}")
    print(f"RECEIPT_DESTINATION={receipt_path}")
    print(f"NEXT_GIT_ADD=git add {dataset_lock.RECEIPT_REL}")
    print(
        "NEXT_GIT_COMMIT=git commit -m 'establish Track A Epoch 002 dataset-lock receipt'"
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    prepare(write=args.write)
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
