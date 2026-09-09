#!/usr/bin/env python3
"""Fail-closed scope, payload, and provenance custody for critical PR lanes."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = "docs/governance/CRITICAL_PR_LANE_CUSTODY_REGISTRY_V1.json"
REGISTRY = ROOT / REGISTRY_PATH
SHA40 = re.compile(r"^[0-9a-f]{40}$")


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
    schema = data["schema_version"]
    assert schema >= 2
    assert 439 in data["controller_issues"]
    assert 441 in data["controller_issues"]
    assert data["scientific_n_increment"] == 0
    if schema >= 3:
        assert data["registry_authority"] == "BASE_BRANCH_ONLY"
    if schema == 3:
        assert data["reconciliation_protocol"] == "SEPARATE_UNREGISTERED_GOVERNANCE_PR"
    if schema >= 4:
        assert 452 in data["controller_issues"]
        assert data["reconciliation_protocol"] == "EXACT_PAYLOAD_BINDING_WITH_FRESH_HEAD_CI"
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


def contaminated_heads(lane: dict) -> set[str]:
    return {
        item["head"].lower()
        for item in lane.get("head_history", [])
        if item.get("classification") == "CONTAMINATED_CROSS_LANE"
    }


def validate_head(lane: dict, head_sha: str, *, schema_version: int) -> None:
    actual = head_sha.lower()
    if not SHA40.fullmatch(actual):
        raise SystemExit("CRITICAL_PR_LANE_CUSTODY_FAIL: invalid head SHA")
    if actual in contaminated_heads(lane):
        raise SystemExit("CRITICAL_PR_LANE_CUSTODY_FAIL: explicitly contaminated head identity")
    if schema_version < 4:
        expected = lane["current_reconciled_head"].lower()
        if actual != expected:
            raise SystemExit(
                "CRITICAL_PR_LANE_CUSTODY_FAIL: unreconciled head movement: "
                f"{actual} != {expected}"
            )


def validate_changed_files(lane: dict, changed_files: list[str], *, exact: bool) -> None:
    allowed_list = lane["allowed_changed_files"]
    allowed = set(allowed_list)
    if len(allowed) != len(allowed_list):
        raise SystemExit("duplicate allowed path in custody registry")
    actual = set(changed_files)
    unexpected = sorted(actual - allowed)
    if unexpected:
        raise SystemExit(
            "CRITICAL_PR_LANE_CUSTODY_FAIL: changed files outside declared lane: "
            + ", ".join(unexpected)
        )
    if not changed_files:
        raise SystemExit("CRITICAL_PR_LANE_CUSTODY_FAIL: registered lane has empty diff")
    if exact and actual != allowed:
        missing = sorted(allowed - actual)
        raise SystemExit(
            "CRITICAL_PR_LANE_CUSTODY_FAIL: exact registered payload file set mismatch; "
            f"missing={missing}"
        )


def fetch_base(base_ref: str) -> None:
    subprocess.run(
        ["git", "fetch", "origin", base_ref, "--depth=1"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
    )


def git_changed_files(base_ref: str, head_sha: str) -> list[str]:
    fetch_base(base_ref)
    output = subprocess.check_output(
        ["git", "diff", "--name-only", f"origin/{base_ref}...{head_sha}"],
        cwd=ROOT,
        text=True,
    )
    return [line.strip() for line in output.splitlines() if line.strip()]


def git_blob_at_head(head_sha: str, path: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", f"{head_sha}:{path}"], cwd=ROOT, text=True
        ).strip().lower()
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"CRITICAL_PR_LANE_CUSTODY_FAIL: missing registered payload path {path}") from exc


def validate_payload_blobs(lane: dict, head_sha: str) -> None:
    expected = lane["required_payload_blobs"]
    if set(expected) != set(lane["allowed_changed_files"]):
        raise SystemExit("CRITICAL_PR_LANE_CUSTODY_FAIL: registry payload/file-set mismatch")
    for path, wanted in expected.items():
        actual = git_blob_at_head(head_sha, path)
        if actual != wanted.lower():
            raise SystemExit(
                "CRITICAL_PR_LANE_CUSTODY_FAIL: registered payload blob drift: "
                f"{path}: {actual} != {wanted.lower()}"
            )


def validate_payload_map_for_test(lane: dict, payload: dict[str, str]) -> None:
    expected = lane["required_payload_blobs"]
    if set(payload) != set(expected):
        missing = sorted(set(expected) - set(payload))
        extra = sorted(set(payload) - set(expected))
        raise SystemExit(
            f"CRITICAL_PR_LANE_CUSTODY_FAIL: payload map set mismatch missing={missing} extra={extra}"
        )
    drift = sorted(path for path in expected if payload[path].lower() != expected[path].lower())
    if drift:
        raise SystemExit("CRITICAL_PR_LANE_CUSTODY_FAIL: payload map blob drift: " + ", ".join(drift))


def self_test(data: dict) -> None:
    lane = lane_for(data, "experiment/track-a-epoch-001-runner")
    assert lane is not None
    schema = data["schema_version"]

    if schema < 4:
        validate_head(lane, lane["current_reconciled_head"], schema_version=schema)
        try:
            validate_head(lane, "0" * 40, schema_version=schema)
        except SystemExit as exc:
            assert "unreconciled head movement" in str(exc)
        else:
            raise AssertionError("unreconciled-head negative control did not fail")
    else:
        assert set(lane["required_payload_blobs"]) == set(lane["allowed_changed_files"])
        validate_payload_map_for_test(lane, dict(lane["required_payload_blobs"]))
        mutated = dict(lane["required_payload_blobs"])
        first = next(iter(mutated))
        mutated[first] = "0" * 40
        try:
            validate_payload_map_for_test(lane, mutated)
        except SystemExit as exc:
            assert "blob drift" in str(exc)
        else:
            raise AssertionError("payload-drift negative control did not fail")
        missing = dict(lane["required_payload_blobs"])
        missing.pop(first)
        try:
            validate_payload_map_for_test(lane, missing)
        except SystemExit as exc:
            assert "set mismatch" in str(exc)
        else:
            raise AssertionError("missing-file negative control did not fail")
        extra = dict(lane["required_payload_blobs"])
        extra["unexpected.txt"] = "0" * 40
        try:
            validate_payload_map_for_test(lane, extra)
        except SystemExit as exc:
            assert "set mismatch" in str(exc)
        else:
            raise AssertionError("extra-file negative control did not fail")
        bad = next(iter(contaminated_heads(lane)))
        try:
            validate_head(lane, bad, schema_version=schema)
        except SystemExit as exc:
            assert "contaminated head" in str(exc)
        else:
            raise AssertionError("contaminated-head negative control did not fail")
        validate_head(lane, "1" * 40, schema_version=schema)

    validate_changed_files(lane, list(lane["allowed_changed_files"]), exact=schema >= 4)
    try:
        validate_changed_files(
            lane,
            list(lane["allowed_changed_files"]) + [".github/workflows/pdmal-solo-pilot-execution.yml"],
            exact=schema >= 4,
        )
    except SystemExit as exc:
        assert "outside declared lane" in str(exc)
    else:
        raise AssertionError("cross-lane contamination negative control did not fail")

    assert any(item["classification"] == "CONTAMINATED_CROSS_LANE" for item in lane["head_history"])
    print(f"CRITICAL_PR_LANE_CUSTODY_SELF_TEST_PASS_SCHEMA_{schema}")


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

    schema = data["schema_version"]
    validate_head(lane, args.head_sha, schema_version=schema)
    changed = git_changed_files(args.base_ref, args.head_sha)
    validate_changed_files(lane, changed, exact=schema >= 4)
    if schema >= 4:
        validate_payload_blobs(lane, args.head_sha)
        print("CUSTODY_BINDING=EXACT_PAYLOAD")
    else:
        print(f"RECONCILED_HEAD={lane['current_reconciled_head']}")
    print(f"CRITICAL_PR_LANE_CUSTODY_PASS: {lane['lane_id']}")
    print(f"LIVE_HEAD={args.head_sha.lower()}")
    print(f"CHANGED_FILES={len(changed)}")
    print("REGISTRY_AUTHORITY=BASE_BRANCH_ONLY")
    print("PRIOR_EXACT_HEAD_EVIDENCE_TRANSFER=PROHIBITED_ON_HEAD_CHANGE")


if __name__ == "__main__":
    main()
