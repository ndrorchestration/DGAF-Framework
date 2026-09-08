#!/usr/bin/env python3
"""Fail-closed scope and exact-head custody guard for registered critical PR lanes."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = "docs/governance/CRITICAL_PR_LANE_CUSTODY_REGISTRY_V1.json"
REGISTRY = ROOT / REGISTRY_PATH


def read_registry_text(registry_ref: str | None = None) -> str:
    if registry_ref:
        return subprocess.check_output(
            ["git", "show", f"{registry_ref}:{REGISTRY_PATH}"], cwd=ROOT, text=True
        )
    return REGISTRY.read_text(encoding="utf-8")


def load_registry(registry_ref: str | None = None) -> dict:
    data = json.loads(read_registry_text(registry_ref))
    assert data["record_type"] == "DGAF_CRITICAL_PR_LANE_CUSTODY_REGISTRY"
    assert data["registry_id"] == "CRITICAL_PR_LANE_CUSTODY_REGISTRY_V1"
    assert data["schema_version"] >= 3
    assert 439 in data["controller_issues"]
    assert 441 in data["controller_issues"]
    assert data["scientific_n_increment"] == 0
    assert data["registry_authority"] == "BASE_BRANCH_ONLY"
    assert data["reconciliation_protocol"] == "SEPARATE_UNREGISTERED_GOVERNANCE_PR"
    boundary = data["claim_boundary"]
    assert boundary["branch_ref_immutability_established"] is False
    assert boundary["repository_admin_configuration_changed"] is False
    assert boundary["registry_reconciliation_is_scientific_authorization"] is False
    return data


def lane_for(data: dict, head_ref: str) -> dict | None:
    matches = [lane for lane in data["registered_lanes"] if lane["branch"] == head_ref]
    if len(matches) > 1:
        raise SystemExit(f"duplicate custody registry entries for {head_ref}")
    return matches[0] if matches else None


def validate_head(lane: dict, head_sha: str) -> None:
    expected = lane["current_reconciled_head"].lower()
    actual = head_sha.lower()
    if actual != expected:
        raise SystemExit(
            "CRITICAL_PR_LANE_CUSTODY_FAIL: unreconciled head movement: "
            f"{actual} != {expected}"
        )


def validate_changed_files(lane: dict, changed_files: list[str]) -> None:
    allowed = set(lane["allowed_changed_files"])
    if len(allowed) != len(lane["allowed_changed_files"]):
        raise SystemExit("duplicate allowed path in custody registry")
    unexpected = sorted(set(changed_files) - allowed)
    if unexpected:
        raise SystemExit(
            "CRITICAL_PR_LANE_CUSTODY_FAIL: changed files outside declared lane: "
            + ", ".join(unexpected)
        )
    if not changed_files:
        raise SystemExit("CRITICAL_PR_LANE_CUSTODY_FAIL: registered lane has empty diff")


def fetch_base(base_ref: str) -> None:
    subprocess.run(
        ["git", "fetch", "origin", base_ref, "--depth=1"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
    )


def git_changed_files(base_ref: str) -> list[str]:
    fetch_base(base_ref)
    output = subprocess.check_output(
        ["git", "diff", "--name-only", f"origin/{base_ref}...HEAD"],
        cwd=ROOT,
        text=True,
    )
    return [line.strip() for line in output.splitlines() if line.strip()]


def self_test(data: dict) -> None:
    lane = lane_for(data, "experiment/track-a-epoch-001-runner")
    assert lane is not None
    validate_head(lane, lane["current_reconciled_head"])
    try:
        validate_head(lane, "0" * 40)
    except SystemExit as exc:
        assert "unreconciled head movement" in str(exc)
    else:
        raise AssertionError("unreconciled-head negative control did not fail")

    validate_changed_files(lane, list(lane["allowed_changed_files"]))
    try:
        validate_changed_files(
            lane,
            list(lane["allowed_changed_files"])
            + [".github/workflows/pdmal-solo-pilot-execution.yml"],
        )
    except SystemExit as exc:
        assert "outside declared lane" in str(exc)
    else:
        raise AssertionError("cross-lane contamination negative control did not fail")

    history = lane["head_history"]
    assert any(item["classification"] == "CONTAMINATED_CROSS_LANE" for item in history)
    assert history[-1]["head"] == lane["current_reconciled_head"]
    assert history[-1]["evidence_transfer_from_predecessor"] is False
    print("CRITICAL_PR_LANE_CUSTODY_SELF_TEST_PASS")


def assert_nonauthorizing(data: dict) -> None:
    assert data["scientific_n_increment"] == 0
    boundary = data["claim_boundary"]
    assert boundary["branch_ref_immutability_established"] is False
    assert boundary["actor_attribution_established"] is False
    assert boundary["repository_admin_configuration_changed"] is False
    assert boundary["registry_reconciliation_is_scientific_authorization"] is False
    assert boundary["track_a_freeze"] == "NOT_ESTABLISHED"
    assert boundary["track_a_empirical_execution"] == "NOT_AUTHORIZED"
    print("CRITICAL_PR_LANE_CUSTODY_NONAUTHORIZING_BOUNDARY_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--head-ref")
    parser.add_argument("--head-sha")
    parser.add_argument("--base-ref", default="main")
    parser.add_argument("--registry-ref")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--assert-nonauthorizing", action="store_true")
    args = parser.parse_args()

    data = load_registry(args.registry_ref)
    if args.self_test:
        self_test(data)
        return
    if args.assert_nonauthorizing:
        assert_nonauthorizing(data)
        return
    if not args.head_ref or not args.head_sha:
        raise SystemExit("--head-ref and --head-sha are required outside self-test")

    lane = lane_for(data, args.head_ref)
    if lane is None:
        print(f"CRITICAL_PR_LANE_CUSTODY_NOT_REGISTERED: {args.head_ref}")
        return

    validate_head(lane, args.head_sha)
    changed = git_changed_files(args.base_ref)
    validate_changed_files(lane, changed)
    print(f"CRITICAL_PR_LANE_CUSTODY_PASS: {lane['lane_id']}")
    print(f"RECONCILED_HEAD={lane['current_reconciled_head']}")
    print(f"CHANGED_FILES={len(changed)}")
    print("REGISTRY_AUTHORITY=BASE_BRANCH_ONLY")
    print("PRIOR_EXACT_HEAD_EVIDENCE_TRANSFER=PROHIBITED_ON_HEAD_CHANGE")


if __name__ == "__main__":
    main()
