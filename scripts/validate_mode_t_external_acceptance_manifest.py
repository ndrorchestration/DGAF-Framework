#!/usr/bin/env python3
"""Fail-closed validator for the Mode-T external acceptance handoff manifest.

The validator proves only that the handoff is structurally conservative and that its
reviewed Git blobs match the declared immutable review base. It does not perform an
independent security review, external retention, Confidential Space execution, or
protected continuity adjudication.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Mapping

_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")

_TOP_LEVEL = {
    "schema_version",
    "record_class",
    "review_base",
    "reviewed_sources",
    "external_tracks",
    "scientific_state",
    "non_promotion",
}
_SOURCE_KEYS = {"path", "git_blob", "role"}
_TRACK_KEYS = {"issue", "track", "status", "required_output"}
_SCIENTIFIC_STATE = {
    "final_candidate_status": "NOT_DESIGNATED",
    "final_candidate_tracker": 309,
    "p4_status": "OPEN_FAIL_CLOSED",
    "p7_final_binding": "OPEN",
    "p8_status": "OPEN_FAIL_CLOSED",
    "final_p9_status": "NOT_EXECUTED",
    "freeze_status": "NOT_ESTABLISHED",
    "authorization_status": "NOT_GRANTED",
    "empirical_n": 0,
}
_NON_PROMOTION_KEYS = {
    "packet_is_authorization",
    "packet_is_independent_review",
    "packet_is_real_custody_evidence",
    "packet_designates_final_candidate",
    "packet_changes_empirical_n",
}
_EXPECTED_EXTERNAL_ISSUES = {295, 310, 316, 320}


def _mapping(value: Any, label: str, errors: list[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        errors.append(f"{label} must be an object")
        return {}
    return value


def validate_manifest_structure(data: Any) -> list[str]:
    """Return structural/non-promotion errors without consulting Git or the network."""
    errors: list[str] = []
    root = _mapping(data, "manifest", errors)
    if set(root) != _TOP_LEVEL:
        errors.append("manifest top-level keys must match the closed schema")

    if root.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if root.get("record_class") != "DGAF_MODE_T_EXTERNAL_ACCEPTANCE_HANDOFF_V1":
        errors.append("unexpected record_class")

    review_base = _mapping(root.get("review_base"), "review_base", errors)
    if set(review_base) != {"repository", "sha", "tree"}:
        errors.append("review_base keys must be repository/sha/tree only")
    if review_base.get("repository") != "ndrorchestration/DGAF-Framework":
        errors.append("review_base repository mismatch")
    for field in ("sha", "tree"):
        value = review_base.get(field)
        if not isinstance(value, str) or not _SHA1_RE.fullmatch(value):
            errors.append(f"review_base {field} must be a 40-character Git object id")

    sources = root.get("reviewed_sources")
    if not isinstance(sources, list) or not sources:
        errors.append("reviewed_sources must be a non-empty list")
        sources = []
    seen_paths: set[str] = set()
    seen_roles: set[str] = set()
    for index, raw_source in enumerate(sources):
        source = _mapping(raw_source, f"reviewed_sources[{index}]", errors)
        if set(source) != _SOURCE_KEYS:
            errors.append(f"reviewed_sources[{index}] keys must match the closed schema")
        path = source.get("path")
        role = source.get("role")
        blob = source.get("git_blob")
        if not isinstance(path, str) or not path or path.startswith("/") or ".." in Path(path).parts:
            errors.append(f"reviewed_sources[{index}] path is invalid")
        elif path in seen_paths:
            errors.append(f"duplicate reviewed source path: {path}")
        else:
            seen_paths.add(path)
        if not isinstance(role, str) or not role:
            errors.append(f"reviewed_sources[{index}] role is invalid")
        elif role in seen_roles:
            errors.append(f"duplicate reviewed source role: {role}")
        else:
            seen_roles.add(role)
        if not isinstance(blob, str) or not _SHA1_RE.fullmatch(blob):
            errors.append(f"reviewed_sources[{index}] git_blob is invalid")

    tracks = root.get("external_tracks")
    if not isinstance(tracks, list):
        errors.append("external_tracks must be a list")
        tracks = []
    issues: set[int] = set()
    track_names: set[str] = set()
    for index, raw_track in enumerate(tracks):
        track = _mapping(raw_track, f"external_tracks[{index}]", errors)
        if set(track) != _TRACK_KEYS:
            errors.append(f"external_tracks[{index}] keys must match the closed schema")
        issue = track.get("issue")
        name = track.get("track")
        if not isinstance(issue, int):
            errors.append(f"external_tracks[{index}] issue must be an integer")
        elif issue in issues:
            errors.append(f"duplicate external issue: {issue}")
        else:
            issues.add(issue)
        if not isinstance(name, str) or not name:
            errors.append(f"external_tracks[{index}] track is invalid")
        elif name in track_names:
            errors.append(f"duplicate external track: {name}")
        else:
            track_names.add(name)
        if track.get("status") != "NOT_EXECUTED":
            errors.append(f"external_tracks[{index}] must remain NOT_EXECUTED")
        if not isinstance(track.get("required_output"), str) or not track.get("required_output"):
            errors.append(f"external_tracks[{index}] required_output is invalid")
    if issues != _EXPECTED_EXTERNAL_ISSUES:
        errors.append("external issue set must be exactly 295/310/316/320")

    scientific = _mapping(root.get("scientific_state"), "scientific_state", errors)
    if set(scientific) != set(_SCIENTIFIC_STATE):
        errors.append("scientific_state keys must match the closed schema")
    for key, expected in _SCIENTIFIC_STATE.items():
        if scientific.get(key) != expected:
            errors.append(f"scientific_state {key} must remain {expected!r}")

    non_promotion = _mapping(root.get("non_promotion"), "non_promotion", errors)
    if set(non_promotion) != _NON_PROMOTION_KEYS:
        errors.append("non_promotion keys must match the closed schema")
    for key in _NON_PROMOTION_KEYS:
        if non_promotion.get(key) is not False:
            errors.append(f"non_promotion {key} must be false")

    return errors


def _git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return result
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return {}


def validate_repository_binding(data: Mapping[str, Any], repo_root: Path) -> list[str]:
    """Verify declared immutable source identities against the local Git object graph."""
    errors: list[str] = []
    base = data["review_base"]
    base_sha = str(base["sha"])
    expected_tree = str(base["tree"])

    try:
        actual_tree = _git(repo_root, "show", "-s", "--format=%T", base_sha).stdout.strip()
    except subprocess.CalledProcessError as exc:
        return [f"review_base commit is unavailable: {exc.stderr.strip()}"]
    if actual_tree != expected_tree:
        errors.append(f"review_base tree mismatch: expected {expected_tree}, got {actual_tree}")

    ancestor = _git(repo_root, "merge-base", "--is-ancestor", base_sha, "HEAD", check=False)
    if ancestor.returncode != 0:
        errors.append("review_base must be an ancestor of HEAD")

    for source in data["reviewed_sources"]:
        path = source["path"]
        expected_blob = source["git_blob"]
        result = _git(repo_root, "ls-tree", base_sha, "--", path, check=False)
        if result.returncode != 0 or not result.stdout.strip():
            errors.append(f"reviewed source missing at review_base: {path}")
            continue
        meta, _, returned_path = result.stdout.rstrip("\n").partition("\t")
        parts = meta.split()
        if len(parts) != 3 or returned_path != path:
            errors.append(f"unexpected git ls-tree shape for {path}")
            continue
        actual_blob = parts[2]
        if actual_blob != expected_blob:
            errors.append(f"reviewed source blob mismatch for {path}: expected {expected_blob}, got {actual_blob}")

    control_path = "docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md"
    control = _git(repo_root, "show", f"{base_sha}:{control_path}", check=False)
    if control.returncode != 0:
        errors.append("control-state file is unavailable at review_base")
        return errors
    frontmatter = _frontmatter(control.stdout)
    expected_frontmatter = {
        "final_candidate_status": "NOT_DESIGNATED",
        "final_candidate_tracker": "309",
        "candidate_status": "PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED",
        "empirical_n": "0",
    }
    for key, expected in expected_frontmatter.items():
        if frontmatter.get(key) != expected:
            errors.append(f"control-state {key} mismatch: expected {expected!r}, got {frontmatter.get(key)!r}")
    if "| P4 Security / Blinding | OPEN / FAIL-CLOSED |" not in control.stdout:
        errors.append("control-state P4 OPEN / FAIL-CLOSED marker is missing")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="docs/governance/mode_t_external_acceptance_manifest.json",
    )
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = validate_manifest_structure(data)
    if not errors:
        errors.extend(validate_repository_binding(data, Path(args.repo_root).resolve()))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: source-bound external acceptance handoff is structurally conservative")
    print("external_outputs=NOT_EXECUTED")
    print("final_candidate_status=NOT_DESIGNATED")
    print("p4_status=OPEN_FAIL_CLOSED")
    print("authorization_status=NOT_GRANTED")
    print("empirical_n=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
