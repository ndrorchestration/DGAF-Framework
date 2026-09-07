"""Fail-closed tests for the developer-run Solo Pilot track."""
from __future__ import annotations

import os

import pytest

from run_pilot import (
    HIGH_ASSURANCE_EXPERIMENT_ID,
    SOLO_AUTHORITY_RELATIVE_PATH,
    SOLO_EXPERIMENT_ID,
    require_mode,
    require_solo_pilot_authorization,
    validate_solo_authorization_envelope,
    validate_solo_epoch_authority,
)


def _authorized_record(*, epoch_id: str, apparatus_sha: str) -> dict:
    return {
        "schema_version": 2,
        "record_type": "DGAF_PDMAL_SOLO_EPOCH_AUTHORITY",
        "protocol_version": "0.7.6",
        "status": "AUTHORIZED",
        "epoch_id": epoch_id,
        "apparatus_commit_sha": apparatus_sha,
        "authorization": {
            "type": "REPOSITORY_BOUND_EPOCH_AUTHORIZATION_ENVELOPE",
            "decision": "GRANTED",
            "authority_issue": 369,
            "legacy_self_authorization_sufficient": False,
        },
        "authorization_envelope_contract": {
            "must_be_direct_child_of_apparatus_commit": True,
            "only_changed_path": SOLO_AUTHORITY_RELATIVE_PATH,
            "apparatus_code_executes_from_envelope_without_other_file_changes": True,
            "reason": "A commit cannot contain its own SHA without circular identity. The authorization envelope therefore names its direct-parent apparatus commit and may change only this authority record.",
        },
        "historical_experiment_001_authority_reusable": False,
        "legacy_environment_only_authorization_permitted": False,
    }


def _configure_legacy_solo_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PROTOCOL_FROZEN", "1")
    monkeypatch.setenv("PDMAL_SOLO_PILOT_AUTHORIZED", "1")
    monkeypatch.setenv("PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED", "1")
    monkeypatch.setenv("PDMAL_SOLO_EPOCH_ID", "SOLO-EPOCH-003")
    monkeypatch.setenv("PDMAL_FROZEN_COMMIT_SHA", "a" * 40)
    monkeypatch.setenv("PDMAL_BLINDING_KEY", "solo-test-blinding-key-0000000000000000")
    monkeypatch.delenv("PDMAL_PILOT_AUTHORIZED", raising=False)


def test_solo_mode_is_explicit_and_distinct(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_MODE", "solo_pilot")
    assert require_mode() == "solo_pilot"
    assert SOLO_EXPERIMENT_ID == "PDMAL-SOLO-PILOT-V1"
    assert HIGH_ASSURANCE_EXPERIMENT_ID == "PDMAL-PILOT-V1"
    assert SOLO_EXPERIMENT_ID != HIGH_ASSURANCE_EXPERIMENT_ID


def test_legacy_environment_variables_cannot_authorize_current_epoch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_legacy_solo_env(monkeypatch)
    with pytest.raises(SystemExit, match="repository epoch authority status is 'NOT_AUTHORIZED'"):
        require_solo_pilot_authorization()


def test_repository_authority_accepts_exact_epoch_and_apparatus_sha() -> None:
    sha = "a" * 40
    epoch = "SOLO-P30-EMPIRICAL-EPOCH-003"
    record = _authorized_record(epoch_id=epoch, apparatus_sha=sha)
    assert validate_solo_epoch_authority(record, apparatus_sha=sha, requested_epoch_id=epoch) == epoch


def test_repository_authority_rejects_epoch_mismatch() -> None:
    sha = "a" * 40
    record = _authorized_record(epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003", apparatus_sha=sha)
    with pytest.raises(SystemExit, match="PDMAL_SOLO_EPOCH_ID does not match"):
        validate_solo_epoch_authority(record, apparatus_sha=sha, requested_epoch_id="OTHER-EPOCH")


def test_repository_authority_rejects_apparatus_sha_mismatch() -> None:
    record = _authorized_record(epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003", apparatus_sha="a" * 40)
    with pytest.raises(SystemExit, match="not bound to the requested apparatus commit"):
        validate_solo_epoch_authority(
            record,
            apparatus_sha="b" * 40,
            requested_epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003",
        )


def test_repository_authority_rejects_legacy_self_authorization_semantics() -> None:
    sha = "a" * 40
    record = _authorized_record(epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003", apparatus_sha=sha)
    record["authorization"]["legacy_self_authorization_sufficient"] = True
    with pytest.raises(SystemExit, match="legacy environment self-authorization must remain insufficient"):
        validate_solo_epoch_authority(
            record,
            apparatus_sha=sha,
            requested_epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003",
        )


def test_repository_authority_rejects_historical_authority_reuse() -> None:
    sha = "a" * 40
    record = _authorized_record(epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003", apparatus_sha=sha)
    record["historical_experiment_001_authority_reusable"] = True
    with pytest.raises(SystemExit, match="historical experiment-001 authority must not be reusable"):
        validate_solo_epoch_authority(
            record,
            apparatus_sha=sha,
            requested_epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003",
        )


def test_authorization_envelope_accepts_direct_child_one_file_change() -> None:
    validate_solo_authorization_envelope(
        apparatus_sha="a" * 40,
        envelope_sha="b" * 40,
        parent_shas=["a" * 40],
        changed_paths=[SOLO_AUTHORITY_RELATIVE_PATH],
    )


def test_authorization_envelope_rejects_non_direct_parent() -> None:
    with pytest.raises(SystemExit, match="direct single-parent child"):
        validate_solo_authorization_envelope(
            apparatus_sha="a" * 40,
            envelope_sha="c" * 40,
            parent_shas=["b" * 40],
            changed_paths=[SOLO_AUTHORITY_RELATIVE_PATH],
        )


def test_authorization_envelope_rejects_any_apparatus_change() -> None:
    with pytest.raises(SystemExit, match="may change only"):
        validate_solo_authorization_envelope(
            apparatus_sha="a" * 40,
            envelope_sha="b" * 40,
            parent_shas=["a" * 40],
            changed_paths=[SOLO_AUTHORITY_RELATIVE_PATH, "experiments/pdmal_pilot/run_pilot.py"],
        )


def test_high_assurance_authorization_is_not_implied_by_solo_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_legacy_solo_env(monkeypatch)
    assert os.getenv("PDMAL_PILOT_AUTHORIZED") is None
