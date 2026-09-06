"""Adversarial controls for the PDMAL pilot boundary."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

from pilot_artifact_schema import ARTIFACT_SCHEMA_VERSION, canonical_json_bytes, validate_artifact
from run_pilot import (
    _trial_combinations,
    blind_condition,
    blinded_trial_schedule,
    require_frozen_commit,
)
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


def test_blinded_trial_schedule_is_complete_keyed_and_reconstructible() -> None:
    seed = 20260819
    key = "custody-key-a"
    schedule = blinded_trial_schedule(seed=seed, key=key)
    canonical = _trial_combinations()

    assert len(schedule) == 180
    assert len(set(schedule)) == 180
    assert set(schedule) == set(canonical)
    assert schedule == blinded_trial_schedule(seed=seed, key=key)
    assert schedule != canonical
    assert schedule != blinded_trial_schedule(seed=seed, key="custody-key-b")
    assert schedule != blinded_trial_schedule(seed=seed + 1, key=key)


def test_old_public_trial_id_condition_decoder_no_longer_recovers_schedule() -> None:
    """Regression for #307: canonical 9-cell condition blocks must be broken."""
    schedule = blinded_trial_schedule(seed=20260819, key="fixed-regression-custody-key")
    guessed = []
    for trial_id, (_, actual_condition, _) in enumerate(schedule):
        canonical_condition_index = (trial_id % 36) // 9
        guessed_condition = CONDITIONS[canonical_condition_index]
        guessed.append(guessed_condition == actual_condition)
    assert not all(guessed)
    assert sum(guessed) < len(schedule)


def test_runtime_ceiling_is_fail_closed() -> None:
    assert SEED_RUNTIME_CEILING_SECONDS == 300.0
    assert validate_seed_runtime(300.0) is True
    assert validate_seed_runtime(300.000001) is False


def _rehash(record: dict) -> None:
    record["artifact_sha256"] = hashlib.sha256(
        canonical_json_bytes({k: v for k, v in record.items() if k != "artifact_sha256"})
    ).hexdigest()


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
        "status": "SUCCESS",
        "excluded": False,
        "exclusion_reason": None,
        "environment_fingerprint": "env",
    }
    _rehash(record)
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
        "schema_version": ARTIFACT_SCHEMA_VERSION, "artifact_version": "seed-20260819",
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
    _rehash(bad)
    document["records"][0] = bad
    with pytest.raises(AssertionError, match="ffcr_success requires SUCCESS or RECOVERED status"):
        validate_artifact(document, expected_seed=20260819)


def test_artifact_rejects_duplicate_matrix_cells() -> None:
    document = _document()
    # Make one record a duplicate matrix cell while preserving a distinct ID.
    document["records"][9]["blinded_condition_id"] = document["records"][0]["blinded_condition_id"]
    document["records"][9]["topology"] = document["records"][0]["topology"]
    document["records"][9]["failure_count"] = document["records"][0]["failure_count"]
    _rehash(document["records"][9])
    with pytest.raises(AssertionError, match="duplicate pilot matrix cell"):
        validate_artifact(document, expected_seed=20260819)


def test_artifact_binds_record_commit_to_document_sha() -> None:
    document = _document()
    record = document["records"][0]
    record["experiment_commit_sha"] = "b" * 40
    _rehash(record)
    with pytest.raises(AssertionError, match="experiment_commit_sha does not match"):
        validate_artifact(document, expected_seed=20260819)


@pytest.mark.parametrize("field,value", [
    ("governance_trace", [{"decision": "PASS"}]),
    ("runtime_ms", 1),
    ("condition", "dgaf"),
])
def test_condition_identity_side_channel_fields_fail_closed(field: str, value: object) -> None:
    document = _document()
    record = document["records"][0]
    record[field] = value
    _rehash(record)
    with pytest.raises(AssertionError, match="unexpected record fields"):
        validate_artifact(document, expected_seed=20260819)
