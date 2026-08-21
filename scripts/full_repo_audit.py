#!/usr/bin/env python3
"""Full tracked-file repository coverage and consistency audit.

This is a QA/reporting control, not an epistemic authorization gate.
It inventories every Git-tracked file, hashes each file, scans readable text,
and records findings without silently rewriting historical evidence.
"""
from __future__ import annotations

import hashlib
import json
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


def main() -> int:
    files = tracked_files()
    records = []
    findings = []
    counts = {name: 0 for name in PATTERNS}

    for path in files:
        text, data = read_text(path)
        record = {
            "path": str(path),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "text": text is not None,
        }
        if text is not None:
            for name, pattern in PATTERNS.items():
                count = text.count(pattern)
                counts[name] += count
                if count:
                    record.setdefault("matches", {})[name] = count

            if "EXPECTED_COMMIT:" in text and "e1f077f" in text:
                findings.append({
                    "severity": "CRITICAL",
                    "type": "workflow_historical_commit_binding",
                    "path": str(path),
                })

            if "340%" in text and any(
                word in text.lower() for word in ("closed", "verified", "confirmed")
            ):
                findings.append({
                    "severity": "HIGH",
                    "type": "340_claim_status_language",
                    "path": str(path),
                })

            if "FLAG-02" in text and "qualitative" in text.lower():
                findings.append({
                    "severity": "REVIEW",
                    "type": "FLAG02_namespace_migration",
                    "path": str(path),
                })

        records.append(record)

    if Path("SESSION_ANCHOR.md").exists() and Path("docs/SESSION_ANCHORS.md").exists():
        findings.append({
            "severity": "HIGH",
            "type": "duplicate_anchor_documents",
            "paths": ["SESSION_ANCHOR.md", "docs/SESSION_ANCHORS.md"],
        })

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    report = {
        "schema_version": "1.0",
        "audit_head": head,
        "tracked_file_count": len(files),
        "text_file_count": sum(r["text"] for r in records),
        "binary_or_unreadable_count": sum(not r["text"] for r in records),
        "pattern_counts": counts,
        "findings": findings,
        "files": records,
    }
    Path("full_repo_audit.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )

    print(json.dumps({
        "audit_head": head,
        "tracked_file_count": len(files),
        "text_file_count": report["text_file_count"],
        "binary_or_unreadable_count": report["binary_or_unreadable_count"],
        "pattern_counts": counts,
        "finding_count": len(findings),
    }, indent=2, sort_keys=True))
    for finding in findings:
        print(json.dumps(finding, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
