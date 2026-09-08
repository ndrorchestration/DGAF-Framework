#!/usr/bin/env python3
"""Validate the repository-native protected-main remediation target.

This validator does not mutate GitHub repository settings. It validates only the
machine-readable policy that an administrator can later apply and verify.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/governance/PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY_V1.json"

EXPECTED_GLOBAL = {
    "PPTL CI",
    "Governance CI",
    "Validate canonical control-state HEAD binding",
    "Pre-freeze PDMAL contract validation",
    "IP & Claim Hygiene Check",
    "evidence-validation",
    "full-repo-audit",
    "truth-layer",
    "truth-layer-tests",
    "Markdown Lint — PR Scope",
    "Markdown Lint — Public Surface + Repository Ratchet",
    "PDMAL Pre-Freeze Runner Validation",
}

CONDITIONAL_MARKERS = (
    "Mode-T",
    "Track A",
    "B1",
    "B2",
    "B3",
    "Epoch 004",
    "Canonical P30",
    "Canonical Profile",
    "Canonical Treatment",
    "Solo",
    "P6a",
    "P9",
    "Sentinel Deontic Precedence",
    "KAPPA v36 Authority",
    "Seven-Gate Treatment Fidelity Audit",
    "E2B Verifier Lock",
    "External Acceptance",
    "Historical runtime-evidence",
    "Legacy Apogee Runtime Identity Migration",
)


def main() -> None:
    data = json.loads(POLICY.read_text(encoding="utf-8"))

    assert data["record_type"] == "DGAF_PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY"
    assert data["policy_id"] == "PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY_V1"
    assert data["repository"] == "ndrorchestration/DGAF-Framework"
    assert data["target_branch"] == "main"
    assert data["issue"] == 277
    assert data["classification"] == "ADMIN_CONFIGURATION_REMEDIATION_TARGET"
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
    assert observed["reference_main_sha"] == "002f6c7037c7e72c31c39499cba97681da76a962"
    assert observed["reference_green_documentation_pr"] == 434
    assert observed["reference_green_documentation_pr_returned_workflows"] == "17/17 SUCCESS"
    assert observed["reference_green_documentation_pr_merge_state"] == "BLOCKED"
    assert observed["reference_policy_pr"] == 438
    assert observed["reference_policy_pr_initial_head"] == "adbd6bef17665e6ae30c6505c245805ddff77d1d"
    assert observed["reference_policy_pr_initial_returned_workflows"] == "16/16 SUCCESS"
    assert "57 of 68 required status checks expected" in observed["reference_policy_pr_merge_attempt"]

    desired = data["desired_policy"]
    assert desired["require_pull_request"] is True
    assert desired["required_approving_review_count"] >= 1
    assert desired["prevent_direct_write_bypass"] is True
    assert desired["allow_unintended_bypass_actors"] is False

    global_contexts = desired["globally_required_contexts"]
    assert len(global_contexts) == len(set(global_contexts)), "duplicate global context"
    assert set(global_contexts) == EXPECTED_GLOBAL
    assert "Propagation consistency — advisory" not in global_contexts

    for context in global_contexts:
        assert not any(marker in context for marker in CONDITIONAL_MARKERS), (
            f"conditional/specialized context incorrectly global: {context}"
        )

    families = desired["conditional_context_families_not_globally_required"]
    assert len(families) == len(set(families)), "duplicate conditional family"
    assert desired["specialized_gate_strategy"] == (
        "PATH_AWARE_RULE_OR_ALWAYS_RUNNING_FAIL_CLOSED_AGGREGATOR"
    )

    tests = data["acceptance_tests"]
    assert len(tests) >= 7
    assert any("documentation PR" in item for item in tests)
    assert any("specialized-path PR" in item for item in tests)
    assert any("Direct ordinary contents writes" in item for item in tests)

    boundary = data["claim_boundary"]
    assert boundary["repository_admin_configuration_changed"] is False
    assert boundary["freeze_established"] is False
    assert boundary["empirical_execution_authorized"] is False
    assert boundary["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert boundary["high_assurance"] == "PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0"

    print("PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY_PASS")
    print("OBSERVED_REQUIRED_CONTEXTS=68")
    print("OBSERVED_EXPECTED_MISSING_CONTEXTS=57")
    print("ADMIN_SETTINGS_MUTATION_PERFORMED=false")
    print("SCIENTIFIC_N_INCREMENT=0")


if __name__ == "__main__":
    main()
