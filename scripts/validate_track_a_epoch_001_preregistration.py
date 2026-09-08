#!/usr/bin/env python3
"""Fail-closed validator for Track A topology-robustness Epoch 001 preregistration.

Proposal validation only. This script never authorizes or executes empirical
collection.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json"
PROFILE = ROOT / "docs/governance/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1.json"
ADJUDICATION = ROOT / "docs/governance/TRACK_A_NONEMPIRICAL_MATRIX_ADJUDICATION_V1.json"

BOUND_BLOBS = {
    "docs/governance/WORKLOAD_SPECIFIC_DGAF_EVALUATION_TRACKS_V1.md": "7108829fdb8d0c86548762b9f548276a3a302d38",
    "docs/governance/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1.json": "339d9ada4978ffd0c1eee67c310323f1e7fdc06a",
    "docs/qa/APOGEE_11Q_PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1_S078.json": "217028dc03aad6eb6a1a13cb6e32418782c43b08",
    "docs/governance/TRACK_A_NONEMPIRICAL_MATRIX_ADJUDICATION_V1.json": "26cb5817283727bac3c51135384810e850ce65e8",
    "experiments/pdmal_pilot/task_engine.py": "90135e1c6dfccc3b56ffdc0dcb9eb50a0b2a5b05",
    "experiments/pdmal_pilot/harness_contract.py": "bb97c54ddf087fef568b1b3c8f8df72c30dad11e",
}

TOPOLOGIES = ["ring", "pdmal", "random_regular", "small_world", "complete"]
FAILURE_COUNTS = [0, 1, 2, 3, 4, 5, 6, 8, 10]
SEEDS = list(range(20261301, 20261351))
HISTORICAL_SEEDS = (
    set(range(20260819, 20260869))
    | set(range(20260901, 20260951))
    | set(range(20261001, 20261051))
    | {20261101, 20261102, 20261201, 20261202}
)
FORBIDDEN_OBSERVED_RESULT_KEYS = {
    "observed_effect",
    "observed_ci_lower",
    "observed_ci_upper",
    "observed_p_value",
    "completed_observations",
    "primary_result",
    "empirical_result",
}


def git_blob(path: str) -> str:
    return subprocess.check_output(
        ["git", "hash-object", path],
        cwd=ROOT,
        text=True,
    ).strip()


def reject_observed_results(value: Any) -> None:
    if isinstance(value, dict):
        forbidden = FORBIDDEN_OBSERVED_RESULT_KEYS & set(value)
        assert not forbidden, f"preregistration contains observed-result fields: {sorted(forbidden)}"
        for child in value.values():
            reject_observed_results(child)
    elif isinstance(value, list):
        for child in value:
            reject_observed_results(child)


def main() -> int:
    d = json.loads(SPEC.read_text(encoding="utf-8"))
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    adjudication = json.loads(ADJUDICATION.read_text(encoding="utf-8"))

    assert d["record_type"] == "TRACK_A_TOPOLOGY_ROBUSTNESS_EMPIRICAL_EPOCH_PREREGISTRATION"
    assert d["schema_version"] == 1
    assert d["controller_issue"] == 410
    assert d["epoch_id"] == "TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
    assert d["status"] == "PROPOSAL_ONLY_NOT_AUTHORIZED"
    assert d["verification_class"] == "DEVELOPER_PREREGISTERED_NONINDEPENDENT"
    assert d["independent_verification"] is False
    assert d["empirical_execution_authorized"] is False
    assert d["scientific_n_increment_at_preregistration"] == 0
    reject_observed_results(d)

    for path, expected in BOUND_BLOBS.items():
        actual = git_blob(path)
        assert actual == expected, f"bound source drift: {path}: {actual} != {expected}"

    bindings = d["source_bindings"]
    assert bindings["architecture_merge_sha"] == "5e4f00a065c00cefec0b3a79c32b88a5f36a55c2"
    assert bindings["profile_merge_sha"] == "b1e333ee9f9e0a4da78788e5ff019603296888eb"
    assert bindings["qualification_merge_sha"] == "647f612a2412818dca0d632229f352e857e1187e"
    assert bindings["adjudication_merge_sha"] == "ccabc065d0c1d183e1954ea36a947289fb084831"
    for path, expected in BOUND_BLOBS.items():
        key = {
            "docs/governance/WORKLOAD_SPECIFIC_DGAF_EVALUATION_TRACKS_V1.md": "architecture_blob_sha",
            "docs/governance/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1.json": "profile_blob_sha",
            "docs/qa/APOGEE_11Q_PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1_S078.json": "qualification_blob_sha",
            "docs/governance/TRACK_A_NONEMPIRICAL_MATRIX_ADJUDICATION_V1.json": "adjudication_blob_sha",
            "experiments/pdmal_pilot/task_engine.py": "task_engine_blob_sha",
            "experiments/pdmal_pilot/harness_contract.py": "harness_blob_sha",
        }[path]
        assert bindings[key] == expected

    assert profile["profile_id"] == "PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1"
    assert profile["algorithm"]["public_id"] == "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
    assert profile["algorithm"]["alpha"] == 0.5
    assert profile["algorithm"]["public_condition_axis"] is False
    assert profile["algorithm"]["dgaf_semantic_gate_path"] is False
    assert profile["diagnostic_probe"]["topologies"] == TOPOLOGIES
    assert profile["diagnostic_probe"]["failure_counts"] == FAILURE_COUNTS

    assert adjudication["profile_id"] == profile["profile_id"]
    assert adjudication["algorithm_id"] == profile["algorithm"]["public_id"]
    assert adjudication["adjudication_result"] == "PASS_ADVANCE_TO_PROSPECTIVE_EMPIRICAL_PROTOCOL_PROPOSAL"
    assert adjudication["empirical_evidence"] is False
    assert adjudication["scientific_n_increment"] == 0
    assert adjudication["next_gate"]["required"] == "TRACK_A_PROSPECTIVE_EMPIRICAL_PROTOCOL_PROPOSAL"
    assert adjudication["next_gate"]["empirical_execution"] == "NOT_AUTHORIZED"
    assert adjudication["next_gate"]["freeze_status"] == "NOT_ESTABLISHED"

    factor = d["treatment_factor"]
    assert factor["algorithm_id"] == profile["algorithm"]["public_id"]
    assert factor["algorithm_alpha"] == 0.5
    assert factor["primary_topology"] == "pdmal"
    assert factor["primary_comparator"] == "random_regular"
    assert factor["descriptive_topologies"] == ["ring", "small_world", "complete"]
    assert factor["prohibited_treatment_labels"] == ["dgaf", "full_dgaf", "canonical_dgaf"]
    assert factor["public_condition_axis"] is False
    assert factor["dgaf_semantic_gate_path"] is False
    assert d["directional_hypothesis"] == "mean_seed_paired_ffcr_pdmal_minus_random_regular > 0"

    endpoint = d["endpoint"]
    assert endpoint["primary_field"] == "ffcr_success"
    assert endpoint["source_property"] == "ConsensusTrialResult.consensus_success"
    assert endpoint["consensus_threshold"] == 0.01
    assert endpoint["iterations"] == 100
    assert endpoint["convergence_early_stopping"] is False
    assert endpoint["missing_outcome_policy"] == "FAIL_CLOSED_NO_RECONSTRUCTION_OR_IMPUTATION"

    matrix = d["matrix"]
    seeds = matrix["seeds"]
    assert matrix["topologies"] == TOPOLOGIES
    assert matrix["failure_counts"] == FAILURE_COUNTS
    assert matrix["node_count"] == 20
    assert matrix["seed_rule"] == "inclusive_integer_range_20261301_20261350"
    assert seeds == SEEDS
    assert len(seeds) == len(set(seeds)) == matrix["seeds_count"] == 50
    assert not (set(seeds) & HISTORICAL_SEEDS)
    assert matrix["historical_seed_ranges_excluded"] == [
        "20260819..20260868",
        "20260901..20260950",
        "20261001..20261050",
    ]
    assert matrix["diagnostic_seeds_excluded"] == [20261101, 20261102, 20261201, 20261202]
    assert matrix["cells_per_seed"] == len(TOPOLOGIES) * len(FAILURE_COUNTS) == 45
    assert matrix["primary_pair_cells_per_seed"] == 2 * len(FAILURE_COUNTS) == 18
    assert matrix["expected_total_observations"] == len(SEEDS) * 45 == 2250

    sample = d["sample_size"]
    assert sample["planned_paired_seed_n"] == 50
    assert sample["no_outcome_dependent_resizing"] is True
    assert sample["no_outcome_dependent_stopping"] is True
    assert sample["replacement_seeds_allowed"] is False
    assert "not a formal power or minimum-detectable-effect guarantee" in sample["rationale"]

    analysis = d["primary_analysis"]
    assert analysis["analysis_implementation_status"] == "NOT_YET_IMPLEMENTED_OR_BOUND"
    assert analysis["statistical_unit"] == "root_seed"
    assert analysis["paired_effect"] == "FFCR_pdmal(seed) - FFCR_random_regular(seed)"
    assert analysis["estimand"] == "equal_weight_mean_seed_paired_ffcr_difference"
    assert analysis["bootstrap"] == "paired_seed_effects_percentile"
    assert analysis["bootstrap_resamples"] == 10000
    assert analysis["bootstrap_seed"] == 20261399
    assert analysis["bootstrap_seed"] not in set(SEEDS)
    assert analysis["alpha"] == 0.05
    assert analysis["confidence_interval"] == "TWO_SIDED_95_PERCENTILE"
    assert analysis["directional_support_rule"] == "estimate_gt_0_and_two_sided_95pct_ci_lower_gt_0"
    assert analysis["p_value_required"] is False
    assert analysis["multiplicity_policy"].startswith("ONE_CONFIRMATORY_CONTRAST_NO_ADJUSTMENT")

    qc = d["prospective_qc"]
    assert qc["expected_unique_cells"] == 2250
    assert qc["complete_seed_required_for_primary_analysis"] is True
    assert qc["duplicate_cells_allowed"] is False
    assert qc["silent_cell_repair_allowed"] is False
    assert qc["silent_seed_drop_allowed"] is False
    assert qc["replacement_seed_allowed"] is False
    assert qc["outcome_dependent_qc_changes_allowed"] is False

    blind = d["blinding_and_custody"]
    assert blind["fresh_blinding_key_required"] is True
    assert blind["pre_unblinding_topology_labels"] == "OPAQUE_IDS_ONLY"
    assert blind["protected_mapping_required"] is True
    assert blind["plaintext_topology_in_public_pre_unblinding_dataset"] is False
    assert blind["topology_fingerprint_in_public_pre_unblinding_dataset"] is False
    assert blind["outcome_inspection_during_collection"] is False
    assert blind["dataset_hash_lock_before_unblinding"] is True
    assert blind["separate_unblinding_authorization_required"] is True
    assert blind["same_operator_key_custody_is_independent"] is False
    assert blind["independence_classification"] == "NONINDEPENDENT_UNLESS_SEPARATELY_ESTABLISHED"

    controls = d["collection_controls"]
    assert controls["runner_status"] == "NOT_YET_IMPLEMENTED"
    assert controls["runner_must_be_separately_reviewed"] is True
    assert controls["runner_must_bind_exact_preregistration_blob"] is True
    assert controls["analysis_must_be_separately_implemented_and_bound"] is True
    assert controls["environment_reproducibility_evidence_required"] is True
    assert controls["negative_authorization_tests_required"] is True
    assert controls["historical_pooling_allowed"] is False
    assert controls["exact_frozen_commit_required"] is True
    assert controls["freeze_status"] == "NOT_ESTABLISHED"
    assert controls["one_file_execution_authorization_required"] is True
    assert controls["collection_authorization"] == "NOT_AUTHORIZED"

    ceiling = d["claim_ceiling"]
    assert ceiling["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert ceiling["integrated_track_c"] == "NOT_AUTHORIZED"
    assert ceiling["independent_validation"] == "NOT_ESTABLISHED"
    assert ceiling["high_assurance"] == "NOT_AUTHORIZED_N0"

    next_gate = d["next_gate"]
    assert next_gate["required"] == "SEPARATELY_REVIEWED_TRACK_A_EMPIRICAL_RUNNER_AND_ANALYSIS_IMPLEMENTATION"
    assert next_gate["freeze_status"] == "NOT_ESTABLISHED"
    assert next_gate["empirical_execution"] == "NOT_AUTHORIZED"
    assert next_gate["scientific_n_increment"] == 0

    print("TRACK_A_EPOCH_001_PREREGISTRATION_PASS_PROPOSAL_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
