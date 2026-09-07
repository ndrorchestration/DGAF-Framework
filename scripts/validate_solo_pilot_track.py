#!/usr/bin/env python3
"""Validate the v0.7.6 Solo Pilot governance contract fail-closed."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/GOVERNANCE/SOLO_PILOT_TRACK_V0.7.6.json"
AUTHORITY = ROOT / "docs/GOVERNANCE/SOLO_EPOCH_AUTHORITY_V1.json"

EXPECTED_CONTROLS = {
    "exact_checked_out_commit_binding",
    "repository_bound_epoch_authorization",
    "explicit_pre_execution_freeze",
    "protected_blinding_key",
    "blinded_condition_identifiers",
    "keyed_trial_order",
    "canonical_180_cell_matrix_per_seed",
    "artifact_schema_validation",
    "sha256_sidecars",
    "runtime_ceiling",
    "durable_retention",
    "no_outcome_dependent_protocol_edit_without_refreeze",
}
EXPECTED_HIGH_ASSURANCE_BLOCKERS = {277, 295, 310, 316, 320}


def validate_manifest(document: dict) -> None:
    assert document.get("schema_version") == 2
    assert document.get("record_type") == "DGAF_PDMAL_V0_7_6_SOLO_PILOT_TRACK"
    assert document.get("status") == "EXPERIMENT_001_APPARATUS_FALSIFICATION_FUTURE_EPOCH_NOT_AUTHORIZED"
    assert document.get("protocol_version") == "0.7.6"
    assert document.get("execution_mode") == "solo_pilot"
    assert document.get("historical_experiment_id") == "PDMAL-SOLO-PILOT-V1"

    historical = document["historical_evidence"]
    assert historical == {
        "two_seed_qc_retained_observations": 360,
        "experiment_001_retained_observations": 9000,
        "experiment_001_classification": "APPARATUS_FALSIFICATION_EVIDENCE",
        "efficacy_eligible_observations": 0,
        "scientific_n_for_efficacy": 0,
    }

    future = document["future_epoch"]
    assert future == {
        "authorization_status": "NOT_GRANTED",
        "authority_record": "docs/GOVERNANCE/SOLO_EPOCH_AUTHORITY_V1.json",
        "blocking_issue": 369,
        "legacy_environment_self_authorization_sufficient": False,
        "historical_experiment_001_authority_reusable": False,
    }

    assert set(document["controls_retained"]) == EXPECTED_CONTROLS
    assert set(document["high_assurance_prerequisites_not_satisfied_by_solo_evidence"]) == EXPECTED_HIGH_ASSURANCE_BLOCKERS

    separation = document["track_separation"]
    assert separation == {
        "solo_does_not_satisfy_high_assurance_blockers": True,
        "high_assurance_track_preserved": True,
        "experiment_001_results_are_retained": True,
        "experiment_001_results_are_efficacy_eligible": False,
        "solo_results_are_independently_verified": False,
    }

    may = set(document["claim_ceiling"]["may_claim"])
    must_not = set(document["claim_ceiling"]["must_not_claim_without_separate_evidence"])
    assert "experiment 001 is apparatus-falsification evidence" in may
    assert "DGAF efficacy from experiment 001" in must_not
    assert "independent verification" in must_not
    assert "production readiness" in must_not


def validate_authority(document: dict) -> None:
    assert document.get("schema_version") == 1
    assert document.get("record_type") == "DGAF_PDMAL_SOLO_EPOCH_AUTHORITY"
    assert document.get("protocol_version") == "0.7.6"
    assert document.get("status") == "NOT_AUTHORIZED"
    assert document.get("epoch_id") is None
    assert document.get("frozen_commit_sha") is None
    assert document.get("scientific_n_increment_authorized") == 0
    assert document.get("historical_experiment_001_authority_reusable") is False
    assert document.get("legacy_environment_only_authorization_permitted") is False

    auth = document["authorization"]
    assert auth["type"] == "REPOSITORY_BOUND_EPOCH_AUTHORIZATION"
    assert auth["decision"] == "NOT_GRANTED"
    assert auth["authority_issue"] == 369
    assert auth["legacy_self_authorization_sufficient"] is False
    assert auth["required_runtime_env"] == {
        "PDMAL_SOLO_EPOCH_ID": "MUST_MATCH_AUTHORIZED_EPOCH_ID",
        "PDMAL_PROTOCOL_FROZEN": "1",
        "PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED": "1",
    }
    assert len(document["required_before_grant"]) >= 6


def self_test(manifest: dict, authority: dict) -> None:
    manifest_mutations = []

    changed = copy.deepcopy(manifest)
    changed["track_separation"]["experiment_001_results_are_efficacy_eligible"] = True
    manifest_mutations.append(changed)

    changed = copy.deepcopy(manifest)
    changed["future_epoch"]["authorization_status"] = "GRANTED"
    manifest_mutations.append(changed)

    changed = copy.deepcopy(manifest)
    changed["future_epoch"]["legacy_environment_self_authorization_sufficient"] = True
    manifest_mutations.append(changed)

    changed = copy.deepcopy(manifest)
    changed["historical_evidence"]["scientific_n_for_efficacy"] = 9000
    manifest_mutations.append(changed)

    for index, mutation in enumerate(manifest_mutations, start=1):
        try:
            validate_manifest(mutation)
        except (AssertionError, KeyError):
            continue
        raise AssertionError(f"manifest negative control {index} unexpectedly passed")

    authority_mutations = []

    changed = copy.deepcopy(authority)
    changed["status"] = "AUTHORIZED"
    authority_mutations.append(changed)

    changed = copy.deepcopy(authority)
    changed["authorization"]["decision"] = "GRANTED"
    authority_mutations.append(changed)

    changed = copy.deepcopy(authority)
    changed["authorization"]["legacy_self_authorization_sufficient"] = True
    authority_mutations.append(changed)

    changed = copy.deepcopy(authority)
    changed["scientific_n_increment_authorized"] = 9000
    authority_mutations.append(changed)

    for index, mutation in enumerate(authority_mutations, start=1):
        try:
            validate_authority(mutation)
        except (AssertionError, KeyError):
            continue
        raise AssertionError(f"authority negative control {index} unexpectedly passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    authority = json.loads(AUTHORITY.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    validate_authority(authority)
    if args.self_test:
        self_test(manifest, authority)
    print("solo pilot track: PASS (historical apparatus-falsification / future epoch fail-closed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
