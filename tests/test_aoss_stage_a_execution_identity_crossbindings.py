import hashlib
from pathlib import Path

import pytest

import scripts.aoss_stage_a.execution_identity_candidate as identity
from scripts.aoss_stage_a.external_admission_decision_intake import (
    ExternalAdmissionDecisionIntakeError,
    prepare_external_admission_decision_intake,
)
from scripts.aoss_stage_a.external_admission_decision_intake import (
    record_sha256 as intake_record_sha256,
)
from scripts.aoss_stage_a.installed_environment_evidence import (
    capture_installed_environment_evidence_candidate,
)
from scripts.aoss_stage_a.runtime_binding import RuntimeFacts

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "registry/aoss_v0_6_stage_a_source_driver_recipe_catalog_v1.json"
CATALOG_SHA = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
EXTERNAL_SHA = "d" * 64
REAL_ACP_VERIFIER = identity._verify_frozen_acp_checkout


@pytest.fixture(autouse=True)
def _stub_frozen_acp_verification(monkeypatch):
    monkeypatch.setattr(identity, "_verify_frozen_acp_checkout", lambda _path: None, raising=False)


def _facts(root: Path, *, executable: Path | None = None):
    interpreter = executable or _interpreter(root)
    return RuntimeFacts(
        implementation="cpython",
        version="3.12.3",
        platform_system="TestOS",
        platform_machine="x86_64",
        executable=str(interpreter.resolve()),
        prefix=str(root.resolve()),
        base_prefix=str(root.resolve()),
    )


def _interpreter(root: Path, name: str = "python.exe") -> Path:
    path = root / name
    path.write_bytes(b"exact-interpreter-candidate\n")
    return path


def _driver(_root: Path) -> Path:
    return ROOT / "scripts" / "aoss_stage_a" / "source_driver.py"


def _acp_root(root: Path, name: str = "agent-control-plane") -> Path:
    path = root / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def _output(root: Path, attempt: str = "aoss-stage-a-attempt-0001") -> Path:
    path = root / "retained" / attempt / "source-driver-result.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _kwargs(root: Path, *, interpreter: Path | None = None):
    interpreter = interpreter or _interpreter(root)
    driver = _driver(root)
    acp = _acp_root(root)
    attempt = "aoss-stage-a-attempt-0001"
    output = _output(root, attempt)
    return {
        "interpreter_path": str(interpreter.resolve()),
        "interpreter_sha256": hashlib.sha256(interpreter.read_bytes()).hexdigest(),
        "argv": [
            "scripts/aoss_stage_a/source_driver.py",
            "--acp-root",
            str(acp.resolve()),
            "--recipe-class",
            "normal_completion",
            "--run-id",
            attempt,
            "--output",
            str(output.resolve()),
        ],
        "working_directory": str(ROOT.resolve()),
        "destination_uri": output.resolve().as_uri(),
        "attempt_id": attempt,
        "recipe_catalog_sha256": CATALOG_SHA,
        "environment_candidate_record_sha256": "c" * 64,
        "source_driver_path": "scripts/aoss_stage_a/source_driver.py",
        "source_driver_file": driver,
        "recipe_catalog_file": CATALOG,
    }


def _candidate(root: Path):
    return identity.prepare_execution_identity_candidate(**_kwargs(root))


def _set_option(candidate: dict, flag: str, value: str) -> None:
    argv = candidate["executable_identity"]["argv"]
    index = argv.index(flag)
    argv[index + 1] = value


def test_prepare_rejects_interpreter_digest_not_matching_file(tmp_path):
    kwargs = _kwargs(tmp_path)
    kwargs["interpreter_sha256"] = "b" * 64

    with pytest.raises(identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_INTERPRETER_SHA_MISMATCH"):
        identity.prepare_execution_identity_candidate(**kwargs)


def test_validation_rejects_interpreter_bytes_changed_after_prepare(tmp_path):
    candidate = _candidate(tmp_path)
    Path(candidate["executable_identity"]["interpreter_path"]).write_bytes(b"substituted\n")

    with pytest.raises(identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_INTERPRETER_SHA_MISMATCH"):
        identity.validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
            recipe_catalog_file=CATALOG,
        )


def test_candidate_records_and_reverifies_frozen_acp_checkout_path(tmp_path):
    candidate = _candidate(tmp_path)
    expected = str((tmp_path / "agent-control-plane").resolve())
    assert candidate["source"]["checkout_path"] == expected

    other = _acp_root(tmp_path, "other-agent-control-plane")
    _set_option(candidate, "--acp-root", str(other.resolve()))
    with pytest.raises(identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_ACP_ROOT_PATH_MISMATCH"):
        identity.validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
            recipe_catalog_file=CATALOG,
        )


def test_validation_rejects_run_id_attempt_mismatch(tmp_path):
    candidate = _candidate(tmp_path)
    _set_option(candidate, "--run-id", "different-attempt")

    with pytest.raises(identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_RUN_ID_ATTEMPT_MISMATCH"):
        identity.validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
            recipe_catalog_file=CATALOG,
        )


def test_validation_rejects_output_destination_mismatch(tmp_path):
    candidate = _candidate(tmp_path)
    other = tmp_path / "retained" / "other-attempt" / "source-driver-result.json"
    other.parent.mkdir(parents=True)
    _set_option(candidate, "--output", str(other.resolve()))

    with pytest.raises(
        identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_OUTPUT_DESTINATION_MISMATCH"
    ):
        identity.validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
            recipe_catalog_file=CATALOG,
        )


def test_prepare_rejects_unreserved_output_parent(tmp_path):
    kwargs = _kwargs(tmp_path)
    missing = tmp_path / "not-reserved" / "source-driver-result.json"
    output_index = kwargs["argv"].index("--output") + 1
    kwargs["argv"][output_index] = str(missing.resolve())
    kwargs["destination_uri"] = missing.resolve().as_uri()

    with pytest.raises(identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_OUTPUT_PARENT_MISSING"):
        identity.prepare_execution_identity_candidate(**kwargs)


def test_validation_rejects_output_that_already_exists(tmp_path):
    candidate = _candidate(tmp_path)
    output = Path(
        candidate["executable_identity"]["argv"][candidate["executable_identity"]["argv"].index("--output") + 1]
    )
    output.write_bytes(b"preexisting\n")

    with pytest.raises(identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_OUTPUT_ALREADY_EXISTS"):
        identity.validate_execution_identity_candidate(
            candidate,
            source_driver_file=_driver(tmp_path),
            recipe_catalog_file=CATALOG,
        )


def test_external_intake_rejects_environment_execution_interpreter_path_mismatch(tmp_path):
    environment_interpreter = _interpreter(tmp_path, "environment-python.exe")
    execution_interpreter = _interpreter(tmp_path, "execution-python.exe")
    environment = capture_installed_environment_evidence_candidate(
        observed_at="2026-10-15T16:13:16Z",
        facts=_facts(tmp_path, executable=environment_interpreter),
    )
    kwargs = _kwargs(tmp_path, interpreter=execution_interpreter)
    kwargs["environment_candidate_record_sha256"] = intake_record_sha256(environment)
    candidate = identity.prepare_execution_identity_candidate(**kwargs)

    with pytest.raises(
        ExternalAdmissionDecisionIntakeError,
        match="EXTERNAL_DECISION_ENVIRONMENT_INTERPRETER_PATH_MISMATCH",
    ):
        prepare_external_admission_decision_intake(
            environment_candidate=environment,
            execution_identity_candidate=candidate,
            reviewer_identity="external-reviewer:example",
            reviewed_at="2026-10-15T17:00:00Z",
            external_record_uri="https://example.invalid/aoss-stage-a/decision.json",
            external_record_sha256=EXTERNAL_SHA,
            independence_claimed=False,
            independence_basis=None,
            installed_environment_decision="BLOCKED",
            source_driver_executable_decision="BLOCKED",
            destination_attempt_decision="BLOCKED",
        )


def test_prepare_rejects_checkout_without_frozen_git_identity(tmp_path, monkeypatch):
    monkeypatch.setattr(identity, "_verify_frozen_acp_checkout", REAL_ACP_VERIFIER)
    with pytest.raises(identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_ACP_CHECKOUT_INVALID"):
        identity.prepare_execution_identity_candidate(**_kwargs(tmp_path))


def test_validation_reverifies_checkout_after_prepare(tmp_path, monkeypatch):
    candidate = _candidate(tmp_path)
    monkeypatch.setattr(identity, "_verify_frozen_acp_checkout", REAL_ACP_VERIFIER)
    with pytest.raises(identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_ACP_CHECKOUT_INVALID"):
        identity.validate_execution_identity_candidate(candidate)


def test_validation_rejects_dangling_output_symlink(tmp_path):
    candidate = _candidate(tmp_path)
    output = Path(candidate["executable_identity"]["argv"][-1])
    try:
        output.symlink_to(output.parent / "missing-result.json")
    except OSError:
        pytest.skip("symlink creation unavailable on this platform")
    candidate["destination_identity"]["uri"] = output.resolve().as_uri()
    with pytest.raises(identity.ExecutionIdentityCandidateError, match="EXECUTION_IDENTITY_OUTPUT_ALREADY_EXISTS"):
        identity.validate_execution_identity_candidate(candidate)
