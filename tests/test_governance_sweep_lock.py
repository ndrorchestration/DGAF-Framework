"""Guard the non-empirical governance sweep's deterministic CI toolchain."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "governance-sweep.yml"
LOCK = ROOT / "requirements-ci-control-plane-py312-ubuntu2404-x64.lock"


def _assert_sweep_contract(source: str) -> None:
    assert "runs-on: ubuntu-24.04" in source
    assert "python-version: '3.12.14'" in source
    assert "ref: ${{ github.sha }}" in source
    assert "persist-credentials: false" in source
    assert 'run: test "$(git rev-parse HEAD)" = "$EXPECTED_SHA"' in source
    assert "run: bash scripts/bootstrap_ci_pip.sh" in source
    assert "--require-hashes" in source
    assert "--only-binary=:all:" in source
    assert "-r requirements-ci-control-plane-py312-ubuntu2404-x64.lock" in source
    assert "pip install --disable-pip-version-check pytest httpx" not in source
    assert "run: python -m pytest -q tests/test_ahg_conductor.py" in source
    assert "This workflow does not claim external certification or empirical validation." in source


def test_sweep_uses_hash_bound_ci_dependencies_without_empirical_promotion() -> None:
    _assert_sweep_contract(WORKFLOW.read_text(encoding="utf-8"))
    lock = LOCK.read_text(encoding="utf-8")
    assert "pytest==9.1.1" in lock
    assert "--hash=sha256:" in lock


@pytest.mark.parametrize(
    ("before", "after"),
    [
        ("runs-on: ubuntu-24.04", "runs-on: ubuntu-latest"),
        ("python-version: '3.12.14'", "python-version: '3.12'"),
        ("ref: ${{ github.sha }}", "ref: main"),
        ("persist-credentials: false", "persist-credentials: true"),
        ("--require-hashes", "--no-cache-dir"),
        ("--only-binary=:all:", "--no-deps"),
        ("run: bash scripts/bootstrap_ci_pip.sh", "run: python -m pip --version"),
        (
            "-r requirements-ci-control-plane-py312-ubuntu2404-x64.lock",
            "pytest httpx -q",
        ),
        (
            "This workflow does not claim external certification or empirical validation.",
            "This workflow establishes external certification and empirical validation.",
        ),
    ],
)
def test_sweep_contract_rejects_reproducibility_and_claim_mutations(before: str, after: str) -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert before in source
    with pytest.raises(AssertionError):
        _assert_sweep_contract(source.replace(before, after, 1))
