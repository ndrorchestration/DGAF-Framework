# AKDC Gate 16 — Real loopback HTTP idempotent receiver and lost-ACK falsification

**Classification:** STACKED DRAFT / STANDARD-LIB LOCAL TCP / PUBLISHED TEST KEYS / SYNTHETIC RECEIVER-LOCAL MARKER / NO EXTERNAL IDENTITY OR AUTHORIZATION.

## What changes from Gate 15

Gate 15 verified two separate SQLite databases in a single local Python process: a sender outbox and receiver inbox plus synthetic marker. Gate 16 moves the receiving operation into a **separate OS process serving actual HTTP over TCP bound to 127.0.0.1** using Python's standard library. This tests transport framing, missing/mutated signatures and lost replies across process boundaries; it does **not** use an actual remote server, TLS, authenticated operator or official MCP HTTP SDK. All state remains fixture-only.

`experiments/akdc/loopback_consumer_research.py` implements a deliberately bounded `POST /v1/research/idempotent-receipt` handler with maximum 2,048-byte request body, strict JSON shape, SHA256-HMAC of raw request bytes **plus domain/method/path**, constant-time MAC comparison, and two test-only public signing-key epochs mapped to one fixed fixture subject. The receiver calls the unchanged Gate 15 SQLite receiver `accept` and returns a synthetic state, never a real effect. It does not provide confidentiality or real principal authentication: the demonstration keys are published in code and are NOT secrets; the listener is unencrypted loopback HTTP.

The sender's pending receipt tag remains unchanged when the **HTTP MAC signing epoch** switches from A to B. This tests continuity of idempotency across the transport-key switch, which is distinct from the earlier negative control: **rotating the HMAC key that originally derives the sender receipt tag changes its identity and creates a second receiver marker**. Receiver-side deduplication therefore depends on an independently stable operation identifier. There is no real credential revocation lifecycle or secure key management.

## Predeclared falsification

Fifteen new standard-library tests run the server in a separate subprocess and connect via real `http.client.HTTPConnection` on 127.0.0.1. Cases include: normal first/duplicate HTTP deliveries; eight concurrent HTTP requests; receiver restart; lost response **after receiver COMMIT** and before sender ACK, followed by redrive and ACK with another fixture signing epoch; missing/wrong MAC, altered signed body, unknown/revoked fixture epoch; invalid idempotency key and conflicting payload; wrong route/method; same key across two independent sender DBs; and the HMAC-derived sender-key-rotation duplication negative control.

**Expected lost-ACK result:** receiver has one inbox row and one test marker; sender keeps one pending outbox item and no local marker; second transport attempt yields `DUPLICATE_RECEIVER_MARKER` and acknowledges sender without adding a second receiver marker. Sender SQLite ACK is deliberately **not** atomically coupled to receiver SQLite commit. A real remote nontransactional effect would still risk duplication as Gate 14 established.

The existing AKDC research CI matrix for Python 3.10/3.11/3.12, Black, isort, mypy, flake8 and pytest includes both new files. **No Gate16 exact-head test/CI PASS is claimed until observed.** The separate inherited Python `pip-audit` dependency failure remains non-waived under [#1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [#1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530). The official MCP SDK Gate 12/13 trials are separate earlier evidence, not repeated by this new Python HTTP fixture.

## Non-promotion boundary

This is a localhost socket fixture authenticated only in the narrow sense of possession of **publicly known test keys**. It cannot authenticate a real person, establish enterprise network trust, enforce consent/delegation/policy, secure secrets, guarantee external effects, withstand cross-host partitions, prove TLS/revocation, or increase scientific sample count. It has no new production wiring or permission to merge. For consequential exactly-once outcomes, still require independently authenticated principal and operation-scoped stable key, receiver-owned idempotency integrated with the **actual consequential operation**, explicit replay/key-epoch retention, partition/crash recovery and independent review. Keep [#1536](https://github.com/ndrorchestration/DGAF-Framework/issues/1536) open.

**Ceilings:** DGAF_V1_RELEASE=HOLD; SCIENTIFIC_N_INCREMENT=0; HIGH_ASSURANCE=NOT_AUTHORIZED; INDEPENDENT_VALIDATION=NOT_ESTABLISHED. PR stacked on Gate 15; protected main, CommitGate, SYN-AUTH-01 #1508 unchanged.
