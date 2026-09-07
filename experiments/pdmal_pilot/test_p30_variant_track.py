"""Fail-closed controls for the DGAF-P30-EXPLICIT-0.45 Solo variant."""
from __future__ import annotations

from pathlib import Path

import pytest

from p30_remediation_diagnostic import P30_BINDING_ID, P30_FIXTURE_CONFIDENCE
from run_p30_variant import (
    VARIANT_BINDING_KIND,
    VARIANT_EXPERIMENT_ID,
    VARIANT_MODE,
    VARIANT_OBSERVATIONS,
    VARIANT_SCOPE,
    VARIANT_SEEDS,
    VARIANT_SEED_START,
    _task_for,
    require_variant_authorization,
)


def _configure(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PDMAL_MODE", VARIANT_MODE)
    monkeypatch.setenv("PDMAL_PROTOCOL_FROZEN", "1")
    monkeypatch.setenv("PDMAL_SOLO_P30_VARIANT_AUTHORIZED", "1")
    monkeypatch.setenv("PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED", "1")
    monkeypatch.setenv("PDMAL_P30_BINDING_ID", P30_BINDING_ID)
    monkeypatch.setenv("PDMAL_P30_BINDING_KIND", VARIANT_BINDING_KIND)
    monkeypatch.setenv("PDMAL_P30_CONFIDENCE", "0.45")
    monkeypatch.setenv("PDMAL_BLINDING_KEY", "variant-test-blinding-key-00000000000000")
    monkeypatch.setenv("PDMAL_ARCHIVE_ROOT", str(tmp_path / "archive"))
    monkeypatch.delenv("PDMAL_PILOT_AUTHORIZED", raising=False)


def test_variant_identity_and_sample_are_fixed() -> None:
    assert VARIANT_MODE == "solo_p30_variant"
    assert VARIANT_EXPERIMENT_ID == "PDMAL-SOLO-P30-EXPLICIT-V1"
    assert VARIANT_SCOPE == "DGAF-P30-EXPLICIT-0.45"
    assert VARIANT_SEED_START == 20260901
    assert VARIANT_SEEDS == 50
    assert VARIANT_OBSERVATIONS == 9000
    assert P30_FIXTURE_CONFIDENCE == 0.45


def test_variant_authorization_accepts_exact_declared_binding(monkeypatch, tmp_path) -> None:
    _configure(monkeypatch, tmp_path)
    key, archive = require_variant_authorization()
    assert len(key) >= 32
    assert archive == (tmp_path / "archive").resolve()


@pytest.mark.parametrize(
    ("name", "value", "match"),
    [
        ("PDMAL_MODE", "solo_pilot", "PDMAL_MODE=solo_p30_variant"),
        ("PDMAL_SOLO_P30_VARIANT_AUTHORIZED", "0", "PDMAL_SOLO_P30_VARIANT_AUTHORIZED=1"),
        ("PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED", "0", "PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED=1"),
        ("PDMAL_P30_BINDING_ID", "OTHER", "PDMAL_P30_BINDING_ID"),
        ("PDMAL_P30_BINDING_KIND", "REAL_CALIBRATED", "PDMAL_P30_BINDING_KIND"),
        ("PDMAL_P30_CONFIDENCE", "0.46", "PDMAL_P30_CONFIDENCE"),
    ],
)
def test_variant_authorization_rejects_binding_drift(monkeypatch, tmp_path, name, value, match) -> None:
    _configure(monkeypatch, tmp_path)
    monkeypatch.setenv(name, value)
    with pytest.raises(SystemExit, match=match):
        require_variant_authorization()


def test_variant_rejects_high_assurance_claim(monkeypatch, tmp_path) -> None:
    _configure(monkeypatch, tmp_path)
    monkeypatch.setenv("PDMAL_PILOT_AUTHORIZED", "1")
    with pytest.raises(SystemExit, match="high-assurance authorization"):
        require_variant_authorization()


def test_dgaf_task_uses_explicit_fixture_and_control_does_not() -> None:
    dgaf = _task_for(topology="dodecahedral", failure_count=0, condition="dgaf")
    null = _task_for(topology="dodecahedral", failure_count=0, condition="null")
    assert dgaf.__class__.__name__ == "P30FixtureConsensusTask"
    assert null.__class__.__name__ == "ConsensusTask"
