"""Schema/integrity validation for authorized PDMAL pilot artifacts.

Separate from the pre-freeze contract schema. This validates artifact
structure and record hashes; it does not authorize execution or unblind labels.
The explicit FFCR outcome and its matrix coordinates are part of the pilot
artifact contract because P8 analysis consumes them directly after unblinding.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

ARTIFACT_SCHEMA_VERSION = "1.0"
REQUIRED_RECORD_FIELDS = {
    "experiment_id", "protocol_version", "experiment_commit_sha", "seed_id",
    "blinded_condition_id", "trial_id", "topology", "failure_count",
    "primary_outcome", "secondary_outcomes", "failure", "recovery", "ffcr_success",
    "runtime_ms", "status", "excluded", "exclusion_reason",
    "environment_fingerprint", "artifact_sha256",
}
ALLOWED_STATUS = {"SUCCESS", "RECOVERED", "UNRECOVERED_FAILURE"}
CANONICAL_TOPOLOGIES = {"ring", "pdmal", "random_regular", "small_world", "complete"}
CANONICAL_FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)
EXPECTED_CELLS_PER_CONDITION = len(CANONICAL_TOPOLOGIES) * len(CANONICAL_FAILURE_COUNTS)
EXPECTED_RECORD_COUNT = 4 * EXPECTED_CELLS_PER_CONDITION


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _require_full_sha(value: Any, field: str) -> None:
    if not isinstance(value, str) or len(value) != 40:
        raise AssertionError(f"{field} must be a full 40-character SHA")
    try:
        int(value, 16)
    except ValueError as exc:
        raise AssertionError(f"{field} must contain only hexadecimal characters") from exc


def validate_record(
    record: Mapping[str, Any],
    *,
    expected_experiment_id: str | None = None,
    expected_protocol_version: str | None = None,
    expected_commit_sha: str | None = None,
    expected_seed: int | None = None,
    expected_environment_fingerprint: str | None = None,
) -> None:
    missing = REQUIRED_RECORD_FIELDS - set(record)
    if missing:
        raise AssertionError(f"missing required record fields: {sorted(missing)}")

    _require_full_sha(record["experiment_commit_sha"], "experiment_commit_sha")
    if expected_commit_sha is not None and record["experiment_commit_sha"] != expected_commit_sha:
        raise AssertionError("record experiment_commit_sha does not match frozen_commit_sha")
    if expected_experiment_id is not None and record["experiment_id"] != expected_experiment_id:
        raise AssertionError("record experiment_id does not match artifact experiment_id")
    if expected_protocol_version is not None and record["protocol_version"] != expected_protocol_version:
        raise AssertionError("record protocol_version does not match artifact protocol_version")
    if expected_seed is not None and record["seed_id"] != expected_seed:
        raise AssertionError("record seed_id does not match artifact seed_id")
    if expected_environment_fingerprint is not None and record["environment_fingerprint"] != expected_environment_fingerprint:
        raise AssertionError("record environment_fingerprint does not match artifact environment_fingerprint")

    if not isinstance(record["seed_id"], int) or isinstance(record["seed_id"], bool):
        raise AssertionError("seed_id must be an integer and not a boolean")
    if not isinstance(record["trial_id"], int) or isinstance(record["trial_id"], bool) or record["trial_id"] < 0:
        raise AssertionError("trial_id must be a non-negative integer")
    if not isinstance(record["experiment_id"], str) or not record["experiment_id"]:
        raise AssertionError("experiment_id must be a non-empty string")
    if not isinstance(record["protocol_version"], str) or not record["protocol_version"]:
        raise AssertionError("protocol_version must be a non-empty string")
    if not isinstance(record["environment_fingerprint"], str) or not record["environment_fingerprint"]:
        raise AssertionError("environment_fingerprint must be a non-empty string")

    sha = record["artifact_sha256"]
    if not isinstance(sha, str) or len(sha) != 64:
        raise AssertionError("artifact_sha256 must be a 64-character SHA-256 digest")
    try:
        int(sha, 16)
    except ValueError as exc:
        raise AssertionError("artifact_sha256 must contain only hexadecimal characters") from exc

    if not isinstance(record["blinded_condition_id"], str) or not record["blinded_condition_id"].startswith("blind_"):
        raise AssertionError("condition must remain blinded")
    expected = hashlib.sha256(canonical_json_bytes({k: v for k, v in record.items() if k != "artifact_sha256"})).hexdigest()
    if sha != expected:
        raise AssertionError("artifact_sha256 does not match canonical record payload")
    if record["status"] not in ALLOWED_STATUS:
        raise AssertionError(f"invalid status: {record['status']!r}")
    if record["status"] == "RECOVERED" and record["recovery"] is not True:
        raise AssertionError("RECOVERED records require recovery=true")
    if not isinstance(record["topology"], str) or record["topology"] not in CANONICAL_TOPOLOGIES:
        raise AssertionError("topology is not in the canonical pilot topology set")
    if not isinstance(record["failure_count"], int) or isinstance(record["failure_count"], bool) or record["failure_count"] not in CANONICAL_FAILURE_COUNTS:
        raise AssertionError("failure_count is not in the canonical pilot matrix")
    if not isinstance(record["ffcr_success"], bool):
        raise AssertionError("ffcr_success must be boolean")
    if record["ffcr_success"] and record["status"] not in {"SUCCESS", "RECOVERED"}:
        raise AssertionError("ffcr_success requires SUCCESS or RECOVERED status")
    if not isinstance(record["excluded"], bool):
        raise AssertionError("excluded must be boolean")
    if record["excluded"] and not record["exclusion_reason"]:
        raise AssertionError("excluded records require an exclusion_reason")
    if not record["excluded"] and record["exclusion_reason"] is not None:
        raise AssertionError("non-excluded records must have null exclusion_reason")


def validate_artifact(document: Mapping[str, Any], *, expected_seed: int | None = None) -> None:
    required = {
        "schema_version", "artifact_version", "protocol_status",
        "empirical_data_collection", "frozen_commit_sha", "seed_id",
        "runtime_seconds", "records",
    }
    missing = required - set(document)
    if missing:
        raise AssertionError(f"artifact missing fields: {sorted(missing)}")
    if document["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise AssertionError("unsupported schema_version")
    if document["protocol_status"] != "FROZEN":
        raise AssertionError("pilot artifact must declare FROZEN")
    if document["empirical_data_collection"] is not True:
        raise AssertionError("pilot artifact must declare empirical_data_collection=true")
    if expected_seed is not None and document["seed_id"] != expected_seed:
        raise AssertionError("seed mismatch")
    _require_full_sha(document["frozen_commit_sha"], "frozen_commit_sha")
    if not isinstance(document["artifact_version"], str) or not document["artifact_version"]:
        raise AssertionError("artifact_version must be a non-empty string")
    if not isinstance(document["runtime_seconds"], (int, float)) or isinstance(document["runtime_seconds"], bool) or document["runtime_seconds"] < 0:
        raise AssertionError("runtime_seconds must be a non-negative number")

    records = document["records"]
    if not isinstance(records, list) or len(records) != EXPECTED_RECORD_COUNT:
        raise AssertionError(f"expected {EXPECTED_RECORD_COUNT} records, got {len(records) if isinstance(records, list) else 'non-list'}")

    seen_matrix: set[tuple[str, str, int]] = set()
    condition_cells: dict[str, set[tuple[str, int]]] = {}
    seen_trial_ids: set[int] = set()
    condition_counts: dict[str, int] = {}
    expected_experiment_id: str | None = None
    expected_protocol_version: str | None = None
    expected_environment_fingerprint: str | None = None

    for record in records:
        expected_experiment_id = expected_experiment_id or (record.get("experiment_id") if isinstance(record.get("experiment_id"), str) else None)
        expected_protocol_version = expected_protocol_version or (record.get("protocol_version") if isinstance(record.get("protocol_version"), str) else None)
        expected_environment_fingerprint = expected_environment_fingerprint or (record.get("environment_fingerprint") if isinstance(record.get("environment_fingerprint"), str) else None)
        validate_record(
            record,
            expected_experiment_id=expected_experiment_id,
            expected_protocol_version=expected_protocol_version,
            expected_commit_sha=document["frozen_commit_sha"],
            expected_seed=document["seed_id"],
            expected_environment_fingerprint=expected_environment_fingerprint,
        )
        key = (record["blinded_condition_id"], record["topology"], record["failure_count"])
        if key in seen_matrix:
            raise AssertionError(f"duplicate pilot matrix cell: {key!r}")
        seen_matrix.add(key)
        condition = record["blinded_condition_id"]
        condition_cells.setdefault(condition, set()).add((record["topology"], record["failure_count"]))
        trial_id = record["trial_id"]
        if trial_id in seen_trial_ids:
            raise AssertionError(f"duplicate trial_id: {trial_id}")
        seen_trial_ids.add(trial_id)
        condition_counts[condition] = condition_counts.get(condition, 0) + 1

    if seen_trial_ids != set(range(EXPECTED_RECORD_COUNT)):
        raise AssertionError(f"trial_id values must be exactly 0..{EXPECTED_RECORD_COUNT - 1}")
    if set(condition_counts) != {record["blinded_condition_id"] for record in records} or len(condition_counts) != 4:
        raise AssertionError("artifact must contain exactly four distinct blinded condition identifiers")
    if set(condition_counts.values()) != {EXPECTED_CELLS_PER_CONDITION}:
        raise AssertionError(f"each blinded condition must contain exactly {EXPECTED_CELLS_PER_CONDITION} matrix cells")

    expected_matrix = {(topology, failure_count) for topology in CANONICAL_TOPOLOGIES for failure_count in CANONICAL_FAILURE_COUNTS}
    if any(cells != expected_matrix for cells in condition_cells.values()):
        raise AssertionError("each blinded condition must contain the complete canonical pilot matrix")


def verify_sidecar(raw: bytes, sidecar: str, filename: str) -> None:
    expected = f"{hashlib.sha256(raw).hexdigest()}  {filename}\n"
    if sidecar != expected:
        raise AssertionError("artifact sidecar does not match raw artifact")
