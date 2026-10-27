# AKDC Gate 15 — Separately committed idempotent receiver research (2026-10-27)

**State:** STACKED DRAFT / SYNTHETIC LOCAL SQLITE-ONLY CONSUMER / NO AUTHORITY, REAL EFFECT, TRANSPORT OR SCIENTIFIC N.

## Prior falsification and testable hypothesis

Gate 14's local outbox experiment demonstrated an important counterexample: appending to a file then crashing **before** committing the sender's SQLite receipt causes the sender to retry and append a second time. A sender's atomic outbox cannot atomically include an arbitrary external service.

Gate 15 tests the **narrower** receiver-side invariant: when the receiver processes a stable idempotency key, can it commit its own synthetic inbox row **and** synthetic marker in one receiver-local SQLite transaction, so that a sender crash *after receiver commit but before sender acknowledgment* does not make that receiver-local marker repeat?

Implementation: `experiments/akdc/idempotent_consumer_research.py`. The receiver owns a **separate SQLite file** from the Gate 14 sender, with strict user_version, CHECK, primary-key, and foreign-key validation, WAL/FULL, and `BEGIN IMMEDIATE`. It accepts only 64-character hex tags for its identity and payload. Under that identical key/payload, a duplicate returns `DUPLICATE_RECEIVER_MARKER`; a key reused with conflicting payload fails closed. Receiver outcome is the literal `SYNTHETIC_RECEIVER_MARKER` only. This is *not* a real external effect.

The sender obtains its pending tag/payload from the Gate 14 outbox, delivers them to the receiver-local transaction, **then separately ACKs its own SQLite outbox**. The two databases do *not* participate in a shared atomic commit. Crash injection immediately after receiver commit but before sender ACK must leave a receiver marker plus a pending sender entry; a later redrive must return a duplicate and successfully ACK.

## Predeclared controls

Fourteen research tests cover normal first/duplicate delivery, crash after receiver commit before sender ACK, crash after ACK, 32-thread and 8-process sender contention, receiver crashes before/after its own COMMIT, reopening the receiver, different-payload collision rejection, multiple independent producer files with the same stable idempotency identity, altered schema and unversioned store refusal, malformed keys, and **HMAC key-epoch rotation causing a new receiver identity**.

**Status:** source/tests are committed to a new research branch and added to the existing hash-locked Python 3.10/3.11/3.12 quality+pytest matrix. Exact-head GitHub Actions results are required before claiming any passing tests. The inherited locked-toolchain security audit remains a separate non-waived blocker under [#1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [#1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530).

## Claims deliberately excluded

An idempotent receiver **only** prevents duplicate insertions of the simulated effect **inside the same receiver database**, given the same stable key and shared database. It does NOT guarantee exactly-once email, file append, payment, API callback, external transaction, remote network partition behavior, external user consent or independent authorization. The Gate 14 external-file double-append counterexample still applies to a receiver that dispatches a nontransactional external effect. Sender identity, provider identity and operation bindings remain **unverified assertions**; signing, replay nonce scope, revocation and key lifecycle are not proven. Cross-region/independent receiver stores, lost key epochs, durable power failures and disaster recovery remain untested. This is not a production SDK live transport exercise; prior Gate 13's MCP SDK results remain separately categorized.

The research acceptance state stays `DGAF_V1_RELEASE=HOLD`, `SCIENTIFIC_N_INCREMENT=0`, `HIGH_ASSURANCE=NOT_AUTHORIZED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`. The separate replay issue [#1536](https://github.com/ndrorchestration/DGAF-Framework/issues/1536) stays open; no CommitGate, protected main or SYN-AUTH-01 #1508 modifications.
