#!/usr/bin/env python3
"""Prepare local Track A Epoch 002 interpretation and content-addressed repository note."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import validate_track_a_epoch_002_interpretation as interpretation
import validate_track_a_epoch_002_locked_analysis_result as result_validator


def canonical_json_bytes(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def refuse_existing(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if resolved.exists():
        raise SystemExit(f"refusing to overwrite existing {label}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-output", type=Path, required=True)
    parser.add_argument("--local-interpretation-output", type=Path, required=True)
    parser.add_argument("--output-record", type=Path, required=True)
    parser.add_argument("--parent-ref", default="HEAD")
    args = parser.parse_args()

    analysis_output = result_validator.require_external_regular_file(args.analysis_output, "locked analysis output")
    local_destination = refuse_existing(args.local_interpretation_output, "local interpretation artifact")
    if not result_validator.outside_repository(local_destination):
        raise SystemExit("local interpretation artifact must remain outside the repository")

    result_event, accepted_output_sha256 = interpretation.accepted_result_binding(args.parent_ref)
    authorization_event, _ = result_validator.validate_authorization_history(args.parent_ref)
    output_bytes = analysis_output.read_bytes()
    observed_output_sha256 = result_validator.validate_local_output_bytes(
        output_bytes,
        authorization_event_sha=authorization_event,
    )
    if observed_output_sha256 != accepted_output_sha256:
        raise SystemExit("retained locked-analysis output does not match the accepted result receipt")

    output = result_validator.load_json_bytes(output_bytes, "retained locked-analysis output")
    result = output["result"]
    local_artifact = interpretation.expected_local_interpretation(
        result_event_sha=result_event,
        locked_output_sha256=observed_output_sha256,
        result=result,
    )
    interpretation.validate_local_interpretation(
        local_artifact,
        result_event_sha=result_event,
        locked_output_sha256=observed_output_sha256,
        result=result,
    )

    local_destination.parent.mkdir(parents=True, exist_ok=True)
    local_bytes = canonical_json_bytes(local_artifact)
    local_destination.write_bytes(local_bytes)
    interpretation_sha256 = interpretation.validate_external_interpretation_bytes(
        local_bytes,
        result_event_sha=result_event,
        locked_output_sha256=observed_output_sha256,
        result=result,
    )

    parent_sha = result_validator.git("rev-parse", args.parent_ref)
    note = interpretation.expected_repository_note(
        result_event_sha=result_event,
        interpretation_sha256=interpretation_sha256,
        parent_sha=parent_sha,
        generated_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    interpretation.validate_repository_note(note, result_event_sha=result_event, parent_sha=parent_sha)

    record_destination = refuse_existing(args.output_record, "interpretation note candidate")
    record_destination.parent.mkdir(parents=True, exist_ok=True)
    record_destination.write_bytes(canonical_json_bytes(note))

    print("TRACK_A_EPOCH_002_LOCAL_INTERPRETATION=PREPARED")
    print(f"LOCKED_ANALYSIS_OUTPUT_SHA256={observed_output_sha256}")
    print(f"LOCAL_INTERPRETATION_SHA256={interpretation_sha256}")
    print(f"LOCAL_INTERPRETATION_PATH={local_destination}")
    print(f"INTERPRETATION_NOTE_CANDIDATE_PATH={record_destination}")
    print("NUMERICAL_OUTCOME_COPIED_TO_REPOSITORY_NOTE=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
