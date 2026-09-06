#!/usr/bin/env python3
"""Fail-closed static leakage contract for the P4-B Mode-T continuity helper.

This validator intentionally reviews the current helper/report/CI surfaces rather than
protected material. It must never require a mapping, key, nonce, plaintext, or secret.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERIFIER = ROOT / "experiments/pdmal_pilot/mode_t_strict_verifier.go"
WORKFLOWS = [
    ROOT / ".github/workflows/p4-b-mode-t-strict-verifier-prototype.yml",
    ROOT / ".github/workflows/p4-b-mode-t-cross-runner-repro.yml",
    ROOT / ".github/workflows/p4-b-mode-t-live-synthetic-continuity.yml",
    ROOT / ".github/workflows/p4-b-mode-t-leakage-contract.yml",
]

EXPECTED_JSON_TAGS = {
    "schema_version",
    "evidence_class",
    "status",
    "control_plane_sha",
    "github_run_id",
    "github_run_attempt",
    "tlock_version",
    "tlock_source_commit",
    "network_endpoint",
    "chain_hash",
    "scheme",
    "public_key_verified",
    "network_metadata_verified",
    "strict_chain_enforced",
    "ciphertext_sha256",
    "expected_plaintext_sha256",
    "plaintext_commitment_match",
    "plaintext_persisted",
    "plaintext_emitted",
    "empirical_data_collection",
    "freeze_established",
    "pilot_authorized",
    "empirical_n",
    "classification",
}

EXPECTED_FLAG_NAMES = {
    "endpoint",
    "ciphertext",
    "expected-plaintext-sha256",
    "evidence-sha",
    "run-id",
    "run-attempt",
}

ALLOWED_PLAIN_BYTES_LINES = {
    "plainBytes := plaintext.Bytes()",
    "actualPlaintextSHA256 := sha256Hex(plainBytes)",
    "zeroBytes(plainBytes)",
}

SENSITIVE_ENV_TOKEN = re.compile(
    r"(?:^|_)(?:PLAINTEXT|MAPPING|PRIVATE_KEY|KEY|NONCE|SECRET|TOKEN|PASSWORD|PASSPHRASE)(?:_|$)"
)


def fail(message: str) -> None:
    print(f"LEAKAGE_CONTRACT_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")


def validate_verifier() -> dict[str, object]:
    text = read(VERIFIER)

    if "tlock.New(network).Strict().Decrypt" not in text:
        fail("strict decrypt call missing")
    if "tlock.New(network).Decrypt" in text:
        fail("unstrict decrypt call present")
    if "os.WriteFile" in text or "os.Create(" in text or "ioutil.WriteFile" in text:
        fail("verifier contains file-output primitive")
    if "json.NewEncoder(os.Stdout).Encode(report)" not in text:
        fail("stdout is not constrained to continuity report JSON")
    if "json.NewEncoder(os.Stderr).Encode(failureReport{" not in text:
        fail("stderr is not constrained to failure report JSON")

    for forbidden in (
        "fmt.Print",
        "log.Print",
        "os.Stdout.Write",
        "os.Stderr.Write",
        "os.Setenv",
        "os.Getenv",
        "os.LookupEnv",
    ):
        if forbidden in text:
            fail(f"verifier contains forbidden direct output/environment primitive: {forbidden}")

    tags = set(re.findall(r'json:"([^",]+)', text))
    if tags != EXPECTED_JSON_TAGS:
        added = sorted(tags - EXPECTED_JSON_TAGS)
        missing = sorted(EXPECTED_JSON_TAGS - tags)
        fail(f"report JSON surface changed; added={added} missing={missing}")

    flag_names = set(re.findall(r'flag\.String\("([^"]+)"', text))
    if flag_names != EXPECTED_FLAG_NAMES:
        added = sorted(flag_names - EXPECTED_FLAG_NAMES)
        missing = sorted(EXPECTED_FLAG_NAMES - flag_names)
        fail(f"CLI flag surface changed; added={added} missing={missing}")

    for flag_name in flag_names:
        lowered = flag_name.lower()
        if any(
            token in lowered
            for token in ("mapping", "private-key", "nonce", "secret", "password", "passphrase")
        ):
            fail(f"protected-material CLI flag is forbidden: {flag_name}")
        if "plaintext" in lowered and flag_name != "expected-plaintext-sha256":
            fail(f"raw/plaintext CLI flag is forbidden: {flag_name}")

    plain_bytes_lines = {
        line.strip() for line in text.splitlines() if "plainBytes" in line
    }
    if plain_bytes_lines != ALLOWED_PLAIN_BYTES_LINES:
        fail(f"plaintext byte-flow surface changed: {sorted(plain_bytes_lines)}")
    if "zeroBytes(plainBytes)" not in text or "plaintext.Reset()" not in text:
        fail("decrypted plaintext is not explicitly zeroed/reset after hashing")

    if 'json:"plaintext"' in text or 'json:"mapping"' in text or 'json:"private_key"' in text:
        fail("raw protected material appears in JSON report schema")

    return {
        "json_tags_reviewed": len(tags),
        "cli_flags_reviewed": len(flag_names),
        "plaintext_byte_flow_allowlisted": True,
        "strict_decrypt_only": True,
        "environment_input_surface_absent": True,
    }


def artifact_paths(text: str) -> list[str]:
    paths: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("test-artifacts/") or stripped.startswith("comparison/result/"):
            paths.append(stripped)
    return paths


def validate_workflow(path: Path) -> dict[str, object]:
    text = read(path)
    rel = str(path.relative_to(ROOT))

    if "permissions:\n  contents: read" not in text:
        fail(f"{rel}: permissions are not contents:read")
    if "${{ secrets." in text or "secrets[" in text:
        fail(f"{rel}: repository/organization secret reference is forbidden")
    if "id-token: write" in text or "contents: write" in text:
        fail(f"{rel}: write-capable permissions are forbidden")
    for marker in (
        "GITHUB_STEP_SUMMARY",
        "GITHUB_OUTPUT",
        "::set-output",
        "set -x",
        "bash -x",
    ):
        if marker in text:
            fail(f"{rel}: forbidden output/debug surface present: {marker}")

    env_names = set(
        match.group(1)
        for match in re.finditer(
            r"^\s{2,}([A-Z][A-Z0-9_]*)\s*:", text, flags=re.MULTILINE
        )
    )
    sensitive_names = sorted(
        name for name in env_names if SENSITIVE_ENV_TOKEN.search(name)
    )
    if sensitive_names:
        fail(f"{rel}: protected-material environment names present: {sensitive_names}")

    if "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" not in text:
        fail(f"{rel}: exact checkout action pin missing")

    uploads = text.count("actions/upload-artifact@")
    paths = artifact_paths(text)
    if uploads:
        if not paths:
            fail(f"{rel}: upload-artifact has no reviewable text-evidence path")
        for artifact_path in paths:
            if not (
                artifact_path.endswith(".txt")
                or artifact_path.endswith(".txt.sha256")
            ):
                fail(f"{rel}: non-text evidence path would be uploaded: {artifact_path}")
            lowered = artifact_path.lower()
            if any(
                token in lowered
                for token in (
                    "ciphertext",
                    "plaintext",
                    "mapping",
                    "private-key",
                    "nonce",
                    ".tle",
                    ".age",
                    ".bin",
                )
            ):
                fail(
                    f"{rel}: protected-material-like artifact path is forbidden: {artifact_path}"
                )

    return {
        "workflow": rel,
        "environment_names_reviewed": len(env_names),
        "artifact_paths_reviewed": len(paths),
        "secret_references": False,
        "step_outputs_or_summaries": False,
        "write_permissions": False,
    }


def main() -> None:
    verifier_result = validate_verifier()
    workflow_results = [validate_workflow(path) for path in WORKFLOWS]
    result = {
        "schema_version": 1,
        "contract": "P4_B_MODE_T_LEAKAGE_SURFACE_V1",
        "status": "PASS",
        "verifier": verifier_result,
        "workflows": workflow_results,
        "protected_material_used": False,
        "empirical_data_collection": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
