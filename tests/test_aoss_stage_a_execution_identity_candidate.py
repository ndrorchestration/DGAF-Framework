from copy import deepcopy
import hashlib
from pathlib import Path

import pytest

from scripts.aoss_stage_a.execution_identity_candidate import (
    ExecutionIdentityCandidateError,
    prepare_execution_identity_candidate,
    validate_execution_identity_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT / "registry/aoss_v0_6_stage_a_source_driver_recipe_catalog_v1.json"
CATALOG_SHA = hashlib.sha256(CATALOG_FILE.read_bytes()).hexdigest()

SHA_A = "a" * 64
SHA_C = "c" * 64


def _driver(root: Path) -> Path:
    driver = root / "scripts" / "aoss_stage_a" / "source_driver.py"
    driver.parent.mkdir(parents=True, exist_ok=True)
    if not driver.exists():
        driver.write_bytes(b"# source-driver candidate\n")
    return driver


def _candidate(tmp_path: Path | None = None):
    root = tmp_path or Path(__file__).resolve().parents[1]
    driver = _driver(root)
    return prepare_execution_identity_candidate(
        interpreter_path="/opt/python/3.12.3/bin/python",
        interpreter_sha256=SHA_A,
        argv=[
            "scripts/aoss_stage_a/source_driver.py",
            "--acp-root",
            "/srv/agent-control-plane",
            "--recipe-class",
            "normal_completion",
            "--run-id",
            "run-0001",
            "--output",
            "/srv/aoss-stage-a/retained/attempt-0001/source-driver-result.json",
        ],
        working_directory=str(root),
        destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
        attempt_id="aoss-stage-a-attempt-0001",
        recipe_catalog_sha256=CATALOG_SHA,
        environment_candidate_record_sha256=SHA_C,
        source_driver_path="scripts/aoss_stage_a/source_driver.py",
        source_driver_file=driver,
    )


def test_non_fixture_candidate_validates_without_acceptance(tmp_path):
    candidate = _candidate(tmp_path)
    report = validate_execution_identity_candidate(
        candidate,
        source_driver_file=_driver(tmp_path),
    )

    assert report["candidate_validation"] == "PASS_NON_FIXTURE_IDENTITY_CANDIDATE"
    assert report["installed_environment_acceptance"] == "NOT_ESTABLISHED"
    assert report["source_driver_binding"] == "NOT_ESTABLISHED"
    assert report["executable_acceptance"] == "NOT_ESTABLISHED"
    assert report["destination_acceptance"] == "NOT_ESTABLISHED"
    assert report["external_adjudication"] == "NOT_EXECUTED"
    assert report["execution_allowed"] is False
    assert report["scientific_n_increment"] == 0


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        (
            "destination_identity",
            {"kind": "NON_FIXTURE_DESTINATION_CANDIDATE", "uri": "fixture://bad"},
            "EXECUTION_IDENTITY_DESTINATION_FIXTURE_FORBIDDEN",
        ),
        (
            "attempt_identity",
            {
                "kind": "PROSPECTIVE_ATTEMPT_CANDIDATE",
                "attempt_id": "synthetic-fixture-attempt",
                "created_before_execution": True,
                "outcome_inspected": False,
            },
            "EXECUTION_IDENTITY_ATTEMPT_FIXTURE_FORBIDDEN",
        ),
    ],
)
def test_candidate_rejects_fixture_identity_substitution(tmp_path, field, value, error):
    candidate = _candidate(tmp_path)
    candidate[field] = value

    with pytest.raises(ExecutionIdentityCandidateError, match=error):
        validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
        )


def test_candidate_rejects_post_inspection_attempt(tmp_path):
    candidate = _candidate(tmp_path)
    candidate["attempt_identity"]["outcome_inspected"] = True

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_OUTCOME_ALREADY_INSPECTED",
    ):
        validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
        )


def test_candidate_rejects_source_commit_drift(tmp_path):
    candidate = _candidate(tmp_path)
    candidate["source"]["commit"] = "0" * 40

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_SOURCE_COMMIT_MISMATCH",
    ):
        validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
        )


def test_candidate_rejects_adjudication_prepopulation(tmp_path):
    candidate = _candidate(tmp_path)
    candidate["adjudication"]["reviewer_identity"] = "self"

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_ADJUDICATION_PREMATURE",
    ):
        validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("installed_environment_acceptance", "ACCEPTED"),
        ("source_driver_binding", "ESTABLISHED"),
        ("executable_acceptance", "ACCEPTED"),
        ("destination_acceptance", "ACCEPTED"),
        ("execution_allowed", True),
        ("collection_execution_readiness", "ESTABLISHED"),
        ("outcomes_generated", True),
        ("scientific_n_increment", 1),
    ],
)
def test_candidate_cannot_promote_readiness(tmp_path, field, value):
    candidate = _candidate(tmp_path)
    candidate[field] = value

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match=f"EXECUTION_IDENTITY_BOUNDARY_DRIFT_{field.upper()}",
    ):
        validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
        )


def test_candidate_detects_executable_identity_mutation(tmp_path):
    candidate = _candidate(tmp_path)
    mutated = deepcopy(candidate)
    mutated["executable_identity"]["interpreter_sha256"] = "not-a-sha"

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_INTERPRETER_SHA_INVALID",
    ):
        validate_execution_identity_candidate(
            mutated,
            source_driver_file=_driver(tmp_path),
        )


def test_prepare_rejects_recipe_catalog_sha_mismatch(tmp_path):
    driver = _driver(tmp_path)

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_RECIPE_CATALOG_SHA_MISMATCH",
    ):
        prepare_execution_identity_candidate(
            interpreter_path="/opt/python/3.12.3/bin/python",
            interpreter_sha256=SHA_A,
            argv=[
                "scripts/aoss_stage_a/source_driver.py",
                "--acp-root",
                "/srv/agent-control-plane",
                "--recipe-class",
                "normal_completion",
                "--run-id",
                "run-0001",
                "--output",
                "/srv/aoss-stage-a/retained/attempt-0001/source-driver-result.json",
            ],
            working_directory=str(tmp_path),
            destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
            attempt_id="aoss-stage-a-attempt-0001",
            recipe_catalog_sha256="b" * 64,
            environment_candidate_record_sha256=SHA_C,
            source_driver_path="scripts/aoss_stage_a/source_driver.py",
            source_driver_file=driver,
        )


def test_validation_rejects_substituted_recipe_catalog(tmp_path):
    candidate = _candidate(tmp_path)
    substituted = tmp_path / "catalog.json"
    substituted.write_bytes(CATALOG_FILE.read_bytes() + b" ")

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_RECIPE_CATALOG_SHA_MISMATCH",
    ):
        validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
            recipe_catalog_file=substituted,
        )


def test_prepare_rejects_argv_not_bound_to_source_driver(tmp_path):
    driver = _driver(tmp_path)

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_ARGV_DRIVER_MISMATCH",
    ):
        prepare_execution_identity_candidate(
            interpreter_path="/opt/python/3.12.3/bin/python",
            interpreter_sha256=SHA_A,
            argv=["-m", "definitely_missing_aoss_driver_901"],
            working_directory=str(tmp_path),
            destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
            attempt_id="aoss-stage-a-attempt-0001",
            recipe_catalog_sha256=CATALOG_SHA,
            environment_candidate_record_sha256=SHA_C,
            source_driver_path="scripts/aoss_stage_a/source_driver.py",
            source_driver_file=driver,
        )


def test_validation_rejects_argv_driver_substitution(tmp_path):
    candidate = _candidate(tmp_path)
    candidate["executable_identity"]["argv"] = ["-m", "definitely_missing_aoss_driver_901"]

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_ARGV_DRIVER_MISMATCH",
    ):
        validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
        )


def test_prepare_rejects_non_driver_cli_shape(tmp_path):
    driver = _driver(tmp_path)

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_ARGV_SHAPE_MISMATCH",
    ):
        prepare_execution_identity_candidate(
            interpreter_path="/opt/python/3.12.3/bin/python",
            interpreter_sha256=SHA_A,
            argv=["scripts/aoss_stage_a/source_driver.py", "--plan", "stage-a"],
            working_directory=str(tmp_path),
            destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
            attempt_id="aoss-stage-a-attempt-0001",
            recipe_catalog_sha256=CATALOG_SHA,
            environment_candidate_record_sha256=SHA_C,
            source_driver_path="scripts/aoss_stage_a/source_driver.py",
            source_driver_file=driver,
        )


def test_prepare_rejects_workdir_that_resolves_to_different_driver(tmp_path):
    driver = _driver(tmp_path)
    wrong_root = tmp_path / "wrong-root"
    wrong_root.mkdir()

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_ARGV_DRIVER_RESOLUTION_MISMATCH",
    ):
        prepare_execution_identity_candidate(
            interpreter_path="/opt/python/3.12.3/bin/python",
            interpreter_sha256=SHA_A,
            argv=[
            "scripts/aoss_stage_a/source_driver.py",
            "--acp-root",
            "/srv/agent-control-plane",
            "--recipe-class",
            "normal_completion",
            "--run-id",
            "run-0001",
            "--output",
            "/srv/aoss-stage-a/retained/attempt-0001/source-driver-result.json",
        ],
            working_directory=str(wrong_root),
            destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
            attempt_id="aoss-stage-a-attempt-0001",
            recipe_catalog_sha256=CATALOG_SHA,
            environment_candidate_record_sha256=SHA_C,
            source_driver_path="scripts/aoss_stage_a/source_driver.py",
            source_driver_file=driver,
        )


def test_prepare_rejects_missing_source_driver_file(tmp_path):
    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_SOURCE_DRIVER_FILE_MISSING",
    ):
        prepare_execution_identity_candidate(
            interpreter_path="/opt/python/3.12.3/bin/python",
            interpreter_sha256=SHA_A,
            argv=["-m", "definitely_missing_aoss_driver_901"],
            working_directory=str(tmp_path),
            destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
            attempt_id="aoss-stage-a-attempt-0001",
            recipe_catalog_sha256=CATALOG_SHA,
            environment_candidate_record_sha256=SHA_C,
            source_driver_path="scripts/aoss_stage_a/source_driver.py",
            source_driver_file=tmp_path / "scripts" / "aoss_stage_a" / "source_driver.py",
        )


def test_source_driver_digest_is_derived_from_real_file(tmp_path):
    driver = _driver(tmp_path)
    driver.write_bytes(b"print('candidate')\n")
    candidate = prepare_execution_identity_candidate(
        interpreter_path="/opt/python/3.12.3/bin/python",
        interpreter_sha256=SHA_A,
        argv=[
            "scripts/aoss_stage_a/source_driver.py",
            "--acp-root",
            "/srv/agent-control-plane",
            "--recipe-class",
            "normal_completion",
            "--run-id",
            "run-0001",
            "--output",
            "/srv/aoss-stage-a/retained/attempt-0001/source-driver-result.json",
        ],
        working_directory=str(tmp_path),
        destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
        attempt_id="aoss-stage-a-attempt-0001",
        recipe_catalog_sha256=CATALOG_SHA,
        environment_candidate_record_sha256=SHA_C,
        source_driver_path="scripts/aoss_stage_a/source_driver.py",
        source_driver_file=driver,
    )
    assert candidate["source_driver_identity"]["path"] == "scripts/aoss_stage_a/source_driver.py"
    assert (
        candidate["source_driver_identity"]["sha256"] == __import__("hashlib").sha256(driver.read_bytes()).hexdigest()
    )
    report = validate_execution_identity_candidate(candidate, source_driver_file=driver)
    assert report["source_driver_candidate_identity"] == {
        "path": candidate["source_driver_identity"]["path"],
        "sha256": candidate["source_driver_identity"]["sha256"],
    }


def test_structural_validation_rejects_removed_source_driver_identity(tmp_path):
    candidate = _candidate(tmp_path)
    del candidate["source_driver_identity"]

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_SOURCE_DRIVER_MISSING",
    ):
        validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
        )


def test_validation_rejects_missing_driver_even_if_candidate_is_handcrafted(tmp_path):
    candidate = _candidate(tmp_path)
    driver = _driver(tmp_path)
    driver.unlink()

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_SOURCE_DRIVER_FILE_MISSING",
    ):
        validate_execution_identity_candidate(
            candidate,
            source_driver_file=driver,
        )


def test_validation_rejects_substituted_driver_bytes(tmp_path):
    candidate = _candidate(tmp_path)
    driver = _driver(tmp_path)
    driver.write_bytes(b"# substituted bytes\n")

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_SOURCE_DRIVER_SHA_MISMATCH",
    ):
        validate_execution_identity_candidate(candidate, source_driver_file=driver)
