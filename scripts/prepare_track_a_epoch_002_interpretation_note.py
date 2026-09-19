#!/usr/bin/env python3
"""Prepare an external Epoch 002 interpretation packet and content-addressed note.

The numerical estimate, confidence interval, and classification remain in the
external local packet. The repository note contains only the packet SHA-256 and
the accepted locked-result event identity.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import validate_track_a_epoch_002_interpretation as validator


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-output", type=Path, required=True)
    parser.add_argument("--interpretation-packet", type=Path, required=True)
    parser.add_argument("--output-record", type=Path, required=True)
    parser.add_argument("--parent-ref", default="HEAD")
    args = parser.parse_args()

    analysis_output = validator.require_external_regular_file(
        args.analysis_output,
        "locked analysis output",
    )
    packet_destination = validator.require_external_new_path(
        args.interpretation_packet,
        "interpretation packet",
    )

    packet, result_event = validator.build_local_interpretation_packet(
        analysis_output.read_bytes(),
        ref=args.parent_ref,
    )
    packet_bytes = validator.canonical_json_bytes(packet)
    packet_sha256 = validator.packet_sha256(packet)

    parent_sha = validator.git("rev-parse", args.parent_ref)
    note = validator.expected_note_record(
        result_event_sha=result_event,
        packet_sha256=packet_sha256,
        interpretation_parent_sha=parent_sha,
        generated_at_utc=(
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        ),
    )
    validator.validate_note_record(
        note,
        result_event_sha=result_event,
        interpretation_parent_sha=parent_sha,
    )

    note_destination = args.output_record.expanduser().resolve()
    if note_destination.exists():
        raise SystemExit("refusing to overwrite an existing interpretation-note candidate")

    packet_destination.parent.mkdir(parents=True, exist_ok=True)
    note_destination.parent.mkdir(parents=True, exist_ok=True)
    packet_destination.write_bytes(packet_bytes)
    note_destination.write_bytes(validator.canonical_json_bytes(note))

    print("TRACK_A_EPOCH_002_LOCAL_INTERPRETATION_PACKET=PREPARED_EXTERNAL")
    print(f"INTERPRETATION_PACKET_SHA256={packet_sha256}")
    print(f"INTERPRETATION_PACKET_PATH={packet_destination}")
    print("TRACK_A_EPOCH_002_INTERPRETATION_NOTE_CANDIDATE=PREPARED")
    print(f"INTERPRETATION_NOTE_PATH={note_destination}")
    print("NUMERICAL_OUTCOME_COPIED_TO_REPOSITORY_RECORD=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
