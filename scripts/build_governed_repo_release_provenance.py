#!/usr/bin/env python3
"""Generate and validate a bounded Governed Repo release-provenance manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

SHA40 = re.compile(r"^[0-9a-f]{40}$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exactly_one(paths: list[Path], label: str) -> Path:
    if len(paths) != 1:
        raise ValueError(f"expected exactly one {label}, found {len(paths)}")
    return paths[0]


def require_sha(value: str, label: str) -> str:
    if not SHA40.fullmatch(value):
        raise ValueError(f"{label} must be a lowercase 40-hex SHA")
    return value


def package_version(pyproject: Path) -> str:
    with pyproject.open("rb") as handle:
        data = tomllib.load(handle)
    value = data["project"]["version"]
    if not isinstance(value, str) or not value.strip():
        raise ValueError("package version missing")
    return value


def build_manifest(args: argparse.Namespace) -> dict:
    dist = Path(args.dist_dir)
    wheel = exactly_one(sorted(dist.glob("*.whl")), "wheel")
    sdist = exactly_one(sorted(dist.glob("*.tar.gz")), "sdist")
    source_sha = require_sha(args.source_sha, "source_sha")
    action_sha = require_sha(args.action_sha, "action_sha")

    manifest = {
        "schema_version": "governed_repo_release_provenance.v1",
        "repository": args.repository,
        "source": {
            "commit_sha": source_sha,
            "canonical_source_path": "packages/governed-repo/src/governed_repo/core.py",
        },
        "package": {
            "distribution": "ndrorchestration-governed-repo",
            "version": package_version(Path(args.pyproject)),
            "wheel": {"filename": wheel.name, "sha256": sha256(wheel)},
            "sdist": {"filename": sdist.name, "sha256": sha256(sdist)},
        },
        "action": {
            "path": "actions/governed-repo/action.yml",
            "source_sha": action_sha,
        },
        "verification": {
            "python_versions": ["3.10", "3.11", "3.12", "3.13", "3.14"],
            "package_matrix_required": True,
        },
        "workflow": {
            "name": "Governed Repo Release Provenance",
            "run_id": args.workflow_run_id,
            "run_attempt": args.workflow_run_attempt,
        },
        "non_effects": {
            "merge_executed": False,
            "mutation_executed": False,
            "authorization_effect": "NONE",
        },
        "claim_ceiling": [
            "publication_readiness_not_established",
            "independent_validation_not_established",
            "production_security_not_established",
            "merge_authority_not_granted",
            "compliance_or_certification_not_established",
            "high_assurance_not_authorized",
            "product_market_fit_not_established",
        ],
    }
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict) -> None:
    required_top = {
        "schema_version",
        "repository",
        "source",
        "package",
        "action",
        "verification",
        "workflow",
        "non_effects",
        "claim_ceiling",
    }
    if set(manifest) != required_top:
        raise ValueError("manifest top-level fields do not match v1 contract")
    if manifest["schema_version"] != "governed_repo_release_provenance.v1":
        raise ValueError("unexpected schema version")
    require_sha(manifest["source"]["commit_sha"], "source.commit_sha")
    require_sha(manifest["action"]["source_sha"], "action.source_sha")
    if manifest["source"]["canonical_source_path"] != "packages/governed-repo/src/governed_repo/core.py":
        raise ValueError("unexpected canonical source path")
    if manifest["action"]["path"] != "actions/governed-repo/action.yml":
        raise ValueError("unexpected Action path")
    if manifest["package"]["distribution"] != "ndrorchestration-governed-repo":
        raise ValueError("unexpected distribution")
    for key in ("wheel", "sdist"):
        artifact = manifest["package"][key]
        if not artifact["filename"]:
            raise ValueError(f"{key} filename missing")
        if not re.fullmatch(r"[0-9a-f]{64}", artifact["sha256"]):
            raise ValueError(f"{key} sha256 invalid")
    if manifest["verification"]["python_versions"] != ["3.10", "3.11", "3.12", "3.13", "3.14"]:
        raise ValueError("unexpected Python verification matrix")
    if manifest["verification"]["package_matrix_required"] is not True:
        raise ValueError("package matrix must be required")
    if not manifest["workflow"]["run_id"] or not manifest["workflow"]["run_attempt"]:
        raise ValueError("workflow identity incomplete")
    if manifest["non_effects"] != {
        "merge_executed": False,
        "mutation_executed": False,
        "authorization_effect": "NONE",
    }:
        raise ValueError("non-effect invariants violated")
    if not manifest["claim_ceiling"]:
        raise ValueError("claim ceiling missing")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist-dir", required=True)
    parser.add_argument("--pyproject", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--action-sha", required=True)
    parser.add_argument("--workflow-run-id", required=True)
    parser.add_argument("--workflow-run-attempt", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = build_manifest(args)
    except (KeyError, OSError, ValueError) as exc:
        print(f"release provenance generation failed: {exc}", file=sys.stderr)
        return 2

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
