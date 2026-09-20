from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate_aoss_v0_6_stage_a_collection_authorization.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("aoss_stage_a_auth_test", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_repository_state_matches_current_authorization_phase() -> None:
    validator = load_validator()
    validator.validate_repository_state()


def test_expected_authorization_is_exact_and_bounded() -> None:
    validator = load_validator()
    record = validator.expected_authorization()
    validator.validate_authorization(record)
    assert record["outcome_collection_authorized"] is True
    assert record["external_validation_established"] is False
    assert record["scientific_n_increment"] == 0
    assert record["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert record["high_assurance"] == "NOT_AUTHORIZED"
    assert record["scope"]["episode_classes"] == 16
    assert record["scope"]["exact_byte_replay_passes_per_episode"] == 5


def test_authorization_cannot_widen_to_high_assurance() -> None:
    validator = load_validator()
    broken = copy.deepcopy(validator.expected_authorization())
    broken["high_assurance"] = "AUTHORIZED"
    with pytest.raises(SystemExit, match="schema"):
        validator.validate_authorization(broken)


def test_authorization_cannot_establish_external_validation() -> None:
    validator = load_validator()
    broken = copy.deepcopy(validator.expected_authorization())
    broken["external_validation_established"] = True
    with pytest.raises(SystemExit, match="schema"):
        validator.validate_authorization(broken)


def test_authorization_cannot_change_acp_commit() -> None:
    validator = load_validator()
    broken = copy.deepcopy(validator.expected_authorization())
    broken["source_system"]["commit"] = "0" * 40
    with pytest.raises(SystemExit, match="schema"):
        validator.validate_authorization(broken)


def test_authorization_preserves_track_a_epoch_002_boundary() -> None:
    validator = load_validator()
    assert "DOES_NOT_REOPEN_OR_POOL_TRACK_A_EPOCH_002" in validator.expected_authorization()["non_effects"]


def test_precollection_receipt_binds_all_frozen_contracts(monkeypatch) -> None:
    validator = load_validator()
    auth_ref = validator.SOURCE_BASIS
    original_load_json_at_ref = validator.load_json_at_ref
    original_git = validator.git

    def fake_load_json_at_ref(ref, relpath):
        if relpath == validator.AUTH_REL:
            return validator.expected_authorization()
        return original_load_json_at_ref(ref, relpath)

    def fake_git(*args):
        if args[:1] == ("rev-parse",) and len(args) == 2 and args[1] == auth_ref:
            return auth_ref
        if args[:1] == ("rev-parse",) and len(args) == 2 and args[1] == f"{auth_ref}:{validator.AUTH_REL}":
            return "a" * 40
        return original_git(*args)

    monkeypatch.setattr(validator, "load_json_at_ref", fake_load_json_at_ref)
    monkeypatch.setattr(validator, "git", fake_git)
    receipt = validator.expected_precollection_receipt(auth_ref)
    assert set(receipt["frozen_contract_blobs"]) == set(validator.CONTRACT_PATHS)
    assert receipt["outcomes_generated_before_receipt"] is False
    assert receipt["scientific_n_increment"] == 0
