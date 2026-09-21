import pytest

from scripts.aoss_stage_a.source_driver_binding import (
    SourceDriverBindingError,
    validate_unaccepted_source_driver_binding,
)

EXPECTED_CLASSES = [
    "normal_completion",
    "policy_denial",
    "unknown_capability_rejection",
    "handler_failure",
    "cancellation",
    "exact_budget_success",
    "budget_exhaustion",
    "suppressed_budget_exception_fail_closed",
    "missing_event",
    "reordered_exported_events",
    "duplicate_replayed_event",
    "stale_timestamp",
    "malformed_manifest",
    "mismatched_run_id",
    "source_order_ambiguity",
    "missing_authority_evidence",
]


def _binding(**changes):
    value = {
        "record_type": "AOSS_V0_6_STAGE_A_SOURCE_DRIVER_BINDING",
        "schema_version": 1,
        "status": "PROPOSED_NON_COLLECTING_SYNTHETIC_ONLY",
        "controller_issue": 901,
        "catalog_path": "registry/aoss_v0_6_stage_a_source_driver_recipe_catalog_v1.json",
        "recipe_version": "AOSS_V0_6_STAGE_A_SYNTHETIC_RECIPE_CATALOG_V1",
        "recipe_classes": EXPECTED_CLASSES,
        "source_repository": "ndrorchestration/agent-control-plane",
        "source_commit": "dbab7c1afafec524ce7c18157de2089cafe79c87",
        "driver_import_allowed": False,
        "acp_execution_allowed": False,
        "accepted_outcome_artifacts": False,
        "executable_identity": None,
        "destination_identity": None,
        "source_driver_binding": "NOT_ESTABLISHED",
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
    value.update(changes)
    return value


def test_proposed_binding_verifies_catalog_and_exact_source_without_accepting_driver():
    report = validate_unaccepted_source_driver_binding(_binding())

    assert report["catalog_binding"] == "PASS_PROPOSED_NON_COLLECTING"
    assert report["source_driver_binding"] == "NOT_ESTABLISHED"
    assert report["driver_execution"] == "NOT_PERFORMED"
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["outcomes_generated"] is False
    assert report["scientific_n_increment"] == 0


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("source_commit", "wrong", "SOURCE_COMMIT_MISMATCH"),
        ("recipe_classes", EXPECTED_CLASSES[:-1], "RECIPE_CLASS_SET_MISMATCH"),
        ("driver_import_allowed", True, "DRIVER_IMPORT_PREMATURE"),
        ("acp_execution_allowed", True, "ACP_EXECUTION_PREMATURE"),
        ("executable_identity", "sha256:fixture", "EXECUTABLE_BINDING_PREMATURE"),
        ("destination_identity", "fixture-destination", "DESTINATION_BINDING_PREMATURE"),
        ("source_driver_binding", "ACCEPTED", "SOURCE_DRIVER_ACCEPTANCE_PREMATURE"),
        ("outcomes_generated", True, "OUTCOME_GENERATION_PREMATURE"),
    ],
)
def test_binding_drift_fails_closed(field, value, code):
    with pytest.raises(SourceDriverBindingError, match=code):
        validate_unaccepted_source_driver_binding(_binding(**{field: value}))
