"""Read-only regression contract for Vercel secret argv."""
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / ".github/workflows/deploy.yml",
    ROOT / ".github/workflows/live-staging-breaker.yml",
]
@pytest.mark.parametrize("file", FILES)
def test_vercel_api_token_never_in_cli_or_curl_argv(file: Path) -> None:
    source = file.read_text(encoding="utf8")
    assert '--token="$VERCEL_TOKEN"' not in source
    assert '-H "Authorization: Bearer $VERCEL_TOKEN"' not in source
    assert 'VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}' in source
    assert 'curl -fsS --config - --get' in source
    assert 'printf \'header = "Authorization: Bearer %s"\\n\' "$VERCEL_TOKEN"' in source

def test_restricted_environment_and_ref_both_remain() -> None:
    prod = FILES[0].read_text(encoding="utf8")
    preview = FILES[1].read_text(encoding="utf8")
    assert "environment: Production" in prod
    assert "environment: Preview" in preview
    assert "persist-credentials: false" in prod
    assert "persist-credentials: false" in preview
    assert "github.ref == 'refs/heads/main'" in prod
    assert "github.ref == 'refs/heads/main'" in preview


@pytest.mark.parametrize("file", FILES)
def test_bypass_credentials_do_not_appear_in_curl_argv(file: Path) -> None:
    text = file.read_text(encoding="utf8")
    assert '-H "x-vercel-protection-bypass: $VERCEL_AUTOMATION_BYPASS_SECRET"' not in text
    assert 'curl -fsS --config -' in text
    assert 'printf \'header = "x-vercel-protection-bypass: %s"\\n\' "$VERCEL_AUTOMATION_BYPASS_SECRET"' in text


def test_production_verifier_uses_protected_environment_and_step_scoped_bypass() -> None:
    source = FILES[0].read_text(encoding="utf8")
    verify = source.split("  verify:", 1)[1]
    job_header = verify.split("    steps:", 1)[0]
    assert "environment: Production" in job_header
    assert "VERCEL_AUTOMATION_BYPASS_SECRET" not in job_header
    assert "persist-credentials: false" in verify
    for name in (
        "Require runtime bypass credential",
        "Health preflight",
        "Prove staging breaker is unavailable in production",
        "30-turn live regression",
        "Audit baseline",
        "Prove Tektite demo is unavailable in production",
    ):
        section = verify.split("      - name: " + name + "\n", 1)[1]
        assert section.startswith("        env:\n          VERCEL_AUTOMATION_BYPASS_SECRET: ")



def test_vercel_git_automatic_deployments_remain_disabled() -> None:
    import json
    config = json.loads((ROOT / "vercel.json").read_text(encoding="utf8"))
    assert config.get("git", {}).get("deploymentEnabled") is False
