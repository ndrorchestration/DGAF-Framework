#!/usr/bin/env python3
"""Prepare a repository-safe Track A Epoch 002 post-interpretation disposition candidate."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import validate_track_a_epoch_002_post_interpretation_disposition as disposition


def canonical_json_bytes(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-record", type=Path, required=True)
    parser.add_argument("--parent-ref", default="HEAD")
    args = parser.parse_args()

    output = args.output_record.expanduser().resolve()
    if output.exists():
        raise SystemExit("refusing to overwrite existing disposition candidate")

    iv = disposition.interpretation_validator()
    parent_sha = iv.result_validator().git("rev-parse", args.parent_ref)
    record = disposition.expected_record(
        parent_sha=parent_sha,
        generated_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        disposition=disposition.CLOSED,
        defect=None,
    )
    disposition.validate_record(record, parent_sha=parent_sha)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_json_bytes(record))

    print("TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION_CANDIDATE=PREPARED")
    print(f"DISPOSITION={disposition.CLOSED}")
    print(f"DISPOSITION_CANDIDATE_PATH={output}")
    print("PRIVATE_NUMERICAL_INTERPRETATION_REQUIRED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")
    print("NEW_EMPIRICAL_EPOCH_AUTHORIZED=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
