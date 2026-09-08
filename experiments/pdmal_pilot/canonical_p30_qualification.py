"""Canonical P-30 step-8 qualification verification for PDMAL candidate profiles.

This module deliberately does not score 11Q and does not estimate confidence.
It verifies an already-produced external qualification artifact against an exact
profile identity, exact profile-source SHA, and externally supplied artifact
SHA-256. It is non-empirical infrastructure.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Callable

PROFILE_ID = "DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1"
RECORD_TYPE = "DGAF_P30_11Q_PROFILE_QUALIFICATION"
RUBRIC = "P-11 11Q Attestation Scoring"
ALLOWED_VERIFICATION_CLASSES = {
    "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT",
    "INDEPENDENT_VERIFIED",
}
FORBIDDEN_KEYS = {
    "empirical_outcomes",
    "ffcr",
    "agent_values",
    "topology",
    "failure_count",
    "runtime_confidence_scalar",
    "default_constant",
    "phi_constant",
    "synthetic_confidence_fixture",
}


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_KEYS or _contains_forbidden_key(child):
                return True
    elif isinstance(value, list):
        return any(_contains_forbidden_key(item) for item in value)
    return False


def verify_qualification_artifact(
    artifact_bytes: bytes,
    *,
    expected_sha256: str,
    expected_profile_id: str,
    expected_profile_source_sha: str,
) -> bool:
    """Return True only for an exact, qualifying, source-bound P-30 artifact."""
    if not artifact_bytes or len(expected_sha256) != 64 or len(expected_profile_source_sha) != 40:
        return False
    if hashlib.sha256(artifact_bytes).hexdigest() != expected_sha256.lower():
        return False
    try:
        data = json.loads(artifact_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    if not isinstance(data, dict) or _contains_forbidden_key(data):
        return False
    if data.get("record_type") != RECORD_TYPE or data.get("schema_version") != 1:
        return False
    if data.get("attestation_gate") != "P-30" or data.get("rubric") != RUBRIC:
        return False
    if data.get("profile_id") != expected_profile_id:
        return False
    if data.get("profile_source_sha") != expected_profile_source_sha:
        return False
    if data.get("verification_class") not in ALLOWED_VERIFICATION_CLASSES:
        return False

    scoring = data.get("scoring_summary")
    if not isinstance(scoring, dict):
        return False
    try:
        percentage = float(scoring["percentage"])
        q11 = int(scoring["q11_score"])
        open_blg_count = int(scoring.get("open_blg_count", 0))
    except (KeyError, TypeError, ValueError):
        return False
    tier = scoring.get("tier")
    result = scoring.get("attestation_result")

    s_pass = tier == "S-TIER" and percentage >= 95.0 and q11 >= 9 and result == "GRANTED"
    a_pass = (
        tier == "A-TIER"
        and percentage >= 85.0
        and result == "CONDITIONAL"
        and open_blg_count > 0
    )
    return s_pass or a_pass


def build_qualification_verifier_hook(
    artifact_bytes: bytes,
    *,
    expected_sha256: str,
    expected_profile_id: str,
    expected_profile_source_sha: str,
) -> Callable[[str, dict], str]:
    """Build a TGL-compatible step-8 hook returning PASS or KILL only."""

    def _hook(input_text: str, context: dict) -> str:
        del input_text, context
        return (
            "PASS"
            if verify_qualification_artifact(
                artifact_bytes,
                expected_sha256=expected_sha256,
                expected_profile_id=expected_profile_id,
                expected_profile_source_sha=expected_profile_source_sha,
            )
            else "KILL"
        )

    return _hook
