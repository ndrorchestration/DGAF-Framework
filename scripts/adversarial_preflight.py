#!/usr/bin/env python3
"""Fail-closed adversarial pre-flight for DGAF/PDMAL freeze readiness."""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

BLOCKING = {
    "candidate_sha": "immutable candidate SHA",
    "deployment_id": "exact deployment identity",
    "runtime": "candidate runtime execution",
    "p2": "P2 runtime verification",
    "p6a": "P6a CORS verification",
    "artifact": "candidate-bound artifact",
    "blinding": "operational blinding verification",
    "custody": "durable custody round trip",
    "p7": "primary contrast lock",
    "p8": "analysis lock",
    "p9": "independent verification",
}


def git_head(root: Path) -> str:
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--state", type=Path, help="Optional JSON state file with boolean/enum gate states")
    args = ap.parse_args()
    root = args.root.resolve()
    state = {}
    if args.state:
        state = json.loads(args.state.read_text())
    head = git_head(root)
    print(f"candidate_sha={head}")
    failures = []
    for key, description in BLOCKING.items():
        value = state.get(key, "UNKNOWN")
        if value is not True and value != "VERIFIED":
            failures.append((key, description, value))
    empirical_n = state.get("empirical_n", 0)
    authorized = state.get("pilot_authorized", False)
    if authorized and empirical_n == 0 and not state.get("authorization_evidence"):
        failures.append(("authorization", "pilot authorization evidence", "MISSING"))
    if failures:
        print("ADVERSARIAL PREFLIGHT: BLOCKED")
        for key, desc, value in failures:
            print(f"- {key}: {value} — {desc}")
        return 2
    print("ADVERSARIAL PREFLIGHT: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
