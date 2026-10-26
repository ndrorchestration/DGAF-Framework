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

## Gate 7 — MCP MRTR normative field validation (2026-10-26)

**Research-only correction:** The published MCP 2026-07-28 `InputRequiredResult` definition says at least one of `inputRequests` or `requestState` MUST be present. Its JSON Schema machine `required` list, however, includes only `resultType`; the additional either/or condition is described but not encoded in that array. Former AKDC synthetic ingress classification and raw-frame normalization accepted a bare `{"resultType":"input_required"}` object. Four red-test cases exposed missing requirements/type and hybrid handling.

The research branch now runs the same bounded structural check at both layers. It refuses missing required MRTR context, wrong `inputRequests` object type, wrong `requestState` string type, and unsupported hybrids with `content`/`isError`. Existing input-required fixtures now contain opaque `requestState`. This does not interpret MRTR request bodies, attest state, complete client capabilities or fulfill a multi-round trip.

**Local evidence:** 72/72 combined pinned-source local Python tests passed (previous 68 plus four counterexample regressions), resource warnings treated as errors; 4/4 dedicated pytest scenarios also passed, with three subtests. The pre-fix red run produced failures, establishing that the tests detect the former defect. This is **not** exact GitHub Actions or official SDK compatibility evidence. Original reference validator blob remains `fab53669c69ea0b26bc9a55bce2ab157ac8f5348`. Official upstream schema blob examined: `213c58f6d9a1c2ce6ad055afe90bbdb095a29ee8`.

**Reproducibility archive:** `AKDC_Gate7_MCP_MRTR_2026-10-26.zip`, SHA-256 `4117d21c057607ed4da0fac58275d63fcf19c4de9568597bbdb6d3e3dbcf858e`, conversation artifact only. Local reference package plus corrections, counterexample tests and report; not an exact PR-head GitHub checkout.

**Remaining blocker:** Await independent exact-head Black/isort/mypy/multi-Python CI and non-waived inherited `pip-audit`; do not interpret missing PR-triggered run listings as success or failure. Scope excludes official live SDK traces, authenticated principal binding, `requestState` security review, raw byte-custody/redaction policy, production authorization, scientific samples, and any change to `SYN-AUTH-01` #1508.

