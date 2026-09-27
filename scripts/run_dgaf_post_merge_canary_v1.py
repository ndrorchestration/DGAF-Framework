#!/usr/bin/env python3
"""Run DGAF Post-Merge Mainline Canary v1 and emit bounded evidence."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SMOKE_RUNNER = ROOT / "scripts/run_dgaf_smoke_v1.py"
HEAD_VALIDATOR = ROOT / "scripts/validate_control_state_head.py"
SCHEMA = "dgaf.post_merge_canary.v1"


def _load_smoke_runner() -> ModuleType:
    spec = importlib.util.spec_from_file_location("dgaf_smoke_v1_runner", SMOKE_RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
    ).strip()


def _run_head_binding() -> tuple[int, str]:
    completed = subprocess.run(
        [sys.executable, str(HEAD_VALIDATOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=os.environ.copy(),
    )
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode, output


def build_result(
    *,
    expected_revision: str,
    actual_revision: str,
    predecessor: str,
    smoke_result: dict[str, Any],
    head_binding_returncode: int,
    head_binding_output: str,
) -> dict[str, Any]:
    head_outcome = "PASS" if actual_revision == expected_revision else "FAIL"
    smoke_outcome = (
        "PASS"
        if smoke_result.get("outcome") == "PASS"
        and smoke_result.get("revision") == expected_revision
        else "FAIL"
    )
    control_state_outcome = "PASS" if head_binding_returncode == 0 else "FAIL"

    gates = {
        "CANARY_HEAD": {
            "outcome": head_outcome,
            "expected_revision": expected_revision,
            "actual_revision": actual_revision,
        },
        "CANARY_SMOKE": {
            "outcome": smoke_outcome,
            "smoke_revision": smoke_result.get("revision"),
            "smoke_outcome": smoke_result.get("outcome"),
        },
        "CANARY_CONTROL_STATE": {
            "outcome": control_state_outcome,
            "diagnostic": head_binding_output,
        },
    }
    outcome = (
        "PASS"
        if all(gate["outcome"] == "PASS" for gate in gates.values())
        else "FAIL"
    )

    return {
        "schema": SCHEMA,
        "revision": expected_revision,
        "predecessor": predecessor,
        "outcome": outcome,
        "gates": gates,
        "smoke": smoke_result,
        "boundary": {
            "scientific_n_increment": 0,
            "authorization_effect": "NONE",
            "deployment_health": "NOT_ESTABLISHED",
            "production_readiness": "NOT_ESTABLISHED",
            "independent_validation": "NOT_ESTABLISHED",
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED",
        },
    }


def run_canary() -> dict[str, Any]:
    expected_revision = os.environ.get("DGAF_REVISION") or os.environ.get(
        "GITHUB_SHA"
    )
    if not expected_revision:
        raise SystemExit("DGAF_REVISION or GITHUB_SHA is required")

    predecessor = os.environ.get("GITHUB_EVENT_BEFORE", "")
    actual_revision = _git_head()

    smoke_runner = _load_smoke_runner()
    smoke_result = smoke_runner.run_smoke()
    head_binding_returncode, head_binding_output = _run_head_binding()

    return build_result(
        expected_revision=expected_revision,
        actual_revision=actual_revision,
        predecessor=predecessor,
        smoke_result=smoke_result,
        head_binding_returncode=head_binding_returncode,
        head_binding_output=head_binding_output,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="artifacts/dgaf-post-merge-canary-v1/result.json",
    )
    args = parser.parse_args()

    result = run_canary()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["outcome"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
