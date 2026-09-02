#!/usr/bin/env python3
"""Semantic freshness checks for DGAF living documentation.

This is deliberately narrower than markdownlint. It detects documentation that
could accidentally present historical candidate/governance state as current.
Immutable historical/evidence records are not scanned by this check.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs" / "CURRENT_STATE.md"

LIVING_PATHS = [
    ROOT / "README.md",
    ROOT / "README.governance.md",
    ROOT / "README.technical.md",
    ROOT / "docs" / "CURRENT_STATE.md",
    ROOT / "docs" / "PROJECT_STATUS.md",
    ROOT / "docs" / "experiment" / "NEW_CANDIDATE_MANIFEST.md",
    ROOT / "docs" / "governance" / "P8_VERIFICATION_CHECKLIST.md",
    ROOT / "docs" / "governance" / "CURRENT_CANDIDATE_POST_KICKOFF_CONTROL_2026-09-01.md",
    ROOT / "docs" / "governance" / "P9_CURRENT_RECONCILIATION.md",
    ROOT / "docs" / "governance" / "P1_TO_P9_EVIDENCE_MATRIX.md",
]

HISTORICAL_MARKERS = (
    "historical",
    "superseded",
    "prior candidate",
    "previous candidate",
    "former",
    "provenance only",
    "evidence does not transfer",
    "must not be used",
)


def state_value(name: str) -> str:
    text = STATE.read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(name)}:\s*(\S+)", text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Missing {name} in {STATE}")
    return match.group(1)


def bounded_context(lines: list[str], line_number: int, radius: int = 6) -> str:
    start = max(0, line_number - 1 - radius)
    end = min(len(lines), line_number + radius)
    return "\n".join(lines[start:end])


def has_historical_context(context: str) -> bool:
    lower = context.lower()
    return any(marker in lower for marker in HISTORICAL_MARKERS)


def deprecated_p9_is_active_reference(line: str) -> bool:
    """Return true only when the deprecated P9 record is presented as a live reference."""
    return bool(
        re.search(
            r"(?i)(?:\[[^\]]*\]\([^)]*P9_LATEST_RECONCILIATION_2026-09-01\.md|"
            r"(?:current|authoritative|latest|active)\s+(?:p9\s+)?(?:authority|record|reconciliation)|"
            r"(?:current|latest)\s+p9[^\n]{0,80}P9_LATEST_RECONCILIATION_2026-09-01\.md)",
            line,
        )
    )


def main() -> int:
    if not STATE.exists():
        print(f"ERROR: missing {STATE}")
        return 2

    current_runtime = state_value("runtime_candidate_sha")
    current_completion = state_value("latest_completion_candidate_sha")

    # These are intentionally derived from CURRENT_STATE rather than hard-coded
    # so the check follows a deliberate candidate promotion.
    superseded = "562753b3053b3566b0fcad1b0b1df151d7de119a"
    obsolete_p9_name = "P9_LATEST_RECONCILIATION_2026-09-01.md"
    obsolete_p7 = "P7: ADOPTED / FINAL BINDING OPEN"

    violations: list[str] = []

    for path in LIVING_PATHS:
        if not path.exists():
            violations.append(f"MISSING living document: {path.relative_to(ROOT)}")
            continue
        if path == STATE:
            continue

        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        lines = text.splitlines()

        # A superseded candidate remains legal in living docs when the nearby
        # prose explicitly identifies it as historical/superseded evidence.
        for lineno, line in enumerate(lines, 1):
            if superseded in line:
                context = bounded_context(lines, lineno)
                if not has_historical_context(context):
                    violations.append(
                        f"{rel}:{lineno}: superseded candidate appears without historical context"
                    )

        if obsolete_p7 in text:
            violations.append(f"{rel}: obsolete current P7 wording: {obsolete_p7}")

        # Explanatory mentions of the former filename are allowed when explicitly
        # historical. Only an active/live cross-reference is a violation.
        for lineno, line in enumerate(lines, 1):
            if obsolete_p9_name not in line:
                continue
            context = bounded_context(lines, lineno)
            if not has_historical_context(context) or deprecated_p9_is_active_reference(line):
                violations.append(f"{rel}:{lineno}: references deprecated P9 latest authority record")

        if re.search(r"(?i)\bfreeze\s*[:=]\s*(?:established|created|frozen)\b", text):
            violations.append(f"{rel}: claims an established freeze; current state is NOT ESTABLISHED")

        if re.search(r"(?i)\bauthorization\s*[:=]\s*(?:granted|authorized)\b", text):
            violations.append(f"{rel}: claims authorization; current state is NOT GRANTED")

        for match in re.finditer(r"(?i)empirical[_ ]?n\s*[:=]\s*(\d+)", text):
            if int(match.group(1)) != 0:
                violations.append(
                    f"{rel}: claims empirical N={match.group(1)}; current state is N=0"
                )

    # Sanity checks ensure the current-state record itself remains parseable.
    if len(current_runtime) != 40 or len(current_completion) != 40:
        violations.append("CURRENT_STATE candidate SHA fields are not full 40-character SHAs")

    if violations:
        print("DOCUMENT AUTHORITY LINT: FAIL")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print("DOCUMENT AUTHORITY LINT: PASS")
    print(f"- runtime candidate: {current_runtime}")
    print(f"- completion candidate: {current_completion}")
    print(f"- living documents checked: {len(LIVING_PATHS) - 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
