from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_dgaf_self_application_cold_start_execution_record.py"
MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"


def load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cold_start_execution_record_validator", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def manifest_sha() -> str:
    return hashlib.sha256(MANIFEST.read_bytes()).hexdigest()


def base_record(*, executed: bool = False, execution_mode: str = "OPERATOR_LOCAL_REPLAY") -> dict[str, Any]:
    source_manifest = manifest()
    per_step_results: list[dict[str, Any]] = []
    for index, measure in enumerate(source_manifest["measures"], start=1):
        status = "PASS" if executed else "NOT_EXECUTED"
        per_step_results.append(
            {
                "step_index": index,
                "measure_id": measure["id"],
                "question": measure["question"],
                "failure_record": measure["failure_record"],
                "metric": measure["metric"],
                "status": status,
                "evidence_retained": executed,
                "evidence_location": f"artifacts/cold-start/step-{index}.json" if executed else None,
                "operator_observation": "step evidence retained" if executed else "",
            }
        )

    if execution_mode == "INDEPENDENT_REVIEWER_REPLAY":
        executor_relationship = "EXTERNAL_REVIEWER"
        retained_context_allowed = False
    else:
        executor_relationship = "SAME_SYSTEM_OPERATOR"
        retained_context_allowed = True

    return {
        "schema_version": "dgaf.self_application.cold_start_execution_record.v1",
        "evidence_class": "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION",
        "controller_issue": "issue://1022",
        "external_review_controller": "issue://929",
        "claim_ceiling": {
            "scientific_n_increment": 0,
            "independent_validation": "NOT_ESTABLISHED",
            "external_validation": "NOT_ESTABLISHED",
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED",
        },
        "same_system_run_independence": "NOT_ESTABLISHED",
        "runtime_authorization_effect": "NONE",
        "scientific_state_effect": "NONE",
        "execution_mode": execution_mode,
        "operator_context": {
            "retained_context_allowed": retained_context_allowed,
            "executor_relationship": executor_relationship,
            "environment_description": "bounded test fixture environment",
        },
        "manifest": {
            "path": "registry/dgaf_self_application_cold_start_manifest_v1.json",
            "sha256": manifest_sha(),
            "schema_version": source_manifest["schema_version"],
        },
        "per_step_results": per_step_results,
        "summary": {
            "cold_start_completion_rate": 1.0 if executed else 0.0,
            "raw_per_step_results_retained_before_summary": True,
            "same_system_run_independence": "NOT_ESTABLISHED",
            "external_review_controller": "issue://929",
        },
        "executed_cold_start_reproduction": executed,
        "interpretation": "bounded validator fixture only; no scientific promotion",
    }


def test_valid_operator_local_nonexecuted_record_passes():
    module = load_module()
    record = base_record(executed=False)

    assert module.validate_record(record, MANIFEST) == []


def test_valid_operator_local_executed_record_passes_without_promoting_claims():
    module = load_module()
    record = base_record(executed=True)

    assert module.validate_record(record, MANIFEST) == []
    assert record["claim_ceiling"]["scientific_n_increment"] == 0
    assert record["claim_ceiling"]["independent_validation"] == "NOT_ESTABLISHED"


def test_executed_step_requires_retained_evidence_and_observation():
    module = load_module()
    record = base_record(executed=True)
    record["per_step_results"][0]["evidence_retained"] = False
    record["per_step_results"][0]["evidence_location"] = None
    record["per_step_results"][0]["operator_observation"] = ""

    errors = module.validate_record(record, MANIFEST)

    assert any("must retain evidence" in error for error in errors)
    assert any("requires evidence_location" in error for error in errors)
    assert any("requires operator_observation" in error for error in errors)


def test_manifest_measure_order_and_identity_must_match():
    module = load_module()
    record = base_record(executed=False)
    record["per_step_results"][0]["measure_id"] = "wrong-measure"

    errors = module.validate_record(record, MANIFEST)

    assert any("measure_id must match manifest" in error for error in errors)


def test_external_reviewer_replay_rejects_retained_context():
    module = load_module()
    record = base_record(executed=False, execution_mode="INDEPENDENT_REVIEWER_REPLAY")
    record["operator_context"]["retained_context_allowed"] = True

    errors = module.validate_record(record, MANIFEST)

    assert any("retained_context_allowed=false" in error for error in errors)


def test_cli_writes_validation_result(tmp_path: Path, monkeypatch):
    module = load_module()
    record_path = tmp_path / "execution-record.json"
    output_path = tmp_path / "validation-result.json"
    record_path.write_text(json.dumps(base_record(executed=False)), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate_dgaf_self_application_cold_start_execution_record.py",
            "--record",
            str(record_path),
            "--manifest",
            str(MANIFEST),
            "--output",
            str(output_path),
        ],
    )

    assert module.main() == 0
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["schema_version"] == "dgaf.self_application.cold_start_execution_record_validation_result.v1"
    assert result["valid"] is True
    assert result["scientific_state_effect"] == "NONE"
    assert result["claim_ceiling"]["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
