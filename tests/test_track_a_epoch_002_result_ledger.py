import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_result_ledger.py"
SPEC = importlib.util.spec_from_file_location("epoch_002_result_ledger", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def record(record_type, record_id, predecessors=None, status="PASS"):
    return {
        "record_type": record_type,
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "record_id": record_id,
        "generated_at_utc": "2026-09-09T00:00:00Z",
        "producer": {"system": "test", "version_or_commit": "f66afb7"},
        "immutable_subject": {"commit_sha": "a" * 40},
        "evidence_scope": "structural test only",
        "non_effects": [
            "DOES_NOT_AUTHORIZE_COLLECTION",
            "DOES_NOT_INCREMENT_SCIENTIFIC_N",
            "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
            "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
        ],
        "status": status,
        "predecessor_record_ids": predecessors or [],
        "authorization_effect": "NONE",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def write_ledger(tmp_path, records):
    path = tmp_path / "ledger.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    return path


def test_accepts_prospective_blocked_first_record(tmp_path):
    path = write_ledger(tmp_path, [record("PRECOLLECTION_GATE_CHECKLIST", "E002-GATE-0001", status="BLOCKED")])
    MODULE.validate_ledger(path)


def test_rejects_skipped_record_type(tmp_path):
    path = write_ledger(tmp_path, [record("QC_LEDGER", "E002-QC-0001")])
    with pytest.raises(ValueError, match="invalid record order"):
        MODULE.validate_ledger(path)


def test_rejects_missing_predecessor_link(tmp_path):
    records = [
        record("PRECOLLECTION_GATE_CHECKLIST", "E002-GATE-0001"),
        record("COLLECTION_START_RECEIPT", "E002-START-0001"),
    ]
    with pytest.raises(ValueError, match="must reference prior record"):
        MODULE.validate_ledger(write_ledger(tmp_path, records))


def test_rejects_records_after_terminal_non_pass_status(tmp_path):
    records = [
        record("PRECOLLECTION_GATE_CHECKLIST", "E002-GATE-0001", status="BLOCKED"),
        record("COLLECTION_START_RECEIPT", "E002-START-0001", ["E002-GATE-0001"]),
    ]
    with pytest.raises(ValueError, match="cannot follow a non-PASS"):
        MODULE.validate_ledger(write_ledger(tmp_path, records))
