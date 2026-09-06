from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import mode_t_timing_study as timing
from task_engine import AttemptStatus


def test_canonical_timing_shapes_match_locked_pilot_and_analysis() -> None:
    assert timing.expected_trials_per_seed() == 180
    documents = timing.build_synthetic_analysis_documents(seed_count=2)
    assert len(documents) == 2
    assert all(len(document["records"]) == 180 for document in documents)
    assert {
        record["blinded_condition_id"]
        for record in documents[0]["records"]
    } == set(timing.CONDITION_MAP)


def test_synthetic_analysis_fixture_contains_no_pilot_outcome_artifact_fields() -> None:
    document = timing.build_synthetic_analysis_documents(seed_count=1)[0]
    forbidden = {
        "primary_outcome",
        "secondary_outcomes",
        "artifact_sha256",
        "runtime_ms",
        "status",
        "environment_fingerprint",
    }
    for record in document["records"]:
        assert forbidden.isdisjoint(record)


def test_timing_stats_reject_invalid_samples() -> None:
    with pytest.raises(ValueError):
        timing._timing_stats([])
    with pytest.raises(ValueError):
        timing._timing_stats([float("nan")])
    with pytest.raises(ValueError):
        timing._timing_stats([-1.0])


def test_required_tlock_reverification_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("P4_MODE_T_TLOCK_SHA256_VERIFIED", raising=False)
    monkeypatch.delenv("P4_MODE_T_TLOCK_SHA256", raising=False)
    with pytest.raises(RuntimeError, match="tlock release asset"):
        timing._tlock_reverification_stage(require_tlock_verification=True)


def test_matrix_timing_accepts_returned_fail_closed_trial_classification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ReturnedFailureTask:
        def __init__(self, *, topology: str, failure_count: int, condition: str) -> None:
            del topology, failure_count, condition

        def run_detailed(self, *, seed: int, attempt: int = 1):
            del seed, attempt
            return SimpleNamespace(attempt_status=AttemptStatus.FAILURE)

    monkeypatch.setattr(timing, "_validate_canonical_shapes", lambda: None)
    monkeypatch.setattr(timing, "TOPOLOGY_SPECS", {"ring": object()})
    monkeypatch.setattr(timing, "CONDITION_VALUES", ("dgaf",))
    monkeypatch.setattr(timing, "PILOT_FAILURE_COUNTS", (0,))
    monkeypatch.setattr(timing, "ConsensusTask", ReturnedFailureTask)

    assert timing.measure_full_synthetic_matrix(1234) >= 0.0


def test_matrix_timing_still_fails_on_execution_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class RaisingTask:
        def __init__(self, *, topology: str, failure_count: int, condition: str) -> None:
            del topology, failure_count, condition

        def run_detailed(self, *, seed: int, attempt: int = 1):
            del seed, attempt
            raise RuntimeError("synthetic execution crash")

    monkeypatch.setattr(timing, "_validate_canonical_shapes", lambda: None)
    monkeypatch.setattr(timing, "TOPOLOGY_SPECS", {"ring": object()})
    monkeypatch.setattr(timing, "CONDITION_VALUES", ("dgaf",))
    monkeypatch.setattr(timing, "PILOT_FAILURE_COUNTS", (0,))
    monkeypatch.setattr(timing, "ConsensusTask", RaisingTask)

    with pytest.raises(RuntimeError, match="synthetic execution crash"):
        timing.measure_full_synthetic_matrix(1234)


def test_partial_study_cannot_propose_w(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("P4_MODE_T_TLOCK_SHA256_VERIFIED", "1")
    monkeypatch.setenv("P4_MODE_T_TLOCK_SHA256", timing.EXPECTED_TLOCK_SHA256)
    monkeypatch.setenv("EVIDENCE_SHA", "a" * 40)
    monkeypatch.setattr(
        timing,
        "measure_full_synthetic_matrix",
        lambda seed: 1000.0 + float(seed % 10),
    )
    monkeypatch.setattr(timing, "measure_locked_primary_analysis", lambda: 25.0)

    output = tmp_path / "timing.json"
    artifact = timing.run_study(
        output_path=output,
        repetitions=2,
        require_tlock_verification=True,
    )

    assert artifact["coverage_complete"] is False
    assert artifact["w_proposal_eligible"] is False
    assert artifact["numeric_w_selected"] is False
    assert artifact["proposed_w_seconds"] is None
    assert artifact["empirical_data_collection"] is False
    assert artifact["secret_instantiation"] is False
    assert artifact["stages"]["exact_tlock_asset_reverification"]["status"] == "PASS"
    assert artifact["stages"]["synthetic_timelock_encryption_timing"]["status"] == "NOT_EXECUTED"
    assert artifact["stages"]["external_transparency_retention_timing"]["status"] == "NOT_EXECUTED"

    raw = output.read_bytes()
    sidecar = output.with_suffix(".json.sha256").read_text(encoding="utf-8")
    expected_digest, expected_name = sidecar.split()
    assert expected_name == output.name
    assert expected_digest == hashlib.sha256(raw).hexdigest()
    assert json.loads(raw)["epistemic_status"] == "PARTIAL_SYNTHETIC_TIMING_NOT_W_EVIDENCE"


def test_repetition_bounds_are_fail_closed(tmp_path: Path) -> None:
    for invalid in (0, 21, True):
        with pytest.raises(ValueError):
            timing.run_study(output_path=tmp_path / "x.json", repetitions=invalid)
