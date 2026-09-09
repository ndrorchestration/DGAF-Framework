#!/usr/bin/env python3
"""Fail closed on GitHub issue-closing keyword syntax in pull-request bodies.

DGAF uses explicit issue-state adjudication for governance gates. GitHub's parser can
interpret a state-transition keyword followed by an issue reference semantically,
even when ordinary prose intends negation. This checker prevents that syntax from
appearing in PR bodies targeting the governed base branch.

This is a pre-merge/detective control unless repository settings make its workflow a
required check. It does not establish preventive branch protection by itself.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Iterable


_REFERENCE = r"(?:#[0-9]+|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[0-9]+|https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/issues/[0-9]+)"
_CLOSING_KEYWORD = r"(?:close(?:s|d)?|fix(?:es|ed)?|resolve(?:s|d)?)"
_DANGEROUS = re.compile(
    rf"\b(?P<keyword>{_CLOSING_KEYWORD})\b[\s:,-]*(?:\[\s*)?(?P<reference>{_REFERENCE})",
    re.IGNORECASE,
)


class GuardInputError(ValueError):
    """Raised when the checker cannot establish the requested PR-body input."""


def find_dangerous_closure_syntax(body: str) -> list[dict[str, object]]:
    """Return every closing-keyword + issue-reference match with line provenance."""
    findings: list[dict[str, object]] = []
    for match in _DANGEROUS.finditer(body):
        line = body.count("\n", 0, match.start()) + 1
        findings.append(
            {
                "line": line,
                "match": match.group(0),
                "keyword": match.group("keyword"),
                "reference": match.group("reference"),
            }
        )
    return findings


def _load_event(path: Path, required_base: str | None) -> tuple[str, str | None]:
    try:
        event = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GuardInputError(f"cannot read valid GitHub event JSON: {exc}") from exc

    pr = event.get("pull_request")
    if not isinstance(pr, dict):
        raise GuardInputError("event does not contain a pull_request object")

    base = pr.get("base")
    base_ref = base.get("ref") if isinstance(base, dict) else None
    if required_base is not None and base_ref != required_base:
        return "", base_ref if isinstance(base_ref, str) else None

    body = pr.get("body")
    if body is None:
        body = ""
    if not isinstance(body, str):
        raise GuardInputError("pull_request.body must be a string or null")
    return body, base_ref if isinstance(base_ref, str) else None


def _emit_findings(findings: Iterable[dict[str, object]]) -> None:
    print("FAIL: PR body contains GitHub issue-closing keyword syntax.")
    for item in findings:
        print(
            f"- line {item['line']}: {item['match']!r} "
            f"(keyword={item['keyword']!r}, reference={item['reference']!r})"
        )
    print("Use neutral references such as 'Related: #123' or 'Issue #123 remains OPEN'.")
    print("Issue-state transitions must be adjudicated explicitly outside PR-body prose.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--event-path", type=Path, help="GitHub event JSON containing pull_request.body")
    source.add_argument("--body-file", type=Path, help="UTF-8 file containing only the PR body")
    source.add_argument("--body", help="PR body supplied directly")
    parser.add_argument(
        "--required-base",
        help="When --event-path is used, scan only when pull_request.base.ref equals this value",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.event_path is not None:
            body, base_ref = _load_event(args.event_path, args.required_base)
            if args.required_base is not None and base_ref != args.required_base:
                print(
                    f"SKIP: PR base is {base_ref!r}; guard is scoped to {args.required_base!r}."
                )
                return 0
        elif args.body_file is not None:
            body = args.body_file.read_text(encoding="utf-8")
        else:
            body = args.body or ""
    except (GuardInputError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3

    findings = find_dangerous_closure_syntax(body)
    if findings:
        _emit_findings(findings)
        return 2

    print("PASS: no GitHub issue-closing keyword syntax found in PR body.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
