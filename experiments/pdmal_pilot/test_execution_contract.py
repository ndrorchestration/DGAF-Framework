import pytest

from deviations import DeviationRegister
from run_pilot import main
from sample_size import required_n


def test_runner_requires_explicit_mode(monkeypatch):
    monkeypatch.delenv("PDMAL_MODE", raising=False)
    with pytest.raises(SystemExit, match="PDMAL_MODE"):
        main(["--seeds", "2"])


def test_contract_mode_is_fixed_to_two_validation_seeds(monkeypatch):
    monkeypatch.setenv("PDMAL_MODE", "contract")
    with pytest.raises(SystemExit, match="fixed at 2"):
        main(["--seeds", "50"])


def test_contract_mode_never_authorizes_pilot(monkeypatch, capsys, tmp_path):
    monkeypatch.setenv("PDMAL_MODE", "contract")
    assert main(["--seeds", "2", "--output-dir", str(tmp_path)]) == 0
    assert "no empirical data collection performed" in capsys.readouterr().out


def test_pilot_mode_fails_closed_without_freeze_and_authorization(monkeypatch):
    monkeypatch.setenv("PDMAL_MODE", "pilot")
    monkeypatch.delenv("PDMAL_PROTOCOL_FROZEN", raising=False)
    monkeypatch.delenv("PDMAL_PILOT_AUTHORIZED", raising=False)
    with pytest.raises(SystemExit, match="PDMAL_PROTOCOL_FROZEN"):
        main(["--seeds", "50"])


def test_pilot_mode_requires_exact_frozen_sha_before_executor(monkeypatch):
    monkeypatch.setenv("PDMAL_MODE", "pilot")
    monkeypatch.setenv("PDMAL_PROTOCOL_FROZEN", "1")
    monkeypatch.setenv("PDMAL_PILOT_AUTHORIZED", "1")
    monkeypatch.setenv("PDMAL_FROZEN_COMMIT_SHA", "0" * 40)
    with pytest.raises(SystemExit, match="frozen SHA mismatch"):
        main(["--seeds", "50"])


def test_pilot_executor_path_is_present():
    import run_pilot

    assert hasattr(run_pilot, "ConsensusTask")
    assert run_pilot.ConsensusTask.__name__ == "ConsensusTask"


def test_sample_size_reference_case():
    assert required_n(0.15) == 8


def test_sample_size_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        required_n(0)
    with pytest.raises(ValueError):
        required_n(0.1, alpha=1.0)


def test_deviation_register_records_and_serializes(tmp_path):
    register = DeviationRegister()
    register.record(
        "DEV-001",
        seed_id="seed_001",
        trial_id="trial_001",
        condition="blind_abc",
        cause="test_fixture",
        description="synthetic contract deviation",
        affected_metrics=("runtime",),
        comparability_impact="none",
        include_exclude_decision="include",
        authorization="test",
    )
    assert len(register) == 1
    path = tmp_path / "deviations.json"
    register.write_json(path)
    assert "DEV-001" in path.read_text(encoding="utf-8")
