from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZER_SCRIPT = ROOT / "scripts" / "materialize_dgaf_self_application_cold_start_scaffold.py"
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


def test_materializer_writes_validator_admissible_scaffold_bundle(tmp_path: Path):
    materializer = load_module("cold_start_scaffold_materializer", MATERIALIZER_SCRIPT)
    validator = load_module("cold_start_execution_record_validator", VALIDATOR_SCRIPT)
    output_dir = tmp_path / "cold-start-scaffold"

    summary = materializer.materialize_scaffold(output_dir=output_dir, manifest_path=MANIFEST)

    record_path = output_dir / "cold_start_execution_record.json"
    validation_path = output_dir / "cold_start_execution_record_validation_result.json"
    summary_path = output_dir / "cold_start_scaffold_materialization_summary.json"

    assert record_path.exists()
    assert validation_path.exists()
    assert summary_path.exists()
    assert summary == json.loads(summary_path.read_text(encoding="utf-8"))

    record = json.loads(record_path.read_text(encoding="utf-8"))
    validation_result = json.loads(validation_path.read_text(encoding="utf-8"))

    assert validator.validate_record(record, MANIFEST) == []
    assert validation_result["valid"] is True
    assert validation_result["errors"] == []
    assert summary["record_sha256"] == sha256(record_path)
    assert summary["validation_result_sha256"] == sha256(validation_path)
    assert summary["validation_valid"] is True
    assert summary["executed_cold_start_reproduction"] is False
    assert summary["scientific_state_effect"] == "NONE"
    assert summary["runtime_authorization_effect"] == "NONE"
    assert summary["claim_ceiling"]["scientific_n_increment"] == 0
    assert summary["claim_ceiling"]["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"


def test_materializer_cli_writes_same_bounded_bundle(tmp_path: Path, monkeypatch):
    materializer = load_module("cold_start_scaffold_materializer", MATERIALIZER_SCRIPT)
    output_dir = tmp_path / "cli-scaffold"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "materialize_dgaf_self_application_cold_start_scaffold.py",
            "--manifest",
            str(MANIFEST),
            "--output-dir",
            str(output_dir),
        ],
    )

    assert materializer.main() == 0

    summary = json.loads(
        (output_dir / "cold_start_scaffold_materialization_summary.json").read_text(encoding="utf-8")
    )
    record = json.loads((output_dir / "cold_start_execution_record.json").read_text(encoding="utf-8"))
    validation = json.loads(
        (output_dir / "cold_start_execution_record_validation_result.json").read_text(encoding="utf-8")
    )
    assert record["executed_cold_start_reproduction"] is False
    assert validation["valid"] is True
    assert summary["validation_valid"] is True
    assert summary["interpretation"].startswith("Operator-local scaffold materialization only")
