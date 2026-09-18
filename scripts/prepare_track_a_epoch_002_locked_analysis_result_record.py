#!/usr/bin/env python3
"""Prepare a content-addressed Track A Epoch 002 locked-analysis result record.

This local operator helper reads the retained analysis output only to validate its
frozen structure and compute its SHA-256. Numerical outcomes are not copied into
the repository result record.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import validate_track_a_epoch_002_locked_analysis_result as validator


def canonical_json_bytes(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-output", type=Path, required=True)
    parser.add_argument("--output-record", type=Path, required=True)
    parser.add_argument("--parent-ref", default="HEAD")
    args = parser.parse_args()

    analysis_output = validator.require_external_regular_file(args.analysis_output, "locked analysis output")
    authorization_event, _ = validator.validate_authorization_history(args.parent_ref)
    parent_sha = validator.git("rev-parse", args.parent_ref)
    output_sha256 = validator.validate_local_output_bytes(
        analysis_output.read_bytes(),
        authorization_event_sha=authorization_event,
    )

    record = validator.expected_result_record(
        authorization_event_sha=authorization_event,
        output_sha256=output_sha256,
        result_parent_sha=parent_sha,
        generated_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    validator.validate_result_record(
        record,
        authorization_event_sha=authorization_event,
        result_parent_sha=parent_sha,
    )

    destination = args.output_record.expanduser().resolve()
    if destination.exists():
        raise SystemExit("refusing to overwrite an existing result record candidate")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(canonical_json_bytes(record))

    print("TRACK_A_EPOCH_002_RESULT_RECORD_CANDIDATE=PREPARED")
    print(f"LOCKED_ANALYSIS_OUTPUT_SHA256={output_sha256}")
    print(f"RESULT_RECORD_PATH={destination}")
    print("NUMERICAL_OUTCOME_COPIED_TO_RECORD=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
