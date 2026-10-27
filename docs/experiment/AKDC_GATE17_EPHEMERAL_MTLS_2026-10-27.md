# AKDC Gate 17 — Ephemeral mutual-TLS localhost transport falsification

**Status: STACKED RESEARCH DRAFT / MUTUAL TLS WITH EPHEMERAL TEST CERTIFICATES / NOT AN EXTERNALLY AUTHENTICATED PERSON OR AUTHORIZED EFFECT.**

## Prior evidence and new research question

Gate 16 passed 161 tests and 47 subtests on Python 3.10, 3.11, and 3.12 using a separate localhost HTTP server process, a receiver-local synthetic SQLite inbox marker, and two published HMAC fixture keys. Gate 16 did **not** provide TLS or real identity authentication.

Gate 17 adds `experiments/akdc/mtls_loopback_research.py` and `tests/test_akdc_mtls_loopback_research.py` to test **actual TLS 1.3 mutual certificate verification over 127.0.0.1**, without treating test trust as production trust. The test runner generates a fresh ephemeral CA, server certificate with `IP:127.0.0.1` SAN, two distinct trusted client certificates, and a rogue CA/client certificate via locally installed OpenSSL. These keys live only in temporary runner files and are **not checked into Git or uploaded as artifacts**.

The same bounded Gate 16 HTTP handler verifies a fixture-HMAC binding of HTTP method/path/body, checks a fixed synthetic request shape, and uses the Gate 15 receiver-local SQLite inbox+marker transaction. Its method never executes an external effect and its `authority` response remains `NOT_GRANTED`. The separate sender SQLite outbox performs an ACK **after** the receiver commits. TLS trust is established only against an ephemeral test CA; this is not an independent real-world identity authority, user consent or a production key policy.

## Predeclared falsification

Eleven new test cases:
- TLS 1.3 server and a trusted fixture client perform first/duplicate receipt delivery.
- Deliberately lose the server's HTTP reply **after its local DB COMMIT**; the sender stays pending, and a redrive with a second ephemeral trusted client certificate and alternate public fixture-HMAC epoch must produce a duplicate receipt and then ACK.
- Eight concurrent mTLS deliveries yield one first and seven duplicate receiver-local markers.
- Receiver process restart preserves the same receipt.
- No client certificate, rogue client certificate, untrusted server CA and server hostname/SAN mismatch must be rejected at TLS.
- A valid mTLS connection with a wrong fixture message MAC must be refused by the application.
- **Negative control:** both distinct trusted test client certificates may address the same idempotency key because no per-cert principal/operation ownership policy exists.
- **Negative control:** rotation of the sender's *separate receipt-tag HMAC key* creates another idempotency identity, even with mTLS, allowing a second local receiver marker.

A CA-issued certificate proves only possession of one ephemeral test credential within this test trust root. No certificate-revocation list/OCSP, key compromise, hardware key custody, real principal-to-permission mapping, public DNS, external host or actual remote service is exercised. The retained public fixture HMAC keys are deliberately **not secrets**. There is no independent scientific or security review.

The existing AKDC research-only GitHub Actions Python 3.10/3.11/3.12 matrix runs the two new files through compileall, flake8, Black, isort, mypy and pytest. At authoring, **no Gate 17 test or CI success is yet claimed**. The inherited locked Python dependency `pip-audit` failure remains independently blocking under [Black #1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [additional advisories #1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530). No scan waiver or direct lock edits.

## Required downstream gate (not satisfied here)

A consequential externally idempotent operation requires independently authenticated principal-to-scope binding, stable operation ID across *all* signing and receipt-key epochs, actual TLS deployment and revocation policy, real downstream effect endpoint whose own idempotency boundary encloses the effect, failure recovery under partitions and host crashes, operational logging without sensitive bearer-token retention, and external review. The prior Gate 14 **double append after crash** remains an explicit falsifier for claims about arbitrary external effects.

**Non-promotion:** DGAF_V1_RELEASE=HOLD; SCIENTIFIC_N_INCREMENT=0; HIGH_ASSURANCE=NOT_AUTHORIZED; INDEPENDENT_VALIDATION=NOT_ESTABLISHED. All AKDC PRs stacked DRAFT/UNMERGED; protected main, CommitGate, production authz and SYN-AUTH-01 #1508 unchanged. Tracked risk issue [#1536](https://github.com/ndrorchestration/DGAF-Framework/issues/1536) remains OPEN.
