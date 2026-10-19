"""Operator-local fake-provider effect pilot, not a confirmatory scientific evaluation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments/governance_benchmark/effect_pilot/run_pilot.py"
spec = importlib.util.spec_from_file_location("effect_pilot_v1", SOURCE)
assert spec and spec.loader
pilot = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = pilot
spec.loader.exec_module(pilot)

ORACLE_SHA256 = "1d4312938a5847c6e000faa73a10c0660108044aebc84319b45be414bd4f34d0"


def test_requires_explicit_oracle_identity() -> None:
    with pytest.raises(RuntimeError, match="BLOCKED_ORACLE_DIGEST_NOT_SUPPLIED"):
        pilot.run()


def test_oracle_mutation_fails_closed(tmp_path: Path) -> None:
    original = pilot.ORACLE.read_text(encoding="utf-8")
    mutated = tmp_path / "oracle.json"
    mutated.write_text(original.replace("NORMAL_SUCCESS", "SILENT_DRIFT"), encoding="utf-8")
    with pytest.raises(RuntimeError, match="BLOCKED_ORACLE_DIGEST_MISMATCH"):
        pilot.run(mutated, expected_sha256=ORACLE_SHA256)


def test_effects_are_measured_from_fake_provider_log() -> None:
    report = pilot.run(expected_sha256=ORACLE_SHA256)
    rows = report["rows"]
    assert len(rows) == 8
    assert report["summary"]["operator_oracle_matches"] == 8
    assert report["summary"]["arm_parity"] is True
    for row in rows:
        assert len(row["observed_completed_effects"]) == 1
        assert row["effect_count_matches"]
        assert row["no_duplicate_completed_effects"]
        assert row["actual_external_effect"] is False
        assert row["human_active_minutes"] is None


def test_unknown_outcome_does_not_blindly_repeat_provider_write() -> None:
    report = pilot.run(expected_sha256=ORACLE_SHA256)
    for row in report["rows"]:
        if row["case_id"] == "GOV2-04":
            assert row["decisions"][-2:] == ["OUTCOME_UNKNOWN", "RECONCILE_REQUIRED"]
            assert row["fake_provider_attempts"] == 1


def test_interleaved_second_claim_never_dispatches() -> None:
    report = pilot.run(expected_sha256=ORACLE_SHA256)
    for row in report["rows"]:
        if row["case_id"] == "GOV2-05":
            assert row["decisions"][1] == "IN_FLIGHT"
            assert row["fake_provider_attempts"] == 1


def test_recovery_not_satisfied_by_receipt_or_synthetic_timeout_alone() -> None:
    report = pilot.run(expected_sha256=ORACLE_SHA256)
    for row in report["rows"]:
        if row["case_id"] == "GOV2-06":
            assert "RECONCILE_REQUIRED" in row["decisions"]
            assert "NON_EFFECT_OBSERVED" in row["decisions"]
            assert row["fake_provider_attempts"] == 2
            assert row["observed_completed_effects"] == [row["case_id"] + ":operation"]


def test_no_scientific_or_independent_claim() -> None:
    report = pilot.run(expected_sha256=ORACLE_SHA256)
    assert report["summary"]["scientific_n_increment"] == 0
    assert report["summary"]["human_workload_measurements"] == 0
    assert report["claim_ceiling"]["INDEPENDENT_VALIDATION"] == "NOT_ESTABLISHED"
    assert "NOT_INDEPENDENTLY_VALIDATED" in report["scope"]


def test_static_operator_oracle_digest_is_pinned() -> None:
    assert pilot.oracle_digest() == ORACLE_SHA256


def test_corrupt_fake_provider_duplicate_effect_is_caught(monkeypatch: pytest.MonkeyPatch) -> None:
    original_dispatch = pilot.FakeProvider.dispatch

    def duplicate_dispatch(provider, operation_id: str, fault: str = "NONE"):
        response = original_dispatch(provider, operation_id, fault=fault)
        provider.completed_effect_ids.append(operation_id)
        return response

    monkeypatch.setattr(pilot.FakeProvider, "dispatch", duplicate_dispatch)
    report = pilot.run(expected_sha256=ORACLE_SHA256)
    assert report["summary"]["operator_oracle_matches"] < report["summary"]["total_rows"]
    assert any(not row["no_duplicate_completed_effects"] for row in report["rows"])


def test_matched_conventional_ledger_is_separate_implementation() -> None:
    dgaf_ledger = pilot.InMemoryIdempotencyLedger()
    conventional_ledger = pilot.ConventionalMatchedLedger()
    assert type(dgaf_ledger) is not type(conventional_ledger)
    assert pilot.ConventionalConflict is not pilot.IdempotencyConflict
    assert pilot.ConventionalInFlight is not pilot.IdempotencyInFlight
