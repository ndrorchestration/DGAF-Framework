#!/usr/bin/env python3
"""Validate the v0.7.6 Solo Pilot governance contract fail-closed."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/GOVERNANCE/SOLO_PILOT_TRACK_V0.7.6.json"

EXPECTED_CONTROLS = {
    "exact_checked_out_commit_binding",
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
EXPECTED_BLOCKERS = {277, 295, 310, 316, 320}


def validate(document: dict) -> None:
    assert document.get("schema_version") == 1
    assert document.get("record_type") == "DGAF_PDMAL_V0_7_6_SOLO_PILOT_TRACK"
    assert document.get("status") == "AVAILABLE_NOT_EXECUTED"
    assert document.get("protocol_version") == "0.7.6"
    assert document.get("empirical_n_at_definition") == 0
    assert document.get("execution_mode") == "solo_pilot"
    assert document.get("experiment_id") == "PDMAL-SOLO-PILOT-V1"

    auth = document["authorization"]
    assert auth["type"] == "DEVELOPER_SELF_AUTHORIZATION"
    assert auth["required_env"] == {
        "PDMAL_PROTOCOL_FROZEN": "1",
        "PDMAL_SOLO_PILOT_AUTHORIZED": "1",
        "PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED": "1",
    }
    assert auth["forbidden_high_assurance_assertion"] == {"PDMAL_PILOT_AUTHORIZED": "1"}

    assert set(document["controls_retained"]) == EXPECTED_CONTROLS
    assert set(document["high_assurance_prerequisites_not_required_for_solo_execution"]) == EXPECTED_BLOCKERS

    separation = document["track_separation"]
    assert separation == {
        "solo_does_not_satisfy_high_assurance_blockers": True,
        "high_assurance_track_preserved": True,
        "solo_results_are_empirical": True,
        "solo_results_are_independently_verified": False,
    }

    may = set(document["claim_ceiling"]["may_claim"])
    must_not = set(document["claim_ceiling"]["must_not_claim_without_separate_evidence"])
    assert "developer-run empirical pilot" in may
    assert "actual Solo empirical N after successful retained execution" in may
    assert "independent verification" in must_not
    assert "real Confidential Space qualification" in must_not
    assert "production readiness" in must_not


def self_test(document: dict) -> None:
    mutations = []

    changed = copy.deepcopy(document)
    changed["track_separation"]["solo_results_are_independently_verified"] = True
    mutations.append(changed)

    changed = copy.deepcopy(document)
    changed["track_separation"]["solo_does_not_satisfy_high_assurance_blockers"] = False
    mutations.append(changed)

    changed = copy.deepcopy(document)
    changed["authorization"]["forbidden_high_assurance_assertion"] = {}
    mutations.append(changed)

    changed = copy.deepcopy(document)
    changed["controls_retained"].remove("protected_blinding_key")
    mutations.append(changed)

    changed = copy.deepcopy(document)
    changed["claim_ceiling"]["must_not_claim_without_separate_evidence"].remove("independent verification")
    mutations.append(changed)

    for index, mutation in enumerate(mutations, start=1):
        try:
            validate(mutation)
        except (AssertionError, KeyError):
            continue
        raise AssertionError(f"negative control {index} unexpectedly passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate(document)
    if args.self_test:
        self_test(document)
    print("solo pilot track: PASS (bounded/self-authorized/not-independent)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
