#!/usr/bin/env python3
"""Validate a source-bound, non-promoting Mode-T external result intake envelope.

This validator can preserve an external party's reported result and evidence references.
It deliberately cannot verify independence, authenticate retrieved artifacts, adjudicate P4,
designate a final candidate, create a freeze, grant authorization, or change empirical N.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Mapping

_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

_TOP_LEVEL = {
    "schema_version",
    "record_class",
    "record_state",
    "source_handoff",
    "track",
    "producer",
    "submission",
    "external_result",
    "ingestion_state",
    "scientific_state",
    "non_promotion",
}
_SOURCE_HANDOFF_KEYS = {
    "repository",
    "handoff_merge_sha",
    "handoff_tree",
    "handoff_manifest_path",
    "handoff_manifest_git_blob",
    "review_base_sha",
    "review_base_tree",
}
_TRACK_KEYS = {"issue", "track", "required_output"}
_PRODUCER_KEYS = {
    "name",
    "organization",
    "external_identifier",
    "independence_claimed",
    "independence_basis",
    "attribution_evidence_refs",
}
_SUBMISSION_KEYS = {"submitted_at_utc", "external_record_uri", "external_record_sha256"}
_EXTERNAL_RESULT_KEYS = {
    "execution_state",
    "execution_phase",
    "external_disposition",
    "claims",
    "evidence_artifacts",
}
_CLAIM_KEYS = {"claim_id", "result", "evidence_refs", "notes"}
_ARTIFACT_KEYS = {"artifact_id", "uri", "sha256", "media_type", "description"}
_INGESTION_STATE = {
    "attribution_verified": False,
    "artifacts_retrieved": False,
    "cryptographic_reverification_status": "NOT_EXECUTED",
    "governance_adjudication_status": "NOT_EXECUTED",
}
_SCIENTIFIC_STATE = {
    "final_candidate_status": "NOT_DESIGNATED",
    "final_candidate_tracker": 309,
    "p4_status": "OPEN_FAIL_CLOSED",
    "p7_final_binding": "OPEN",
    "p8_status": "OPEN_FAIL_CLOSED",
    "final_p9_status": "NOT_EXECUTED",
    "freeze_status": "NOT_ESTABLISHED",
    "authorization_status": "NOT_GRANTED",
    "empirical_n": 0,
}
_NON_PROMOTION_KEYS = {
    "envelope_is_acceptance_evidence",
    "envelope_verifies_independence",
    "envelope_verifies_artifact_authenticity",
    "envelope_closes_p4",
    "envelope_designates_final_candidate",
    "envelope_grants_authorization",
    "envelope_changes_empirical_n",
}
_TRACKS = {
    320: "independent_oidc_security_review",
    316: "production_rac_retention_and_authority",
    310: "real_confidential_space_admission",
    295: "protected_continuity_acceptance",
}
_RECORD_STATES = {"TEMPLATE", "EXTERNAL_SUBMISSION_UNVERIFIED"}
_EXECUTION_STATES = {"NOT_EXECUTED", "EXECUTED"}
_EXECUTION_PHASES = {
    "STAGE_A_APPARATUS_QUALIFICATION",
    "STAGE_B_FINAL_CANDIDATE_ACCEPTANCE",
    "TRACK_SPECIFIC",
}
_EXTERNAL_DISPOSITIONS = {"PASS", "FAIL", "BLOCKED", "CONDITIONAL", "UNKNOWN"}
_CLAIM_RESULTS = {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE"}


def _mapping(value: Any, label: str, errors: list[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        errors.append(f"{label} must be an object")
        return {}
    return value


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nullable_string(value: Any) -> bool:
    return value is None or _nonempty_string(value)


def validate_intake_structure(data: Any) -> list[str]:
    """Return closed-schema and non-promotion errors without consulting Git/network."""
    errors: list[str] = []
    root = _mapping(data, "envelope", errors)
    if set(root) != _TOP_LEVEL:
        errors.append("envelope top-level keys must match the closed schema")

    if root.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if root.get("record_class") != "DGAF_MODE_T_EXTERNAL_RESULT_INTAKE_V1":
        errors.append("unexpected record_class")

    record_state = root.get("record_state")
    if record_state not in _RECORD_STATES:
        errors.append("record_state must be TEMPLATE or EXTERNAL_SUBMISSION_UNVERIFIED")

    source = _mapping(root.get("source_handoff"), "source_handoff", errors)
    if set(source) != _SOURCE_HANDOFF_KEYS:
        errors.append("source_handoff keys must match the closed schema")
    if source.get("repository") != "ndrorchestration/DGAF-Framework":
        errors.append("source_handoff repository mismatch")
    if source.get("handoff_manifest_path") != (
        "docs/governance/mode_t_external_acceptance_manifest.json"
    ):
        errors.append("unexpected handoff_manifest_path")
    for field in (
        "handoff_merge_sha",
        "handoff_tree",
        "handoff_manifest_git_blob",
        "review_base_sha",
        "review_base_tree",
    ):
        value = source.get(field)
        if not isinstance(value, str) or not _SHA1_RE.fullmatch(value):
            errors.append(f"source_handoff {field} must be a 40-character Git object id")

    track = _mapping(root.get("track"), "track", errors)
    if set(track) != _TRACK_KEYS:
        errors.append("track keys must match the closed schema")
    if not _nullable_string(track.get("required_output")):
        errors.append("track required_output must be null or a non-empty string")

    producer = _mapping(root.get("producer"), "producer", errors)
    if set(producer) != _PRODUCER_KEYS:
        errors.append("producer keys must match the closed schema")
    for field in (
        "name",
        "organization",
        "external_identifier",
        "independence_basis",
    ):
        if not _nullable_string(producer.get(field)):
            errors.append(f"producer {field} must be null or a non-empty string")
    if not isinstance(producer.get("independence_claimed"), bool):
        errors.append("producer independence_claimed must be boolean")
    attribution_refs = producer.get("attribution_evidence_refs")
    if not isinstance(attribution_refs, list) or not all(
        _nonempty_string(ref) for ref in attribution_refs
    ):
        errors.append(
            "producer attribution_evidence_refs must be a list of non-empty strings"
        )
        attribution_refs = []

    submission = _mapping(root.get("submission"), "submission", errors)
    if set(submission) != _SUBMISSION_KEYS:
        errors.append("submission keys must match the closed schema")
    for field in ("submitted_at_utc", "external_record_uri", "external_record_sha256"):
        if not _nullable_string(submission.get(field)):
            errors.append(f"submission {field} must be null or a non-empty string")

    result = _mapping(root.get("external_result"), "external_result", errors)
    if set(result) != _EXTERNAL_RESULT_KEYS:
        errors.append("external_result keys must match the closed schema")
    if result.get("execution_state") not in _EXECUTION_STATES:
        errors.append("external_result execution_state is invalid")
    phase = result.get("execution_phase")
    if phase is not None and phase not in _EXECUTION_PHASES:
        errors.append("external_result execution_phase is invalid")
    if result.get("external_disposition") not in _EXTERNAL_DISPOSITIONS:
        errors.append("external_result external_disposition is invalid")

    claims = result.get("claims")
    if not isinstance(claims, list):
        errors.append("external_result claims must be a list")
        claims = []
    artifacts = result.get("evidence_artifacts")
    if not isinstance(artifacts, list):
        errors.append("external_result evidence_artifacts must be a list")
        artifacts = []

    artifact_ids: set[str] = set()
    for index, raw_artifact in enumerate(artifacts):
        artifact = _mapping(raw_artifact, f"evidence_artifacts[{index}]", errors)
        if set(artifact) != _ARTIFACT_KEYS:
            errors.append(f"evidence_artifacts[{index}] keys must match the closed schema")
        artifact_id = artifact.get("artifact_id")
        if not _nonempty_string(artifact_id):
            errors.append(f"evidence_artifacts[{index}] artifact_id is invalid")
        elif artifact_id in artifact_ids:
            errors.append(f"duplicate artifact_id: {artifact_id}")
        else:
            artifact_ids.add(artifact_id)
        for field in ("uri", "media_type", "description"):
            if not _nonempty_string(artifact.get(field)):
                errors.append(f"evidence_artifacts[{index}] {field} is invalid")
        digest = artifact.get("sha256")
        if not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
            errors.append(f"evidence_artifacts[{index}] sha256 is invalid")

    unknown_attribution_refs = set(attribution_refs) - artifact_ids
    if unknown_attribution_refs:
        errors.append(
            "producer attribution_evidence_refs reference unknown artifacts: "
            f"{sorted(unknown_attribution_refs)}"
        )

    claim_ids: set[str] = set()
    for index, raw_claim in enumerate(claims):
        claim = _mapping(raw_claim, f"claims[{index}]", errors)
        if set(claim) != _CLAIM_KEYS:
            errors.append(f"claims[{index}] keys must match the closed schema")
        claim_id = claim.get("claim_id")
        if not _nonempty_string(claim_id):
            errors.append(f"claims[{index}] claim_id is invalid")
        elif claim_id in claim_ids:
            errors.append(f"duplicate claim_id: {claim_id}")
        else:
            claim_ids.add(claim_id)
        if claim.get("result") not in _CLAIM_RESULTS:
            errors.append(f"claims[{index}] result is invalid")
        refs = claim.get("evidence_refs")
        if not isinstance(refs, list) or not all(_nonempty_string(ref) for ref in refs):
            errors.append(f"claims[{index}] evidence_refs must be a list of non-empty strings")
        else:
            unknown = set(refs) - artifact_ids
            if unknown:
                errors.append(f"claims[{index}] references unknown artifacts: {sorted(unknown)}")
        if not _nullable_string(claim.get("notes")):
            errors.append(f"claims[{index}] notes must be null or a non-empty string")

    ingestion = _mapping(root.get("ingestion_state"), "ingestion_state", errors)
    if set(ingestion) != set(_INGESTION_STATE):
        errors.append("ingestion_state keys must match the closed schema")
    for key, expected in _INGESTION_STATE.items():
        if ingestion.get(key) != expected:
            errors.append(f"ingestion_state {key} must remain {expected!r}")

    scientific = _mapping(root.get("scientific_state"), "scientific_state", errors)
    if set(scientific) != set(_SCIENTIFIC_STATE):
        errors.append("scientific_state keys must match the closed schema")
    for key, expected in _SCIENTIFIC_STATE.items():
        if scientific.get(key) != expected:
            errors.append(f"scientific_state {key} must remain {expected!r}")

    non_promotion = _mapping(root.get("non_promotion"), "non_promotion", errors)
    if set(non_promotion) != _NON_PROMOTION_KEYS:
        errors.append("non_promotion keys must match the closed schema")
    for key in _NON_PROMOTION_KEYS:
        if non_promotion.get(key) is not False:
            errors.append(f"non_promotion {key} must be false")

    if record_state == "TEMPLATE":
        if any(track.get(field) is not None for field in _TRACK_KEYS):
            errors.append("template track identity/required_output must remain null")
        if any(
            producer.get(field) is not None
            for field in (
                "name",
                "organization",
                "external_identifier",
                "independence_basis",
            )
        ):
            errors.append("template producer identity/basis must remain null")
        if producer.get("independence_claimed") is not False:
            errors.append("template independence_claimed must remain false")
        if attribution_refs:
            errors.append("template attribution_evidence_refs must remain empty")
        if any(submission.get(field) is not None for field in _SUBMISSION_KEYS):
            errors.append("template submission fields must remain null")
        if result.get("execution_state") != "NOT_EXECUTED":
            errors.append("template execution_state must remain NOT_EXECUTED")
        if result.get("execution_phase") is not None:
            errors.append("template execution_phase must remain null")
        if result.get("external_disposition") != "UNKNOWN":
            errors.append("template external_disposition must remain UNKNOWN")
        if claims or artifacts:
            errors.append("template claims/evidence_artifacts must remain empty")

    if record_state == "EXTERNAL_SUBMISSION_UNVERIFIED":
        issue = track.get("issue")
        name = track.get("track")
        if not isinstance(issue, int) or issue not in _TRACKS:
            errors.append("external submission issue must be one of 295/310/316/320")
        elif name != _TRACKS[issue]:
            errors.append("external submission track name does not match issue")
        if not _nonempty_string(track.get("required_output")):
            errors.append("external submission required_output is required")
        for field in ("name", "external_identifier"):
            if not _nonempty_string(producer.get(field)):
                errors.append(f"external submission producer {field} is required")
        if not _nullable_string(producer.get("organization")):
            errors.append("external submission producer organization is invalid")
        if producer.get("independence_claimed") is True and not _nonempty_string(
            producer.get("independence_basis")
        ):
            errors.append(
                "external submission claiming independence requires independence_basis"
            )
        if not attribution_refs:
            errors.append(
                "external submission requires at least one attribution evidence reference"
            )
        submitted_at = submission.get("submitted_at_utc")
        if not isinstance(submitted_at, str) or not _UTC_RE.fullmatch(submitted_at):
            errors.append("external submission submitted_at_utc must be second-precision UTC")
        if not _nonempty_string(submission.get("external_record_uri")):
            errors.append("external submission external_record_uri is required")
        record_digest = submission.get("external_record_sha256")
        if not isinstance(record_digest, str) or not _SHA256_RE.fullmatch(record_digest):
            errors.append("external submission external_record_sha256 is invalid")
        if result.get("execution_state") != "EXECUTED":
            errors.append("external submission execution_state must be EXECUTED")
        if result.get("execution_phase") not in _EXECUTION_PHASES:
            errors.append("external submission execution_phase is required")
        if issue == 310 and result.get("execution_phase") not in {
            "STAGE_A_APPARATUS_QUALIFICATION",
            "STAGE_B_FINAL_CANDIDATE_ACCEPTANCE",
        }:
            errors.append("Issue 310 submission must distinguish Stage A from Stage B")
        if not claims:
            errors.append("external submission must contain at least one claim")
        if not artifacts:
            errors.append("external submission must contain at least one evidence artifact")

    return errors


def _git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def validate_repository_binding(data: Mapping[str, Any], repo_root: Path) -> list[str]:
    """Verify the intake envelope is bound to the immutable #343 handoff source graph."""
    errors: list[str] = []
    source = data["source_handoff"]
    handoff_sha = str(source["handoff_merge_sha"])
    expected_tree = str(source["handoff_tree"])

    try:
        actual_tree = _git(repo_root, "show", "-s", "--format=%T", handoff_sha).stdout.strip()
    except subprocess.CalledProcessError as exc:
        return [f"handoff merge is unavailable: {exc.stderr.strip()}"]
    if actual_tree != expected_tree:
        errors.append(f"handoff tree mismatch: expected {expected_tree}, got {actual_tree}")

    ancestor = _git(repo_root, "merge-base", "--is-ancestor", handoff_sha, "HEAD", check=False)
    if ancestor.returncode != 0:
        errors.append("handoff merge must be an ancestor of HEAD")

    manifest_path = str(source["handoff_manifest_path"])
    tree_result = _git(repo_root, "ls-tree", handoff_sha, "--", manifest_path, check=False)
    if tree_result.returncode != 0 or not tree_result.stdout.strip():
        errors.append("handoff manifest is missing at handoff merge")
        return errors
    meta, _, returned_path = tree_result.stdout.rstrip("\n").partition("\t")
    parts = meta.split()
    if len(parts) != 3 or returned_path != manifest_path:
        errors.append("unexpected git ls-tree shape for handoff manifest")
        return errors
    if parts[2] != source["handoff_manifest_git_blob"]:
        errors.append("handoff manifest Git blob does not match source_handoff")

    manifest_result = _git(repo_root, "show", f"{handoff_sha}:{manifest_path}", check=False)
    if manifest_result.returncode != 0:
        errors.append("handoff manifest cannot be read from handoff merge")
        return errors
    manifest = json.loads(manifest_result.stdout)
    if manifest.get("record_class") != "DGAF_MODE_T_EXTERNAL_ACCEPTANCE_HANDOFF_V1":
        errors.append("source handoff manifest record_class mismatch")
    base = manifest.get("review_base", {})
    if base.get("sha") != source["review_base_sha"]:
        errors.append("review_base_sha does not match handoff manifest")
    if base.get("tree") != source["review_base_tree"]:
        errors.append("review_base_tree does not match handoff manifest")

    if data.get("record_state") == "EXTERNAL_SUBMISSION_UNVERIFIED":
        issue = data["track"]["issue"]
        track_name = data["track"]["track"]
        matching = [
            track
            for track in manifest.get("external_tracks", [])
            if track.get("issue") == issue and track.get("track") == track_name
        ]
        if len(matching) != 1:
            errors.append("external submission track is not uniquely bound in handoff manifest")
        else:
            source_track = matching[0]
            if source_track.get("status") != "NOT_EXECUTED":
                errors.append("source handoff track must originate from NOT_EXECUTED state")
            if data["track"].get("required_output") != source_track.get("required_output"):
                errors.append("external submission required_output does not match handoff manifest")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--intake",
        default="docs/governance/mode_t_external_result_intake_template.json",
    )
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    intake_path = Path(args.intake)
    data = json.loads(intake_path.read_text(encoding="utf-8"))
    errors = validate_intake_structure(data)
    if not errors:
        errors.extend(validate_repository_binding(data, Path(args.repo_root).resolve()))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: Mode-T external result intake is source-bound and non-promoting")
    print(f"record_state={data['record_state']}")
    print("attribution_verified=false")
    print("artifacts_retrieved=false")
    print("governance_adjudication_status=NOT_EXECUTED")
    print("p4_status=OPEN_FAIL_CLOSED")
    print("authorization_status=NOT_GRANTED")
    print("empirical_n=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
