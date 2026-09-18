from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts/run_track_a_epoch_002_locked_primary_analysis.py"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "track_a_epoch_002_locked_primary_analysis_runner",
        RUNNER_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_runner_is_local_fail_closed_and_nonpromoting() -> None:
    runner = load_runner()
    source = RUNNER_PATH.read_text(encoding="utf-8")

    assert runner.ANALYSIS_BLOB_SHA == "d4495f7cdf211b974039ec0e66292dc62ea0881f"
    assert runner.ANALYSIS_CONFIG_SHA256 == "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
    assert runner.REQUIREMENTS_BLOB_SHA == "00c1f779e97030f9b25ae494642edb31b5b09de5"
    assert "canonical_dgaf_efficacy" in source
    assert "NOT_ESTABLISHED" in source
    assert "NOT_AUTHORIZED_N0" in source
    assert "requests." not in source
    assert "urllib" not in source


def test_locked_environment_requires_exact_versions(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = load_runner()
    monkeypatch.setattr(
        runner,
        "load_repo_object",
        lambda relpath: {
            "protocol_id": runner.PROTOCOL_ID,
            "status": "ANALYSIS_IMPLEMENTATION_LOCKED_NONEMPIRICAL",
            "environment": {"python_version": "3.12.0"},
            "numpy_version": "2.5.1",
        },
    )
    monkeypatch.setattr(runner.platform, "python_version", lambda: "3.12.0")
    monkeypatch.setattr(runner.np, "__version__", "2.5.1")

    assert runner.validate_locked_environment() == {
        "python": "3.12.0",
        "numpy": "2.5.1",
    }

    monkeypatch.setattr(runner.platform, "python_version", lambda: "3.12.3")
    with pytest.raises(SystemExit, match="Python version mismatch"):
        runner.validate_locked_environment()


def test_materialized_input_must_match_accepted_digest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = load_runner()
    source = tmp_path / "input.json"
    document = {
        "record_type": "TRACK_A_EPOCH_002_UNBLINDED_ANALYSIS_INPUT",
        "schema_version": 1,
        "protocol_id": runner.PROTOCOL_ID,
        "paired_seed_units": 50,
        "record_count": 2250,
        "records": [{} for _ in range(2250)],
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "outcome_aggregation_performed": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "primary_analysis_status": "NOT_AUTHORIZED_NOT_RUN",
    }
    source.write_bytes(runner.canonical_json_bytes(document))
    digest = runner.sha256_bytes(source.read_bytes())
    monkeypatch.setattr(
        runner,
        "load_repo_object",
        lambda relpath: {"materialized_input_sha256": digest},
    )

    records, observed = runner.validate_materialized_input(source)
    assert len(records) == 2250
    assert observed == digest

    monkeypatch.setattr(
        runner,
        "load_repo_object",
        lambda relpath: {"materialized_input_sha256": "0" * 64},
    )
    with pytest.raises(SystemExit, match="digest does not match accepted evidence"):
        runner.validate_materialized_input(source)


def test_execute_writes_only_local_content_addressed_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = load_runner()
    input_path = tmp_path / "input.json"
    input_path.write_text("{}", encoding="utf-8")
    output_dir = tmp_path / "out"

    monkeypatch.setattr(
        runner,
        "validate_authorization",
        lambda: (
            "a" * 40,
            {"record_id": "E002-ANALYSIS-AUTH-0001"},
        ),
    )
    monkeypatch.setattr(
        runner,
        "validate_locked_environment",
        lambda: {"python": "3.12.0", "numpy": "2.5.1"},
    )
    monkeypatch.setattr(
        runner,
        "validate_materialized_input",
        lambda path: ([], "b" * 64),
    )
    monkeypatch.setattr(
        runner,
        "load_module",
        lambda path, name: SimpleNamespace(
            analyze=lambda records: {
                "protocol_id": runner.PROTOCOL_ID,
                "classification": "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED",
                "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
                "high_assurance": "NOT_AUTHORIZED_N0",
            }
        ),
    )

    destination, digest = runner.execute(input_path, output_dir)

    assert destination == output_dir / runner.OUTPUT_NAME
    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload["authorization_event_commit_sha"] == "a" * 40
    assert payload["materialized_input_sha256"] == "b" * 64
    assert payload["scientific_n_increment"] == 0
    assert payload["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert payload["independent_validation"] == "NOT_ESTABLISHED"
    assert payload["high_assurance"] == "NOT_AUTHORIZED_N0"
    assert (output_dir / runner.OUTPUT_SIDECAR_NAME).read_text(encoding="ascii") == (
        f"{digest}  {runner.OUTPUT_NAME}\n"
    )

    with pytest.raises(SystemExit, match="refusing to overwrite"):
        runner.execute(input_path, output_dir)


def test_preflight_never_reads_or_executes_analysis_input(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = load_runner()
    calls: list[str] = []

    def fake_authorization() -> tuple[str, dict[str, object]]:
        calls.append("authorization")
        return "a" * 40, {}

    def fake_environment() -> dict[str, str]:
        calls.append("environment")
        return {}

    def fake_frozen(ref: str = "HEAD") -> None:
        calls.append(f"frozen:{ref}")

    monkeypatch.setattr(runner, "validate_authorization", fake_authorization)
    monkeypatch.setattr(runner, "validate_locked_environment", fake_environment)
    monkeypatch.setattr(runner, "validate_frozen_identities", fake_frozen)
    monkeypatch.setattr(
        runner,
        "validate_materialized_input",
        lambda path: pytest.fail("preflight must not read materialized input"),
    )

    runner.preflight()

    assert calls == ["authorization", "environment", "frozen:HEAD"]
