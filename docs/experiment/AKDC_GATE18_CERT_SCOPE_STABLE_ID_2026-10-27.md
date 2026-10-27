# AKDC Gate 18 — Ephemeral mTLS principal binding and stable scoped operation identity

**Classification:** STACKED DRAFT / RESEARCH ONLY / TEST CA TRUST / NO EXTERNAL PRINCIPAL, PRODUCTION PERMISSION, REAL EFFECT OR SCIENTIFIC N.

## Motivation and precise claim

Gate 17 proved TLS 1.3 mutual certificate verification with ephemeral CA, but its own negative controls found that **different CA-trusted client certificates could submit the same synthetic operation** and that rotating the sender's HMAC-derived receipt tag created a second receiver idempotency identity. Cryptographic client-certificate acceptance alone is not authorization for a specific operation.

Gate 18 extends only this synthetic research fixture. `experiments/akdc/cert_bound_receiver_research.py` requires an **explicit, immutable-at-startup policy** mapping each exact SHA-256 fingerprint of a test client's DER certificate to a synthetic principal label and an allowed fixture action set. Valid-CA but unlisted client certificates receive HTTP 403 **before receiver writes**; an enrolled client claiming another principal or an unlisted action also receives HTTP 403. Only the fixed test action `akdc-confirm-fixture` can create a fixed `SYNTHETIC_RECEIVER_MARKER` in the existing receiver-local SQLite database. The server continues to require TLS 1.3 and a CA-signed client certificate, and remains bound to **127.0.0.1**.

The idempotency identity is now derived using a canonical SHA-256 digest of `[domain, principal, action, operation_id]`. This is a **non-secret stable identifier**, not a MAC or authorization token. An immutable operation ID is necessary to remain stable across TLS certificate replacement and sender HMAC-key rotation, while a different scoped principal or operation ID must yield a different identity. Request payload digest rebinding against an existing idempotency key is rejected by the existing receiver ledger.

## Predeclared 17 adversarial tests

The tests create the CA and keys only in a disposable temporary directory via OpenSSL. Fixtures include:
- two distinct CA-trusted leaf client certificates both explicitly mapped to `fixture-alpha`, to model identity-preserving certificate renewal;
- a third CA-trusted client mapped to `fixture-beta` but **not** authorized for the fixed `akdc-confirm-fixture` action;
- a fourth CA-trusted but **unlisted** client, plus a rogue CA/client and a server certificate bearing the expected localhost IP SAN.

The tests exercise allowed first/duplicate delivery, certificate rotation under one principal, HMAC-derived **sender receipt tag rotation** counterexample versus a stable explicit receiver operation ID, rejection of impersonation, operation-scope denial, missing or rogue certificate, unknown trusted certificate, payload rebinding, eight concurrent network calls, an HTTP reply dropped after SQLite commit followed by retry using the renewed certificate, reboot-required local fixture policy removal, malformed operation identity and invalid policy-file refusal. In the key-rotation test the **sender-local SQLite outbox still contains two distinct receipt rows** under two secrets: only the new receiver-local identity remains one. This does not repair the producer's historical receipt store or establish a global key-epoch transition.

**At PR creation these are planned test claims, not verified test outcomes.** Acceptance requires the latest exact-head GitHub Actions Python 3.10–3.12 quality/mypy/pytest results; the new test files are included in the repository's existing hash-locked nonrelease AKDC matrix.

## Boundaries deliberately NOT crossed

The enrolled CA and certificate fingerprints are only temporary **synthetic fixture credentials**; they do not verify real human identities or real operator entitlement. The static in-memory allowlist has neither dynamic revocation propagation nor trust of an external PKI. Restart-based policy removal is not immediate revocation. The operation ID is caller-supplied and no production authority delegates its ownership. The receiver effect marker and sender outbox are local SQLite only. A genuine outside-service effect may still be duplicated after post-effect crash, as demonstrated by Gate 14. This gate has no real HTTPS host, credential lifecycle, hardware key custody, production external SDK, OAuth policy, provider identity, consent, delegated authorization, independent tester or scientific efficacy result. TLS certificate matching and fixture action allowlisting do not create a production access-control system.

The inherited Python package-security audit remains a distinct **blocking** failure under [#1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [#1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530); locks are not modified and advisories are not waived. Related [replay boundary issue #1536](https://github.com/ndrorchestration/DGAF-Framework/issues/1536) remains OPEN, pending independently grounded real principal/operation authority, revocation, externally stable operation IDs and effect-endpoint idempotency.

**Immutable ceilings:** `DGAF_V1_RELEASE=HOLD`; `SCIENTIFIC_N_INCREMENT=0`; `HIGH_ASSURANCE=NOT_AUTHORIZED`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`. All stacked AKDC PRs remain DRAFT/UNMERGED; protected `main`, CommitGate and SYN-AUTH-01 #1508 unchanged.
