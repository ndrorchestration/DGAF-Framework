from pathlib import Path

DEPLOY_WORKFLOW = Path(".github/workflows/deploy.yml")
STAGING_WORKFLOW = Path(".github/workflows/live-staging-breaker.yml")
REGRESSION_WORKFLOW = Path(".github/workflows/regression.yml")
REGRESSION_SCRIPT = Path("scripts/live_regression_v17.py")
VERSION_INVENTORY = Path("docs/VERSION_REFERENCE_INVENTORY.md")

VERCEL_CLI_VERSION = "59.11.7"
HTTPX_VERSION = "0.28.1"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_vercel_cli_is_exactly_pinned_and_verified() -> None:
    for path in (DEPLOY_WORKFLOW, STAGING_WORKFLOW):
        text = _read(path)
        assert f"VERCEL_CLI_VERSION: {VERCEL_CLI_VERSION}" in text
        assert 'npm install -g "vercel@${VERCEL_CLI_VERSION}"' in text
        assert 'test "$actual_version" = "$VERCEL_CLI_VERSION"' in text
        assert "vercel@latest" not in text


def test_live_regression_httpx_installs_are_exactly_pinned() -> None:
    for path in (DEPLOY_WORKFLOW, REGRESSION_WORKFLOW):
        text = _read(path)
        assert f"HTTPX_VERSION: {HTTPX_VERSION}" in text
        assert '"httpx==${HTTPX_VERSION}"' in text
        assert "pip install httpx" not in text


def test_live_regression_script_never_self_installs_dependencies() -> None:
    text = _read(REGRESSION_SCRIPT)
    assert "import httpx" in text
    assert "subprocess" not in text
    assert "pip install" not in text
    assert "check_call" not in text


def test_version_inventory_does_not_claim_nonexistent_npm_lockfile() -> None:
    text = _read(VERSION_INVENTORY)
    assert "| `package-lock.json` | **absent** |" in text
    assert "transitive npm resolution is **not repository-locked**" in text
    assert "regenerated on next `npm install`" not in text
