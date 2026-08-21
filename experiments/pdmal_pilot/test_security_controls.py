"""Adversarial controls for the PDMAL pilot boundary."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import pytest

from pilot_artifact_schema import validate_artifact
from run_pilot import blind_condition, require_frozen_commit
from task_engine import SEED_RUNTIME_CEILING_SECONDS, validate_seed_runtime

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "experiments" / "pdmal_pilot" / "run_pilot.py"


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
    labels = ["null", "simple", "static", "dgaf"]
    blinded = [blind_condition(label, "test-only-key") for label in labels]
    assert len(set(blinded)) == len(labels)
    assert all(value.startswith("blind_") for value in blinded)
    assert all(label not in value for label, value in zip(labels, blinded))


def test_mock_unblinding_requires_the_custody_key() -> None:
    key = "mock-custody-key"
    mapping = {blind_condition(label, key): label for label in ("null", "simple", "static", "dgaf")}
    assert mapping[blind_condition("dgaf", key)] == "dgaf"
    wrong_mapping = {blind_condition(label, "wrong-key"): label for label in mapping.values()}
    assert blind_condition("dgaf", key) not in wrong_mapping


def test_runtime_ceiling_is_fail_closed() -> None:
    assert SEED_RUNTIME_CEILING_SECONDS == 300.0
    assert validate_seed_runtime(300.0) is True
    assert validate_seed_runtime(300.000001) is False


def _record() -> dict:
    record = {
        "experiment_id": "PDMAL-PILOT-V1",
        "protocol_version": "0.7.4",
        "experiment_commit_sha": "a" * 40,
        "seed_id": 20260819,
        "blinded_condition_id": "blind_0123456789abcdef",
        "trial_id": 0,
        "primary_outcome": 0.1,
        "secondary_outcomes": {"topology": "ring", "failure_count": 0, "final_mean": 0.0},
        "failure": False,
        "recovery": True,
        "runtime_ms": 1,
        "status": "SUCCESS",
        "excluded": False,
        "exclusion_reason": None,
        "environment_fingerprint": "env",
    }
    record["artifact_sha256"] = hashlib.sha256(
        (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    return record


def test_artifact_substitution_is_detectable() -> None:
    document = {
        "schema_version": "1.0",
        "artifact_version": "seed-20260819",
        "protocol_status": "FROZEN",
        "empirical_data_collection": True,
        "frozen_commit_sha": "a" * 40,
        "seed_id": 20260819,
        "runtime_seconds": 1.0,
        "records": [_record() for _ in range(180)],
    }
    validate_artifact(document, expected_seed=20260819)
    document["records"][0]["primary_outcome"] = 999.0
    with pytest.raises(AssertionError, match="artifact_sha256"):
        validate_artifact(document, expected_seed=20260819)
