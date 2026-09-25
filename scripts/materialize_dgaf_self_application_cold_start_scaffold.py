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
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "dgaf_self_application_cold_start_scaffold"
BUILDER_SCRIPT = ROOT / "scripts" / "build_dgaf_self_application_cold_start_execution_record.py"
VALIDATOR_SCRIPT = ROOT / "scripts" / "validate_dgaf_self_application_cold_start_execution_record.py"

MATERIALIZATION_SCHEMA_VERSION = "dgaf.self_application.cold_start_scaffold_materialization.v1"
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


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _relative_to_root(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def materialize_scaffold(output_dir: Path = DEFAULT_OUTPUT_DIR, manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    builder = _load_module("cold_start_execution_record_builder", BUILDER_SCRIPT)
    validator = _load_module("cold_start_execution_record_validator", VALIDATOR_SCRIPT)

    output_dir.mkdir(parents=True, exist_ok=True)
    record_path = output_dir / "cold_start_execution_record.json"
    validation_path = output_dir / "cold_start_execution_record_validation_result.json"
    summary_path = output_dir / "cold_start_scaffold_materialization_summary.json"

    record = builder.build_execution_record(manifest_path)
    _write_json(record_path, record)

    validation_result = validator.build_validation_result(record_path, manifest_path)
    _write_json(validation_path, validation_result)
    if validation_result.get("valid") is not True:
        raise RuntimeError("cold-start scaffold materialization produced an invalid execution record")

    summary = {
        "schema_version": MATERIALIZATION_SCHEMA_VERSION,
        "evidence_class": EVIDENCE_CLASS,
        "controller_issue": "issue://1022",
        "external_review_controller": "issue://929",
        "claim_ceiling": CLAIM_CEILING,
        "manifest_path": _relative_to_root(manifest_path),
        "manifest_sha256": _sha256(manifest_path),
        "record_path": _relative_to_root(record_path),
        "record_sha256": _sha256(record_path),
        "validation_result_path": _relative_to_root(validation_path),
        "validation_result_sha256": _sha256(validation_path),
        "validation_valid": True,
        "executed_cold_start_reproduction": False,
        "scientific_state_effect": "NONE",
        "runtime_authorization_effect": "NONE",
        "interpretation": (
            "Operator-local scaffold materialization only. It writes a NOT_EXECUTED execution record "
            "and its validation result for retained local evidence handling; it does not execute cold-start "
            "reproduction, establish independence, increment scientific N, or authorize High-Assurance operation."
        ),
    }
    _write_json(summary_path, summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Materialize a bounded DGAF cold-start NOT_EXECUTED scaffold bundle."
    )
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to cold-start manifest JSON.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory that will receive the scaffold record, validation result, and summary.",
    )
    args = parser.parse_args()

    summary = materialize_scaffold(output_dir=Path(args.output_dir), manifest_path=Path(args.manifest))
    print(f"wrote cold-start scaffold materialization summary: {summary['record_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
