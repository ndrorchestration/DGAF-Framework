#!/usr/bin/env python3
"""Validate the NDR human/machine registry release identity."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "docs" / "NDR_PATTERN_REGISTRY_UNIFIED.md"
MACHINE = ROOT / "docs" / "ndr_patterns_unified.json"

md = MARKDOWN.read_text(encoding="utf-8")
data = json.loads(MACHINE.read_text(encoding="utf-8"))

md_release = re.search(r"Registry release identity:\*\*\s+`([^`]+)`", md)
md_watermark = re.search(r"Effective watermark:\*\*\s+\*\*(P-\d+)\*\*", md)
md_total = re.search(r"Total named P-series patterns\s*\|\s*\*\*(\d+)\*\*", md)
if not (md_release and md_watermark and md_total):
    raise SystemExit("Registry consistency check failed: canonical Markdown metadata is not parseable.")

release_id = md_release.group(1)
md_watermark_n = int(md_watermark.group(1).split("-")[1])
md_total_n = int(md_total.group(1))

json_watermark = str(data.get("registry_watermark", ""))
json_total = int(data.get("total_p_series", 0))
json_version = str(data.get("version", ""))
json_updated = str(data.get("last_updated", ""))

expected_release = "NDR-REGISTRY-2026-07-03-P42"

if release_id != expected_release:
    raise SystemExit(f"Registry consistency check failed: unexpected release identity {release_id!r}.")

if md_watermark_n != 42 or md_total_n != 42:
    raise SystemExit(
        f"Registry consistency check failed: Markdown={md_watermark_n}/{md_total_n}; expected P-42/42."
    )

if json_watermark != "P-42" or json_total != 42:
    raise SystemExit(
        f"Registry consistency check failed: JSON={json_watermark}/{json_total}; expected P-42/42."
    )

if json_version != "2.4" or json_updated != "2026-07-03":
    raise SystemExit(
        "Registry consistency check failed: machine-readable release metadata "
        f"version={json_version!r}, updated={json_updated!r}."
    )

print(
    "Registry identity check passed: "
    f"{release_id} / P-42 / 42 patterns / JSON v{json_version}."
)
