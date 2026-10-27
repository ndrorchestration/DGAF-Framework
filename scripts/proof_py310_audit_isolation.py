"""Research-only Python 3.10 workload / Python 3.11 auditor separation.

Never use generated outputs as canonical DGAF locks. The current pinned
pip-audit 2.10.1 requires CacheControl[filecache], introducing vulnerable
filelock on Python 3.10. This proof removes ONLY the scanner from the
diagnostic 3.10 requirements and audits every resolved workload package using
a separately hash-locked Python 3.11 scanner; nothing is waived.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
SOURCE = ROOT / "requirements-ci.txt"
WORKLOAD_SOURCE = ROOT / "py310-isolated-workload-requirements.txt"
REPORT = ROOT / "py310-isolated-resolver-report.json"
LOCK = ROOT / "py310-isolated-workload-hash.lock"
MANIFEST = ROOT / "py310-isolated-manifest.json"
AUDIT = ROOT / "py310-isolated-audit.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def make_source() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    original = [
        line.strip() for line in source.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert original.count("pip-audit==2.10.1") == 1, "exact scanner pin required"
    assert "black==26.10.1" in original
    assert "setuptools==84.2.1" in original
    assert "certifi==2026.10.23" in original
    candidate = source.replace("pip-audit==2.10.1\n", "")
    other = [
        line.strip() for line in candidate.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert len(original) == len(other) + 1
    assert other == [x for x in original if x != "pip-audit==2.10.1"]
    WORKLOAD_SOURCE.write_text(
        "# DIAGNOSTIC workload, NOT canonical. Auditor removed for an isolated scanner.\n"
        + candidate, encoding="utf-8"
    )
    print(json.dumps({
        "stage": "SOURCE_PREPARED", "source_sha256": sha(SOURCE),
        "workload_source_sha256": sha(WORKLOAD_SOURCE),
        "original_direct_pins": len(original), "diagnostic_direct_pins": len(other),
        "scanner_removed_only": True, "authority": "NOT_GRANTED"
    }, sort_keys=True))


def emit_lock() -> None:
    assert sys.version_info[:2] == (3, 10), "resolver must run in Python 3.10"
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    rows = {}
    for item in report.get("install", []):
        metadata = item.get("metadata") or {}
        name, version = metadata.get("name"), metadata.get("version")
        digest = (
            (item.get("download_info") or {}).get("archive_info") or {}
        ).get("hashes", {}).get("sha256")
        assert isinstance(name, str) and isinstance(version, str)
        assert isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest)
        key = canonical(name)
        assert key not in rows, "duplicate resolved package"
        rows[key] = (version, digest)
    assert rows and "pip-audit" not in rows and "filelock" not in rows, (
        "scanner-only vulnerable dependency must be absent from diagnostic workload"
    )
    assert "pip" in rows and "setuptools" in rows
    body = [
        "# TEST-ONLY COMPLETE HASH LOCK — NOT DGAF CANONICAL",
        f"# workload_source_sha256: {sha(WORKLOAD_SOURCE)}",
        "# python_minor: 3.10",
        "# runner: ubuntu-24.04/x64",
        "# resolver: pip==26.2.1",
        "",
    ]
    resolved_lines = []
    for name, (version, digest) in sorted(rows.items()):
        body.extend((f"{name}=={version} \\", f"    --hash=sha256:{digest}"))
        resolved_lines.append(f"{name}=={version} sha256:{digest}")
    LOCK.write_text("\n".join(body) + "\n", encoding="utf-8")
    resolved_hash = hashlib.sha256("\n".join(resolved_lines).encode()).hexdigest()
    MANIFEST.write_text(json.dumps({
        "schema": "AKDC_CI_PY310_ISOLATED_AUDITOR_DIAGNOSTIC_V1",
        "scientific_state_effect": "NONE", "authorization_effect": "NONE",
        "source_sha256": sha(SOURCE),
        "workload_source_sha256": sha(WORKLOAD_SOURCE),
        "workload_lock_sha256": sha(LOCK),
        "resolved_set_sha256": resolved_hash,
        "resolved_package_count": len(rows),
        "python_full": platform.python_version(),
        "python_minor": "3.10",
        "scanner_not_in_workload": True,
        "filelock_not_in_workload": True,
        "security_audit_status": "NOT_YET_VERIFIED",
    }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(MANIFEST.read_text())


def lock_members() -> dict[str, str]:
    lines = LOCK.read_text(encoding="utf-8").splitlines()
    rows = {}
    for i, line in enumerate(lines):
        if not line or line.startswith("#"):
            continue
        m = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^ ]+) \\", line)
        if m is None:
            if re.fullmatch(r"    --hash=sha256:[a-f0-9]{64}", line):
                continue
            raise AssertionError("invalid lock record")
        assert i + 1 < len(lines)
        assert re.fullmatch(r"    --hash=sha256:[a-f0-9]{64}", lines[i + 1])
        name = canonical(m.group(1))
        assert name not in rows
        rows[name] = m.group(2)
    return rows


def verify_audit() -> None:
    d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert d["workload_lock_sha256"] == sha(LOCK)
    assert d["workload_source_sha256"] == sha(WORKLOAD_SOURCE)
    assert d["source_sha256"] == sha(SOURCE)
    packages = lock_members()
    assert len(packages) == d["resolved_package_count"]
    assert "pip-audit" not in packages and "filelock" not in packages
    result = json.loads(AUDIT.read_text(encoding="utf-8"))
    observations = result.get("dependencies") if isinstance(result, dict) else result
    assert isinstance(observations, list), "unexpected auditor JSON contract"
    audited = {}
    for entry in observations:
        assert isinstance(entry, dict)
        name, version = entry.get("name"), entry.get("version")
        assert isinstance(name, str) and isinstance(version, str)
        key = canonical(name)
        assert key not in audited
        assert entry.get("vulns") == [], (key, entry.get("vulns"))
        audited[key] = version
    assert audited == packages, (
        "auditor coverage incomplete or package identities differed",
        set(packages) - set(audited), set(audited) - set(packages)
    )
    d["security_audit_status"] = "PASSED_COMPLETE_INDEPENDENT_HASHED_REQUIREMENTS_SCAN"
    d["audited_package_count"] = len(audited)
    d["audit_json_sha256"] = sha(AUDIT)
    MANIFEST.write_text(json.dumps(d, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("ISOLATED_AUDITOR_COVERAGE_COMPLETE_AND_NONWAIVED", len(audited))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("source", "lock", "verify"))
    args = ap.parse_args()
    {"source": make_source, "lock": emit_lock, "verify": verify_audit}[args.command]()


if __name__ == "__main__":
    main()
