# AKDC Gate 13 — Atomic MRTR receipt research (2026-10-26)

**Status:** Stacked draft research only. No authenticated principal, no real-world effect, no scientific N or release permission.

## Baseline and bounded implementation

Gate 12 verified with official MCP TypeScript SDK v2.4.0 that tampered HMAC-sealed requestState is refused before handler execution but an unchanged valid signed requestState can be replayed. Gate 13 explores a **separate receipt registry** for application-level deduplication: `experiments/akdc/mrtr_receipt_ledger_research.py` uses SQLite BEGIN IMMEDIATE, WAL, synchronous=FULL and version/schema verification. A first matching verified fixture retry stores a fixed `RECORD_ONLY / SYNTHETIC_COMPLETE` receipt, further identical attempts return `DUPLICATE_RECORDED`, and the same nonce under a different binding is refused.

Token nonces and claimed principal/action/operation identities are represented by domain-separated HMAC-SHA256 tags, keyed by a caller-supplied secret. The principal remains **only a synthetic caller claim**; this is not identity authentication or encrypted storage. The SDK test uses a fresh ephemeral key and no real user data or external network endpoint.

## Experiments and regression design

Fourteen dedicated Python tests cover 32 threads and eight independent processes racing to record the same fixture nonce, crash before commit (no receipt), crash after commit (receipt survives reopen), rebinding denial, malformed requests, weakened/unversioned schema rejection, hashed-data nonretention, and key-rotation failure to maintain replay identity. All tests must pass independently on the exact research branch; a newly opened PR or local intuition is not acceptance evidence.

The separate official SDK in-process probe uses a signed multi-round-trip state token and a synthetic confirmation. It runs initial input_required, tampered-state error, two valid sequential retries, and four concurrent retries. The six valid retry handlers call separate Python processes against one SQLite file. Expected result: **one FIRST_RECORDED, five DUPLICATE_RECORDED, one persisted receipt**, plus eight SDK-generated JSON-RPC frame pairs. The Python verifier must independently normalize those eight captures into DGAF record-only evidence and confirm no synthetic state/form/tool-result content is retained in normalized records.

CI reuses the SHA-enforced, hosted-frozen Gate 11 15-entry npm lock (`aebc3f74fedec3a5d3927d992609a6a3a1dc1460d456f561f186e47c45646afd`) with npm ci and separate non-waived npm audit. The Python quality workflow is separately subject to pre-existing locked CI dependency advisories [#1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [#1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530).

## Claims not established

- A record receipt is not an executed effect or an exactly-once effect guarantee. Crashes around real external execution need a transactional outbox/idempotent effect endpoint plus recovery and compensation contracts.
- Local shared-file SQLite locks do not prove cross-host distributed consensus, power-failure durability on arbitrary filesystems, or multi-region availability.
- A changed receipt-key epoch changes nonce HMAC tags and can admit the same valid token under a new identity (negative control).
- SDK-signed state is not client or principal authentication. The consent response is synthetic and cannot authorize an actual tool.
- No real transport TLS, multi-tenant secrets, revocation, official A2A SDK, independent validation, release or production governance integration.

**Research gating:** Exact-head CI and its SHA-referenced artifacts must be inspected before declaring engineering pass. Tracked need: [#1536](https://github.com/ndrorchestration/DGAF-Framework/issues/1536). `DGAF_V1_RELEASE=HOLD`; `SCIENTIFIC_N_INCREMENT=0`; `HIGH_ASSURANCE=NOT_AUTHORIZED`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`. Stacked PR [#1538](https://github.com/ndrorchestration/DGAF-Framework/pull/1538) remains DRAFT/unmerged; protected main and SYN-AUTH-01 #1508 untouched.