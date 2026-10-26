"""Rehearse security audits of four immutable DGAF CI locks from a supported auditor.

A non-admitting evidence collector: status 0 is NOT release/security authorization.
An audit failure, missing lock, unexpected exit, or malformed output fails closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LOCKS = (
    ("requirements-ci-py310-ubuntu2404-x64.lock", "3.10"),
    ("requirements-ci-py311-ubuntu2404-x64.lock", "3.11"),
    ("requirements-ci-py312-ubuntu2404-x64.lock", "3.12"),
    ("requirements-ci-control-plane-py312-ubuntu2404-x64.lock", "3.12"),
)
VERSION_LINE = re.compile(r"^# python_minor: (\d+\.\d+)$", re.MULTILINE)
PACKAGE_LINE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([^\s]+)\s*\\", re.MULTILINE)


def inspect_locks(root: Path) -> list[dict]:
    """Validate inventory before network auditing, retaining raw source fingerprints."""
    rows = []
    for name, expected_minor in LOCKS:
        path = root / name
        if not path.is_file():
            raise ValueError(f"missing canonical lock: {name}")
        raw = path.read_bytes()
        source = raw.decode("utf-8")
        minors = VERSION_LINE.findall(source)
        if minors != [expected_minor]:
            raise ValueError(f"invalid interpreter binding in {name}")
        packages = PACKAGE_LINE.findall(source)
        names = [p.lower().replace("_", "-").replace(".", "-") for p, _ in packages]
        if not names or len(names) != len(set(names)):
            raise ValueError(f"missing or duplicate package pins in {name}")
        for package, version in packages:
            escaped = re.escape(f"{package}=={version}")
            hash_line = rf"^{escaped}[ \t]*\\\r?\n[ \t]+--hash=sha256:[0-9a-f]{{64}}(?:\r?\n|$)"
            if re.search(hash_line, source, re.MULTILINE) is None:
                raise ValueError(f"missing exact hash for {package} in {name}")
        rows.append(
            {
                "filename": name,
                "python_minor": expected_minor,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "package_count": len(packages),
                # Internal check only: never report clean if a scanner silently omits a pin.
                "_expected_pins": {
                    name.lower().replace("_", "-").replace(".", "-"): version for name, version in packages
                },
            }
        )
    return rows


def interpret_result(exit_code: int, output: str, expected_pins: dict | None = None) -> dict:
    """Fail on partial/substituted/duplicated reports as well as actual advisories."""
    try:
        payload = json.loads(output)
    except (json.JSONDecodeError, ValueError):
        return {"status": "AUDIT_ERROR", "exit_code": exit_code, "vulnerability_count": None}
    deps = payload.get("dependencies") if isinstance(payload, dict) else None
    if not isinstance(deps, list) or not deps or any(not isinstance(dep, dict) for dep in deps):
        return {"status": "AUDIT_ERROR", "exit_code": exit_code, "vulnerability_count": None}
    observed = {}
    for dep in deps:
        name, version = dep.get("name"), dep.get("version")
        if not isinstance(name, str) or not name.strip() or not isinstance(version, str) or not version.strip():
            return {"status": "AUDIT_ERROR", "exit_code": exit_code, "vulnerability_count": None}
        normalized = name.lower().replace("_", "-").replace(".", "-")
        if normalized in observed:
            return {"status": "AUDIT_ERROR", "exit_code": exit_code, "vulnerability_count": None}
        observed[normalized] = version
    if expected_pins is not None and observed != expected_pins:
        return {
            "status": "AUDIT_ERROR",
            "exit_code": exit_code,
            "vulnerability_count": None,
            "coverage": "MISSING_SUBSTITUTED_OR_EXTRA_PACKAGE",
            "expected_package_count": len(expected_pins),
            "observed_package_count": len(observed),
        }
    count = 0
    findings_by_package = []
    for dep in deps:
        findings = dep.get("vulns")
        if not isinstance(findings, list) or any(
            not isinstance(vuln, dict) or not isinstance(vuln.get("id"), str) for vuln in findings
        ):
            return {"status": "AUDIT_ERROR", "exit_code": exit_code, "vulnerability_count": None}
        if findings:
            findings_by_package.append(
                {
                    "package": str(dep.get("name", "UNKNOWN"))[:100],
                    "version": str(dep.get("version", "UNKNOWN"))[:50],
                    "advisory_ids": [str(vuln.get("id", "UNKNOWN"))[:100] for vuln in findings],
                }
            )
        count += len(findings)
    if exit_code == 0 and count == 0:
        status = "NO_REPORTED_VULNERABILITIES"
    elif exit_code == 1 and count > 0:
        status = "VULNERABILITIES_FOUND"
    else:
        status = "AUDIT_ERROR"
    return {
        "status": status,
        "exit_code": exit_code,
        "vulnerability_count": count,
        "dependency_count": len(deps),
        "findings": findings_by_package,
    }


def audit_command(lock: Path | None) -> list[str]:
    """Use an installed scanner; no pip resolution or version rewriting on target locks."""
    command = [sys.executable, "-m", "pip_audit"]
    if lock is None:
        return command + ["--local", "--format=json", "--progress-spinner=off"]
    return command + [
        "--require-hashes",
        "--disable-pip",
        "-r",
        str(lock),
        "--format=json",
        "--progress-spinner=off",
    ]


def rehearse(root: Path, output: Path, *, runner=subprocess.run) -> dict:
    """Always save a report for admissibility review; no advisory waivers."""
    report = {
        "evidence_class": "SAME_SYSTEM_SECURITY_REHEARSAL",
        "admission": "NOT_AUTHORIZED",
        "security_clearance": "NOT_ESTABLISHED",
        "scientific_n_increment": 0,
        # A pull_request GITHUB_SHA is a synthetic test merge, not the PR head.
        "github_event_sha": os.environ.get("GITHUB_SHA", "UNSET"),
        "pr_head_sha": os.environ.get("PR_HEAD_SHA", "UNSET"),
        "pr_base_sha": os.environ.get("PR_BASE_SHA", "UNSET"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID", "UNSET"),
        "scanner_environment": "PYTHON_3_11_EXPECTED_NOT_ATTESTED",
        "locks": [],
    }
    try:
        inventory = inspect_locks(root)
        targets = [(None, None)] + [(item, root / str(item["filename"])) for item in inventory]
        for item, path in targets:
            command = audit_command(path)
            try:
                process = runner(command, text=True, capture_output=True, timeout=180)
                result = interpret_result(
                    process.returncode,
                    process.stdout,
                    None if item is None else item["_expected_pins"],
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                result = {
                    "status": "AUDIT_ERROR",
                    "exit_code": None,
                    "vulnerability_count": None,
                    "error_type": type(exc).__name__,
                }
            record = {"target": "auditor_environment" if item is None else "canonical_lock"}
            if item is not None:
                # Keep the expected package mapping internal; expose only verified count.
                record.update({key: value for key, value in item.items() if key != "_expected_pins"})
            record["command_flags"] = command[3:]
            record.update(result)
            report["locks"].append(record)
        statuses = [record["status"] for record in report["locks"]]
        if any(status == "AUDIT_ERROR" for status in statuses):
            report["result"] = "AUDIT_ERROR"
        elif any(status == "VULNERABILITIES_FOUND" for status in statuses):
            report["result"] = "BLOCKED_VULNERABILITIES"
        else:
            report["result"] = "NO_REPORTED_VULNERABILITIES_ONLY"
    except (OSError, UnicodeError, ValueError) as exc:
        report["result"] = "AUDIT_ERROR"
        report["error_type"] = type(exc).__name__
        report["error"] = str(exc)[:200]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path("test-artifacts/gate0-lock-audit-rehearsal.json"))
    options = parser.parse_args()
    report = rehearse(options.root, options.output)
    print(json.dumps({"result": report["result"], "output": str(options.output)}))
    return 0 if report["result"] == "NO_REPORTED_VULNERABILITIES_ONLY" else 1


if __name__ == "__main__":
    sys.exit(main())
