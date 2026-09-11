#!/usr/bin/env python3
"""Validate the fail-closed Track A Epoch 002 dataset-lock boundary.

The evidence manifest is a content-addressed description of retained blinded
collection/QC evidence. The repository receipt is a later one-file state event.
Neither surface creates authority to unblind, analyze, or promote scientific
state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, NoReturn, cast

from jsonschema import Draft202012Validator

from scripts import validate_track_a_epoch_002_result_ledger as structural
from scripts import validate_track_a_epoch_002_result_record_semantics as semantics

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = Path(__file__).resolve()
EVIDENCE_SCHEMA_PATH = (
    ROOT / "docs/experiment/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE_SCHEMA.json"
)
RESULT_SCHEMA_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
RECEIPT_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json"
)
RECEIPT_PATH = ROOT / RECEIPT_REL
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
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


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid or missing {label}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be one JSON object")
    return cast(dict[str, Any], value)


def load_records(path: Path) -> list[dict[str, Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid or missing result ledger: {exc}")
    return require_record_list(value)


def require_record_list(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        fail("result ledger must be a JSON array")
    if any(not isinstance(record, dict) for record in value):
        fail("result ledger entries must be JSON objects")
    return cast(list[dict[str, Any]], value)


def validate_with_existing_validators(records: list[dict[str, Any]]) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".json"
    ) as handle:
        json.dump(records, handle, sort_keys=True)
        handle.flush()
        path = Path(handle.name)
        try:
            structural.validate_ledger(path)
            semantics.validate_ledger(path)
        except (ValueError, SystemExit) as exc:
            fail(
                "retained ledger violates existing structural/semantic contract: "
                f"{exc}"
            )


def validate_prelock_ledger(records: list[dict[str, Any]]) -> str:
    validate_with_existing_validators(records)
    expected_prefix = structural.ORDER[:LOCK_INDEX]
    actual_prefix = [record.get("record_type") for record in records]
    if len(records) != LOCK_INDEX or actual_prefix != expected_prefix:
        fail(
            "pre-lock ledger must be complete through QC_LEDGER with all 50 seed "
            "records"
        )
    if any(record.get("status") != "PASS" for record in records):
        fail(
            "pre-lock ledger must be complete through QC_LEDGER with only PASS "
            "predecessors"
        )
    qc = records[-1]
    qc_id = qc.get("record_id")
    if (
        qc.get("record_type") != "QC_LEDGER"
        or not isinstance(qc_id, str)
        or not qc_id
    ):
        fail("pre-lock ledger must terminate at an identified QC_LEDGER")
    return qc_id


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


def validate_transition(
    before: list[dict[str, Any]], after: list[dict[str, Any]]
) -> None:
    if len(after) != len(before) + 1 or after[:-1] != before:
        fail(
            "dataset-lock event must append exactly one record without predecessor "
            "rewrites"
        )
    qc_id = validate_prelock_ledger(before)
    validate_lock_record(after[-1], qc_id)
    validate_with_existing_validators(after)


def validate_retained_ledger(path: Path, *, require_lock: bool) -> None:
    records = load_records(path)
    validate_with_existing_validators(records)
    has_lock = any(
        record.get("record_type") == "DATASET_LOCK_RECEIPT" for record in records
    )
    if require_lock:
        if not has_lock or records[-1].get("record_type") != "DATASET_LOCK_RECEIPT":
            fail("retained ledger must terminate at DATASET_LOCK_RECEIPT")
    elif has_lock:
        fail("current boundary requires DATASET_LOCK_RECEIPT to remain absent")


def validate_schema(instance: object, schema_path: Path, label: str) -> None:
    schema = load_object(schema_path, f"{label} schema")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # pragma: no cover - repository schema defect
        fail(f"invalid {label} schema: {exc}")
    errors = list(Draft202012Validator(schema).iter_errors(instance))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "<root>"
        fail(f"{label} schema violation at {location}: {first.message}")


def validate_evidence_manifest(manifest: dict[str, Any]) -> None:
    validate_schema(manifest, EVIDENCE_SCHEMA_PATH, "evidence manifest")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        fail(f"cannot hash evidence manifest: {exc}")
    return digest.hexdigest()


def validate_receipt_against_manifest(
    receipt: dict[str, Any], manifest: dict[str, Any], manifest_sha256: str
) -> None:
    validate_evidence_manifest(manifest)
    if not HEX64.fullmatch(manifest_sha256):
        fail("evidence manifest digest must be one lowercase SHA-256")
    validate_schema(receipt, RESULT_SCHEMA_PATH, "dataset-lock receipt")
    try:
        semantics.validate_record_semantics(receipt, semantics.validate_policy())
    except SystemExit as exc:
        fail(f"dataset-lock receipt semantic violation: {exc}")
    qc_id = manifest.get("qc_record_id")
    if not isinstance(qc_id, str):
        fail("evidence manifest QC_LEDGER identity is missing")
    validate_lock_record(receipt, qc_id)
    if receipt.get("immutable_subject") != {"sha256": manifest_sha256}:
        fail("dataset-lock receipt evidence manifest digest mismatch")


def require_event_shape(
    *,
    changed_paths: list[str],
    receipt_history: list[str],
    head_sha: str,
    receipt_existed_at_parent: bool,
) -> None:
    if changed_paths != [RECEIPT_REL]:
        fail(f"dataset-lock event must change only {RECEIPT_REL}; got {changed_paths}")
    if receipt_existed_at_parent:
        fail("dataset-lock receipt unexpectedly existed at parent")
    if receipt_history != [head_sha]:
        fail("dataset-lock receipt must have one first-and-only history entry at HEAD")


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
        fail(
            f"dataset-lock head parent {parent} does not equal expected base {base}"
        )
    return parent


def validate_event(
    expected_base_sha: str, evidence_manifest_path: Path, result_ledger_path: Path
) -> None:
    parent = event_parent(expected_base_sha)
    head = git("rev-parse", "HEAD").lower()
    changed = [
        line
        for line in git(
            "diff-tree", "--no-commit-id", "--name-only", "-r", head
        ).splitlines()
        if line
    ]
    history = [
        line
        for line in git("log", "--format=%H", "--", RECEIPT_REL).splitlines()
        if line
    ]
    require_event_shape(
        changed_paths=changed,
        receipt_history=history,
        head_sha=head,
        receipt_existed_at_parent=git_path_exists(RECEIPT_REL, parent),
    )
    if not RECEIPT_PATH.is_file() or not git_path_exists(RECEIPT_REL, head):
        fail("dataset-lock receipt is absent at event head")

    records = load_records(result_ledger_path)
    qc_id = validate_prelock_ledger(records)
    manifest = load_object(evidence_manifest_path, "evidence manifest")
    validate_evidence_manifest(manifest)
    if manifest.get("qc_record_id") != qc_id:
        fail(
            "evidence manifest QC_LEDGER identity does not match retained pre-lock "
            "ledger"
        )
    manifest_digest = sha256_file(evidence_manifest_path)
    receipt = load_object(RECEIPT_PATH, "dataset-lock receipt")
    validate_receipt_against_manifest(receipt, manifest, manifest_digest)

    print("TRACK_A_EPOCH_002_DATASET_LOCK=VALIDATED_NONAUTHORIZING_EVENT")
    print(f"DATASET_LOCK_EVIDENCE_SHA256={manifest_digest}")
    print("DATASET_LOCK_AUTHORIZATION_EFFECT=REQUIRES_SEPARATE_EXACT_COMMIT")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_manifest_file(path: Path) -> None:
    manifest = load_object(path, "evidence manifest")
    validate_evidence_manifest(manifest)
    print(
        "TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE=PASS "
        f"SHA256={sha256_file(path)}"
    )


def validate_boundary() -> None:
    if RECEIPT_PATH.exists() or git_path_exists(RECEIPT_REL):
        fail("tooling mode requires canonical DATASET_LOCK_RECEIPT to remain absent")
    print("TRACK_A_EPOCH_002_DATASET_LOCK_TOOLING=PASS_LOCK_ABSENT")
    print("DATASET_LOCK_ESTABLISHED=FALSE")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("SCIENTIFIC_N_INCREMENT=0")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--validate-event", action="store_true")
    mode.add_argument("--validate-evidence-manifest", type=Path)
    mode.add_argument("--expect-absent", action="store_true")
    parser.add_argument("--expected-base-sha")
    parser.add_argument("--evidence-manifest", type=Path)
    parser.add_argument("--result-ledger", type=Path)
    args = parser.parse_args(argv)

    if args.validate_event:
        required = (
            args.expected_base_sha,
            args.evidence_manifest,
            args.result_ledger,
        )
        if any(value is None for value in required):
            fail(
                "--validate-event requires --expected-base-sha, --evidence-manifest, "
                "and --result-ledger"
            )
        validate_event(
            cast(str, args.expected_base_sha),
            cast(Path, args.evidence_manifest),
            cast(Path, args.result_ledger),
        )
    elif args.validate_evidence_manifest is not None:
        if any(
            value is not None
            for value in (
                args.expected_base_sha,
                args.evidence_manifest,
                args.result_ledger,
            )
        ):
            fail("manifest-only validation does not accept event arguments")
        validate_manifest_file(args.validate_evidence_manifest)
    else:
        if any(
            value is not None
            for value in (
                args.expected_base_sha,
                args.evidence_manifest,
                args.result_ledger,
            )
        ):
            fail("--expect-absent does not accept event arguments")
        validate_boundary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
