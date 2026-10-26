# AKDC Gate 6 validation checkpoint — 2026-10-26

## Objective

Introduce explicit A2A and MCP frame-to-record normalization without allowing source transport success to become governance authority. Pin protocol versions; disclose receiver-assigned ordering; bind decoded frames to a reproducible digest and to DGAF's existing external envelope.

## Results

The local combined suite passed 68/68 tests, zero skipped, with ResourceWarnings treated as errors: 42 inherited Gate 3–5 tests and 26 new raw-frame tests. Tests were performed in a controlled local Python process against a pinned DGAF validator snapshot, not a live A2A/MCP endpoint, official SDK trace, or GitHub CI.

## Adversarial controls

A2A: unsupported versions/states, legacy shapes, fake wire sequence field, mixed union branches, missing status, unbounded frame, non-JSON numbers, receiver counter spoofing, disconnected streams and mutable input. MCP: mismatched IDs, mismatched method, missing request metadata, unsupported versions/results, absent wire resultType, protocol error versus tool error and content mutation.

The normalization output includes a SHA-256 of the canonicalized JSON object(s), receiver stream ID and counter, and a NOT_ESTABLISHED capture-attestation label. DGAF's pinned ingress validator checks the recalculated evidence digest and classifies the record as external/unverified.

## Limits and open gates

1. The frame-hash is of canonical **decoded** JSON, not the original byte stream, and therefore cannot establish a byte-exact network capture.
2. A2A protocol events do not contain the internal sequence; the local receipt counter has no distributed ordering guarantees. Across reconnects the same wire frame may get a new event ID.
3. Self-asserted identity fields, raw content confidentiality, log redaction, authentication, revocation, trusted envelope binding and exactly-once consequential effects remain unverified.
4. The subset parser is **not** a full A2A or MCP schema conformance implementation. Some application SDKs strip MCP wire-only `resultType` before exposing the result.
5. No real-world benchmarks, blinded study, efficacy promotion, official SDK tests or independent reviewers.
6. Full Python 3.10–3.12 quality and security CI are still separate; inherited pinned CI dependency vulnerability remediation is tracked outside AKDC.

Next: capture actual negotiated raw protocol exchanges in a controlled, cost-free local SDK harness; create independent negative/comparator cases; validate privacy/redaction before retaining captured payloads. Keep all experimental outputs non-authoritative.