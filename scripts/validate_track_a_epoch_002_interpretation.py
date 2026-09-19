#!/usr/bin/env python3
"""Fail-closed Track A Epoch 002 interpretation/adjudication validator.

Repository tooling never imports empirical numerical outcomes into CI. Local
operator tooling may validate the retained locked-analysis output and construct
an external interpretation packet. The repository INTERPRETATION_NOTE stores
only the packet content address and the accepted locked-result event identity.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
RESULT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
NOTE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_INTERPRETATION_NOTE.json"
SCHEMA_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
SEMANTICS_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json"
PREREG_REL = "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"
RESULT_VALIDATOR_REL = "scripts/validate_track_a_epoch_002_locked_analysis_result.py"

RESULT_RECORD_ID = "E002-ANALYSIS-RESULT-0001"
NOTE_RECORD_ID = "E002-INTERPRET-0001"
NOTE_SCOPE = "LOCAL_INTERPRETATION_PACKET_CONTENT_ADDRESS_ONLY"
PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_INTERPRETATION_VALIDATOR"

FULL_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]

EXPECTED_CONFIRMATORY_CONTRACT = {
    "research_question": (
        "Under the fixed reference neighbor-mean alpha-0.5 consensus algorithm, "
        "does the PDMAL topology yield higher failure-and-recovery success than "
        "the matched random-regular topology across the preregistered failure-count panel?"
    ),
    "directional_hypothesis": "PDMAL_TOPOLOGY_FFCR_GREATER_THAN_RANDOM_REGULAR",
    "algorithm_id": "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1",
    "endpoint": "ffcr_success",
    "primary_topology": "pdmal",
    "primary_comparator": "random_regular",
    "paired_seed_units": 50,
    "estimand": "mean of 50 paired_seed_effect values",
    "bootstrap": "paired_seed_effects_percentile",
    "bootstrap_resamples": 10000,
    "bootstrap_seed": 20270251,
    "confidence_interval": "two_sided_95_percentile",
    "alpha": 0.05,
    "confirmatory_test_count": 1,
}

EXPECTED_CLAIM_SCOPE = (
    "TRACK_A_PDMAL_VS_RANDOM_REGULAR_TOPOLOGY_ROBUSTNESS_"
    "UNDER_EXACT_FROZEN_REFERENCE_ALGORITHM_AND_PROTOCOL"
)

EXPECTED_SEPARATION_CONSTRAINTS = {
    "track_a_epoch_001_pooled": False,
    "epoch_003_pooled": False,
    "epoch_004_pooled": False,
    "structural_diagnostic_seeds_pooled": False,
    "other_topology_comparisons": "EXPLORATORY_ONLY",
    "failure_count_specific_effects": "EXPLORATORY_ONLY",
    "post_hoc_subgroups": "EXPLORATORY_ONLY",
    "confirmatory_relabeling_from_exploratory_results": False,
    "verification_class": "SAME_SYSTEM_NONINDEPENDENT",
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_INTERPRETATION_FAIL: {message}")


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def git_bytes(ref: str, relpath: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{ref}:{relpath}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        fail(f"cannot read {ref}:{relpath}: {detail}")
    return completed.stdout


def git_object_exists(spec: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", spec],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def load_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        fail(f"{label} is invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be one JSON object")
    return value


def load_repo_json(relpath: str) -> dict[str, Any]:
    try:
        return load_json_bytes((ROOT / relpath).read_bytes(), relpath)
    except OSError as exc:
        fail(f"cannot read {relpath}: {exc}")


def outside_repository(path: Path) -> bool:
    try:
        path.relative_to(ROOT)
    except ValueError:
        return True
    return False


def require_external_regular_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not outside_repository(resolved):
        fail(f"{label} must remain outside the repository")
    if resolved.is_symlink() or not resolved.is_file():
        fail(f"{label} must be an external regular file")
    return resolved


def require_external_new_path(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not outside_repository(resolved):
        fail(f"{label} must remain outside the repository")
    if resolved.exists():
        fail(f"refusing to overwrite existing {label}")
    return resolved


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load module {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def result_validator() -> Any:
    return load_module(
        ROOT / RESULT_VALIDATOR_REL,
        "track_a_epoch_002_result_for_interpretation",
    )


def validate_preregistered_contract() -> dict[str, Any]:
    prereg = load_repo_json(PREREG_REL)
    if prereg.get("protocol_id") != PROTOCOL_ID:
        fail("preregistration protocol drift")
    if prereg.get("research_question") != EXPECTED_CONFIRMATORY_CONTRACT["research_question"]:
        fail("preregistered research question drift")
    if prereg.get("directional_hypothesis") != EXPECTED_CONFIRMATORY_CONTRACT["directional_hypothesis"]:
        fail("preregistered directional hypothesis drift")

    algorithm = prereg.get("algorithm")
    endpoint = prereg.get("endpoint")
    analysis = prereg.get("primary_analysis")
    multiplicity = prereg.get("multiplicity_policy")
    historical = prereg.get("historical_evidence_policy")
    ceiling = prereg.get("claim_ceiling")
    if not all(isinstance(value, dict) for value in (algorithm, endpoint, analysis, multiplicity, historical, ceiling)):
        fail("preregistration contract sections are malformed")

    checks = {
        "algorithm_id": algorithm.get("public_id"),
        "endpoint": endpoint.get("field"),
        "primary_topology": analysis.get("primary_topology"),
        "primary_comparator": analysis.get("primary_comparator"),
        "paired_seed_units": prereg.get("sample_size_rationale", {}).get("paired_seed_units"),
        "estimand": analysis.get("estimand"),
        "bootstrap": analysis.get("bootstrap"),
        "bootstrap_resamples": analysis.get("bootstrap_resamples"),
        "bootstrap_seed": analysis.get("bootstrap_seed"),
        "confidence_interval": analysis.get("confidence_interval"),
        "alpha": analysis.get("alpha"),
        "confirmatory_test_count": multiplicity.get("confirmatory_test_count"),
    }
    for key, expected in EXPECTED_CONFIRMATORY_CONTRACT.items():
        if key in {"research_question", "directional_hypothesis"}:
            continue
        if checks.get(key) != expected:
            fail(f"preregistered confirmatory contract drift: {key}")

    if multiplicity.get("confirmatory_family") != ["pdmal_vs_random_regular"]:
        fail("confirmatory family drift")
    if multiplicity.get("other_topology_comparisons") != "EXPLORATORY_ONLY":
        fail("other-topology multiplicity policy drift")
    if multiplicity.get("failure_count_specific_effects") != "EXPLORATORY_ONLY":
        fail("failure-count multiplicity policy drift")
    if multiplicity.get("post_hoc_subgroups") != "EXPLORATORY_ONLY":
        fail("post-hoc subgroup policy drift")
    if multiplicity.get("confirmatory_relabeling_from_exploratory_results") is not False:
        fail("confirmatory relabeling prohibition drift")

    for key in (
        "pool_experiment_001",
        "pool_epoch_003",
        "pool_epoch_004",
        "pool_structural_diagnostic_seeds",
        "pool_track_a_epoch_001",
    ):
        if historical.get(key) is not False:
            fail(f"historical pooling prohibition drift: {key}")

    if ceiling.get("allowed_if_executed") != EXPECTED_CLAIM_SCOPE:
        fail("Track A exact-scope claim ceiling drift")
    if ceiling.get("canonical_dgaf_efficacy") != "NOT_ESTABLISHED":
        fail("canonical DGAF efficacy ceiling drift")
    if ceiling.get("integrated_track_c") != "NOT_ESTABLISHED":
        fail("integrated Track C ceiling drift")
    if ceiling.get("independent_validation") != "NOT_ESTABLISHED":
        fail("independent-validation ceiling drift")
    if ceiling.get("high_assurance") != "NOT_AUTHORIZED_N0":
        fail("High-Assurance ceiling drift")
    if ceiling.get("production_readiness") != "NOT_ESTABLISHED":
        fail("production-readiness ceiling drift")
    return prereg


def validate_result_history(ref: str = "HEAD") -> tuple[str, dict[str, Any]]:
    validator = result_validator()
    event = validator.validate_accepted_result(ref)
    record = load_json_bytes(git_bytes(ref, RESULT_REL), "accepted locked-analysis result")
    if record.get("record_id") != RESULT_RECORD_ID:
        fail("accepted locked-result record_id drift")
    if record.get("record_type") != "LOCKED_ANALYSIS_RESULT_RECORD":
        fail("accepted locked-result record_type drift")
    subject = record.get("immutable_subject")
    if not isinstance(subject, dict) or set(subject) != {"commit_sha", "sha256"}:
        fail("accepted locked-result immutable subject drift")
    if not isinstance(subject.get("sha256"), str) or len(subject["sha256"]) != 64:
        fail("accepted locked-result output digest is malformed")
    return event, record


def interpretation_statement(classification: str) -> str:
    statements = {
        "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS": (
            "The preregistered directional-support rule is satisfied for the exact "
            "frozen PDMAL-versus-random-regular contrast."
        ),
        "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS": (
            "The preregistered directional-negative rule is satisfied for the exact "
            "frozen PDMAL-versus-random-regular contrast."
        ),
        "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED": (
            "Neither preregistered directional rule is satisfied for the exact frozen "
            "PDMAL-versus-random-regular contrast."
        ),
    }
    if classification not in statements:
        fail("unknown locked-result classification")
    return statements[classification]


def expected_local_interpretation_packet(
    analysis_output: dict[str, Any],
    *,
    result_event_sha: str,
    output_sha256: str,
) -> dict[str, Any]:
    validate_preregistered_contract()
    result = analysis_output.get("result")
    if not isinstance(result, dict):
        fail("locked-analysis result is malformed")
    packet_result = {
        "estimate_pdmal_minus_random_regular": result.get("estimate_pdmal_minus_random_regular"),
        "two_sided_95pct_percentile_ci": result.get("two_sided_95pct_percentile_ci"),
        "classification": result.get("classification"),
    }
    classification = packet_result["classification"]
    return {
        "record_type": "TRACK_A_EPOCH_002_LOCAL_INTERPRETATION_PACKET",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "locked_analysis_result_event_commit_sha": result_event_sha,
        "locked_analysis_result_record_id": RESULT_RECORD_ID,
        "locked_analysis_output_sha256": output_sha256,
        "confirmatory_contract": dict(EXPECTED_CONFIRMATORY_CONTRACT),
        "result": packet_result,
        "interpretation": {
            "classification": classification,
            "statement": interpretation_statement(str(classification)),
            "claim_scope": EXPECTED_CLAIM_SCOPE,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "integrated_track_c": "NOT_ESTABLISHED",
            "independent_validation": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED_N0",
            "production_readiness": "NOT_ESTABLISHED",
        },
        "separation_constraints": dict(EXPECTED_SEPARATION_CONSTRAINTS),
        "scientific_n_increment": 0,
    }


def validate_local_interpretation_packet_object(
    packet: dict[str, Any],
    *,
    expected_result_event_sha: str,
    expected_output_sha256: str,
) -> None:
    expected_keys = {
        "record_type",
        "schema_version",
        "protocol_id",
        "locked_analysis_result_event_commit_sha",
        "locked_analysis_result_record_id",
        "locked_analysis_output_sha256",
        "confirmatory_contract",
        "result",
        "interpretation",
        "separation_constraints",
        "scientific_n_increment",
    }
    if set(packet) != expected_keys:
        fail("local interpretation packet field set drift")
    fixed = {
        "record_type": "TRACK_A_EPOCH_002_LOCAL_INTERPRETATION_PACKET",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "locked_analysis_result_event_commit_sha": expected_result_event_sha,
        "locked_analysis_result_record_id": RESULT_RECORD_ID,
        "locked_analysis_output_sha256": expected_output_sha256,
        "confirmatory_contract": EXPECTED_CONFIRMATORY_CONTRACT,
        "separation_constraints": EXPECTED_SEPARATION_CONSTRAINTS,
        "scientific_n_increment": 0,
    }
    for key, expected in fixed.items():
        if packet.get(key) != expected:
            fail(f"local interpretation packet binding drift: {key}")

    result = packet.get("result")
    if not isinstance(result, dict) or set(result) != {
        "estimate_pdmal_minus_random_regular",
        "two_sided_95pct_percentile_ci",
        "classification",
    }:
        fail("local interpretation result field set drift")

    estimate = result.get("estimate_pdmal_minus_random_regular")
    ci = result.get("two_sided_95pct_percentile_ci")
    classification = result.get("classification")
    if not isinstance(estimate, (int, float)) or isinstance(estimate, bool) or not math.isfinite(float(estimate)):
        fail("local interpretation estimate must be finite")
    if not isinstance(ci, list) or len(ci) != 2:
        fail("local interpretation confidence interval is malformed")
    if any(not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(float(x)) for x in ci):
        fail("local interpretation confidence interval must be finite")
    estimate_f = float(estimate)
    low, high = float(ci[0]), float(ci[1])
    if not (-1.0 <= estimate_f <= 1.0 and -1.0 <= low <= high <= 1.0):
        fail("local interpretation estimate or interval is outside the FFCR contrast range")

    validator = result_validator()
    expected_classification = validator.expected_classification(estimate_f, low, high)
    if classification != expected_classification:
        fail("local interpretation classification is inconsistent with estimate and interval")

    interpretation = packet.get("interpretation")
    expected_interpretation = {
        "classification": classification,
        "statement": interpretation_statement(str(classification)),
        "claim_scope": EXPECTED_CLAIM_SCOPE,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "integrated_track_c": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
        "production_readiness": "NOT_ESTABLISHED",
    }
    if interpretation != expected_interpretation:
        fail("local interpretation claim ceiling or statement drift")


def build_local_interpretation_packet(
    analysis_output_bytes: bytes,
    *,
    ref: str = "HEAD",
) -> tuple[dict[str, Any], str]:
    result_event, result_record = validate_result_history(ref)
    validate_preregistered_contract()

    subject = result_record["immutable_subject"]
    authorization_event_sha = subject["commit_sha"]
    expected_output_sha256 = subject["sha256"]

    validator = result_validator()
    actual_output_sha256 = validator.validate_local_output_bytes(
        analysis_output_bytes,
        authorization_event_sha=authorization_event_sha,
    )
    if actual_output_sha256 != expected_output_sha256:
        fail("retained local analysis output does not match the accepted result-record content address")

    analysis_output = load_json_bytes(analysis_output_bytes, "retained locked-analysis output")
    packet = expected_local_interpretation_packet(
        analysis_output,
        result_event_sha=result_event,
        output_sha256=actual_output_sha256,
    )
    validate_local_interpretation_packet_object(
        packet,
        expected_result_event_sha=result_event,
        expected_output_sha256=actual_output_sha256,
    )
    return packet, result_event


def validate_schema(record: dict[str, Any]) -> None:
    schema = load_repo_json(SCHEMA_REL)
    try:
        Draft202012Validator(schema).validate(record)
    except ValidationError as exc:
        fail(f"interpretation note schema validation failed: {exc.message}")


def validate_semantics(record: dict[str, Any]) -> None:
    semantics = load_repo_json(SEMANTICS_REL)
    records = semantics.get("records")
    profiles = semantics.get("profiles")
    if not isinstance(records, dict) or not isinstance(profiles, dict):
        fail("result-record semantic policy is malformed")
    if records.get("INTERPRETATION_NOTE") != {
        "authority_class": "NONAUTHORIZING_OBSERVATION",
        "pass_profile": "OBSERVATIONAL_PASS",
    }:
        fail("interpretation-note semantic classification drift")
    if profiles.get("OBSERVATIONAL_PASS") != {
        "authorization_effect": "NONE",
        "required_non_effects": FULL_NON_EFFECTS,
        "forbidden_non_effects": [],
    }:
        fail("observational PASS profile drift")
    if record.get("authorization_effect") != "NONE":
        fail("interpretation note cannot carry authorization")
    if record.get("non_effects") != FULL_NON_EFFECTS:
        fail("interpretation note must preserve the full non-effect ceiling")


def expected_note_record(
    *,
    result_event_sha: str,
    packet_sha256: str,
    interpretation_parent_sha: str,
    generated_at_utc: str,
) -> dict[str, Any]:
    return {
        "record_type": "INTERPRETATION_NOTE",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "record_id": NOTE_RECORD_ID,
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": interpretation_parent_sha,
        },
        "immutable_subject": {
            "commit_sha": result_event_sha,
            "sha256": packet_sha256,
        },
        "evidence_scope": NOTE_SCOPE,
        "non_effects": list(FULL_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": [RESULT_RECORD_ID],
        "authorization_effect": "NONE",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def validate_note_record(
    record: dict[str, Any],
    *,
    result_event_sha: str,
    interpretation_parent_sha: str,
) -> None:
    validate_schema(record)
    validate_semantics(record)
    subject = record.get("immutable_subject")
    if not isinstance(subject, dict) or set(subject) != {"commit_sha", "sha256"}:
        fail("interpretation-note immutable subject is malformed")
    packet_sha256 = subject.get("sha256")
    if not isinstance(packet_sha256, str) or len(packet_sha256) != 64:
        fail("interpretation packet digest is malformed")
    try:
        int(packet_sha256, 16)
    except ValueError:
        fail("interpretation packet digest is not hexadecimal")

    expected = expected_note_record(
        result_event_sha=result_event_sha,
        packet_sha256=packet_sha256,
        interpretation_parent_sha=interpretation_parent_sha,
        generated_at_utc=str(record.get("generated_at_utc", "")),
    )
    if record != expected:
        fail("interpretation note does not match the exact non-promotional admission contract")


def validate_tooling_only() -> None:
    result_event, _ = validate_result_history("HEAD")
    validate_preregistered_contract()
    candidate = expected_note_record(
        result_event_sha=result_event,
        packet_sha256="0" * 64,
        interpretation_parent_sha=git("rev-parse", "HEAD"),
        generated_at_utc="2026-01-01T00:00:00Z",
    )
    validate_note_record(
        candidate,
        result_event_sha=result_event,
        interpretation_parent_sha=git("rev-parse", "HEAD"),
    )
    if (ROOT / NOTE_REL).exists() or git_object_exists(f"HEAD:{NOTE_REL}"):
        fail("tooling mode requires the canonical interpretation note to remain absent")


def validate_note_event(head: str, *, accepted_parent_sha: str) -> str:
    head = git("rev-parse", head)
    lineage = git("rev-list", "--parents", "-n", "1", head).split()
    if len(lineage) != 2 or lineage[0] != head:
        fail("interpretation-note event must have exactly one parent")
    parent = lineage[1]
    if parent != accepted_parent_sha:
        fail("interpretation-note parent is not the accepted protected-main parent")

    changed = [
        line
        for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines()
        if line
    ]
    if changed != [NOTE_REL]:
        fail("interpretation-note event must create exactly the canonical note")
    if git_object_exists(f"{parent}:{NOTE_REL}"):
        fail("interpretation note must be creation-only")
    history = [
        line for line in git("log", "--format=%H", head, "--", NOTE_REL).splitlines() if line
    ]
    if history != [head]:
        fail("interpretation note must have first-and-only immutable history")

    result_event, _ = validate_result_history(parent)
    if git_bytes(parent, RESULT_REL) != git_bytes(head, RESULT_REL):
        fail("locked-analysis result record changed during interpretation-note admission")
    record = load_json_bytes(git_bytes(head, NOTE_REL), "interpretation note")
    validate_note_record(
        record,
        result_event_sha=result_event,
        interpretation_parent_sha=parent,
    )
    return parent


def validate_accepted_note(ref: str = "HEAD") -> str:
    if not git_object_exists(f"{ref}:{NOTE_REL}"):
        fail("accepted-state validation requires the interpretation note")
    history = [
        line for line in git("log", "--format=%H", ref, "--", NOTE_REL).splitlines() if line
    ]
    if len(history) != 1:
        fail("interpretation note must have one immutable history event")
    event = history[0]
    lineage = git("rev-list", "--parents", "-n", "1", event).split()
    if len(lineage) != 2 or lineage[0] != event:
        fail("accepted interpretation-note event must have exactly one parent")
    parent = lineage[1]
    changed = [
        line
        for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", event).splitlines()
        if line
    ]
    if changed != [NOTE_REL]:
        fail("accepted interpretation-note event changed more than its canonical note")
    if git_object_exists(f"{parent}:{NOTE_REL}"):
        fail("accepted interpretation note is not creation-only")
    result_event, _ = validate_result_history(parent)
    if git_bytes(parent, RESULT_REL) != git_bytes(event, RESULT_REL):
        fail("locked-analysis result record changed during accepted interpretation event")
    record = load_json_bytes(git_bytes(event, NOTE_REL), "accepted interpretation note")
    validate_note_record(
        record,
        result_event_sha=result_event,
        interpretation_parent_sha=parent,
    )
    return event


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    ).encode("utf-8")


def packet_sha256(packet: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(packet)).hexdigest()


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
        print("TRACK_A_EPOCH_002_INTERPRETATION_TOOLING=PASS_NONEXECUTING")
        print("INTERPRETATION_NOTE=ABSENT")
    elif args.accepted_state:
        validate_accepted_note("HEAD")
        print("TRACK_A_EPOCH_002_INTERPRETATION_NOTE=ESTABLISHED_PRESERVED")
    else:
        if not args.accepted_parent:
            fail("--accepted-parent is required for event validation")
        validate_note_event(args.event_commit, accepted_parent_sha=args.accepted_parent)
        print("TRACK_A_EPOCH_002_INTERPRETATION_EVENT=VALIDATED_PENDING_ACCEPTANCE")

    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
