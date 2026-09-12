from __future__ import annotations

import ast
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

import pytest

from scripts import validate_track_a_epoch_002_collection_authorization as authorization

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "experiments/pdmal_pilot/run_track_a_epoch_002.py"
CONTRACT = json.loads((ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json").read_text(encoding="utf-8"))

SAMPLE_CUSTODY = {
    "custody_receipt_blob_sha": "1" * 40,
    "custody_certificate_blob_sha": "2" * 40,
    "custody_encrypted_private_key_sha256": "3" * 64,
    "custody_certificate_sha256": "4" * 64,
    "custody_certificate_public_key_der_sha256": "5" * 64,
}


def load_runner_expected_authorization() -> Callable[..., dict[str, Any]]:
    tree = ast.parse(RUNNER_PATH.read_text(encoding="utf-8"), filename=str(RUNNER_PATH))
    functions: list[ast.stmt] = [
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "expected_authorization"
    ]
    assert len(functions) == 1
    module = ast.Module(body=functions, type_ignores=[])
    ast.fix_missing_locations(module)
    bindings = CONTRACT["source_bindings"]
    matrix = CONTRACT["matrix"]
    namespace: dict[str, Any] = {
        "PROTOCOL_ID": CONTRACT["protocol_id"],
        "EPOCH_ID": CONTRACT["epoch_id"],
        "PREREG_MERGE_SHA": bindings["preregistration_merge_sha"],
        "ANALYSIS_LOCK_MERGE_SHA": bindings["analysis_lock_merge_sha"],
        "ANALYSIS_BLOB_SHA": bindings["analysis_blob_sha"],
        "ANALYSIS_CONFIG_SHA256": bindings["analysis_config_sha256"],
        "REQUIREMENTS_LOCK_BLOB_SHA": bindings["requirements_lock_blob_sha"],
        "ALGORITHM_ID": CONTRACT["algorithm_id"],
        "SEEDS": tuple(matrix["seeds"]),
        "EXPECTED_TOTAL": matrix["expected_total_observations"],
    }
    exec(compile(module, str(RUNNER_PATH), "exec"), namespace)
    function = namespace["expected_authorization"]
    assert callable(function)
    return function


def sample_record() -> dict[str, Any]:
    return authorization.expected_record(
        CONTRACT,
        authorization_parent_sha="a" * 40,
        candidate_sha="b" * 40,
        candidate_tree_sha="c" * 40,
        preflight_blob_sha="d" * 40,
        freeze_blob_sha="e" * 40,
        closure_blob_sha="f" * 40,
        verification_blob_sha="0" * 40,
        custody=SAMPLE_CUSTODY,
    )


def test_expected_record_matches_runner_contract_exactly() -> None:
    runner_expected = load_runner_expected_authorization()
    helper_record = sample_record()
    runner_record = runner_expected(
        authorization_parent_sha="a" * 40,
        candidate_sha="b" * 40,
        candidate_tree_sha="c" * 40,
        preflight_blob_sha="d" * 40,
        freeze_blob_sha="e" * 40,
        closure_blob_sha="f" * 40,
        verification_blob_sha="0" * 40,
        custody=SAMPLE_CUSTODY,
    )
    assert helper_record == runner_record


def test_expected_record_authorizes_collection_only() -> None:
    record = sample_record()
    assert record["authorize_empirical_collection"] is True
    assert record["authorize_unblinding"] is False
    assert record["authorize_primary_analysis"] is False
    assert record["historical_pooling_allowed"] is False
    assert record["epoch_004_substitution_allowed"] is False
    assert record["high_assurance_authorized"] is False
    assert record["custody_class"] == "SAME_SYSTEM_NONINDEPENDENT"
    assert record["custody_recovery_drill"] == "PASS"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("authorize_empirical_collection", False),
        ("authorize_unblinding", True),
        ("authorize_primary_analysis", True),
        ("historical_pooling_allowed", True),
        ("epoch_004_substitution_allowed", True),
        ("high_assurance_authorized", True),
        ("custody_class", "INDEPENDENT"),
        ("custody_recovery_drill", "NOT_RUN"),
    ],
)
def test_validate_record_rejects_scope_or_authority_mutation(field: str, value: object) -> None:
    expected = sample_record()
    changed = deepcopy(expected)
    changed[field] = value
    with pytest.raises(SystemExit, match="authorization record mismatch"):
        authorization.validate_record(changed, expected)


def test_validate_record_rejects_extra_authority_field() -> None:
    expected = sample_record()
    changed = deepcopy(expected)
    changed["authorize_high_assurance"] = True
    with pytest.raises(SystemExit, match="authorization record mismatch"):
        authorization.validate_record(changed, expected)


def test_contract_preserves_human_control_and_pr_non_authority() -> None:
    contract = authorization.validate_contract()
    assert contract["authorization"]["pr_validation_can_authorize"] is False
    reconciler = authorization.load_object(authorization.RECONCILER_PATH, "reconciler")
    node = authorization.find_reconciler_node(reconciler, "collection_authorization")
    assert node is not None
    assert node["action_class"] == "human_controlled"


def isolate_authorization_absence(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Mask only authorization-event presence while preserving every other real path check."""
    original_git_path_exists = authorization.git_path_exists
    monkeypatch.setattr(authorization, "AUTH_PATH", tmp_path / "missing-authorization.json")
    monkeypatch.setattr(
        authorization,
        "git_path_exists",
        lambda path, revision="HEAD": (
            False if path == authorization.AUTH_REL else original_git_path_exists(path, revision)
        ),
    )


def test_boundary_proves_authorization_absent_when_authorization_absent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    isolate_authorization_absence(monkeypatch, tmp_path)
    authorization.validate_boundary()
    output = capsys.readouterr().out
    assert "TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION_TOOLING=PASS_AUTHORIZATION_ABSENT" in output
    assert "ACTION_CLASS=HUMAN_CONTROLLED" in output
    assert "PR_VALIDATION_CAN_AUTHORIZE=FALSE" in output
    assert "SUCCESSOR_COLLECTION_AUTHORIZED=FALSE" in output
    assert "EMPIRICAL_EXECUTION_PERFORMED=FALSE" in output
    assert "SCIENTIFIC_N_INCREMENT=0" in output


def test_tool_has_no_authorization_write_or_execution_surface() -> None:
    text = (ROOT / "scripts/validate_track_a_epoch_002_collection_authorization.py").read_text(encoding="utf-8")
    assert "--write" not in text
    assert "write_text(" not in text
    assert "--execute" not in text
    assert "PDMAL_TRACK_A_EPOCH_002_AUTHORIZED" not in text
    assert "PDMAL_TOPOLOGY_BLINDING_KEY" not in text


def test_current_contract_stays_not_authorized() -> None:
    contract = authorization.validate_contract()
    assert contract["successor_collection"] == "NOT_AUTHORIZED"
    assert contract["primary_analysis"] == "NOT_AUTHORIZED"
    assert contract["scientific_n_increment"] == 0
    assert contract["authorization"]["collection_authorized"] is False
