# AKDC Gate 9 — keyed capture commitments (synthetic research, 2026-10-26)

**State:** STACKED DRAFT / NO LIVE SDK / NO IDENTITY AUTHENTICATION / NO SCIENTIFIC N / NO RELEASE.

## Motive and bounded design

Gate 8 retained an unkeyed canonical-decoded frame SHA-256 and separately persisted a deterministic SHA-derived MCP request-correlation ID. Low-entropy source values could potentially be guessed offline, and repeated IDs could be correlated. This research experiment replaces the frame and event-identity fingerprints with domain-separated HMAC-SHA256 using an explicitly supplied `capture_key` (bytes, minimum length 32) and a public `key_id`. The lower-level `content_digest` over the minimized DGAF envelope remains plain SHA-256 and is not described as confidential.

Captured request/response JSON-RPC IDs are matched **before** retention; the output stores a constant inert `correlation-withheld`, not an unkeyed hash of the original request ID. The original bytes are not retained by the observation. The `capture_reference` now states `commitment_scheme=HMAC-SHA256-V1-RESEARCH` and the public key ID. The secret key itself must not be added to evidence or logs.

Two purpose-specific HMAC domains are `AKDC-FRAME-V1` and `AKDC-EVENT-V1`, computed over canonicalized *decoded JSON*; they do not claim raw HTTP byte integrity or verified sender identity. The event identity also incorporates the receiver's untrusted stream/receipt witness and key ID.

## Execution and falsification

The local reproducibility archive from the Gate 8 pinned-validator snapshot ran **90/90 unittest tests successfully, 0 skipped** with `ResourceWarning` promoted to error: the prior 80 tests and 10 new research tests for required key, weak/nonbytes/invalid IDs, determinism, key rotation, reference HMAC, raw correlation-ID omission, evidence tampering and A2A/MCP parity. Local content is not a byte-exact copy of the updated GitHub PR. The actual **exact-head CI must run separately** on all three Python versions, checking flake8, Black, isort, mypy and pytest, and the independent `pip-audit` remains unwaived.

Archive: `AKDC_Gate9_Keyed_Commitments_2026-10-26.zip`, SHA-256 `42e8884000e55ddf74dbe4b53c2f2f6246ca1195c2edf23a71c80512c220c9c5` (conversation attachment only, not a release). DGAF reference validator Git blob: `fab53669c69ea0b26bc9a55bce2ab157ac8f5348`.

## Security and scientific ceilings

- A key's 32-byte **length** does not establish its entropy, secrecy, origin, safe derivation, or rotation. Tests use a public fixture-only key. No KMS, vault, HSM, key recovery, rotation, revocation, identity attestation or key lifecycle has been implemented.
- HMAC only mitigates offline dictionary guessing while the input key remains secret; it does not encrypt or erase source content, and records still contain unverified provider/runtime/receiver metadata.
- Key or key-ID rotation changes locally derived event identity, potentially partitioning replay domains; prior deduplication must not be interpreted as continuity across key epochs.
- Existing `PRESENTED_NOT_GRANTED` / `RECORD_ONLY` classification remains non-authoritative. No live transport, full SDK conformance, distributed exactly-once execution, power-loss durability, full privacy certification, independent empirical result or scientific N increase.
- Distinct remediation tracks: [Black #1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [other dependency advisories #1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530). Do not waive the `pip-audit` failure to accept this research.

**Research ceiling:** `DGAF_V1_RELEASE=HOLD`; `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `HIGH_ASSURANCE=NOT_AUTHORIZED`. No production wiring, freeze changes, or use of unfrozen SYN-AUTH-01 #1508.
