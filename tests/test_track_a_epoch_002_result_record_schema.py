import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json").read_text())


def valid_record():
    return {
        "record_type": "PRECOLLECTION_GATE_CHECKLIST",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "record_id": "E002-GATE-0001",
        "generated_at_utc": "2026-09-09T00:00:00Z",
        "producer": {"system": "DGAF validator", "version_or_commit": "2095f0e"},
        "immutable_subject": {"commit_sha": "a" * 40},
        "evidence_scope": "prospective structural gate record",
        "non_effects": [
            "DOES_NOT_AUTHORIZE_COLLECTION",
            "DOES_NOT_INCREMENT_SCIENTIFIC_N",
            "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
            "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
        ],
        "status": "BLOCKED",
        "predecessor_record_ids": [],
        "authorization_effect": "NONE",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def test_result_record_envelope_accepts_prospective_blocked_record():
    jsonschema.validate(valid_record(), SCHEMA)


@pytest.mark.parametrize(
    "field,value",
    [
        ("private_key", "not-allowed"),
        ("passphrase", "not-allowed"),
        ("api_token", "not-allowed"),
    ],
)
def test_result_record_envelope_rejects_secret_bearing_fields(field, value):
    record = valid_record()
    record[field] = value
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(record, SCHEMA)


def test_result_record_envelope_rejects_scientific_state_promotion():
    record = valid_record()
    record["scientific_state_effect"]["empirical_n_increment"] = 1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(record, SCHEMA)


def test_result_record_envelope_requires_immutable_subject():
    record = valid_record()
    record["immutable_subject"] = {}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(record, SCHEMA)
