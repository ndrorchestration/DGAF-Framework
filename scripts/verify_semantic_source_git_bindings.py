#!/usr/bin/env python3
"""Verify semantic-source manifest path/blob bindings against local Git history."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


class GitBindingError(ValueError):
    """Raised when a declared semantic-source binding cannot be verified."""


def load_manifest(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GitBindingError("manifest root must be a JSON object")
    return value


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise GitBindingError(detail)
    return result.stdout.strip()


def resolve_commit(repo: Path, commit: str) -> str:
    if not SHA1_RE.fullmatch(commit):
        raise GitBindingError("repository_commit must be a lowercase 40-character Git SHA")
    resolved = run_git(repo, "rev-parse", "--verify", f"{commit}^{{commit}}")
    if resolved != commit:
        raise GitBindingError(f"repository_commit resolved unexpectedly: declared {commit}, resolved {resolved}")
    return resolved


def resolve_blob(repo: Path, commit: str, path: str) -> str:
    if not path or path.startswith("/") or ".." in Path(path).parts:
        raise GitBindingError(f"invalid repository-relative artifact path: {path!r}")
    object_id = run_git(repo, "rev-parse", "--verify", f"{commit}:{path}")
    object_type = run_git(repo, "cat-file", "-t", object_id)
    if object_type != "blob":
        raise GitBindingError(f"{path}: expected blob, found {object_type}")
    if not SHA1_RE.fullmatch(object_id):
        raise GitBindingError(f"{path}: resolved object is not a SHA-1 object id")
    return object_id


def verify_manifest_bindings(manifest: dict[str, Any], repo: Path) -> list[str]:
    errors: list[str] = []
    commit = manifest.get("repository_commit")
    if not isinstance(commit, str):
        return ["repository_commit must be a string"]

    try:
        resolve_commit(repo, commit)
    except GitBindingError as exc:
        return [f"repository_commit: {exc}"]

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return ["artifacts must be a non-empty array"]

    seen_paths: set[str] = set()
    for index, item in enumerate(artifacts):
        prefix = f"artifacts[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        path = item.get("path")
        declared = item.get("git_blob_sha1")
        if not isinstance(path, str) or not path:
            errors.append(f"{prefix}.path must be non-empty")
            continue
        if path in seen_paths:
            errors.append(f"{prefix}.path is duplicated: {path}")
            continue
        seen_paths.add(path)

        if not isinstance(declared, str) or not SHA1_RE.fullmatch(declared):
            errors.append(f"{prefix}.git_blob_sha1 must be a lowercase 40-character Git SHA")
            continue

        try:
            actual = resolve_blob(repo, commit, path)
        except GitBindingError as exc:
            errors.append(f"{path}: {exc}")
            continue

        if actual != declared:
            errors.append(f"{path}: declared blob {declared} does not match {commit}:{path} -> {actual}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="local Git repository containing the manifest's declared repository_commit",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="explicit check mode; verification is read-only in all modes",
    )
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest)
        errors = verify_manifest_bindings(manifest, args.repo.resolve())
    except (OSError, json.JSONDecodeError, GitBindingError) as exc:
        print(f"SEMANTIC_SOURCE_GIT_BINDING_FAIL: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"SEMANTIC_SOURCE_GIT_BINDING_FAIL: {error}", file=sys.stderr)
        return 1

    mode = "CHECK" if args.check else "VERIFY"
    print(f"SEMANTIC_SOURCE_GIT_BINDING_{mode}=PASS")
    print(f"REPOSITORY_COMMIT={manifest['repository_commit']}")
    print(f"ARTIFACT_COUNT={len(manifest['artifacts'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
