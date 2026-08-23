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


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def validate_record(record: Mapping[str, Any]) -> None:
    missing = REQUIRED_RECORD_FIELDS - set(record)
    if missing:
        raise AssertionError(f"missing required record fields: {sorted(missing)}")
    sha = record["artifact_sha256"]
    if not isinstance(sha, str) or len(sha) != 64:
        raise AssertionError("artifact_sha256 must be a 64-character SHA-256 digest")
    int(sha, 16)
    if not isinstance(record["blinded_condition_id"], str) or not record["blinded_condition_id"].startswith("blind_"):
        raise AssertionError("condition must remain blinded")
    expected = hashlib.sha256(canonical_json_bytes({k: v for k, v in record.items() if k != "artifact_sha256"})).hexdigest()
    if sha != expected:
        raise AssertionError("artifact_sha256 does not match canonical record payload")
    if record["status"] not in ALLOWED_STATUS:
        raise AssertionError(f"invalid status: {record['status']!r}")
    if not isinstance(record["topology"], str) or not record["topology"]:
        raise AssertionError("topology must be a non-empty string")
    if not isinstance(record["failure_count"], int) or isinstance(record["failure_count"], bool) or record["failure_count"] < 0:
        raise AssertionError("failure_count must be a non-negative integer")
    if not isinstance(record["ffcr_success"], bool):
        raise AssertionError("ffcr_success must be boolean")
    if record["ffcr_success"] and record["status"] != "SUCCESS":
        raise AssertionError("ffcr_success requires SUCCESS status")
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
    if len(document["frozen_commit_sha"]) != 40:
        raise AssertionError("frozen_commit_sha must be a full SHA")
    records = document["records"]
    if not isinstance(records, list) or len(records) != 180:
        raise AssertionError(f"expected 180 records, got {len(records) if isinstance(records, list) else 'non-list'}")
    for record in records:
        validate_record(record)


def verify_sidecar(raw: bytes, sidecar: str, filename: str) -> None:
    expected = f"{hashlib.sha256(raw).hexdigest()}  {filename}\n"
    if sidecar != expected:
        raise AssertionError("artifact sidecar does not match raw artifact")
