from __future__ import annotations

import csv
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
BLIND_LABELS = {name: f"Topology_{chr(65 + i)}" for i, name in enumerate(TOPOLOGIES)}


def blind_rows(rows: Iterable[dict]) -> list[dict]:
    """Return copies with topology identities masked for pilot precision work."""
    return [{**row, "topology": BLIND_LABELS[row["topology"]]} for row in rows]


def write_csv(rows: Iterable[dict], commit_short: str, output_dir: str | Path) -> tuple[Path, str]:
    destination_dir = Path(output_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = destination_dir / f"raw_pilot_{commit_short}_{timestamp}.csv"
    rows = list(rows)
    if not rows:
        raise ValueError("cannot persist an empty pilot dataset")
    fields = sorted({key for row in rows for key in row})
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    (destination.with_suffix(destination.suffix + ".sha256")).write_text(
        f"{digest}  {destination.name}\n", encoding="utf-8"
    )
    return destination, digest


def environment_commit_short() -> str:
    sha = os.environ.get("GITHUB_SHA", "local-unversioned")
    return sha[:7] if sha != "local-unversioned" else sha
