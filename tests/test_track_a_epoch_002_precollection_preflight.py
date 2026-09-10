from __future__ import annotations

import ast
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

import pytest

from scripts import prepare_track_a_epoch_002_precollection_preflight as preflight

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json").read_text(encoding="utf-8"))
RUNNER_PATH = ROOT / "experiments/pdmal_pilot/run_track_a_epoch_002.py"


def load_runner_expected_preflight() -> Callable[..., dict[str, Any]]:
    """Load only the runner's pure preflight constructor, without runtime deps."""
    tree = ast.parse(RUNNER_PATH.read_text(encoding="utf-8"), filename=str(RUNNER_PATH))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "expected_preflight"]
    assert len(functions) == 1

    module = ast.Module(body=functions, type_ignores=[])
    ast.fix_missing_locations(module)
    bindings = CONTRACT["source_bindings"]
    matrix = CONTRACT["matrix"]
    namespace: dict[str, Any] = {
        "PROTOCOL_ID": CONTRACT["protocol_id"],
        "PREREG_MERGE_SHA": bindings["preregistration_merge_sha"],
        "ANALYSIS_LOCK_MERGE_SHA": bindings["analysis_lock_merge_sha"],
        "ANALYSIS_BLOB_SHA": bindings["analysis_blob_sha"],
        "ANALYSIS_CONFIG_SHA256": bindings["analysis_config_sha256"],
        "REQUIREMENTS_LOCK_BLOB_SHA": bindings["requirements_lock_blob_sha"],
        "ALGORITHM_ID": CONTRACT["algorithm_id"],
        "EXPECTED_CELLS_PER_SEED": matrix["cells_per_seed"],
        "EXPECTED_TOTAL": matrix["expected_total_observations"],
    }
    exec(compile(module, str(RUNNER_PATH), "exec"), namespace)
    function = namespace["expected_preflight"]
    assert callable(function)
    return function


def custody_fixture() -> dict[str, str]:
    return {
        "custody_receipt_blob_sha": "1" * 40,
        "custody_certificate_blob_sha": "2" * 40,
        "custody_encrypted_private_key_sha256": "3" * 64,
        "custody_certificate_sha256": "4" * 64,
        "custody_certificate_public_key_der_sha256": "5" * 64,
    }


def test_helper_expected_record_matches_collection_runner_contract() -> None:
    runner_expected_preflight = load_runner_expected_preflight()
    candidate_sha = "a" * 40
    candidate_tree = "b" * 40
    custody = custody_fixture()

    helper_record = preflight.expected_record(
        CONTRACT,
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        custody=custody,
    )
    runner_record = runner_expected_preflight(
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        custody=custody,
    )

    assert helper_record == runner_record


def test_expected_record_is_explicitly_non_authorizing() -> None:
    record = preflight.expected_record(
        CONTRACT,
        candidate_sha="a" * 40,
        candidate_tree_sha="b" * 40,
        custody=custody_fixture(),
    )

    assert record["preflight_status"] == "PASS"
    assert record["custody_class"] == "SAME_SYSTEM_NONINDEPENDENT"
    assert record["custody_recovery_drill"] == "PASS"
    assert record["collection_authorized"] is False
    assert record["unblinding_authorized"] is False
    assert record["primary_analysis_authorized"] is False
    assert record["high_assurance_authorized"] is False
    assert record["scientific_n_increment"] == 0


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("track_a_freeze",), "ESTABLISHED"),
        (("successor_collection",), "AUTHORIZED"),
        (("primary_analysis",), "AUTHORIZED"),
        (("scientific_n_increment",), 1),
        (("authorization", "pr_validation_can_authorize"), True),
        (("authorization", "collection_authorized"), True),
        (("authorization", "unblinding_authorized"), True),
        (("authorization", "primary_analysis_authorized"), True),
        (("authorization", "high_assurance_authorized"), True),
    ],
)
def test_contract_boundary_rejects_authority_promotion(path: tuple[str, ...], value: object) -> None:
    contract = deepcopy(CONTRACT)
    target = contract
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value

    with pytest.raises(SystemExit, match="EPOCH_002_PREFLIGHT_FAIL"):
        preflight.validate_contract_boundary(contract)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("receipt_schema_version_required", 1),
        ("legacy_receipt_authorizes_successor_collection", True),
        ("each_recorded_backup_recovery_must_pass", False),
        ("distinct_backup_storage_classes_required", False),
        ("custody_class_required", "INDEPENDENT"),
        ("independent_custody_required", True),
        ("minimum_distinct_encrypted_user_controlled_backups", 1),
        ("custody_receipt_authorizes_collection", True),
    ],
)
def test_contract_boundary_rejects_custody_weakening(field: str, value: object) -> None:
    contract = deepcopy(CONTRACT)
    contract["custody_precondition"][field] = value

    with pytest.raises(SystemExit, match="EPOCH_002_PREFLIGHT_FAIL"):
        preflight.validate_contract_boundary(contract)


def test_validate_record_rejects_extra_or_changed_fields() -> None:
    expected = preflight.expected_record(
        CONTRACT,
        candidate_sha="a" * 40,
        candidate_tree_sha="b" * 40,
        custody=custody_fixture(),
    )

    extra = deepcopy(expected)
    extra["authorization"] = True
    with pytest.raises(SystemExit, match="record mismatch"):
        preflight.validate_record(extra, expected)

    changed = deepcopy(expected)
    changed["collection_authorized"] = True
    with pytest.raises(SystemExit, match="record mismatch"):
        preflight.validate_record(changed, expected)


def test_helper_has_no_secret_input_surface() -> None:
    text = (ROOT / "scripts/prepare_track_a_epoch_002_precollection_preflight.py").read_text(encoding="utf-8")

    assert "--passphrase" not in text
    assert "PDMAL_BLINDING_KEY" not in text
    assert "genpkey" not in text
    assert "pkcs8" not in text.lower()
    assert preflight.RECEIPT_REL.endswith("TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json")
    assert preflight.CERT_REL.endswith("TRACK_A_SUCCESSOR_CUSTODY_CERT.pem")


def test_current_contract_remains_non_authorizing() -> None:
    preflight.validate_contract_boundary(CONTRACT)
