from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_post_interpretation_disposition.py"


def load_validator(name: str):
    spec = importlib.util.spec_from_file_location(name, VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_closed_disposition_is_outcome_agnostic(monkeypatch: pytest.MonkeyPatch) -> None:
    v = load_validator("epoch002_post_interpretation_closed_test")
    monkeypatch.setattr(
        v,
        "validate_predecessors",
        lambda ref="HEAD": {
            "interpretation_event_commit_sha": "a" * 40,
            "interpretation_note_blob_sha": "b" * 40,
            "locked_result_event_commit_sha": "c" * 40,
            "locked_result_record_blob_sha": "d" * 40,
        },
    )
    record = v.expected_record(parent_sha="e" * 40, generated_at_utc="2026-09-19T14:00:00Z")
    assert record["disposition"] == v.CLOSED
    assert record["evidence_class"] == "SAME_SYSTEM_NONINDEPENDENT"
    assert record["lane_effect"]["rerun_authorized"] is False
    assert record["future_work"]["new_empirical_epoch_authorized"] is False
    assert record["scientific_state_effect"]["empirical_n_increment"] == 0
    assert record["scientific_state_effect"]["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    rendered = json.dumps(record)
    assert "estimate_pdmal_minus_random_regular" not in rendered
    assert "two_sided_95pct_percentile_ci" not in rendered
    assert "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS" not in rendered
    assert "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS" not in rendered
    assert "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED" not in rendered


def test_closed_disposition_rejects_defect_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    v = load_validator("epoch002_post_interpretation_closed_defect_test")
    monkeypatch.setattr(v, "validate_predecessors", lambda ref="HEAD": {})
    with pytest.raises(SystemExit, match="closed disposition cannot carry a defect"):
        v.expected_record(
            parent_sha="e" * 40,
            generated_at_utc="2026-09-19T14:00:00Z",
            disposition=v.CLOSED,
            defect={"defect_id": "DEF-001", "summary": "unexpected defect", "evidence_refs": ["x"]},
        )


def test_open_defect_requires_specific_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    v = load_validator("epoch002_post_interpretation_open_defect_test")
    monkeypatch.setattr(v, "validate_predecessors", lambda ref="HEAD": {})
    with pytest.raises(SystemExit, match="requires a defect object"):
        v.expected_record(
            parent_sha="e" * 40,
            generated_at_utc="2026-09-19T14:00:00Z",
            disposition=v.OPEN_DEFECT,
            defect=None,
        )

    record = v.expected_record(
        parent_sha="e" * 40,
        generated_at_utc="2026-09-19T14:00:00Z",
        disposition=v.OPEN_DEFECT,
        defect={
            "defect_id": "E002-PROV-001",
            "summary": "Specific predecessor provenance mismatch requires remediation.",
            "evidence_refs": ["commit:abc", "path:record.json"],
        },
    )
    assert record["disposition"] == v.OPEN_DEFECT
    assert record["lane_effect"]["epoch_002_lifecycle"] == "OPEN_ONLY_FOR_NAMED_DEFECT_REMEDIATION"
    assert record["lane_effect"]["rerun_authorized"] is False


def test_contract_rejects_claim_promotion(monkeypatch: pytest.MonkeyPatch) -> None:
    v = load_validator("epoch002_post_interpretation_claim_test")
    monkeypatch.setattr(
        v,
        "validate_predecessors",
        lambda ref="HEAD": {
            "interpretation_event_commit_sha": "a" * 40,
            "interpretation_note_blob_sha": "b" * 40,
            "locked_result_event_commit_sha": "c" * 40,
            "locked_result_record_blob_sha": "d" * 40,
        },
    )
    record = v.expected_record(parent_sha="e" * 40, generated_at_utc="2026-09-19T14:00:00Z")
    record["scientific_state_effect"]["canonical_dgaf_efficacy"] = "ESTABLISHED"
    with pytest.raises(SystemExit, match="does not match the exact outcome-agnostic contract"):
        v.validate_record(record, parent_sha="e" * 40)


def test_contract_rejects_future_authorization(monkeypatch: pytest.MonkeyPatch) -> None:
    v = load_validator("epoch002_post_interpretation_auth_test")
    monkeypatch.setattr(
        v,
        "validate_predecessors",
        lambda ref="HEAD": {
            "interpretation_event_commit_sha": "a" * 40,
            "interpretation_note_blob_sha": "b" * 40,
            "locked_result_event_commit_sha": "c" * 40,
            "locked_result_record_blob_sha": "d" * 40,
        },
    )
    record = v.expected_record(parent_sha="e" * 40, generated_at_utc="2026-09-19T14:00:00Z")
    record["future_work"]["new_empirical_epoch_authorized"] = True
    with pytest.raises(SystemExit, match="does not match the exact outcome-agnostic contract"):
        v.validate_record(record, parent_sha="e" * 40)


def test_tooling_source_never_reads_private_numerical_result() -> None:
    source = VALIDATOR_PATH.read_text(encoding="utf-8")
    preparer = (ROOT / "scripts/prepare_track_a_epoch_002_post_interpretation_disposition.py").read_text(
        encoding="utf-8"
    )
    combined = source + preparer
    assert "analysis-output" not in combined
    assert "track_a_epoch_002_local_interpretation.json" not in combined
    assert "estimate_pdmal_minus_random_regular" in source
    assert "PRIVATE_NUMERICAL_INTERPRETATION_REQUIRED=FALSE" in preparer
