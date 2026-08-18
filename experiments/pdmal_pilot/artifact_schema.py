"""Pre-freeze validation for canonical per-seed experimental artifacts.

This module validates schema/integrity fields only. It does not execute an
experimental workload and cannot authorize data collection.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

REQUIRED_SEED_FIELDS = {
    "experiment_id",
    "protocol_version",
    "experiment_commit_sha",
    "seed_id",
    "blinded_condition_id",
    "trial_id",
    "primary_outcome",
    "secondary_outcomes",
    "failure",
    "recovery",
    "runtime_ms",
    "status",
    "excluded",
    "exclusion_reason",
    "environment_fingerprint",
    "artifact_sha256",
}

ALLOWED_STATUS = {"SUCCESS", "RECOVERED", "UNRECOVERED_FAILURE"}


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def validate_seed_record(record: Mapping[str, Any]) -> None:
    missing = REQUIRED_SEED_FIELDS - set(record)
    if missing:
        raise AssertionError(f"artifact record missing fields: {sorted(missing)}")
    if record["status"] not in ALLOWED_STATUS:
        raise AssertionError(f"invalid trial status: {record['status']!r}")
    if not isinstance(record["excluded"], bool):
        raise AssertionError("excluded must be boolean")
    if record["excluded"] and not record["exclusion_reason"]:
        raise AssertionError("excluded records require an exclusion_reason")
    if not record["excluded"] and record["exclusion_reason"] is not None:
        raise AssertionError("non-excluded records must have null exclusion_reason")
    if not isinstance(record["environment_fingerprint"], str) or not record["environment_fingerprint"]:
        raise AssertionError("environment_fingerprint must be non-empty")
    if not isinstance(record["artifact_sha256"], str) or len(record["artifact_sha256"]) != 64:
        raise AssertionError("artifact_sha256 must be a 64-character SHA-256 hex digest")
    try:
        int(record["artifact_sha256"], 16)
    except ValueError as exc:
        raise AssertionError("artifact_sha256 must be hexadecimal") from exc


def validate_artifact_document(document: Mapping[str, Any]) -> None:
    """Validate a per-seed document without recomputing its external sidecar."""
    required_document = {"artifact_version", "protocol_status", "empirical_data_collection", "records"}
    missing = required_document - set(document)
    if missing:
        raise AssertionError(f"artifact document missing fields: {sorted(missing)}")
    if document["protocol_status"] != "PRE-FREEZE":
        raise AssertionError("pre-freeze artifact must declare PRE-FREEZE")
    if document["empirical_data_collection"] is not False:
        raise AssertionError("pre-freeze artifact must not authorize empirical collection")
    records = document["records"]
    if not isinstance(records, list) or not records:
        raise AssertionError("records must be a non-empty list")
    for record in records:
        if not isinstance(record, Mapping):
            raise AssertionError("each artifact record must be an object")
        validate_seed_record(record)


def sha256_sidecar(raw_artifact: bytes, filename: str) -> str:
    """Return the canonical sidecar line for a raw artifact."""
    return f"{sha256_bytes(raw_artifact)}  {filename}\n"
