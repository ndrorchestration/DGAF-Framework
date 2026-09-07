"""Fail-closed tests for the developer-run Solo Pilot track."""
from __future__ import annotations

import os

import pytest

from run_pilot import (
    HIGH_ASSURANCE_EXPERIMENT_ID,
    SOLO_EXPERIMENT_ID,
    require_mode,
    require_solo_pilot_authorization,
    validate_solo_epoch_authority,
)


def _authorized_record(*, epoch_id: str, frozen_sha: str) -> dict:
    return {
        "schema_version": 1,
        "record_type": "DGAF_PDMAL_SOLO_EPOCH_AUTHORITY",
        "protocol_version": "0.7.6",
        "status": "AUTHORIZED",
        "epoch_id": epoch_id,
        "frozen_commit_sha": frozen_sha,
        "authorization": {
            "type": "REPOSITORY_BOUND_EPOCH_AUTHORIZATION",
            "decision": "GRANTED",
            "authority_issue": 369,
            "legacy_self_authorization_sufficient": False,
        },
        "historical_experiment_001_authority_reusable": False,
        "legacy_environment_only_authorization_permitted": False,
    }


def _configure_legacy_solo_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PROTOCOL_FROZEN", "1")
    monkeypatch.setenv("PDMAL_SOLO_PILOT_AUTHORIZED", "1")
    monkeypatch.setenv("PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED", "1")
    monkeypatch.setenv("PDMAL_SOLO_EPOCH_ID", "SOLO-EPOCH-003")
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
        require_solo_pilot_authorization("a" * 40)


def test_repository_authority_accepts_only_exact_epoch_and_sha() -> None:
    sha = "a" * 40
    epoch = "SOLO-P30-EMPIRICAL-EPOCH-003"
    record = _authorized_record(epoch_id=epoch, frozen_sha=sha)
    assert validate_solo_epoch_authority(record, frozen_sha=sha, requested_epoch_id=epoch) == epoch


def test_repository_authority_rejects_epoch_mismatch() -> None:
    sha = "a" * 40
    record = _authorized_record(epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003", frozen_sha=sha)
    with pytest.raises(SystemExit, match="PDMAL_SOLO_EPOCH_ID does not match"):
        validate_solo_epoch_authority(record, frozen_sha=sha, requested_epoch_id="OTHER-EPOCH")


def test_repository_authority_rejects_frozen_sha_mismatch() -> None:
    record = _authorized_record(epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003", frozen_sha="a" * 40)
    with pytest.raises(SystemExit, match="not bound to this frozen commit"):
        validate_solo_epoch_authority(
            record,
            frozen_sha="b" * 40,
            requested_epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003",
        )


def test_repository_authority_rejects_legacy_self_authorization_semantics() -> None:
    sha = "a" * 40
    record = _authorized_record(epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003", frozen_sha=sha)
    record["authorization"]["legacy_self_authorization_sufficient"] = True
    with pytest.raises(SystemExit, match="legacy environment self-authorization must remain insufficient"):
        validate_solo_epoch_authority(
            record,
            frozen_sha=sha,
            requested_epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003",
        )


def test_repository_authority_rejects_historical_authority_reuse() -> None:
    sha = "a" * 40
    record = _authorized_record(epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003", frozen_sha=sha)
    record["historical_experiment_001_authority_reusable"] = True
    with pytest.raises(SystemExit, match="historical experiment-001 authority must not be reusable"):
        validate_solo_epoch_authority(
            record,
            frozen_sha=sha,
            requested_epoch_id="SOLO-P30-EMPIRICAL-EPOCH-003",
        )


def test_high_assurance_authorization_is_not_implied_by_solo_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_legacy_solo_env(monkeypatch)
    assert os.getenv("PDMAL_PILOT_AUTHORIZED") is None
