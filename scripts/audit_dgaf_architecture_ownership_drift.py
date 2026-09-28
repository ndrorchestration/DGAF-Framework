from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "architecture" / "DGAF_ARTIFACT_OWNERSHIP_REGISTRY.v1.json"

SENSITIVE_PATTERNS = (
    re.compile(r"authorization|authorize|admission|allow|deny|policy", re.I),
    re.compile(r"state_machine|transition|control_state|status", re.I),
    re.compile(r"replay|idempot|revocation|trust_anchor", re.I),
    re.compile(r"custody|freeze|unblind|materializ", re.I),
    re.compile(r"receipt|provenance|evidence|attestation", re.I),
    re.compile(r"rollback|compensat|reconcil|postcondition", re.I),
)

IN_SCOPE_PREFIXES = ("scripts/","schemas/","app/lib/","registry/")
EXTENSIONS = {".py",".ts",".js",".json",".yaml",".yml"}


def registered_paths() -> set[str]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {str(r["path"]) for r in data["records"]}


def candidate_paths() -> list[str]:
    registered = registered_paths()
    findings: list[str] = []
    for prefix in IN_SCOPE_PREFIXES:
        base = ROOT / prefix
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in registered:
                continue
            if any(part in {"node_modules","__pycache__"} for part in path.parts):
                continue
            name_hit = any(rx.search(rel) for rx in SENSITIVE_PATTERNS)
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")[:12000]
            except OSError:
                text = ""
            content_hits = sum(bool(rx.search(text)) for rx in SENSITIVE_PATTERNS)
            if name_hit or content_hits >= 2:
                findings.append(rel)
    return sorted(set(findings))


def main() -> int:
    findings = candidate_paths()
    print("DGAF architecture ownership drift scan: ADVISORY")
    print(f"UNMAPPED_AUTHORITY_SENSITIVE_CANDIDATES={len(findings)}")
    for path in findings:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
