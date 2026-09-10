#!/usr/bin/env python3
"""Validate the Track A Epoch 002 runner without executing empirical work."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDMAL = ROOT / "experiments/pdmal_pilot"
CONTRACT = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json"
RUNNER = PDMAL / "run_track_a_epoch_002.py"
TESTS = PDMAL / "test_track_a_epoch_002_runner.py"
WORKFLOW = ROOT / ".github/workflows/track-a-epoch-002-runner.yml"

CUSTODY_CONTRACT = ROOT / "docs/experiment/TRACK_A_SUCCESSOR_SOLO_CUSTODY_CONTRACT.md"
CUSTODY_VALIDATOR = ROOT / "scripts/validate_track_a_successor_solo_custody_receipt.py"

EXPECTED_UPSTREAM_BLOBS = {
    (
        ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"
    ): "9668ec54e50c40b04d40cfa64b817950df4bbffa",
    ROOT / "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json": "26980e27185b3a77980204b2d46a4fdab7e5fc7e",
    PDMAL / "track_a_epoch_002_analysis.py": "d4495f7cdf211b974039ec0e66292dc62ea0881f",
    PDMAL / "requirements-full-lock.txt": "00c1f779e97030f9b25ae494642edb31b5b09de5",
    PDMAL / "task_engine.py": "90135e1c6dfccc3b56ffdc0dcb9eb50a0b2a5b05",
    PDMAL / "harness_contract.py": "bb97c54ddf087fef568b1b3c8f8df72c30dad11e",
    PDMAL / "topology_utils.py": "7ae92ba8a9ab964537e5dafa5e12de36b841391e",
    CUSTODY_CONTRACT: "c9b31ab6fa5d062e1dfec3dc33a46eb3642fee97",
    CUSTODY_VALIDATOR: "93423101961aa3e572539ad4767d32a7803cc92a",
}

FUTURE_ARTIFACTS = (
    ROOT / "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json",
)


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def load_runner():
    sys.path.insert(0, str(PDMAL))
    spec = importlib.util.spec_from_file_location("track_a_epoch_002_runner", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    for path, expected in EXPECTED_UPSTREAM_BLOBS.items():
        assert git_blob(path) == expected, f"upstream source drift: {path}"

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    runner = load_runner()

    assert contract["record_type"] == "TRACK_A_EPOCH_002_RUNNER_CONTRACT"
    assert contract["schema_version"] == 1
    assert contract["controller_issue"] == 523
    assert contract["status"] == "RUNNER_BOUND_NOT_AUTHORIZED"
    assert contract["protocol_id"] == "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
    assert contract["epoch_id"] == "TRACK_A_EPOCH_002"
    assert contract["algorithm_id"] == "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"

    bindings = contract["source_bindings"]
    assert bindings["successor_custody_contract_blob_sha"] == EXPECTED_UPSTREAM_BLOBS[CUSTODY_CONTRACT]
    assert bindings["successor_custody_receipt_validator_blob_sha"] == EXPECTED_UPSTREAM_BLOBS[CUSTODY_VALIDATOR]

    identity = contract["identity_policy"]
    assert identity["self_referential_blob_pins_allowed"] is False
    assert identity["runner_contract_test_workflow_self_hash_cycle_allowed"] is False
    assert identity["runner_identity_is_bound_later_by_exact_candidate_freeze"] is True
    assert identity["protected_source_drift_after_freeze_prohibited"] is True

    assert runner.PROTOCOL_ID == contract["protocol_id"]
    assert runner.EPOCH_ID == contract["epoch_id"]
    assert runner.ALGORITHM_ID == contract["algorithm_id"]
    assert runner.MODE == "track_a_epoch_002"
    assert runner.SEEDS == tuple(range(20270201, 20270251))
    assert runner.TOPOLOGIES == (
        "ring",
        "pdmal",
        "random_regular",
        "small_world",
        "complete",
    )
    assert runner.FAILURE_COUNTS == (0, 1, 2, 3, 4, 5, 6, 8, 10)
    assert runner.EXPECTED_CELLS_PER_SEED == 45
    assert runner.EXPECTED_TOTAL == 2250
    assert runner.CONDITION == "null"

    matrix = contract["matrix"]
    assert tuple(matrix["seeds"]) == runner.SEEDS
    assert tuple(matrix["topologies"]) == runner.TOPOLOGIES
    assert tuple(matrix["failure_counts"]) == runner.FAILURE_COUNTS
    assert matrix["cells_per_seed"] == 45
    assert matrix["expected_total_observations"] == 2250
    assert matrix["historical_epoch_001_pooling_allowed"] is False
    assert matrix["historical_epoch_004_substitution_allowed"] is False

    canonical = tuple((topology, failure) for topology in runner.TOPOLOGIES for failure in runner.FAILURE_COUNTS)
    keyed = runner.ordered_matrix_cells(runner.SEEDS[0], b"validation-only-secret-material!!")
    assert len(keyed) == len(set(keyed)) == 45
    assert set(keyed) == set(canonical)
    assert keyed != canonical

    endpoint = contract["endpoint"]
    assert endpoint["field"] == "ffcr_success"
    assert endpoint["type"] == "strict_boolean"
    assert endpoint["boolean_coercion_allowed"] is False
    assert endpoint["reconstruction_or_imputation_allowed"] is False

    custody = contract["custody_precondition"]
    assert custody["receipt_must_validate"] is True
    assert custody["receipt_schema_version_required"] == 2
    assert custody["legacy_receipt_authorizes_successor_collection"] is False
    assert custody["recovery_drill_must_pass"] is True
    assert custody["each_recorded_backup_recovery_must_pass"] is True
    assert custody["distinct_backup_storage_classes_required"] is True
    assert custody["custody_class_required"] == "SAME_SYSTEM_NONINDEPENDENT"
    assert custody["independent_custody_required"] is False
    assert custody["minimum_distinct_encrypted_user_controlled_backups"] == 2
    assert custody["receipt_blob_sha_must_be_bound_by_preflight"] is True
    assert custody["certificate_blob_sha_must_be_bound_by_preflight"] is True
    assert custody["certificate_fingerprint_must_be_bound_by_preflight_and_authorization"] is True
    assert custody["custody_receipt_authorizes_collection"] is False

    expected_order = [
        "TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT",
        "TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT",
        "TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST",
        "TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET",
        "TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION",
        "TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION",
    ]
    assert contract["successor_gate_chain"]["order"] == expected_order

    for path in FUTURE_ARTIFACTS:
        assert not path.exists(), f"runner PR must not contain future artifact: {path}"

    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "github.event.pull_request.head.sha" in workflow
    assert "Prove checkout is exact PR head" in workflow
    assert "Prove custody and successor gates are absent" in workflow
    assert "SCIENTIFIC_N_INCREMENT=0" in workflow
    assert "run_track_a_epoch_002.py --execute" not in workflow

    authorization = contract["authorization"]
    assert authorization["pr_validation_can_authorize"] is False
    assert authorization["collection_authorized"] is False
    assert authorization["unblinding_authorized"] is False
    assert authorization["primary_analysis_authorized"] is False
    assert authorization["high_assurance_authorized"] is False
    assert contract["scientific_n_increment"] == 0
    assert contract["track_a_freeze"] == "NOT_ESTABLISHED"
    assert contract["successor_collection"] == "NOT_AUTHORIZED"
    assert contract["primary_analysis"] == "NOT_AUTHORIZED"
    assert contract["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert contract["high_assurance"] == "NOT_AUTHORIZED_N0"

    print("TRACK_A_EPOCH_002_RUNNER_BINDING=PASS_NONEMPIRICAL")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
