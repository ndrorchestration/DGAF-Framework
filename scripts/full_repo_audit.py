#!/usr/bin/env python3
"""Full tracked-file repository coverage and consistency audit.

QA/reporting control only. This inventories every Git-tracked file, hashes each
file, scans readable text, and reports possible consistency/provenance findings.
It never promotes evidence, rewrites history, or authorizes a freeze.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

PATTERNS = {
    "historical_freeze": "3510b86889cd341f7a7cf9ab684fd37b2fafd758",
    "historical_p6a": "e1f077fec746acd6066db689ef40db000e027f2f",
    "claim_340": "340%",
    "flag_02": "FLAG-02",
    "pilot_authorization": "PDMAL_PILOT_AUTHORIZED",
    "empirical_zero": "Empirical N = 0",
    "new_freeze_false": "new_freeze_created: false",
}

FULL_SHA = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")


def tracked_files() -> list[Path]:
    raw = subprocess.check_output(["git", "ls-files", "-z"])
    return [Path(x.decode("utf-8")) for x in raw.split(b"\0") if x]


def read_text(path: Path) -> tuple[str | None, bytes]:
    data = path.read_bytes()
    if b"\x00" in data[:8192]:
        return None, data
    try:
        return data.decode("utf-8"), data
    except UnicodeDecodeError:
        return None, data


def semantic_findings(path: Path, text: str, head: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    normalized = path.as_posix()
    is_workflow = normalized.startswith(".github/workflows/")

    if normalized == "scripts/full_repo_audit.py":
        return findings

    if is_workflow:
        repository_binding_text = "\n".join(
            line
            for line in text.splitlines()
            if not re.match(
                r"^\s*-?\s*uses:\s*[^\s@]+@[0-9a-fA-F]{40}(?:\s|#|$)",
                line,
            )
        )
        for referenced in sorted(set(FULL_SHA.findall(repository_binding_text))):
            if referenced != head:
                findings.append(
                    {
                        "severity": "REVIEW",
                        "type": "workflow_literal_40hex_review",
                        "path": str(path),
                        "referenced_commit": referenced,
                        "audit_head": head,
                    }
                )

        if "EXPECTED_COMMIT" in text and "e1f077f" in text:
            findings.append(
                {
                    "severity": "CRITICAL",
                    "type": "workflow_historical_commit_binding",
                    "path": str(path),
                }
            )

    lower = text.lower()

    def windows(needle: str, radius: int = 320) -> list[str]:
        out: list[str] = []
        start = 0
        needle_lower = needle.lower()
        while True:
            idx = lower.find(needle_lower, start)
            if idx < 0:
                break
            out.append(lower[max(0, idx - radius) : idx + len(needle) + radius])
            start = idx + len(needle)
        return out

    claim_340_qualifiers = (
        "unverified",
        "historical",
        "illustrative",
        "not canonical",
        "not a current verified result",
        "must not be interpreted as",
        "requires empirical validation",
        "downgraded",
        "correction",
        "not 340%",
        "corrected to",
        "replaced with",
    )
    for context in windows("340%"):
        has_promotion = any(word in context for word in ("closed", "verified", "confirmed"))
        has_qualifier = any(q in context for q in claim_340_qualifiers)
        if has_promotion and not has_qualifier:
            findings.append(
                {
                    "severity": "HIGH",
                    "type": "340_claim_status_language",
                    "path": str(path),
                }
            )
            break

    flag02_qualifiers = (
        "historical",
        "formerly",
        "former ",
        "temporal namespace",
        "current terminology correction",
        "legacy",
        "superseded",
    )
    for context in windows("FLAG-02"):
        if "qualitative" not in context:
            continue
        if any(q in context for q in flag02_qualifiers):
            continue
        findings.append(
            {
                "severity": "REVIEW",
                "type": "FLAG02_namespace_migration",
                "path": str(path),
            }
        )
        break

    return findings


def main() -> int:
    files = tracked_files()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    records: list[dict[str, object]] = []
    findings: list[dict[str, object]] = []
    counts: dict[str, int] = {name: 0 for name in PATTERNS}

    for path in files:
        text, data = read_text(path)
        record: dict[str, object] = {
            "path": str(path),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "text": text is not None,
        }
        if text is not None:
            matches: dict[str, int] = {}
            for name, pattern in PATTERNS.items():
                count = text.count(pattern)
                counts[name] += count
                if count:
                    matches[name] = count
            if matches:
                record["matches"] = matches

            findings.extend(semantic_findings(path, text, head))

        records.append(record)

    if Path("SESSION_ANCHOR.md").exists() and Path("docs/SESSION_ANCHORS.md").exists():
        findings.append(
            {
                "severity": "HIGH",
                "type": "duplicate_anchor_documents",
                "paths": ["SESSION_ANCHOR.md", "docs/SESSION_ANCHORS.md"],
            }
        )

    report = {
        "schema_version": "1.1",
        "audit_head": head,
        "tracked_file_count": len(files),
        "text_file_count": sum(1 for r in records if bool(r["text"])),
        "binary_or_unreadable_count": sum(1 for r in records if not bool(r["text"])),
        "pattern_counts": counts,
        "findings": findings,
        "files": records,
    }
    Path("full_repo_audit.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    summary = {
        "audit_head": head,
        "tracked_file_count": len(files),
        "text_file_count": report["text_file_count"],
        "binary_or_unreadable_count": report["binary_or_unreadable_count"],
        "pattern_counts": counts,
        "finding_count": len(findings),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    for finding in findings:
        print(json.dumps(finding, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
