#!/usr/bin/env python3
"""
P-10 — Session Graduation Check
DGAF-Framework · NDR Pattern P-10

Runs 4 checks to verify session is ready to graduate.
Outputs GRADUATION_REPORT.md with pass/fail per check.
sys.exit(1) on any failure — CI-integrable as pre-push hook or merge gate.

Usage:
    python scripts/session_graduation_check.py --session S041
    python scripts/session_graduation_check.py --session S042 --anchor SESSION_ANCHOR.md
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

CROSS_REF_REQUIRED_PATHS = [
    "pptl/",
    "docs/NDR_PATTERN_REGISTRY.md",
    ".github/workflows/",
    "CO_ORCH_QUEUE.md",
    "ENSEMBLE_ROSTER.md",
    "SESSION_ANCHOR.md",
    "SWEEP_LOG.md",
]


def check_session_anchor_sealed(session: str, anchor_path: Path) -> tuple[bool, str]:
    """Check 1: SESSION_ANCHOR.md header contains '# SESSION ANCHOR — {session}'"""
    if not anchor_path.exists():
        return False, f"SESSION_ANCHOR not found at {anchor_path}"
    content = anchor_path.read_text(encoding="utf-8")
    expected = f"# SESSION ANCHOR — {session}"
    if expected in content:
        return True, f"Found '{expected}' in SESSION_ANCHOR.md"
    return False, f"Expected '{expected}' not found in SESSION_ANCHOR.md"


def check_cross_ref_complete(cross_ref_path: Path) -> tuple[bool, str]:
    """Check 2: CROSS_REF.md contains all required path strings."""
    if not cross_ref_path.exists():
        return False, f"CROSS_REF.md not found at {cross_ref_path}"
    content = cross_ref_path.read_text(encoding="utf-8")
    missing = [p for p in CROSS_REF_REQUIRED_PATHS if p not in content]
    if not missing:
        return True, f"All {len(CROSS_REF_REQUIRED_PATHS)} required paths present in CROSS_REF.md"
    return False, f"Missing from CROSS_REF.md: {missing}"


def check_co_orch_queue_clear(queue_path: Path) -> tuple[bool, str]:
    """Check 3: CO_ORCH_QUEUE.md has zero PENDING or IN_PROGRESS OPPs."""
    if not queue_path.exists():
        return False, f"CO_ORCH_QUEUE.md not found at {queue_path}"
    content = queue_path.read_text(encoding="utf-8")
    pending = len(re.findall(r"\bPENDING\b", content))
    in_progress = len(re.findall(r"\bIN_PROGRESS\b", content))
    open_items = pending + in_progress
    if open_items == 0:
        return True, "CO_ORCH_QUEUE.md: zero PENDING or IN_PROGRESS entries"
    return False, f"CO_ORCH_QUEUE.md has {open_items} open items (PENDING={pending}, IN_PROGRESS={in_progress})"


def check_zero_open_blgs(anchor_path: Path) -> tuple[bool, str]:
    """Check 4: No BLG entries without '✅ CLOSED' in SESSION_ANCHOR.md."""
    if not anchor_path.exists():
        return False, f"SESSION_ANCHOR not found at {anchor_path}"
    content = anchor_path.read_text(encoding="utf-8")
    blg_section_match = re.search(r"## BLG Status.*?(?=\n## |\Z)", content, re.DOTALL)
    if not blg_section_match:
        return False, "BLG Status section not found in SESSION_ANCHOR.md"
    blg_section = blg_section_match.group(0)
    rows = re.findall(r"\|\s*(S\d+-BLG-\S+|S\d+\s+\S+)\s*\|\s*(.+?)\s*\|", blg_section)
    open_blgs = [(ref, status) for ref, status in rows if "✅ CLOSED" not in status and "ALL RESOLVED" not in status]
    if not open_blgs:
        return True, f"BLG Status: all entries resolved ({len(rows)} total)"
    return False, f"Open BLGs: {[ref for ref, _ in open_blgs]}"


def run_graduation_check(session: str, anchor_path: Path = None, queue_path: Path = None,
                         cross_ref_path: Path = None) -> dict:
    anchor_path = anchor_path or REPO_ROOT / "SESSION_ANCHOR.md"
    queue_path = queue_path or REPO_ROOT / "CO_ORCH_QUEUE.md"
    cross_ref_path = cross_ref_path or REPO_ROOT / "CROSS_REF.md"

    checks = [
        ("SESSION_ANCHOR sealed", check_session_anchor_sealed(session, anchor_path)),
        ("CROSS_REF complete", check_cross_ref_complete(cross_ref_path)),
        ("CO_ORCH_QUEUE clear", check_co_orch_queue_clear(queue_path)),
        ("Zero open BLGs", check_zero_open_blgs(anchor_path)),
    ]

    results = {name: {"pass": passed, "detail": detail} for name, (passed, detail) in checks}
    all_pass = all(r["pass"] for r in results.values())
    verdict = "GRADUATED" if all_pass else "NOT READY"
    return {"session": session, "verdict": verdict, "all_pass": all_pass, "checks": results}


def write_graduation_report(result: dict, report_path: Path = None) -> Path:
    report_path = report_path or REPO_ROOT / "GRADUATION_REPORT.md"
    lines = [
        f"# GRADUATION REPORT — {result['session']}",
        f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Verdict:** {'\u2705 GRADUATED' if result['all_pass'] else '\u274c NOT READY'}",
        "",
        "## Check Results",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    for name, info in result["checks"].items():
        icon = "✅ PASS" if info["pass"] else "❌ FAIL"
        lines.append(f"| {name} | {icon} | {info['detail']} |")
    if not result["all_pass"]:
        lines += [
            "",
            "## Action Items",
            "",
            "Resolve all FAIL items before re-running graduation check.",
        ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="P-10 Session Graduation Check")
    parser.add_argument("--session", required=True, help="Session ID, e.g. S041")
    parser.add_argument("--anchor", default=None, help="Path to SESSION_ANCHOR.md")
    parser.add_argument("--queue", default=None, help="Path to CO_ORCH_QUEUE.md")
    parser.add_argument("--cross-ref", default=None, help="Path to CROSS_REF.md")
    parser.add_argument("--report", default=None, help="Output path for GRADUATION_REPORT.md")
    args = parser.parse_args()

    anchor = Path(args.anchor) if args.anchor else None
    queue = Path(args.queue) if args.queue else None
    cross_ref = Path(args.cross_ref) if args.cross_ref else None
    report = Path(args.report) if args.report else None

    result = run_graduation_check(args.session, anchor, queue, cross_ref)
    report_path = write_graduation_report(result, report)

    print(f"\nGRADUATION CHECK — {result['session']}")
    print(f"Verdict: {result['verdict']}")
    for name, info in result["checks"].items():
        icon = "✅" if info["pass"] else "❌"
        print(f"  {icon} {name}: {info['detail']}")
    print(f"\nReport written to: {report_path}")

    sys.exit(0 if result["all_pass"] else 1)


if __name__ == "__main__":
    main()
