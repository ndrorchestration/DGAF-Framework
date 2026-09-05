#!/usr/bin/env python3
"""Validate non-secret P4 Mode T execution preconditions.

This helper is deliberately pre-secret and non-authorizing. It does not generate,
accept, decrypt, or persist a real blinding key, condition mapping, commitment
nonce, empirical observation, freeze, or authorization. It is a design-control
validator for Issue #287 and must not be wired into the empirical runner until a
separate reviewed migration explicitly authorizes that integration.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_RUNNER_CLASS = "github-hosted-standard-vm"
FORBIDDEN_PUBLIC_KEYS = {
    "raw_blinding_key",
    "cleartext_mapping",
    "key_commitment_nonce",
    "mapping_commitment_nonce",
    "recovery_seed",
    "recovery_phrase",
    "plaintext_release_bundle",
}


class ModeTPreconditionError(ValueError):
    """Raised when a Mode T pre-secret invariant is not satisfied."""


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise ModeTPreconditionError(message)


def _expect_nonempty(value: Any, field: str) -> str:
    _expect(isinstance(value, str) and bool(value.strip()), f"{field} must be non-empty")
    return value.strip()


def _expect_positive_int(value: Any, field: str) -> int:
    _expect(isinstance(value, int) and not isinstance(value, bool) and value > 0, f"{field} must be a positive integer")
    return value


def _expect_hex40(value: Any, field: str) -> str:
    text = _expect_nonempty(value, field)
    _expect(bool(HEX40.fullmatch(text)), f"{field} must be a 40-character lowercase hex SHA")
    return text


def _expect_hex64(value: Any, field: str) -> str:
    text = _expect_nonempty(value, field)
    _expect(bool(HEX64.fullmatch(text)), f"{field} must be a 64-character lowercase hex SHA-256")
    return text


def _walk_forbidden_public_keys(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            _expect(isinstance(key, str), f"{path} contains a non-string key")
            _expect(key not in FORBIDDEN_PUBLIC_KEYS, f"forbidden protected-material field in public payload: {path}.{key}")
            _walk_forbidden_public_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden_public_keys(child, f"{path}[{index}]")


def validate_preconditions(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate only non-secret execution preconditions.

    The input is expected to be a public metadata object. Unknown additional
    fields are permitted only if they do not use explicitly forbidden
    protected-material field names.
    """

    _expect(isinstance(payload, dict), "payload must be an object")
    _walk_forbidden_public_keys(payload)

    run_id = _expect_positive_int(payload.get("github_run_id"), "github_run_id")
    run_attempt = _expect_positive_int(payload.get("github_run_attempt"), "github_run_attempt")
    _expect(run_attempt == 1, "github_run_attempt must equal 1; reruns fail closed")

    authorization_run_id = _expect_positive_int(payload.get("authorization_run_id"), "authorization_run_id")
    authorization_attempt = _expect_positive_int(payload.get("authorization_attempt"), "authorization_attempt")
    _expect(authorization_run_id == run_id, "authorization is bound to a different GitHub run ID")
    _expect(authorization_attempt == 1, "authorization_attempt must equal 1")

    github_sha = _expect_hex40(payload.get("github_sha"), "github_sha")
    expected_github_sha = _expect_hex40(payload.get("expected_github_sha"), "expected_github_sha")
    _expect(github_sha == expected_github_sha, "runtime GitHub SHA differs from frozen expected SHA")

    workflow_sha256 = _expect_hex64(payload.get("workflow_sha256"), "workflow_sha256")
    expected_workflow_sha256 = _expect_hex64(payload.get("expected_workflow_sha256"), "expected_workflow_sha256")
    _expect(workflow_sha256 == expected_workflow_sha256, "workflow digest differs from frozen expected digest")

    helper_sha256 = _expect_hex64(payload.get("helper_sha256"), "helper_sha256")
    expected_helper_sha256 = _expect_hex64(payload.get("expected_helper_sha256"), "expected_helper_sha256")
    _expect(helper_sha256 == expected_helper_sha256, "helper digest differs from frozen expected digest")

    runner_class = _expect_nonempty(payload.get("runner_class"), "runner_class")
    _expect(runner_class == ALLOWED_RUNNER_CLASS, f"runner_class must equal {ALLOWED_RUNNER_CLASS}")

    debug_enabled = payload.get("debug_enabled")
    _expect(debug_enabled is False, "debug mode must be explicitly false before secret generation")

    chain_hash = _expect_hex64(payload.get("timelock_chain_hash"), "timelock_chain_hash")
    expected_chain_hash = _expect_hex64(payload.get("expected_timelock_chain_hash"), "expected_timelock_chain_hash")
    _expect(chain_hash == expected_chain_hash, "timelock chain hash differs from frozen expected chain")

    strict_chain_binding = payload.get("strict_chain_binding")
    _expect(strict_chain_binding is True, "strict timelock chain binding must be enabled")

    current_round = _expect_positive_int(payload.get("current_round"), "current_round")
    release_round = _expect_positive_int(payload.get("release_round"), "release_round")
    minimum_round_gap = _expect_positive_int(payload.get("minimum_round_gap"), "minimum_round_gap")
    _expect(release_round > current_round, "release_round must be in the future")
    _expect(
        release_round - current_round >= minimum_round_gap,
        "release_round does not satisfy the frozen minimum round gap",
    )

    p6_retention_status = _expect_nonempty(payload.get("p6_retention_status"), "p6_retention_status")
    _expect(
        p6_retention_status == "RESERVATION_AND_AUTHORIZATION_RETAINED",
        "independent P6 reservation/authorization retention is not established",
    )

    authorization_status = _expect_nonempty(payload.get("authorization_status"), "authorization_status")
    _expect(authorization_status == "GRANTED_FOR_EXACT_RESERVED_RUN", "exact-run pilot authorization is not granted")

    return {
        "schema_version": 1,
        "evidence_class": "P4_MODE_T_PRE_SECRET_PRECONDITION_CHECK",
        "result": "PASS",
        "github_run_id": run_id,
        "github_run_attempt": run_attempt,
        "github_sha": github_sha,
        "workflow_sha256": workflow_sha256,
        "helper_sha256": helper_sha256,
        "runner_class": runner_class,
        "timelock_chain_hash": chain_hash,
        "release_round": release_round,
        "minimum_round_gap": minimum_round_gap,
        "p6_retention_status": p6_retention_status,
        "authorization_status": authorization_status,
        "secret_instantiation": "NOT_PERFORMED_BY_THIS_VALIDATOR",
        "empirical_execution": "NOT_PERFORMED_BY_THIS_VALIDATOR",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        result = validate_preconditions(raw)
    except (OSError, json.JSONDecodeError, ModeTPreconditionError) as exc:
        print(f"P4 Mode T precondition validation FAIL-CLOSED: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("P4 Mode T precondition validation PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
