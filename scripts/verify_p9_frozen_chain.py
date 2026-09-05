#!/usr/bin/env python3
"""Fail-closed verifier for a future immutable PDMAL freeze.

This verifier is intentionally unusable as a final-P9 PASS against the current
PRE-FREEZE control state. It validates a finalized JSON freeze object, compares
its byte digest to an externally supplied SHA-256, independently resolves key
identities from the frozen candidate manifest and final P7 binding document,
and validates a separate post-freeze P8 verification record.

The P8 verification record is deliberately external to the immutable freeze so
post-freeze verification evidence cannot change the bytes it claims to verify.
The verification-record commit identity is also external to the record so the
record does not self-embed the SHA of the commit whose hash depends on it.

This verifier does not execute the experiment, authorize a pilot, or perform
unblinding.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_PREDICATES = ("P1", "P2", "P3", "P4", "P5", "P6", "P6a")
EXPECTED_FREEZE_RECORD_TYPE = "PDMAL_IMMUTABLE_FREEZE"
EXPECTED_P8_VERIFICATION_RECORD_TYPE = "PDMAL_P8_FREEZE_VERIFICATION"
EXPECTED_FREEZE_PATH = "docs/experiment/PDMAL_IMMUTABLE_FREEZE.json"


class VerificationError(RuntimeError):
    """Raised when final-chain verification must fail closed."""


def _fail(message: str) -> None:
    raise VerificationError(message)


def _expect(condition: bool, message: str) -> None:
    if not condition:
        _fail(message)


def _expect_nonempty(value: Any, field: str) -> str:
    _expect(isinstance(value, str) and bool(value.strip()), f"{field} must be non-empty")
    return value.strip()


def _expect_hex40(value: Any, field: str) -> str:
    text = _expect_nonempty(value, field)
    _expect(bool(HEX40.fullmatch(text)), f"{field} must be 40 lowercase hex characters")
    return text


def _expect_hex64(value: Any, field: str) -> str:
    text = _expect_nonempty(value, field)
    _expect(bool(HEX64.fullmatch(text)), f"{field} must be 64 lowercase hex characters")
    return text


def _dict_at(obj: dict[str, Any], key: str) -> dict[str, Any]:
    value = obj.get(key)
    _expect(isinstance(value, dict), f"{key} must be an object")
    return value


def _decode_json_object(raw: bytes, field: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(f"{field} must be UTF-8 JSON: {exc}")
    _expect(isinstance(value, dict), f"{field} root must be an object")
    return value


def _extract_fenced_yaml_scalar(text: str, key: str) -> str:
    """Extract one unambiguous scalar from fenced YAML-like control documents."""

    matches: list[str] = []
    in_yaml = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped == "```yaml":
            in_yaml = True
            continue
        if in_yaml and stripped == "```":
            in_yaml = False
            continue
        if not in_yaml:
            continue
        match = re.match(rf"^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", raw_line)
        if not match:
            continue
        value = match.group(1).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'\"', "'"}:
            value = value[1:-1]
        matches.append(value)

    _expect(len(matches) == 1, f"{key} must appear exactly once in fenced YAML; found {len(matches)}")
    return matches[0]


def _candidate_identity(candidate_manifest: Path) -> dict[str, str]:
    text = candidate_manifest.read_text(encoding="utf-8")
    candidate_sha = _expect_hex40(
        _extract_fenced_yaml_scalar(text, "candidate_sha"),
        "candidate_manifest.candidate_sha",
    )
    candidate_tree = _expect_hex40(
        _extract_fenced_yaml_scalar(text, "candidate_tree_sha"),
        "candidate_manifest.candidate_tree_sha",
    )
    deployment_id = _expect_nonempty(
        _extract_fenced_yaml_scalar(text, "deployment_id"),
        "candidate_manifest.deployment_id",
    )
    return {
        "candidate_sha": candidate_sha,
        "candidate_tree_sha": candidate_tree,
        "deployment_id": deployment_id,
    }


def _p7_identity(p7_binding: Path) -> dict[str, str]:
    text = p7_binding.read_text(encoding="utf-8")
    status = _expect_nonempty(_extract_fenced_yaml_scalar(text, "status"), "p7.status")
    _expect(status == "CLOSED", f"P7 must be CLOSED for final P9; found {status!r}")

    return {
        "candidate_sha": _expect_hex40(
            _extract_fenced_yaml_scalar(text, "candidate_sha"), "p7.candidate_sha"
        ),
        "candidate_tree_sha": _expect_hex40(
            _extract_fenced_yaml_scalar(text, "candidate_tree_sha"), "p7.candidate_tree_sha"
        ),
        "deployment_id": _expect_nonempty(
            _extract_fenced_yaml_scalar(text, "deployment_id"), "p7.deployment_id"
        ),
        "protocol_version": _expect_nonempty(
            _extract_fenced_yaml_scalar(text, "protocol_version"), "p7.protocol_version"
        ),
        "protocol_blob_sha": _expect_hex40(
            _extract_fenced_yaml_scalar(text, "protocol_blob_sha"), "p7.protocol_blob_sha"
        ),
        "protocol_content_sha256": _expect_hex64(
            _extract_fenced_yaml_scalar(text, "protocol_content_sha256"), "p7.protocol_content_sha256"
        ),
        "analysis_blob_sha": _expect_hex40(
            _extract_fenced_yaml_scalar(text, "analysis_blob_sha"), "p7.analysis_blob_sha"
        ),
        "analysis_config_sha256": _expect_hex64(
            _extract_fenced_yaml_scalar(text, "analysis_config_sha256"), "p7.analysis_config_sha256"
        ),
        "runner_blob_sha": _expect_hex40(
            _extract_fenced_yaml_scalar(text, "runner_blob_sha"), "p7.runner_blob_sha"
        ),
        "artifact_schema_blob_sha": _expect_hex40(
            _extract_fenced_yaml_scalar(text, "artifact_schema_blob_sha"), "p7.artifact_schema_blob_sha"
        ),
        "final_control_plane_commit": _expect_hex40(
            _extract_fenced_yaml_scalar(text, "final_control_plane_commit"), "p7.final_control_plane_commit"
        ),
        "selected_p9_verifier_script_sha256": _expect_hex64(
            _extract_fenced_yaml_scalar(text, "selected_p9_verifier_script_sha256"),
            "p7.selected_p9_verifier_script_sha256",
        ),
        "selected_p9_workflow_sha256": _expect_hex64(
            _extract_fenced_yaml_scalar(text, "selected_p9_workflow_sha256"),
            "p7.selected_p9_workflow_sha256",
        ),
    }


def _validate_evidence_ref(ref: Any, predicate: str, index: int) -> None:
    _expect(isinstance(ref, dict), f"predicates.{predicate}.evidence[{index}] must be an object")
    _expect_nonempty(ref.get("id"), f"predicates.{predicate}.evidence[{index}].id")
    _expect_hex64(ref.get("sha256"), f"predicates.{predicate}.evidence[{index}].sha256")


def _validate_p8_verification_record(
    *,
    record_bytes: bytes,
    expected_record_sha256: str,
    freeze_commit_sha: str,
    freeze_sha256: str,
) -> dict[str, str]:
    expected_record_sha256 = _expect_hex64(expected_record_sha256, "expected_p8_verification_sha256")
    actual_record_sha256 = hashlib.sha256(record_bytes).hexdigest()
    _expect(
        actual_record_sha256 == expected_record_sha256,
        "P8 verification record byte SHA-256 does not match externally supplied digest",
    )

    record = _decode_json_object(record_bytes, "P8 verification record")
    _expect(record.get("schema_version") == 1, "P8 verification schema_version must equal 1")
    _expect(
        record.get("record_type") == EXPECTED_P8_VERIFICATION_RECORD_TYPE,
        "P8 verification record_type mismatch",
    )
    _expect(record.get("status") == "PASS", "P8 independent freeze verification must PASS")
    _expect(
        "verification_commit_sha" not in record,
        "P8 verification record must not self-embed its containing commit SHA",
    )

    freeze_ref = _dict_at(record, "freeze")
    _expect(
        _expect_hex40(freeze_ref.get("commit_sha"), "p8_verification.freeze.commit_sha") == freeze_commit_sha,
        "P8 verification record references a different freeze commit",
    )
    _expect(
        _expect_nonempty(freeze_ref.get("path"), "p8_verification.freeze.path") == EXPECTED_FREEZE_PATH,
        "P8 verification record freeze path mismatch",
    )
    _expect(
        _expect_hex64(freeze_ref.get("expected_sha256"), "p8_verification.freeze.expected_sha256") == freeze_sha256,
        "P8 verification expected freeze digest differs from supplied freeze digest",
    )
    _expect(
        _expect_hex64(freeze_ref.get("retrieved_sha256"), "p8_verification.freeze.retrieved_sha256") == freeze_sha256,
        "P8 verification retrieved freeze digest differs from supplied freeze digest",
    )

    verifier_id = _expect_nonempty(record.get("verifier_id"), "p8_verification.verifier_id")
    verification_method = _expect_nonempty(record.get("verification_method"), "p8_verification.verification_method")
    verified_at = _expect_nonempty(record.get("verified_at"), "p8_verification.verified_at")

    return {
        "record_sha256": actual_record_sha256,
        "verifier_id": verifier_id,
        "verification_method": verification_method,
        "verified_at": verified_at,
    }


def validate_freeze(
    *,
    freeze_bytes: bytes,
    expected_sha256: str,
    p8_verification_bytes: bytes,
    expected_p8_verification_sha256: str,
    candidate_manifest: Path,
    p7_binding: Path,
    freeze_commit_sha: str,
    p8_verification_commit_sha: str,
    p9_verifier_script_sha256: str,
    p9_workflow_sha256: str,
) -> dict[str, Any]:
    expected_sha256 = _expect_hex64(expected_sha256, "expected_freeze_sha256")
    freeze_commit_sha = _expect_hex40(freeze_commit_sha, "freeze_commit_sha")
    p8_verification_commit_sha = _expect_hex40(p8_verification_commit_sha, "p8_verification_commit_sha")
    p9_verifier_script_sha256 = _expect_hex64(p9_verifier_script_sha256, "p9_verifier_script_sha256")
    p9_workflow_sha256 = _expect_hex64(p9_workflow_sha256, "p9_workflow_sha256")
    _expect(
        p8_verification_commit_sha != freeze_commit_sha,
        "P8 verification commit must be distinct from the immutable freeze commit",
    )

    actual_sha256 = hashlib.sha256(freeze_bytes).hexdigest()
    _expect(actual_sha256 == expected_sha256, "freeze byte SHA-256 does not match externally supplied digest")

    freeze = _decode_json_object(freeze_bytes, "freeze object")
    _expect(freeze.get("schema_version") == 1, "freeze schema_version must equal 1")
    _expect(freeze.get("record_type") == EXPECTED_FREEZE_RECORD_TYPE, "record_type mismatch")
    _expect(freeze.get("freeze_state") == "FROZEN", "freeze_state must be FROZEN")
    _expect(
        "independent_freeze_verification" not in freeze,
        "immutable freeze must not embed post-freeze verification evidence",
    )

    accepted_control_plane = _expect_hex40(freeze.get("accepted_control_plane_commit"), "accepted_control_plane_commit")
    _expect(
        accepted_control_plane != freeze_commit_sha,
        "accepted_control_plane_commit must be the pre-freeze accepted control state, not a self-embedded freeze commit SHA",
    )

    candidate = _dict_at(freeze, "candidate")
    candidate_sha = _expect_hex40(candidate.get("sha"), "candidate.sha")
    candidate_tree = _expect_hex40(candidate.get("tree_sha"), "candidate.tree_sha")
    deployment_id = _expect_nonempty(candidate.get("deployment_id"), "candidate.deployment_id")

    canonical_candidate = _candidate_identity(candidate_manifest)
    _expect(candidate_sha == canonical_candidate["candidate_sha"], "freeze candidate SHA differs from canonical manifest")
    _expect(candidate_tree == canonical_candidate["candidate_tree_sha"], "freeze candidate tree differs from canonical manifest")
    _expect(deployment_id == canonical_candidate["deployment_id"], "freeze deployment differs from canonical manifest")

    apparatus = _dict_at(freeze, "apparatus")
    _expect_hex40(apparatus.get("source_sha"), "apparatus.source_sha")
    _expect_hex40(apparatus.get("p35_boundary_sha"), "apparatus.p35_boundary_sha")

    protocol = _dict_at(freeze, "protocol")
    protocol_version = _expect_nonempty(protocol.get("version"), "protocol.version")
    protocol_blob = _expect_hex40(protocol.get("blob_sha"), "protocol.blob_sha")
    protocol_content = _expect_hex64(protocol.get("content_sha256"), "protocol.content_sha256")

    analysis = _dict_at(freeze, "analysis")
    analysis_blob = _expect_hex40(analysis.get("implementation_blob_sha"), "analysis.implementation_blob_sha")
    analysis_config = _expect_hex64(analysis.get("config_sha256"), "analysis.config_sha256")
    runner_blob = _expect_hex40(analysis.get("runner_blob_sha"), "analysis.runner_blob_sha")
    schema_blob = _expect_hex40(analysis.get("artifact_schema_blob_sha"), "analysis.artifact_schema_blob_sha")

    p7 = _p7_identity(p7_binding)
    comparisons = {
        "candidate_sha": candidate_sha,
        "candidate_tree_sha": candidate_tree,
        "deployment_id": deployment_id,
        "protocol_version": protocol_version,
        "protocol_blob_sha": protocol_blob,
        "protocol_content_sha256": protocol_content,
        "analysis_blob_sha": analysis_blob,
        "analysis_config_sha256": analysis_config,
        "runner_blob_sha": runner_blob,
        "artifact_schema_blob_sha": schema_blob,
        "final_control_plane_commit": accepted_control_plane,
        "selected_p9_verifier_script_sha256": p9_verifier_script_sha256,
        "selected_p9_workflow_sha256": p9_workflow_sha256,
    }
    for key, value in comparisons.items():
        _expect(value == p7[key], f"freeze/final verifier {key} differs from final P7 binding")

    predicates = _dict_at(freeze, "predicates")
    for predicate in REQUIRED_PREDICATES:
        record = predicates.get(predicate)
        _expect(isinstance(record, dict), f"predicates.{predicate} must be an object")
        _expect(record.get("status") == "CLOSED / VERIFIED", f"{predicate} must be CLOSED / VERIFIED")
        evidence = record.get("evidence")
        _expect(isinstance(evidence, list) and evidence, f"{predicate} must contain retained evidence references")
        for index, ref in enumerate(evidence):
            _validate_evidence_ref(ref, predicate, index)

    custody = _dict_at(freeze, "p4_custody")
    _expect(custody.get("status") == "CLOSED / VERIFIED", "P4 custody must be CLOSED / VERIFIED")
    for field in (
        "key_commitment_sha256",
        "mapping_commitment_sha256",
        "custodian_attestation_sha256",
        "execution_no_access_attestation_sha256",
        "independent_custody_review_sha256",
    ):
        _expect_hex64(custody.get(field), f"p4_custody.{field}")
    _expect_nonempty(custody.get("custodian_id"), "p4_custody.custodian_id")
    _expect_nonempty(custody.get("execution_principal_id"), "p4_custody.execution_principal_id")
    _expect(
        custody.get("custodian_id") != custody.get("execution_principal_id"),
        "P4 custodian and execution principal must be distinct",
    )

    p8_verification = _validate_p8_verification_record(
        record_bytes=p8_verification_bytes,
        expected_record_sha256=expected_p8_verification_sha256,
        freeze_commit_sha=freeze_commit_sha,
        freeze_sha256=actual_sha256,
    )

    authorization = _dict_at(freeze, "pilot_authorization")
    _expect(authorization.get("status") == "NOT_GRANTED", "pilot authorization must still be NOT_GRANTED during P9")
    _expect(authorization.get("record_id") is None, "pilot authorization record_id must be null during P9")

    empirical = _dict_at(freeze, "empirical_execution")
    _expect(empirical.get("status") == "NOT_EXECUTED", "empirical execution must remain NOT_EXECUTED during P9")
    _expect(empirical.get("n") == 0, "empirical N must remain 0 during P9")

    unblinding = _dict_at(freeze, "unblinding")
    _expect(unblinding.get("status") == "NOT_EXECUTED", "unblinding must remain NOT_EXECUTED during P9")

    return {
        "schema_version": 1,
        "evidence_class": "PDMAL_P9_FINAL_FROZEN_CHAIN_VERIFICATION",
        "epistemic_scope": "FINAL_FROZEN_CHAIN_INTEGRITY_NOT_EFFICACY",
        "result": "PASS",
        "freeze_commit_sha": freeze_commit_sha,
        "freeze_sha256": actual_sha256,
        "p8_verification_commit_sha": p8_verification_commit_sha,
        "p8_verification_sha256": p8_verification["record_sha256"],
        "p8_verifier_id": p8_verification["verifier_id"],
        "accepted_control_plane_commit": accepted_control_plane,
        "candidate_sha": candidate_sha,
        "candidate_tree_sha": candidate_tree,
        "deployment_id": deployment_id,
        "p9_verifier_script_sha256": p9_verifier_script_sha256,
        "p9_workflow_sha256": p9_workflow_sha256,
        "p7_status": "CLOSED",
        "p4_status": "CLOSED / VERIFIED",
        "freeze_verification_status": "PASS",
        "pilot_authorization": "NOT_GRANTED",
        "empirical_n": 0,
        "unblinding": "NOT_EXECUTED",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--expected-freeze-sha256", required=True)
    parser.add_argument("--freeze-commit-sha", required=True)
    parser.add_argument("--p8-verification", required=True, type=Path)
    parser.add_argument("--expected-p8-verification-sha256", required=True)
    parser.add_argument("--p8-verification-commit-sha", required=True)
    parser.add_argument("--candidate-manifest", required=True, type=Path)
    parser.add_argument("--p7-binding", required=True, type=Path)
    parser.add_argument("--p9-verifier-script-sha256", required=True)
    parser.add_argument("--p9-workflow-sha256", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    try:
        result = validate_freeze(
            freeze_bytes=args.freeze.read_bytes(),
            expected_sha256=args.expected_freeze_sha256,
            p8_verification_bytes=args.p8_verification.read_bytes(),
            expected_p8_verification_sha256=args.expected_p8_verification_sha256,
            candidate_manifest=args.candidate_manifest,
            p7_binding=args.p7_binding,
            freeze_commit_sha=args.freeze_commit_sha,
            p8_verification_commit_sha=args.p8_verification_commit_sha,
            p9_verifier_script_sha256=args.p9_verifier_script_sha256,
            p9_workflow_sha256=args.p9_workflow_sha256,
        )
    except (OSError, VerificationError) as exc:
        print(f"P9 verification FAIL-CLOSED: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    sidecar = args.output.with_suffix(args.output.suffix + ".sha256")
    sidecar.write_text(hashlib.sha256(payload.encode("utf-8")).hexdigest() + "\n", encoding="utf-8")
    print("P9 final frozen-chain verification PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
