#!/usr/bin/env python3
"""Generate a conservative, non-destructive branch disposition ledger.

The classifier intentionally proves only a narrow fact: whether a branch tip is
fully represented by the selected base branch. It never deletes or rewrites a
ref and never interprets unique work as obsolete merely from its age or name.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

API_ROOT = "https://api.github.com"

ACTIVE = "ACTIVE_DO_NOT_PRUNE"
MERGED = "MERGED_SAFE_TO_PRUNE_CANDIDATE"
REVIEW = "REVIEW_REQUIRED"


@dataclass(frozen=True)
class CompareFacts:
    status: str
    ahead_by: int
    behind_by: int
    branch_sha: str


def classify_branch(*, is_open_pr_head: bool, facts: CompareFacts | None, error: str | None = None) -> str:
    """Return a conservative disposition from explicit GitHub evidence only."""
    if is_open_pr_head:
        return ACTIVE
    if error is not None or facts is None:
        return REVIEW
    if facts.ahead_by == 0 and facts.status in {"behind", "identical"}:
        return MERGED
    return REVIEW


class GitHubClient:
    def __init__(self, token: str, repository: str) -> None:
        if "/" not in repository:
            raise ValueError("repository must be OWNER/REPO")
        self.token = token
        self.repository = repository

    def _get(self, path: str) -> Any:
        request = urllib.request.Request(
            f"{API_ROOT}{path}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "dgaf-branch-disposition-inventory",
            },
        )
        # API_ROOT is a fixed HTTPS GitHub origin; callers supply only the API path.
        with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310
            return json.load(response)

    def paginated(self, path: str) -> Iterable[dict[str, Any]]:
        separator = "&" if "?" in path else "?"
        page = 1
        while True:
            items = self._get(f"{path}{separator}per_page=100&page={page}")
            if not isinstance(items, list):
                raise ValueError(f"expected list response for {path}")
            yield from items
            if len(items) < 100:
                return
            page += 1

    def branch(self, name: str) -> dict[str, Any]:
        quoted = urllib.parse.quote(name, safe="")
        return self._get(f"/repos/{self.repository}/branches/{quoted}")

    def compare(self, base: str, head: str) -> dict[str, Any]:
        base_q = urllib.parse.quote(base, safe="")
        head_q = urllib.parse.quote(head, safe="")
        return self._get(f"/repos/{self.repository}/compare/{base_q}...{head_q}")


def build_ledger(client: GitHubClient, base: str) -> dict[str, Any]:
    branches = list(client.paginated(f"/repos/{client.repository}/branches"))
    open_prs = list(client.paginated(f"/repos/{client.repository}/pulls?state=open"))
    open_heads = {
        pr.get("head", {}).get("ref")
        for pr in open_prs
        if pr.get("head", {}).get("repo", {}).get("full_name") == client.repository
    }

    base_record = next((branch for branch in branches if branch.get("name") == base), None)
    if base_record is None:
        base_record = client.branch(base)
    base_sha = base_record["commit"]["sha"]

    records: list[dict[str, Any]] = []
    counts = {ACTIVE: 0, MERGED: 0, REVIEW: 0}

    for branch in sorted(branches, key=lambda item: item["name"]):
        name = branch["name"]
        if name == base:
            continue
        branch_sha = branch["commit"]["sha"]
        is_active = name in open_heads
        facts: CompareFacts | None = None
        error: str | None = None
        if not is_active:
            try:
                comparison = client.compare(base, name)
                facts = CompareFacts(
                    status=str(comparison.get("status", "unknown")),
                    ahead_by=int(comparison.get("ahead_by", -1)),
                    behind_by=int(comparison.get("behind_by", -1)),
                    branch_sha=branch_sha,
                )
            except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError) as exc:
                error = f"{type(exc).__name__}: {exc}"

        disposition = classify_branch(is_open_pr_head=is_active, facts=facts, error=error)
        counts[disposition] += 1
        record: dict[str, Any] = {
            "branch": name,
            "branch_sha": branch_sha,
            "disposition": disposition,
            "open_pr_head": is_active,
        }
        if facts is not None:
            record["compare"] = {
                "status": facts.status,
                "ahead_by": facts.ahead_by,
                "behind_by": facts.behind_by,
            }
        if error is not None:
            record["error"] = error
        records.append(record)

    return {
        "schema": "DGAF_BRANCH_DISPOSITION_LEDGER_V1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": client.repository,
        "base_branch": base,
        "base_sha": base_sha,
        "branch_count_including_base": len(branches),
        "non_base_branch_count": len(records),
        "open_pull_request_count": len(open_prs),
        "counts": counts,
        "policy": {
            "auto_delete": False,
            "merged_candidate_meaning": "ahead_by=0 and compare status is behind/identical; deletion still requires separate review/action",
            "review_required_meaning": "unique/diverged/ambiguous/error state; no prune inference permitted",
        },
        "branches": records,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--base", default="main")
    parser.add_argument("--output", type=Path, default=Path("branch-disposition-ledger.json"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is required", file=sys.stderr)
        return 2
    if not args.repository:
        print("--repository or GITHUB_REPOSITORY is required", file=sys.stderr)
        return 2

    client = GitHubClient(token, args.repository)
    ledger = build_ledger(client, args.base)
    args.output.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(ledger["counts"], sort_keys=True))
    print(f"wrote {args.output} for {ledger['non_base_branch_count']} non-base refs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
