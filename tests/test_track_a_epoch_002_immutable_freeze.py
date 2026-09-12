from __future__ import annotations

import ast
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

import pytest

from scripts import prepare_track_a_epoch_002_immutable_freeze as freeze

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "experiments/pdmal_pilot/run_track_a_epoch_002.py"
CONTRACT = json.loads((ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json").read_text(encoding="utf-8"))


def load_runner_expected_freeze() -> Callable[..., dict[str, Any]]:
    tree = ast.parse(RUNNER_PATH.read_text(encoding="utf-8"), filename=str(RUNNER_PATH))
    functions: list[ast.stmt] = [
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "expected_freeze"
    ]
    assert len(functions) == 1
    module = ast.Module(body=functions, type_ignores=[])
    ast.fix_missing_locations(module)
    namespace: dict[str, Any] = {"PROTOCOL_ID": CONTRACT["protocol_id"]}
    exec(compile(module, str(RUNNER_PATH), "exec"), namespace)
    function = namespace["expected_freeze"]
    assert callable(function)
    return function


def resolve_literal(node: ast.AST, values: dict[str, Any]) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return values[node.id]
    if isinstance(node, ast.Tuple):
        return tuple(resolve_literal(element, values) for element in node.elts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left = str(resolve_literal(node.left, values)).rstrip("/")
        right = str(resolve_literal(node.right, values)).lstrip("/")
        return f"{left}/{right}"
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id in {"Path", "str"} and len(node.args) == 1:
            return str(resolve_literal(node.args[0], values))
    raise AssertionError(f"unsupported runner literal: {ast.dump(node)}")


def runner_protected_source_paths() -> tuple[str, ...]:
    tree = ast.parse(RUNNER_PATH.read_text(encoding="utf-8"), filename=str(RUNNER_PATH))
    values: dict[str, Any] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            values[target.id] = resolve_literal(node.value, values)
        except (AssertionError, KeyError):
            continue
    protected = values["PROTECTED_SOURCE_PATHS"]
    assert isinstance(protected, tuple)
    assert all(isinstance(path, str) for path in protected)
    return protected


def sample_record() -> dict[str, Any]:
    return freeze.expected_record(
        protocol_id=CONTRACT["protocol_id"],
        candidate_sha="a" * 40,
        candidate_tree_sha="b" * 40,
        preflight_blob_sha="c" * 40,
        protected_source_blobs={"example": "d" * 40},
    )


def test_expected_record_matches_collection_runner_contract() -> None:
    runner_expected_freeze = load_runner_expected_freeze()
    protected = {"example": "d" * 40}
    helper_record = freeze.expected_record(
        protocol_id=CONTRACT["protocol_id"],
        candidate_sha="a" * 40,
        candidate_tree_sha="b" * 40,
        preflight_blob_sha="c" * 40,
        protected_source_blobs=protected,
    )
    runner_record = runner_expected_freeze(
        candidate_sha="a" * 40,
        candidate_tree_sha="b" * 40,
        preflight_blob_sha="c" * 40,
        protected_source_blobs=protected,
    )
    assert helper_record == runner_record


def test_protected_source_paths_match_runner_exactly() -> None:
    assert freeze.PROTECTED_SOURCE_PATHS == runner_protected_source_paths()
    assert freeze.PREFLIGHT_REL not in freeze.PROTECTED_SOURCE_PATHS
    assert freeze.FREEZE_REL not in freeze.PROTECTED_SOURCE_PATHS


def test_expected_record_is_non_authorizing() -> None:
    record = sample_record()
    assert record["freeze_status"] == "ESTABLISHED"
    assert record["scientific_n_increment"] == 0
    assert record["collection_authorized"] is False
    assert record["unblinding_authorized"] is False
    assert record["primary_analysis_authorized"] is False
    assert record["high_assurance_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("freeze_status", "NOT_ESTABLISHED"),
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
    with pytest.raises(SystemExit, match="freeze record mismatch"):
        freeze.validate_record(changed, expected)


def test_validate_record_rejects_extra_field() -> None:
    expected = sample_record()
    changed = deepcopy(expected)
    changed["authorization"] = True
    with pytest.raises(SystemExit, match="freeze record mismatch"):
        freeze.validate_record(changed, expected)


def test_source_drift_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(freeze, "git_path_exists", lambda path, revision="HEAD": True)
    monkeypatch.setattr(freeze, "git_blob", lambda path, revision: "b" * 40)
    monkeypatch.setattr(freeze, "is_ancestor", lambda ancestor, descendant: True)
    monkeypatch.setattr(freeze, "git", lambda *args: "c" * 40)
    with pytest.raises(SystemExit, match="protected source drift"):
        freeze.require_sources_unchanged("a" * 40, {"example": "a" * 40})


def test_downstream_gate_presence_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        freeze,
        "git_path_exists",
        lambda path, revision="HEAD": path == freeze.AUTH_REL,
    )
    with pytest.raises(SystemExit, match="downstream successor gates must remain absent"):
        freeze.reject_downstream_gates()


def test_candidate_tree_mismatch_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    candidate = "a" * 40
    candidate_tree = "b" * 40
    record = {"candidate_sha": candidate, "candidate_tree_sha": candidate_tree}
    path = tmp_path / "preflight.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    monkeypatch.setattr(freeze, "PREFLIGHT_PATH", path)
    monkeypatch.setattr(freeze, "git_path_exists", lambda path, revision="HEAD": True)
    monkeypatch.setattr(freeze.preflight, "prepare", lambda sha: record)
    monkeypatch.setattr(
        freeze.preflight,
        "expected_record_for_candidate",
        lambda sha: record,
        raising=False,
    )
    monkeypatch.setattr(freeze.preflight, "validate_record", lambda actual, expected: None)
    monkeypatch.setattr(freeze, "git", lambda *args: "c" * 40)
    with pytest.raises(SystemExit, match="candidate tree mismatch"):
        freeze.require_valid_preflight()


def test_require_valid_preflight_does_not_reapply_preflight_creation_gate(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    candidate = "a" * 40
    candidate_tree = "b" * 40
    record = {"candidate_sha": candidate, "candidate_tree_sha": candidate_tree}
    path = tmp_path / "preflight.json"
    path.write_text(json.dumps(record), encoding="utf-8")

    monkeypatch.setattr(freeze, "PREFLIGHT_PATH", path)
    monkeypatch.setattr(freeze, "git_path_exists", lambda path, revision="HEAD": True)
    monkeypatch.setattr(
        freeze.preflight,
        "prepare",
        lambda sha: pytest.fail("accepted predecessor validation re-applied the preflight creation gate"),
    )
    monkeypatch.setattr(
        freeze.preflight,
        "expected_record_for_candidate",
        lambda sha: record,
        raising=False,
    )
    monkeypatch.setattr(freeze.preflight, "validate_record", lambda actual, expected: None)
    monkeypatch.setattr(
        freeze,
        "git",
        lambda *args: candidate_tree if args == ("rev-parse", f"{candidate}^{{tree}}") else "c" * 40,
    )
    monkeypatch.setattr(freeze, "git_history", lambda path, revision="HEAD": ("d" * 40,))
    monkeypatch.setattr(freeze, "is_ancestor", lambda ancestor, descendant: True)
    monkeypatch.setattr(freeze, "git_blob", lambda path, revision: "e" * 40)

    actual_record, actual_candidate, actual_tree, preflight_blob = freeze.require_valid_preflight()
    assert actual_record == record
    assert actual_candidate == candidate
    assert actual_tree == candidate_tree
    assert preflight_blob == "e" * 40


def test_prepare_fails_closed_while_preflight_absent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    original_git_path_exists = freeze.git_path_exists
    monkeypatch.setattr(freeze, "PREFLIGHT_PATH", tmp_path / "missing-preflight.json")
    monkeypatch.setattr(freeze, "FREEZE_PATH", tmp_path / "missing-freeze.json")
    monkeypatch.setattr(freeze, "DOWNSTREAM_REL", ())
    monkeypatch.setattr(
        freeze,
        "git_path_exists",
        lambda path, revision="HEAD": (
            False if path == freeze.FREEZE_REL else original_git_path_exists(path, revision)
        ),
    )
    with pytest.raises(SystemExit, match="canonical preflight record is absent"):
        freeze.prepare()


def test_boundary_proves_freeze_absent_when_freeze_absent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    original_git_path_exists = freeze.git_path_exists
    monkeypatch.setattr(freeze, "FREEZE_PATH", tmp_path / "missing-freeze.json")
    monkeypatch.setattr(freeze, "DOWNSTREAM_REL", ())
    monkeypatch.setattr(
        freeze,
        "git_path_exists",
        lambda path, revision="HEAD": (
            False if path == freeze.FREEZE_REL else original_git_path_exists(path, revision)
        ),
    )
    freeze.validate_boundary()
    output = capsys.readouterr().out
    assert "TRACK_A_EPOCH_002_FREEZE_TOOLING=PASS_FREEZE_ABSENT" in output
    assert "TRACK_A_FREEZE=NOT_ESTABLISHED" in output
    assert "SUCCESSOR_COLLECTION_AUTHORIZED=FALSE" in output
    assert "SCIENTIFIC_N_INCREMENT=0" in output


def test_helper_has_no_secret_input_surface() -> None:
    text = (ROOT / "scripts/prepare_track_a_epoch_002_immutable_freeze.py").read_text(encoding="utf-8")
    assert "--passphrase" not in text
    assert "PDMAL_BLINDING_KEY" not in text
    assert "genpkey" not in text
    assert "private_key_encrypted" not in text


def test_current_runner_contract_remains_non_authorizing() -> None:
    contract = freeze.validate_non_authorizing_contract()
    assert contract["track_a_freeze"] == "NOT_ESTABLISHED"
    assert contract["successor_collection"] == "NOT_AUTHORIZED"
    assert contract["primary_analysis"] == "NOT_AUTHORIZED"
    assert contract["scientific_n_increment"] == 0
