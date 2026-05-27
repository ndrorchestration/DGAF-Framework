"""C2-004 — AttestationGate unit tests.

Markers: attestation
Gate: Phase 5 (AttestationGate impl)
Status: UNLOCKED — impl delivered in pptl/attestation_gate.py
"""
import time
import pytest

from pptl.attestation_gate import (
    AttestationGate,
    AttestationRecord,
    AttestationResult,
    AttestationStatus,
    _default_stub_verifier,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def gate():
    return AttestationGate()


def _record(claim="output is compliant", evidence="3/3 sources confirmed", agent="sentinel"):
    return AttestationRecord(agent_id=agent, claim=claim, evidence=evidence)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.attestation
def test_attest_valid_record_returns_attested(gate):
    result = gate.attest(_record())
    assert result.status == AttestationStatus.ATTESTED
    assert result.passed is True
    assert result.record_id


@pytest.mark.attestation
def test_attest_empty_claim_returns_rejected(gate):
    result = gate.attest(_record(claim=""))
    assert result.status == AttestationStatus.REJECTED
    assert result.passed is False
    assert "empty" in result.reason


@pytest.mark.attestation
def test_attest_empty_evidence_returns_rejected(gate):
    result = gate.attest(_record(evidence=""))
    assert result.status == AttestationStatus.REJECTED
    assert "empty" in result.reason


@pytest.mark.attestation
def test_attest_short_evidence_rejected(gate):
    result = gate.attest(_record(evidence="abc"))
    assert result.status == AttestationStatus.REJECTED
    assert "short" in result.reason


@pytest.mark.attestation
def test_verify_attested_record_returns_record(gate):
    result = gate.attest(_record())
    record = gate.verify(result.record_id)
    assert record is not None
    assert record.agent_id == "sentinel"


@pytest.mark.attestation
def test_verify_unknown_id_returns_none(gate):
    assert gate.verify("nonexistent-id-00000") is None


@pytest.mark.attestation
def test_revoke_attested_record(gate):
    result = gate.attest(_record())
    assert gate.revoke(result.record_id) is True
    assert gate.verify(result.record_id) is None
    r = gate.get_result(result.record_id)
    assert r.status == AttestationStatus.REVOKED


@pytest.mark.attestation
def test_revoke_unknown_id_returns_false(gate):
    assert gate.revoke("bad-id-999") is False


@pytest.mark.attestation
def test_revoke_rejected_record_returns_false(gate):
    result = gate.attest(_record(claim=""))
    assert result.status == AttestationStatus.REJECTED
    assert gate.revoke(result.record_id) is False


@pytest.mark.attestation
def test_audit_log_grows_with_operations(gate):
    gate.attest(_record())
    gate.attest(_record(claim="second claim", evidence="evidence data here"))
    log = gate.audit_log()
    assert len(log) == 2
    assert all(isinstance(r, AttestationResult) for r in log)


@pytest.mark.attestation
def test_stats_reflects_all_states(gate):
    r1 = gate.attest(_record())
    gate.attest(_record(claim=""))          # rejected
    gate.revoke(r1.record_id)
    s = gate.stats()
    assert s["total"] == 2
    assert s["revoked"] == 1
    assert s["rejected"] == 1
    assert s["attested"] == 0


@pytest.mark.attestation
def test_custom_verifier_is_used(gate):
    def always_reject(record):
        return False, "policy: all claims rejected in test mode"
    g = AttestationGate(evidence_verifier=always_reject)
    result = g.attest(_record())
    assert result.status == AttestationStatus.REJECTED
    assert "test mode" in result.reason


@pytest.mark.attestation
def test_record_signature_is_stable():
    r = AttestationRecord(agent_id="a", claim="c", evidence="e" * 10, timestamp=1000.0)
    r2 = AttestationRecord(agent_id="a", claim="c", evidence="e" * 10, timestamp=1000.0)
    assert r.signature == r2.signature


@pytest.mark.attestation
def test_audit_log_fifo_eviction():
    g = AttestationGate(max_audit_log=3)
    for i in range(5):
        g.attest(_record(claim=f"claim {i}", evidence=f"evidence {i} here"))
    assert len(g.audit_log()) == 3
