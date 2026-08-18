"""CI guardrail for DGAF evidence-tier integrity.

The validator is intentionally conservative: it fails on ambiguous or
contradictory evidence declarations instead of guessing intent.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence" / "claims.json"
SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}
FORBIDDEN_PRODUCTION_MARKERS = (
    "// stub",
    "# stub",
    "notimplemented",
    "not implemented",
    "placeholder",
)


def load_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise ValueError("evidence/claims.json must contain a top-level claims list")
    return data


def iter_sources() -> list[Path]:
    roots = [ROOT / "app", ROOT / "pages", ROOT / "components", ROOT / "src", ROOT / "tests", ROOT / "tools"]
    files: list[Path] = []
    for base in roots:
        if not base.exists():
            continue
        files.extend(p for p in base.rglob("*") if p.is_file() and p.suffix in SOURCE_EXTENSIONS)
    return files


def main() -> int:
    failures: list[str] = []
    registry = load_registry()
    claim_ids = set()

    for claim in registry["claims"]:
        claim_id = claim.get("claim_id")
        mode = claim.get("evidence_mode")
        if not claim_id:
            failures.append("claim without claim_id")
            continue
        if claim_id in claim_ids:
            failures.append(f"duplicate claim_id: {claim_id}")
        claim_ids.add(claim_id)
        if mode not in {"synthetic", "integration", "empirical", "production"}:
            failures.append(f"{claim_id}: unsupported evidence_mode={mode!r}")
        if mode in {"empirical", "production"} and not claim.get("run_id"):
            failures.append(f"{claim_id}: {mode} claim requires run_id")
        if mode == "empirical" and not claim.get("dataset"):
            failures.append(f"{claim_id}: empirical claim requires dataset")
        if claim.get("status") == "VERIFIED" and mode in {"synthetic", "integration"}:
            failures.append(f"{claim_id}: VERIFIED cannot be backed only by {mode} evidence")

    # Guard explicit production/evidence annotations against obvious stubs.
    pattern = re.compile(r"evidence_mode\(\s*['\"]production['\"]")
    for path in iter_sources():
        text = path.read_text(encoding="utf-8", errors="replace")
        if not pattern.search(text):
            continue
        lowered = text.lower()
        for marker in FORBIDDEN_PRODUCTION_MARKERS:
            if marker in lowered:
                failures.append(f"{path.relative_to(ROOT)}: production source contains forbidden marker {marker!r}")

    if failures:
        print("TRUTH-LAYER VALIDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("TRUTH-LAYER VALIDATION: PASS")
    print(f"Claims checked: {len(registry['claims'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
