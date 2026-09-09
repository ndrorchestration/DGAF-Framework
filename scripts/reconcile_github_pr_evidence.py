#!/usr/bin/env python3
"""Read-only reconciliation for a GitHub pull-request evidence snapshot.

This tool deliberately consumes an already-collected JSON snapshot and emits a
non-authorizing report. It makes no network calls, mutates no source of record,
and cannot grant scientific or empirical authorization.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SHA_RE = re.compile(r"^[0-9a-f]{40,64}$")
FORBIDDEN_KEY_FRAGMENTS = ("token", "password", "passphrase", "private_key", "secret")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def reject_secrets(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            require(
                not any(fragment in lowered for fragment in FORBIDDEN_KEY_FRAGMENTS),
                f"secret-bearing field prohibited at {path}.{key}",
            )
            reject_secrets(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_secrets(child, f"{path}[{index}]")


def reconcile(snapshot: dict[str, Any], expected_head_sha: str) -> dict[str, Any]:
    require(set(snapshot) == {"repository", "pull_request", "workflow_runs"}, "snapshot keys invalid")
    require(isinstance(snapshot["repository"], str) and "/" in snapshot["repository"], "repository invalid")
    require(isinstance(expected_head_sha, str) and SHA_RE.fullmatch(expected_head_sha), "expected head SHA invalid")
    reject_secrets(snapshot)

    pull_request = snapshot["pull_request"]
    require(isinstance(pull_request, dict), "pull_request must be an object")
    require(
        set(pull_request) == {"number", "head_sha", "state"},
        "pull_request keys invalid",
    )
    require(isinstance(pull_request["number"], int) and pull_request["number"] > 0, "PR number invalid")
    require(isinstance(pull_request["head_sha"], str) and SHA_RE.fullmatch(pull_request["head_sha"]), "PR head SHA invalid")
    require(pull_request["state"] in {"open", "closed", "merged"}, "PR state invalid")

    workflow_runs = snapshot["workflow_runs"]
    require(isinstance(workflow_runs, list), "workflow_runs must be a list")
    run_names: set[str] = set()
    failed: list[str] = []
    pending: list[str] = []
    invalid: list[str] = []
    for index, run in enumerate(workflow_runs):
        require(isinstance(run, dict), f"workflow_runs[{index}] must be an object")
        require(set(run) == {"name", "status", "conclusion", "head_sha"}, f"workflow_runs[{index}] keys invalid")
        name = run["name"]
        require(isinstance(name, str) and name and name not in run_names, "workflow names must be distinct")
        run_names.add(name)
        require(run["status"] in {"completed", "in_progress", "queued"}, f"workflow status invalid for {name}")
        require(run["conclusion"] in {"success", "failure", "cancelled", None}, f"workflow conclusion invalid for {name}")
        require(isinstance(run["head_sha"], str) and SHA_RE.fullmatch(run["head_sha"]), f"workflow head SHA invalid for {name}")
        if run["head_sha"] != expected_head_sha:
            invalid.append(name)
        elif run["status"] != "completed":
            pending.append(name)
        elif run["conclusion"] != "success":
            failed.append(name)

    stale_subject = pull_request["head_sha"] != expected_head_sha
    status = "PASS"
    if stale_subject or invalid:
        status = "STALE"
    elif failed:
        status = "FAIL"
    elif pending:
        status = "BLOCKED"

    return {
        "record_type": "GITHUB_PR_EVIDENCE_RECONCILIATION_REPORT",
        "schema_version": 1,
        "repository": snapshot["repository"],
        "pull_request_number": pull_request["number"],
        "expected_head_sha": expected_head_sha,
        "observed_head_sha": pull_request["head_sha"],
        "reconciliation_status": status,
        "stale_workflows": sorted(invalid),
        "failed_workflows": sorted(failed),
        "pending_workflows": sorted(pending),
        "authorization_effect": "NONE",
        "scientific_state_effect": "NONE",
        "mutated_authority_of_record": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--expected-head-sha", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    require(isinstance(snapshot, dict), "snapshot must be a JSON object")
    report = reconcile(snapshot, args.expected_head_sha)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
