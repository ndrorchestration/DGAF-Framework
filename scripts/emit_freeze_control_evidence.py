#!/usr/bin/env python3
"""Emit machine-readable E2b verifier and M6 negative-state evidence.

This script is observational and fail-closed: it never authorizes a pilot,
creates a freeze, unblinds labels, or changes empirical state.

Two identities are always recorded separately:
- verifier_commit_sha: the Git revision containing this evidence machinery;
- target_candidate_sha: the executable apparatus being evaluated.

The verifier must never silently relabel its own branch HEAD as the apparatus
candidate. The target candidate is supplied explicitly by the workflow.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "freeze_controls"

CANDIDATE_PATHS = (
    ".github/workflows/governance-ci.yml",
    "experiments/pdmal_pilot/analysis.py",
    "experiments/pdmal_pilot/pilot_artifact_schema.py",
    "experiments/pdmal_pilot/run_pilot.py",
    "experiments/pdmal_pilot/requirements-full-lock.txt",
    "docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md",
)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout.strip()


def git_show_bytes(commit_sha: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit_sha}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        timeout=30,
    )
    return result.stdout


def require_full_sha(value: str, label: str) -> str:
    normalized = value.strip().lower()
    if len(normalized) != 40 or any(char not in "0123456789abcdef" for char in normalized):
        raise RuntimeError(f"{label} must be a full 40-character SHA")
    return normalized


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def pip_freeze_digest() -> tuple[str, list[str]]:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    lines = sorted(line.strip() for line in result.stdout.splitlines() if line.strip())
    return hashlib.sha256("\n".join(lines).encode()).hexdigest(), lines


def pip_version() -> str:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "--version"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def observed_negative_state() -> dict[str, Any]:
    freeze_manifest = ROOT / "docs" / "experiment" / "FREEZE_MANIFEST.md"
    current_state = ROOT / "docs" / "CURRENT_STATE.md"
    freeze_text = freeze_manifest.read_text(encoding="utf-8") if freeze_manifest.exists() else ""
    state_text = current_state.read_text(encoding="utf-8") if current_state.exists() else ""

    pilot_artifacts = sorted(
        str(path.relative_to(ROOT))
        for pattern in ("pilot_seed_*.json", "pilot_summary.json")
        for path in ROOT.rglob(pattern)
        if ".git" not in path.parts
    )

    authorization = os.getenv("PDMAL_PILOT_AUTHORIZED")
    protocol_frozen = os.getenv("PDMAL_PROTOCOL_FROZEN")
    mode = os.getenv("PDMAL_MODE")
    blinding_key_present = bool(os.getenv("PDMAL_BLINDING_KEY"))

    observed = {
        "freeze_manifest_declares_pre_freeze": "PRE-FREEZE" in freeze_text,
        "current_state_mentions_n_zero": "N = 0" in state_text or "N=0" in state_text,
        "current_state_mentions_not_granted": "NOT GRANTED" in state_text,
        "pilot_authorization_env_absent": authorization not in {"1", "true", "TRUE"},
        "protocol_frozen_env_absent": protocol_frozen not in {"1", "true", "TRUE"},
        "pilot_mode_not_selected": mode != "pilot",
        "blinding_key_absent": not blinding_key_present,
        "pilot_artifacts_in_workspace": pilot_artifacts,
        "pilot_artifact_scan_count": len(pilot_artifacts),
        "pilot_invocation_in_this_job": False,
    }

    required = (
        observed["freeze_manifest_declares_pre_freeze"],
        observed["current_state_mentions_n_zero"],
        observed["current_state_mentions_not_granted"],
        observed["pilot_authorization_env_absent"],
        observed["protocol_frozen_env_absent"],
        observed["pilot_mode_not_selected"],
        observed["blinding_key_absent"],
        observed["pilot_artifact_scan_count"] == 0,
        observed["pilot_invocation_in_this_job"],
    )
    if not all(required):
        raise RuntimeError(f"M6 negative-state predicate failed: {observed}")
    return observed


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    verifier_commit_sha = require_full_sha(git("rev-parse", "HEAD"), "verifier_commit_sha")
    target_candidate_sha = require_full_sha(
        os.getenv("PDMAL_TARGET_CANDIDATE_SHA", ""),
        "PDMAL_TARGET_CANDIDATE_SHA",
    )

    # Ensure the target candidate exists locally and contains the expected apparatus files.
    git("cat-file", "-e", f"{target_candidate_sha}^{{commit}}")
    target_source_sha256 = {
        path: sha256_bytes(git_show_bytes(target_candidate_sha, path))
        for path in CANDIDATE_PATHS
    }

    target_lock_sha = target_source_sha256["experiments/pdmal_pilot/requirements-full-lock.txt"]
    current_lock_sha = sha256_file(ROOT / "experiments/pdmal_pilot/requirements-full-lock.txt")
    if target_lock_sha != current_lock_sha:
        raise RuntimeError(
            "verifier dependency lock differs from target candidate lock; refusing to emit E2b evidence"
        )

    verifier_workflow_sha = sha256_file(ROOT / ".github/workflows/governance-ci.yml")
    freeze_state = observed_negative_state()
    freeze_state["state_hash"] = hashlib.sha256(canonical_bytes(freeze_state)).hexdigest()

    package_digest, packages = pip_freeze_digest()
    negative_document = {
        "evidence_class": "PRE_FREEZE_NEGATIVE_STATE_OBSERVED",
        "verifier_commit_sha": verifier_commit_sha,
        "target_candidate_sha": target_candidate_sha,
        "workflow": os.getenv("GITHUB_WORKFLOW"),
        "workflow_run_id": os.getenv("GITHUB_RUN_ID"),
        "observations": freeze_state,
        "interpretation": {
            "empirical_n_observed_in_workspace": 0,
            "pilot_authorization": "NOT_GRANTED",
            "freeze": "NOT_CREATED",
            "unblinding": "NOT_PERFORMED_IN_THIS_JOB",
        },
        "limitations": [
            "This artifact proves the observed negative-state conditions in the current verification job and workspace; it is not a retrospective proof that no pilot execution ever occurred elsewhere.",
            "Historical pilot execution claims require separately retained execution records and custody evidence.",
        ],
    }
    negative_path = OUTPUT_DIR / "negative_state_evidence.json"
    negative_path.write_bytes(canonical_bytes(negative_document))
    negative_sha = sha256_file(negative_path)

    fingerprint = {
        "evidence_class": "VERIFIER_TOOLCHAIN_FINGERPRINT",
        "verifier_commit_sha": verifier_commit_sha,
        "target_candidate_sha": target_candidate_sha,
        "target_candidate_source_sha256": target_source_sha256,
        "verifier_workflow_definition_sha256": verifier_workflow_sha,
        "dependency_lock_path": "experiments/pdmal_pilot/requirements-full-lock.txt",
        "dependency_lock_sha256": target_lock_sha,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "pip_version": pip_version(),
        "platform": platform.platform(),
        "runner_os": os.getenv("RUNNER_OS"),
        "runner_arch": os.getenv("RUNNER_ARCH"),
        "github_workflow": os.getenv("GITHUB_WORKFLOW"),
        "github_run_id": os.getenv("GITHUB_RUN_ID"),
        "github_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "github_event_name": os.getenv("GITHUB_EVENT_NAME"),
        "installed_package_digest_sha256": package_digest,
        "installed_package_count": len(packages),
        "negative_state_artifact_sha256": negative_sha,
    }
    fingerprint_path = OUTPUT_DIR / "verifier_toolchain_fingerprint.json"
    fingerprint_path.write_bytes(canonical_bytes(fingerprint))

    manifest = {
        "evidence_class": "CANDIDATE_EVIDENCE_MANIFEST",
        "verifier_commit_sha": verifier_commit_sha,
        "target_candidate_sha": target_candidate_sha,
        "workflow_run_id": os.getenv("GITHUB_RUN_ID"),
        "e2b_artifact": str(fingerprint_path.relative_to(ROOT)),
        "e2b_artifact_sha256": sha256_file(fingerprint_path),
        "m6_artifact": str(negative_path.relative_to(ROOT)),
        "m6_artifact_sha256": negative_sha,
        "authorization": "NOT_GRANTED",
        "freeze": "NOT_CREATED",
        "empirical_n": 0,
    }
    manifest_path = OUTPUT_DIR / "candidate_evidence_manifest.json"
    manifest_path.write_bytes(canonical_bytes(manifest))

    print(json.dumps({
        "verifier_commit_sha": verifier_commit_sha,
        "target_candidate_sha": target_candidate_sha,
        "e2b_artifact": str(fingerprint_path),
        "m6_artifact": str(negative_path),
        "manifest": str(manifest_path),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
