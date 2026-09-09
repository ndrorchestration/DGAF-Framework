#!/usr/bin/env python3
"""Detect direct writes to DGAF's default branch after they occur.

This is a compensating detective control for Issue #277 while repository-admin
required-PR enforcement is unavailable through the current automation surface. It
queries GitHub's commit-to-pull-request association endpoint and requires the pushed
``main`` head to be the exact merge commit of one closed, merged PR targeting main.

This script does NOT prevent a direct push and is not tamper-proof against a push that
also disables the workflow. It must never be represented as branch protection or as a
substitute for repository-admin required-PR / required-check enforcement.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from typing import Any, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
API_VERSION = "2022-11-28"
DEFAULT_BASE_REF = "main"


class ProvenanceAuditError(RuntimeError):
    """Raised when a main-branch push cannot be attributed to one merged PR."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ProvenanceAuditError(message)


def _validated_sha(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and _SHA_RE.fullmatch(value) is not None,
        f"{label} must be a full lowercase 40-character commit SHA",
    )
    return value


def classify_associated_pulls(
    head_sha: str,
    pulls: Sequence[Mapping[str, Any]],
    *,
    base_ref: str = DEFAULT_BASE_REF,
) -> dict[str, Any]:
    """Require one exact merged-PR association for the pushed head commit."""
    sha = _validated_sha(head_sha, "head_sha")
    _require(isinstance(base_ref, str) and bool(base_ref), "base_ref must be non-empty")
    _require(
        isinstance(pulls, Sequence) and not isinstance(pulls, (str, bytes)),
        "associated pulls must be a sequence",
    )

    exact: list[dict[str, Any]] = []
    for pull in pulls:
        _require(isinstance(pull, Mapping), "associated pull entry must be an object")
        if pull.get("state") != "closed" or not pull.get("merged_at"):
            continue
        base = pull.get("base")
        if not isinstance(base, Mapping) or base.get("ref") != base_ref:
            continue
        if pull.get("merge_commit_sha") != sha:
            continue
        number = pull.get("number")
        _require(
            isinstance(number, int) and not isinstance(number, bool) and number > 0,
            "matching pull request number must be a positive integer",
        )
        exact.append(
            {
                "number": number,
                "html_url": pull.get("html_url"),
                "merged_at": pull.get("merged_at"),
            }
        )

    _require(
        len(exact) == 1,
        "pushed main head is not the exact merge commit of exactly one closed merged PR targeting main",
    )
    matched = exact[0]
    return {
        "main_push_provenance_audit": "PASS_MERGED_PR_ASSOCIATION",
        "head_sha": sha,
        "base_ref": base_ref,
        "pull_request_number": matched["number"],
        "pull_request_url": matched["html_url"],
        "merged_at": matched["merged_at"],
        "preventive_enforcement_established": False,
        "detective_control_only": True,
    }


def fetch_associated_pulls(
    repository: str,
    head_sha: str,
    token: str,
    *,
    attempts: int = 4,
    retry_delay_seconds: float = 2.0,
) -> list[Mapping[str, Any]]:
    """Read GitHub's authenticated commit-to-PR association with bounded retries."""
    _require(
        isinstance(repository, str) and _REPOSITORY_RE.fullmatch(repository) is not None,
        "repository must be owner/name",
    )
    sha = _validated_sha(head_sha, "head_sha")
    _require(isinstance(token, str) and bool(token), "GitHub token is required")
    _require(
        isinstance(attempts, int) and not isinstance(attempts, bool) and attempts > 0,
        "attempts must be a positive integer",
    )
    _require(retry_delay_seconds >= 0, "retry_delay_seconds must be non-negative")

    url = f"https://api.github.com/repos/{repository}/commits/{sha}/pulls"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "dgaf-main-push-provenance-audit/1",
    }

    last_error: str | None = None
    for attempt in range(1, attempts + 1):
        request = Request(url, headers=headers, method="GET")
        try:
            with urlopen(request, timeout=20) as response:  # nosec B310: fixed api.github.com URL
                payload = json.loads(response.read().decode("utf-8"))
            _require(isinstance(payload, list), "GitHub associated-pulls response must be a list")
            if payload or attempt == attempts:
                return payload
            last_error = "no associated pull requests returned"
        except HTTPError as exc:
            last_error = f"GitHub API HTTP {exc.code}"
        except (URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            last_error = f"GitHub API read failed: {type(exc).__name__}"

        if attempt < attempts:
            time.sleep(retry_delay_seconds)

    raise ProvenanceAuditError(last_error or "GitHub associated-pulls read failed")


def _live_inputs() -> tuple[str, str, str]:
    _require(os.environ.get("GITHUB_EVENT_NAME") == "push", "live audit requires a push event")
    _require(os.environ.get("GITHUB_REF") == "refs/heads/main", "live audit requires refs/heads/main")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    head_sha = os.environ.get("GITHUB_SHA", "")
    token = os.environ.get("GH_TOKEN", "")
    return repository, head_sha, token


def main() -> int:
    try:
        repository, head_sha, token = _live_inputs()
        pulls = fetch_associated_pulls(repository, head_sha, token)
        result = classify_associated_pulls(head_sha, pulls)
    except ProvenanceAuditError as exc:
        print(f"FAIL_MAIN_PUSH_PROVENANCE: {exc}", file=sys.stderr)
        print(
            "This is detective evidence only; configure repository-admin required-PR and required-check enforcement to prevent direct writes.",
            file=sys.stderr,
        )
        return 1

    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
