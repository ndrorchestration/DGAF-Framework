#!/usr/bin/env python3
"""Fail-closed validator for the canonical PDMAL treatment-profile candidate."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "docs/governance/CANONICAL_PDMAL_TREATMENT_PROFILE_CANDIDATE_V1.json"
MODULE = ROOT / "experiments/pdmal_pilot/canonical_p30_qualification.py"
MIGRATION = ROOT / "docs/governance/LEGACY_APOGEE_RUNTIME_IDENTITY_MIGRATION_2026-09-07.json"


def validate() -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    migration = json.loads(MIGRATION.read_text(encoding="utf-8"))
    assert profile["record_type"] == "DGAF_CANONICAL_PDMAL_TREATMENT_PROFILE_CANDIDATE"
    assert profile["profile_id"] == "DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1"
    assert profile["empirical_authorization"] is False
    assert profile["scientific_n_increment"] == 0
    p30 = profile["canonical_p30"]
    assert p30["authority"] == "S035_P11_11Q_ATTESTATION"
    assert p30["location"] == "EXTERNAL_GOVERNANCE_PROMOTION_ATTESTATION"
    assert p30["per_turn_scoring"] is False
    assert p30["tgl_step"] == 8
    assert p30["step8_semantics"] == "VERIFY_EXTERNAL_QUALIFICATION_ARTIFACT"
    legacy = profile["legacy_runtime_gate"]
    assert legacy["id"] == "LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1"
    assert legacy["allowed_in_profile"] is False
    assert migration["legacy_runtime_gate"]["id"] == legacy["id"]
    assert profile["next_gate"]["new_canonical_empirical_epoch"] == "NOT_AUTHORIZED"
    forbidden = set(profile["forbidden_step8_inputs"])
    required_forbidden = {
        "empirical_outcomes", "ffcr", "agent_values", "topology", "failure_count",
        "runtime_confidence_scalar", "default_constant", "phi_constant",
        "synthetic_confidence_fixture",
    }
    assert forbidden == required_forbidden
    text = MODULE.read_text(encoding="utf-8")
    for token in required_forbidden:
        assert f'"{token}"' in text
    assert "build_qualification_verifier_hook" in text
    assert "verify_qualification_artifact" in text


if __name__ == "__main__":
    validate()
    print("Canonical treatment profile: PASS_NONEMPIRICAL_CANDIDATE")
