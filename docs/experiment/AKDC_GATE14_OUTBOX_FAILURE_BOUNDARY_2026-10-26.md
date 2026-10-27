# AKDC Gate 14 — Local transactional outbox and external-effect crash falsification

**State:** STACKED DRAFT / NONRELEASE / LOCAL SYNTHETIC TESTS / NO AUTHENTICATED PRINCIPAL / NO SCIENTIFIC N.

## Grounded starting point

Gate 13's official MCP v2.4.0 in-process SDK test proved an atomic single receipt across concurrent synthetic retries, including crashes and reopening. It did not execute effects. Gate 14 builds a separate **SQLite-only** outbox experiment around that missing receipt-to-effect boundary. The source remains in `experiments/akdc/mrtr_outbox_research.py` and must not be wired to protected DGAF CommitGate or consequential actions.

## Explicitly falsifiable design

A SQLite transaction atomically inserts both a receipt and its pending outbox row. A separate `dispatch_one` atomically records a **synthetic marker in the same SQLite database** and changes both receipt/outbox status to APPLIED. Race and abrupt process-death injections test the behavior before and after each COMMIT. The sink option deliberately appends a harmless marker to an **external test file**, with `fsync` and immediate crash *before SQLite commit*. The SQLite transaction rolls back, but the appended marker remains; replay writes the marker a **second time**. This is the expected negative control proving local DB atomicity cannot establish exactly-once external effects.

The experiment requires a caller-supplied 32+ byte HMAC key and accepts only a fixture-specific action label, synthetic nonce, bounded asserted principal and SHA-256-shaped operation digest. Neither the synthetic identity claim nor the HMAC key establishes authenticated principal, signing-key secrecy, trusted delegation, epoch continuity or authorization. Schema version, column shape, CHECK and foreign-key checks fail closed on missing/weakened database contracts. WAL/FULL durability does not prove behavior under arbitrary power failures or network filesystems.

## Evidence (strictly scoped)

An isolated local Python 3.13 unittest suite passed **18/18 tests, zero skipped**, including warning-as-error cleanup. Tests include 32 threads, 8 independent processes, malformed claims, binding collisions, key epoch weakness, DB schema corruption, crash-before/after enqueue/dispatch commits, single persisted local effect, and the reproducible **two-file-appends** counterexample. This local result does NOT establish exact-head GitHub Actions Python 3.10/3.11/3.12 CI, whose code-quality and non-waived security gates must be observed separately.

The new source and tests are included in the repository's existing **hash-locked, research-only Python quality workflow**. Existing dependency advisories tracked under [#1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [#1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530) remain blockers; no waiver or manual hash edit. This Gate 14 Python experiment does **not** add a new authenticated official SDK run; the real SDK Gate 13 result remains separately pinned evidence.

## Non-promotion, recovery and next gate

Receipt/outbox/local-marker atomicity is not exactly-once delivery or effect. The actual external sink test demonstrates **at-least-once can duplicate** after a crash before acknowledgment; a production design needs a trusted principal and policy-bound operation ID, an independently idempotent downstream consumer (or other distributed coordination/compensation policy), revocation, key-epoch continuity, crash/split-brain recovery, monitored redrive and independent review. `SYN-AUTH-01` benchmark and scientific samples remain untouched.

**Ceilings:** `DGAF_V1_RELEASE=HOLD`; `SCIENTIFIC_N_INCREMENT=0`; `HIGH_ASSURANCE=NOT_AUTHORIZED`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`. All research PRs remain DRAFT/UNMERGED; protected `main` and production governance unchanged. Related replay issue [#1536](https://github.com/ndrorchestration/DGAF-Framework/issues/1536) stays OPEN.
