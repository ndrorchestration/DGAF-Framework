#!/usr/bin/env python3
"""Block active public claim-language that exceeds the current DGAF evidence policy.

The checker scans the same text/source suffix family used by CI and distinguishes
historical records by artifact context. Explicit disclaimers and future-policy
statements are treated as non-assertive so the gate detects positive claims rather
than the vocabulary used to prohibit or qualify them.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
# Definitional policy / vocabulary / register docs whose purpose is to
# ENUMERATE the prohibited claim-language as rules or audit records. These are
# not active claims and would self-flag the checker's own vocabulary.
EXCLUDED_RAW = {
    "docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md",
    "docs/evidence/EVIDENCE_LADDER_POLICY.md",
    "docs/evidence/EPISTEMIC_CONSISTENCY_RULES.md",
    "docs/EPISTEMIC_EVIDENCE_STANDARD.md",
    "docs/EPISTEMIC_SUPERSESSION_REGISTER.md",
    "docs/QUALITY_REGISTRY_CLAIM_REVIEW_2026-08-16.md",
    "docs/SEMANTIC_CLAIM_REVIEW_2026-08-16.md",
    "docs/gates/ACOUSTIC_GATES.md",
    "docs/gates/GATE_1111.md",
    "docs/gates/GATE_11Q.md",
    "docs/gates/TELESCOPIC_LENS.md",
    "docs/taxonomy/EPISTEMIC_CROSS_REPO_SWEEP_2026-08-15.md",
    "docs/taxonomy/EPISTEMIC_VOCABULARY_STANDARD.md",
    "docs/research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md",
}
# Case-insensitive so exclusions apply on case-sensitive Linux CI regardless of
# on-disk casing (files are stored UPPERCASE, e.g. docs/EPISTEMIC_EVIDENCE_STANDARD.md).
EXCLUDED = {p.lower() for p in EXCLUDED_RAW}
ALLOWED_SUFFIXES = {".md", ".py", ".ts", ".tsx", ".yml", ".yaml", ".json"}
# CI workflows and this checker's own scripts are configuration, not publishable
# claim-language. The checker must not scan its own definition file
# (claim-hygiene.yml defines the 'production-ready' regex string and would
# self-flag) nor its own source/comment lines (which contain the lexicon).
EXCLUDED_PARTS = {".git", "node_modules", ".venv", "venv", "__pycache__", "htmlcov", ".github", "scripts"}

PATTERNS = [
    re.compile(r"\bDGAF\s+(?:Certified|Official|Endorsed|Verified|Approved)\b", re.I),
    re.compile(r"\b(?:production[- ]ready|guarantees? convergence|guaranteed convergence)\b", re.I),
    re.compile(r"\b(?:universally safe|universal safety|proven efficacy|empirically superior)\b", re.I),
]
HISTORICAL_CONTEXT = re.compile(
    r"\b(?:historical record|historical metadata|historically|legacy attestation|attested project metadata|historical certification|historical snapshot)\b",
    re.I,
)
ACTIVE_CONTEXT = re.compile(
    r"\b(?:current|active|production|live|present|now|today|status:\s*(?:certified|verified|approved))\b",
    re.I,
)
NON_ASSERTIVE_CONTEXT = re.compile(
    r"(?:\b(?:not|never|no|without|cannot|can't|must not|should not|do not|does not|doesn't)\b[^\n.;]{0,160}|\b(?:future|proposed|requires? separate governance|requires? explicit governance|requires? independent evidence)\b[^\n.;]{0,160})",
    re.I,
)


def line_is_non_assertive(line: str) -> bool:
    """Return True when a matched term appears inside an explicit disclaimer/policy."""
    return bool(NON_ASSERTIVE_CONTEXT.search(line))


def artifact_is_historical(text: str, line_number: int) -> bool:
    """Allow a flagged term only when the surrounding artifact is clearly historical.

    Look at the document header and a bounded context window around the finding.
    A single historical word on the same line as an active claim is insufficient.
    """
    lines = text.splitlines()
    header = "\n".join(lines[:40])
    start = max(0, line_number - 6)
    end = min(len(lines), line_number + 5)
    context = "\n".join(lines[start:end])
    return bool(
        HISTORICAL_CONTEXT.search(header)
        or (HISTORICAL_CONTEXT.search(context) and not ACTIVE_CONTEXT.search(context))
    )


def main() -> int:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in ALLOWED_SUFFIXES:
            continue
        rel = path.relative_to(ROOT)
        if rel.as_posix().lower() in EXCLUDED or any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        lines = text.splitlines()
        for lineno, line in enumerate(lines, 1):
            for pattern in PATTERNS:
                if not pattern.search(line):
                    continue
                if line_is_non_assertive(line) or artifact_is_historical(text, lineno):
                    continue
                print(f"::error file={rel},line={lineno}::Unsupported active claim-language: {line.strip()}")
                return 1

    print("Claim-hygiene check passed: no unbounded active certification/efficacy/convergence language detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
