from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_materialization.py"
DATASET_LOCK_EVIDENCE_PATH = ROOT / ("docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE.json")


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "epoch_002_materialization_operator_provenance",
        MODULE_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def operator_materialization_evidence_fixture(dataset_lock: dict) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "evidence_execution_class": "OPERATOR_CODESPACE",
        "operator_execution_receipt_sha256": "1" * 64,
        "evidence_tooling_commit_sha": "2" * 40,
        "materializer_path": "scripts/materialize_track_a_epoch_002_unblinded_input.py",
        "materializer_commit_sha": "3" * 40,
        "materializer_blob_sha": "4" * 40,
        "dataset_lock_record_id": "E002-DATASET-LOCK-A16973BD7AA9E1EB",
        "dataset_lock_commit_sha": "e7ba2fe6fc6b3587957c59231da81ae107cacab2",
        "dataset_lock_receipt_sha256": "5" * 64,
        "unblinding_decision_record_id": "E002-UNBLINDING-00112233",
        "unblinding_decision_commit_sha": "bf6279b9989f211e324ff3e9012788bed95e5c84",
        "unblinding_decision_sha256": "6" * 64,
        "public_artifact": dict(dataset_lock["public_artifact"]),
        "protected_artifact": dict(dataset_lock["protected_artifact"]),
        "materialized_input_sha256": "7" * 64,
        "materialization_manifest_sha256": "8" * 64,
        "materialization_sidecar_sha256": "9" * 64,
        "paired_seed_units": 50,
        "record_count": 2250,
        "structure_validation": "PASS",
        "durable_retention": {
            "class": "LOCAL_CUSTODY_ARCHIVE",
            "id": "epoch002-materialization-evidence-content-addressed",
        },
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "secret_material_persisted": False,
        "outcome_aggregation_performed": False,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "historical_pooling_allowed": False,
        "epoch_001_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "materialization_evidence_status": ("MATERIALIZATION_PASS_PENDING_REPOSITORY_RECEIPT"),
    }


def test_operator_materialization_evidence_matches_accepted_dataset_lock_without_actions_ids() -> None:
    validator = load_validator()
    dataset_lock = json.loads(DATASET_LOCK_EVIDENCE_PATH.read_text(encoding="utf-8"))
    evidence = operator_materialization_evidence_fixture(dataset_lock)

    validator.validate_evidence_against_dataset_lock(evidence, dataset_lock)
