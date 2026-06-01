#!/usr/bin/env python3
"""
vercel_inventory_helper.py
DGAF-Framework · scripts/ · S068 · 2026-05-31

Usage:
    vercel ls --json > vercel_deployments.json
    python scripts/vercel_inventory_helper.py vercel_deployments.json

Outputs a ready-to-paste JSON fragment for ECOSYSTEM_INVENTORY.md.
Paste the output back to Amethyst to close Q-S068-VERCEL-DETAIL.
"""

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def load_deployments(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "deployments" in data:
        return data["deployments"]
    raise ValueError("Unexpected Vercel JSON format: no 'deployments' array found")


def pick_latest(
    deployments: List[Dict[str, Any]], env: Optional[str]
) -> Optional[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    for d in deployments:
        meta = d.get("meta", {}) or {}
        env_tag = (
            meta.get("deploymentType") or meta.get("env") or d.get("target")
        )
        if env is None or (env_tag and str(env_tag).lower() == env.lower()):
            candidates.append(d)
    if not candidates:
        return None

    def parse_created(dep: Dict[str, Any]) -> datetime:
        created = (
            dep.get("createdAt") or dep.get("created") or dep.get("created_at")
        )
        if not created:
            return datetime.fromtimestamp(0, tz=timezone.utc)
        try:
            if isinstance(created, (int, float)):
                return datetime.fromtimestamp(created / 1000, tz=timezone.utc)
            return datetime.fromisoformat(str(created).replace("Z", "+00:00"))
        except Exception:
            return datetime.fromtimestamp(0, tz=timezone.utc)

    candidates.sort(key=parse_created, reverse=True)
    return candidates[0]


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: vercel_inventory_helper.py vercel_deployments.json",
            file=sys.stderr,
        )
        sys.exit(1)

    deployments = load_deployments(sys.argv[1])

    latest_preview = pick_latest(deployments, "preview")
    latest_production = pick_latest(deployments, "production")

    now_iso = datetime.now(timezone.utc).isoformat()

    preview_url = (
        f"https://{latest_preview['url']}"
        if latest_preview and latest_preview.get("url")
        else None
    )
    production_url = (
        f"https://{latest_production['url']}"
        if latest_production and latest_production.get("url")
        else None
    )

    status = (
        "blocked_human_required"
        if preview_url is None and production_url is None
        else "verified"
    )

    print("{")
    print(f'  "vercel.preview_url": {json.dumps(preview_url)},')
    print(f'  "vercel.production_url": {json.dumps(production_url)},')
    print('  "vercel.last_sync_session": "S068",')
    print('  "vercel.last_verified_by": "Ender",')
    print(f'  "vercel.last_verified_at": {json.dumps(now_iso)},')
    print(f'  "vercel.status": {json.dumps(status)}')
    print("}")


if __name__ == "__main__":
    main()
