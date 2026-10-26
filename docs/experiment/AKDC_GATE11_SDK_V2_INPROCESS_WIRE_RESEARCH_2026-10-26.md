# AKDC Gate 11 — published MCP SDK v2 in-process wire reproduction

**Status:** DRAFT / CODE AND CI REQUESTED / SDK EXECUTION NOT YET VERIFIED / NO PRODUCTION OR SCIENTIFIC ADMISSION.

## Difference from Gate 10

Gate 10 used two **exact official specification example** JSON fixtures. Gate 11 goes beyond them by running the **published official TypeScript MCP SDK v2 client and server packages** over the SDK's **in-process Streamable HTTP handler** path. Unlike the 2025-era `InMemoryTransport` example, this path is designed to negotiate **MCP 2026-07-28**. It involves no public network MCP endpoint, external user data, real tool effects, third-party credentials or human elicitation.

Primary documented implementation references:
- [Official SDK v2 testing guide](https://ts.sdk.modelcontextprotocol.io/v2/testing)
- [2026-07-28 migration and wire discriminator behavior](https://ts.sdk.modelcontextprotocol.io/v2/migration/support-2026-07-28)
- [Official MCP SDK v2 MRTR guide](https://ts.sdk.modelcontextprotocol.io/v2/servers/input-required)

## Bounded implementation

`experiments/akdc/sdk_v2_probe/` includes a separate `package.json` with exact **direct dependencies** `@modelcontextprotocol/client@2.4.0`, `@modelcontextprotocol/server@2.4.0` and `zod@4.2.0`. A custom local `fetch` wrapper captures the SDK-emitted JSON-RPC requests and its handler's responses, including JSON or SSE framing, in ephemeral test memory. The test covers only:
1. A synthetic read-only `tools/call` returning `complete`.
2. A synthetic `input_required` result carrying a harmless opaque requestState. Client automatic fulfillment is explicitly disabled. It never supplies elicitation answers or retries.

The probe asserts **real SDK-negotiated protocol version**, typed JSON-RPC request ID correlation, required 2026 wire `resultType`, the SDK public API's omission of complete-result `resultType`, and two trace pairs. A follow-up Python verifier reads that generated test-only wire fixture through Gate 9 normalization and the original, unchanged `validate_external_runtime_envelope` source; it asserts admission remains **PRESENTED_NOT_GRANTED / RECORD_ONLY** and that synthetic raw tool text / MRTR requestState are absent from the DGAF envelope.

## Supply-chain and evidence caveat

The first GitHub Action run resolves **temporary** transitive npm dependencies through a scratch `npm install --package-lock-only`, then `npm ci --ignore-scripts`. The resolved `package-lock.json`, synthetic wire fixture and trace manifest are uploaded for review. **This initial resolution is NOT a signed, reviewed or repo-frozen npm lock, even though direct versions are fixed.** It must be independently reviewed and checked in with exact integrity pins before reproducibility can be claimed. In addition, a separate non-waived `npm audit --audit-level=high` job tests this new Node SDK dependency tree; a failed advisory blocks SDK-probe admission. The inherited Python CI security audit and issues [#1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) / [#1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530) remain distinct.

The SDK trace artifact contains **synthetic test-only input/output**, deliberately not real user or proprietary data. The raw-wire fixture is test evidence for this SDK instance, not a cryptographic attestation of external sender identity or real distributed interoperability. Only the **local harness** has an HMAC key, and it uses an explicitly public, test-only key; this does not establish production secrecy. HTTP framing over a fake `test.local` origin is served in-process and does not test real network behavior, TLS, reconnects, custody, actual peer authentication, MRTR client fulfillment or retry state integrity.

## Gates

1. Validate the exact Gate 10 baseline CI separately.
2. Require the new Gate 11 action to complete its real SDK trace and Python consumer steps, and retain their raw GitHub job logs and artifact identifiers.
3. Inspect and freeze the resolved npm lock and run separate `npm audit`, with no waiver.
4. Add independently produced official SDK traces across capability negotiation, MRTR rounds and network transport **only** after privacy/security review.

**Hard ceilings:** `DGAF_V1_RELEASE=HOLD`; `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `HIGH_ASSURANCE=NOT_AUTHORIZED`. No protected main, production runtime, authorization, scientific experiment, pilot state, or SYN-AUTH-01 #1508 changes.
