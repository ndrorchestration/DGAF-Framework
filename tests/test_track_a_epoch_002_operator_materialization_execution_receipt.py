from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts" / "prepare_track_a_epoch_002_operator_materialization.py"
SCHEMA = ROOT / "docs" / "experiment" / "TRACK_A_EPOCH_002_OPERATOR_MATERIALIZATION_EXECUTION_RECEIPT_SCHEMA.json"


def load_helper() -> Any:
    spec = importlib.util.spec_from_file_location("epoch002_operator_materialization", HELPER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contracts(helper: Any) -> dict[str, Any]:
    return {
        "dataset_lock_evidence": {
            "public_artifact": {},
            "protected_artifact": {},
        },
        "dataset_lock_receipt": {"record_id": "E002-DATASET-LOCK-TEST0001"},
        "dataset_lock_receipt_sha256": "a" * 64,
        "dataset_lock_receipt_canonical_sha256": "2" * 64,
        "unblinding_decision": {"record_id": "E002-UNBLINDING-TEST0001"},
        "unblinding_decision_sha256": "b" * 64,
        "unblinding_decision_canonical_sha256": "3" * 64,
        "dataset_lock_commit_sha": "c" * 40,
        "unblinding_decision_commit_sha": "d" * 40,
        "evidence_tooling_commit_sha": "e" * 40,
        "materializer_commit_sha": "f" * 40,
        "materializer_blob_sha": "1" * 40,
    }


def generated_receipt() -> dict[str, Any]:
    helper = load_helper()
    bundle = helper.build_bundle_documents(
        materialized_input=helper.canonical(
            {
                "record_type": "TRACK_A_EPOCH_002_UNBLINDED_ANALYSIS_INPUT",
                "schema_version": 1,
                "protocol_id": helper.PROTOCOL,
                "paired_seed_units": 50,
                "record_count": 2250,
                "records": [],
                "primary_analysis_authorized": False,
                "primary_analysis_run": False,
                "outcome_aggregation_performed": False,
                "scientific_n_increment": 0,
                "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            }
        ),
        contracts=contracts(helper),
        retention_id="epoch002-materialization-test-retention",
    )
    return json.loads(bundle[helper.EXECUTION_RECEIPT_NAME])


def schema_validator() -> Draft202012Validator:
    assert SCHEMA.is_file(), "operator materialization execution receipt schema is absent"
    return Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))


def test_generated_operator_execution_receipt_conforms_to_closed_schema() -> None:
    validator = schema_validator()
    errors = sorted(validator.iter_errors(generated_receipt()), key=lambda error: list(error.path))
    assert not errors, [error.message for error in errors]


def test_operator_execution_receipt_schema_rejects_authority_promotion_and_extra_fields() -> None:
    validator = schema_validator()
    receipt = generated_receipt()

    promoted = dict(receipt)
    promoted["primary_analysis_authorized"] = True
    assert list(validator.iter_errors(promoted))

    extended = dict(receipt)
    extended["unexpected_authority"] = "PRIMARY_ANALYSIS"
    assert list(validator.iter_errors(extended))


def test_invalid_execution_receipt_blocks_atomic_bundle_promotion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    helper = load_helper()
    payload = helper.canonical({"synthetic": True})
    bound_contracts = contracts(helper)
    real_builder = helper.build_bundle_documents

    class FakeMaterializer:
        @staticmethod
        def materialize(
            public_archive: Path,
            protected_archive: Path,
            custody_private_key: Path,
            output_dir: Path,
            *,
            contracts: dict[str, Any],
        ) -> dict[str, str]:
            del public_archive, protected_archive, custody_private_key, contracts
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / helper.OUTPUT_NAME).write_bytes(payload)
            return {"materialized_input_sha256": helper.digest_bytes(payload)}

    class FakeEvidenceValidator:
        @staticmethod
        def validate_evidence_against_dataset_lock(
            evidence: dict[str, Any],
            dataset_lock_evidence: dict[str, Any],
        ) -> None:
            del evidence, dataset_lock_evidence

    def load_fake_module(path: Path, name: str) -> Any:
        del name
        if path == helper.MATERIALIZER_PATH:
            return FakeMaterializer
        return FakeEvidenceValidator

    def invalid_builder(**kwargs: Any) -> dict[str, bytes]:
        bundle = real_builder(**kwargs)
        receipt = json.loads(bundle[helper.EXECUTION_RECEIPT_NAME])
        receipt["primary_analysis_authorized"] = True
        bundle[helper.EXECUTION_RECEIPT_NAME] = helper.canonical(receipt)
        return bundle

    monkeypatch.setattr(helper, "load_repository_contracts", lambda: bound_contracts)
    monkeypatch.setattr(helper, "load_module", load_fake_module)
    monkeypatch.setattr(helper, "build_bundle_documents", invalid_builder)

    final_output = tmp_path / "final"
    with pytest.raises(SystemExit, match="operator execution receipt schema violation"):
        helper.prepare_operator_bundle(
            Path("public.tar"),
            Path("protected.tar"),
            Path("custody-key.pem"),
            final_output,
            retention_id="epoch002-materialization-test-retention",
        )

    assert final_output.is_dir()
    assert list(final_output.iterdir()) == []


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
