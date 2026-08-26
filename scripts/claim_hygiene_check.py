#!/usr/bin/env python3
"""Block active public claim-language that exceeds the current DGAF evidence policy.

Historical records are allowed when the same artifact explicitly labels the status
as historical/attested. Policy and governance documents are excluded from direct
status scanning because they define the rules rather than claim conformance.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {
    Path("docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md"),
    Path("docs/evidence/EVIDENCE_LADDER_POLICY.md"),
    Path("docs/evidence/EPISTEMIC_CONSISTENCY_RULES.md"),
    Path("docs/EPISTEMIC_EVIDENCE_STANDARD.md"),
}

PATTERNS = [
    re.compile(r"\bDGAF\s+(?:Certified|Official|Endorsed|Verified|Approved)\b", re.I),
    re.compile(r"\b(?:production[- ]ready|guarantees? convergence|guaranteed convergence)\b", re.I),
    re.compile(r"\b(?:universally safe|universal safety|proven efficacy|empirically superior)\b", re.I),
]

HISTORICAL_MARKERS = re.compile(
    r"\b(?:historical|historically|historical metadata|attested project metadata|legacy)\b",
    re.I,
)

for path in ROOT.rglob("*.md"):
    rel = path.relative_to(ROOT)
    if rel in EXCLUDED or ".git" in rel.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for lineno, line in enumerate(text.splitlines(), 1):
        if not any(p.search(line) for p in PATTERNS):
            continue
        # Historical records are permitted only when the artifact itself labels the
        # surrounding record historical/attested; current-looking claims remain fatal.
        if HISTORICAL_MARKERS.search(line):
            continue
        print(f"::error file={rel},line={lineno}::{line.strip()}")
        raise SystemExit(1)

print("Claim-hygiene check passed: no unbounded active certification/efficacy/convergence language detected.")
