#!/usr/bin/env python3
"""Fail closed when canonical control-state main-tip metadata is stale.

The invariant is intentionally evaluated against the CI-provided commit SHA,
not against a locally inferred ref, so a passing check proves that the
control-state record is reconciled to the commit being validated.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required") from exc

path = Path("docs/governance/CONTROL_STATE_2026-08-31.yaml")
if not path.exists():
    raise SystemExit(f"missing control-state file: {path}")

state = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
recorded = state.get("last_reconciled_main_tip")
actual = os.environ.get("GITHUB_SHA")

if not actual:
    raise SystemExit("GITHUB_SHA is required for live HEAD reconciliation")
if not recorded:
    raise SystemExit("control state missing last_reconciled_main_tip")
if recorded != actual:
    raise SystemExit(
        "control-state HEAD drift: "
        f"last_reconciled_main_tip={recorded} != GITHUB_SHA={actual}"
    )

print(f"control-state HEAD reconciliation: PASS ({actual})")
