# AKDC Gate 10 — upstream MCP MRTR golden examples (research only)

**Status:** STACKED DRAFT / SYNTHETIC RECEIVER ADMISSION / NO SDK OR LIVE NETWORK / SCIENTIFIC N=0 / NOT AUTHORIZED FOR RELEASE.

## Independently sourced baseline

Two MCP 2026-07-28 published, unmodified JSON examples were fetched from the official `modelcontextprotocol/modelcontextprotocol` upstream:

1. [Input-required response with opaque requestState only](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/examples/InputRequiredResult/input-required-result-with-request-state-only.json) — upstream Git blob `7f1dec1f69d35db2428079a52911ade51f86451f`.
2. [Input-required response with elicitation, sampling and requestState](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/examples/InputRequiredResult/input-required-result-with-elicitation-and-sampling-and-request-state.json) — upstream Git blob `6ffc95394446982b375e13c4bf6a23eb4e3d7ced`.

The copies under `experiments/akdc/fixtures/mcp-2026-07-28/` reproduce both Git blobs **byte-for-byte**, checked after committing. `tests/test_akdc_upstream_mrtr_examples_research.py` revalidates those blob hashes before interpreting fixture contents. The examples are publisher-authored normative illustrations, **not captures from any SDK, live server, or authenticated party**.

## Gate 10 scoped engineering

`experiments/akdc/mrtr_upstream_fixture_research.py` adds a **separate test-wrapper**, not production transport code. It accepts a caller-supplied set of declared MRTR input-method capabilities and refuses nested requests with missing/undeclared methods or malformed request object shape before delegating to the existing nonauthorizing AKDC Gate 9 observer.

The recognized methods come from the published protocol (elicitation/create, sampling/createMessage, roots/list). The declared capability set is a test fixture assertion, **not independently negotiated, authenticated or authorized**. The wrapper never fulfills input requests, echoes requestState, retries calls, dispatches tools or verifies nested method schemas. The test does not imply that deprecated sampling/roots usage is recommended.

## Falsification and evidence

Ten new local tests passed, plus the 90 inherited Gate 3–9 unit tests, for **100/100 local tests PASS with zero skips** and Python ResourceWarning treated as error. Tests include provenance hash validation, permitted/unpermitted published MRTR examples, partial capability declaration denial, unknown/malformed method denial, no retention of example input content or opaque requestState, keyed HMAC change when opaque source state changes, and continuing DGAF record-only admission.

This is LOCAL reproducibility evidence, **not** a source-byte-exact GitHub PR-head quality result. The research-only Python 3.10/3.11/3.12 GitHub Actions matrix is independently required. The non-waived CI dependency audit still blocks aggregate acceptance; independent issues are [Black #1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [other CI toolchain advisories #1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530).

## Next independently admissible step

Run a **capturing official MCP SDK transport pair** with a reproducible, independently reviewed dependency lock and protocol version negotiation; correlate real raw-wire JSON-RPC request/response IDs before capture minimization. Establish a trustworthy provenance witness, capability declarations, and key-lifecycle policy; only then compare captured bytes with these published examples. A live SDK test is NOT evidenced here.

**Ceilings unchanged:** DGAF_V1_RELEASE=HOLD; SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED. No CommitGate, execution, custody, protected-main, scientific experiment or SYN-AUTH-01 #1508 modifications.
