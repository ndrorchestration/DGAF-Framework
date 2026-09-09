#!/usr/bin/env python3
"""Controlled synthetic Sigstore/Rekor timing helper for DGAF P4 Mode T.

The helper is intentionally non-authorizing and accepts only synthetic metadata.
Execution creates a public transparency-log side effect and must therefore only be
called from the repository's manual-dispatch workflow.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any

EVIDENCE_CLASS = "P4_MODE_T_SYNTHETIC_TIMING_NOT_AUTHORIZATION"
OIDC_ISSUER = "https://token.actions.githubusercontent.com"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class RekorTimingError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_synthetic_blob(*, evidence_sha: str, run_id: str, run_attempt: str, workflow_ref: str) -> bytes:
    if not SHA_RE.fullmatch(evidence_sha):
        raise RekorTimingError("invalid evidence SHA")
    if not run_id.isdigit() or int(run_id) < 1:
        raise RekorTimingError("invalid run id")
    if not run_attempt.isdigit() or int(run_attempt) != 1:
        raise RekorTimingError("only first workflow attempt is accepted")
    if not workflow_ref.startswith("ndrorchestration/DGAF-Framework/.github/workflows/"):
        raise RekorTimingError("unexpected workflow identity")

    payload = {
        "schema_version": 1,
        "evidence_class": EVIDENCE_CLASS,
        "repository": "ndrorchestration/DGAF-Framework",
        "evidence_sha": evidence_sha,
        "github_run_id": run_id,
        "github_run_attempt": run_attempt,
        "github_workflow_ref": workflow_ref,
        "empirical_data_collection": False,
        "protected_material_present": False,
        "secret_instantiation": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "authorization_consumed": False,
        "analysis_lock_created": False,
        "numeric_w_selected": False,
        "empirical_n": 0,
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def extract_tlog_evidence(bundle: dict[str, Any]) -> dict[str, Any]:
    material = bundle.get("verificationMaterial")
    if not isinstance(material, dict):
        raise RekorTimingError("bundle missing verificationMaterial")
    entries = material.get("tlogEntries")
    if not isinstance(entries, list) or not entries:
        raise RekorTimingError("bundle contains no transparency-log entries")

    entry = entries[0]
    if not isinstance(entry, dict):
        raise RekorTimingError("invalid transparency-log entry")

    integrated_time = entry.get("integratedTime")
    log_index = entry.get("logIndex")
    try:
        integrated_time_int = int(integrated_time)
        log_index_int = int(log_index)
    except (TypeError, ValueError) as exc:
        raise RekorTimingError("invalid transparency-log time/index") from exc
    if integrated_time_int < 1 or log_index_int < 0:
        raise RekorTimingError("invalid transparency-log time/index bounds")

    has_inclusion_proof = isinstance(entry.get("inclusionProof"), dict)
    has_inclusion_promise = isinstance(entry.get("inclusionPromise"), dict)
    if not (has_inclusion_proof or has_inclusion_promise):
        raise RekorTimingError("transparency-log entry lacks inclusion material")

    log_id = entry.get("logId")
    if isinstance(log_id, dict):
        log_id = log_id.get("keyId")
    if not isinstance(log_id, str) or not log_id:
        log_id = "UNAVAILABLE_IN_BUNDLE"

    return {
        "tlog_entry_count": len(entries),
        "integrated_time": integrated_time_int,
        "log_index": log_index_int,
        "log_id": log_id,
        "has_inclusion_proof": has_inclusion_proof,
        "has_inclusion_promise": has_inclusion_promise,
    }


def _run_checked(args: list[str], *, timeout: int) -> float:
    start = time.monotonic_ns()
    proc = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        check=False,
    )
    elapsed_ms = (time.monotonic_ns() - start) / 1_000_000.0
    if proc.returncode != 0:
        raise RekorTimingError(f"command failed with exit code {proc.returncode}")
    return round(elapsed_ms, 6)


def execute(*, cosign: Path, cosign_sha256: str, blob_path: Path, bundle_path: Path, output_path: Path) -> None:
    if not SHA256_RE.fullmatch(cosign_sha256):
        raise RekorTimingError("invalid cosign SHA-256")

    evidence_sha = os.environ.get("EVIDENCE_SHA", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "")
    workflow_ref = os.environ.get("GITHUB_WORKFLOW_REF", "")
    if os.environ.get("GITHUB_EVENT_NAME") != "workflow_dispatch":
        raise RekorTimingError("Rekor timing execution is manual-dispatch only")

    blob = build_synthetic_blob(
        evidence_sha=evidence_sha,
        run_id=run_id,
        run_attempt=run_attempt,
        workflow_ref=workflow_ref,
    )
    blob_path.parent.mkdir(parents=True, exist_ok=True)
    blob_path.write_bytes(blob)

    expected_identity = f"https://github.com/{workflow_ref}"
    sign_ms = _run_checked(
        [str(cosign), "sign-blob", "--bundle", str(bundle_path), "--yes", str(blob_path)],
        timeout=90,
    )
    if not bundle_path.is_file() or bundle_path.stat().st_size < 1:
        raise RekorTimingError("cosign produced no bundle")

    verify_ms = _run_checked(
        [
            str(cosign),
            "verify-blob",
            "--bundle",
            str(bundle_path),
            "--certificate-identity",
            expected_identity,
            "--certificate-oidc-issuer",
            OIDC_ISSUER,
            str(blob_path),
        ],
        timeout=60,
    )

    bundle_raw = bundle_path.read_bytes()
    try:
        bundle = json.loads(bundle_raw)
    except json.JSONDecodeError as exc:
        raise RekorTimingError("bundle is not valid JSON") from exc
    tlog = extract_tlog_evidence(bundle)

    evidence = {
        "schema_version": 1,
        "evidence_class": "P4_MODE_T_SYNTHETIC_REKOR_TIMING_V1",
        "control_plane_sha": evidence_sha,
        "github_run_id": run_id,
        "github_run_attempt": run_attempt,
        "github_workflow_ref": workflow_ref,
        "certificate_identity": expected_identity,
        "certificate_oidc_issuer": OIDC_ISSUER,
        "cosign_sha256": cosign_sha256,
        "synthetic_blob_sha256": sha256_bytes(blob),
        "bundle_sha256": sha256_bytes(bundle_raw),
        "sign_submission_ms": sign_ms,
        "bundle_verification_ms": verify_ms,
        **tlog,
        "public_transparency_side_effect": True,
        "empirical_data_collection": False,
        "protected_material_present": False,
        "secret_instantiation": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "authorization_consumed": False,
        "analysis_lock_created": False,
        "numeric_w_selected": False,
        "w_proposal_eligible": False,
        "empirical_n": 0,
    }
    raw = (json.dumps(evidence, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(raw)
    digest = sha256_bytes(raw)
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="utf-8"
    )
    print(json.dumps({"status": "PASS", "evidence_sha256": digest}, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cosign", type=Path, required=True)
    parser.add_argument("--cosign-sha256", required=True)
    parser.add_argument("--blob", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    execute(
        cosign=args.cosign,
        cosign_sha256=args.cosign_sha256,
        blob_path=args.blob,
        bundle_path=args.bundle,
        output_path=args.output,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
