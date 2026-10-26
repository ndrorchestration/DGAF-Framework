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


## Verified hosted execution and dependency-lock closure (2026-10-26)

Official TypeScript SDK v2 in-process wire job **SUCCESS** at commit `6f0f72cd61fbf21dd756431ae926f6dfd9b756d4`, workflow run `40335433472`, job `121615612128`. Its separate **non-waived npm audit SUCCESS**, job `121615611669`, after updating isolated research fixture Zod direct pin from `4.2.0` to audit-reported `4.6.7` for `GHSA-mrhx-c7xc-m3w5`. The earlier Zod vulnerability was observed, not waived. These results do not remediate inherited Python CI advisories in #1477/#1530.

The actual SDK negotiated **MCP 2026-07-28**, generated exactly **two correlated raw JSON-RPC tools/call exchanges** with result types `complete` and `input_required`, and both were admitted as non-authorizing DGAF observations through the original pinned DGAF ingress code. Raw synthetic wire fixture SHA-256: `f07f8a3ca2f266b2e6e312e97d54bd872c4898abca076ffa0594eee63f380796`. This demonstrates tested in-process SDK behavior only; no live network, real identity or side-effect execution.

Hosted Actions artifact `12656947266` captured the 15-entry npm lock plus trace; exact extracted `package-lock.json` SHA-256 `aebc3f74fedec3a5d3927d992609a6a3a1dc1460d456f561f186e47c45646afd`, Git blob `1b047420c3677d13bd2aac9432b1acf08dbadd3e`. The exact archived lock bytes were committed into this stacked **DRAFT** PR, and the branch's research workflow was revised to enforce SHA-256 equality and use **npm ci** for both SDK execution and npm audit. This moves from initial floating transitive resolution to pinned-integrity reproducibility at the *research dependency tree* level. It is not a signed official DGAF bootstrap or independently reviewed security authorization.

**Next acceptance checkpoint:** verify the *new exact head* SHA-lock enforcement workflow; prior green jobs are historical and do not certify the revised workflow. Its result remains an explicit open gate until observed.
