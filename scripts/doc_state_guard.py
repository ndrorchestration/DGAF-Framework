#!/usr/bin/env python3
"""Later-state document guard (A5).

Reports (non-blocking) when documentation files that may follow a code change
appear to have been modified after the nearest apparatus commit on the branch.

EXEMPT (canonical state documents that deliberately evolve over time):
  - docs/FREEZE_MANIFEST.md
  - evidence/claims.json
  - docs/GOVERNANCE_ARCHITECTURE_AUDIT.md
  - docs/FORWARD_PLAN.md
  - docs/verification_plan.md

Everything else is IN-SCOPE: if a doc-only commit touches in-scope paths (anything
under docs/ other than the exempt list, plus evidence/ and GOVERNANCE_ARCHITECTURE_AUDIT.md),
and the nearest apparatus commit is more than ``max_drift_commits`` behind HEAD, report
a drift anomaly. This is REPORT-ONLY: no failure is induced.

The guard does not block documentation work; it surfaces potential later-state
drift so reviewers can confirm that doc-only commits are not silently carrying
apparatus changes.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPARATUS_DIRS = (
    "experiments/pdmal_pilot",
)
EXEMPT_PATHS = frozenset((
    "docs/FREEZE_MANIFEST.md",
    "evidence/claims.json",
    "docs/GOVERNANCE_ARCHITECTURE_AUDIT.md",
    "docs/FORWARD_PLAN.md",
    "docs/verification_plan.md",
))
TOOLS_DIR = "tools"


def run_git(*args: str) -> str:
    """Run a git subcommand and return stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def nearest_apparatus_commit() -> str:
    """Find the most recent commit that touched an apparatus directory."""
    rev_list = run_git(
        "rev-list", "HEAD",
        "--ancestry-path",
        *(f"-- {d}/" for d in APPARATUS_DIRS),
    )
    if rev_list:
        return rev_list.splitlines()[0]
    return run_git("rev-parse", "HEAD") or ""


def files_changed_since(commit_sha: str) -> list[str]:
    """Return paths changed between commit_sha and HEAD."""
    if not commit_sha:
        return []
    diff = run_git("diff", "--name-only", f"{commit_sha}..HEAD")
    return [p for p in diff.splitlines() if p]


def classify(path: str) -> str:
    if path in EXEMPT_PATHS:
        return "exempt"
    if any(path.startswith(d + "/") or path == d for d in APPARATUS_DIRS):
        return "apparatus"
    if path.startswith(TOOLS_DIR + "/") or path == TOOLS_DIR:
        return "tools"
    return "other_doc"


def main() -> int:
    parser = argparse.ArgumentParser(description="Later-state document guard (report-only)")
    parser.add_argument("--max-drift-commits", type=int, default=4,
                        help="Max commits between apparatus change and doc change before reporting (default 4)")
    args = parser.parse_args()

    apparatus_sha = nearest_apparatus_commit()
    changed = files_changed_since(apparatus_sha)

    scope_changed: list[tuple[str, str]] = []
    for path in changed:
        label = classify(path)
        if label == "exempt":
            continue
        scope_changed.append((path, label))

    if not scope_changed:
        print("DOC_STATE_GUARD: PASS — no in-scope documentation drift detected")
        return 0

    apparatus_age = 0
    if apparatus_sha:
        ancestry = run_git("rev-list", "--count", f"{apparatus_sha}..HEAD")
        try:
            apparatus_age = int(ancestry) if ancestry else 0
        except ValueError:
            apparatus_age = 0

    reported: list[str] = []
    for path, label in scope_changed:
        if label == "apparatus":
            continue  # apparatus changes are the reference point, not drift
        if apparatus_age > args.max_drift_commits:
            reported.append(f"{path} (doc drift: {apparatus_age} commits since nearest apparatus change)")

    if reported:
        print("DOC_STATE_GUARD: REPORT — potential later-state documentation drift detected:")
        for line in reported:
            print(f"  - {line}")
        print(f"  (nearest apparatus commit: {apparatus_sha[:8] if apparatus_sha else 'unknown'})")
        print(f"  EXEMPT paths: {', '.join(sorted(EXEMPT_PATHS))}")
        print("  This is report-only; no failure induced.")
        return 0

    print("DOC_STATE_GUARD: PASS — in-scope documentation changes are within drift tolerance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
