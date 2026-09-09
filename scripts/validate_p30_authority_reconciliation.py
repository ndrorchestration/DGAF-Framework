#!/usr/bin/env python3
"""Fail-closed validator for the P-30 authority reconciliation record."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/governance/P30_AUTHORITY_RECONCILIATION_2026-09-07.json"

EXPECTED_CANONICAL_AUTHORITY = "S035_P11_11Q_ATTESTATION"
EXPECTED_RUNTIME_IDENTITY = "UNASSIGNED_PENDING_SEMANTIC_MIGRATION"
EXPECTED_EMPIRICAL_GATE = "PROHIBITED_PENDING_SEMANTIC_MIGRATION"
REQUIRED_CANONICAL_SOURCES = {
    "docs/patterns/NDR_PATTERN_REGISTRY.md",
    "docs/qa/APOGEE_11Q_S035.json",
    "docs/qa/APOGEE_11Q_P34.json",
    "docs/agents/apogee/APOGEE_KB.md",
}
REQUIRED_RUNTIME_SOURCES = {
    "components/ensemble_v17.py",
    "pages/api/triad.ts",
    "experiments/pdmal_pilot/pdmaltgl_gate_binding.py",
}


def validate_record(data: dict) -> None:
    assert data == json.loads(json.dumps(data)), "record must be JSON-serializable"
    assert data["record_type"] == "DGAF_P30_AUTHORITY_RECONCILIATION"
    assert data["schema_version"] == 1
    assert data["empirical_change"] is False

    canonical = data["canonical_p30"]
    assert canonical["identity"] == "P-30"
    assert canonical["registered_session"] == "S035"
    assert canonical["authority"] == EXPECTED_CANONICAL_AUTHORITY
    assert canonical["rubric"] == "P-11 11Q Attestation Scoring"
    assert set(canonical["source_paths"]) == REQUIRED_CANONICAL_SOURCES

    runtime = data["legacy_runtime_scalar_gate"]
    assert runtime["identity"] == EXPECTED_RUNTIME_IDENTITY
    assert runtime["equivalent_to_canonical_p30"] is False
    assert runtime["confidence_provenance"] == "NOT_ESTABLISHED_FOR_CANONICAL_PDMAL"
    assert runtime["restored_experiment_terminal_rule"] == "D_TO_KILL"
    assert runtime["thresholds"] == {
        "S": 0.90,
        "A": 0.75,
        "B": 0.60,
        "C": 0.45,
        "D_below": 0.45,
    }
    assert set(runtime["source_paths"]) == REQUIRED_RUNTIME_SOURCES

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

    empirical = data["empirical_gate"]
    assert empirical["new_canonical_dgaf_empirical_epoch"] == EXPECTED_EMPIRICAL_GATE
    assert empirical["fresh_empirical_authorization_granted"] is False
    assert empirical["high_assurance_authorization_changed"] is False

    retained = data["retained_evidence"]
    assert retained["experiment_001"] == "APPARATUS_FALSIFICATION_UNPOOLED"
    assert retained["epoch_002"] == "NON_EMPIRICAL_DIAGNOSTIC_PASS"
    assert retained["epoch_003"] == "NEGATIVE_FOR_SYNTHETIC_DGAF_P30_EXPLICIT_0_45_VARIANT_UNPOOLED"

    for path in REQUIRED_CANONICAL_SOURCES | REQUIRED_RUNTIME_SOURCES:
        assert (ROOT / path).exists(), f"missing authority source: {path}"


def main() -> None:
    data = json.loads(RECORD.read_text(encoding="utf-8"))
    validate_record(data)
    print("P-30 authority reconciliation: PASS_SEPARATION_BOUNDARY")


if __name__ == "__main__":
    main()
