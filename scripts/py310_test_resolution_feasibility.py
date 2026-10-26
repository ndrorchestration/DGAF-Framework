"""Non-admitting Python 3.10 test-only dependency resolution experiment.

Counterfactual direct pins, pip --dry-run evidence; never a lock or security waiver.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

PIN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([^\s#]+)$")
NORMALIZE = re.compile(r"[-_.]+")
CHANGES = {"pip-audit": None, "black": "26.10.1", "setuptools": "84.1.0"}


def canonical(name: str) -> str:
    return NORMALIZE.sub("-", name).lower()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prepare(source: Path, directory: Path) -> dict[str, Any]:
    """Write temporary counterfactual requirements, preserving all other pins."""
    raw = source.read_bytes()
    found: dict[str, str] = {}
    output = [
        "# RESEARCH ONLY: temporary Python 3.10 test-source candidate",
        "# NOT A SIGNED LOCK, NOT ADMITTED, NO SECURITY CLEARANCE",
    ]
    for line in raw.decode("utf-8").splitlines():
        clean = line.strip()
        if not clean or clean.startswith("#"):
            continue
        match = PIN.fullmatch(clean)
        if match is None:
            raise ValueError(f"unrecognized direct requirement: {clean[:80]}")
        name, version = match.groups()
        key = canonical(name)
        if key in found:
            raise ValueError(f"duplicate direct requirement: {key}")
        found[key] = version
        if key not in CHANGES:
            output.append(f"{name}=={version}")
        elif CHANGES[key] is not None:
            output.append(f"{name}=={CHANGES[key]}")
    if not all(key in found for key in CHANGES):
        raise ValueError("required baseline pins missing")
    if found["pip-audit"] != "2.10.1" or found["black"] != "26.5.1" or found["setuptools"] != "83.0.0":
        raise ValueError("baseline pins drifted; refuse silent source migration")
    directory.mkdir(parents=True, exist_ok=True)
    candidate = ("\n".join(output) + "\n").encode("utf-8")
    (directory / "py310-test-only-research.in").write_bytes(candidate)
    plan: dict[str, Any] = {
        "status": "COUNTERFACTUAL_NOT_ADMITTED",
        "security_clearance": "NOT_ESTABLISHED",
        "authorization": "NOT_AUTHORIZED",
        "python_target": "3.10",
        "baseline_source_sha256": digest(raw),
        "candidate_source_sha256": digest(candidate),
        "changed_direct_requirements": {
            "pip-audit": {"from": found["pip-audit"], "to": "EXCLUDED_FROM_TEST_ONLY_SOURCE"},
            "black": {"from": found["black"], "to": CHANGES["black"]},
            "setuptools": {"from": found["setuptools"], "to": CHANGES["setuptools"]},
        },
        "direct_requirements_count": len(found) - 1,
    }
    (directory / "plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
    return plan


def evaluate(directory: Path, report_path: Path) -> dict[str, Any]:
    """Check a real Python 3.10 pip dry-run report without asserting clearance."""
    plan = json.loads((directory / "plan.json").read_text())
    candidate = (directory / "py310-test-only-research.in").read_bytes()
    if digest(candidate) != plan["candidate_source_sha256"]:
        raise ValueError("candidate source changed after preparation")
    direct: dict[str, str] = {}
    for line in candidate.decode("utf-8").splitlines():
        match = PIN.fullmatch(line.strip())
        if match:
            key = canonical(match.group(1))
            if key in direct:
                raise ValueError("duplicate candidate direct pin")
            direct[key] = match.group(2)
    raw = report_path.read_bytes()
    report = json.loads(raw)
    if not isinstance(report, dict) or report.get("version") != "1":
        raise ValueError("unrecognized pip resolver report schema")
    env = report.get("environment")
    if not isinstance(env, dict) or env.get("python_version") != "3.10":
        raise ValueError("resolver report not bound to Python 3.10")
    rows = report.get("install")
    if not isinstance(rows, list) or not rows:
        raise ValueError("missing resolved packages")
    resolved: dict[str, str] = {}
    for item in rows:
        meta = item.get("metadata") if isinstance(item, dict) else None
        if not isinstance(meta, dict):
            raise ValueError("missing package metadata")
        name, version = meta.get("name"), meta.get("version")
        if not isinstance(name, str) or not isinstance(version, str):
            raise ValueError("incomplete package identity")
        key = canonical(name)
        if key in resolved:
            raise ValueError("duplicate resolved package identity")
        resolved[key] = version
    for name, pin in direct.items():
        if resolved.get(name) != pin:
            raise ValueError(f"missing or changed directly pinned package: {name}")
    forbidden = {"pip-audit", "cachecontrol", "filelock"}
    remaining = sorted(forbidden.intersection(resolved))
    status = "SCANNER_CHAIN_STILL_PRESENT" if remaining else "GRAPH_SPLIT_FEASIBLE_NOT_SECURITY_CLEARED"
    summary: dict[str, Any] = {
        "status": status,
        "security_clearance": "NOT_ESTABLISHED",
        "authorization": "NOT_AUTHORIZED",
        "python_target": env["python_version"],
        "baseline_source_sha256": plan["baseline_source_sha256"],
        "candidate_source_sha256": plan["candidate_source_sha256"],
        "pip_report_sha256": digest(raw),
        "resolved_package_count": len(resolved),
        "scanner_chain_packages_still_present": remaining,
        "resolved_versions": dict(sorted(resolved.items())),
        "limitations": "dry-run is not hash-bound installation, vulnerability audit, or accepted release lock",
    }
    (directory / "evaluation.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["prepare", "evaluate"])
    parser.add_argument("--source", type=Path, default=Path("requirements-ci.txt"))
    parser.add_argument("--output-dir", type=Path, default=Path("test-artifacts/py310-resolution"))
    parser.add_argument("--pip-report", type=Path, default=Path("test-artifacts/py310-resolution/pip-report.json"))
    args = parser.parse_args()
    try:
        result = (
            prepare(args.source, args.output_dir)
            if args.phase == "prepare"
            else evaluate(args.output_dir, args.pip_report)
        )
    except (OSError, ValueError, KeyError, TypeError, UnicodeError) as exc:
        print(json.dumps({"status": "RESEARCH_ERROR", "type": type(exc).__name__, "error": str(exc)[:200]}))
        return 1
    print(json.dumps({"status": result["status"], "security_clearance": "NOT_ESTABLISHED"}))
    return 2 if result["status"] == "SCANNER_CHAIN_STILL_PRESENT" else 0


if __name__ == "__main__":
    raise SystemExit(main())
