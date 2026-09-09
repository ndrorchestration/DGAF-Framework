from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import mode_t_timing_study as timing
from task_engine import AttemptStatus


def _valid_encryption_evidence(head: str) -> dict:
    return {
        "schema_version": 1,
        "evidence_class": timing.TLOCK_ENCRYPTION_EVIDENCE_CLASS,
        "control_plane_sha": head,
        "tlock_sha256": timing.EXPECTED_TLOCK_SHA256,
        "network_endpoint": timing.EXPECTED_DRAND_ENDPOINT,
        "chain_hash": timing.EXPECTED_QUICKNET_CHAIN_HASH,
        "scheme": timing.EXPECTED_QUICKNET_SCHEME,
        "public_key": timing.EXPECTED_QUICKNET_PUBLIC_KEY,
        "network_metadata_verified": True,
        "metadata_current_round": 1000,
        "target_round": 2200,
        "sample_count": 5,
        "samples_ms": [101.0, 98.5, 102.25, 99.75, 100.5],
        "payload_class": "P4_MODE_T_SYNTHETIC_TIMING_NOT_AUTHORIZATION",
        "payload_bytes": 4096,
        "all_encryptions_succeeded": True,
        "ciphertexts_retained": False,
        "empirical_data_collection": False,
        "secret_instantiation": False,
        "pilot_authorized": False,
    }


def _write_json(path: Path, document: dict) -> Path:
    path.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")
    return path


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


def test_valid_tlock_encryption_evidence_is_accepted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    head = "a" * 40
    monkeypatch.setenv("EVIDENCE_SHA", head)
    path = _write_json(tmp_path / "encryption.json", _valid_encryption_evidence(head))

    stage = timing._load_tlock_encryption_stage(path)

    assert stage["status"] == "PASS"
    assert stage["chain_hash"] == timing.EXPECTED_QUICKNET_CHAIN_HASH
    assert stage["statistics"]["sample_count"] == 5
    assert stage["ciphertexts_retained"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("control_plane_sha", "b" * 40, "head mismatch"),
        ("tlock_sha256", "0" * 64, "tlock digest mismatch"),
        ("chain_hash", "0" * 64, "chain hash mismatch"),
        ("scheme", "wrong-scheme", "scheme mismatch"),
        ("public_key", "wrong-key", "public key mismatch"),
        ("network_metadata_verified", False, "lacks verified network metadata"),
        ("ciphertexts_retained", True, "must not retain ciphertext"),
        ("empirical_data_collection", True, "must be non-empirical"),
        ("secret_instantiation", True, "must not instantiate"),
        ("pilot_authorized", True, "must not assert pilot authorization"),
    ],
)
def test_tlock_encryption_evidence_mismatches_fail_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: object,
    match: str,
) -> None:
    head = "a" * 40
    monkeypatch.setenv("EVIDENCE_SHA", head)
    evidence = _valid_encryption_evidence(head)
    evidence[field] = value
    path = _write_json(tmp_path / "encryption.json", evidence)

    with pytest.raises(ValueError, match=match):
        timing._load_tlock_encryption_stage(path)


def test_tlock_encryption_evidence_rejects_invalid_round_and_sample_contracts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    head = "a" * 40
    monkeypatch.setenv("EVIDENCE_SHA", head)

    evidence = _valid_encryption_evidence(head)
    evidence["target_round"] = evidence["metadata_current_round"]
    with pytest.raises(ValueError, match="invalid round binding"):
        timing._load_tlock_encryption_stage(_write_json(tmp_path / "round.json", evidence))

    evidence = _valid_encryption_evidence(head)
    evidence["samples_ms"] = [1.0, 2.0]
    evidence["sample_count"] = 2
    with pytest.raises(ValueError, match="sample count"):
        timing._load_tlock_encryption_stage(_write_json(tmp_path / "samples.json", evidence))


def test_partial_study_cannot_propose_w_even_with_encryption_timing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    head = "a" * 40
    monkeypatch.setenv("P4_MODE_T_TLOCK_SHA256_VERIFIED", "1")
    monkeypatch.setenv("P4_MODE_T_TLOCK_SHA256", timing.EXPECTED_TLOCK_SHA256)
    monkeypatch.setenv("EVIDENCE_SHA", head)
    monkeypatch.setattr(
        timing,
        "measure_full_synthetic_matrix",
        lambda seed: 1000.0 + float(seed % 10),
    )
    monkeypatch.setattr(timing, "measure_locked_primary_analysis", lambda: 25.0)
    encryption_path = _write_json(
        tmp_path / "encryption.json", _valid_encryption_evidence(head)
    )

    output = tmp_path / "timing.json"
    artifact = timing.run_study(
        output_path=output,
        repetitions=2,
        require_tlock_verification=True,
        tlock_encryption_evidence=encryption_path,
    )

    assert artifact["coverage_complete"] is False
    assert artifact["w_proposal_eligible"] is False
    assert artifact["numeric_w_selected"] is False
    assert artifact["proposed_w_seconds"] is None
    assert artifact["empirical_data_collection"] is False
    assert artifact["secret_instantiation"] is False
    assert artifact["stages"]["exact_tlock_asset_reverification"]["status"] == "PASS"
    assert artifact["stages"]["synthetic_timelock_encryption_timing"]["status"] == "PASS"
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
