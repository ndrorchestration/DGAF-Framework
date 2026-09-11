#!/usr/bin/env python3
"""Validate the fail-closed Track A Epoch 002 dataset-lock boundary.

This tool never creates result records, executes empirical work, unblinds labels,
or authorizes analysis. It validates only a retained ledger and a future exact
one-record dataset-lock append after completed blinded collection and QC.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, NoReturn, cast

from scripts import validate_track_a_epoch_002_result_ledger as structural
from scripts import validate_track_a_epoch_002_result_record_semantics as semantics

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = Path(__file__).resolve()
LEDGER_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_RESULT_LEDGER.json"
LEDGER_PATH = ROOT / LEDGER_REL
HEX40 = re.compile(r"^[0-9a-f]{40}$")
LOCK_INDEX = structural.ORDER.index("DATASET_LOCK_RECEIPT")

ALL_NON_EFFECTS = {
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
}
EXPECTED_SCIENTIFIC_EFFECT = {
    "empirical_n_increment": 0,
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"EPOCH_002_DATASET_LOCK_FAIL: {message}")


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except subprocess.CalledProcessError as exc:
        fail(f"git {' '.join(args)} failed ({exc.returncode})")


def git_path_exists(path: str, revision: str = "HEAD") -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}:{path}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def load_records(path: Path) -> list[dict[str, Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid or missing result ledger: {exc}")
    return require_record_list(value)


def load_records_text(text: str, label: str) -> list[dict[str, Any]]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"invalid {label}: {exc}")
    return require_record_list(value)


def require_record_list(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        fail("result ledger must be a JSON array")
    if any(not isinstance(record, dict) for record in value):
        fail("result ledger entries must be JSON objects")
    return cast(list[dict[str, Any]], value)


def validate_with_existing_validators(records: list[dict[str, Any]]) -> None:
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json") as handle:
        json.dump(records, handle, sort_keys=True)
        handle.flush()
        path = Path(handle.name)
        try:
            structural.validate_ledger(path)
            semantics.validate_ledger(path)
        except (ValueError, SystemExit) as exc:
            fail(f"retained ledger violates existing structural/semantic contract: {exc}")


def validate_lock_record(record: dict[str, Any], qc_record_id: str) -> None:
    if record.get("record_type") != "DATASET_LOCK_RECEIPT":
        fail("appended record must be DATASET_LOCK_RECEIPT")
    if record.get("status") != "PASS":
        fail("dataset lock requires PASS")
    if record.get("predecessor_record_ids") != [qc_record_id]:
        fail("dataset lock must directly reference prior QC_LEDGER")
    if record.get("authorization_effect") != "REQUIRES_SEPARATE_EXACT_COMMIT":
        fail("dataset-lock semantic ceiling requires separate exact unblinding commit")
    if set(record.get("non_effects", [])) != ALL_NON_EFFECTS:
        fail("dataset-lock semantic ceiling requires full non-authorization set")
    if record.get("scientific_state_effect") != EXPECTED_SCIENTIFIC_EFFECT:
        fail("dataset-lock semantic ceiling forbids scientific-state promotion")


def validate_transition(before: list[dict[str, Any]], after: list[dict[str, Any]]) -> None:
    if len(after) != len(before) + 1 or after[:-1] != before:
        fail("dataset-lock event must append exactly one record without predecessor rewrites")

    expected_prefix = structural.ORDER[:LOCK_INDEX]
    actual_prefix = [record.get("record_type") for record in before]
    if len(before) != LOCK_INDEX or actual_prefix != expected_prefix:
        fail("pre-lock ledger must be complete through QC_LEDGER with all 50 seed records")
    if any(record.get("status") != "PASS" for record in before):
        fail("pre-lock ledger must be complete through QC_LEDGER with only PASS predecessors")

    qc = before[-1]
    if qc.get("record_type") != "QC_LEDGER":
        fail("pre-lock ledger must terminate at QC_LEDGER")
    qc_id = qc.get("record_id")
    if not isinstance(qc_id, str) or not qc_id:
        fail("QC_LEDGER record_id missing")

    validate_lock_record(after[-1], qc_id)
    validate_with_existing_validators(before)
    validate_with_existing_validators(after)


def validate_retained_ledger(path: Path, *, require_lock: bool) -> None:
    records = load_records(path)
    validate_with_existing_validators(records)
    has_lock = any(record.get("record_type") == "DATASET_LOCK_RECEIPT" for record in records)
    if require_lock:
        if not has_lock or records[-1].get("record_type") != "DATASET_LOCK_RECEIPT":
            fail("retained ledger must terminate at DATASET_LOCK_RECEIPT")
    elif has_lock:
        fail("current boundary requires DATASET_LOCK_RECEIPT to remain absent")


def event_parent(expected_base_sha: str) -> str:
    base = expected_base_sha.lower()
    if not HEX40.fullmatch(base):
        fail("malformed expected base SHA")
    head = git("rev-parse", "HEAD").lower()
    parents = git("rev-list", "--parents", "-n", "1", head).lower().split()[1:]
    if len(parents) != 1:
        fail("dataset-lock head must have exactly one parent")
    parent = parents[0]
    if parent != base:
        fail(f"dataset-lock head parent {parent} does not equal expected base {base}")
    return parent


def validate_event(expected_base_sha: str) -> None:
    parent = event_parent(expected_base_sha)
    head = git("rev-parse", "HEAD").lower()
    changed = tuple(line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines() if line)
    if changed != (LEDGER_REL,):
        fail(f"dataset-lock head must change only {LEDGER_REL}; changed={list(changed)}")
    if not git_path_exists(LEDGER_REL, parent):
        fail("result ledger must already exist at dataset-lock parent")
    if not LEDGER_PATH.is_file() or not git_path_exists(LEDGER_REL, head):
        fail("result ledger is absent at dataset-lock head")

    before = load_records_text(git("show", f"{parent}:{LEDGER_REL}"), "parent result ledger")
    after = load_records(LEDGER_PATH)
    validate_transition(before, after)

    print("TRACK_A_EPOCH_002_DATASET_LOCK=VALIDATED_NONAUTHORIZING_EVENT")
    print("DATASET_LOCK_AUTHORIZATION_EFFECT=REQUIRES_SEPARATE_EXACT_COMMIT")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_boundary() -> None:
    if LEDGER_PATH.exists() or git_path_exists(LEDGER_REL):
        validate_retained_ledger(LEDGER_PATH, require_lock=False)
    print("TRACK_A_EPOCH_002_DATASET_LOCK_TOOLING=PASS_LOCK_ABSENT")
    print("DATASET_LOCK_ESTABLISHED=FALSE")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("SCIENTIFIC_N_INCREMENT=0")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--validate", action="store_true")
    mode.add_argument("--expect-absent", action="store_true")
    parser.add_argument("--expected-base-sha")
    args = parser.parse_args(argv)

    if args.validate:
        if args.expected_base_sha is None:
            fail("--validate requires --expected-base-sha")
        validate_event(args.expected_base_sha)
    else:
        if args.expected_base_sha is not None:
            fail("--expected-base-sha is valid only with --validate")
        validate_boundary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
