#!/usr/bin/env python3
"""
lint_provenance.py — NDR Metrics Provenance Linter
Stub v0.1 · S069 QA · Amethyst × COLLEEN

Status: STUB ONLY — interface defined; full implementation pending Role 5 staffing.

Purpose:
  Scans all markdown files in docs/ for unverified metric claims and ensures
  they carry the required qualification notice. Blocks CI merge if any
  unverified metric is present without its provenance qualifier.

Interface contract (do not change without COLLEEN secondary sign-off):
  - Entry point: main()
  - Returns: sys.exit(0) on PASS, sys.exit(1) on FAIL
  - Output: PROVENANCE_LINT_REPORT.md written to docs/qa/
  - Config: reads docs/qa/METRICS_PROVENANCE.md for the verified/unverified status
    of each registered metric claim

Metrics tracked (from METRICS_PROVENANCE.md):
  - 340% coordination gain (status: UNVERIFIED — highest priority)
  - governance_clear improvement (status: VERIFIED via Apogee A-11Q)
  - 82.6% → 100% KAPPA calibration improvement (status: VERIFIED)
  - P-11 attestation score (status: VERIFIED)
  - Cross-substrate replication gap (status: UNVERIFIED)

Unverified metric qualifier pattern (required in all docs):
  '⚠️ UNVERIFIED — see METRICS_PROVENANCE.md'
  or equivalent machine-readable marker: <!-- METRIC:UNVERIFIED -->

CI integration:
  - Triggered by: .github/workflows/pptl-ci.yml (add to governance matrix step)
  - Pre-commit hook: scripts/pre-commit-lint-provenance.sh (to be created)

See also:
  - docs/qa/METRICS_PROVENANCE.md — provenance registry and backfill queue
  - docs/governance/NDR_RESEARCH_PROGRAM_CHARTER_v1.md — falsifiability clause
  - P-03 (Governance Contract Test) — CI enforcement parent pattern
"""

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DOCS_ROOT = Path(__file__).parent.parent / "docs"
PROVENANCE_REGISTRY = DOCS_ROOT / "qa" / "METRICS_PROVENANCE.md"
REPORT_OUTPUT = DOCS_ROOT / "qa" / "PROVENANCE_LINT_REPORT.md"

# Unverified metric patterns to scan for
UNVERIFIED_METRICS = [
    {
        "pattern": r"340%",
        "description": "340% coordination gain",
        "status": "UNVERIFIED",
        "required_qualifier": r"UNVERIFIED|METRIC:UNVERIFIED",
        "priority": "P0",
    },
    {
        "pattern": r"cross.substrate replication",
        "description": "Cross-substrate replication gap",
        "status": "UNVERIFIED",
        "required_qualifier": r"UNVERIFIED|METRIC:UNVERIFIED",
        "priority": "P1",
    },
]

# ---------------------------------------------------------------------------
# STUB: Implementation placeholder
# ---------------------------------------------------------------------------

def scan_file(filepath: Path) -> list:
    """
    STUB — Scan a single markdown file for unverified metric occurrences
    without required qualifiers.
    Returns: list of violation dicts with keys: file, line, metric, context
    TODO (Role 5): Implement.
    """
    raise NotImplementedError("scan_file() — stub. Pending Role 5.")


def write_report(violations: list, scanned: int) -> None:
    """
    STUB — Write PROVENANCE_LINT_REPORT.md to docs/qa/
    TODO (Role 5): Implement.
    """
    raise NotImplementedError("write_report() — stub. Pending Role 5.")


def main() -> int:
    """
    STUB entry point — exits 0 (pass-through) until full implementation.
    IMPORTANT: Switch to sys.exit(len(violations)) once implemented.
    """
    print("[lint_provenance] STUB v0.1 — pass-through mode. Full implementation pending Role 5.")
    print(f"[lint_provenance] Would scan: {DOCS_ROOT}")
    print(f"[lint_provenance] Tracking {len(UNVERIFIED_METRICS)} unverified metric(s): " +
          ", ".join(m['description'] for m in UNVERIFIED_METRICS))
    print("[lint_provenance] PASS (stub — not enforcing). See QA-05 backlog.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
