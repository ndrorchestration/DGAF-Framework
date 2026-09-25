from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_cold_start_manifest_is_bounded_and_nonpromoting():
    manifest = load_manifest()

    assert manifest["schema_version"] == "dgaf.self_application.cold_start_manifest.v1"
    assert manifest["evidence_class"] == "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
    assert manifest["controller_issue"] == "issue://1022"
    assert manifest["external_review_controller"] == "issue://929"
    assert manifest["same_system_run_independence"] == "NOT_ESTABLISHED"
    assert manifest["runtime_authorization_effect"] == "NONE"
    assert manifest["scientific_state_effect"] == "NONE"
    assert manifest["claim_ceiling"] == {
        "scientific_n_increment": 0,
        "independent_validation": "NOT_ESTABLISHED",
        "external_validation": "NOT_ESTABLISHED",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }


def test_cold_start_measures_cover_required_reproduction_risks():
    manifest = load_manifest()
    measures = {measure["id"]: measure for measure in manifest["measures"]}

    assert set(measures) == {
        "documented_prerequisites",
        "command_order",
        "evidence_locations",
        "environment_reproduction",
        "retained_context_dependence",
    }
    assert measures["documented_prerequisites"]["metric"] == "undocumented_prerequisite_count"
    assert measures["command_order"]["metric"] == "manual_decision_count"
    assert measures["evidence_locations"]["metric"] == "ambiguous_evidence_location_count"
    assert measures["environment_reproduction"]["metric"] == "setup_failure_count"
    assert measures["retained_context_dependence"]["metric"] == "hidden_context_dependency_count"

    assert all(measure["failure_record"] for measure in measures.values())
    assert all(measure["question"].endswith("?") for measure in measures.values())


def test_acceptance_contract_fails_closed_and_preserves_independence_boundary():
    manifest = load_manifest()
    contract = manifest["acceptance_contract"]

    assert contract == {
        "raw_per_step_results_retained_before_summary": True,
        "same_system_runs_must_not_be_labeled_independent": True,
        "external_review_must_route_to_issue_929": True,
        "unexpected_success_without_required_evidence_is_not_acceptance": True,
        "missing_or_ambiguous_required_input_fails_closed": True,
    }


def test_summary_requirements_are_mechanically_derived_metric_names():
    manifest = load_manifest()
    measure_metrics = {measure["metric"] for measure in manifest["measures"]}
    summary_requirements = set(manifest["summary_requirements"])

    assert "cold_start_completion_rate" in summary_requirements
    assert measure_metrics < summary_requirements
    assert len(summary_requirements) == len(measure_metrics) + 1
