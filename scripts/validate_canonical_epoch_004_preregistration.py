#!/usr/bin/env python3
"""Fail-closed validator for canonical Solo empirical Epoch 004 preregistration.

Proposal validation only. This script never authorizes or executes empirical collection.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/experiment/CANONICAL_SOLO_EMPIRICAL_EPOCH_004_PREREGISTRATION.json"
ANALYSIS = ROOT / "experiments/pdmal_pilot/analysis.py"

EXPECTED_ANALYSIS_BLOB = "a269ed226b1d261663994fc3ef0e8a1a96da6cd3"
EXPECTED_ANALYSIS_CONFIG_SHA256 = "6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data, usedforsecurity=False).hexdigest()


def validate() -> None:
    d = json.loads(SPEC.read_text(encoding="utf-8"))
    assert d["record_type"] == "DGAF_CANONICAL_SOLO_EMPIRICAL_EPOCH_PREREGISTRATION"
    assert d["epoch_id"] == "PDMAL-SOLO-CANONICAL-EPOCH-004"
    assert d["status"] == "PROPOSAL_ONLY_NOT_AUTHORIZED"
    assert d["empirical_execution_authorized"] is False
    assert d["scientific_n_increment_at_preregistration"] == 0
    assert d["independent_verification"] is False

    treatment = d["canonical_treatment"]
    assert treatment["profile_id"] == "DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1"
    assert treatment["profile_merge_sha"] == "c8a07306d212e23cc5a4c1e0d98b7e8f47f45e21"
    assert treatment["qualification_merge_sha"] == "2fbd54454ad45df26cdd3b51793268ac3e597336"
    assert treatment["qualification_sha256"] == ("4d0346f6a05046f03ce5a399d1dd4de2d31b69f683988fe9af20802d2c062d78")
    assert treatment["qualification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    assert treatment["reachability_merge_sha"] == "621356297f803f0a3e8e3319d54878a5bb0282a5"
    assert treatment["reachability_run_id"] == 34176977560
    assert treatment["reachability_artifact_id"] == 10037645166
    assert treatment["reachability_artifact_digest"] == (
        "sha256:814222ba8fad2d1ef7dbd6d620fe0620f31e7a74c27d13b20f054c82efb90aa4"
    )
    assert treatment["required_tgl_steps"] == [1, 2, 3, 4, 5, 6, 8]

    matrix = d["matrix"]
    seeds = matrix["seeds"]
    assert matrix["seed_rule"] == "inclusive_integer_range_20261001_20261050"
    assert seeds == list(range(20261001, 20261051))
    assert len(seeds) == len(set(seeds)) == 50
    exp001 = set(range(20260819, 20260869))
    epoch003 = set(range(20260901, 20260951))
    assert not (set(seeds) & exp001)
    assert not (set(seeds) & epoch003)
    assert matrix["conditions"] == ["null", "simple", "static", "dgaf"]
    assert matrix["topologies"] == ["ring", "pdmal", "random_regular", "small_world", "complete"]
    assert matrix["failure_counts"] == [0, 1, 2, 3, 4, 5, 6, 8, 10]
    assert matrix["cells_per_seed"] == 180
    assert matrix["expected_total_observations"] == 9000

    analysis_bytes = ANALYSIS.read_bytes()
    assert git_blob_sha(analysis_bytes) == EXPECTED_ANALYSIS_BLOB
    primary = d["primary_analysis"]
    assert primary["statistical_source_blob_sha"] == EXPECTED_ANALYSIS_BLOB
    assert primary["analysis_config_sha256"] == EXPECTED_ANALYSIS_CONFIG_SHA256
    assert primary["bootstrap_resamples"] == 10000
    assert primary["bootstrap_seed"] == 20260823
    assert primary["alpha"] == 0.05

    controls = d["collection_controls"]
    assert controls["runner_status"] == "NOT_YET_IMPLEMENTED_OR_AUTHORIZED"
    assert controls["fresh_blinding_key_required"] is True
    assert controls["same_system_key_custody_is_independent"] is False
    assert controls["outcome_inspection_during_collection"] is False
    assert controls["dataset_lock_before_unblinding"] is True
    assert controls["separate_unblinding_authorization_required"] is True
    assert controls["historical_pooling_allowed"] is False
    assert controls["precollection_treatment_input_preflight_required"] is True
    assert controls["exact_frozen_commit_required"] is True
    assert controls["one_file_execution_authorization_required"] is True


if __name__ == "__main__":
    validate()
    print("CANONICAL_EPOCH_004_PREREGISTRATION_PASS_PROPOSAL_ONLY")
