from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
OPERATOR_BUNDLE = ROOT / "scripts" / "prepare_track_a_epoch_002_operator_materialization.py"
VALIDATOR = ROOT / "scripts" / "validate_track_a_epoch_002_materialization.py"


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_operator_materialization_bundle_helper_exists() -> None:
    assert OPERATOR_BUNDLE.is_file(), "operator materialization bundle helper is absent"


def stage1_matches_accepted_binding(helper: Any) -> bool:
    current = helper.MATERIALIZER_PATH.read_bytes()
    accepted = helper.git_bytes("show", f"{helper.MATERIALIZER_COMMIT}:{helper.MATERIALIZER_REL}")
    return current == accepted


def assert_stage2_fails_closed_pending_rebind(helper: Any) -> None:
    with pytest.raises(
        SystemExit,
        match="scripts/materialize_track_a_epoch_002_unblinded_input.py drifted from its accepted commit",
    ):
        helper.load_repository_contracts()


def test_repository_contracts_bind_accepted_chain() -> None:
    helper = load_module(OPERATOR_BUNDLE, "epoch002_operator_bundle_contracts")

    if not stage1_matches_accepted_binding(helper):
        assert_stage2_fails_closed_pending_rebind(helper)
        return

    contracts = helper.load_repository_contracts()

    assert contracts["dataset_lock_commit_sha"] == "e7ba2fe6fc6b3587957c59231da81ae107cacab2"
    assert contracts["unblinding_decision_commit_sha"] == "bf6279b9989f211e324ff3e9012788bed95e5c84"
    assert contracts["evidence_tooling_commit_sha"] == "84e3a9ca5af8f87f63c14b06de8aa21430542ada"
    assert contracts["materializer_commit_sha"] == "ebed3db8b5469e8ba8e18aed752aee7baccf05fc"
    assert contracts["materializer_blob_sha"] == "ebc2163003ee9079a887cf378e357fd5078bf1a3"
    assert contracts["dataset_lock_receipt_sha256"]
    assert contracts["unblinding_decision_sha256"]
    assert contracts["dataset_lock_receipt_canonical_sha256"]
    assert contracts["unblinding_decision_canonical_sha256"]


def test_bundle_documents_validate_and_preserve_non_effects() -> None:
    helper = load_module(OPERATOR_BUNDLE, "epoch002_operator_bundle_builder")

    if not stage1_matches_accepted_binding(helper):
        assert_stage2_fails_closed_pending_rebind(helper)
        return

    validator = load_module(VALIDATOR, "epoch002_operator_bundle_validator")
    contracts = helper.load_repository_contracts()
    materialized_input = helper.canonical(
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
    )
    bundle = helper.build_bundle_documents(
        materialized_input=materialized_input,
        contracts=contracts,
        retention_id="epoch002-materialization-local-custody",
    )

    evidence = json.loads(bundle[helper.EVIDENCE_NAME])
    receipt = json.loads(bundle[helper.EXECUTION_RECEIPT_NAME])
    validator.validate_evidence_against_dataset_lock(
        evidence,
        contracts["dataset_lock_evidence"],
    )

    input_sha = helper.digest_bytes(materialized_input)
    assert bundle[helper.SIDECAR_NAME] == f"{input_sha}  {helper.OUTPUT_NAME}\n".encode()
    assert evidence["materialized_input_sha256"] == input_sha
    assert evidence["materialization_manifest_sha256"] == helper.digest_bytes(bundle[helper.MANIFEST_NAME])
    assert evidence["materialization_sidecar_sha256"] == helper.digest_bytes(bundle[helper.SIDECAR_NAME])
    assert evidence["operator_execution_receipt_sha256"] == helper.digest_bytes(bundle[helper.EXECUTION_RECEIPT_NAME])
    assert receipt["repository_materialization_established"] is False
    assert receipt["primary_analysis_authorized"] is False
    assert receipt["primary_analysis_run"] is False
    assert receipt["scientific_n_increment"] == 0
    assert receipt["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"

    serialized = b"\n".join(bundle.values()).lower()
    assert b"begin private key" not in serialized
    assert b"custody_private_key" not in serialized
    assert b"passphrase" not in serialized
    assert b"decrypted_mapping" not in serialized


def test_preflight_refuses_partial_or_existing_bundle(tmp_path: Path) -> None:
    helper = load_module(OPERATOR_BUNDLE, "epoch002_operator_bundle_preflight")
    existing = tmp_path / helper.MANIFEST_NAME
    existing.write_text("preserve me", encoding="utf-8")

    with pytest.raises(SystemExit):
        helper.preflight_output_paths(tmp_path)

    assert existing.read_text(encoding="utf-8") == "preserve me"


def test_post_materialization_failure_leaves_final_output_empty(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    helper = load_module(OPERATOR_BUNDLE, "epoch002_operator_bundle_atomicity")
    payload = b'{"synthetic":true}\n'
    contracts = {
        "dataset_lock_evidence": {},
        "dataset_lock_receipt": {},
        "dataset_lock_receipt_canonical_sha256": "a" * 64,
        "unblinding_decision": {},
        "unblinding_decision_canonical_sha256": "b" * 64,
    }

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

    class FakeValidator:
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
        return FakeValidator

    def fail_after_materialization(**kwargs: Any) -> dict[str, bytes]:
        del kwargs
        raise RuntimeError("synthetic post-materialization failure")

    monkeypatch.setattr(helper, "load_repository_contracts", lambda: contracts)
    monkeypatch.setattr(helper, "load_module", load_fake_module)
    monkeypatch.setattr(helper, "build_bundle_documents", fail_after_materialization)

    final_output = tmp_path / "final"
    with pytest.raises(RuntimeError, match="synthetic post-materialization failure"):
        helper.prepare_operator_bundle(
            Path("public.tar"),
            Path("protected.tar"),
            Path("custody-key.pem"),
            final_output,
            retention_id="synthetic-retention",
        )

    assert final_output.is_dir()
    assert list(final_output.iterdir()) == []


def test_source_preserves_secret_and_analysis_boundary() -> None:
    text = OPERATOR_BUNDLE.read_text(encoding="utf-8")
    assert "--custody-private-key" in text
    assert "--passphrase" not in text
    assert "--private-key-passphrase" not in text
    assert "PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN" in text
    assert 'primary_analysis_authorized": True' not in text
    assert 'scientific_n_increment": 1' not in text


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
