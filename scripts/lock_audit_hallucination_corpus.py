#!/usr/bin/env python3
"""Lock Task-4 audit corpora without scoring or self-certifying independence.

This tool is an intake/custody boundary for EVAL-001 audit_hallucination_rate.
It validates exact corpus structure and one-to-one sample alignment, hashes the
exact admitted bytes, and emits a deterministic lock manifest plus SHA-256
sidecar. It does not evaluate model performance and cannot establish that the
generated-output producer was independent of the expected answers.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "DGAF_AUDIT_HALLUCINATION_CORPUS_LOCK_V1"
EXPECTED_SAMPLES = 100
SAMPLE_ID_FIELD = "sample_id"
REQUIRED_AUDIT_FIELDS = (
    "role",
    "curvature",
    "contraction",
    "gate_result",
    "timestamp",
    "session_id",
)


class CorpusValidationError(ValueError):
    """Raised when an audit corpus cannot satisfy the intake contract."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_json_object(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CorpusValidationError(f"{label} must be valid UTF-8 JSON") from exc
    if not isinstance(parsed, dict):
        raise CorpusValidationError(f"{label} must be a JSON object")
    return parsed, raw


def _load_jsonl(path: Path, label: str) -> tuple[list[dict[str, Any]], bytes]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CorpusValidationError(f"{label} must be valid UTF-8 JSONL") from exc

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CorpusValidationError(
                f"{label} line {line_number} is not valid JSON"
            ) from exc
        if not isinstance(record, dict):
            raise CorpusValidationError(
                f"{label} line {line_number} must be a JSON object"
            )
        records.append(record)
    return records, raw


def _index_records(
    records: list[dict[str, Any]], label: str
) -> dict[str, dict[str, Any]]:
    if len(records) != EXPECTED_SAMPLES:
        raise CorpusValidationError(
            f"{label} must contain exactly {EXPECTED_SAMPLES} records; got {len(records)}"
        )

    indexed: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        sample_id = record.get(SAMPLE_ID_FIELD)
        if not isinstance(sample_id, str) or not sample_id.strip():
            raise CorpusValidationError(
                f"{label}[{index}] requires a non-empty string {SAMPLE_ID_FIELD}"
            )
        if sample_id in indexed:
            raise CorpusValidationError(f"{label} duplicate sample_id: {sample_id}")
        indexed[sample_id] = record
    return indexed


def _validate_ground_truth(indexed: dict[str, dict[str, Any]]) -> None:
    for sample_id, record in indexed.items():
        missing = [
            field
            for field in REQUIRED_AUDIT_FIELDS
            if field not in record or record[field] is None
        ]
        if missing:
            raise CorpusValidationError(
                f"ground_truth sample {sample_id} missing required non-null fields: {missing}"
            )


def _generated_completeness(indexed: dict[str, dict[str, Any]]) -> dict[str, int]:
    return {
        field: sum(
            field in record and record[field] is not None for record in indexed.values()
        )
        for field in REQUIRED_AUDIT_FIELDS
    }


def _validate_provenance_role(metadata: dict[str, Any], expected_role: str) -> None:
    if metadata.get("corpus_role") != expected_role:
        raise CorpusValidationError(
            f"provenance corpus_role must be {expected_role!r}"
        )


def build_lock_manifest(
    ground_truth_path: Path,
    generated_outputs_path: Path,
    ground_truth_provenance_path: Path,
    generated_outputs_provenance_path: Path,
) -> dict[str, Any]:
    ground_truth, ground_truth_bytes = _load_jsonl(
        ground_truth_path, "ground_truth"
    )
    generated, generated_bytes = _load_jsonl(
        generated_outputs_path, "generated_outputs"
    )
    gt_index = _index_records(ground_truth, "ground_truth")
    generated_index = _index_records(generated, "generated_outputs")
    _validate_ground_truth(gt_index)

    gt_ids = set(gt_index)
    generated_ids = set(generated_index)
    if gt_ids != generated_ids:
        missing = sorted(gt_ids - generated_ids)
        extra = sorted(generated_ids - gt_ids)
        raise CorpusValidationError(
            f"sample_id sets must align exactly; missing_generated={missing}, extra_generated={extra}"
        )

    gt_provenance, gt_provenance_bytes = _load_json_object(
        ground_truth_provenance_path, "ground_truth_provenance"
    )
    generated_provenance, generated_provenance_bytes = _load_json_object(
        generated_outputs_provenance_path, "generated_outputs_provenance"
    )
    _validate_provenance_role(gt_provenance, "ground_truth")
    _validate_provenance_role(generated_provenance, "generated_outputs")

    ordered_ids = sorted(gt_ids)
    aligned_ids_bytes = json.dumps(
        ordered_ids, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")

    return {
        "schema": SCHEMA,
        "sample_count": EXPECTED_SAMPLES,
        "sample_id_field": SAMPLE_ID_FIELD,
        "required_audit_fields": list(REQUIRED_AUDIT_FIELDS),
        "ground_truth": {
            "sha256": sha256_bytes(ground_truth_bytes),
            "provenance_sha256": sha256_bytes(gt_provenance_bytes),
            "provenance_claims": gt_provenance,
            "structure_validation": "PASS",
            "required_field_completeness": {
                field: EXPECTED_SAMPLES for field in REQUIRED_AUDIT_FIELDS
            },
        },
        "generated_outputs": {
            "sha256": sha256_bytes(generated_bytes),
            "provenance_sha256": sha256_bytes(generated_provenance_bytes),
            "provenance_claims": generated_provenance,
            "structure_validation": "PASS",
            "field_completeness": _generated_completeness(generated_index),
        },
        "alignment": {
            "status": "PASS",
            "aligned_sample_ids_sha256": sha256_bytes(aligned_ids_bytes),
        },
        "generation_independence": {
            "status": "NOT_VERIFIED",
            "reason": (
                "Supplied provenance claims are retained but cannot independently prove "
                "that generated outputs were produced without access to expected answers."
            ),
        },
        "task4_scoring_authorized": False,
        "performance_scoring_performed": False,
        "model_performance_result_exists": False,
        "track_a_state_effect": "NONE",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def write_manifest(manifest: dict[str, Any], output_path: Path) -> str:
    payload = (
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    output_path.write_bytes(payload)
    digest = sha256_bytes(payload)
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="utf-8"
    )
    return digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument("--generated-outputs", type=Path, required=True)
    parser.add_argument("--ground-truth-provenance", type=Path, required=True)
    parser.add_argument("--generated-outputs-provenance", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = build_lock_manifest(
        args.ground_truth,
        args.generated_outputs,
        args.ground_truth_provenance,
        args.generated_outputs_provenance,
    )
    digest = write_manifest(manifest, args.output)
    print(f"AUDIT_CORPUS_LOCK=PASS sha256={digest}")
    print("GENERATION_INDEPENDENCE=NOT_VERIFIED")
    print("TASK4_SCORING_AUTHORIZED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
