from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "packages" / "governed-repo" / "pyproject.toml"

SCHEMA_VERSION = "governed_repo.release_provenance.v1"
EVIDENCE_CLASS = "INTERNAL_RELEASE_CANDIDATE_PROVENANCE"
CONTROLLER_ISSUE = "issue://1214"
REPOSITORY = "ndrorchestration/DGAF-Framework"
CANONICAL_SOURCE = "packages/governed-repo/src/governed_repo/core.py"
ACTION_PATH = "actions/governed-repo"
WORKFLOW_NAME = "Governed Repo P0 Package"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
PROJECT_VERSION = re.compile(r'^version\s*=\s*"([^"]+)"\s*(?:#.*)?$')

CLAIM_CEILING = {
    "publication_readiness": "NOT_ESTABLISHED",
    "independent_validation": "NOT_ESTABLISHED",
    "production_security": "NOT_ESTABLISHED",
    "compliance_certification": "NOT_ESTABLISHED",
    "high_assurance": "NOT_AUTHORIZED",
    "product_market_fit": "NOT_ESTABLISHED",
}
NON_EFFECTS = {
    "merge_executed": False,
    "mutation_executed": False,
    "authorization_effect": "NONE",
    "publication_effect": "NONE",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_version(pyproject: Path = PYPROJECT) -> str:
    """Read the one string project.version using only Python 3.10 stdlib."""
    in_project = False
    versions: list[str] = []

    for raw_line in pyproject.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("[") and line.endswith("]"):
            in_project = line == "[project]"
            continue
        if not in_project or not line or line.startswith("#"):
            continue
        match = PROJECT_VERSION.fullmatch(line)
        if match:
            versions.append(match.group(1))

    if len(versions) != 1:
        raise ValueError("expected exactly one string project.version in [project]")
    return versions[0]


def _single_artifact(dist_dir: Path, pattern: str, kind: str) -> Path:
    matches = sorted(dist_dir.glob(pattern))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {kind}, found {len(matches)}")
    return matches[0]


def build_manifest(
    *,
    dist_dir: Path,
    source_sha: str,
    workflow_run_id: str,
    python_versions: list[str],
    release_notes_ref: str,
) -> dict[str, Any]:
    if not SHA40.fullmatch(source_sha):
        raise ValueError("source_sha must be a 40-character lowercase hexadecimal commit SHA")
    if not workflow_run_id.isdigit():
        raise ValueError("workflow_run_id must contain only digits")
    if not python_versions or len(set(python_versions)) != len(python_versions):
        raise ValueError("python_versions must be a non-empty unique list")
    if any(re.fullmatch(r"3\.[0-9]+", value) is None for value in python_versions):
        raise ValueError("python_versions entries must look like 3.10")
    if not release_notes_ref.strip():
        raise ValueError("release_notes_ref must be non-empty")

    wheel = _single_artifact(dist_dir, "*.whl", "wheel")
    sdist = _single_artifact(dist_dir, "*.tar.gz", "sdist")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "evidence_class": EVIDENCE_CLASS,
        "controller_issue": CONTROLLER_ISSUE,
        "repository": REPOSITORY,
        "source": {
            "sha": source_sha,
            "canonical_source_path": CANONICAL_SOURCE,
        },
        "package": {
            "distribution_name": "ndrorchestration-governed-repo",
            "version": package_version(),
            "wheel": {"filename": wheel.name, "sha256": sha256_file(wheel)},
            "sdist": {"filename": sdist.name, "sha256": sha256_file(sdist)},
        },
        "action": {"path": ACTION_PATH, "source_sha": source_sha},
        "compatibility": {"python_versions": list(python_versions)},
        "workflow": {
            "name": WORKFLOW_NAME,
            "run_id": workflow_run_id,
            "source_sha": source_sha,
        },
        "release_notes_ref": release_notes_ref,
        "non_effects": dict(NON_EFFECTS),
        "claim_ceiling": dict(CLAIM_CEILING),
    }
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_top = {
        "schema_version",
        "evidence_class",
        "controller_issue",
        "repository",
        "source",
        "package",
        "action",
        "compatibility",
        "workflow",
        "release_notes_ref",
        "non_effects",
        "claim_ceiling",
    }
    if set(manifest) != expected_top:
        errors.append("top-level fields must match the v1 contract exactly")

    constants = {
        "schema_version": SCHEMA_VERSION,
        "evidence_class": EVIDENCE_CLASS,
        "controller_issue": CONTROLLER_ISSUE,
        "repository": REPOSITORY,
    }
    for key, expected in constants.items():
        if manifest.get(key) != expected:
            errors.append(f"{key} must be {expected!r}")

    source = manifest.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
        source = {}
    source_sha = source.get("sha")
    if not isinstance(source_sha, str) or not SHA40.fullmatch(source_sha):
        errors.append("source.sha must be a lowercase 40-character commit SHA")
    if source.get("canonical_source_path") != CANONICAL_SOURCE:
        errors.append("source.canonical_source_path must identify the package core")

    package = manifest.get("package")
    if not isinstance(package, dict):
        errors.append("package must be an object")
        package = {}
    if package.get("distribution_name") != "ndrorchestration-governed-repo":
        errors.append("package.distribution_name is invalid")
    if not isinstance(package.get("version"), str) or not package.get("version"):
        errors.append("package.version must be non-empty")
    for kind in ("wheel", "sdist"):
        artifact = package.get(kind)
        if not isinstance(artifact, dict):
            errors.append(f"package.{kind} must be an object")
            continue
        if not isinstance(artifact.get("filename"), str) or not artifact.get("filename"):
            errors.append(f"package.{kind}.filename must be non-empty")
        digest = artifact.get("sha256")
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            errors.append(f"package.{kind}.sha256 must be lowercase SHA-256")

    action = manifest.get("action")
    if not isinstance(action, dict):
        errors.append("action must be an object")
        action = {}
    if action.get("path") != ACTION_PATH:
        errors.append("action.path is invalid")
    if action.get("source_sha") != source_sha:
        errors.append("action.source_sha must equal source.sha")

    compatibility = manifest.get("compatibility")
    versions = compatibility.get("python_versions") if isinstance(compatibility, dict) else None
    if not isinstance(versions, list) or not versions:
        errors.append("compatibility.python_versions must be non-empty")
    elif len(set(versions)) != len(versions) or any(
        not isinstance(value, str) or re.fullmatch(r"3\.[0-9]+", value) is None for value in versions
    ):
        errors.append("compatibility.python_versions must contain unique Python 3.x strings")

    workflow = manifest.get("workflow")
    if not isinstance(workflow, dict):
        errors.append("workflow must be an object")
        workflow = {}
    if workflow.get("name") != WORKFLOW_NAME:
        errors.append("workflow.name is invalid")
    run_id = workflow.get("run_id")
    if not isinstance(run_id, str) or not run_id.isdigit():
        errors.append("workflow.run_id must contain only digits")
    if workflow.get("source_sha") != source_sha:
        errors.append("workflow.source_sha must equal source.sha")

    release_notes_ref = manifest.get("release_notes_ref")
    if not isinstance(release_notes_ref, str) or not release_notes_ref.strip():
        errors.append("release_notes_ref must be non-empty")
    if manifest.get("non_effects") != dict(NON_EFFECTS):
        errors.append("non_effects must preserve the non-authorizing, non-publishing boundary")
    if manifest.get("claim_ceiling") != dict(CLAIM_CEILING):
        errors.append("claim_ceiling must preserve v1 release-candidate limits")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Governed Repo release provenance candidate.")
    parser.add_argument("--dist-dir", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--workflow-run-id", required=True)
    parser.add_argument("--python-version", action="append", required=True)
    parser.add_argument("--release-notes-ref", default="issue://1214")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    manifest = build_manifest(
        dist_dir=Path(args.dist_dir),
        source_sha=args.source_sha,
        workflow_run_id=args.workflow_run_id,
        python_versions=args.python_version,
        release_notes_ref=args.release_notes_ref,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
