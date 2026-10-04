#!/usr/bin/env python3
"""Advisory lifecycle consistency checks for adopted DGAF architecture controls."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[1]

ACTIVE_NON_AUTHORIZING = "ACTIVE_NON_AUTHORIZING"
ACCEPTED = "ACCEPTED"

ALLOWED_LIFECYCLE_STATES = {
    "PROPOSED",
    ACTIVE_NON_AUTHORIZING,
    ACCEPTED,
    "REJECTED",
    "SUPERSEDED",
    "HISTORICAL",
    "RETIRED",
}

# This is intentionally an explicit adopted baseline rather than a recursive
# scan. Historical/proposed architecture material may legitimately use other
# lifecycle states and must not be silently promoted by file presence alone.
ADOPTED_BASELINE: Mapping[str, str] = {
    "docs/architecture/DGAF_ARCHITECTURE_LIFECYCLE_VOCABULARY.md": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_EVIDENCE_STATE_SEMANTIC_MAPPING.md": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_SYSTEM_ARCHITECTURE_TAXONOMY.md": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_CORE_COMPONENT_INVENTORY.md": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_ARCHITECTURE_MAPPING_METHOD.md": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_CUSTODY_FREEZE_RECOVERY_BOUNDARY.md": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/AAR_DGAF_KERNEL_ALIGNMENT.md": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_ARCHITECTURE_DEBT_REGISTER.v1.json": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_ARTIFACT_OWNERSHIP_REGISTRY.v1.json": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_ASSURANCE_BUNDLE_REGISTRY.v1.json": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_PROFILE_BUNDLE_REGISTRY.v1.json": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/DGAF_CORE_COMPONENT_REGISTRY.v1.json": ACTIVE_NON_AUTHORIZING,
    "docs/architecture/ADR-001-DGAF-ARCHITECTURE-OWNERSHIP-MAPPING.md": ACCEPTED,
}

_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s+([A-Z_]+)\b", re.MULTILINE)


def read_lifecycle(path: Path) -> str:
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        status = data.get("status")
        if not isinstance(status, str) or not status:
            raise ValueError(f"{path}: top-level status missing")
        return status

    text = path.read_text(encoding="utf-8")
    match = _STATUS_RE.search(text)
    if match is None:
        raise ValueError(f"{path}: Markdown status missing or unparseable")
    return match.group(1)


def validate_architecture_lifecycle(
    *,
    root: Path = ROOT,
    baseline: Mapping[str, str] = ADOPTED_BASELINE,
) -> list[str]:
    errors: list[str] = []

    for relative_path, expected in baseline.items():
        path = root / relative_path
        if not path.is_file():
            errors.append(f"{relative_path}: adopted architecture control missing")
            continue

        try:
            observed = read_lifecycle(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
            continue

        if observed not in ALLOWED_LIFECYCLE_STATES:
            errors.append(f"{relative_path}: invalid lifecycle state {observed!r}")
            continue

        is_adr = Path(relative_path).name.startswith("ADR-")
        if observed in {"ACCEPTED", "REJECTED"} and not is_adr:
            errors.append(f"{relative_path}: {observed} is reserved for architecture decision records")

        if observed != expected:
            errors.append(f"{relative_path}: lifecycle {observed!r} != adopted baseline {expected!r}")

    return errors


def main() -> int:
    errors = validate_architecture_lifecycle()
    if errors:
        print("DGAF architecture lifecycle consistency: ADVISORY_FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("DGAF architecture lifecycle consistency: PASS " f"({len(ADOPTED_BASELINE)} adopted controls)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
