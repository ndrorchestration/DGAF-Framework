#!/usr/bin/env python3
"""Fail-closed changed-file scope guard for registered critical PR branches."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/governance/CRITICAL_PR_LANE_CUSTODY_REGISTRY_V1.json"


def load_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert data["record_type"] == "DGAF_CRITICAL_PR_LANE_CUSTODY_REGISTRY"
    assert data["registry_id"] == "CRITICAL_PR_LANE_CUSTODY_REGISTRY_V1"
    assert data["controller_issue"] == 439
    assert data["scientific_n_increment"] == 0
    assert data["claim_boundary"]["branch_ref_immutability_established"] is False
    assert data["claim_boundary"]["repository_admin_configuration_changed"] is False
    return data


def lane_for(data: dict, head_ref: str) -> dict | None:
    matches = [lane for lane in data["registered_lanes"] if lane["branch"] == head_ref]
    if len(matches) > 1:
        raise SystemExit(f"duplicate custody registry entries for {head_ref}")
    return matches[0] if matches else None


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


def git_changed_files(base_ref: str) -> list[str]:
    subprocess.run(
        ["git", "fetch", "origin", base_ref, "--depth=1"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
    )
    output = subprocess.check_output(
        ["git", "diff", "--name-only", f"origin/{base_ref}...HEAD"],
        cwd=ROOT,
        text=True,
    )
    return [line.strip() for line in output.splitlines() if line.strip()]


def self_test(data: dict) -> None:
    lane = lane_for(data, "experiment/track-a-epoch-001-runner")
    assert lane is not None
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
    assert lane["known_good_historical_head"] == "bdf79ddfd3a42ad8ebf4861bfd8cb8c6a85da0ea"
    assert lane["known_contaminated_historical_head"] == "dd2577224b497e9da01add59cd850e08ee364362"
    print("CRITICAL_PR_LANE_CUSTODY_SELF_TEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--head-ref")
    parser.add_argument("--base-ref", default="main")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    data = load_registry()
    if args.self_test:
        self_test(data)
        return
    if not args.head_ref:
        raise SystemExit("--head-ref is required outside self-test")

    lane = lane_for(data, args.head_ref)
    if lane is None:
        print(f"CRITICAL_PR_LANE_CUSTODY_NOT_REGISTERED: {args.head_ref}")
        return

    changed = git_changed_files(args.base_ref)
    validate_changed_files(lane, changed)
    print(f"CRITICAL_PR_LANE_CUSTODY_PASS: {lane['lane_id']}")
    print(f"CHANGED_FILES={len(changed)}")
    print("PRIOR_EXACT_HEAD_EVIDENCE_TRANSFER=PROHIBITED_ON_HEAD_CHANGE")


if __name__ == "__main__":
    main()
