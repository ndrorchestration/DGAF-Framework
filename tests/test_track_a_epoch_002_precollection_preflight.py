from __future__ import annotations

import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from scripts import prepare_track_a_epoch_002_precollection_preflight as preflight

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads(
    (ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json").read_text(encoding="utf-8")
)
PDMAL = ROOT / "experiments/pdmal_pilot"


def load_runner():
    sys.path.insert(0, str(PDMAL))
    try:
        path = PDMAL / "run_track_a_epoch_002.py"
        spec = importlib.util.spec_from_file_location("track_a_epoch_002_runner_for_preflight_test", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(str(PDMAL))


def custody_fixture() -> dict[str, str]:
    return {
        "custody_receipt_blob_sha": "1" * 40,
        "custody_certificate_blob_sha": "2" * 40,
        "custody_encrypted_private_key_sha256": "3" * 64,
        "custody_certificate_sha256": "4" * 64,
        "custody_certificate_public_key_der_sha256": "5" * 64,
    }


def test_helper_expected_record_matches_collection_runner_contract() -> None:
    runner = load_runner()
    candidate_sha = "a" * 40
    candidate_tree = "b" * 40
    custody = custody_fixture()

    helper_record = preflight.expected_record(
        CONTRACT,
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        custody=custody,
    )
    runner_record = runner.expected_preflight(
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
