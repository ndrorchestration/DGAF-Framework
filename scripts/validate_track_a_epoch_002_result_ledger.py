#!/usr/bin/env python3
"""Fail-closed structural validator for Track A Epoch 002 result-record ledgers.

This tool validates retained prospective records only. It cannot create records,
authorize collection, unblind labels, run analysis, or advance scientific state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
PER_SEED_RECORD_COUNT = 50
ORDER = (
    [
        "PRECOLLECTION_GATE_CHECKLIST",
        "COLLECTION_START_RECEIPT",
    ]
    + ["PER_SEED_EXECUTION_RECORD"] * PER_SEED_RECORD_COUNT
    + [
        "QC_LEDGER",
        "DATASET_LOCK_RECEIPT",
        "UNBLINDING_DECISION_RECORD",
        "MATERIALIZATION_RECEIPT",
        "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD",
        "LOCKED_ANALYSIS_RESULT_RECORD",
        "INTERPRETATION_NOTE",
    ]
)


def load_records(path: Path) -> list[dict]:
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("ledger must be a JSON array")
    return records


def validate_ledger(path: Path) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    records = load_records(path)

    if not records:
        raise ValueError("ledger must contain at least one retained record")

    seen_ids: set[str] = set()
    expected_index = 0
    prior_id: str | None = None
    terminal_seen = False

    for record in records:
        errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
        if errors:
            raise ValueError(f"schema-invalid record: {errors[0].message}")

        record_id = record["record_id"]
        if record_id in seen_ids:
            raise ValueError(f"duplicate record_id: {record_id}")
        seen_ids.add(record_id)

        if terminal_seen:
            raise ValueError("records cannot follow a non-PASS record")
        if expected_index >= len(ORDER):
            raise ValueError("ledger contains more records than the defined ordered sequence")

        record_type = record["record_type"]
        if record_type != ORDER[expected_index]:
            raise ValueError(
                f"invalid record order: expected {ORDER[expected_index]}, got {record_type}"
            )

        predecessors = record["predecessor_record_ids"]
        if prior_id is None:
            if predecessors:
                raise ValueError("first record must not declare predecessors")
        elif prior_id not in predecessors:
            raise ValueError(f"record {record_id} must reference prior record {prior_id}")

        if record["status"] != "PASS":
            terminal_seen = True
        prior_id = record_id
        expected_index += 1

    if len(records) > len(ORDER):
        raise ValueError("ledger contains more records than the defined ordered sequence")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    validate_ledger(args.ledger)
    print("TRACK_A_EPOCH_002_RESULT_LEDGER_PASS_STRUCTURAL_ONLY")


if __name__ == "__main__":
    main()
