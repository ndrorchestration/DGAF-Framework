from pathlib import Path

WORKFLOW_PATH = Path(".github/workflows/python-tests.yml")
REQUIREMENTS_CI_PATH = Path("requirements-ci.txt")
HISTORICAL_EPOCH_001_MATERIALIZER = "scripts/materialize_track_a_epoch_001_unblinded_input.py"
BANDIT_TARGETS = "bandit -r components/ scripts/ api/ experiments/"


def _workflow_text() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def _between(text: str, start: str, end: str) -> str:
    assert start in text, f"missing start marker: {start}"
    assert end in text, f"missing end marker: {end}"
    return text.split(start, 1)[1].split(end, 1)[0]


def test_quality_workflow_triggers_cover_contract_and_config_changes() -> None:
    text = _workflow_text()
    push = _between(text, "  push:\n", "  pull_request:\n")
    pull_request = _between(text, "  pull_request:\n", "\njobs:\n")

    for block in (push, pull_request):
        assert "- '.flake8'" in block
        assert "- '.github/workflows/python-tests.yml'" in block


def test_primary_quality_steps_are_blocking() -> None:
    text = _workflow_text()
    quality_block = _between(
        text,
        "    - name: Lint with flake8\n",
        "    - name: Prove quality tools reject controlled violations\n",
    )

    assert "--exit-zero" not in quality_block
    assert "continue-on-error:" not in quality_block

    expected_commands = (
        "flake8 components --count --select=E9,F63,F82 --show-source --statistics",
        "flake8 components --count --statistics --max-line-length=120",
        "black --check components/ tests/ --line-length=120",
        "isort --check-only components/ tests/ --profile=black",
        "mypy components/ --ignore-missing-imports --no-implicit-optional",
    )
    for command in expected_commands:
        assert command in quality_block


def test_negative_controls_cover_each_blocking_quality_tool() -> None:
    text = _workflow_text()
    negative_block = _between(
        text,
        "    - name: Prove quality tools reject controlled violations\n",
        "    - name: Run pytest with coverage and preserve diagnostics\n",
    )

    assert "if: matrix.python-version == '3.12'" in negative_block
    assert 'if [ "$status" -eq 0 ]; then' in negative_block

    for command in (
        "run_negative flake8 flake8",
        "run_negative black black --check",
        "run_negative isort isort --check-only",
        "run_negative mypy mypy",
    ):
        assert command in negative_block


def test_bandit_full_report_and_blocking_threshold_contract() -> None:
    text = _workflow_text()
    full_report = _between(
        text,
        "    - name: Run full first-party Bandit report\n",
        "    - name: Block medium-or-higher Bandit findings with medium-or-higher confidence\n",
    )
    blocking = _between(
        text,
        "    - name: Block medium-or-higher Bandit findings with medium-or-higher confidence\n",
        "    - name: Audit installed CI environment with pip-audit\n",
    )

    assert BANDIT_TARGETS in full_report
    assert "-f json -o bandit-report.json" in full_report
    assert "-f txt | tee bandit-report.txt" in full_report
    assert "bandit-report.status" in full_report
    assert "-x " not in full_report
    assert "--exclude " not in full_report
    assert HISTORICAL_EPOCH_001_MATERIALIZER not in full_report

    assert BANDIT_TARGETS in blocking
    assert "-ll -ii" in blocking
    assert f"-x {HISTORICAL_EPOCH_001_MATERIALIZER}" in blocking
    assert "continue-on-error:" not in blocking
    assert "--exit-zero" not in blocking


def test_dependency_audit_is_pinned_noninteractive_and_blocking() -> None:
    requirements = REQUIREMENTS_CI_PATH.read_text(encoding="utf-8")
    assert "pip-audit==2.10.1" in requirements
    assert "safety==" not in requirements

    text = _workflow_text()
    audit = _between(
        text,
        "    - name: Audit installed CI environment with pip-audit\n",
        "    - name: Upload security reports\n",
    )

    assert "python -m pip_audit --local --format=json --output pip-audit-report.json" in audit
    assert "python -m pip_audit --local --format=columns | tee pip-audit-report.txt" in audit
    assert "pip-audit-report.status" in audit
    assert 'if [ "$json_status" -ne 0 ] || [ "$text_status" -ne 0 ]; then' in audit
    assert "continue-on-error:" not in audit
    assert "|| true" not in audit
    assert "safety check" not in text
    assert "safety scan" not in text


def test_advisory_exceptions_remain_scoped_outside_primary_quality_block() -> None:
    text = _workflow_text()
    quality_block = _between(
        text,
        "    - name: Lint with flake8\n",
        "    - name: Prove quality tools reject controlled violations\n",
    )

    assert "continue-on-error:" not in quality_block
    assert "fail_ci_if_error: false" in text
    assert "Run full first-party Bandit report" in text
    assert "Block medium-or-higher Bandit findings with medium-or-higher confidence" in text
    assert "Audit installed CI environment with pip-audit" in text
