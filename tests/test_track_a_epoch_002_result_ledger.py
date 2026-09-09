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


def append_record(records, record_type, record_id, status="PASS"):
    predecessors = [records[-1]["record_id"]] if records else []
    records.append(record(record_type, record_id, predecessors, status=status))


def execution_prefix(seed_count):
    records = []
    append_record(records, "PRECOLLECTION_GATE_CHECKLIST", "E002-GATE-0001")
    append_record(records, "COLLECTION_START_RECEIPT", "E002-START-0001")
    for seed_index in range(seed_count):
        append_record(
            records,
            "PER_SEED_EXECUTION_RECORD",
            f"E002-SEED-{seed_index + 1:04d}",
        )
    return records


def write_ledger(tmp_path, records):
    path = tmp_path / "ledger.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    return path


def test_accepts_prospective_blocked_first_record(tmp_path):
    path = write_ledger(
        tmp_path,
        [record("PRECOLLECTION_GATE_CHECKLIST", "E002-GATE-0001", status="BLOCKED")],
    )
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


def test_accepts_partial_per_seed_prefix(tmp_path):
    MODULE.validate_ledger(write_ledger(tmp_path, execution_prefix(17)))


def test_accepts_exactly_fifty_per_seed_records_before_qc(tmp_path):
    records = execution_prefix(MODULE.PER_SEED_RECORD_COUNT)
    append_record(records, "QC_LEDGER", "E002-QC-0001")
    MODULE.validate_ledger(write_ledger(tmp_path, records))


def test_rejects_qc_before_fifty_per_seed_records(tmp_path):
    records = execution_prefix(MODULE.PER_SEED_RECORD_COUNT - 1)
    append_record(records, "QC_LEDGER", "E002-QC-0001")
    with pytest.raises(ValueError, match="expected PER_SEED_EXECUTION_RECORD"):
        MODULE.validate_ledger(write_ledger(tmp_path, records))


def test_rejects_fifty_first_per_seed_record(tmp_path):
    records = execution_prefix(MODULE.PER_SEED_RECORD_COUNT)
    append_record(records, "PER_SEED_EXECUTION_RECORD", "E002-SEED-0051")
    with pytest.raises(ValueError, match="expected QC_LEDGER"):
        MODULE.validate_ledger(write_ledger(tmp_path, records))


def test_accepts_complete_ordered_ledger(tmp_path):
    records = execution_prefix(MODULE.PER_SEED_RECORD_COUNT)
    for record_type, record_id in (
        ("QC_LEDGER", "E002-QC-0001"),
        ("DATASET_LOCK_RECEIPT", "E002-LOCK-0001"),
        ("UNBLINDING_DECISION_RECORD", "E002-UNBLIND-0001"),
        ("MATERIALIZATION_RECEIPT", "E002-MATERIALIZE-0001"),
        ("PRIMARY_ANALYSIS_AUTHORIZATION_RECORD", "E002-ANALYSIS-AUTH-0001"),
        ("LOCKED_ANALYSIS_RESULT_RECORD", "E002-ANALYSIS-RESULT-0001"),
        ("INTERPRETATION_NOTE", "E002-INTERPRET-0001"),
    ):
        append_record(records, record_type, record_id)
    MODULE.validate_ledger(write_ledger(tmp_path, records))


def test_rejects_records_beyond_complete_order(tmp_path):
    records = execution_prefix(MODULE.PER_SEED_RECORD_COUNT)
    for record_type, record_id in (
        ("QC_LEDGER", "E002-QC-0001"),
        ("DATASET_LOCK_RECEIPT", "E002-LOCK-0001"),
        ("UNBLINDING_DECISION_RECORD", "E002-UNBLIND-0001"),
        ("MATERIALIZATION_RECEIPT", "E002-MATERIALIZE-0001"),
        ("PRIMARY_ANALYSIS_AUTHORIZATION_RECORD", "E002-ANALYSIS-AUTH-0001"),
        ("LOCKED_ANALYSIS_RESULT_RECORD", "E002-ANALYSIS-RESULT-0001"),
        ("INTERPRETATION_NOTE", "E002-INTERPRET-0001"),
    ):
        append_record(records, record_type, record_id)
    append_record(records, "INTERPRETATION_NOTE", "E002-INTERPRET-0002")
    with pytest.raises(ValueError, match="more records than the defined ordered sequence"):
        MODULE.validate_ledger(write_ledger(tmp_path, records))
