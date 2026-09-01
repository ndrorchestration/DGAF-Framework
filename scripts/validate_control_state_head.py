#!/usr/bin/env python3
"""Fail closed on stale control-state reconciliation without a self-reference.

The recorded tip identifies the main-branch state that was reconciled when the
control-state file itself changed. Documentation-only commits must not force
that field to equal their own SHA.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required") from exc

CONTROL_STATE = "docs/governance/CONTROL_STATE_2026-08-31.yaml"
path = Path(CONTROL_STATE)
if not path.exists():
    raise SystemExit(f"missing control-state file: {path}")

state = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
recorded = state.get("last_reconciled_main_tip")
actual = os.environ.get("GITHUB_SHA")
event = os.environ.get("GITHUB_EVENT_NAME", "")
before = os.environ.get("GITHUB_EVENT_BEFORE")
base = os.environ.get("GITHUB_BASE_SHA")

if not actual:
    raise SystemExit("GITHUB_SHA is required for live HEAD reconciliation")
if not recorded:
    raise SystemExit("control state missing last_reconciled_main_tip")

# For a push, determine whether this commit actually changed the canonical
# control-state file. If it did, the new record must name the immediately
# preceding main tip (the push event's before SHA). If it did not, the prior
# reconciliation remains valid and the documentation-only commit must not be
# forced into a self-referential invariant.
if event == "push" and before:
    changed = subprocess.run(
        ["git", "diff", "--name-only", before, actual, "--", CONTROL_STATE],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if changed:
        if recorded != before:
            raise SystemExit(
                "control-state reconciliation drift on control-state change: "
                f"last_reconciled_main_tip={recorded} != push_before={before}"
            )
        print(
            "control-state HEAD reconciliation: PASS "
            f"(control-state changed; reconciled source={before}; resulting HEAD={actual})"
        )
    else:
        print(
            "control-state HEAD reconciliation: PASS "
            f"(control-state unchanged; retained reconciled source={recorded}; HEAD={actual})"
        )
elif event == "pull_request" and base:
    changed = subprocess.run(
        ["git", "diff", "--name-only", base, actual, "--", CONTROL_STATE],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if changed and recorded != base:
        raise SystemExit(
            "control-state reconciliation drift in pull request: "
            f"last_reconciled_main_tip={recorded} != base_sha={base}"
        )
    print(
        "control-state HEAD reconciliation: PASS "
        f"(PR control-state {'changed' if changed else 'unchanged'}; HEAD={actual})"
    )
else:
    # Non-push/manual validation cannot establish the event predecessor.
    # Preserve fail-closed behavior rather than inventing a predecessor.
    if recorded != actual:
        raise SystemExit(
            "control-state HEAD reconciliation requires a push/PR predecessor: "
            f"last_reconciled_main_tip={recorded} != GITHUB_SHA={actual}"
        )
    print(f"control-state HEAD reconciliation: PASS ({actual})")
