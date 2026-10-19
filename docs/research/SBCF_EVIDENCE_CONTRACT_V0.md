# SBCF Evidence Reconciliation Contract v0 (synthetic)

Status: DRAFT / FAIL-CLOSED / NOT AUTHORIZED. No live enforcement or cryptographically authenticated source identity.

The `attestation.py` prototype requires all enumerated sources, rejects duplicates and unexpected sources, requires minimum revision, checks agreement on five state dimensions and demands a restrictive regime. Source names and revisions are caller-provided strings and numbers: **not proof of independent provenance**. Freshness by revision is weaker than timestamped signed evidence with nonce and trusted source registry.

## Required real-world upgrade gates
1. Trust-root identity binding: registered independent, mutually authenticated observation service (not agent-controlled).
2. Source-specific projections: no assumption that worker registry and capability broker can each truthfully attest every dimension. Define per-source authority by field.
3. Anti-replay: signed nonce, monotonically increasing per-source sequence, trusted clock / TTL, exact policy+run+source identity.
4. Independent tamper-evident evidence sink, cryptographic chain head external to the agent and policy engine.
5. Atomic / bounded-staleness observation of credentials, workers, pending queues and actual network policy; explicit UNKNOWN on incomplete scope.
6. Fault injection: dropped, stale, duplicated, contradictory, forged, swapped-source and split-brain records, with fail-closed outcomes.
7. Independent reviewer reproducibility and raw evidence retention before certification.

The current QA only establishes behavior of a deterministic synthetic predicate, and cannot be used to certify real quarantine.
