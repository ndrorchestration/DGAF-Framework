"""AttestationGate — Phase 5 scaffold.

Provides cryptographic-style claim attestation for agent outputs within
the PPTL governance pipeline. In Phase 5 stub mode, evidence verification
is a configurable policy function rather than a live LLM call — swap in
a real verifier by passing ``evidence_verifier`` at construction time.

Integration point:
    AlignmentGate (co_orchestration_schema.py) should call
    ``gate.attest(record)`` before emitting PASS; REJECTED or REVOKED
    records must block downstream Opportunity.mark_done().
"""
from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# Domain enums & value objects
# ---------------------------------------------------------------------------

class AttestationStatus(str, Enum):
    ATTESTED = "ATTESTED"
    REJECTED = "REJECTED"
    PENDING  = "PENDING"
    REVOKED  = "REVOKED"


@dataclass
class AttestationRecord:
    """Immutable claim submitted by an agent for attestation."""
    agent_id:  str
    claim:     str
    evidence:  str
    timestamp: float = field(default_factory=time.time)
    signature: str   = field(default="")

    def __post_init__(self) -> None:
        if not self.signature:
            self.signature = self._compute_signature()

    def _compute_signature(self) -> str:
        payload = f"{self.agent_id}|{self.claim}|{self.evidence}|{self.timestamp:.6f}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    @property
    def fingerprint(self) -> str:
        """Stable ID derived from claim content (not timestamp)."""
        payload = f"{self.agent_id}|{self.claim}|{self.evidence}"
        return hashlib.sha256(payload.encode()).hexdigest()[:24]


@dataclass
class AttestationResult:
    record_id:   str
    status:      AttestationStatus
    reason:      str
    attested_at: float = field(default_factory=time.time)

    @property
    def passed(self) -> bool:
        return self.status == AttestationStatus.ATTESTED

    def to_dict(self) -> dict:
        return {
            "record_id":   self.record_id,
            "status":      self.status.value,
            "reason":      self.reason,
            "attested_at": self.attested_at,
        }


# ---------------------------------------------------------------------------
# Default stub verifier — replace in Phase 5 with LLM-backed verifier
# ---------------------------------------------------------------------------

def _default_stub_verifier(record: AttestationRecord) -> tuple[bool, str]:
    """Stub policy: accept any non-empty claim with non-empty evidence.

    Phase 5 replacement: call an LLM or rules engine with record.claim
    and record.evidence; return (True, reason) or (False, rejection_reason).
    """
    if not record.claim.strip():
        return False, "claim is empty"
    if not record.evidence.strip():
        return False, "evidence is empty"
    if len(record.evidence) < 8:
        return False, "evidence too short (min 8 chars)"
    return True, "stub: claim and evidence present"


# ---------------------------------------------------------------------------
# AttestationGate
# ---------------------------------------------------------------------------

class AttestationGate:
    """Govern agent claim attestation within the PPTL orchestration pipeline.

    Args:
        evidence_verifier: Callable[[AttestationRecord], tuple[bool, str]].
            Defaults to _default_stub_verifier. Swap for Phase 5 LLM verifier.
        max_audit_log: Maximum audit log entries before FIFO eviction.

    Example::

        gate = AttestationGate()
        record = AttestationRecord(
            agent_id="sentinel",
            claim="output is hallucination-free",
            evidence="cross-ref: 3/3 sources confirmed",
        )
        result = gate.attest(record)
        assert result.passed
        assert gate.verify(result.record_id) is not None
    """

    def __init__(
        self,
        evidence_verifier: Optional[Callable] = None,
        max_audit_log: int = 1000,
    ) -> None:
        self._verifier: Callable = evidence_verifier or _default_stub_verifier
        self._max_audit: int = max_audit_log
        self._store:     Dict[str, AttestationRecord] = {}
        self._results:   Dict[str, AttestationResult] = {}
        self._audit:     List[AttestationResult]      = []

    # ------------------------------------------------------------------
    # Core interface
    # ------------------------------------------------------------------

    def attest(self, record: AttestationRecord) -> AttestationResult:
        """Evaluate a claim and store the result."""
        record_id = str(uuid.uuid4())
        passed, reason = self._verifier(record)
        status = AttestationStatus.ATTESTED if passed else AttestationStatus.REJECTED
        result = AttestationResult(record_id=record_id, status=status, reason=reason)
        self._store[record_id]   = record
        self._results[record_id] = result
        self._append_audit(result)
        return result

    def verify(self, record_id: str) -> Optional[AttestationRecord]:
        """Return the stored record if it exists and is not REVOKED."""
        result = self._results.get(record_id)
        if result is None:
            return None
        if result.status == AttestationStatus.REVOKED:
            return None
        return self._store.get(record_id)

    def get_result(self, record_id: str) -> Optional[AttestationResult]:
        """Return the AttestationResult for a given record_id."""
        return self._results.get(record_id)

    def revoke(self, record_id: str) -> bool:
        """Revoke a previously ATTESTED record. Returns True if revoked."""
        result = self._results.get(record_id)
        if result is None:
            return False
        if result.status not in (AttestationStatus.ATTESTED, AttestationStatus.PENDING):
            return False
        revoked = AttestationResult(
            record_id=record_id,
            status=AttestationStatus.REVOKED,
            reason="revoked by orchestrator",
        )
        self._results[record_id] = revoked
        self._append_audit(revoked)
        return True

    def audit_log(self) -> List[AttestationResult]:
        """Return full audit log (immutable snapshot)."""
        return list(self._audit)

    def pending_count(self) -> int:
        """Count records in PENDING status."""
        return sum(
            1 for r in self._results.values()
            if r.status == AttestationStatus.PENDING
        )

    def attested_count(self) -> int:
        return sum(
            1 for r in self._results.values()
            if r.status == AttestationStatus.ATTESTED
        )

    def rejected_count(self) -> int:
        return sum(
            1 for r in self._results.values()
            if r.status == AttestationStatus.REJECTED
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _append_audit(self, result: AttestationResult) -> None:
        self._audit.append(result)
        if len(self._audit) > self._max_audit:
            self._audit = self._audit[-self._max_audit:]

    def stats(self) -> dict:
        return {
            "total":    len(self._results),
            "attested": self.attested_count(),
            "rejected": self.rejected_count(),
            "pending":  self.pending_count(),
            "revoked":  sum(
                1 for r in self._results.values()
                if r.status == AttestationStatus.REVOKED
            ),
        }

    def __repr__(self) -> str:
        s = self.stats()
        return (
            f"AttestationGate(total={s['total']}, attested={s['attested']}, "
            f"rejected={s['rejected']}, revoked={s['revoked']})"
        )
