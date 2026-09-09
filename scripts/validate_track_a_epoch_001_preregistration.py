#!/usr/bin/env python3
"""Fail-closed validator for Track A topology-robustness Epoch 001 preregistration.

Proposal validation only. This script cannot authorize or execute empirical collection.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json"

BOUND_BLOBS = {
    ROOT / "docs/governance/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1.json":
        "339d9ada4978ffd0c1eee67c310323f1e7fdc06a",
    ROOT / "docs/qa/APOGEE_11Q_PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1_S078.json":
        "217028dc03aad6eb6a1a13cb6e32418782c43b08",
    ROOT / "docs/governance/TRACK_A_NONEMPIRICAL_MATRIX_ADJUDICATION_V1.json":
        "26cb5817283727bac3c51135384810e850ce65e8",
}


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def validate() -> None:
    d = json.loads(SPEC.read_text(encoding="utf-8"))

    assert d["record_type"] == "TRACK_A_TOPOLOGY_ROBUSTNESS_EMPIRICAL_PREREGISTRATION"
    assert d["controller_issue"] == 410
    assert d["protocol_id"] == "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
    assert d["status"] == "PROPOSAL_ONLY_NOT_AUTHORIZED"
    assert d["verification_class"] == "DEVELOPER_PREREGISTERED_NONINDEPENDENT"
    assert d["independent_verification"] is False
    assert d["empirical_execution_authorized"] is False
    assert d["scientific_n_increment_at_preregistration"] == 0

    for path, expected in BOUND_BLOBS.items():
        assert git_blob(path) == expected, f"bound source drift: {path}"

    b = d["source_bindings"]
    assert b["architecture_merge_sha"] == "5e4f00a065c00cefec0b3a79c32b88a5f36a55c2"
    assert b["profile_merge_sha"] == "b1e333ee9f9e0a4da78788e5ff019603296888eb"
    assert b["qualification_merge_sha"] == "647f612a2412818dca0d632229f352e857e1187e"
    assert b["adjudication_merge_sha"] == "ccabc065d0c1d183e1954ea36a947289fb084831"
    assert b["profile_id"] == "PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1"
    assert b["retained_structural_artifact_id"] == 10041800252
    assert b["retained_structural_archive_digest"] == "sha256:629ee0be7a48606685f2452800ab4e482611fb45f7268d881e934488e1c1c1d5"
    assert b["retained_structural_payload_sha256"] == "e51497d150530d983f94002d23a21608be9135ca300d29a47b126ed184fdc489"

    alg = d["algorithm"]
    assert alg == {
        "public_id": "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1",
        "alpha": 0.5,
        "condition_axis": False,
        "dgaf_semantic_gate_path": False,
    }

    matrix = d["matrix"]
    assert matrix["topologies"] == ["ring", "pdmal", "random_regular", "small_world", "complete"]
    assert matrix["failure_counts"] == [0, 1, 2, 3, 4, 5, 6, 8, 10]
    assert matrix["seed_rule"] == "inclusive_integer_range_20270101_20270150"
    assert matrix["seeds"] == list(range(20270101, 20270151))
    assert len(matrix["seeds"]) == len(set(matrix["seeds"])) == 50
    prior = (
        set(range(20260819, 20260869))
        | set(range(20260901, 20260951))
        | set(range(20261001, 20261051))
        | {20261201, 20261202}
    )
    assert not (set(matrix["seeds"]) & prior)
    assert matrix["seed_count"] == 50
    assert matrix["cells_per_seed"] == 45
    assert matrix["expected_total_observations"] == 2250

    endpoint = d["endpoint"]
    assert endpoint["field"] == "ffcr_success"
    assert endpoint["type"] == "boolean"
    assert endpoint["success_definition"] == "pre_existing_fixed_convergence_contract"
    assert endpoint["endpoint_changes_after_freeze_allowed"] is False

    primary = d["primary_analysis"]
    assert primary["primary_topology"] == "pdmal"
    assert primary["primary_comparator"] == "random_regular"
    assert primary["bootstrap"] == "paired_seed_effects_percentile"
    assert primary["bootstrap_resamples"] == 10000
    assert primary["bootstrap_seed"] == 20270151
    assert primary["confidence_interval"] == "two_sided_95_percentile"
    assert primary["alpha"] == 0.05
    assert primary["directional_support_rule"] == "estimate_gt_0_and_two_sided_95pct_ci_lower_gt_0"
    assert primary["directional_negative_rule"] == "estimate_lt_0_and_two_sided_95pct_ci_upper_lt_0"

    mult = d["multiplicity_policy"]
    assert mult["confirmatory_family"] == ["pdmal_vs_random_regular"]
    assert mult["confirmatory_test_count"] == 1
    assert mult["other_topology_comparisons"] == "EXPLORATORY_ONLY"
    assert mult["failure_count_specific_effects"] == "EXPLORATORY_ONLY"
    assert mult["confirmatory_relabeling_from_exploratory_results"] is False

    sample = d["sample_size_rationale"]
    assert sample["paired_seed_units"] == 50
    assert sample["power_claim"] == "NONE"

    qc = d["prospective_qc"]
    assert qc["require_exact_seed_count"] == 50
    assert qc["require_exact_topology_count"] == 5
    assert qc["require_exact_failure_count_count"] == 9
    assert qc["require_exact_total_observations"] == 2250
    assert qc["require_one_record_per_seed_topology_failure_cell"] is True
    assert qc["require_no_duplicate_cells"] is True
    assert qc["require_boolean_ffcr_success"] is True
    assert qc["outcome_based_exclusion_allowed"] is False
    assert qc["missing_cell_policy"] == "FAIL_CLOSED_NO_CONFIRMATORY_ANALYSIS"

    blind = d["blinding_and_custody"]
    assert blind["analysis_label_blinding_required"] is True
    assert blind["full_topology_concealment_claimed"] is False
    assert blind["fresh_mapping_key_after_protocol_freeze"] is True
    assert blind["dataset_and_key_separate"] is True
    assert blind["same_developer_custody_is_independent"] is False
    assert blind["dataset_structural_lock_before_key_release"] is True
    assert blind["separate_unblinding_authorization_required"] is True
    assert blind["outcome_inspection_before_dataset_lock"] is False

    hist = d["historical_evidence_policy"]
    assert all(hist[k] is False for k in (
        "pool_experiment_001",
        "pool_epoch_003",
        "pool_epoch_004",
        "pool_structural_diagnostic_seeds",
        "historical_outcomes_may_tune_endpoint_or_seed_panel",
    ))

    ceiling = d["claim_ceiling"]
    assert ceiling["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert ceiling["integrated_track_c"] == "NOT_ESTABLISHED"
    assert ceiling["independent_validation"] == "NOT_ESTABLISHED"
    assert ceiling["high_assurance"] == "NOT_AUTHORIZED_N0"

    gates = d["next_gates"]
    assert gates["analysis_implementation_lock"] == "REQUIRED_BEFORE_COLLECTION"
    assert gates["runner_implementation"] == "SEPARATE_PR_REQUIRED"
    assert gates["precollection_preflight"] == "REQUIRED"
    assert gates["exact_candidate_freeze"] == "NOT_ESTABLISHED"
    assert gates["collection_authorization"] == "SEPARATE_EXACT_COMMIT_REQUIRED"
    assert gates["empirical_execution"] == "NOT_AUTHORIZED"
    assert gates["high_assurance"] == "NOT_AUTHORIZED"
    assert gates["high_assurance_empirical_n"] == 0


if __name__ == "__main__":
    validate()
    print("TRACK_A_EPOCH_001_PREREGISTRATION_PASS_PROPOSAL_ONLY")
