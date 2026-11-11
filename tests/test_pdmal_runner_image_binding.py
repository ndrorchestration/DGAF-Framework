"""Ensure PDMAL contract CI retains its exact interpreter and non-waivable gates."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARN = ROOT / ".github" / "workflows" / "pdmal-harness-validation.yml"
PREFREEZE = ROOT / ".github" / "workflows" / "pdmal-pre-freeze-runner.yml"


def test_pdmal_contract_workflows_use_compatible_pinned_runner():
    for path in (HARN, PREFREEZE):
        content = path.read_text(encoding="utf-8")
        assert "runs-on: ubuntu-24.04" in content
        assert "runs-on: ubuntu-latest" not in content
        assert "python-version: '3.12.0'" in content
        assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in content
        assert "continue-on-error: true" not in content


def test_pdmal_harness_contract_remains_enforced():
    content = HARN.read_text(encoding="utf-8")
    assert "sys.version_info[:3] == (3,12,0)" in content
    assert "test_harness_contract.py -q" in content
    assert "if-no-files-found: error" in content


def test_pdmal_prefreeze_historical_checks_remain_enforced():
    content = PREFREEZE.read_text(encoding="utf-8")
    assert "git checkout --detach" in content
    assert "--require-hashes -r experiments/pdmal_pilot/requirements-full-lock.txt" in content
    assert "test_pilot_artifact_schema.py test_security_controls.py" in content
    assert "pilot execution prohibited" in content
    assert "FINAL_CANDIDATE_STATUS" in content
