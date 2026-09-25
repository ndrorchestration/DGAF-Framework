from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "registry" / "dgaf_self_application_cold_start_execution_record_v1.schema.json"
MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"


def load_schema() -> dict:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def test_execution_record_schema_is_bounded_and_nonpromoting():
    schema = load_schema()
    properties = schema["properties"]

    assert properties["schema_version"]["const"] == "dgaf.self_application.cold_start_execution_record.v1"
    assert properties["evidence_class"]["const"] == "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
    assert properties["controller_issue"]["const"] == "issue://1022"
    assert properties["external_review_controller"]["const"] == "issue://929"
    assert properties["same_system_run_independence"]["const"] == "NOT_ESTABLISHED"
    assert properties["runtime_authorization_effect"]["const"] == "NONE"
    assert properties["scientific_state_effect"]["const"] == "NONE"

    claim_ceiling = properties["claim_ceiling"]["properties"]
    assert claim_ceiling["scientific_n_increment"]["const"] == 0
    assert claim_ceiling["independent_validation"]["const"] == "NOT_ESTABLISHED"
    assert claim_ceiling["external_validation"]["const"] == "NOT_ESTABLISHED"
    assert claim_ceiling["canonical_dgaf_efficacy"]["const"] == "NOT_ESTABLISHED"
    assert claim_ceiling["high_assurance"]["const"] == "NOT_AUTHORIZED"


def test_execution_record_schema_requires_raw_per_step_evidence_fields():
    schema = load_schema()
    step_schema = schema["properties"]["per_step_results"]["items"]

    assert schema["properties"]["per_step_results"]["minItems"] == 5
    assert step_schema["additionalProperties"] is False
    for field in (
        "step_index",
        "measure_id",
        "question",
        "failure_record",
        "metric",
        "status",
        "evidence_retained",
        "evidence_location",
        "operator_observation",
    ):
        assert field in step_schema["required"]

    assert step_schema["properties"]["status"]["enum"] == [
        "PASS",
        "FAIL",
        "BLOCKED",
        "NOT_EXECUTED",
    ]


def test_execution_record_schema_tracks_manifest_measures_without_claiming_execution():
    schema = load_schema()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert len(manifest["measures"]) == schema["properties"]["per_step_results"]["minItems"]
    manifest_schema = schema["properties"]["manifest"]["properties"]
    assert manifest_schema["path"]["const"] == "registry/dgaf_self_application_cold_start_manifest_v1.json"
    assert manifest_schema["schema_version"]["const"] == manifest["schema_version"]
    assert schema["properties"]["executed_cold_start_reproduction"]["type"] == "boolean"


def test_execution_record_schema_separates_same_system_from_external_replay():
    schema = load_schema()
    operator_context = schema["properties"]["operator_context"]

    assert operator_context["additionalProperties"] is False
    assert operator_context["properties"]["retained_context_allowed"]["type"] == "boolean"
    assert operator_context["properties"]["executor_relationship"]["enum"] == [
        "SAME_SYSTEM_OPERATOR",
        "EXTERNAL_REVIEWER",
    ]
    assert schema["properties"]["execution_mode"]["enum"] == [
        "OPERATOR_LOCAL_REPLAY",
        "INDEPENDENT_REVIEWER_REPLAY",
    ]


def test_execution_record_schema_summary_cannot_promote_independence():
    schema = load_schema()
    summary = schema["properties"]["summary"]

    assert summary["properties"]["raw_per_step_results_retained_before_summary"]["const"] is True
    assert summary["properties"]["same_system_run_independence"]["const"] == "NOT_ESTABLISHED"
    assert summary["properties"]["external_review_controller"]["const"] == "issue://929"
