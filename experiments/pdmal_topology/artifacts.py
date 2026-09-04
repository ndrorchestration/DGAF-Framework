from __future__ import annotations

import csv
import hashlib
import hmac
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")


def blind_label(topology: str, secret: str) -> str:
    if not secret:
        raise ValueError("a non-empty external blinding secret is required")
    digest = hmac.new(secret.encode("utf-8"), topology.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"Topology_{digest[:12]}"


def blind_rows(rows: Iterable[dict], secret: str) -> list[dict]:
    """Return copies with topology identities masked using an external secret."""
    return [{**row, "topology": blind_label(row["topology"], secret)} for row in rows]


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
    """Return the exact candidate identity supplied by the governance workflow.

    On pull_request runs GITHUB_SHA can identify GitHub's synthetic merge commit,
    while the workflow explicitly checks out CANDIDATE_SHA. Prefer the latter so
    persisted artifact names cannot silently bind to a different commit identity.
    """
    sha = os.environ.get("CANDIDATE_SHA") or os.environ.get("GITHUB_SHA") or "local-unversioned"
    return sha[:7] if sha != "local-unversioned" else sha
