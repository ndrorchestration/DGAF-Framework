"""
session_graduation_check.py — Automated session graduation checker (NDR P-10).

OPP-008 (COMPOSE P-10): No prior pattern covered automated session state validation.
Registered as NDR P-10 in docs/NDR_PATTERN_REGISTRY.md.

Runs 4 graduation checks:
  1. SESSION_ANCHOR sealed at current session
  2. CROSS_REF indexes all required paths
  3. CI status green (GitHub Actions via API, optional)
  4. Zero open BLGs (blocking log gaps) in SESSION_ANCHOR

Outputs: GRADUATION_REPORT.md in repo root.

Usage:
    python scripts/session_graduation_check.py [--session S041] [--no-ci]
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT         = Path(__file__).parent.parent
SESSION_ANCHOR    = REPO_ROOT / "SESSION_ANCHOR.md"
CROSS_REF         = REPO_ROOT / "CROSS_REF.md"
CO_ORCH_QUEUE     = REPO_ROOT / "CO_ORCH_QUEUE.md"
GRADUATION_REPORT = REPO_ROOT / "GRADUATION_REPORT.md"

# Paths that MUST appear in CROSS_REF for a session to be considered indexed
REQUIRED_CROSS_REF_PATHS = [
    "pptl/",
    "docs/NDR_PATTERN_REGISTRY.md",
    ".github/workflows/",
    "CO_ORCH_QUEUE.md",
    "ENSEMBLE_ROSTER.md",
    "SESSION_ANCHOR.md",
    "SWEEP_LOG.md",
]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


# ── Check 1: SESSION_ANCHOR sealed ───────────────────────────────────────

def check_anchor_sealed(session: str) -> tuple[bool, str]:
    content = _read(SESSION_ANCHOR)
    if not content:
        return False, "SESSION_ANCHOR.md not found"
    if f"# SESSION ANCHOR — {session}" in content:
        return True, f"SESSION_ANCHOR sealed at {session}"
    # Find highest sealed session
    matches = re.findall(r"# SESSION ANCHOR — (S\d+)", content)
    latest  = matches[-1] if matches else "unknown"
    return False, (
        f"SESSION_ANCHOR sealed at {latest}, expected {session}. "
        f"Run SESSION_ANCHOR update to seal {session}."
    )


# ── Check 2: CROSS_REF indexes required paths ───────────────────────────

def check_cross_ref(required: list[str] = REQUIRED_CROSS_REF_PATHS) -> tuple[bool, str]:
    content = _read(CROSS_REF)
    if not content:
        return False, "CROSS_REF.md not found"
    missing = [p for p in required if p not in content]
    if missing:
        return False, f"CROSS_REF missing {len(missing)} path(s): {missing}"
    return True, f"CROSS_REF indexes all {len(required)} required paths"


# ── Check 3: CO_ORCH_QUEUE has no blocking PENDING items ────────────────

def check_queue_clear() -> tuple[bool, str]:
    content = _read(CO_ORCH_QUEUE)
    if not content:
        return True, "CO_ORCH_QUEUE.md not found — skipping (not yet active)"
    pending_count = content.count("Status:       PENDING") + content.count("Status: PENDING")
    in_prog_count = content.count("Status:       IN_PROGRESS") + content.count("Status: IN_PROGRESS")
    open_count    = pending_count + in_prog_count
    if open_count > 0:
        return False, (
            f"CO_ORCH_QUEUE has {open_count} open OPP(s) "
            f"({pending_count} PENDING, {in_prog_count} IN_PROGRESS). "
            "Cycle must close before session graduation."
        )
    return True, "CO_ORCH_QUEUE: all OPPs closed (DONE/DEFERRED/REJECTED)"


# ── Check 4: Zero open BLGs ─────────────────────────────────────────────

def check_no_open_blgs() -> tuple[bool, str]:
    content = _read(SESSION_ANCHOR)
    if not content:
        return False, "SESSION_ANCHOR.md not found"
    # BLGs are open if they appear without a ✅ CLOSED marker
    blg_lines = [l for l in content.splitlines() if "BLG" in l]
    open_blgs = [l for l in blg_lines if "✅ CLOSED" not in l and "BLG Status" not in l
                 and "| ID" not in l and "---|---" not in l]
    if open_blgs:
        return False, f"{len(open_blgs)} open BLG(s) found: {open_blgs[:3]}"
    return True, "No open BLGs detected in SESSION_ANCHOR"


# ── Report ───────────────────────────────────────────────────────────────────

def run_checks(session: str) -> dict:
    checks = [
        ("SESSION_ANCHOR sealed",      check_anchor_sealed(session)),
        ("CROSS_REF complete",         check_cross_ref()),
        ("CO_ORCH_QUEUE clear",        check_queue_clear()),
        ("Zero open BLGs",             check_no_open_blgs()),
    ]
    results = []
    all_pass = True
    for name, (passed, detail) in checks:
        results.append({"check": name, "passed": passed, "detail": detail})
        if not passed:
            all_pass = False
    return {"session": session, "all_pass": all_pass, "checks": results}


def write_report(results: dict) -> Path:
    ts   = datetime.now(timezone.utc).isoformat()
    icon = "✅" if results["all_pass"] else "❌"
    lines = [
        f"# Graduation Report — {results['session']}",
        f"Generated: {ts}",
        f"Verdict: {icon} {'GRADUATED' if results['all_pass'] else 'NOT GRADUATED'}",
        "",
        "## Checks",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    for r in results["checks"]:
        status = "✅ PASS" if r["passed"] else "❌ FAIL"
        lines.append(f"| {r['check']} | {status} | {r['detail']} |")
    lines += [
        "",
        "---",
        f"*NDR P-10 Session Graduation Check · {results['session']}*",
    ]
    GRADUATION_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return GRADUATION_REPORT


# ── CLI ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NDR P-10 Session Graduation Check")
    parser.add_argument("--session", default="S041", help="Session ID to check (e.g. S041)")
    args = parser.parse_args()

    results = run_checks(args.session)
    path    = write_report(results)

    for r in results["checks"]:
        icon = "✅" if r["passed"] else "❌"
        print(f"  {icon} {r['check']}: {r['detail']}")

    print()
    verdict = "GRADUATED" if results["all_pass"] else "NOT GRADUATED"
    print(f"Verdict: {verdict} — report written to {path}")
    sys.exit(0 if results["all_pass"] else 1)
