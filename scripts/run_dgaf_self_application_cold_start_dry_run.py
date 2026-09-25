from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"

EVIDENCE_CLASS = "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
CLAIM_CEILING = {
    "scientific_n_increment": 0,
    "independent_validation": "NOT_ESTABLISHED",
    "external_validation": "NOT_ESTABLISHED",
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    "high_assurance": "NOT_AUTHORIZED",
}


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "dgaf.self_application.cold_start_manifest.v1":
        raise ValueError("unexpected cold-start manifest schema_version")
    if data.get("evidence_class") != EVIDENCE_CLASS:
        raise ValueError("unexpected cold-start evidence_class")
    if data.get("claim_ceiling") != CLAIM_CEILING:
        raise ValueError("unexpected cold-start claim ceiling")
    if data.get("same_system_run_independence") != "NOT_ESTABLISHED":
        raise ValueError("same-system dry runs must not claim independence")
    if data.get("runtime_authorization_effect") != "NONE":
        raise ValueError("cold-start dry run must not authorize runtime transitions")
    if data.get("scientific_state_effect") != "NONE":
        raise ValueError("cold-start dry run must not change scientific state")
    return data


def build_dry_run_record(manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    manifest_bytes = manifest_path.read_bytes()
    manifest = load_manifest(manifest_path)
    measures = manifest.get("measures", [])
    if not isinstance(measures, list) or not measures:
        raise ValueError("cold-start manifest must contain non-empty measures")

    per_step_results: list[dict[str, Any]] = []
    for index, measure in enumerate(measures, start=1):
        measure_id = measure.get("id")
        failure_record = measure.get("failure_record")
        metric = measure.get("metric")
        question = measure.get("question")
        if not all(isinstance(value, str) and value for value in (measure_id, failure_record, metric, question)):
            raise ValueError(f"measure {index} is missing required string fields")
        per_step_results.append(
            {
                "step_index": index,
                "measure_id": measure_id,
                "question": question,
                "failure_record": failure_record,
                "metric": metric,
                "status": "NOT_EXECUTED",
                "evidence_retained": False,
                "interpretation": "Dry-run contract placeholder only; no cold-start reproduction executed.",
            }
        )

    summary = {
        "cold_start_completion_rate": 0.0,
        "undocumented_prerequisite_count": None,
        "manual_decision_count": None,
        "ambiguous_evidence_location_count": None,
        "setup_failure_count": None,
        "hidden_context_dependency_count": None,
        "raw_per_step_results_retained_before_summary": True,
        "same_system_run_independence": "NOT_ESTABLISHED",
        "external_review_controller": manifest["external_review_controller"],
    }

    interpretation = (
        "Internal dry-run contract record only. It retains the measurement scaffold but does not execute "
        "cold-start reproduction or establish independence."
    )

    return {
        "schema_version": "dgaf.self_application.cold_start_dry_run_result.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "evidence_class": EVIDENCE_CLASS,
        "claim_ceiling": CLAIM_CEILING,
        "controller_issue": manifest["controller_issue"],
        "external_review_controller": manifest["external_review_controller"],
        "same_system_run_independence": "NOT_ESTABLISHED",
        "runtime_authorization_effect": "NONE",
        "scientific_state_effect": "NONE",
        "manifest": {
            "path": str(manifest_path.relative_to(ROOT)),
            "sha256": _sha256_bytes(manifest_bytes),
            "schema_version": manifest["schema_version"],
        },
        "per_step_results": per_step_results,
        "summary": summary,
        "executed_cold_start_reproduction": False,
        "interpretation": interpretation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit bounded DGAF self-application cold-start dry-run JSON.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to cold-start manifest JSON.")
    parser.add_argument("--output", required=True, help="Output JSON path.")
    args = parser.parse_args()

    output_path = Path(args.output)
    record = build_dry_run_record(Path(args.manifest))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote cold-start dry-run record: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
