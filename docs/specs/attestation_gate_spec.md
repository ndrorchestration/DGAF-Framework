# AttestationGate Interface Spec

**Phase:** 5 (stub delivered; LLM verifier Phase 5 upgrade)
**Module:** `pptl/attestation_gate.py`
**Status:** SCAFFOLD — stub verifier active; production verifier TBD

---

## Purpose

AttestationGate governs whether an agent's claimed output can be trusted
before it propagates downstream through the AlignmentGate. It enforces
the **claim–evidence–attestation** contract: every agent assertion that
affects governance state must carry verifiable evidence.

---

## Domain Model

```
AttestationRecord
  agent_id:  str          # who is making the claim
  claim:     str          # the assertion (e.g. "output is hallucination-free")
  evidence:  str          # supporting evidence (source refs, cross-checks)
  timestamp: float        # unix epoch (auto)
  signature: str          # sha256[:16] of payload (auto)
  fingerprint: str        # content-stable ID (property)

AttestationResult
  record_id:   str                # uuid4
  status:      AttestationStatus  # ATTESTED | REJECTED | PENDING | REVOKED
  reason:      str
  attested_at: float
  passed:      bool               # property, True iff ATTESTED
```

---

## Interface Contract

| Method | Signature | Returns | Side effects |
|---|---|---|---|
| `attest` | `(record: AttestationRecord) -> AttestationResult` | result with status | stores record + result, appends audit log |
| `verify` | `(record_id: str) -> AttestationRecord \| None` | record or None | None if REVOKED or unknown |
| `get_result` | `(record_id: str) -> AttestationResult \| None` | result or None | read-only |
| `revoke` | `(record_id: str) -> bool` | True if revoked | updates result to REVOKED, appends audit log |
| `audit_log` | `() -> list[AttestationResult]` | snapshot copy | read-only |
| `stats` | `() -> dict` | counts by status | read-only |

---

## Status Lifecycle

```
             attest()          revoke()
NEW ──────► PENDING ──────► ATTESTED ──────► REVOKED
                    └──────► REJECTED
```

> **Note:** Current stub skips PENDING — records go directly to
> ATTESTED or REJECTED. Phase 5 async verifier will use PENDING
> while the LLM evaluation is in flight.

---

## Integration: AlignmentGate

```python
# co_orchestration_schema.py — recommended integration point
from pptl.attestation_gate import AttestationGate, AttestationRecord

class AlignmentGate:
    def __init__(self, ..., attestation_gate: AttestationGate | None = None):
        self._attest = attestation_gate

    def evaluate(self, agent_id: str, output: str, evidence: str) -> bool:
        if self._attest:
            record = AttestationRecord(
                agent_id=agent_id,
                claim=output,
                evidence=evidence,
            )
            result = self._attest.attest(record)
            if not result.passed:
                return False  # block downstream regardless of alignment score
        return self._alignment_score(...) >= self.threshold
```

---

## Phase 5 Upgrade Path

Replace `_default_stub_verifier` with a real verifier:

```python
def llm_evidence_verifier(record: AttestationRecord) -> tuple[bool, str]:
    # Call LLM with record.claim + record.evidence
    # Return (True, rationale) or (False, rejection_reason)
    ...

gate = AttestationGate(evidence_verifier=llm_evidence_verifier)
```

No other interface changes required. All C2-004 tests pass unchanged.

---

## Tradeoffs

| Concern | Decision |
|---|---|  
| Sync vs async attest | Sync stub now; async Phase 5 (PENDING state pre-wired) |
| Signature scheme | SHA-256 truncated — not cryptographic, trace-only |
| Audit log eviction | FIFO ring buffer (default 1000) — adjust for production |
| LLM verifier coupling | Zero coupling in stub — injected via constructor |
