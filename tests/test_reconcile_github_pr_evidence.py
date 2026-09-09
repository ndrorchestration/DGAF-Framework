from __future__ import annotations

import copy

import pytest

from scripts.reconcile_github_pr_evidence import reconcile


HEAD = "a" * 40
OTHER = "b" * 40


def snapshot() -> dict[str, object]:
    return {
        "repository": "ndrorchestration/DGAF-Framework",
        "pull_request": {"number": 541, "head_sha": HEAD, "state": "open"},
        "workflow_runs": [
            {"name": "Governance CI", "status": "completed", "conclusion": "success", "head_sha": HEAD},
            {"name": "Doc Lint", "status": "completed", "conclusion": "success", "head_sha": HEAD},
        ],
    }


def test_exact_subject_with_successful_workflows_passes() -> None:
    report = reconcile(snapshot(), HEAD)
    assert report["reconciliation_status"] == "PASS"
    assert report["authorization_effect"] == "NONE"
    assert report["scientific_state_effect"] == "NONE"
    assert report["mutated_authority_of_record"] is False


def test_changed_pr_head_is_stale() -> None:
    record = snapshot()
    pull_request = record["pull_request"]
    assert isinstance(pull_request, dict)
    pull_request["head_sha"] = OTHER
    assert reconcile(record, HEAD)["reconciliation_status"] == "STALE"


def test_workflow_bound_to_other_head_is_stale() -> None:
    record = snapshot()
    runs = record["workflow_runs"]
    assert isinstance(runs, list) and isinstance(runs[0], dict)
    runs[0]["head_sha"] = OTHER
    report = reconcile(record, HEAD)
    assert report["reconciliation_status"] == "STALE"
    assert report["stale_workflows"] == ["Governance CI"]


def test_pending_workflow_blocks_but_does_not_fail() -> None:
    record = snapshot()
    runs = record["workflow_runs"]
    assert isinstance(runs, list) and isinstance(runs[0], dict)
    runs[0]["status"] = "in_progress"
    runs[0]["conclusion"] = None
    report = reconcile(record, HEAD)
    assert report["reconciliation_status"] == "BLOCKED"
    assert report["pending_workflows"] == ["Governance CI"]


def test_failed_workflow_fails() -> None:
    record = snapshot()
    runs = record["workflow_runs"]
    assert isinstance(runs, list) and isinstance(runs[0], dict)
    runs[0]["conclusion"] = "failure"
    report = reconcile(record, HEAD)
    assert report["reconciliation_status"] == "FAIL"
    assert report["failed_workflows"] == ["Governance CI"]


def test_secret_bearing_input_is_rejected() -> None:
    record = copy.deepcopy(snapshot())
    record["token"] = "must-not-appear"
    with pytest.raises(ValueError, match="secret-bearing field prohibited"):
        reconcile(record, HEAD)
