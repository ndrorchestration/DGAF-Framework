import hashlib

from components.evidence_gate import (
    AUTHORIZATION_EFFECT_NONE,
    ClaimScope,
    EvidenceAdmissionReason,
    EvidenceObject,
    EvidenceTarget,
    ProvenanceBinding,
    admit_evidence,
)


BYTES = b'{"result":"pass"}\n'
DIGEST = hashlib.sha256(BYTES).hexdigest()


def evidence(**overrides):
    values = {
        "evidence_id": "ev-1",
        "evidence_type": "test-result",
        "digest_algorithm": "sha256",
        "content_digest": DIGEST,
        "source_class": "LOCAL_TEST",
        "observed_at": "2026-10-01T12:00:00Z",
    }
    values.update(overrides)
    return EvidenceObject(**values)


def target(**overrides):
    values = {
        "target_type": "source_revision",
        "target_id": "abc123",
        "scope_id": "unit-test:test_widget",
        "source_revision": "abc123",
        "environment_identity": "python-3.12",
    }
    values.update(overrides)
    return EvidenceTarget(**values)


def provenance(**overrides):
    values = {
        "producer_class": "LOCAL_TEST",
        "custody_class": "SAME_SYSTEM",
        "source_identity": "abc123",
        "runtime_identity": "pytest",
        "environment_identity": "python-3.12",
    }
    values.update(overrides)
    return ProvenanceBinding(**values)


def claim(**overrides):
    values = {
        "claim_id": "claim-1",
        "claim_class": "deterministic-test",
        "scope_id": "unit-test:test_widget",
        "evidence_class": "TESTED",
        "limitations": ("local deterministic test only",),
        "excluded_claims": ("production_ready", "independently_validated"),
    }
    values.update(overrides)
    return ClaimScope(**values)


def admit(**kwargs):
    return admit_evidence(
        kwargs.pop("evidence", evidence()),
        kwargs.pop("target", target()),
        kwargs.pop("provenance", provenance()),
        kwargs.pop("claim_scope", claim()),
        evidence_bytes=kwargs.pop("evidence_bytes", BYTES),
        expected_target=kwargs.pop("expected_target", target()),
        required_producer_class=kwargs.pop("required_producer_class", "LOCAL_TEST"),
        **kwargs,
    )


def test_exact_evidence_admits_without_authorization_effect():
    receipt = admit()
    assert receipt.admitted is True
    assert receipt.reason_code is EvidenceAdmissionReason.ADMITTED
    assert receipt.verified_digest == DIGEST
    assert receipt.authorization_effect == AUTHORIZATION_EFFECT_NONE
    assert receipt.digest_checked is True
    assert receipt.target_checked is True
    assert receipt.environment_checked is True
    assert receipt.provenance_checked is True
    assert receipt.claim_scope_checked is True
    assert receipt.claim_ceiling == ("production_ready", "independently_validated")


def test_missing_bytes_are_not_evidence_acceptance():
    receipt = admit(evidence_bytes=None)
    assert receipt.admitted is False
    assert receipt.reason_code is EvidenceAdmissionReason.EVIDENCE_MISSING_OR_INVALID
    assert receipt.digest_checked is False


def test_digest_drift_fails_closed():
    receipt = admit(evidence_bytes=b"different")
    assert receipt.admitted is False
    assert receipt.reason_code is EvidenceAdmissionReason.DIGEST_MISMATCH
    assert receipt.digest_checked is True


def test_scope_mismatch_fails_as_target_identity_mismatch():
    expected = target(scope_id="integration:test_widget")
    receipt = admit(expected_target=expected)
    assert receipt.reason_code is EvidenceAdmissionReason.TARGET_IDENTITY_MISMATCH


def test_source_revision_mismatch_fails_closed():
    expected = target(source_revision="def456")
    receipt = admit(expected_target=expected)
    assert receipt.reason_code is EvidenceAdmissionReason.SOURCE_IDENTITY_MISMATCH
    assert receipt.source_checked is True


def test_environment_mismatch_fails_closed():
    expected = target(environment_identity="python-3.13")
    receipt = admit(expected_target=expected)
    assert receipt.reason_code is EvidenceAdmissionReason.ENVIRONMENT_IDENTITY_MISMATCH
    assert receipt.environment_checked is True


def test_provenance_class_mismatch_fails_closed():
    receipt = admit(required_producer_class="GITHUB_ACTIONS")
    assert receipt.reason_code is EvidenceAdmissionReason.PROVENANCE_CLASS_MISMATCH
    assert receipt.provenance_checked is True


def test_required_receipt_check_failure_fails_closed():
    receipt = admit(receipt_checker=lambda e, t, p, c: False)
    assert receipt.reason_code is EvidenceAdmissionReason.RECEIPT_MISMATCH
    assert receipt.receipt_checked is True


def test_required_manifest_check_failure_fails_closed():
    receipt = admit(manifest_checker=lambda e, t, p, c: False)
    assert receipt.reason_code is EvidenceAdmissionReason.MANIFEST_MISMATCH
    assert receipt.manifest_checked is True


def test_content_set_check_failure_fails_closed():
    receipt = admit(content_set_checker=lambda e, t, p, c: False)
    assert receipt.reason_code is EvidenceAdmissionReason.CONTENT_SET_MISMATCH
    assert receipt.content_set_checked is True


def test_custody_check_failure_fails_closed():
    receipt = admit(custody_checker=lambda e, t, p, c: False)
    assert receipt.reason_code is EvidenceAdmissionReason.CUSTODY_REQUIREMENT_UNSATISFIED
    assert receipt.custody_checked is True


def test_claim_scope_checker_can_block_overbroad_claim():
    receipt = admit(claim_scope_checker=lambda e, t, p, c: False)
    assert receipt.reason_code is EvidenceAdmissionReason.CLAIM_SCOPE_EXCEEDS_EVIDENCE
    assert receipt.claim_scope_checked is True


def test_claim_scope_must_match_target_scope():
    receipt = admit(
        claim_scope=claim(scope_id="system-wide"),
        claim_scope_checker=lambda e, t, p, c: True,
    )
    assert receipt.reason_code is EvidenceAdmissionReason.CLAIM_SCOPE_EXCEEDS_EVIDENCE


def test_changed_target_requires_explicit_transfer():
    receipt = admit(expected_target=target(target_id="def456", source_revision=None))
    assert receipt.reason_code is EvidenceAdmissionReason.HISTORICAL_TRANSFER_NOT_ESTABLISHED
    assert receipt.historical_transfer_checked is True


def test_explicit_transfer_can_continue_but_source_checks_still_apply():
    expected = target(target_id="def456", source_revision=None)
    receipt = admit(
        expected_target=expected,
        historical_transfer_checker=lambda old, new, e, p, c: True,
    )
    assert receipt.admitted is True
    assert receipt.historical_transfer_checked is True


def test_checker_exception_fails_closed():
    def broken(e, t, p, c):
        raise RuntimeError("unavailable")

    receipt = admit(receipt_checker=broken)
    assert receipt.admitted is False
    assert receipt.reason_code is EvidenceAdmissionReason.RECEIPT_MISMATCH
    assert receipt.receipt_checked is True


def test_unperformed_optional_checks_remain_false():
    receipt = admit()
    assert receipt.receipt_checked is False
    assert receipt.manifest_checked is False
    assert receipt.content_set_checked is False
    assert receipt.custody_checked is False
