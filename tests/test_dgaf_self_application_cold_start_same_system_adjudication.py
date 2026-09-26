from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
HARNESS_SCRIPT = ROOT / "scripts" / "run_dgaf_self_application_cold_start_same_system_execution.py"
ADJUDICATOR_SCRIPT = ROOT / "scripts" / "adjudicate_dgaf_self_application_cold_start_same_system_execution.py"
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


def test_same_system_execution_adjudicator_emits_non_promoting_record(tmp_path: Path):
    harness = load_module("cold_start_same_system_execution", HARNESS_SCRIPT)
    adjudicator = load_module("cold_start_same_system_adjudication", ADJUDICATOR_SCRIPT)
    output_dir = tmp_path / "same-system-cold-start"

    harness_summary = harness.run_same_system_execution(output_dir=output_dir, manifest_path=MANIFEST)
    adjudication = adjudicator.adjudicate_same_system_execution(output_dir=output_dir)

    adjudication_path = output_dir / "cold_start_same_system_adjudication.json"
    record_path = output_dir / "cold_start_execution_record.json"
    summary_path = output_dir / "cold_start_same_system_execution_summary.json"
    validation_path = output_dir / "cold_start_execution_record_validation_result.json"

    assert adjudication_path.exists()
    assert adjudication == json.loads(adjudication_path.read_text(encoding="utf-8"))
    assert adjudication["schema_version"] == "dgaf.self_application.cold_start_same_system_adjudication.v1"
    assert adjudication["evidence_class"] == "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
    assert adjudication["controller_issue"] == "issue://1022"
    assert adjudication["external_review_controller"] == "issue://929"

    assert adjudication["input_summary_path"] == "cold_start_same_system_execution_summary.json"
    assert adjudication["input_summary_sha256"] == sha256(summary_path)
    assert adjudication["record_sha256"] == sha256(record_path)
    assert adjudication["validation_result_sha256"] == sha256(validation_path)
    assert adjudication["validation_valid"] is True
    assert adjudication["executed_cold_start_reproduction"] is True

    assert adjudication["pass_count"] == harness_summary["pass_count"]
    assert adjudication["fail_count"] == harness_summary["fail_count"]
    assert adjudication["blocked_count"] == harness_summary["blocked_count"]
    assert adjudication["fail_count"] == 0
    assert adjudication["blocked_count"] >= 1
    assert adjudication["internal_remediation_required"] is False
    assert adjudication["external_replay_required"] is True
    assert adjudication["classification"] == "SAME_SYSTEM_EXECUTED_EXTERNAL_REPLAY_REQUIRED"

    assert adjudication["same_system_run_independence"] == "NOT_ESTABLISHED"
    assert adjudication["scientific_state_effect"] == "NONE"
    assert adjudication["runtime_authorization_effect"] == "NONE"
    assert adjudication["claim_ceiling"]["scientific_n_increment"] == 0
    assert adjudication["claim_ceiling"]["independent_validation"] == "NOT_ESTABLISHED"
    assert adjudication["claim_ceiling"]["external_validation"] == "NOT_ESTABLISHED"
    assert adjudication["claim_ceiling"]["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert adjudication["claim_ceiling"]["high_assurance"] == "NOT_AUTHORIZED"


def test_same_system_execution_adjudicator_fails_closed_on_invalid_summary(tmp_path: Path):
    adjudicator = load_module("cold_start_same_system_adjudication", ADJUDICATOR_SCRIPT)
    output_dir = tmp_path / "same-system-cold-start"
    output_dir.mkdir(parents=True)
    (output_dir / "cold_start_same_system_execution_summary.json").write_text(
        json.dumps(
            {
                "validation_valid": False,
                "executed_cold_start_reproduction": True,
                "scientific_state_effect": "NONE",
                "runtime_authorization_effect": "NONE",
            }
        ),
        encoding="utf-8",
    )

    try:
        adjudicator.adjudicate_same_system_execution(output_dir=output_dir)
    except ValueError as exc:
        assert "valid same-system execution summary" in str(exc)
    else:
        raise AssertionError("adjudicator must fail closed on invalid same-system execution summaries")
