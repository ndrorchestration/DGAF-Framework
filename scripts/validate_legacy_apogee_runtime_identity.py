#!/usr/bin/env python3
"""Fail-closed validator for the legacy Apogee runtime identity migration."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "docs/governance/LEGACY_APOGEE_RUNTIME_IDENTITY_MIGRATION_2026-09-07.json"
RECONCILIATION = ROOT / "docs/governance/P30_AUTHORITY_RECONCILIATION_2026-09-07.json"

LEGACY_ID = "LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1"
CANONICAL_AUTHORITY = "S035_P11_11Q_ATTESTATION"
CANONICAL_LOCATION = "EXTERNAL_GOVERNANCE_PROMOTION_ATTESTATION"
RETIRED = "RETIRED_FROM_CANONICAL_DGAF_TREATMENT"
REQUIRED_HISTORICAL_SURFACES = {
    "components/ensemble_v17.py",
    "experiments/pdmal_pilot/pdmaltgl_gate_binding.py",
    "experiments/pdmal_pilot/dgaf_tgl_adapter.py",
    "experiments/pdmal_pilot/p30_remediation_diagnostic.py",
    "experiments/pdmal_pilot/run_p30_variant.py",
    ".github/workflows/pdmal-solo-p30-variant-execution.yml",
    "experiments/pdmal_pilot/test_p30_variant_track.py",
    "experiments/pdmal_pilot/test_restore_five_gates_parity.py",
}


def validate(data: dict, reconciliation: dict) -> None:
    assert data["record_type"] == "DGAF_LEGACY_APOGEE_RUNTIME_IDENTITY_MIGRATION"
    assert data["schema_version"] == 1
    assert data["empirical_change"] is False

    canonical = data["canonical_p30"]
    assert canonical["authority"] == CANONICAL_AUTHORITY
    assert canonical["location"] == CANONICAL_LOCATION
    assert canonical["inside_per_turn_pdmal_consensus_dynamics"] is False
    assert reconciliation["canonical_p30"]["authority"] == CANONICAL_AUTHORITY

    legacy = data["legacy_runtime_gate"]
    assert legacy["id"] == LEGACY_ID
    assert legacy["id"] != "P-30"
    assert not legacy["id"].startswith("P-")
    assert legacy["canonical_pattern_id"] is None
    assert legacy["canonical_treatment_status"] == RETIRED
    assert legacy["historical_designation_issue"] == 165
    assert legacy["historical_symbols_preserved"] is True
    assert legacy["historical_semantics"]["terminal_rule"] == "D_TO_KILL"
    assert legacy["historical_semantics"]["thresholds"] == {
        "S": 0.90,
        "A": 0.75,
        "B": 0.60,
        "C": 0.45,
    }

    bridge = data["bridge"]
    assert bridge["p11_11q_to_runtime_confidence"] == "NOT_ESTABLISHED"
    for key in (
        "implicit_numeric_bridge_allowed",
        "agent_values_proxy_allowed",
        "outcome_derived_proxy_allowed",
        "default_constant_as_calibrated_confidence_allowed",
        "phi_constant_as_calibrated_confidence_allowed",
        "synthetic_fixture_as_calibrated_confidence_allowed",
    ):
        assert bridge[key] is False, f"{key} must remain fail-closed"

    assert set(data["historical_surfaces"]) == REQUIRED_HISTORICAL_SURFACES
    for path in REQUIRED_HISTORICAL_SURFACES:
        assert (ROOT / path).exists(), f"missing audited historical surface: {path}"

    policy = data["historical_evidence_policy"]
    assert policy["rewrite_prior_experiments"] is False
    assert policy["pool_with_future_canonical_experiment"] is False
    assert policy["epoch_003_identity_preserved"] == "DGAF-P30-EXPLICIT-0.45"

    next_gate = data["next_gate"]
    assert next_gate["required"] == "NONEMPIRICAL_CANONICAL_TREATMENT_PROFILE"
    assert next_gate["new_canonical_empirical_epoch"] == "NOT_AUTHORIZED"
    assert next_gate["high_assurance_authorization_changed"] is False

    wrapper = (ROOT / legacy["compatibility_wrapper"]).read_text(encoding="utf-8")
    assert f'LEGACY_APOGEE_RUNTIME_GATE_ID = "{LEGACY_ID}"' in wrapper
    assert f'CANONICAL_P30_AUTHORITY = "{CANONICAL_AUTHORITY}"' in wrapper
    assert f'CANONICAL_TREATMENT_STATUS = "{RETIRED}"' in wrapper


def main() -> None:
    data = json.loads(MIGRATION.read_text(encoding="utf-8"))
    reconciliation = json.loads(RECONCILIATION.read_text(encoding="utf-8"))
    validate(data, reconciliation)
    print("Legacy Apogee runtime identity: PASS_NONCANONICAL_SEPARATION")


if __name__ == "__main__":
    main()
