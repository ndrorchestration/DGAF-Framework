from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "dgaf_self_application_cold_start_same_system_execution"
BUILDER_SCRIPT = ROOT / "scripts" / "build_dgaf_self_application_cold_start_execution_record.py"
VALIDATOR_SCRIPT = ROOT / "scripts" / "validate_dgaf_self_application_cold_start_execution_record.py"
RUNBOOK = ROOT / "docs" / "qa" / "DGAF_OPERATOR_SELFTEST.md"
ARTIFACT_WORKFLOW = ROOT / ".github" / "workflows" / "dgaf-cold-start-scaffold-artifact.yml"

EXECUTION_SUMMARY_SCHEMA_VERSION = "dgaf.self_application.cold_start_same_system_execution.v1"
EVIDENCE_CLASS = "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
CLAIM_CEILING = {
    "scientific_n_increment": 0,
    "independent_validation": "NOT_ESTABLISHED",
    "external_validation": "NOT_ESTABLISHED",
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    "high_assurance": "NOT_AUTHORIZED",
}


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _relative_to_output(path: Path, output_dir: Path) -> str:
    return str(path.resolve().relative_to(output_dir.resolve()))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_text_if_present(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _source_status(required_tokens: list[str], source_text: str) -> tuple[str, list[str]]:
    missing = [token for token in required_tokens if token not in source_text]
    return ("PASS" if not missing else "FAIL", missing)


def _probe_measure(measure_id: str) -> dict[str, Any]:
    runbook_text = _read_text_if_present(RUNBOOK)
    workflow_text = _read_text_if_present(ARTIFACT_WORKFLOW)

    if measure_id == "documented_prerequisites":
        status, missing = _source_status(
            [
                "Python 3.12",
                "clean DGAF checkout",
                "ACP checkout",
                "dbab7c1afafec524ce7c18157de2089cafe79c87",
                "scientific_n_increment=0",
            ],
            runbook_text,
        )
        return {
            "status": status,
            "observation": (
                "Repository runbook exposes the bounded operator prerequisites."
                if status == "PASS"
                else "Repository runbook is missing required prerequisite tokens."
            ),
            "evidence": {
                "runbook_path": str(RUNBOOK.relative_to(ROOT)),
                "runbook_sha256": _sha256(RUNBOOK) if RUNBOOK.exists() else None,
                "missing_tokens": missing,
            },
        }

    if measure_id == "command_order":
        status, missing = _source_status(
            [
                "One-command Windows path",
                "Direct Python path",
                "powershell -NoProfile",
                "run_dgaf_operator_selftest.py",
            ],
            runbook_text,
        )
        return {
            "status": status,
            "observation": (
                "Canonical runbook provides explicit command-order paths."
                if status == "PASS"
                else "Canonical command-order documentation is incomplete."
            ),
            "evidence": {
                "runbook_path": str(RUNBOOK.relative_to(ROOT)),
                "runbook_sha256": _sha256(RUNBOOK) if RUNBOOK.exists() else None,
                "missing_tokens": missing,
            },
        }

    if measure_id == "evidence_locations":
        status, missing = _source_status(
            ["Evidence packet", "operator_selftest_report.json", "logs/*.json"],
            runbook_text,
        )
        workflow_status, workflow_missing = _source_status(
            ["Upload retained cold-start scaffold artifact", "cold_start_execution_record.json"],
            workflow_text,
        )
        combined_status = "PASS" if status == "PASS" and workflow_status == "PASS" else "FAIL"
        return {
            "status": combined_status,
            "observation": (
                "Repository documentation and artifact workflow expose retained evidence locations."
                if combined_status == "PASS"
                else "Evidence-location documentation or artifact workflow coverage is incomplete."
            ),
            "evidence": {
                "runbook_path": str(RUNBOOK.relative_to(ROOT)),
                "runbook_sha256": _sha256(RUNBOOK) if RUNBOOK.exists() else None,
                "artifact_workflow_path": str(ARTIFACT_WORKFLOW.relative_to(ROOT)),
                "artifact_workflow_sha256": _sha256(ARTIFACT_WORKFLOW) if ARTIFACT_WORKFLOW.exists() else None,
                "missing_runbook_tokens": missing,
                "missing_workflow_tokens": workflow_missing,
            },
        }

    if measure_id == "environment_reproduction":
        return {
            "status": "BLOCKED",
            "observation": (
                "A same-system repository harness cannot establish clean-environment reproduction; "
                "this remains blocked pending operator-local or external replay evidence."
            ),
            "evidence": {
                "reason": "same-system harness does not provision an independent clean environment",
                "external_review_controller": "issue://929",
            },
        }

    if measure_id == "retained_context_dependence":
        return {
            "status": "BLOCKED",
            "observation": (
                "A same-system run cannot independently rule out retained-context dependence; "
                "external reviewer replay remains required."
            ),
            "evidence": {
                "reason": "same-system operator relationship is intentionally retained and non-independent",
                "external_review_controller": "issue://929",
            },
        }

    return {
        "status": "BLOCKED",
        "observation": f"No bounded probe is implemented for manifest measure {measure_id!r}.",
        "evidence": {"reason": "unrecognized manifest measure"},
    }


def _count_for_status(status: str) -> int:
    return 0 if status == "PASS" else 1


def run_same_system_execution(
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> dict[str, Any]:
    builder = _load_module("cold_start_execution_record_builder", BUILDER_SCRIPT)
    validator = _load_module("cold_start_execution_record_validator", VALIDATOR_SCRIPT)

    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir = output_dir / "evidence"
    record_path = output_dir / "cold_start_execution_record.json"
    validation_path = output_dir / "cold_start_execution_record_validation_result.json"
    summary_path = output_dir / "cold_start_same_system_execution_summary.json"

    manifest = _load_json(manifest_path)
    base_record = builder.build_execution_record(manifest_path)
    per_step_results: list[dict[str, Any]] = []
    metric_counts: dict[str, int] = {}

    measures = manifest.get("measures")
    if not isinstance(measures, list) or not measures:
        raise ValueError("cold-start manifest must contain a non-empty measures array")

    for index, measure in enumerate(measures, start=1):
        if not isinstance(measure, dict):
            raise ValueError(f"measure {index} must be an object")
        measure_id = measure.get("id")
        if not isinstance(measure_id, str) or not measure_id:
            raise ValueError(f"measure {index} is missing id")
        probe = _probe_measure(measure_id)
        evidence_path = evidence_dir / f"{index:02d}_{measure_id}.json"
        evidence_payload = {
            "schema_version": "dgaf.self_application.cold_start_step_evidence.v1",
            "evidence_class": EVIDENCE_CLASS,
            "controller_issue": "issue://1022",
            "external_review_controller": "issue://929",
            "measure": measure,
            "status": probe["status"],
            "operator_observation": probe["observation"],
            "probe_evidence": probe["evidence"],
            "claim_ceiling": CLAIM_CEILING,
            "scientific_state_effect": "NONE",
            "runtime_authorization_effect": "NONE",
        }
        _write_json(evidence_path, evidence_payload)
        metric_name = measure.get("metric")
        if isinstance(metric_name, str) and metric_name:
            metric_counts[metric_name] = _count_for_status(probe["status"])
        per_step_results.append(
            {
                "step_index": index,
                "measure_id": measure_id,
                "question": measure["question"],
                "failure_record": measure["failure_record"],
                "metric": measure["metric"],
                "status": probe["status"],
                "evidence_retained": True,
                "evidence_location": _relative_to_output(evidence_path, output_dir),
                "operator_observation": probe["observation"],
            }
        )

    pass_count = sum(1 for step in per_step_results if step["status"] == "PASS")
    fail_count = sum(1 for step in per_step_results if step["status"] == "FAIL")
    blocked_count = sum(1 for step in per_step_results if step["status"] == "BLOCKED")
    completion_rate = 1.0

    record = dict(base_record)
    record["operator_context"] = {
        "retained_context_allowed": True,
        "executor_relationship": "SAME_SYSTEM_OPERATOR",
        "environment_description": "operator-local same-system cold-start execution harness",
    }
    record["per_step_results"] = per_step_results
    record["summary"] = {
        "cold_start_completion_rate": completion_rate,
        "raw_per_step_results_retained_before_summary": True,
        "same_system_run_independence": "NOT_ESTABLISHED",
        "external_review_controller": "issue://929",
        "pass_count": pass_count,
        "fail_count": fail_count,
        "blocked_count": blocked_count,
        **metric_counts,
    }
    record["executed_cold_start_reproduction"] = True
    record["interpretation"] = (
        "Same-system operator-local cold-start execution only. Results are retained internal engineering "
        "evidence and do not establish independence, external validation, scientific efficacy, scientific N, "
        "or High-Assurance authorization."
    )
    _write_json(record_path, record)

    validation_result = validator.build_validation_result(record_path, manifest_path)
    _write_json(validation_path, validation_result)
    if validation_result.get("valid") is not True:
        raise RuntimeError("same-system cold-start execution produced an invalid execution record")

    summary = {
        "schema_version": EXECUTION_SUMMARY_SCHEMA_VERSION,
        "evidence_class": EVIDENCE_CLASS,
        "controller_issue": "issue://1022",
        "external_review_controller": "issue://929",
        "claim_ceiling": CLAIM_CEILING,
        "record_path": _relative_to_output(record_path, output_dir),
        "record_sha256": _sha256(record_path),
        "validation_result_path": _relative_to_output(validation_path, output_dir),
        "validation_result_sha256": _sha256(validation_path),
        "validation_valid": True,
        "executed_cold_start_reproduction": True,
        "same_system_run_independence": "NOT_ESTABLISHED",
        "scientific_state_effect": "NONE",
        "runtime_authorization_effect": "NONE",
        "pass_count": pass_count,
        "fail_count": fail_count,
        "blocked_count": blocked_count,
        "cold_start_completion_rate": completion_rate,
        "metric_counts": metric_counts,
        "interpretation": (
            "Same-system operator-local cold-start execution only. The record contains retained per-step "
            "evidence before summary, but remains internal engineering validation with no claim promotion."
        ),
    }
    _write_json(summary_path, summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded same-system DGAF cold-start execution.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to cold-start manifest JSON.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory that will receive the execution record, validation result, summary, and evidence.",
    )
    args = parser.parse_args()

    summary = run_same_system_execution(output_dir=Path(args.output_dir), manifest_path=Path(args.manifest))
    print(f"wrote same-system cold-start execution record: {summary['record_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
