"""Behavioral negative controls for DGAF PDMAL publication guard (#1418).

Run against a disposable checkout of PR #1414 only. This tests the real
checked-out guard shell with synthetic settings. No workflow dispatch,
producer, real blinding key, artifact, or scientific execution occurs.
Same-operator engineering QA is not independent validation.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/pdmal-instrumentation-dry-run.yml"
GUARD_NAME = "Block unapproved structural artifact publication (#1399)"
SENTINEL = "POST_GUARD_EXECUTED_UNEXPECTEDLY"


def _workflow() -> dict:
    loaded = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _guard() -> tuple[dict, list[dict]]:
    workflow = _workflow()
    # PyYAML 1.1 historically parses unquoted GitHub Actions 'on' as True.
    triggers = workflow.get("on", workflow.get(True))
    assert isinstance(triggers, dict)
    assert {"push", "pull_request", "workflow_dispatch"} <= triggers.keys()
    jobs = workflow.get("jobs")
    assert isinstance(jobs, dict) and set(jobs) == {"pdmal-dry-run"}
    job = jobs["pdmal-dry-run"]
    steps = job.get("steps")
    assert isinstance(steps, list) and len(steps) > 1
    assert sum(s.get("name") == GUARD_NAME for s in steps) == 1
    guard = steps[0]
    assert guard.get("name") == GUARD_NAME
    assert not guard.get("if") and not guard.get("continue-on-error")
    assert not job.get("continue-on-error")
    assert guard.get("env", {}).get("PDMAL_REPO_PRIVATE") == "${{ github.event.repository.private }}"
    assert isinstance(guard.get("run"), str) and "set -euo pipefail" in guard["run"]
    return guard, steps


def _run_guard(value: str | None, *, script: str | None = None) -> subprocess.CompletedProcess[str]:
    guard, _ = _guard()
    env = {"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", "/tmp")}
    if value is not None:
        env["PDMAL_REPO_PRIVATE"] = value
    # The marker must never run after correct fail-closed behavior.
    code = (guard["run"] if script is None else script) + "\nprintf '%s\\n' '" + SENTINEL + "'\n"
    return subprocess.run(["bash", "-c", code], env=env, capture_output=True,
                          text=True, timeout=5, check=False)


@pytest.mark.parametrize("value", [None, "", "false", "true", "TRUE", "1", "null", "unexpected"])
def test_all_synthetic_privacy_values_fail_closed(value: str | None) -> None:
    result = _run_guard(value)
    assert result.returncode != 0, (value, result)
    assert SENTINEL not in result.stdout + result.stderr
    if value is None:
        assert "unbound variable" in result.stderr
    elif value == "true":
        assert "custody/audience decision is not independently approved" in result.stdout
    else:
        assert "blocked in a public repository" in result.stdout


def test_structural_order_and_artifact_paths() -> None:
    _, steps = _guard()
    artifact_steps = [i for i, step in enumerate(steps)
                      if "upload-artifact" in str(step.get("uses", ""))]
    assert len(artifact_steps) >= 2
    assert min(artifact_steps) > 0
    assert any(s.get("name") == "Checkout control plane for candidate resolution"
               for s in steps[1:])
    assert steps[0]["name"] == GUARD_NAME


def test_mutation_control_proves_the_oracle_is_sensitive() -> None:
    guard, _ = _guard()
    assert guard["run"].count("exit 1") == 2
    # In-memory negative control only; never mutate the checked-out guard.
    weakened = guard["run"].replace("exit 1", ":")
    result = _run_guard("true", script=weakened)
    assert result.returncode == 0
    assert SENTINEL in result.stdout


def test_credential_boundary_is_not_misstated() -> None:
    workflow = _workflow()
    job = workflow["jobs"]["pdmal-dry-run"]
    # Source exposes a job-scoped secret binding; no secret values are read.
    assert "PDMAL_BLINDING_KEY" in job.get("env", {})
    guard, _ = _guard()
    assert "PDMAL_BLINDING_KEY" not in guard.get("env", {})
