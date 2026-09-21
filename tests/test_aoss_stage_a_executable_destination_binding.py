import pytest

from scripts.aoss_stage_a.executable_destination_binding import (
    ExecutableDestinationBindingError,
    validate_proposed_executable_destination_binding,
)


def _binding(**changes):
    value = {
        "record_type": "AOSS_V0_6_STAGE_A_EXECUTABLE_DESTINATION_BINDING",
        "schema_version": 1,
        "controller_issue": 901,
        "status": "PROPOSED_NON_COLLECTING_IDENTITY_ONLY",
        "source_repository": "ndrorchestration/agent-control-plane",
        "source_commit": "dbab7c1afafec524ce7c18157de2089cafe79c87",
        "source_module": "src/agent_control_plane/core.py",
        "source_module_blob": "1341df7296a426b336b76ac6b1e4df67611ec931",
        "executable_identity": {
            "kind": "SOURCE_MODULE_PROVENANCE_ONLY",
            "repository": "ndrorchestration/agent-control-plane",
            "commit": "dbab7c1afafec524ce7c18157de2089cafe79c87",
            "path": "src/agent_control_plane/core.py",
            "blob": "1341df7296a426b336b76ac6b1e4df67611ec931",
        },
        "destination_identity": {
            "kind": "SYNTHETIC_FIXTURE_ONLY",
            "uri": "fixture://aoss-v0.6-stage-a/non-collecting",
        },
        "attempt_identity": {
            "kind": "SYNTHETIC_FIXTURE_ONLY",
            "attempt_id": "aoss-stage-a-fixture-0001",
        },
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "outcomes_generated": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
    value.update(changes)
    return value


def test_proposed_identity_binding_verifies_exact_source_and_fixture_identities():
    report = validate_proposed_executable_destination_binding(_binding())

    assert report["identity_contract"] == "PASS_PROPOSED_NON_COLLECTING"
    assert report["executable_acceptance"] == "NOT_ESTABLISHED"
    assert report["destination_acceptance"] == "NOT_ESTABLISHED"
    assert report["execution"] == "NOT_PERFORMED"
    assert report["outcomes_generated"] is False
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["scientific_n_increment"] == 0


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("source_commit", "wrong", "SOURCE_COMMIT_MISMATCH"),
        ("source_module_blob", "wrong", "SOURCE_MODULE_BLOB_MISMATCH"),
        ("executable_identity", None, "EXECUTABLE_IDENTITY_MISMATCH"),
        ("destination_identity", {"kind": "REAL_DESTINATION"}, "DESTINATION_FIXTURE_BOUNDARY"),
        ("attempt_identity", {"kind": "REAL_ATTEMPT"}, "ATTEMPT_FIXTURE_BOUNDARY"),
        ("executable_acceptance", "ACCEPTED", "EXECUTABLE_ACCEPTANCE_PREMATURE"),
        ("destination_acceptance", "ACCEPTED", "DESTINATION_ACCEPTANCE_PREMATURE"),
        ("execution_allowed", True, "EXECUTION_PREMATURE"),
        ("outcomes_generated", True, "OUTCOME_GENERATION_PREMATURE"),
    ],
)
def test_identity_drift_fails_closed(field, value, code):
    with pytest.raises(ExecutableDestinationBindingError, match=code):
        validate_proposed_executable_destination_binding(_binding(**{field: value}))
