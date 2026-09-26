from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "dgaf_self_application_cold_start_same_system_execution"

ADJUDICATION_SCHEMA_VERSION = "dgaf.self_application.cold_start_same_system_adjudication.v1"
EVIDENCE_CLASS = "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
CLAIM_CEILING = {
    "scientific_n_increment": 0,
    "independent_validation": "NOT_ESTABLISHED",
    "external_validation": "NOT_ESTABLISHED",
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    "high_assurance": "NOT_AUTHORIZED",
}


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


def _require_summary_boundary(summary: dict[str, Any]) -> None:
    if summary.get("validation_valid") is not True:
        raise ValueError("valid same-system execution summary is required for adjudication")
    if summary.get("executed_cold_start_reproduction") is not True:
        raise ValueError("valid same-system execution summary must be executed")
    if summary.get("same_system_run_independence") != "NOT_ESTABLISHED":
        raise ValueError("same-system independence must remain NOT_ESTABLISHED")
    if summary.get("scientific_state_effect") != "NONE":
        raise ValueError("same-system adjudication cannot promote scientific state")
    if summary.get("runtime_authorization_effect") != "NONE":
        raise ValueError("same-system adjudication cannot authorize runtime effects")
    if summary.get("claim_ceiling") != CLAIM_CEILING:
        raise ValueError("same-system execution summary must preserve the accepted claim ceiling")


def _require_validation_result(validation_result: dict[str, Any]) -> None:
    if validation_result.get("valid") is not True:
        raise ValueError("validation result must be valid before adjudication")
    errors = validation_result.get("errors")
    if errors not in ([], None):
        raise ValueError("validation result must not contain errors before adjudication")
    if validation_result.get("claim_ceiling") != CLAIM_CEILING:
        raise ValueError("validation result must preserve the accepted claim ceiling")


def _classify(pass_count: int, fail_count: int, blocked_count: int) -> tuple[str, bool, bool]:
    external_replay_required = True
    internal_remediation_required = fail_count > 0
    if fail_count > 0:
        return (
            "SAME_SYSTEM_EXECUTED_INTERNAL_REMEDIATION_REQUIRED",
            internal_remediation_required,
            external_replay_required,
        )
    if blocked_count > 0:
        return (
            "SAME_SYSTEM_EXECUTED_EXTERNAL_REPLAY_REQUIRED",
            internal_remediation_required,
            external_replay_required,
        )
    if pass_count > 0:
        return (
            "SAME_SYSTEM_EXECUTED_EXTERNAL_REPLAY_REQUIRED",
            internal_remediation_required,
            external_replay_required,
        )
    return "SAME_SYSTEM_EXECUTED_NO_ADMISSIBLE_STEPS", True, external_replay_required


def adjudicate_same_system_execution(output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    summary_path = output_dir / "cold_start_same_system_execution_summary.json"
    record_path = output_dir / "cold_start_execution_record.json"
    validation_path = output_dir / "cold_start_execution_record_validation_result.json"
    adjudication_path = output_dir / "cold_start_same_system_adjudication.json"

    summary = _load_json(summary_path)
    _require_summary_boundary(summary)
    record = _load_json(record_path)
    validation_result = _load_json(validation_path)
    _require_validation_result(validation_result)

    pass_count = int(summary.get("pass_count", 0))
    fail_count = int(summary.get("fail_count", 0))
    blocked_count = int(summary.get("blocked_count", 0))
    classification, internal_remediation_required, external_replay_required = _classify(
        pass_count,
        fail_count,
        blocked_count,
    )

    if record.get("summary", {}).get("pass_count") != pass_count:
        raise ValueError("record and summary pass_count disagree")
    if record.get("summary", {}).get("fail_count") != fail_count:
        raise ValueError("record and summary fail_count disagree")
    if record.get("summary", {}).get("blocked_count") != blocked_count:
        raise ValueError("record and summary blocked_count disagree")
    if record.get("claim_ceiling") != CLAIM_CEILING:
        raise ValueError("execution record must preserve the accepted claim ceiling")

    adjudication = {
        "schema_version": ADJUDICATION_SCHEMA_VERSION,
        "evidence_class": EVIDENCE_CLASS,
        "controller_issue": "issue://1022",
        "external_review_controller": "issue://929",
        "input_summary_path": _relative_to_output(summary_path, output_dir),
        "input_summary_sha256": _sha256(summary_path),
        "record_path": _relative_to_output(record_path, output_dir),
        "record_sha256": _sha256(record_path),
        "validation_result_path": _relative_to_output(validation_path, output_dir),
        "validation_result_sha256": _sha256(validation_path),
        "validation_valid": True,
        "executed_cold_start_reproduction": True,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "blocked_count": blocked_count,
        "classification": classification,
        "internal_remediation_required": internal_remediation_required,
        "external_replay_required": external_replay_required,
        "same_system_run_independence": "NOT_ESTABLISHED",
        "claim_ceiling": CLAIM_CEILING,
        "scientific_state_effect": "NONE",
        "runtime_authorization_effect": "NONE",
        "interpretation": (
            "Same-system adjudication only. It can classify internal remediation needs, but cannot establish "
            "independent validation, external validation, scientific efficacy, scientific N, or High-Assurance."
        ),
    }
    _write_json(adjudication_path, adjudication)
    return adjudication


def main() -> int:
    parser = argparse.ArgumentParser(description="Adjudicate bounded same-system DGAF cold-start execution.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory containing the execution record, validation result, and summary.",
    )
    args = parser.parse_args()

    adjudication = adjudicate_same_system_execution(output_dir=Path(args.output_dir))
    print(f"wrote same-system cold-start adjudication: {adjudication['classification']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
