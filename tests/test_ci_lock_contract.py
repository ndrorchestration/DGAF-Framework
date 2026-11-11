from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "requirements-ci.txt"
WORKFLOW = ROOT / ".github" / "workflows" / "python-tests.yml"
CONTROL_PLANE_WORKFLOW = ROOT / ".github" / "workflows" / "control-plane-contract.yml"
CANONICAL_PROFILE_WORKFLOW = ROOT / ".github" / "workflows" / "canonical-treatment-profile.yml"
AOSS_STAGE_A_FOUNDATION_WORKFLOW = ROOT / ".github" / "workflows" / "aoss-stage-a-collector-foundation.yml"
AOSS_STAGE_A_PREDATA_WORKFLOW = ROOT / ".github" / "workflows" / "aoss-v0-6-stage-a-predata-readiness.yml"
AOSS_STAGE_A_AUTH_WORKFLOW = ROOT / ".github" / "workflows" / "aoss-v0-6-stage-a-collection-authorization.yml"
TRACK_A_EPOCH_002_RUNNER_WORKFLOW = ROOT / ".github" / "workflows" / "track-a-epoch-002-primary-analysis-runner.yml"
TRACK_A_EPOCH_002_RESULT_SEMANTICS_WORKFLOW = (
    ROOT / ".github" / "workflows" / "track-a-epoch-002-result-record-semantics.yml"
)
TRACK_A_EPOCH_002_LOCKED_RESULT_ADMISSION_WORKFLOW = (
    ROOT / ".github" / "workflows" / "track-a-epoch-002-locked-result-admission.yml"
)
TRACK_A_EPOCH_002_INTERPRETATION_WORKFLOW = ROOT / ".github" / "workflows" / "track-a-epoch-002-interpretation.yml"
TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION_WORKFLOW = (
    ROOT / ".github" / "workflows" / "track-a-epoch-002-post-interpretation-disposition.yml"
)
TRACK_A_EPOCH_002_OPERATOR_ADMISSION_WORKFLOW = (
    ROOT / ".github" / "workflows" / "track-a-epoch-002-operator-admission.yml"
)
TRACK_A_EPOCH_002_MATERIALIZATION_WORKFLOW = ROOT / ".github" / "workflows" / "track-a-epoch-002-materialization.yml"
CONTROL_PLANE_LOCK = ROOT / "requirements-ci-control-plane-py312-ubuntu2404-x64.lock"
BOOTSTRAP = ROOT / "scripts" / "bootstrap_ci_pip.sh"

EXPECTED_SOURCE_SHA256 = "71c54083bbfe492fc720a1d10269227926d1cd4ec7cfc5c0f46ce98ea53cd31b"
EXPECTED_LOCKS = {
    "3.10": (
        ROOT / "requirements-ci-py310-ubuntu2404-x64.lock",
        "94c433176ed0b10d6b34ea349ac04f56fc6ebf6dbc237afc7c12d86214e720ca",
        "8e755aeea828f521856320292a5494679e551f5ea48017ae943dbf8498fef952",
    ),
    "3.11": (
        ROOT / "requirements-ci-py311-ubuntu2404-x64.lock",
        "f26dd40766f8b792b8fdfe8db4fd9e02ea3103d849e83c768758dca53bf31065",
        "b88eb9fedae08705492fcdb052d10317db079f0f8945d202874cea1bde742482",
    ),
    "3.12": (
        ROOT / "requirements-ci-py312-ubuntu2404-x64.lock",
        "7d518736493f261966c5b39b7ecce0fe6bf3c81b797dc667d3fce4c265c28f05",
        "229bd468723ad5d6d001f0b1109ebc68e8916e9b476016f70163b9736e7920d9",
    ),
}
CONTROL_PLANE_LOCK_SHA256 = "f3ab0b096d3c6cec1cabe69664c01fc2c3d05795f9c2dead1ef0e28fd0e19065"
CONTROL_PLANE_RESOLVED_SET_SHA256 = "f1e5f7d5c1f67c016915ed9a9307f7a8fe10233fc1aea6151f8ecfceb66e94e8"
CONTROL_PLANE_OVERLAY_SHA256 = "0f7011f8e062802ab40c0bcfa852c079b99f0097f1a3ea085d2eacfef42263f9"
PIP_WHEEL_SHA256 = "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e"
PIN_RE = re.compile(r"^([A-Za-z0-9_.-]+)==([^\s\\]+)(?:\s+\\)?$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def direct_pins() -> dict[str, str]:
    pins: dict[str, str] = {}
    for raw in SOURCE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # This exact PEP 508 marker means the scanner remains mandatory for
        # Python 3.11/3.12 but is absent from the Python 3.10 workload lock.
        if line.startswith("pip-audit=="):
            assert line == 'pip-audit==2.10.1 ; python_version >= "3.11"', line
            line = "pip-audit==2.10.1"
        match = PIN_RE.fullmatch(line)
        assert match, line
        name = canonical(match.group(1))
        assert name not in pins, "duplicate direct CI requirement"
        pins[name] = match.group(2)
    return pins


def lock_pins(path: Path) -> dict[str, tuple[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    pins: dict[str, tuple[str, str]] = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue
        match = PIN_RE.fullmatch(line)
        assert match and line.endswith("\\"), line
        assert i + 1 < len(lines)
        hash_line = lines[i + 1].strip()
        assert re.fullmatch(r"--hash=sha256:[0-9a-f]{64}", hash_line), hash_line
        key = canonical(match.group(1))
        assert key not in pins, key
        pins[key] = (match.group(2), hash_line.split(":", 1)[1])
        i += 2
    return pins


def test_source_and_canonical_lock_identities_are_bound() -> None:
    assert sha256(SOURCE) == EXPECTED_SOURCE_SHA256
    for minor, (path, expected_lock_sha, resolved_set_sha) in EXPECTED_LOCKS.items():
        text = path.read_text(encoding="utf-8")
        assert sha256(path) == expected_lock_sha
        assert f"# source_sha256: {EXPECTED_SOURCE_SHA256}" in text
        assert f"# python_minor: {minor}" in text
        assert "# runner_os: ubuntu-24.04" in text
        assert "# runner_arch: x64" in text
        assert "# resolver: pip==26.2.1" in text
        assert "# binary_policy: only-binary=:all:" in text
        assert f"# resolved_set_sha256: {resolved_set_sha}" in text


def test_every_direct_ci_pin_is_exactly_represented_in_every_lock() -> None:
    direct = direct_pins()
    assert len(direct) == 18
    assert direct["pip-audit"] == "2.10.1"
    assert direct["msgpack"] == "1.2.3"
    assert direct["requests"] == "2.34.2"
    for minor, (path, _, _) in EXPECTED_LOCKS.items():
        locked = lock_pins(path)
        for name, version in direct.items():
            if minor == "3.10" and name == "pip-audit":
                assert "pip-audit" not in locked
                assert "filelock" not in locked
                continue
            assert name in locked, (minor, name)
            assert locked[name][0] == version, (minor, name, version)
        if minor in ("3.11", "3.12"):
            assert locked["filelock"][0] == "4.2.9"
    assert direct["pip-audit"] == "2.10.1"


def test_scanner_python_marker_is_exact_and_required_security_job_is_unchanged() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    marker = 'pip-audit==2.10.1 ; python_version >= "3.11"'
    assert source.splitlines().count(marker) == 1
    assert "pip-audit==2.10.1\n" not in source
    assert "requests==2.34.2\n" in source
    assert "msgpack==1.2.3\n" in source

    security = WORKFLOW.read_text(encoding="utf-8").split("  security-scan:", 1)[1]
    assert "python-version: '3.11'" in security
    assert "requirements-ci-py311-ubuntu2404-x64.lock" in security
    assert "python -m pip_audit --local --format=json --output pip-audit-report.json" in security
    assert "continue-on-error: true" not in security


def test_every_lock_requirement_is_hash_bound() -> None:
    for path, _, _ in EXPECTED_LOCKS.values():
        locked = lock_pins(path)
        assert locked
        assert all(re.fullmatch(r"[0-9a-f]{64}", digest) for _, digest in locked.values())


def test_python_workflow_consumes_interpreter_scoped_hash_locks() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert workflow.count("runs-on: ubuntu-24.04") == 4
    assert "python-version: ['3.10', '3.11', '3.12']" in workflow
    assert 'ci_lock="requirements-ci-py${python_minor//./}-ubuntu2404-x64.lock"' in workflow
    assert 'python_minor="${{ matrix.python-version }}"' in workflow
    assert workflow.count("--require-hashes") == 4
    assert workflow.count("--only-binary=:all:") == 4
    assert workflow.count("bash scripts/bootstrap_ci_pip.sh") == 4
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert "requirements-ci.txt pyyaml" not in workflow


def test_control_plane_augmented_lock_is_bound_and_hash_complete() -> None:
    text = CONTROL_PLANE_LOCK.read_text(encoding="utf-8")
    assert sha256(CONTROL_PLANE_LOCK) == CONTROL_PLANE_LOCK_SHA256
    assert f"# source_sha256: {EXPECTED_SOURCE_SHA256}" in text
    assert f"# overlay_sha256: {CONTROL_PLANE_OVERLAY_SHA256}" in text
    assert f"# resolved_set_sha256: {CONTROL_PLANE_RESOLVED_SET_SHA256}" in text
    assert "# python_minor: 3.12" in text
    assert "# runner_os: ubuntu-24.04" in text
    assert "# resolver: pip==26.2.1" in text

    locked = lock_pins(CONTROL_PLANE_LOCK)
    assert len(locked) == 66
    assert locked["pandas"][0] == "3.0.5"
    assert all(re.fullmatch(r"[0-9a-f]{64}", digest) for _, digest in locked.values())


def test_control_plane_workflow_consumes_augmented_hash_lock() -> None:
    workflow = CONTROL_PLANE_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-control-plane-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt pandas==3.0.5" not in workflow
    assert "assert pandas.__version__ == '3.0.5'" in workflow


def test_canonical_treatment_profile_workflow_uses_bound_py312_lock() -> None:
    workflow = CANONICAL_PROFILE_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "python-version: '3.12'" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow


def test_aoss_stage_a_foundation_uses_bound_py312_lock_without_collection_promotion() -> None:
    workflow = AOSS_STAGE_A_FOUNDATION_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.3'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert 'assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"' in workflow
    assert 'assert report["outcomes_generated"] is False' in workflow
    assert 'assert report["scientific_n_increment"] == 0' in workflow


def test_aoss_stage_a_predata_readiness_uses_bound_py312_lock_without_authorization() -> None:
    workflow = AOSS_STAGE_A_PREDATA_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.3'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert "ready only for separate authorization review" in workflow.lower()
    assert "validate_aoss_v0_6_stage_a_predata_readiness.py --assert-ready" in workflow
    assert "run_aoss_v0_6_stage_a.py" not in workflow


def test_aoss_stage_a_collection_authorization_uses_bound_py312_lock_without_authority_drift() -> None:
    workflow = AOSS_STAGE_A_AUTH_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.3'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert 'CHANGED="$(git diff --name-only "$BASE_SHA" "$HEAD_SHA")"' in workflow
    assert "--validate-state" in workflow
    assert "authorization and precollection receipt cannot change in one PR" in workflow
    assert workflow.count("      - 'requirements-ci.txt'") == 2
    assert workflow.count("      - 'requirements-ci-py312-ubuntu2404-x64.lock'") == 2
    assert workflow.count("      - 'scripts/bootstrap_ci_pip.sh'") == 2
    assert workflow.count("      - 'tests/test_ci_lock_contract.py'") == 2


def test_track_a_epoch002_runner_tooling_uses_bound_py312_lock_without_empirical_execution() -> None:
    workflow = TRACK_A_EPOCH_002_RUNNER_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.3'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert workflow.count("      - 'requirements-ci-py312-ubuntu2404-x64.lock'") == 2
    assert "Run runner unit tests with synthetic inputs only" in workflow
    assert "Prove workflow never executes empirical analysis" in workflow
    assert "PRIMARY_ANALYSIS_EXECUTION=NOT_PERFORMED" in workflow
    assert "SCIENTIFIC_N_INCREMENT=0" in workflow


def test_track_a_epoch002_result_semantics_uses_bound_py312_lock_without_authority() -> None:
    workflow = TRACK_A_EPOCH_002_RESULT_SEMANTICS_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.0'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert "Validate semantic policy coherence" in workflow
    assert "Prove semantic tooling cannot create authority or execute science" in workflow
    assert "RESULT_RECORD_SEMANTIC_TOOLING_NONAUTHORIZING=TRUE" in workflow
    assert "SCIENTIFIC_N_INCREMENT=0" in workflow


def test_track_a_epoch002_locked_result_admission_uses_bound_lock_and_accepted_state_routing() -> None:
    workflow = TRACK_A_EPOCH_002_LOCKED_RESULT_ADMISSION_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.3'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert workflow.count("      - 'requirements-ci-py312-ubuntu2404-x64.lock'") == 2
    assert "value=accepted_state" in workflow
    assert "Validate accepted immutable result state" in workflow
    assert "Run synthetic-only result-admission tests" in workflow
    assert "Prove CI has no empirical execution surface" in workflow
    assert "SCIENTIFIC_N_INCREMENT=0" in workflow


def test_track_a_epoch002_interpretation_uses_bound_lock_and_accepted_state_routing() -> None:
    workflow = TRACK_A_EPOCH_002_INTERPRETATION_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.3'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert workflow.count("      - 'requirements-ci-py312-ubuntu2404-x64.lock'") == 2
    assert "value=accepted_state" in workflow
    assert "Validate accepted immutable interpretation state" in workflow
    assert "Run synthetic-only interpretation tests" in workflow
    assert "Prove CI has no empirical interpretation input" in workflow
    assert "SCIENTIFIC_N_INCREMENT=0" in workflow


def test_track_a_epoch002_post_interpretation_disposition_uses_bound_lock_and_closed_state_routing() -> None:
    workflow = TRACK_A_EPOCH_002_POST_INTERPRETATION_DISPOSITION_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.3'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert workflow.count("      - 'requirements-ci-py312-ubuntu2404-x64.lock'") == 2
    assert "value=accepted_state" in workflow
    assert "Validate accepted immutable disposition state" in workflow
    assert "Run synthetic-only disposition tests" in workflow
    assert "Prove CI has no private numerical interpretation input" in workflow
    assert "NEW_EMPIRICAL_EPOCH_AUTHORIZED=FALSE" in workflow
    assert "SCIENTIFIC_N_INCREMENT=0" in workflow


def test_track_a_epoch002_operator_admission_uses_bound_lock_without_authority_promotion() -> None:
    workflow = TRACK_A_EPOCH_002_OPERATOR_ADMISSION_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.0'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert workflow.count("      - 'requirements-ci-py312-ubuntu2404-x64.lock'") == 1
    assert "tests/test_track_a_epoch_002_operator_codespace_admission.py" in workflow
    assert "tests/test_track_a_epoch_002_operator_admission_preparer.py" in workflow
    assert "workflow_dispatch: {}" in workflow


def test_epoch002_materialization_uses_bound_lock_and_post_receipt_route() -> None:
    workflow = TRACK_A_EPOCH_002_MATERIALIZATION_WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-24.04" in workflow
    assert "python-version: '3.12.3'" in workflow
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow
    assert "bash scripts/bootstrap_ci_pip.sh" in workflow
    assert "requirements-ci-py312-ubuntu2404-x64.lock" in workflow
    assert "--require-hashes" in workflow
    assert "--only-binary=:all:" in workflow
    assert "python -m pip install -r requirements-ci.txt" not in workflow
    assert workflow.count("      - 'requirements-ci-py312-ubuntu2404-x64.lock'") == 2
    assert "value=post_receipt_tooling" in workflow
    assert "Validate post-admission immutable materialization state" in workflow
    assert "TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT=ESTABLISHED_PRESERVED" in workflow
    assert "TRACK_A_EPOCH_002_SUCCESSOR_STATE=OUT_OF_SCOPE_PRESERVED" in workflow
    assert "MATERIALIZATION_TOOLING_EXECUTES_PRIMARY_ANALYSIS=FALSE" in workflow
    assert "SCIENTIFIC_N_INCREMENT=0" in workflow
    assert "CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED" in workflow
    expected_maintenance_occurrences = {
        "requirements-ci.txt": 2,
        "requirements-ci-py312-ubuntu2404-x64.lock": 2,
        "scripts/bootstrap_ci_pip.sh": 1,
        "tests/test_ci_lock_contract.py": 2,
    }
    for path, expected_count in expected_maintenance_occurrences.items():
        assert workflow.count(f"            '{path}'") == expected_count


def test_bootstrap_verifies_exact_pip_wheel_before_install() -> None:
    bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
    assert 'PIP_VERSION="26.2.1"' in bootstrap
    assert f'PIP_SHA256="{PIP_WHEEL_SHA256}"' in bootstrap
    assert "--no-index" in bootstrap
    assert "--find-links" in bootstrap
    assert "sha256sum" in bootstrap


def test_track_a_coordinated_dependency_maintenance_is_exact_bundle_only() -> None:
    workflows = (
        ROOT / ".github" / "workflows" / "track-a-epoch-002-primary-analysis-authorization.yml",
        ROOT / ".github" / "workflows" / "track-a-epoch-002-dataset-lock.yml",
        ROOT / ".github" / "workflows" / "track-a-epoch-002-materialization.yml",
    )
    expected = (
        ".github/workflows/track-a-epoch-002-primary-analysis-authorization.yml",
        ".github/workflows/track-a-epoch-002-dataset-lock.yml",
        ".github/workflows/track-a-epoch-002-materialization.yml",
        "requirements-ci.txt",
        "requirements-ci-py310-ubuntu2404-x64.lock",
        "requirements-ci-py311-ubuntu2404-x64.lock",
        "requirements-ci-py312-ubuntu2404-x64.lock",
        "requirements-ci-control-plane-py312-ubuntu2404-x64.lock",
        "tests/test_ci_lock_contract.py",
        "tests/test_track_a_epoch_002_primary_analysis_authorization.py",
    )

    for workflow in workflows:
        source = workflow.read_text(encoding="utf-8")
        assert source.count("TRACK_A_COORDINATED_DEPENDENCY_MAINTENANCE=EXACT_BUNDLE") == 1
        assert source.count("coordinated dependency maintenance must match the frozen 10-path bundle exactly") == 1
        before, marker, remainder = source.partition("coordinated_bundle=(\n")
        assert marker, workflow
        assert "coordinated_bundle=(" not in before
        body, end_marker, after = remainder.partition("          )\n          coordinated=true")
        assert end_marker, workflow
        assert "coordinated_bundle=(" not in after
        observed = tuple(line.strip().strip("'\\\"") for line in body.splitlines() if line.strip())
        assert observed == expected, workflow


def test_track_a_epoch002_lock_only_event_triggers_cover_all_admitted_locks() -> None:
    """Check exact path filters; this is not a hosted lock-only webhook test."""
    locks = (
        "requirements-ci-py310-ubuntu2404-x64.lock",
        "requirements-ci-py311-ubuntu2404-x64.lock",
        "requirements-ci-py312-ubuntu2404-x64.lock",
        "requirements-ci-control-plane-py312-ubuntu2404-x64.lock",
    )
    workflows = (
        ("track-a-epoch-002-primary-analysis-authorization.yml", ("pull_request", "push")),
        ("track-a-epoch-002-dataset-lock.yml", ("pull_request",)),
        ("track-a-epoch-002-materialization.yml", ("pull_request", "push")),
    )
    for filename, events in workflows:
        source = (ROOT / ".github" / "workflows" / filename).read_text(
            encoding="utf-8"
        )
        trigger_source = source.split("\njobs:\n", 1)[0]
        for event in events:
            delimiter = f"\n  {event}:\n"
            assert delimiter in trigger_source, (filename, event)
            event_body = trigger_source.split(delimiter, 1)[1].split("\n  ", 1)[0]
            assert "\n    paths:\n" in event_body, (filename, event)
            paths_body = event_body.split("\n    paths:\n", 1)[1].split("\n    ", 1)[0]
            paths = [
                line.strip()[2:].strip("'\"")
                for line in paths_body.splitlines()
                if line.strip().startswith("- ")
            ]
            for lock in locks:
                assert paths.count(lock) == 1, (filename, event, lock)
            assert "requirements-ci-rogue.lock" not in paths
        if events == ("pull_request",):
            assert "\n  push:\n" not in trigger_source
