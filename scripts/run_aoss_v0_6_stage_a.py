#!/usr/bin/env python3
"""Non-collecting CLI for the AOSS Stage-A collector foundation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.aoss_stage_a.preflight import PreflightError, inspect_preflight  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--dgaf-root", required=True, type=Path)
    preflight.add_argument("--acp-root", required=True, type=Path)

    subparsers.add_parser("collect")
    args = parser.parse_args()

    if args.command == "collect":
        print("COLLECTION_IMPLEMENTATION_NOT_ACCEPTED", file=sys.stderr)
        return 2

    try:
        report = inspect_preflight(args.dgaf_root, args.acp_root)
    except PreflightError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
