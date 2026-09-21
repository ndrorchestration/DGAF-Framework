from scripts.aoss_stage_a.environment_manifest import (
    EnvironmentManifestError,
    RuntimeFacts,
    observe_unaccepted_environment_manifest,
    validate_synthetic_manifest,
    validate_unaccepted_environment_manifest,
)


def _manifest(**changes):
    value = {
        "record_type": "AOSS_V0_6_STAGE_A_ENVIRONMENT_MANIFEST",
        "status": "SYNTHETIC_FIXTURE_NOT_INSTALLED_ENVIRONMENT",
        "manifest_id": "synthetic-fixture-001",
        "manifest_status": "NOT_ESTABLISHED",
        "runtime_binding_record_type": "AOSS_V0_6_STAGE_A_RUNTIME_BINDING",
        "interpreter_implementation": "cpython",
        "interpreter_version": "3.12.3",
        "dependency_lock_sha256": "81c1ade0b76ff38cbdcbe4ddbc615c273f02dc97a9ff055c8c2889940a2ca6bd",
        "platform_system": "SyntheticOS",
        "platform_machine": "synthetic-machine",
        "environment_observed_at": "2026-09-21T00:00:00Z",
        "source_driver_binding": "NOT_ESTABLISHED",
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }
    value.update(changes)
    return value


def _bound_facts():
    return RuntimeFacts(
        implementation="cpython",
        version="3.12.3",
        platform_system="SyntheticOS",
        platform_machine="synthetic-machine",
        executable="/synthetic/bin/python",
        prefix="/synthetic",
        base_prefix="/synthetic",
    )


def test_synthetic_manifest_validates_without_accepting_environment():
    report = validate_synthetic_manifest(_manifest())

    assert report["manifest_validation"] == "PASS_SYNTHETIC_FIXTURE_NON_COLLECTING"
    assert report["manifest_status"] == "NOT_ESTABLISHED"
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["outcomes_generated"] is False
    assert report["scientific_n_increment"] == 0


def test_observed_environment_is_explicitly_unaccepted():
    manifest = observe_unaccepted_environment_manifest(
        "2026-09-21T00:00:00Z",
        facts=_bound_facts(),
    )
    report = validate_unaccepted_environment_manifest(manifest)

    assert manifest["status"] == "OBSERVED_NOT_ACCEPTED"
    assert manifest["manifest_status"] == "NOT_ESTABLISHED"
    assert report["manifest_validation"] == "PASS_OBSERVED_NOT_ACCEPTED"
    assert report["platform_binding"] == "OBSERVED_NOT_ACCEPTED"
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["outcomes_generated"] is False
    assert report["scientific_n_increment"] == 0


def test_missing_manifest_field_fails_closed():
    value = _manifest()
    del value["platform_machine"]

    try:
        validate_synthetic_manifest(value)
    except EnvironmentManifestError as exc:
        assert str(exc) == "MANIFEST_FIELD_SET_MISMATCH"
    else:
        raise AssertionError("incomplete manifest unexpectedly accepted")


def test_real_environment_status_cannot_be_smuggled_into_fixture():
    try:
        validate_synthetic_manifest(_manifest(status="INSTALLED_ENVIRONMENT_ACCEPTED"))
    except EnvironmentManifestError as exc:
        assert str(exc) == "MANIFEST_STATUS_MUST_REMAIN_SYNTHETIC"
    else:
        raise AssertionError("accepted environment unexpectedly passed")


def test_observed_manifest_cannot_be_relabelled_as_accepted():
    observed = observe_unaccepted_environment_manifest(
        "2026-09-21T00:00:00Z",
        facts=_bound_facts(),
    )
    try:
        validate_unaccepted_environment_manifest(
            {**observed, "status": "INSTALLED_ENVIRONMENT_ACCEPTED"}
        )
    except EnvironmentManifestError as exc:
        assert str(exc) == "MANIFEST_STATUS_MUST_REMAIN_UNACCEPTED"
    else:
        raise AssertionError("accepted environment unexpectedly passed")


def test_drift_and_overclaim_fail_closed():
    for changes, code in [
        ("dependency_lock_sha256", "wrong", "DEPENDENCY_LOCK_DIGEST_MISMATCH"),
        ("environment_observed_at", "not-a-timestamp", "ENVIRONMENT_TIMESTAMP_INVALID"),
        ("outcomes_generated", True, "OUTCOME_GENERATION_PREMATURE"),
        ("scientific_n_increment", 1, "SCIENTIFIC_N_INCREMENT_INVALID"),
    ]:
        value = _manifest(**{changes[0]: changes[1]})
        try:
            validate_synthetic_manifest(value)
        except EnvironmentManifestError as exc:
            assert str(exc) == changes[2]
        else:
            raise AssertionError(f"{changes[2]} unexpectedly passed")
