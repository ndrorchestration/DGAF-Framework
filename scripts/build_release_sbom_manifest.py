#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tool_version(command: list[str]) -> str:
    return subprocess.check_output(command, text=True).strip()


def load_cyclonedx(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("bomFormat") != "CycloneDX":
        raise ValueError(f"{path} is not a CycloneDX JSON document")
    if not isinstance(data.get("components", []), list):
        raise ValueError(f"{path} components must be a list")
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--python-sbom", type=Path, required=True)
    parser.add_argument("--npm-sbom", type=Path, required=True)
    parser.add_argument("--pip-audit-exit-code", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    python_sbom = load_cyclonedx(args.python_sbom)
    npm_sbom = load_cyclonedx(args.npm_sbom)

    result = {
        "schema_version": 1,
        "claim_scope": "G6_SBOM_PROOF_ONLY",
        "source_sha": args.source_sha,
        "release_admission": False,
        "independent_validation": False,
        "security_scan_pass": args.pip_audit_exit_code == 0,
        "pip_audit_exit_code": args.pip_audit_exit_code,
        "toolchain": {
            "python": platform.python_version(),
            "pip_audit": tool_version(["python", "-m", "pip_audit", "--version"]),
            "node": tool_version(["node", "--version"]),
            "npm": tool_version(["npm", "--version"]),
        },
        "artifacts": [
            {
                "kind": "python-ci-py312-cyclonedx",
                "path": str(args.python_sbom),
                "sha256": sha256(args.python_sbom),
                "bytes": args.python_sbom.stat().st_size,
                "component_count": len(python_sbom.get("components", [])),
            },
            {
                "kind": "npm-lock-cyclonedx",
                "path": str(args.npm_sbom),
                "sha256": sha256(args.npm_sbom),
                "bytes": args.npm_sbom.stat().st_size,
                "component_count": len(npm_sbom.get("components", [])),
            },
        ],
        "limitations": [
            "This artifact proves SBOM generation for one exact source SHA only.",
            "SBOM generation is not a security-scan waiver or release admission.",
            "Independent reproduction and final release-candidate binding remain separate Gate 0 requirements.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
