#!/usr/bin/env python3
"""Validate non-authorizing admission of the operator-executed Epoch 002 collection."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/experiment/TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION_SCHEMA.json"
AUTHORIZATION_SHA = "563152fdb254b8ee948a693c287126a8bf8314b8"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_OPERATOR_ADMISSION_FAIL: {message}")


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {label}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be one JSON object")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_record(record: dict[str, Any]) -> None:
    schema = load_object(SCHEMA, "operator admission schema")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or "<root>"
        fail(f"schema-invalid at {location}: {error.message}")

    forbidden = {"collection_workflow_run_id", "evidence_workflow_run_id", "artifact_id"}
    if forbidden & set(record):
        fail("operator admission must not carry GitHub Actions collection identities")
    for retention_key in ("public_retention", "protected_retention"):
        retention = record[retention_key]
        if "artifact_id" in retention:
            fail("operator retention must not carry GitHub Actions artifact IDs")

    if record["collection_authorization_commit_sha"] != AUTHORIZATION_SHA:
        fail("collection authorization identity drift")
    if record["frozen_candidate_sha"] == record["collection_authorization_commit_sha"]:
        fail("frozen candidate must predate collection authorization")


def validate_archives(
    record: dict[str, Any],
    public_archive: Path,
    protected_archive: Path,
) -> None:
    for path, key, label in (
        (public_archive, "public_retention", "public"),
        (protected_archive, "protected_retention", "protected"),
    ):
        if not path.is_file():
            fail(f"{label} archive missing")
        spec = record[key]
        if path.stat().st_size != spec["size_bytes"]:
            fail(f"{label} archive size mismatch")
        if sha256_file(path) != spec["archive_sha256"]:
            fail(f"{label} archive SHA-256 mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--public-archive", type=Path)
    parser.add_argument("--protected-archive", type=Path)
    args = parser.parse_args()

    record = load_object(args.record, "operator admission record")
    validate_record(record)
    if (args.public_archive is None) != (args.protected_archive is None):
        fail("archive validation requires both public and protected archives")
    if args.public_archive is not None and args.protected_archive is not None:
        validate_archives(record, args.public_archive, args.protected_archive)

    print("TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION=PASS_NONAUTHORIZING")
    print("TRACK_A_EPOCH_002_DATASET_LOCK=NOT_ESTABLISHED")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
