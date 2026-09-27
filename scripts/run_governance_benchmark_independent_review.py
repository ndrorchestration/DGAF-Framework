"""Run the frozen governance-benchmark reproduction contract as a reviewer.

This helper records reviewer-supplied identity/disclosure metadata, executes the
repository-native reproduction commands, verifies the regenerated review bundle,
and writes a local receipt. It does not establish independence by itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_SCRIPT = REPO_ROOT / "experiments" / "governance_benchmark" / "package_review_bundle.py"

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

EXPECTED_LAYER_NAMES = {
    "configuration_scaling",
    "cross_domain_interactions",
    "fixed",
    "mutations",
    "provenance_custody",
    "recovery_composition",
    "same_domain_interactions",
    "semantic_equivalence",
    "strong_policy_comparator",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


def environment_record() -> dict[str, Any]:
    try:
        remote = git_output("remote", "get-url", "origin")
    except (subprocess.CalledProcessError, FileNotFoundError):
        remote = None
    return {
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "repository_clone_source": remote,
    }


def run_command(command: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return {
            "command": command,
            "returncode": None,
            "stdout": "",
            "stderr": str(exc),
            "started": False,
        }
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "started": True,
    }


def verify_bundle(
    bundle_path: Path,
    *,
    expected_commit: str,
    expected_bundle_sha256: str,
) -> dict[str, Any]:
    observed_bundle_sha256 = sha256_file(bundle_path)
    checks: dict[str, Any] = {
        "observed_bundle_sha256": observed_bundle_sha256,
        "expected_bundle_sha256": expected_bundle_sha256.upper(),
        "bundle_digest_matches": observed_bundle_sha256 == expected_bundle_sha256.upper(),
        "sha256sums_valid": False,
        "handoff_commit_matches": False,
        "envelope_commit_matches": False,
        "envelope_version": None,
        "envelope_layer_names": [],
        "envelope_layers_complete": False,
        "canonical_layer_digests": {},
        "errors": [],
    }

    try:
        with zipfile.ZipFile(bundle_path) as archive:
            names = set(archive.namelist())
            sums = archive.read("SHA256SUMS.txt").decode("ascii").splitlines()
            manifest_valid = True
            for line in sums:
                if not line:
                    continue
                expected_digest, name = line.split("  ", 1)
                actual_digest = hashlib.sha256(archive.read(name)).hexdigest()
                if actual_digest != expected_digest:
                    manifest_valid = False
                    checks["errors"].append(f"SHA256SUMS mismatch: {name}")
            checks["sha256sums_valid"] = manifest_valid

            handoff = archive.read("REVIEWER_HANDOFF.md").decode("utf-8")
            checks["handoff_commit_matches"] = expected_commit in handoff

            envelope = json.loads(archive.read("evidence-envelope.json"))
            checks["envelope_commit_matches"] = envelope.get("repository_commit") == expected_commit
            checks["envelope_version"] = envelope.get("version")
            layer_digests = envelope.get("canonical_layer_digests", {})
            checks["canonical_layer_digests"] = layer_digests
            checks["envelope_layer_names"] = sorted(layer_digests)
            checks["envelope_layers_complete"] = set(layer_digests) == EXPECTED_LAYER_NAMES

            required = {
                "REVIEWER_HANDOFF.md",
                "SHA256SUMS.txt",
                "evidence-envelope.json",
                "evidence-manifest.json",
                "fixed-benchmark.json",
                "mutations.json",
                "same-domain-interactions.json",
                "cross-domain-interactions.json",
                "strong-policy-comparator.json",
                "semantic-equivalence.json",
                "configuration-scaling.json",
                "recovery-composition.json",
                "provenance-custody.json",
            }
            missing = sorted(required - names)
            if missing:
                checks["errors"].append("missing bundle payloads: " + ", ".join(missing))
    except (OSError, KeyError, ValueError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        checks["errors"].append(str(exc))

    checks["all_identity_checks_pass"] = all(
        (
            checks["bundle_digest_matches"],
            checks["sha256sums_valid"],
            checks["handoff_commit_matches"],
            checks["envelope_commit_matches"],
            checks["envelope_layers_complete"],
            not checks["errors"],
        )
    )
    return checks


def disposition(
    *,
    head_matches: bool,
    tests: dict[str, Any],
    package: dict[str, Any],
    bundle_checks: dict[str, Any] | None,
) -> str:
    if not head_matches:
        return "BLOCKED"
    if not tests["started"] or not package["started"]:
        return "BLOCKED"
    if tests["returncode"] != 0 or package["returncode"] != 0:
        return "MISMATCH"
    if bundle_checks is None or not bundle_checks["all_identity_checks_pass"]:
        return "MISMATCH"
    return "REPRODUCED"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--expected-bundle-sha256", required=True)
    parser.add_argument("--reviewer-identity", required=True)
    parser.add_argument("--affiliation", required=True)
    parser.add_argument("--relationship-disclosure", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("review-reproduction"))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    receipt_path = args.output_dir / "review_receipt.json"
    bundle_path = args.output_dir / f"DGAF-governance-benchmark-review-{args.expected_commit[:8]}.zip"

    try:
        observed_head = git_output("rev-parse", "HEAD")
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        observed_head = f"UNAVAILABLE:{exc}"

    head_matches = observed_head == args.expected_commit

    test_command = [sys.executable, "-m", "pytest", *TEST_PATHS]
    test_result = (
        run_command(test_command)
        if head_matches
        else {
            "command": test_command,
            "returncode": None,
            "stdout": "",
            "stderr": "checked-out HEAD does not match expected frozen commit",
            "started": False,
        }
    )

    package_command = [
        sys.executable,
        str(BUNDLE_SCRIPT),
        "--output",
        str(bundle_path),
    ]
    package_result = (
        run_command(package_command)
        if head_matches
        else {
            "command": package_command,
            "returncode": None,
            "stdout": "",
            "stderr": "checked-out HEAD does not match expected frozen commit",
            "started": False,
        }
    )

    bundle_checks = None
    if package_result["returncode"] == 0 and bundle_path.exists():
        bundle_checks = verify_bundle(
            bundle_path,
            expected_commit=args.expected_commit,
            expected_bundle_sha256=args.expected_bundle_sha256,
        )

    final_disposition = disposition(
        head_matches=head_matches,
        tests=test_result,
        package=package_result,
        bundle_checks=bundle_checks,
    )

    receipt = {
        "schema": "DGAF_GOVERNANCE_BENCHMARK_INDEPENDENT_REVIEW_RECEIPT_V1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "reviewer": {
            "identity": args.reviewer_identity,
            "affiliation": args.affiliation,
            "relationship_disclosure": args.relationship_disclosure,
        },
        "environment": environment_record(),
        "expected_commit": args.expected_commit,
        "observed_commit": observed_head,
        "head_matches": head_matches,
        "commands": {
            "tests": test_result,
            "package": package_result,
        },
        "bundle_checks": bundle_checks,
        "first_observed_result": final_disposition,
        "disposition": final_disposition,
        "interpretation_boundary": [
            "This receipt records reproduction evidence; it does not self-establish reviewer independence.",
            "REPRODUCED does not establish DGAF efficacy, SOTA status, certification, or High-Assurance authorization.",
            "MISMATCH and BLOCKED are valid primary outcomes and must be preserved before diagnostic reruns.",
        ],
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": str(receipt_path), "disposition": final_disposition}, indent=2))

    if final_disposition == "REPRODUCED":
        return 0
    if final_disposition == "MISMATCH":
        return 2
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
