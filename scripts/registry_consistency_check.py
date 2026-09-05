#!/usr/bin/env python3
"""Validate the NDR human/machine registry release identity and provenance lock."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "docs" / "NDR_PATTERN_REGISTRY_UNIFIED.md"
MACHINE = ROOT / "docs" / "ndr_patterns_unified.json"
MANIFEST = ROOT / "docs" / "NDR_REGISTRY_RELEASE_MANIFEST.json"

md = MARKDOWN.read_text(encoding="utf-8")
data = json.loads(MACHINE.read_text(encoding="utf-8"))
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

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
expected_source_commit = "165e24acec4518c11cc1fbe14d44cabac3fd9b9c"
expected_schema = "2.4"
expected_updated = "2026-07-03"

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
if json_version != expected_schema or json_updated != expected_updated:
    raise SystemExit(
        "Registry consistency check failed: machine-readable release metadata "
        f"version={json_version!r}, updated={json_updated!r}."
    )

if manifest.get("registry_release_identity") != expected_release:
    raise SystemExit("Registry provenance check failed: manifest release identity mismatch.")
if manifest.get("representation_source_commit") != expected_source_commit:
    raise SystemExit("Registry provenance check failed: representation source commit mismatch.")
if manifest.get("machine_readable_schema_version") != expected_schema:
    raise SystemExit("Registry provenance check failed: manifest schema version mismatch.")
if manifest.get("effective_watermark") != "P-42":
    raise SystemExit("Registry provenance check failed: manifest watermark mismatch.")


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()

expected_md_sha = manifest["representations"]["markdown"]["git_blob_sha1"]
expected_json_sha = manifest["representations"]["machine_readable"]["git_blob_sha1"]
actual_md_sha = git_blob_sha1(MARKDOWN)
actual_json_sha = git_blob_sha1(MACHINE)
if actual_md_sha != expected_md_sha:
    raise SystemExit(
        f"Registry provenance check failed: Markdown blob {actual_md_sha} != {expected_md_sha}."
    )
if actual_json_sha != expected_json_sha:
    raise SystemExit(
        f"Registry provenance check failed: machine-readable blob {actual_json_sha} != {expected_json_sha}."
    )

print(
    "Registry identity + provenance check passed: "
    f"{release_id} / P-42 / 42 patterns / JSON v{json_version}; "
    f"source={expected_source_commit[:12]}…; "
    f"markdown={actual_md_sha[:12]}…; json={actual_json_sha[:12]}…."
)
