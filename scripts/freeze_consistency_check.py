#!/usr/bin/env python3
"""Fail-closed consistency checks for DGAF/PDMAL freeze predicate metadata.

This is a governance consistency checker, not an authority. It detects
self-contradictory or stale freeze metadata but never upgrades a predicate.

Usage:
    python scripts/freeze_consistency_check.py [--root .]

Exit codes:
    0 = no detected consistency errors
    1 = consistency errors detected
    2 = checker/configuration error
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
from pathlib import Path


EXPECTED_STATUSES = {"VERIFIED", "PARTIAL", "OPEN", "NOT_EXECUTED"}
REQUIRED_PREDICATES = [f"P{i}" for i in range(1, 10)]


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    manifest = root / "docs/experiment/FREEZE_PREDICATES.yaml"
    if not manifest.exists():
        print(f"ERROR: missing {manifest}")
        return 2

    text = manifest.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    current_sha = git(root, "rev-parse", "HEAD")
    recorded = re.search(r"^current_main_sha:\s*(\S+)", text, re.M)
    if recorded and recorded.group(1) not in {"CURRENT_MAIN_AT_VERIFICATION", current_sha}:
        errors.append(f"stale current_main_sha: {recorded.group(1)} != {current_sha}")
    elif recorded and recorded.group(1) == "CURRENT_MAIN_AT_VERIFICATION":
        warnings.append("current_main_sha is intentionally symbolic; predicate file is not candidate-bound")

    found: dict[str, str] = {}
    for match in re.finditer(r"(?ms)^  - id: (P\d+)\n    name: ([^\n]+)\n    status: ([A-Z_]+)\n    blocking: (true|false)", text):
        pid, name, status, blocking = match.groups()
        if pid in found:
            errors.append(f"duplicate predicate: {pid}")
        found[pid] = status
        if status not in EXPECTED_STATUSES:
            errors.append(f"invalid status for {pid}: {status}")
        if blocking != "true":
            warnings.append(f"{pid} is not blocking")

    missing = [p for p in REQUIRED_PREDICATES if p not in found]
    if missing:
        errors.append("missing predicates: " + ", ".join(missing))

    if re.search(r"^authorization:\n(?:.*\n)*?  status:\s*VERIFIED", text, re.M):
        errors.append("authorization cannot be VERIFIED in a pre-freeze predicate inventory")
    if re.search(r"^new_freeze_created:\s*true", text, re.M):
        errors.append("new_freeze_created=true conflicts with PRE-FREEZE state")
    if re.search(r"^empirical_n:\s*[1-9]", text, re.M):
        errors.append("empirical_n > 0 conflicts with the current pre-freeze governance boundary")

    print(f"FREEZE CONSISTENCY CHECK — HEAD {current_sha}")
    print(f"manifest_sha256={sha256(manifest)}")
    print("predicate_status=" + ", ".join(f"{p}:{found.get(p, 'MISSING')}" for p in REQUIRED_PREDICATES))
    for warning in warnings:
        print("WARNING: " + warning)
    for error in errors:
        print("ERROR: " + error)
    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS (consistency only; no predicate is promoted)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
