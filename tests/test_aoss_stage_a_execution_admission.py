import pytest

from scripts.aoss_stage_a.execution_admission import (
    ExecutionAdmissionBoundaryError,
    assess_execution_admission_blockers,
)


def _records():
    runtime = {
        "installed_environment_manifest": "NOT_ESTABLISHED",
    }
    environment = {
        "installed_environment_acceptance": "NOT_ESTABLISHED",
    }
    source_driver = {
        "source_driver_binding": "NOT_ESTABLISHED",
    }
    executable_destination = {
        "executable_identity": {
            "kind": "SOURCE_MODULE_PROVENANCE_ONLY",
        },
        "destination_identity": {
            "kind": "SYNTHETIC_FIXTURE_ONLY",
        },
        "attempt_identity": {
            "kind": "SYNTHETIC_FIXTURE_ONLY",
        },
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "outcomes_generated": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "scientific_n_increment": 0,
    }
    return runtime, environment, source_driver, executable_destination


def test_current_non_collecting_records_report_all_admission_blockers():
    report = assess_execution_admission_blockers(*_records())

    assert report["status"] == "BLOCKED"
    assert report["blocker_count"] == 8
    assert set(report["blockers"]) == {
        "INSTALLED_ENVIRONMENT_MANIFEST_NOT_ESTABLISHED",
        "INSTALLED_ENVIRONMENT_ACCEPTANCE_NOT_ESTABLISHED",
        "SOURCE_DRIVER_BINDING_NOT_ESTABLISHED",
        "EXECUTABLE_ACCEPTANCE_NOT_ESTABLISHED",
        "DESTINATION_ACCEPTANCE_NOT_ESTABLISHED",
        "EXECUTABLE_IDENTITY_NOT_ADMITTED",
        "DESTINATION_FIXTURE_ONLY",
        "ATTEMPT_FIXTURE_ONLY",
    }
    assert report["execution_allowed"] is False
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["outcomes_generated"] is False
    assert report["scientific_n_increment"] == 0


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("execution_allowed", True, "EXECUTION_ENABLED_BEFORE_ACCEPTANCE"),
        ("outcomes_generated", True, "OUTCOMES_PRESENT_BEFORE_ACCEPTANCE"),
        (
            "collection_execution_readiness",
            "ESTABLISHED",
            "READINESS_PROMOTED_BEFORE_ACCEPTANCE",
        ),
        ("scientific_n_increment", 1, "SCIENTIFIC_N_CHANGED_BEFORE_ACCEPTANCE"),
    ],
)
def test_pre_admission_state_cannot_promote_execution(field, value, error):
    runtime, environment, source_driver, executable_destination = _records()
    executable_destination[field] = value

    with pytest.raises(ExecutionAdmissionBoundaryError, match=error):
        assess_execution_admission_blockers(
            runtime,
            environment,
            source_driver,
            executable_destination,
        )


@pytest.mark.parametrize(
    "identity_field",
    ["executable_identity", "destination_identity", "attempt_identity"],
)
def test_identity_envelopes_must_be_explicit_mappings(identity_field):
    runtime, environment, source_driver, executable_destination = _records()
    executable_destination[identity_field] = None

    with pytest.raises(ExecutionAdmissionBoundaryError, match="IDENTITY_INVALID"):
        assess_execution_admission_blockers(
            runtime,
            environment,
            source_driver,
            executable_destination,
        )


def test_blocker_report_never_grants_readiness_when_strings_are_changed():
    runtime, environment, source_driver, executable_destination = _records()
    runtime["installed_environment_manifest"] = "CANDIDATE_PRESENT"
    environment["installed_environment_acceptance"] = "CANDIDATE_PRESENT"
    source_driver["source_driver_binding"] = "CANDIDATE_PRESENT"
    executable_destination["executable_acceptance"] = "CANDIDATE_PRESENT"
    executable_destination["destination_acceptance"] = "CANDIDATE_PRESENT"
    executable_destination["executable_identity"] = {"kind": "CANDIDATE_BYTES"}
    executable_destination["destination_identity"] = {"kind": "CANDIDATE_DESTINATION"}
    executable_destination["attempt_identity"] = {"kind": "CANDIDATE_ATTEMPT"}

    report = assess_execution_admission_blockers(
        runtime,
        environment,
        source_driver,
        executable_destination,
    )

    assert report["status"] == "NO_BLOCKERS_REPORTED"
    assert report["blocker_count"] == 0
    assert report["execution_allowed"] is False
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
