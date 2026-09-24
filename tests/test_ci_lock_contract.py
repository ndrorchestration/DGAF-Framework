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
TRACK_A_EPOCH_002_MATERIALIZATION_WORKFLOW = (
    ROOT / ".github" / "workflows" / "track-a-epoch-002-materialization.yml"
)
CONTROL_PLANE_LOCK = ROOT / "requirements-ci-control-plane-py312-ubuntu2404-x64.lock"
BOOTSTRAP = ROOT / "scripts" / "bootstrap_ci_pip.sh"

EXPECTED_SOURCE_SHA256 = "1abada5e8dabbcb6706e33c5b5dfa30c45b784e8b9a9b18166a52562b5c3dfa9"
EXPECTED_LOCKS = {
    "3.10": (
        ROOT / "requirements-ci-py310-ubuntu2404-x64.lock",
        "18206a193da4de952c25d5384187edd82fa134eb4a9a3c5322f6999258a6d05c",
        "7b7f6edb9c686b921d1450aabc3c8345ec6cb41ca84a6feadd16210dafb3c4e3",
    ),
    "3.11": (
        ROOT / "requirements-ci-py311-ubuntu2404-x64.lock",
        "ff5111b07dc1949c06a6a364722bdece93f1f10e70a0c6e719704c091096344d",
        "dabebe2879148dfed404f1163f17c248ba01ce7b98778782f9c6c12f9acac14d",
    ),
    "3.12": (
        ROOT / "requirements-ci-py312-ubuntu2404-x64.lock",
        "d131e53fc8c8506ee282f4082eae451af77b45c08c37b69fce091b4bca865197",
        "7931d5f2ad8b22cbd71dea2cc60ce4c1f8a3b4ccde34a46be0fa5e284526fba9",
    ),
}
CONTROL_PLANE_LOCK_SHA256 = "208c68c614cbb4a3e17dfc7eaeffdd39b57ee3688f3b662c7c22e7e64d802b70"
CONTROL_PLANE_RESOLVED_SET_SHA256 = "e18eb434f83c2f0e2801f218c77b1fbb8db76526dc57c57a734b3f12a3ed7b41"
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
        match = PIN_RE.fullmatch(line)
        assert match, line
        pins[canonical(match.group(1))] = match.group(2)
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
    assert len(direct) == 15
    for path, _, _ in EXPECTED_LOCKS.values():
        locked = lock_pins(path)
        for name, version in direct.items():
            assert name in locked
            assert locked[name][0] == version


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


def test_track_a_epoch002_materialization_uses_bound_lock_and_post_receipt_maintenance_route() -> None:
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
    for path in (
        "requirements-ci.txt",
        "requirements-ci-py312-ubuntu2404-x64.lock",
        "scripts/bootstrap_ci_pip.sh",
        "tests/test_ci_lock_contract.py",
    ):
        assert workflow.count(f"            '{path}'") == 1


def test_bootstrap_verifies_exact_pip_wheel_before_install() -> None:
    bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
    assert 'PIP_VERSION="26.2.1"' in bootstrap
    assert f'PIP_SHA256="{PIP_WHEEL_SHA256}"' in bootstrap
    assert "--no-index" in bootstrap
    assert "--find-links" in bootstrap
    assert "sha256sum" in bootstrap
