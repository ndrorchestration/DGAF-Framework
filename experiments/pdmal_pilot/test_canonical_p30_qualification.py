from __future__ import annotations

import hashlib
import json

from canonical_p30_qualification import (
    PROFILE_ID,
    build_qualification_verifier_hook,
    verify_qualification_artifact,
)

SOURCE_SHA = "a" * 40


def _artifact(**overrides):
    data = {
        "record_type": "DGAF_P30_11Q_PROFILE_QUALIFICATION",
        "schema_version": 1,
        "attestation_gate": "P-30",
        "rubric": "P-11 11Q Attestation Scoring",
        "profile_id": PROFILE_ID,
        "profile_source_sha": SOURCE_SHA,
        "verification_class": "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT",
        "scoring_summary": {
            "percentage": 96.0,
            "tier": "S-TIER",
            "q11_score": 9,
            "open_blg_count": 0,
            "attestation_result": "GRANTED",
        },
    }
    for key, value in overrides.items():
        if key.startswith("scoring__"):
            data["scoring_summary"][key.removeprefix("scoring__")] = value
        else:
            data[key] = value
    raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return raw, hashlib.sha256(raw).hexdigest()


def _verify(raw, digest, **kwargs):
    return verify_qualification_artifact(
        raw,
        expected_sha256=kwargs.get("expected_sha256", digest),
        expected_profile_id=kwargs.get("expected_profile_id", PROFILE_ID),
        expected_profile_source_sha=kwargs.get("expected_profile_source_sha", SOURCE_SHA),
    )


def test_accepts_source_bound_s_tier_developer_self_attestation():
    raw, digest = _artifact()
    assert _verify(raw, digest)
    hook = build_qualification_verifier_hook(
        raw,
        expected_sha256=digest,
        expected_profile_id=PROFILE_ID,
        expected_profile_source_sha=SOURCE_SHA,
    )
    assert hook("ignored", {"ffcr": 1.0}) == "PASS"


def test_accepts_a_tier_conditional_with_open_blg():
    raw, digest = _artifact(
        scoring__percentage=90.0,
        scoring__tier="A-TIER",
        scoring__q11_score=8,
        scoring__open_blg_count=1,
        scoring__attestation_result="CONDITIONAL",
    )
    assert _verify(raw, digest)


def test_rejects_digest_profile_and_source_drift():
    raw, digest = _artifact()
    assert not _verify(raw, digest, expected_sha256="0" * 64)
    assert not _verify(raw, digest, expected_profile_id="OTHER")
    assert not _verify(raw, digest, expected_profile_source_sha="b" * 40)
    assert not _verify(raw, digest, expected_sha256="G" * 64)
    assert not _verify(raw, digest, expected_profile_source_sha="Z" * 40)


def test_rejects_malformed_and_nonqualifying_evidence():
    assert not _verify(b"not-json", hashlib.sha256(b"not-json").hexdigest())
    raw, digest = _artifact(scoring__percentage=94.9)
    assert not _verify(raw, digest)
    raw, digest = _artifact(scoring__q11_score=8)
    assert not _verify(raw, digest)
    raw, digest = _artifact(scoring__attestation_result="CONDITIONAL")
    assert not _verify(raw, digest)


def test_rejects_a_tier_without_open_blg():
    raw, digest = _artifact(
        scoring__percentage=90.0,
        scoring__tier="A-TIER",
        scoring__q11_score=9,
        scoring__open_blg_count=0,
        scoring__attestation_result="CONDITIONAL",
    )
    assert not _verify(raw, digest)


def test_rejects_wrong_authority_or_unsupported_verification_class():
    raw, digest = _artifact(attestation_gate="LEGACY")
    assert not _verify(raw, digest)
    raw, digest = _artifact(verification_class="SELF_ASSERTED_INDEPENDENT")
    assert not _verify(raw, digest)
    raw, digest = _artifact(verification_class="INDEPENDENT_VERIFIED")
    assert not _verify(raw, digest)


def test_rejects_forbidden_scientific_or_scalar_inputs_anywhere():
    for key in (
        "empirical_outcomes",
        "ffcr",
        "agent_values",
        "topology",
        "failure_count",
        "runtime_confidence_scalar",
        "default_constant",
        "phi_constant",
        "synthetic_confidence_fixture",
    ):
        raw, digest = _artifact(extra={key: 0})
        assert not _verify(raw, digest), key


def test_hook_fails_closed_on_invalid_artifact():
    raw, digest = _artifact(profile_id="WRONG")
    hook = build_qualification_verifier_hook(
        raw,
        expected_sha256=digest,
        expected_profile_id=PROFILE_ID,
        expected_profile_source_sha=SOURCE_SHA,
    )
    assert hook("ignored", {}) == "KILL"
