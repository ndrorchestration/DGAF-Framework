from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from scripts import validate_track_a_epoch_002_dataset_lock as lock

ALL_NON_EFFECTS = {
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
}


def record(
    record_type: str,
    record_id: str,
    *,
    predecessors: list[str] | None = None,
    status: str = "PASS",
    effect: str = "NONE",
    non_effects: set[str] | None = None,
) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "record_id": record_id,
        "generated_at_utc": "2026-09-10T00:00:00Z",
        "producer": {"system": "dataset-lock-test", "version_or_commit": "8414219"},
        "immutable_subject": {"commit_sha": "a" * 40},
        "evidence_scope": "prospective dataset-lock test only",
        "non_effects": sorted(non_effects if non_effects is not None else ALL_NON_EFFECTS),
        "status": status,
        "predecessor_record_ids": predecessors or [],
        "authorization_effect": effect,
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def completed_prefix() -> list[dict[str, Any]]:
    records = [record("PRECOLLECTION_GATE_CHECKLIST", "E002-GATE-0001")]
    records.append(
        record(
            "COLLECTION_START_RECEIPT",
            "E002-START-0001",
            predecessors=[records[-1]["record_id"]],
        )
    )
    for seed_index in range(50):
        records.append(
            record(
                "PER_SEED_EXECUTION_RECORD",
                f"E002-SEED-{seed_index + 1:04d}",
                predecessors=[records[-1]["record_id"]],
            )
        )
    records.append(record("QC_LEDGER", "E002-QC-0001", predecessors=[records[-1]["record_id"]]))
    return records


def lock_record(qc_id: str = "E002-QC-0001") -> dict[str, Any]:
    return record(
        "DATASET_LOCK_RECEIPT",
        "E002-LOCK-0001",
        predecessors=[qc_id],
        effect="REQUIRES_SEPARATE_EXACT_COMMIT",
    )


def write_ledger(tmp_path: Path, records: list[dict[str, Any]]) -> Path:
    path = tmp_path / "ledger.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    return path


def test_valid_dataset_lock_is_exact_append_after_complete_qc(tmp_path: Path) -> None:
    before = completed_prefix()
    after = before + [lock_record()]
    lock.validate_transition(before, after)
    lock.validate_retained_ledger(write_ledger(tmp_path, after), require_lock=True)


def test_dataset_lock_cannot_rewrite_predecessor_evidence() -> None:
    before = completed_prefix()
    after = deepcopy(before) + [lock_record()]
    after[20]["immutable_subject"]["commit_sha"] = "b" * 40
    with pytest.raises(SystemExit, match="must append exactly one record"):
        lock.validate_transition(before, after)


def test_dataset_lock_requires_all_50_seed_records() -> None:
    before = completed_prefix()
    del before[10]
    after = before + [lock_record()]
    with pytest.raises(SystemExit, match="complete through QC_LEDGER"):
        lock.validate_transition(before, after)


def test_dataset_lock_requires_direct_qc_predecessor() -> None:
    before = completed_prefix()
    after = before + [lock_record("E002-SEED-0050")]
    with pytest.raises(SystemExit, match="directly reference prior QC_LEDGER"):
        lock.validate_transition(before, after)


def test_dataset_lock_pass_cannot_authorize_unblinding_or_analysis() -> None:
    before = completed_prefix()
    promoted = lock_record()
    promoted["authorization_effect"] = "BOUNDED_RECORD_ONLY"
    promoted["non_effects"].remove("DOES_NOT_AUTHORIZE_UNBLINDING")
    with pytest.raises(SystemExit, match="dataset-lock semantic ceiling"):
        lock.validate_transition(before, before + [promoted])


def test_non_pass_dataset_lock_has_zero_authority() -> None:
    before = completed_prefix()
    failed = lock_record()
    failed["status"] = "FAIL"
    failed["authorization_effect"] = "NONE"
    with pytest.raises(SystemExit, match="dataset lock requires PASS"):
        lock.validate_transition(before, before + [failed])


def test_current_boundary_proves_dataset_lock_absent(capsys: pytest.CaptureFixture[str]) -> None:
    lock.validate_boundary()
    output = capsys.readouterr().out
    assert "TRACK_A_EPOCH_002_DATASET_LOCK_TOOLING=PASS_LOCK_ABSENT" in output
    assert "UNBLINDING_AUTHORIZED=FALSE" in output
    assert "PRIMARY_ANALYSIS_AUTHORIZED=FALSE" in output
    assert "SCIENTIFIC_N_INCREMENT=0" in output


def test_tool_has_no_write_execution_or_secret_surface() -> None:
    text = lock.MODULE_PATH.read_text(encoding="utf-8")
    assert "--write" not in text
    assert "write_text(" not in text
    assert "--execute" not in text
    assert "PDMAL_TOPOLOGY_BLINDING_KEY" not in text
    assert "PRIVATE_KEY" not in text
