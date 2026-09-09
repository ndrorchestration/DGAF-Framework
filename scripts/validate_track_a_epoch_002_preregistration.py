#!/usr/bin/env python3
"""Fail-closed validator for Track A topology-robustness Epoch 002 preregistration.

This validator proves prospective continuity and seed separation only. It cannot create
custody material, freeze a candidate, authorize empirical collection, or increase N.
"""
from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json"
SUCCESSOR = ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"
EXPECTED_PREDECESSOR_BLOB = "52148950ff054a407c2e6b5cf36103695cf96474"
EXPECTED_BASE_MAIN = "9ca7ef3d70acadc1dee90ebc2c491f91974eb992"


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def _without_bootstrap_seed(primary: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(primary)
    result.pop("bootstrap_seed")
    return result


def validate_records(successor: dict[str, Any], predecessor: dict[str, Any], predecessor_blob: str) -> None:
    assert predecessor_blob == EXPECTED_PREDECESSOR_BLOB, "predecessor preregistration blob drift"

    assert successor["record_type"] == predecessor["record_type"] == "TRACK_A_TOPOLOGY_ROBUSTNESS_EMPIRICAL_PREREGISTRATION"
    assert successor["schema_version"] == 2
    assert successor["controller_issue"] == 523
    assert successor["protocol_id"] == "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
    assert successor["protocol_id"] != predecessor["protocol_id"]
    assert successor["predecessor_protocol_id"] == predecessor["protocol_id"]
    assert successor["status"] == "PROPOSAL_ONLY_NOT_AUTHORIZED"
    assert successor["verification_class"] == "DEVELOPER_PREREGISTERED_NONINDEPENDENT"
    assert successor["independent_verification"] is False
    assert successor["empirical_execution_authorized"] is False
    assert successor["scientific_n_increment_at_preregistration"] == 0
    assert successor["epoch_001_primary_analysis_status"] == "UNANALYZABLE_NOT_RUN"
    assert successor["epoch_001_outcomes_used_for_successor_design"] is False

    bindings = successor["source_bindings"]
    assert bindings["proposal_base_main_sha"] == EXPECTED_BASE_MAIN
    assert bindings["predecessor_preregistration_blob_sha"] == EXPECTED_PREDECESSOR_BLOB
    for key in (
        "architecture_merge_sha",
        "profile_merge_sha",
        "qualification_merge_sha",
        "adjudication_merge_sha",
        "profile_id",
        "profile_blob_sha",
        "qualification_blob_sha",
        "adjudication_blob_sha",
        "retained_structural_artifact_id",
        "retained_structural_archive_digest",
        "retained_structural_payload_sha256",
    ):
        assert bindings[key] == predecessor["source_bindings"][key], f"source-binding drift: {key}"

    # Scientific design is inherited without outcome-driven modification.
    assert successor["research_question"] == predecessor["research_question"]
    assert successor["directional_hypothesis"] == predecessor["directional_hypothesis"]
    assert successor["algorithm"] == predecessor["algorithm"]
    assert successor["endpoint"] == predecessor["endpoint"]
    assert successor["multiplicity_policy"] == predecessor["multiplicity_policy"]
    assert successor["sample_size_rationale"] == predecessor["sample_size_rationale"]
    assert successor["prospective_qc"] == predecessor["prospective_qc"]
    assert successor["claim_ceiling"] == predecessor["claim_ceiling"]
    assert _without_bootstrap_seed(successor["primary_analysis"]) == _without_bootstrap_seed(predecessor["primary_analysis"])

    old_matrix = predecessor["matrix"]
    new_matrix = successor["matrix"]
    assert new_matrix["topologies"] == old_matrix["topologies"]
    assert new_matrix["failure_counts"] == old_matrix["failure_counts"]
    assert new_matrix["seed_rule"] == "inclusive_integer_range_20270201_20270250"
    assert new_matrix["seeds"] == list(range(20270201, 20270251))
    assert len(new_matrix["seeds"]) == len(set(new_matrix["seeds"])) == 50
    assert new_matrix["predecessor_epoch_seeds_excluded"] == old_matrix["seeds"]
    assert new_matrix["historical_seed_ranges_excluded"] == old_matrix["historical_seed_ranges_excluded"]
    assert new_matrix["diagnostic_seeds_excluded"] == old_matrix["diagnostic_seeds_excluded"]
    assert new_matrix["seed_count"] == old_matrix["seed_count"] == 50
    assert new_matrix["cells_per_seed"] == old_matrix["cells_per_seed"] == 45
    assert new_matrix["expected_total_observations"] == old_matrix["expected_total_observations"] == 2250

    excluded = (
        set(old_matrix["seeds"])
        | set(range(20260819, 20260869))
        | set(range(20260901, 20260951))
        | set(range(20261001, 20261051))
        | set(old_matrix["diagnostic_seeds_excluded"])
    )
    assert not (set(new_matrix["seeds"]) & excluded), "successor seed collision"
    bootstrap_seed = successor["primary_analysis"]["bootstrap_seed"]
    assert bootstrap_seed == 20270251
    assert bootstrap_seed not in set(new_matrix["seeds"]) | excluded

    old_blinding = predecessor["blinding_and_custody"]
    new_blinding = successor["blinding_and_custody"]
    for key, value in old_blinding.items():
        assert new_blinding[key] == value, f"blinding/custody scientific drift: {key}"
    assert new_blinding["custody_class_required"] == "SAME_SYSTEM_NONINDEPENDENT"
    assert new_blinding["precollection_recovery_drill_required"] is True
    assert new_blinding["non_secret_recovery_receipt_required"] is True
    assert new_blinding["real_private_key_must_originate_outside_repository"] is True

    old_history = predecessor["historical_evidence_policy"]
    new_history = successor["historical_evidence_policy"]
    for key, value in old_history.items():
        assert new_history[key] == value is False, f"historical policy drift: {key}"
    assert new_history["pool_track_a_epoch_001"] is False
    assert new_history["use_track_a_epoch_001_to_tune_successor"] is False

    gates = successor["next_gates"]
    assert gates["successor_solo_custody_recovery_receipt"] == "REQUIRED_BEFORE_COLLECTION_AUTHORIZATION"
    assert gates["analysis_implementation_lock"] == "REVALIDATION_REQUIRED_BEFORE_COLLECTION"
    assert gates["runner_implementation"] == "REVALIDATION_OR_SUCCESSOR_BINDING_REQUIRED"
    assert gates["precollection_preflight"] == "REQUIRED"
    assert gates["exact_candidate_freeze"] == "NOT_ESTABLISHED"
    assert gates["collection_authorization"] == "SEPARATE_EXACT_COMMIT_REQUIRED"
    assert gates["empirical_execution"] == "NOT_AUTHORIZED"
    assert gates["high_assurance"] == "NOT_AUTHORIZED"
    assert gates["high_assurance_empirical_n"] == 0


def validate() -> None:
    predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
    successor = json.loads(SUCCESSOR.read_text(encoding="utf-8"))
    validate_records(successor, predecessor, git_blob(PREDECESSOR))


if __name__ == "__main__":
    validate()
    print("TRACK_A_EPOCH_002_PREREGISTRATION=PASS_PROPOSAL_ONLY")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
