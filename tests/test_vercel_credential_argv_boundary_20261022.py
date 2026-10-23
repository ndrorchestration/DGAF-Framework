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
    assert 'curl -fsS -H @- --get' in source
    assert 'printf \'Authorization: Bearer %s\\n\' "$VERCEL_TOKEN"' in source

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
    assert 'curl -fsS -H @-' in text
    assert 'printf \'x-vercel-protection-bypass: %s\\n\' "$VERCEL_AUTOMATION_BYPASS_SECRET"' in text


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


@pytest.mark.parametrize(("file", "expected"), [(FILES[0], 5), (FILES[1], 3)])
def test_each_curl_header_stdin_use_rejects_credential_crlf(file: Path, expected: int) -> None:
    source = file.read_text(encoding="utf8")
    assert source.count("-H @-") == expected
    assert source.count("Malformed credential header (CR/LF)") == expected
    assert "--config -" not in source
    assert "|| true" not in source

@pytest.mark.parametrize(("file", "expected"), [(FILES[0], 5), (FILES[1], 3)])
def test_preflight_blocks_curl_process_creation(file: Path, expected: int) -> None:
    """Validate outside the pipeline so malformed credentials never launch curl."""
    lines = file.read_text(encoding="utf8").splitlines()
    found = [(index, line.strip()) for index, line in enumerate(lines)
             if "Malformed credential header (CR/LF)" in line]
    assert len(found) == expected
    for index, guard in found:
        assert guard.startswith("[[ "), "A preflight inside a pipe can still launch curl"
        assert "exit 1; }" in guard
        assert "| curl" not in guard
        assert index + 1 < len(lines)
        pipe = lines[index + 1].strip()
        assert "printf " in pipe
        assert " | curl " in pipe
        assert "-H @-" in pipe

@pytest.mark.parametrize("file", FILES)
def test_actual_bash_preflight_denies_network_process(file: Path, tmp_path: Path) -> None:
    """Run actual source-derived Bash preflights with a stub, never real credentials."""
    import os
    import shutil
    import subprocess

    if os.name == "nt":
        pytest.skip("Bash process-stub control runs on Linux CI")
    bash = shutil.which("bash")
    if bash is None:
        pytest.skip("Bash unavailable")
    lines = file.read_text(encoding="utf8").splitlines()
    sites = [(index, line.strip()) for index, line in enumerate(lines)
             if "Malformed credential header (CR/LF)" in line]
    assert sites
    for index, guard in sites:
        assert guard.startswith("[[ ")
        assert index + 1 < len(lines)
        invocation = lines[index + 1].strip()
        assert "printf '" in invocation and " | curl " in invocation
        # Execute the exact guard and printf expression from the workflow.
        # A stub records whether curl would start without making a request.
        prefix = "printf " + invocation.split("printf ", 1)[1].split(" | curl ", 1)[0]
        variable = ("VERCEL_AUTOMATION_BYPASS_SECRET"
                    if "VERCEL_AUTOMATION_BYPASS_SECRET" in guard else "VERCEL_TOKEN")
        shell = (
            "set -euo pipefail\n"
            'curl() { printf "called\\n" >> "$CALLED_FILE"; cat >/dev/null; }\n'
            + guard + "\n" + prefix + " | curl -H @-\n"
        )
        for case, value, accepted in (
            ("normal", "synthetic-test-token", True),
            ("quote", 'synthetic"quote', True),
            ("cr", "synthetic\rheader: injected", False),
            ("lf", "synthetic\nheader: injected", False),
        ):
            marker = tmp_path / f"curl-site-{index}-{case}"
            env = os.environ.copy()
            env[variable] = value
            env["CALLED_FILE"] = str(marker)
            proc = subprocess.run(
                [bash, "-c", shell], env=env, capture_output=True,
                text=True, timeout=15, check=False,
            )
            assert (proc.returncode == 0) is accepted, (
                f"{file.name} site {index}, case {case}: {proc.stderr}"
            )
            assert marker.exists() is accepted, (
                f"{file.name} site {index}, case {case}: unexpected curl start"
            )
