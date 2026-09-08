#!/usr/bin/env python3
"""Validate the protected-main admin-remediation protocol without mutating settings."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/governance/PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY_V1.json"

CANDIDATE_CORE = {
    "PPTL CI",
    "Governance CI",
    "Validate canonical control-state HEAD binding",
    "Pre-freeze PDMAL contract validation",
    "IP & Claim Hygiene Check",
    "evidence-validation",
    "full-repo-audit",
    "truth-layer",
    "truth-layer-tests",
}

NOT_PROVEN_UNIVERSAL = {
    "Python Tests & Quality Checks",
    "Markdown Lint — PR Scope",
    "Markdown Lint — Public Surface + Repository Ratchet",
    "PDMAL Pre-Freeze Runner Validation",
    "Historical runtime-evidence pre-freeze P3/P5 contract evidence",
}


def main() -> None:
    data = json.loads(POLICY.read_text(encoding="utf-8"))
    assert data["record_type"] == "DGAF_PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY"
    assert data["schema_version"] == 2
    assert data["policy_id"] == "PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY_V1"
    assert data["repository"] == "ndrorchestration/DGAF-Framework"
    assert data["target_branch"] == "main"
    assert data["issue"] == 277
    assert data["classification"] == "ADMIN_CONFIGURATION_REMEDIATION_PROTOCOL"
    assert data["settings_mutation_performed"] is False
    assert data["scientific_n_increment"] == 0

    observed = data["observed_state"]
    assert observed["protected"] is True
    assert observed["required_status_enforcement_level"] == "everyone"
    assert observed["approving_write_access_review_observed_required"] is True
    assert observed["required_approving_review_count_observed"] == 1
    assert observed["global_required_context_hygiene"] == "MISCONFIGURED_OVERBROAD"
    assert observed["global_required_context_count_observed"] == 68
    assert observed["expected_missing_required_contexts_on_green_policy_pr"] == 57
    assert observed["direct_admin_mutation_available_to_current_connector"] is False
    assert observed["reference_documentation_pr"] == 434
    assert observed["reference_governance_pr"] == 440
    assert observed["reference_governance_pr_custody_check"] == "SUCCESS"
    assert "57 of 68 required status checks expected" in observed["reference_policy_pr_merge_attempt"]

    protocol = data["application_protocol"]
    assert protocol["require_pull_request"] is True
    assert protocol["required_approving_review_count"] >= 1
    assert protocol["prevent_direct_write_bypass"] is True
    assert protocol["allow_unintended_bypass_actors"] is False
    assert protocol["literal_global_context_list_authorized_for_application"] is False
    assert set(protocol["candidate_core_contexts_observed_on_multiple_reference_classes"]) == CANDIDATE_CORE
    assert set(protocol["contexts_explicitly_not_safe_to_assume_universal_from_current_evidence"]) == NOT_PROVEN_UNIVERSAL
    assert "Propagation consistency — advisory" in protocol["globally_advisory_not_required"]
    assert protocol["specialized_gate_strategy"] == "PATH_AWARE_RULE_OR_ALWAYS_RUNNING_FAIL_CLOSED_AGGREGATOR"
    assert len(protocol["heterogeneous_reference_classes_required"]) >= 3

    conditional = data["conditional_context_families_not_globally_required"]
    assert len(conditional) == len(set(conditional))
    assert "Track A" in conditional
    assert "Mode-T" in conditional
    assert "Canonical Epoch 004" in conditional

    tests = data["acceptance_tests"]
    assert len(tests) >= 10
    assert any("documentation PR" in item for item in tests)
    assert any("governance/workflow PR" in item for item in tests)
    assert any("code/test PR" in item for item in tests)
    assert any("Direct ordinary contents writes" in item for item in tests)

    boundary = data["claim_boundary"]
    assert boundary["repository_admin_configuration_changed"] is False
    assert boundary["literal_admin_context_list_ready"] is False
    assert boundary["freeze_established"] is False
    assert boundary["empirical_execution_authorized"] is False
    assert boundary["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert boundary["high_assurance"] == "PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0"

    print("PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY_PASS")
    print("OBSERVED_REQUIRED_CONTEXTS=68")
    print("OBSERVED_EXPECTED_MISSING_CONTEXTS=57")
    print("LITERAL_ADMIN_CONTEXT_LIST_READY=false")
    print("ADMIN_SETTINGS_MUTATION_PERFORMED=false")
    print("SCIENTIFIC_N_INCREMENT=0")


if __name__ == "__main__":
    main()
