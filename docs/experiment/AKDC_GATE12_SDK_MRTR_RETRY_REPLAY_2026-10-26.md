# AKDC Gate 12 — Official MCP v2 MRTR retry/replay adversarial probe

**Classification:** EXECUTABLE SDK RESEARCH FIXTURE / NO LIVE NETWORK / NO AUTHENTICATED PRINCIPAL / NO EXTERNAL EFFECT / SCIENTIFIC N=0.

## Objective and implementation

Gate 11 confirmed two MCP 2026-07-28 in-process SDK wire responses without following a genuine multi-round-trip retry. Gate 12 uses the **same exact frozen research dependency set** (`@modelcontextprotocol/client@2.4.0`, `@modelcontextprotocol/server@2.4.0`, `zod@4.6.7`) to exercise the official SDK's `inputRequired`, `acceptedContent`, `createRequestStateCodec`, `ServerOptions.requestState.verify` and manual retry APIs.

The test serves a **no-effect synthetic confirmation** with an in-process `createMcpHandler` HTTP adapter, never making a real network request. It asserts four sequential `tools/call` JSON-RPC pairs, each captured from the actual SDK path:

1. `input_required`: server returns `elicitation/create` and an SDK-HMAC-signed, TTL-bounded opaque `requestState`.
2. `protocol_error`: caller alters the token, server verification rejects `-32602` **before handler re-entry**.
3. `complete`: caller echoes original token and synthetic accepted form, receives a fixture-only result.
4. `complete` again: the caller replays the same valid signed token with the same accepted form and gets another successful result, deliberately demonstrating **HMAC integrity is not single-use/replay prevention**.

Raw request-response typed JSON-RPC IDs and protocol negotiation must match. A separate Python verifier processes all four actual SDK-generated JSON pairs through the existing, unchanged Gate 9 non-authoritative DGAF ingress, asserting `PRESENTED_NOT_GRANTED` and that the signed token, elicitation body and raw result text do not survive in DGAF's minimized record. The synthetic raw trace is allowed only in the test artifact; never retain user data in this form.

## Evidence standard

CI is dedicated to the research branch. Both the SDK exchange and a **separate non-waived npm audit** use an archived, exactly hash-pinned `package-lock.json` generated and frozen at Gate 11 (SHA-256 `aebc3f74fedec3a5d3927d992609a6a3a1dc1460d456f561f186e47c45646afd`) and `npm ci --ignore-scripts`. Passing Gate 11 alone is **not evidence Gate 12 executes**. Gate 12 must produce an exact-head CI job success, manifest digest and downloadable GitHub Actions artifact before claims are advanced.

## Explicit limitations

- The SDK's HMAC state token is **signed but not encrypted**, and minted with ephemeral fixture-only process-local key. It does not authenticate a remote principal. No database-backed nonce, one-time use, distributed key custody, revocation, or identity-bound validation.
- The `elicitation/create` form response is a literal fixture accepted by the synthetic handler, not real user consent or authority to execute a tool.
- This research demonstrates replay *possibility*, **not** prevention. A repeated valid token can succeed twice unless a separate transactional replay registry enforces a single-use policy in the appropriate authorization plane. Gate 4's separate SQLite research receiver does not automatically enforce this SDK token's one-time semantics.
- No TLS, remote HTTP peer, official A2A wire traffic, real MRTR two-phase side effects, signed audit logs, independent scientific evaluation or deployment occurs.
- The inherited Python CI dependency vulnerabilities remain tracked independently in [Black #1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [certifi/filelock/setuptools #1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530). No waiver.

**Hard ceilings:** `DGAF_V1_RELEASE=HOLD`; `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `HIGH_ASSURANCE=NOT_AUTHORIZED`. All AKDC research branches remain draft and unmerged; no protected `main` or SYN-AUTH-01 #1508 modifications.
