from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
BUILDER_SCRIPT = ROOT / "scripts" / "build_dgaf_self_application_cold_start_execution_record.py"
VALIDATOR_SCRIPT = ROOT / "scripts" / "validate_dgaf_self_application_cold_start_execution_record.py"
MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_builder_emits_validator_admissible_nonexecuted_operator_record():
    builder = load_module("cold_start_execution_record_builder", BUILDER_SCRIPT)
    validator = load_module("cold_start_execution_record_validator", VALIDATOR_SCRIPT)

    record = builder.build_execution_record(MANIFEST)

    assert validator.validate_record(record, MANIFEST) == []
    assert record["schema_version"] == "dgaf.self_application.cold_start_execution_record.v1"
    assert record["execution_mode"] == "OPERATOR_LOCAL_REPLAY"
    assert record["operator_context"]["executor_relationship"] == "SAME_SYSTEM_OPERATOR"
    assert record["operator_context"]["retained_context_allowed"] is True
    assert record["executed_cold_start_reproduction"] is False
    assert record["summary"]["cold_start_completion_rate"] == 0.0
    assert record["scientific_state_effect"] == "NONE"
    assert record["runtime_authorization_effect"] == "NONE"
    assert record["claim_ceiling"]["scientific_n_increment"] == 0
    assert record["claim_ceiling"]["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"


def test_builder_retains_one_not_executed_step_per_manifest_measure():
    builder = load_module("cold_start_execution_record_builder", BUILDER_SCRIPT)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    record = builder.build_execution_record(MANIFEST)

    expected_measure_ids = [measure["id"] for measure in manifest["measures"]]
    observed_measure_ids = [step["measure_id"] for step in record["per_step_results"]]
    assert observed_measure_ids == expected_measure_ids
    assert len(record["per_step_results"]) == len(manifest["measures"])
    assert all(step["status"] == "NOT_EXECUTED" for step in record["per_step_results"])
    assert all(step["evidence_retained"] is False for step in record["per_step_results"])
    assert all("evidence_location" not in step for step in record["per_step_results"])
    assert all("operator_observation" not in step for step in record["per_step_results"])


def test_builder_cli_writes_validator_admissible_record(tmp_path: Path, monkeypatch):
    builder = load_module("cold_start_execution_record_builder", BUILDER_SCRIPT)
    validator = load_module("cold_start_execution_record_validator", VALIDATOR_SCRIPT)
    output_path = tmp_path / "cold-start-execution-record.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_dgaf_self_application_cold_start_execution_record.py",
            "--manifest",
            str(MANIFEST),
            "--output",
            str(output_path),
        ],
    )

    assert builder.main() == 0
    record = json.loads(output_path.read_text(encoding="utf-8"))

    assert validator.validate_record(record, MANIFEST) == []
    assert record["executed_cold_start_reproduction"] is False
    assert record["same_system_run_independence"] == "NOT_ESTABLISHED"
