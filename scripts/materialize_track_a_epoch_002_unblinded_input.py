#!/usr/bin/env python3
"""Controlled Stage-1 materializer for Track A Epoch 002."""

from __future__ import annotations

import argparse
import tarfile
from pathlib import Path, PurePosixPath

PRIMARY_ANALYSIS_MARKER = "PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN"


def fail(message: str) -> None:
    raise SystemExit(message)


def read_exact_tar_members(path: Path, expected: frozenset[str], label: str) -> dict[str, bytes]:
    try:
        with tarfile.open(path, "r:") as archive:
            members = archive.getmembers()
            names = [member.name for member in members]
            if len(names) != len(set(names)):
                fail(f"{label}: duplicate tar member")
            if frozenset(names) != expected:
                fail(f"{label}: tar member set mismatch")

            payloads: dict[str, bytes] = {}
            for member in members:
                pure_name = PurePosixPath(member.name)
                if pure_name.is_absolute() or ".." in pure_name.parts or len(pure_name.parts) != 1:
                    fail(f"{label}: unsafe tar member name")
                if not member.isfile():
                    fail(f"{label}: non-regular tar member")
                handle = archive.extractfile(member)
                if handle is None:
                    fail(f"{label}: tar member could not be read")
                payloads[member.name] = handle.read()
            return payloads
    except (OSError, tarfile.TarError) as exc:
        fail(f"{label}: unreadable tar archive: {exc}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-archive", required=True)
    parser.add_argument("--protected-archive", required=True)
    parser.add_argument("--custody-private-key", required=True)
    parser.add_argument("--output-dir", required=True)
    return parser


if __name__ == "__main__":
    build_parser().parse_args()
    print(PRIMARY_ANALYSIS_MARKER)
