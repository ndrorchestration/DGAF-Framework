# AKDC Gate 8 — minimize captured MCP evidence (2026-10-26)

**Status:** STACKED DRAFT / LOCAL ENGINEERING / NO LIVE SDK / NO IDENTITY ASSURANCE / NO SCIENTIFIC N / NO RELEASE AUTHORIZATION.

## Finding

Gate 6/7 preserved the decoded MCP tool response in DGAF's untrusted record-only evidence. That potentially retained text content, structured content, protocol error data, opaque requestState tokens, and inputRequest maps unnecessarily. The request arguments were not persisted, but the original tool reply was. This is a privacy and data-minimization issue even on a non-consequential ingress path.

## Bounded fix

Gate 8 retains only the result category, tool error flag, protocol error code, presence (not values) of MRTR context fields, a hashed local correlation identifier, the canonical-decoded frame-pair digest and the receiver receipt witness. It discards decoded response content, error messages/data and opaque MRTR state before constructing ProtocolObservation. The DGAF record remains RECORD_ONLY, and external claims remain unverified.

Eight new tests check literal sensitive marker absence from the normalized observation and DGAF envelope, alongside invalid content/argument rejection and differing capture digests for differing requests. Earlier positive MRTR fixtures were adapted to require non-retention. Local pinned-source regression: **80/80 PASS, zero skipped**, including all 72 earlier tests, with resource warnings treated as errors. This is **local evidence, not exact-head GitHub CI**.

## Strict limitation

SHA-256 of canonicalized decoded frames is an **unkeyed commitment**, not confidentiality. It can reveal repetition or enable guesses against low-entropy data. Retained principal/runtime/source identifiers and metadata can also be sensitive. This experiment does not establish complete memory erasure, log hygiene, independent privacy certification, authenticated identity, transport security, SDK interoperability, or compliance with any law.

The additional MCP content check covers mandatory field types for selected ContentBlock variants, plus object-shaped tool arguments and string-shaped requestState. It is **not** a recursive JSON Schema validator: annotation schemas, full resource formats, base64/URI checks, nested InputRequest types and capability negotiation remain unverified. Compare against the [pinned official MCP schema](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/schema.json) before claiming conformance.

## Independent gates required

1. Exact-head Black/isort/mypy/flake8/Python 3.10–3.12 CI and non-waived dependency audit; remediation is separately tracked under [issue #1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477).
2. Official SDK-generated raw frame fixtures, redaction at byte-capture boundary, and raw-input lifecycle.
3. Authenticated principal binding/revocation, keyed evidence commitment and replay scope across reconnects.
4. Independent review and a predeclared direct-adapter comparator before any empirical or scientific claim.

Reference DGAF validator Git blob: fab53669c69ea0b26bc9a55bce2ab157ac8f5348. No changes to the separately governed unfrozen SYN-AUTH-01 (#1508), protected main, CommitGate, runtime execution, or scientific N.

**Ceilings:** DGAF_V1_RELEASE=HOLD; SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED.
