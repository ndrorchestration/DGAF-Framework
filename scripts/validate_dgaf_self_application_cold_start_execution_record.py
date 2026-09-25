from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"

EXECUTION_RECORD_SCHEMA_VERSION = "dgaf.self_application.cold_start_execution_record.v1"
VALIDATION_RESULT_SCHEMA_VERSION = "dgaf.self_application.cold_start_execution_record_validation_result.v1"
EVIDENCE_CLASS = "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
CLAIM_CEILING = {
    "scientific_n_increment": 0,
    "independent_validation": "NOT_ESTABLISHED",
    "external_validation": "NOT_ESTABLISHED",
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    "high_assurance": "NOT_AUTHORIZED",
}


class ValidationErrorList(ValueError):
    """Raised when a cold-start execution record fails bounded validation."""

    def __init__(self, errors: list[str]) -> None:
        super().__init__("; ".join(errors))
        self.errors = errors


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _as_measure_map(manifest: dict[str, Any]) -> list[dict[str, str]]:
    measures = manifest.get("measures")
    if not isinstance(measures, list) or not measures:
        raise ValueError("cold-start manifest must contain a non-empty measures array")

    normalized: list[dict[str, str]] = []
    for index, measure in enumerate(measures, start=1):
        if not isinstance(measure, dict):
            raise ValueError(f"manifest measure {index} must be an object")
        normalized_measure = {
            "id": measure.get("id"),
            "question": measure.get("question"),
            "failure_record": measure.get("failure_record"),
            "metric": measure.get("metric"),
        }
        if not all(isinstance(value, str) and value for value in normalized_measure.values()):
            raise ValueError(f"manifest measure {index} is missing required string fields")
        normalized.append(normalized_measure)  # type: ignore[arg-type]
    return normalized


def _expected_completion_rate(per_step_results: list[dict[str, Any]]) -> float:
    if not per_step_results:
        return 0.0
    executed_statuses = {"PASS", "FAIL", "BLOCKED"}
    executed = sum(1 for result in per_step_results if result.get("status") in executed_statuses)
    return executed / len(per_step_results)


def validate_record(record: dict[str, Any], manifest_path: Path = DEFAULT_MANIFEST) -> list[str]:
    manifest = _load_json(manifest_path)
    measures = _as_measure_map(manifest)
    errors: list[str] = []

    expected_top_level = {
        "schema_version",
        "evidence_class",
        "controller_issue",
        "external_review_controller",
        "claim_ceiling",
        "same_system_run_independence",
        "runtime_authorization_effect",
        "scientific_state_effect",
        "execution_mode",
        "operator_context",
        "manifest",
        "per_step_results",
        "summary",
        "executed_cold_start_reproduction",
        "interpretation",
    }
    unexpected = sorted(set(record) - expected_top_level)
    if unexpected:
        errors.append(f"unexpected top-level fields: {unexpected}")

    expected_constants = {
        "schema_version": EXECUTION_RECORD_SCHEMA_VERSION,
        "evidence_class": EVIDENCE_CLASS,
        "controller_issue": "issue://1022",
        "external_review_controller": "issue://929",
        "same_system_run_independence": "NOT_ESTABLISHED",
        "runtime_authorization_effect": "NONE",
        "scientific_state_effect": "NONE",
    }
    for key, expected in expected_constants.items():
        if record.get(key) != expected:
            errors.append(f"{key} must be {expected!r}")

    if record.get("claim_ceiling") != CLAIM_CEILING:
        errors.append("claim_ceiling must preserve the non-promoting #1022 boundary")

    execution_mode = record.get("execution_mode")
    operator_context = record.get("operator_context")
    if not isinstance(operator_context, dict):
        errors.append("operator_context must be an object")
        operator_context = {}

    executor_relationship = operator_context.get("executor_relationship")
    retained_context_allowed = operator_context.get("retained_context_allowed")
    environment_description = operator_context.get("environment_description")
    if not isinstance(environment_description, str) or not environment_description:
        errors.append("operator_context.environment_description must be non-empty")

    if execution_mode == "OPERATOR_LOCAL_REPLAY":
        if executor_relationship != "SAME_SYSTEM_OPERATOR":
            errors.append("OPERATOR_LOCAL_REPLAY requires SAME_SYSTEM_OPERATOR")
    elif execution_mode == "INDEPENDENT_REVIEWER_REPLAY":
        if executor_relationship != "EXTERNAL_REVIEWER":
            errors.append("INDEPENDENT_REVIEWER_REPLAY requires EXTERNAL_REVIEWER")
        if retained_context_allowed is not False:
            errors.append("INDEPENDENT_REVIEWER_REPLAY requires retained_context_allowed=false")
    else:
        errors.append("execution_mode must be OPERATOR_LOCAL_REPLAY or INDEPENDENT_REVIEWER_REPLAY")

    record_manifest = record.get("manifest")
    if not isinstance(record_manifest, dict):
        errors.append("manifest must be an object")
        record_manifest = {}
    expected_manifest_path = "registry/dgaf_self_application_cold_start_manifest_v1.json"
    expected_manifest_schema = "dgaf.self_application.cold_start_manifest.v1"
    if record_manifest.get("path") != expected_manifest_path:
        errors.append(f"manifest.path must be {expected_manifest_path!r}")
    if record_manifest.get("schema_version") != expected_manifest_schema:
        errors.append(f"manifest.schema_version must be {expected_manifest_schema!r}")
    if record_manifest.get("sha256") != _sha256(manifest_path):
        errors.append("manifest.sha256 must match the repository manifest bytes")

    per_step_results = record.get("per_step_results")
    if not isinstance(per_step_results, list):
        errors.append("per_step_results must be an array")
        per_step_results = []
    if len(per_step_results) != len(measures):
        errors.append("per_step_results must contain exactly one result per manifest measure")

    for index, expected_measure in enumerate(measures, start=1):
        if index > len(per_step_results) or not isinstance(per_step_results[index - 1], dict):
            errors.append(f"per_step_results[{index - 1}] must be an object")
            continue
        result = per_step_results[index - 1]
        expected_values = {
            "step_index": index,
            "measure_id": expected_measure["id"],
            "question": expected_measure["question"],
            "failure_record": expected_measure["failure_record"],
            "metric": expected_measure["metric"],
        }
        for key, expected in expected_values.items():
            if result.get(key) != expected:
                errors.append(f"per_step_results[{index - 1}].{key} must match manifest")

        status = result.get("status")
        evidence_location = result.get("evidence_location")
        operator_observation = result.get("operator_observation")
        if status not in {"PASS", "FAIL", "BLOCKED", "NOT_EXECUTED"}:
            errors.append(f"per_step_results[{index - 1}].status is invalid")
        if status != "NOT_EXECUTED":
            if result.get("evidence_retained") is not True:
                errors.append(f"per_step_results[{index - 1}] must retain evidence when executed")
            if not isinstance(evidence_location, str) or not evidence_location:
                errors.append(f"per_step_results[{index - 1}] executed status requires evidence_location")
            if not isinstance(operator_observation, str) or not operator_observation:
                errors.append(f"per_step_results[{index - 1}] executed status requires operator_observation")

    expected_completion = _expected_completion_rate(per_step_results)
    summary = record.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary must be an object")
        summary = {}
    if summary.get("raw_per_step_results_retained_before_summary") is not True:
        errors.append("summary must confirm raw per-step results are retained before summary")
    if summary.get("same_system_run_independence") != "NOT_ESTABLISHED":
        errors.append("summary.same_system_run_independence must remain NOT_ESTABLISHED")
    if summary.get("external_review_controller") != "issue://929":
        errors.append("summary.external_review_controller must remain issue://929")
    if summary.get("cold_start_completion_rate") != expected_completion:
        errors.append("summary.cold_start_completion_rate must match executed step count")

    executed = record.get("executed_cold_start_reproduction")
    if not isinstance(executed, bool):
        errors.append("executed_cold_start_reproduction must be boolean")
    any_executed = any(
        isinstance(result, dict) and result.get("status") in {"PASS", "FAIL", "BLOCKED"}
        for result in per_step_results
    )
    if executed is True and not any_executed:
        errors.append("executed_cold_start_reproduction=true requires at least one executed step")
    if executed is False and any_executed:
        errors.append("executed_cold_start_reproduction=false is incompatible with executed steps")

    interpretation = record.get("interpretation")
    if not isinstance(interpretation, str) or not interpretation:
        errors.append("interpretation must be non-empty")

    return errors


def build_validation_result(record_path: Path, manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    record = _load_json(record_path)
    errors = validate_record(record, manifest_path)
    return {
        "schema_version": VALIDATION_RESULT_SCHEMA_VERSION,
        "record_path": str(record_path),
        "manifest_path": str(manifest_path),
        "valid": not errors,
        "errors": errors,
        "claim_ceiling": CLAIM_CEILING,
        "scientific_state_effect": "NONE",
        "runtime_authorization_effect": "NONE",
        "interpretation": (
            "Validation is an internal engineering gate only; it does not execute reproduction, establish "
            "independence, increment scientific N, or authorize High-Assurance operation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a bounded DGAF cold-start execution record.")
    parser.add_argument("--record", required=True, help="Path to cold-start execution record JSON.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to cold-start manifest JSON.")
    parser.add_argument("--output", help="Optional path for validation result JSON.")
    args = parser.parse_args()

    result = build_validation_result(Path(args.record), Path(args.manifest))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
