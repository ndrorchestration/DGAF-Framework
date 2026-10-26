"""Offline Python Requires-Python compatibility evidence for four canonical CI locks.

This is a bounded metadata check, NOT a vulnerability scan, package resolver,
signed-lock attestation, approval, or permission to change required CI lanes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

LOCKS = (
    ("requirements-ci-py310-ubuntu2404-x64.lock", "3.10"),
    ("requirements-ci-py311-ubuntu2404-x64.lock", "3.11"),
    ("requirements-ci-py312-ubuntu2404-x64.lock", "3.12"),
    ("requirements-ci-control-plane-py312-ubuntu2404-x64.lock", "3.12"),
)
PACKAGE_NAME = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")


class LockEvidenceError(ValueError):
    """Missing or ambiguous lock evidence must fail closed."""


def _one_match(pattern: str, source: str, description: str) -> str:
    matches = re.findall(pattern, source, re.MULTILINE)
    if len(matches) != 1:
        raise LockEvidenceError(f"{description}: expected exactly one match; found {len(matches)}")
    return matches[0]


def evaluate_matrix(
    root: Path, package: str, candidate_version: str, requires_python: str, metadata_source: str
) -> dict:
    """Evaluate interpreter compatibility; never assert vulnerability clearance."""
    if not PACKAGE_NAME.fullmatch(package):
        raise LockEvidenceError("package name is invalid")
    if not metadata_source.startswith("https://"):
        raise LockEvidenceError("metadata source must be an HTTPS URL")
    try:
        Version(candidate_version)
        specifier = SpecifierSet(requires_python)
    except (InvalidVersion, InvalidSpecifier) as exc:
        raise LockEvidenceError(f"invalid release metadata: {exc}") from exc

    rows = []
    for filename, expected_minor in LOCKS:
        path = root / filename
        if not path.is_file():
            raise LockEvidenceError(f"canonical CI lock missing: {filename}")
        raw = path.read_bytes()
        source = raw.decode("utf-8")
        minor = _one_match(r"^# python_minor: ([^\s]+)$", source, f"{filename} Python header")
        if minor != expected_minor:
            raise LockEvidenceError(f"{filename}: expected Python {expected_minor}, found {minor}")
        full = re.findall(r"^# python_full: ([^\s]+)$", source, re.MULTILINE)
        if len(full) > 1 or (full and not full[0].startswith(minor + ".")):
            raise LockEvidenceError(f"{filename}: conflicting Python version header")
        interpreter = full[0] if full else minor + ".0"
        pin = _one_match(
            rf"^{re.escape(package)}==([^\s]+)\s*\\",
            source,
            f"{filename} {package} pin",
        )
        try:
            Version(pin)
        except InvalidVersion as exc:
            raise LockEvidenceError(f"{filename}: invalid installed pin") from exc
        rows.append(
            {
                "lock": filename,
                "lock_sha256": hashlib.sha256(raw).hexdigest(),
                "python_minor": minor,
                "python_full_or_minimum": interpreter,
                "installed_pin": pin,
                "candidate_supported": specifier.contains(interpreter),
            }
        )

    blocked = any(not row["candidate_supported"] for row in rows)
    return {
        "classification": "INCOMPATIBLE" if blocked else "METADATA_COMPATIBLE_ONLY",
        "security_clearance": "NOT_ESTABLISHED",
        "approval": "NOT_AUTHORIZED",
        "metadata_authenticated": False,
        "note": "Requires-Python metadata is supplied by the caller and NOT fetched, verified or attested.",
        "package": package,
        "candidate_version": candidate_version,
        "candidate_requires_python": requires_python,
        "claimed_metadata_source": metadata_source,
        "locks": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--package", required=True)
    parser.add_argument("--candidate-version", required=True)
    parser.add_argument("--requires-python", required=True)
    parser.add_argument("--metadata-source", required=True)
    args = parser.parse_args()
    try:
        report = evaluate_matrix(
            args.root, args.package, args.candidate_version, args.requires_python, args.metadata_source
        )
    except (OSError, UnicodeError, LockEvidenceError) as exc:
        print(json.dumps({"classification": "ERROR", "error": str(exc), "security_clearance": "NOT_ESTABLISHED"}))
        return 1
    print(json.dumps(report, sort_keys=True, indent=2))
    return 2 if report["classification"] == "INCOMPATIBLE" else 0


if __name__ == "__main__":
    sys.exit(main())
