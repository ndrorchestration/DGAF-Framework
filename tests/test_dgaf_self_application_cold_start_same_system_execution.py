from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
HARNESS_SCRIPT = ROOT / "scripts" / "run_dgaf_self_application_cold_start_same_system_execution.py"
VALIDATOR_SCRIPT = ROOT / "scripts" / "validate_dgaf_self_application_cold_start_execution_record.py"
MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_same_system_execution_harness_writes_validator_admissible_retained_record(tmp_path: Path):
    harness = load_module("cold_start_same_system_execution", HARNESS_SCRIPT)
    validator = load_module("cold_start_execution_record_validator", VALIDATOR_SCRIPT)
    output_dir = tmp_path / "same-system-cold-start"

    summary = harness.run_same_system_execution(output_dir=output_dir, manifest_path=MANIFEST)

    record_path = output_dir / "cold_start_execution_record.json"
    validation_path = output_dir / "cold_start_execution_record_validation_result.json"
    summary_path = output_dir / "cold_start_same_system_execution_summary.json"

    assert record_path.exists()
    assert validation_path.exists()
    assert summary_path.exists()
    assert summary == json.loads(summary_path.read_text(encoding="utf-8"))

    record = json.loads(record_path.read_text(encoding="utf-8"))
    validation_result = json.loads(validation_path.read_text(encoding="utf-8"))
    statuses = {step["status"] for step in record["per_step_results"]}

    assert validator.validate_record(record, MANIFEST) == []
    assert validation_result["valid"] is True
    assert validation_result["errors"] == []
    assert record["executed_cold_start_reproduction"] is True
    assert statuses <= {"PASS", "FAIL", "BLOCKED"}
    assert "NOT_EXECUTED" not in statuses
    assert all(step["evidence_retained"] is True for step in record["per_step_results"])
    assert all((output_dir / step["evidence_location"]).exists() for step in record["per_step_results"])
    assert all(step["operator_observation"] for step in record["per_step_results"])
    assert record["claim_ceiling"]["scientific_n_increment"] == 0
    assert record["claim_ceiling"]["independent_validation"] == "NOT_ESTABLISHED"
    assert record["claim_ceiling"]["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert summary["record_sha256"] == sha256(record_path)
    assert summary["validation_result_sha256"] == sha256(validation_path)
    assert summary["validation_valid"] is True
    assert summary["executed_cold_start_reproduction"] is True
    assert summary["scientific_state_effect"] == "NONE"
    assert summary["runtime_authorization_effect"] == "NONE"
    assert summary["claim_ceiling"]["scientific_n_increment"] == 0


def test_same_system_execution_cli_writes_same_bounded_record(tmp_path: Path, monkeypatch):
    harness = load_module("cold_start_same_system_execution", HARNESS_SCRIPT)
    output_dir = tmp_path / "cli-same-system-cold-start"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_dgaf_self_application_cold_start_same_system_execution.py",
            "--manifest",
            str(MANIFEST),
            "--output-dir",
            str(output_dir),
        ],
    )

    assert harness.main() == 0

    record = json.loads((output_dir / "cold_start_execution_record.json").read_text(encoding="utf-8"))
    validation = json.loads(
        (output_dir / "cold_start_execution_record_validation_result.json").read_text(encoding="utf-8")
    )
    summary = json.loads((output_dir / "cold_start_same_system_execution_summary.json").read_text(encoding="utf-8"))

    assert record["executed_cold_start_reproduction"] is True
    assert validation["valid"] is True
    assert summary["validation_valid"] is True
    assert summary["same_system_run_independence"] == "NOT_ESTABLISHED"
    assert summary["interpretation"].startswith("Same-system operator-local cold-start execution only")
