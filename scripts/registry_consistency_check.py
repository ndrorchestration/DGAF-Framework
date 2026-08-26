#!/usr/bin/env python3
"""Ensure the human-readable and machine-readable NDR registries agree on identity."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "docs" / "NDR_PATTERN_REGISTRY_UNIFIED.md"
MACHINE = ROOT / "docs" / "ndr_patterns_unified.json"

md = MARKDOWN.read_text(encoding="utf-8")
data = json.loads(MACHINE.read_text(encoding="utf-8"))

md_match = re.search(r"\*\*Registry watermark:\*\*\s+\*\*(P-\d+)\*\*", md)
md_total = re.search(r"\*\*Total named patterns \(P-series\)\*\*\s+\*\*(\d+)\*\*", md)
if not md_match or not md_total:
    raise SystemExit("Registry consistency check failed: canonical Markdown metadata is not parseable.")

md_watermark = md_match.group(1)
md_total_n = int(md_total.group(1))
json_watermark = str(data.get("registry_watermark", ""))
json_total = int(data.get("total_p_series", 0))

if md_watermark != json_watermark or md_total_n != json_total:
    raise SystemExit(
        "Registry consistency check failed: "
        f"Markdown={md_watermark}/{md_total_n}; JSON={json_watermark}/{json_total}."
    )

print(f"Registry consistency check passed: {md_watermark} / {md_total_n} patterns.")
