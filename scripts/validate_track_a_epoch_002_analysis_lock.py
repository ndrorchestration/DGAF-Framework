#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json"
PROTOCOL = ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"
ANALYSIS = ROOT / "experiments/pdmal_pilot/track_a_epoch_002_analysis.py"
REQUIREMENTS_LOCK = ROOT / "experiments/pdmal_pilot/requirements-full-lock.txt"

EXPECTED_PROTOCOL_BLOB = "9668ec54e50c40b04d40cfa64b817950df4bbffa"
EXPECTED_ANALYSIS_BLOB = "d4495f7cdf211b974039ec0e66292dc62ea0881f"
EXPECTED_REQUIREMENTS_BLOB = "00c1f779e97030f9b25ae494642edb31b5b09de5"
EXPECTED_CONFIG_SHA256 = "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
EXPECTED_PREREG_MERGE = "eed3da6b0c4bae45f13871c45f42027da12ad36e"
EXPECTED_PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
EXPECTED_ALGORITHM_ID = "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
EXPECTED_SEEDS = tuple(range(20270201, 20270251))
EXPECTED_TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
EXPECTED_FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True).strip()


def load_analysis():
    name = "track_a_epoch_002_analysis"
    spec = importlib.util.spec_from_file_location(name, ANALYSIS)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def validate_records(lock: dict, protocol: dict, analysis) -> None:
    assert lock["record_type"] == "TRACK_A_EPOCH_002_ANALYSIS_LOCK"
    assert lock["schema_version"] == 1
    assert lock["controller_issue"] == 523
    assert lock["protocol_id"] == EXPECTED_PROTOCOL_ID
    assert lock["status"] == "ANALYSIS_IMPLEMENTATION_LOCKED_NONEMPIRICAL"
    assert lock["preregistration_merge_sha"] == EXPECTED_PREREG_MERGE
    assert lock["preregistration_blob_sha"] == EXPECTED_PROTOCOL_BLOB
    assert lock["analysis_blob_sha"] == EXPECTED_ANALYSIS_BLOB
    assert lock["analysis_config_sha256"] == EXPECTED_CONFIG_SHA256

    assert protocol["controller_issue"] == 523
    assert protocol["protocol_id"] == EXPECTED_PROTOCOL_ID
    assert protocol["status"] == "PROPOSAL_ONLY_NOT_AUTHORIZED"
    assert protocol["empirical_execution_authorized"] is False
    assert protocol["scientific_n_increment_at_preregistration"] == 0
    assert protocol["epoch_001_primary_analysis_status"] == "UNANALYZABLE_NOT_RUN"
    assert protocol["epoch_001_outcomes_used_for_successor_design"] is False

    assert analysis.PROTOCOL_ID == EXPECTED_PROTOCOL_ID
    assert analysis.ALGORITHM_ID == EXPECTED_ALGORITHM_ID
    assert analysis.SEEDS == EXPECTED_SEEDS
    assert analysis.TOPOLOGIES == EXPECTED_TOPOLOGIES
    assert analysis.FAILURE_COUNTS == EXPECTED_FAILURE_COUNTS
    assert analysis.BOOTSTRAP_RESAMPLES == 10000
    assert analysis.BOOTSTRAP_SEED == 20270251
    assert analysis.ALPHA == 0.05
    assert analysis.analysis_config_sha256() == EXPECTED_CONFIG_SHA256

    matrix = protocol["matrix"]
    primary = protocol["primary_analysis"]
    contract = lock["primary_contract"]
    assert tuple(matrix["seeds"]) == EXPECTED_SEEDS
    assert tuple(matrix["topologies"]) == EXPECTED_TOPOLOGIES
    assert tuple(matrix["failure_counts"]) == EXPECTED_FAILURE_COUNTS
    assert contract["seed_count"] == matrix["seed_count"] == 50
    assert contract["expected_total_records"] == matrix["expected_total_observations"] == 2250
    assert contract["endpoint"] == protocol["endpoint"]["field"] == "ffcr_success"
    assert contract["primary_topology"] == primary["primary_topology"] == "pdmal"
    assert contract["primary_comparator"] == primary["primary_comparator"] == "random_regular"
    assert contract["bootstrap"] == primary["bootstrap"] == "paired_seed_effects_percentile"
    assert contract["bootstrap_resamples"] == primary["bootstrap_resamples"] == 10000
    assert contract["bootstrap_seed"] == primary["bootstrap_seed"] == 20270251
    assert contract["alpha"] == primary["alpha"] == 0.05
    assert contract["confirmatory_test_count"] == protocol["multiplicity_policy"]["confirmatory_test_count"] == 1

    custody = protocol["blinding_and_custody"]
    assert custody["custody_class_required"] == "SAME_SYSTEM_NONINDEPENDENT"
    assert custody["precollection_recovery_drill_required"] is True
    assert custody["non_secret_recovery_receipt_required"] is True
    assert custody["real_private_key_must_originate_outside_repository"] is True

    history = protocol["historical_evidence_policy"]
    assert history["pool_track_a_epoch_001"] is False
    assert history["use_track_a_epoch_001_to_tune_successor"] is False

    gates = protocol["next_gates"]
    assert gates["successor_solo_custody_recovery_receipt"] == "REQUIRED_BEFORE_COLLECTION_AUTHORIZATION"
    assert gates["analysis_implementation_lock"] == "REVALIDATION_REQUIRED_BEFORE_COLLECTION"
    assert gates["runner_implementation"] == "REVALIDATION_OR_SUCCESSOR_BINDING_REQUIRED"
    assert gates["precollection_preflight"] == "REQUIRED"
    assert gates["exact_candidate_freeze"] == "NOT_ESTABLISHED"
    assert gates["collection_authorization"] == "SEPARATE_EXACT_COMMIT_REQUIRED"
    assert gates["empirical_execution"] == "NOT_AUTHORIZED"
    assert gates["high_assurance"] == "NOT_AUTHORIZED"
    assert gates["high_assurance_empirical_n"] == 0

    env = lock["environment"]
    assert env["python_version"] == "3.12.0"
    assert env["requirements_lock_path"] == "experiments/pdmal_pilot/requirements-full-lock.txt"
    assert env["requirements_lock_blob_sha"] == EXPECTED_REQUIREMENTS_BLOB
    assert env["install_policy"] == "PIP_REQUIRE_HASHES"
    assert lock["numpy_version"] == "2.5.1"
    assert lock["pytest_version"] == "9.0.3"

    boundaries = lock["boundaries"]
    assert boundaries["runner_implemented_by_this_lock"] is False
    assert boundaries["successor_custody_recovery_receipt_established"] is False
    assert boundaries["exact_candidate_freeze_established"] is False
    assert boundaries["collection_authorized"] is False
    assert boundaries["unblinding_authorized"] is False
    assert boundaries["primary_analysis_authorized"] is False
    assert boundaries["empirical_execution_authorized"] is False
    assert boundaries["scientific_n_increment"] == 0
    assert boundaries["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert boundaries["high_assurance"] == "NOT_AUTHORIZED_N0"


def main() -> None:
    assert git_blob(PROTOCOL) == EXPECTED_PROTOCOL_BLOB
    assert git_blob(ANALYSIS) == EXPECTED_ANALYSIS_BLOB
    assert git_blob(REQUIREMENTS_LOCK) == EXPECTED_REQUIREMENTS_BLOB
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    validate_records(lock, protocol, load_analysis())
    print("TRACK_A_EPOCH_002_ANALYSIS_LOCK_PASS_NONEMPIRICAL")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


if __name__ == "__main__":
    main()
