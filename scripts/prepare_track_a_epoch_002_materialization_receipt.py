#!/usr/bin/env python3
"""Prepare the canonical non-authorizing Epoch 002 MATERIALIZATION_RECEIPT.

This helper is creation-only. It requires an already accepted one-file
materialization-evidence admission at HEAD, constructs the exact receipt defined
by the accepted validator, and optionally writes exactly the canonical receipt
path. It does not decrypt material, authorize analysis, run analysis, or change
scientific N.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_materialization.py"
RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT_PREP_FAIL: {message}")


def load_validator() -> Any:
    spec = importlib.util.spec_from_file_location(
        "epoch_002_materialization_for_receipt_preparer",
        VALIDATOR_PATH,
    )
    if spec is None or spec.loader is None:
        fail("cannot load materialization validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load_validator()


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def require_clean_worktree() -> None:
    if git("status", "--porcelain"):
        fail("repository worktree must be clean before receipt preparation")


def generated_at_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")


def build_receipt(generated_at_utc: str) -> dict[str, Any]:
    validator.validate_semantic_policy()
    validator.validate_no_analysis_successor()

    if not validator.MATERIALIZATION_EVIDENCE_PATH.exists():
        fail("canonical materialization evidence is absent")
    if validator.MATERIALIZATION_RECEIPT_PATH.exists():
        fail("canonical materialization receipt already exists")

    head = git("rev-parse", "HEAD")
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    if len(parents) != 2:
        fail("accepted evidence-admission HEAD must have exactly one parent")
    evidence_parent = parents[1]

    changed = [
        line
        for line in git("diff", "--name-only", evidence_parent, head).splitlines()
        if line
    ]
    if changed != [validator.MATERIALIZATION_EVIDENCE_REL]:
        fail("HEAD must be the one-file materialization evidence-admission event")

    if validator.git_object_exists(
        f"{evidence_parent}:{validator.MATERIALIZATION_EVIDENCE_REL}"
    ):
        fail("materialization evidence must be creation-only at HEAD")

    if validator.path_history(validator.MATERIALIZATION_EVIDENCE_REL) != [head]:
        fail("materialization evidence must have first-and-only history at HEAD")

    dataset_lock = validator.load_json(validator.DATASET_LOCK_PATH)
    decision = validator.load_json(validator.UNBLINDING_DECISION_PATH)
    evidence = validator.load_json(validator.MATERIALIZATION_EVIDENCE_PATH)
    dataset_lock_evidence = validator.load_json(
        validator.DATASET_LOCK_EVIDENCE_PATH
    )

    validator.validate_dataset_lock_receipt_object(dataset_lock)
    validator.validate_unblinding_decision_object(decision, dataset_lock)
    validator.validate_evidence_against_dataset_lock(
        evidence,
        dataset_lock_evidence,
    )
    validator.validate_evidence_predecessors(evidence, evidence_parent)

    decision_history = validator.path_history(
        validator.UNBLINDING_DECISION_REL,
        evidence_parent,
    )
    if len(decision_history) != 1:
        fail("unblinding decision must have exactly one immutable history event")

    decision_commit = decision_history[0]
    decision_bytes = validator.git(
        "show",
        f"{evidence_parent}:{validator.UNBLINDING_DECISION_REL}",
    ).encode("utf-8")
    decision_digest = validator.sha256_bytes(decision_bytes)
    evidence_digest = validator.sha256_file(
        validator.MATERIALIZATION_EVIDENCE_PATH
    )

    receipt = validator.expected_receipt(
        decision,
        evidence,
        unblinding_decision_commit_sha=decision_commit,
        unblinding_decision_sha256=decision_digest,
        evidence_sha256=evidence_digest,
        materialization_parent_sha=head,
        generated_at_utc=generated_at_utc,
    )

    validator.validate_receipt_object(
        receipt,
        decision,
        evidence,
        unblinding_decision_commit_sha=decision_commit,
        unblinding_decision_sha256=decision_digest,
        evidence_sha256=evidence_digest,
        materialization_parent_sha=head,
    )
    return receipt


def write_receipt(receipt: dict[str, Any]) -> Path:
    require_clean_worktree()
    path = ROOT / RECEIPT_REL
    if path.exists():
        fail("canonical materialization receipt already exists")
    path.write_bytes(canonical_json_bytes(receipt))

    changed = [
        line
        for line in git("status", "--porcelain").splitlines()
        if line.strip()
    ]
    expected_suffix = RECEIPT_REL
    if len(changed) != 1 or not changed[0].endswith(expected_suffix):
        try:
            path.unlink()
        except OSError:
            pass
        fail("receipt preparation changed something other than the canonical receipt path")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--generated-at-utc",
        default=None,
        help="Optional explicit RFC3339 UTC timestamp for deterministic preparation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generated_at = args.generated_at_utc or generated_at_now()
    receipt = build_receipt(generated_at)

    if args.write:
        path = write_receipt(receipt)
        print("TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT=PREPARED_PENDING_COMMIT_AND_REVIEW")
        print(f"MATERIALIZATION_RECEIPT_PATH={path.relative_to(ROOT)}")
    else:
        print(json.dumps(receipt, indent=2, sort_keys=True))
        print("TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT=PASS_DRY_RUN_NOT_WRITTEN")

    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
