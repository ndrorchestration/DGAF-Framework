#!/usr/bin/env python3
"""Fail-closed validator for Track A Epoch 002 post-interpretation disposition.

This gate is outcome-agnostic. It evaluates only whether the accepted result and
interpretation lifecycle is complete and immutable at its bounded scope. It never
reads the operator-local numerical result or interpretation.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
CONTROLLER_ISSUE = 879
RECORD_ID = "E002-POST-INTERPRET-DISPOSITION-0001"
RECORD_TYPE = "TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION"
PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION_VALIDATOR"
INTERPRETATION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_INTERPRETATION_NOTE.json"
RESULT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
DISPOSITION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION.json"
INTERPRETATION_VALIDATOR_REL = "scripts/validate_track_a_epoch_002_interpretation.py"

CLOSED = "CLOSED_BOUNDED_SAME_SYSTEM_NONINDEPENDENT"
OPEN_DEFECT = "OPEN_SPECIFIC_DEFECT"
EVIDENCE_CLASS = "SAME_SYSTEM_NONINDEPENDENT"

NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_AUTHORIZE_NEW_EMPIRICAL_EPOCH",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
    "DOES_NOT_MUTATE_ACCEPTED_RESULT",
    "DOES_NOT_MUTATE_ACCEPTED_INTERPRETATION",
    "DOES_NOT_AUTHORIZE_HISTORICAL_POOLING",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION_FAIL: {message}")


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load module {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def interpretation_validator() -> Any:
    return load_module(
        ROOT / INTERPRETATION_VALIDATOR_REL,
        "track_a_epoch_002_interpretation_for_disposition",
    )


def load_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        fail(f"{label} is invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be one JSON object")
    return value


def validate_predecessors(ref: str = "HEAD") -> dict[str, str]:
    iv = interpretation_validator()
    event = iv.validate_accepted_interpretation(ref)
    result_event, _ = iv.accepted_result_binding(ref)

    note = load_json_bytes(iv.result_validator().git_bytes(ref, INTERPRETATION_REL), "interpretation note")
    result = load_json_bytes(iv.result_validator().git_bytes(ref, RESULT_REL), "locked analysis result record")

    if note.get("record_type") != "INTERPRETATION_NOTE":
        fail("interpretation note record type drift")
    if note.get("record_id") != "E002-INTERPRET-0001":
        fail("interpretation note record id drift")
    if note.get("evidence_scope") != "INTERPRETATION_CONTENT_ADDRESS_ONLY_SAME_SYSTEM_NONINDEPENDENT":
        fail("interpretation evidence scope drift")
    if note.get("status") != "PASS" or note.get("authorization_effect") != "NONE":
        fail("interpretation admission semantics drift")
    if note.get("scientific_state_effect") != {
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "empirical_n_increment": 0,
    }:
        fail("interpretation scientific-state ceiling drift")

    if result.get("record_type") != "LOCKED_ANALYSIS_RESULT_RECORD":
        fail("locked result record type drift")
    if result.get("record_id") != "E002-ANALYSIS-RESULT-0001":
        fail("locked result record id drift")
    if note.get("predecessor_record_ids") != ["E002-ANALYSIS-RESULT-0001"]:
        fail("interpretation predecessor binding drift")

    git = iv.result_validator().git
    return {
        "interpretation_event_commit_sha": event,
        "interpretation_note_blob_sha": git("rev-parse", f"{ref}:{INTERPRETATION_REL}"),
        "locked_result_event_commit_sha": result_event,
        "locked_result_record_blob_sha": git("rev-parse", f"{ref}:{RESULT_REL}"),
    }


def expected_record(
    *,
    parent_sha: str,
    generated_at_utc: str,
    disposition: str = CLOSED,
    defect: dict[str, Any] | None = None,
) -> dict[str, Any]:
    bindings = validate_predecessors(parent_sha)

    if disposition == CLOSED:
        if defect is not None:
            fail("closed disposition cannot carry a defect")
        lane_state = "CLOSED_FOR_EXACT_PREREGISTERED_SCOPE"
        mutation_allowed = False
    elif disposition == OPEN_DEFECT:
        if not isinstance(defect, dict):
            fail("OPEN_SPECIFIC_DEFECT requires a defect object")
        defect_id = defect.get("defect_id")
        summary = defect.get("summary")
        evidence_refs = defect.get("evidence_refs")
        if not isinstance(defect_id, str) or not re.fullmatch(r"[A-Z0-9][A-Z0-9_.-]{2,127}", defect_id):
            fail("specific defect id is malformed")
        if not isinstance(summary, str) or len(summary.strip()) < 12:
            fail("specific defect summary is too short")
        if (
            not isinstance(evidence_refs, list)
            or not evidence_refs
            or not all(isinstance(x, str) and x.strip() for x in evidence_refs)
        ):
            fail("specific defect requires nonempty evidence refs")
        lane_state = "OPEN_ONLY_FOR_NAMED_DEFECT_REMEDIATION"
        mutation_allowed = False
    else:
        fail("unknown disposition")

    return {
        "record_type": RECORD_TYPE,
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "record_id": RECORD_ID,
        "controller_issue": CONTROLLER_ISSUE,
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": parent_sha,
        },
        "predecessor_record_ids": [
            "E002-ANALYSIS-RESULT-0001",
            "E002-INTERPRET-0001",
        ],
        "immutable_subject": bindings,
        "disposition": disposition,
        "specific_defect": defect,
        "evidence_class": EVIDENCE_CLASS,
        "lane_effect": {
            "epoch_002_lifecycle": lane_state,
            "accepted_result_mutation_allowed": mutation_allowed,
            "accepted_interpretation_mutation_allowed": mutation_allowed,
            "rerun_authorized": False,
            "historical_pooling_authorized": False,
        },
        "future_work": {
            "independent_replication": "REQUIRES_SEPARATE_PROPOSAL_PREREGISTRATION_AND_AUTHORIZATION",
            "new_empirical_epoch_authorized": False,
            "claim_promotion_authorized": False,
        },
        "authorization_effect": "NONE",
        "non_effects": list(NON_EFFECTS),
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "independent_validation": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED_N0",
        },
    }


def validate_record(record: dict[str, Any], *, parent_sha: str) -> None:
    disposition = record.get("disposition")
    expected = expected_record(
        parent_sha=parent_sha,
        generated_at_utc=str(record.get("generated_at_utc", "")),
        disposition=str(disposition),
        defect=record.get("specific_defect"),
    )
    if record != expected:
        fail("disposition record does not match the exact outcome-agnostic contract")

    rendered = json.dumps(record, sort_keys=True)
    forbidden = (
        "estimate_pdmal_minus_random_regular",
        "two_sided_95pct_percentile_ci",
        "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS",
        "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS",
        "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED",
    )
    if any(token in rendered for token in forbidden):
        fail("protected numerical/classification interpretation leaked into disposition record")


def validate_tooling_only() -> None:
    iv = interpretation_validator()
    validate_predecessors("HEAD")
    if (ROOT / DISPOSITION_REL).exists() or iv.result_validator().git_object_exists(f"HEAD:{DISPOSITION_REL}"):
        fail("tooling mode requires the disposition record to remain absent")
    record = expected_record(
        parent_sha=iv.result_validator().git("rev-parse", "HEAD"),
        generated_at_utc="2026-01-01T00:00:00Z",
    )
    validate_record(record, parent_sha=iv.result_validator().git("rev-parse", "HEAD"))


def validate_disposition_event(head: str, *, accepted_parent_sha: str) -> str:
    iv = interpretation_validator()
    rv = iv.result_validator()
    head = rv.git("rev-parse", head)
    lineage = rv.git("rev-list", "--parents", "-n", "1", head).split()
    if len(lineage) != 2 or lineage[0] != head:
        fail("disposition event must have exactly one parent")
    parent = lineage[1]
    if parent != accepted_parent_sha:
        fail("disposition parent is not the accepted protected-main parent")

    changed = [line for line in rv.git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines() if line]
    if changed != [DISPOSITION_REL]:
        fail("disposition event must create exactly the canonical disposition record")
    if rv.git_object_exists(f"{parent}:{DISPOSITION_REL}"):
        fail("disposition record must be creation-only")
    history = [line for line in rv.git("log", "--format=%H", head, "--", DISPOSITION_REL).splitlines() if line]
    if history != [head]:
        fail("disposition record must have first-and-only immutable history")

    for rel in (RESULT_REL, INTERPRETATION_REL):
        if rv.git_bytes(parent, rel) != rv.git_bytes(head, rel):
            fail(f"accepted predecessor bytes changed during disposition event: {rel}")

    record = load_json_bytes(rv.git_bytes(head, DISPOSITION_REL), "post-interpretation disposition")
    validate_record(record, parent_sha=parent)
    return parent


def validate_accepted_disposition(ref: str = "HEAD") -> str:
    iv = interpretation_validator()
    rv = iv.result_validator()
    if not rv.git_object_exists(f"{ref}:{DISPOSITION_REL}"):
        fail("accepted-state validation requires the disposition record")
    history = [line for line in rv.git("log", "--format=%H", ref, "--", DISPOSITION_REL).splitlines() if line]
    if len(history) != 1:
        fail("disposition record must have one immutable history event")
    event = history[0]
    lineage = rv.git("rev-list", "--parents", "-n", "1", event).split()
    if len(lineage) != 2 or lineage[0] != event:
        fail("accepted disposition event must have exactly one parent")
    parent = lineage[1]
    changed = [line for line in rv.git("diff-tree", "--no-commit-id", "--name-only", "-r", event).splitlines() if line]
    if changed != [DISPOSITION_REL]:
        fail("accepted disposition event changed more than its canonical record")
    if rv.git_object_exists(f"{parent}:{DISPOSITION_REL}"):
        fail("accepted disposition record is not creation-only")
    for rel in (RESULT_REL, INTERPRETATION_REL):
        if rv.git_bytes(parent, rel) != rv.git_bytes(event, rel):
            fail(f"accepted predecessor bytes changed during disposition event: {rel}")
    record = load_json_bytes(rv.git_bytes(event, DISPOSITION_REL), "accepted post-interpretation disposition")
    validate_record(record, parent_sha=parent)
    return event


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--tooling", action="store_true")
    mode.add_argument("--event-commit")
    mode.add_argument("--accepted-state", action="store_true")
    parser.add_argument("--accepted-parent")
    args = parser.parse_args()

    if args.tooling:
        validate_tooling_only()
        print("TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION_TOOLING=PASS_NONEXECUTING")
        print("POST_INTERPRETATION_DISPOSITION=NOT_ESTABLISHED")
    elif args.accepted_state:
        validate_accepted_disposition("HEAD")
        print("TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION=ESTABLISHED_PRESERVED")
    else:
        if not args.accepted_parent:
            fail("--accepted-parent is required for event validation")
        validate_disposition_event(args.event_commit, accepted_parent_sha=args.accepted_parent)
        print("TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION_EVENT=VALIDATED_PENDING_ACCEPTANCE")

    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")
    print("NEW_EMPIRICAL_EPOCH_AUTHORIZED=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
