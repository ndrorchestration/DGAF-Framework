from __future__ import annotations

import ast
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

import pytest

from scripts import (
    prepare_track_a_epoch_002_verification_classification as verification,
)

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "experiments/pdmal_pilot/run_track_a_epoch_002.py"
CONTRACT = json.loads((ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json").read_text(encoding="utf-8"))


def load_runner_expected_verification() -> Callable[..., dict[str, Any]]:
    tree = ast.parse(RUNNER_PATH.read_text(encoding="utf-8"), filename=str(RUNNER_PATH))
    functions: list[ast.stmt] = [
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "expected_verification"
    ]
    assert len(functions) == 1
    module = ast.Module(body=functions, type_ignores=[])
    ast.fix_missing_locations(module)
    namespace: dict[str, Any] = {"PROTOCOL_ID": CONTRACT["protocol_id"]}
    exec(compile(module, str(RUNNER_PATH), "exec"), namespace)
    function = namespace["expected_verification"]
    assert callable(function)
    return function


def sample_record() -> dict[str, Any]:
    return verification.expected_record(
        protocol_id=CONTRACT["protocol_id"],
        candidate_sha="a" * 40,
        closure_blob_sha="b" * 40,
    )


def test_expected_record_matches_collection_runner_contract() -> None:
    runner_expected_verification = load_runner_expected_verification()
    helper_record = sample_record()
    runner_record = runner_expected_verification(candidate_sha="a" * 40, closure_blob_sha="b" * 40)
    assert helper_record == runner_record


def test_expected_record_is_explicitly_nonindependent_and_nonauthorizing() -> None:
    record = sample_record()
    assert record["verification_status"] == "PASS"
    assert record["verification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    assert record["independent_verification"] is False
    assert record["same_system_custody"] is True
    assert record["scientific_n_increment"] == 0
    assert record["collection_authorized"] is False
    assert record["unblinding_authorized"] is False
    assert record["primary_analysis_authorized"] is False
    assert record["high_assurance_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("verification_status", "INDEPENDENT_PASS"),
        ("verification_class", "INDEPENDENT"),
        ("independent_verification", True),
        ("same_system_custody", False),
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
    with pytest.raises(SystemExit, match="verification record mismatch"):
        verification.validate_record(changed, expected)


def test_validate_record_rejects_extra_field() -> None:
    expected = sample_record()
    changed = deepcopy(expected)
    changed["authorizes_collection"] = True
    with pytest.raises(SystemExit, match="verification record mismatch"):
        verification.validate_record(changed, expected)


def test_collection_authorization_presence_fails_closed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    auth_path = tmp_path / "authorization.json"
    auth_path.write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(verification, "AUTH_PATH", auth_path)
    with pytest.raises(SystemExit, match="collection authorization must remain absent"):
        verification.reject_authorization()


def test_validate_retained_verification_does_not_reapply_creation_gate(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    base_sha = "f" * 40
    candidate_sha = "a" * 40
    closure_blob_sha = "b" * 40
    record = verification.expected_record(
        protocol_id=CONTRACT["protocol_id"],
        candidate_sha=candidate_sha,
        closure_blob_sha=closure_blob_sha,
    )
    verification_path = tmp_path / "verification.json"
    verification_path.write_text(json.dumps(record), encoding="utf-8")

    monkeypatch.setattr(verification, "VERIFICATION_PATH", verification_path)
    monkeypatch.setattr(verification, "validate_contract", lambda: {"protocol_id": CONTRACT["protocol_id"]})
    monkeypatch.setattr(
        verification,
        "reject_authorization",
        lambda: pytest.fail("retained verification validation re-applied the creation-time authorization gate"),
    )
    monkeypatch.setattr(
        verification,
        "git_path_exists",
        lambda path, revision="HEAD": path == verification.VERIFICATION_REL and revision in {"HEAD", base_sha},
    )
    monkeypatch.setattr(verification, "require_valid_closure", lambda: (candidate_sha, closure_blob_sha))
    monkeypatch.setattr(
        verification,
        "git_history",
        lambda path, revision="HEAD": (("d" * 40,) if path == verification.VERIFICATION_REL else ("c" * 40,)),
    )
    monkeypatch.setattr(verification, "is_ancestor", lambda ancestor, descendant: True)
    monkeypatch.setattr(verification, "git_blob", lambda path, revision="HEAD": "9" * 40)

    verification.validate_verification(base_sha)


def test_closure_history_must_be_immutable(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    closure_path = tmp_path / "closure.json"
    closure_path.write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(verification, "CLOSURE_PATH", closure_path)
    monkeypatch.setattr(verification, "git_path_exists", lambda path, revision="HEAD": True)
    monkeypatch.setattr(verification, "validate_contract", lambda: {"protocol_id": CONTRACT["protocol_id"]})
    monkeypatch.setattr(verification.closure, "require_valid_freeze", lambda: ("a" * 40, "b" * 40))
    monkeypatch.setattr(verification.closure, "expected_record", lambda **kwargs: {})
    monkeypatch.setattr(verification.closure, "validate_record", lambda actual, expected: None)
    monkeypatch.setattr(verification, "git_history", lambda path, revision="HEAD": ("c" * 40, "d" * 40))
    with pytest.raises(SystemExit, match="closure packet must have exactly one immutable history commit"):
        verification.require_valid_closure()


def isolate_verification_absence(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Model a pre-verification state without hiding any other repository evidence."""
    original_git_path_exists = verification.git_path_exists
    monkeypatch.setattr(verification, "VERIFICATION_PATH", tmp_path / "missing-verification.json")
    monkeypatch.setattr(
        verification,
        "git_path_exists",
        lambda path, revision="HEAD": (
            False if path == verification.VERIFICATION_REL else original_git_path_exists(path, revision)
        ),
    )


def test_prepare_fails_closed_while_closure_absent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    isolate_verification_absence(monkeypatch, tmp_path)
    monkeypatch.setattr(verification, "CLOSURE_PATH", tmp_path / "missing-closure.json")
    with pytest.raises(SystemExit, match="canonical final-closure packet is absent"):
        verification.prepare()


def test_boundary_proves_verification_absent_when_verification_absent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    isolate_verification_absence(monkeypatch, tmp_path)
    verification.validate_boundary()
    output = capsys.readouterr().out
    assert "TRACK_A_EPOCH_002_VERIFICATION_TOOLING=PASS_VERIFICATION_ABSENT" in output
    assert "INDEPENDENT_VERIFICATION=FALSE" in output
    assert "SUCCESSOR_COLLECTION_AUTHORIZED=FALSE" in output
    assert "SCIENTIFIC_N_INCREMENT=0" in output


def test_helper_has_no_secret_input_surface() -> None:
    text = (ROOT / "scripts/prepare_track_a_epoch_002_verification_classification.py").read_text(encoding="utf-8")
    assert "--passphrase" not in text
    assert "PDMAL_BLINDING_KEY" not in text
    assert "genpkey" not in text
    assert "private_key_encrypted" not in text


def test_current_runner_contract_remains_non_authorizing() -> None:
    contract = verification.validate_contract()
    assert contract["successor_collection"] == "NOT_AUTHORIZED"
    assert contract["primary_analysis"] == "NOT_AUTHORIZED"
    assert contract["scientific_n_increment"] == 0
