import json
from pathlib import Path

import pytest
from scripts.lock_audit_hallucination_corpus import (
    build_lock_manifest,
    CorpusValidationError,
    REQUIRED_AUDIT_FIELDS,
    write_manifest,
)


def audit_record(sample_id: str) -> dict:
    return {
        "sample_id": sample_id,
        "role": "Auditor",
        "curvature": -2.0,
        "contraction": 0.5,
        "gate_result": "PASS",
        "timestamp": f"2026-09-09T00:00:{int(sample_id[1:]) % 60:02d}Z",
        "session_id": f"session-{sample_id}",
    }


def write_jsonl(path: Path, records: list[object]) -> None:
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def write_provenance(path: Path, role: str, **extra: object) -> None:
    payload = {
        "corpus_role": role,
        "producer": "fixture-test",
        "generation_process": "deterministic-test-fixture",
        "source_description": "unit-test only",
        **extra,
    }
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def make_paths(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    gt = tmp_path / "ground_truth.jsonl"
    generated = tmp_path / "generated.jsonl"
    gt_prov = tmp_path / "ground_truth.provenance.json"
    generated_prov = tmp_path / "generated.provenance.json"
    write_jsonl(gt, [audit_record(f"s{i:03d}") for i in range(100)])
    write_jsonl(generated, [audit_record(f"s{i:03d}") for i in range(100)])
    write_provenance(gt_prov, "ground_truth")
    write_provenance(
        generated_prov,
        "generated_outputs",
        expected_answer_access_claim=False,
    )
    return gt, generated, gt_prov, generated_prov


def build(tmp_path: Path) -> dict:
    return build_lock_manifest(*make_paths(tmp_path))


def test_valid_aligned_corpora_lock_without_scoring(tmp_path: Path) -> None:
    manifest = build(tmp_path)
    assert manifest["sample_count"] == 100
    assert manifest["alignment"]["status"] == "PASS"
    assert manifest["ground_truth"]["structure_validation"] == "PASS"
    assert manifest["generated_outputs"]["structure_validation"] == "PASS"
    assert manifest["generation_independence"]["status"] == "NOT_VERIFIED"
    assert manifest["task4_scoring_authorized"] is False
    assert manifest["performance_scoring_performed"] is False
    assert manifest["model_performance_result_exists"] is False
    assert manifest["track_a_state_effect"] == "NONE"
    assert manifest["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"


def test_duplicate_ground_truth_id_rejected(tmp_path: Path) -> None:
    gt, generated, gt_prov, generated_prov = make_paths(tmp_path)
    records = [audit_record(f"s{i:03d}") for i in range(99)]
    records.append(audit_record("s000"))
    write_jsonl(gt, records)
    with pytest.raises(CorpusValidationError, match="duplicate sample_id"):
        build_lock_manifest(gt, generated, gt_prov, generated_prov)


def test_duplicate_generated_id_rejected(tmp_path: Path) -> None:
    gt, generated, gt_prov, generated_prov = make_paths(tmp_path)
    records = [audit_record(f"s{i:03d}") for i in range(99)]
    records.append(audit_record("s000"))
    write_jsonl(generated, records)
    with pytest.raises(CorpusValidationError, match="duplicate sample_id"):
        build_lock_manifest(gt, generated, gt_prov, generated_prov)


def test_missing_and_extra_generated_ids_rejected(tmp_path: Path) -> None:
    gt, generated, gt_prov, generated_prov = make_paths(tmp_path)
    records = [audit_record(f"s{i:03d}") for i in range(1, 100)]
    records.append(audit_record("s999"))
    write_jsonl(generated, records)
    with pytest.raises(CorpusValidationError, match="sample_id sets must align exactly"):
        build_lock_manifest(gt, generated, gt_prov, generated_prov)


def test_ground_truth_missing_required_field_rejected(tmp_path: Path) -> None:
    gt, generated, gt_prov, generated_prov = make_paths(tmp_path)
    records = [audit_record(f"s{i:03d}") for i in range(100)]
    records[7].pop(REQUIRED_AUDIT_FIELDS[0])
    write_jsonl(gt, records)
    with pytest.raises(CorpusValidationError, match="missing required non-null fields"):
        build_lock_manifest(gt, generated, gt_prov, generated_prov)


def test_generated_missing_audit_fields_is_structurally_admissible(tmp_path: Path) -> None:
    gt, generated, gt_prov, generated_prov = make_paths(tmp_path)
    write_jsonl(generated, [{"sample_id": f"s{i:03d}"} for i in range(100)])
    manifest = build_lock_manifest(gt, generated, gt_prov, generated_prov)
    assert set(manifest["generated_outputs"]["field_completeness"].values()) == {0}
    assert manifest["generation_independence"]["status"] == "NOT_VERIFIED"


def test_non_object_record_rejected(tmp_path: Path) -> None:
    gt, generated, gt_prov, generated_prov = make_paths(tmp_path)
    records: list[object] = [audit_record(f"s{i:03d}") for i in range(99)] + ["bad"]
    write_jsonl(generated, records)
    with pytest.raises(CorpusValidationError, match="must be a JSON object"):
        build_lock_manifest(gt, generated, gt_prov, generated_prov)


def test_wrong_sample_count_rejected(tmp_path: Path) -> None:
    gt, generated, gt_prov, generated_prov = make_paths(tmp_path)
    write_jsonl(gt, [audit_record(f"s{i:03d}") for i in range(99)])
    with pytest.raises(CorpusValidationError, match="exactly 100 records"):
        build_lock_manifest(gt, generated, gt_prov, generated_prov)


def test_exact_byte_hash_changes_with_nonsemantic_whitespace(tmp_path: Path) -> None:
    gt, generated, gt_prov, generated_prov = make_paths(tmp_path)
    first = build_lock_manifest(gt, generated, gt_prov, generated_prov)
    gt.write_bytes(gt.read_bytes() + b"\n")
    second = build_lock_manifest(gt, generated, gt_prov, generated_prov)
    assert first["ground_truth"]["sha256"] != second["ground_truth"]["sha256"]
    assert first["alignment"] == second["alignment"]


def test_self_asserted_independence_never_upgrades_status(tmp_path: Path) -> None:
    gt, generated, gt_prov, generated_prov = make_paths(tmp_path)
    write_provenance(
        generated_prov,
        "generated_outputs",
        independently_verified=True,
        expected_answer_access_claim=False,
    )
    manifest = build_lock_manifest(gt, generated, gt_prov, generated_prov)
    assert manifest["generation_independence"]["status"] == "NOT_VERIFIED"
    assert manifest["task4_scoring_authorized"] is False


def test_manifest_and_sidecar_are_deterministic(tmp_path: Path) -> None:
    manifest = build(tmp_path)
    output_a = tmp_path / "a.json"
    output_b = tmp_path / "b.json"
    digest_a = write_manifest(manifest, output_a)
    digest_b = write_manifest(manifest, output_b)
    assert output_a.read_bytes() == output_b.read_bytes()
    assert digest_a == digest_b
    sidecar = output_a.with_suffix(".json.sha256").read_text(encoding="utf-8")
    assert sidecar == f"{digest_a}  a.json\n"
