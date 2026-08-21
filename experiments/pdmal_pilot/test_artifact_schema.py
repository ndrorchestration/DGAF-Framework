from __future__ import annotations

import hashlib
import json

from pilot_artifact_schema import validate_artifact, verify_sidecar


def _record() -> dict:
    record = {
        "experiment_id": "PDMAL-PILOT-V1",
        "protocol_version": "0.7.4",
        "experiment_commit_sha": "a" * 40,
        "seed_id": 20260819,
        "blinded_condition_id": "blind_0123456789abcdef",
        "trial_id": 0,
        "primary_outcome": 0.1,
        "secondary_outcomes": {"topology": "ring", "failure_count": 0, "final_mean": 0.0},
        "failure": False,
        "recovery": True,
        "runtime_ms": 1,
        "status": "SUCCESS",
        "excluded": False,
        "exclusion_reason": None,
        "environment_fingerprint": "env",
    }
    record["artifact_sha256"] = hashlib.sha256(
        (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    return record


def test_valid_pilot_artifact() -> None:
    document = {
        "schema_version": "1.0",
        "artifact_version": "seed-20260819",
        "protocol_status": "FROZEN",
        "empirical_data_collection": True,
        "frozen_commit_sha": "a" * 40,
        "seed_id": 20260819,
        "runtime_seconds": 1.0,
        "records": [_record() for _ in range(180)],
    }
    validate_artifact(document, expected_seed=20260819)


def test_sidecar_matches() -> None:
    raw = b"example artifact\n"
    sidecar = f"{hashlib.sha256(raw).hexdigest()}  pilot_seed_20260819.json\n"
    verify_sidecar(raw, sidecar, "pilot_seed_20260819.json")
