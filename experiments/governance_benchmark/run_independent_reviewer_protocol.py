"""Reviewer-side protocol for independent governance-benchmark reproduction.

This helper creates a creation-only machine-readable execution record. It does
not adjudicate reviewer independence and cannot promote DGAF assurance state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import package_review_bundle  # noqa: E402

TEST_PATHS = (
    "tests/test_comparative_governance_benchmark.py",
    "tests/test_governance_benchmark_mutations.py",
    "tests/test_governance_benchmark_interactions.py",
    "tests/test_governance_benchmark_cross_domain.py",
    "tests/test_governance_benchmark_evidence_manifest.py",
    "tests/test_governance_benchmark_evidence_envelope.py",
    "tests/test_governance_benchmark_review_bundle.py",
    "tests/test_governance_benchmark_strong_policy.py",
    "tests/test_governance_benchmark_semantic_equivalence.py",
    "tests/test_governance_benchmark_configuration_scaling.py",
    "tests/test_governance_benchmark_recovery_composition.py",
    "tests/test_governance_benchmark_provenance_custody.py",
    "tests/test_standards_risk_crosswalk.py",
)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def git_text(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


def run_contract_tests() -> dict[str, Any]:
    command = [sys.executable, "-m", "pytest", "-q", *TEST_PATHS]
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def classify_result(
    *,
    commit_matches: bool,
    tests_returncode: int | None,
    bundle_matches: bool | None,
    blocker: str | None = None,
) -> str:
    if blocker is not None or not commit_matches:
        return "BLOCKED"
    if tests_returncode != 0 or bundle_matches is not True:
        return "MISMATCH"
    return "REPRODUCED"


def creation_only_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def execute_protocol(
    *,
    expected_commit: str,
    expected_bundle_sha256: str,
    output_dir: Path,
    reviewer_id: str,
    affiliation: str,
    relationship_disclosure: str,
    environment_note: str,
) -> dict[str, Any]:
    record_path = output_dir / "independent-review-record.json"
    if record_path.exists():
        raise FileExistsError(
            "independent-review-record.json already exists; preserve the first result and use a new directory for diagnosis"
        )

    current_commit = git_text("rev-parse", "HEAD")
    remote_url = git_text("remote", "get-url", "origin")
    dirty_paths = git_text("status", "--porcelain")
    commit_matches = current_commit == expected_commit

    record: dict[str, Any] = {
        "schema_version": "DGAF_INDEPENDENT_REVIEW_RECORD_V1",
        "reviewer": {
            "reviewer_id": reviewer_id,
            "affiliation": affiliation,
            "relationship_disclosure": relationship_disclosure,
        },
        "environment": {
            "platform": platform.platform(),
            "python": sys.version,
            "environment_note": environment_note,
        },
        "repository": {
            "remote_url": remote_url,
            "expected_commit": expected_commit,
            "observed_commit": current_commit,
            "commit_matches": commit_matches,
            "dirty_worktree": bool(dirty_paths),
            "dirty_paths": dirty_paths.splitlines() if dirty_paths else [],
        },
        "expected_bundle_sha256": expected_bundle_sha256.upper(),
        "claim_effect": {
            "INDEPENDENT_VALIDATION": "NO_AUTOMATIC_EFFECT",
            "SCIENTIFIC_N_INCREMENT": 0,
            "CANONICAL_DGAF_EFFICACY": "NOT_ESTABLISHED",
            "STATE_OF_THE_ART": "NOT_ESTABLISHED",
            "HIGH_ASSURANCE": "NOT_AUTHORIZED",
        },
        "rerun_policy": (
            "Preserve this first record. If diagnosis requires a rerun, use a new output directory "
            "and retain both records with an explanation of what changed."
        ),
    }

    tests_result: dict[str, Any] | None = None
    bundle_sha256: str | None = None
    bundle_matches: bool | None = None
    blocker: str | None = None

    if not commit_matches:
        blocker = "CHECKED_OUT_COMMIT_DOES_NOT_MATCH_FROZEN_TARGET"
    else:
        try:
            tests_result = run_contract_tests()
            bundle_path = output_dir / f"DGAF-governance-benchmark-review-{current_commit[:8]}.zip"
            package_review_bundle.build_bundle(bundle_path)
            bundle_sha256 = sha256_path(bundle_path)
            bundle_matches = bundle_sha256 == expected_bundle_sha256.upper()
        except Exception as exc:  # bounded reviewer record must survive setup/tooling blockers
            blocker = f"{type(exc).__name__}: {exc}"

    status = classify_result(
        commit_matches=commit_matches,
        tests_returncode=None if tests_result is None else tests_result["returncode"],
        bundle_matches=bundle_matches,
        blocker=blocker,
    )

    record.update(
        {
            "first_observed_result": status,
            "status": status,
            "blocker": blocker,
            "contract_tests": tests_result,
            "observed_bundle_sha256": bundle_sha256,
            "bundle_matches": bundle_matches,
        }
    )
    creation_only_write(record_path, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--expected-bundle-sha256", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--affiliation", required=True)
    parser.add_argument("--relationship-disclosure", required=True)
    parser.add_argument("--environment-note", required=True)
    args = parser.parse_args()

    try:
        record = execute_protocol(
            expected_commit=args.expected_commit,
            expected_bundle_sha256=args.expected_bundle_sha256,
            output_dir=args.output_dir,
            reviewer_id=args.reviewer_id,
            affiliation=args.affiliation,
            relationship_disclosure=args.relationship_disclosure,
            environment_note=args.environment_note,
        )
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(json.dumps(record, indent=2, sort_keys=True))
    return {"REPRODUCED": 0, "MISMATCH": 1, "BLOCKED": 2}[record["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
