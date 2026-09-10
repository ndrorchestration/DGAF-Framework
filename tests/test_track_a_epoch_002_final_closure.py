from __future__ import annotations

import ast
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

import pytest

from scripts import prepare_track_a_epoch_002_final_closure as closure

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "experiments/pdmal_pilot/run_track_a_epoch_002.py"
CONTRACT = json.loads((ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json").read_text(encoding="utf-8"))


def load_runner_expected_closure() -> Callable[..., dict[str, Any]]:
    tree = ast.parse(RUNNER_PATH.read_text(encoding="utf-8"), filename=str(RUNNER_PATH))
    functions: list[ast.stmt] = [
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "expected_closure"
    ]
    assert len(functions) == 1
    module = ast.Module(body=functions, type_ignores=[])
    ast.fix_missing_locations(module)
    namespace: dict[str, Any] = {"PROTOCOL_ID": CONTRACT["protocol_id"]}
    exec(compile(module, str(RUNNER_PATH), "exec"), namespace)
    function = namespace["expected_closure"]
    assert callable(function)
    return function


def sample_record() -> dict[str, Any]:
    return closure.expected_record(
        protocol_id=CONTRACT["protocol_id"],
        candidate_sha="a" * 40,
        freeze_blob_sha="b" * 40,
    )


def test_expected_record_matches_collection_runner_contract() -> None:
    runner_expected_closure = load_runner_expected_closure()
    helper_record = closure.expected_record(
        protocol_id=CONTRACT["protocol_id"],
        candidate_sha="a" * 40,
        freeze_blob_sha="b" * 40,
    )
    runner_record = runner_expected_closure(candidate_sha="a" * 40, freeze_blob_sha="b" * 40)
    assert helper_record == runner_record


def test_expected_record_is_non_authorizing() -> None:
    record = sample_record()
    assert record["open_blockers"] == []
    assert record["closure_status"] == "CLOSED_VERIFIED_FOR_AUTHORIZATION_REVIEW"
    assert record["scientific_n_increment"] == 0
    assert record["collection_authorized"] is False
    assert record["unblinding_authorized"] is False
    assert record["primary_analysis_authorized"] is False
    assert record["high_assurance_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("open_blockers", ["invented"]),
        ("closure_status", "AUTHORIZED"),
        ("scientific_n_increment", 1),
        ("collection_authorized", True),
        ("unblinding_authorized", True),
        ("primary_analysis_authorized", True),
        ("high_assurance_authorized", True),
    ],
)
def test_validate_record_rejects_mutation(field: str, value: object) -> None:
    expected = sample_record()
    changed = deepcopy(expected)
    changed[field] = value
    with pytest.raises(SystemExit, match="closure record mismatch"):
        closure.validate_record(changed, expected)


def test_validate_record_rejects_extra_field() -> None:
    expected = sample_record()
    changed = deepcopy(expected)
    changed["authorization"] = True
    with pytest.raises(SystemExit, match="closure record mismatch"):
        closure.validate_record(changed, expected)


def test_downstream_gate_presence_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        closure,
        "git_path_exists",
        lambda path, revision="HEAD": path == closure.AUTH_REL,
    )
    with pytest.raises(SystemExit, match="downstream successor gates must remain absent"):
        closure.reject_downstream_gates()


def test_freeze_history_must_be_immutable(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    record = {
        "frozen_candidate_sha": "a" * 40,
        "frozen_candidate_tree_sha": "b" * 40,
    }
    freeze_path = tmp_path / "freeze.json"
    freeze_path.write_text(json.dumps(record), encoding="utf-8")
    monkeypatch.setattr(closure, "FREEZE_PATH", freeze_path)
    monkeypatch.setattr(closure, "git_path_exists", lambda path, revision="HEAD": True)
    monkeypatch.setattr(closure, "validate_contract", lambda: {"protocol_id": CONTRACT["protocol_id"]})
    monkeypatch.setattr(
        closure.freeze,
        "require_valid_preflight",
        lambda: ({}, "a" * 40, "b" * 40, "c" * 40),
    )
    monkeypatch.setattr(closure.freeze, "protected_source_blobs_at", lambda candidate: {})
    monkeypatch.setattr(closure.freeze, "require_sources_unchanged", lambda candidate, protected: None)
    monkeypatch.setattr(closure.freeze, "expected_record", lambda **kwargs: record)
    monkeypatch.setattr(closure.freeze, "validate_record", lambda actual, expected: None)
    monkeypatch.setattr(closure, "git_history", lambda path, revision="HEAD": ("d" * 40, "e" * 40))
    with pytest.raises(SystemExit, match="freeze manifest must have exactly one immutable history commit"):
        closure.require_valid_freeze()


def test_prepare_fails_closed_while_freeze_absent() -> None:
    with pytest.raises(SystemExit, match="canonical immutable-freeze manifest is absent"):
        closure.prepare()


def test_current_boundary_proves_closure_absent(capsys: pytest.CaptureFixture[str]) -> None:
    closure.validate_boundary()
    output = capsys.readouterr().out
    assert "TRACK_A_EPOCH_002_FINAL_CLOSURE_TOOLING=PASS_CLOSURE_ABSENT" in output
    assert "SUCCESSOR_COLLECTION_AUTHORIZED=FALSE" in output
    assert "SCIENTIFIC_N_INCREMENT=0" in output


def test_helper_has_no_secret_input_surface() -> None:
    text = (ROOT / "scripts/prepare_track_a_epoch_002_final_closure.py").read_text(encoding="utf-8")
    assert "--passphrase" not in text
    assert "PDMAL_BLINDING_KEY" not in text
    assert "genpkey" not in text
    assert "private_key_encrypted" not in text


def test_current_runner_contract_remains_non_authorizing() -> None:
    contract = closure.validate_contract()
    assert contract["track_a_freeze"] == "NOT_ESTABLISHED"
    assert contract["successor_collection"] == "NOT_AUTHORIZED"
    assert contract["primary_analysis"] == "NOT_AUTHORIZED"
    assert contract["scientific_n_increment"] == 0
