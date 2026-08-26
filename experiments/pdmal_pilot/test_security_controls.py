"""Adversarial controls for the PDMAL pilot boundary."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

from pilot_artifact_schema import canonical_json_bytes, validate_artifact
from run_pilot import blind_condition, require_frozen_commit
from task_engine import SEED_RUNTIME_CEILING_SECONDS, validate_seed_runtime

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "experiments" / "pdmal_pilot" / "run_pilot.py"
TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)
CONDITIONS = ("null", "simple", "static", "dgaf")


def test_wrong_sha_rejected_even_when_authorized(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PROTOCOL_FROZEN", "1")
    monkeypatch.setenv("PDMAL_PILOT_AUTHORIZED", "1")
    monkeypatch.setenv("PDMAL_FROZEN_COMMIT_SHA", "0" * 40)
    with pytest.raises(SystemExit, match="frozen SHA mismatch"):
        require_frozen_commit()


def test_task_substitution_is_not_used_by_pilot_path() -> None:
    tree = ast.parse(RUNNER.read_text(encoding="utf-8"))
    pilot = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "run_pilot")
    names = {node.id for node in ast.walk(pilot) if isinstance(node, ast.Name)}
    assert "ConsensusTask" in names
    assert "ScriptedTask" not in names


def test_blinding_outputs_are_distinct_and_do_not_expose_labels() -> None:
    blinded = [blind_condition(label, "test-only-key") for label in CONDITIONS]
    assert len(set(blinded)) == len(CONDITIONS)
    assert all(value.startswith("blind_") for value in blinded)
    assert all(label not in value for label, value in zip(CONDITIONS, blinded))


def test_mock_unblinding_requires_the_custody_key() -> None:
    key = "mock-custody-key"
    mapping = {blind_condition(label, key): label for label in CONDITIONS}
    assert mapping[blind_condition("dgaf", key)] == "dgaf"
    wrong_mapping = {blind_condition(label, "wrong-key"): label for label in mapping.values()}
    assert blind_condition("dgaf", key) not in wrong_mapping


def test_runtime_ceiling_is_fail_closed() -> None:
    assert SEED_RUNTIME_CEILING_SECONDS == 300.0
    assert validate_seed_runtime(300.0) is True
    assert validate_seed_runtime(300.000001) is False


def _record(*, trial_id: int, condition: str, topology: str, failure_count: int, commit_sha: str = "a" * 40) -> dict:
    record = {
        "experiment_id": "PDMAL-PILOT-V1",
        "protocol_version": "0.7.5",
        "experiment_commit_sha": commit_sha,
        "seed_id": 20260819,
        "blinded_condition_id": blind_condition(condition, "test-schema-key"),
        "trial_id": trial_id,
        "topology": topology,
        "failure_count": failure_count,
        "primary_outcome": 0.1,
        "secondary_outcomes": {"final_mean": 0.0},
        "failure": failure_count > 0,
        "recovery": True,
        "ffcr_success": True,
        "runtime_ms": 1,
        "status": "SUCCESS",
        "excluded": False,
        "exclusion_reason": None,
        "environment_fingerprint": "env",
    }
    record["artifact_sha256"] = hashlib.sha256(canonical_json_bytes(record)).hexdigest()
    return record


def _document(*, commit_sha: str = "a" * 40) -> dict:
    records = []
    trial_id = 0
    for condition in CONDITIONS:
        for topology in TOPOLOGIES:
            for failure_count in FAILURE_COUNTS:
                records.append(
                    _record(
                        trial_id=trial_id,
                        condition=condition,
                        topology=topology,
                        failure_count=failure_count,
                        commit_sha=commit_sha,
                    )
                )
                trial_id += 1
    return {
        "schema_version": "1.0", "artifact_version": "seed-20260819",
        "protocol_status": "FROZEN", "empirical_data_collection": True,
        "frozen_commit_sha": commit_sha, "seed_id": 20260819,
        "runtime_seconds": 1.0, "records": records,
    }


def test_artifact_substitution_is_detectable() -> None:
    document = _document()
    validate_artifact(document, expected_seed=20260819)
    document["records"][0]["primary_outcome"] = 999.0
    with pytest.raises(AssertionError, match="artifact_sha256"):
        validate_artifact(document, expected_seed=20260819)


def test_ffcr_contract_fields_are_required_and_semantically_fail_closed() -> None:
    document = _document()
    document["records"][0].pop("ffcr_success")
    with pytest.raises(AssertionError, match="missing required record fields"):
        validate_artifact(document, expected_seed=20260819)

    bad = _record(trial_id=0, condition="null", topology="ring", failure_count=0)
    bad["status"] = "UNRECOVERED_FAILURE"
    bad["artifact_sha256"] = hashlib.sha256(canonical_json_bytes({k: v for k, v in bad.items() if k != "artifact_sha256"})).hexdigest()
    document["records"][0] = bad
    with pytest.raises(AssertionError, match="ffcr_success requires SUCCESS status"):
        validate_artifact(document, expected_seed=20260819)


def test_artifact_rejects_duplicate_matrix_cells() -> None:
    document = _document()
    document["records"][1]["topology"] = document["records"][0]["topology"]
    document["records"][1]["artifact_sha256"] = hashlib.sha256(
        canonical_json_bytes({k: v for k, v in document["records"][1].items() if k != "artifact_sha256"})
    ).hexdigest()
    with pytest.raises(AssertionError, match="duplicate pilot matrix cell"):
        validate_artifact(document, expected_seed=20260819)


def test_artifact_binds_record_commit_to_document_sha() -> None:
    document = _document()
    record = document["records"][0]
    record["experiment_commit_sha"] = "b" * 40
    record["artifact_sha256"] = hashlib.sha256(
        canonical_json_bytes({k: v for k, v in record.items() if k != "artifact_sha256"})
    ).hexdigest()
    with pytest.raises(AssertionError, match="experiment_commit_sha does not match"):
        validate_artifact(document, expected_seed=20260819)
