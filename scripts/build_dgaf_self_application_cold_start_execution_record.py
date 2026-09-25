from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"

EXECUTION_RECORD_SCHEMA_VERSION = "dgaf.self_application.cold_start_execution_record.v1"
EVIDENCE_CLASS = "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
CLAIM_CEILING = {
    "scientific_n_increment": 0,
    "independent_validation": "NOT_ESTABLISHED",
    "external_validation": "NOT_ESTABLISHED",
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    "high_assurance": "NOT_AUTHORIZED",
}


def _load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("cold-start manifest must be a JSON object")
    if data.get("schema_version") != "dgaf.self_application.cold_start_manifest.v1":
        raise ValueError("unexpected cold-start manifest schema_version")
    if data.get("evidence_class") != EVIDENCE_CLASS:
        raise ValueError("unexpected cold-start evidence_class")
    if data.get("claim_ceiling") != CLAIM_CEILING:
        raise ValueError("unexpected cold-start claim ceiling")
    if data.get("same_system_run_independence") != "NOT_ESTABLISHED":
        raise ValueError("same-system execution-record builder must not claim independence")
    if data.get("runtime_authorization_effect") != "NONE":
        raise ValueError("execution-record builder must not authorize runtime transitions")
    if data.get("scientific_state_effect") != "NONE":
        raise ValueError("execution-record builder must not change scientific state")
    return data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest_path_for_record(manifest_path: Path) -> str:
    return str(manifest_path.resolve().relative_to(ROOT))


def _build_not_executed_steps(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    measures = manifest.get("measures")
    if not isinstance(measures, list) or not measures:
        raise ValueError("cold-start manifest must contain a non-empty measures array")

    steps: list[dict[str, Any]] = []
    for index, measure in enumerate(measures, start=1):
        if not isinstance(measure, dict):
            raise ValueError(f"measure {index} must be an object")
        measure_id = measure.get("id")
        question = measure.get("question")
        failure_record = measure.get("failure_record")
        metric = measure.get("metric")
        if not all(isinstance(value, str) and value for value in (measure_id, question, failure_record, metric)):
            raise ValueError(f"measure {index} is missing required string fields")
        steps.append(
            {
                "step_index": index,
                "measure_id": measure_id,
                "question": question,
                "failure_record": failure_record,
                "metric": metric,
                "status": "NOT_EXECUTED",
                "evidence_retained": False,
            }
        )
    return steps


def build_execution_record(manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    manifest = _load_manifest(manifest_path)
    per_step_results = _build_not_executed_steps(manifest)
    return {
        "schema_version": EXECUTION_RECORD_SCHEMA_VERSION,
        "evidence_class": EVIDENCE_CLASS,
        "controller_issue": "issue://1022",
        "external_review_controller": "issue://929",
        "claim_ceiling": CLAIM_CEILING,
        "same_system_run_independence": "NOT_ESTABLISHED",
        "runtime_authorization_effect": "NONE",
        "scientific_state_effect": "NONE",
        "execution_mode": "OPERATOR_LOCAL_REPLAY",
        "operator_context": {
            "retained_context_allowed": True,
            "executor_relationship": "SAME_SYSTEM_OPERATOR",
            "environment_description": "operator-local nonexecuting cold-start scaffold builder",
        },
        "manifest": {
            "path": _manifest_path_for_record(manifest_path),
            "sha256": _sha256(manifest_path),
            "schema_version": manifest["schema_version"],
        },
        "per_step_results": per_step_results,
        "summary": {
            "cold_start_completion_rate": 0.0,
            "raw_per_step_results_retained_before_summary": True,
            "same_system_run_independence": "NOT_ESTABLISHED",
            "external_review_controller": "issue://929",
        },
        "executed_cold_start_reproduction": False,
        "interpretation": (
            "Operator-local scaffold record only. It creates a validator-admissible NOT_EXECUTED record "
            "and does not execute cold-start reproduction, establish independence, increment scientific N, "
            "or authorize High-Assurance operation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a bounded DGAF cold-start execution-record scaffold.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to cold-start manifest JSON.")
    parser.add_argument("--output", required=True, help="Output JSON path.")
    args = parser.parse_args()

    output_path = Path(args.output)
    record = build_execution_record(Path(args.manifest))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote cold-start execution-record scaffold: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
