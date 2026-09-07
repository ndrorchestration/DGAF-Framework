"""Fail-closed tests for the developer-run Solo Pilot track."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from run_pilot import (
    HIGH_ASSURANCE_EXPERIMENT_ID,
    SOLO_EXPERIMENT_ID,
    require_mode,
    require_solo_pilot_authorization,
)


def _configure_solo(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PDMAL_PROTOCOL_FROZEN", "1")
    monkeypatch.setenv("PDMAL_SOLO_PILOT_AUTHORIZED", "1")
    monkeypatch.setenv("PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED", "1")
    monkeypatch.setenv("PDMAL_BLINDING_KEY", "solo-test-blinding-key-0000000000000000")
    monkeypatch.setenv("PDMAL_ARCHIVE_ROOT", str(tmp_path / "archive"))
    monkeypatch.delenv("PDMAL_PILOT_AUTHORIZED", raising=False)


def test_solo_mode_is_explicit_and_distinct(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_MODE", "solo_pilot")
    assert require_mode() == "solo_pilot"
    assert SOLO_EXPERIMENT_ID == "PDMAL-SOLO-PILOT-V1"
    assert HIGH_ASSURANCE_EXPERIMENT_ID == "PDMAL-PILOT-V1"
    assert SOLO_EXPERIMENT_ID != HIGH_ASSURANCE_EXPERIMENT_ID


def test_solo_authorization_requires_limitations_acknowledgement(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _configure_solo(monkeypatch, tmp_path)
    monkeypatch.delenv("PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED")
    with pytest.raises(SystemExit, match="PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED=1"):
        require_solo_pilot_authorization()


def test_solo_authorization_rejects_high_assurance_authorization_claim(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _configure_solo(monkeypatch, tmp_path)
    monkeypatch.setenv("PDMAL_PILOT_AUTHORIZED", "1")
    with pytest.raises(SystemExit, match="high-assurance PDMAL_PILOT_AUTHORIZED must not be asserted"):
        require_solo_pilot_authorization()


def test_solo_authorization_retains_blinding_and_archive_controls(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _configure_solo(monkeypatch, tmp_path)
    key, archive = require_solo_pilot_authorization()
    assert len(key) >= 32
    assert archive == (tmp_path / "archive").resolve()
    assert archive.is_dir()


def test_solo_authorization_rejects_missing_self_authorization(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _configure_solo(monkeypatch, tmp_path)
    monkeypatch.delenv("PDMAL_SOLO_PILOT_AUTHORIZED")
    with pytest.raises(SystemExit, match="PDMAL_SOLO_PILOT_AUTHORIZED=1"):
        require_solo_pilot_authorization()


def test_standard_pilot_authorization_is_not_implied_by_solo_mode(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _configure_solo(monkeypatch, tmp_path)
    assert os.getenv("PDMAL_PILOT_AUTHORIZED") is None
