# Agent Instrument A/B baseline smoke v0.1 — source-locked synthetic engineering check

> **Status:** PROPOSED / DRAFT / INTERNAL SYNTHETIC TEST. **Not** preregistered or scientific evidence. No agent was evaluated. No instrument interface was implemented.
>
> **Relationship:** separate, non-authorizing follow-up to [terminology/protocol draft PR #1570](https://github.com/ndrorchestration/DGAF-Framework/pull/1570); do **not** use this lane to merge or promote #1570.
>
> **Source anchor:** protected `main` `1a95b94332dffb404c5a3ce026d70781a8c10b90`. The reference graph and validator were fetched at their [exact original fixture](https://github.com/ndrorchestration/DGAF-Framework/blob/1a95b94332dffb404c5a3ce026d70781a8c10b90/docs/research/fixtures/STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_REFERENCE.json) and [validator](https://github.com/ndrorchestration/DGAF-Framework/blob/1a95b94332dffb404c5a3ce026d70781a8c10b90/scripts/validate_structural_epistemics_claim_graph.py) identities; their Git blob digests are pinned in the candidate manifest.

## Purpose and limiting distinction

Before considering an instrument-specific API, check whether direct calls and a simple procedural entry point of the **already implemented** ClaimGraph validator produce the same structural judgments on fixed synthetic cases.

- **A-DIRECT:** call `validate_claim_graph(graph)` from Python.
- **B-FIXED-CLI-PROXY:** write an isolated in-memory-derived JSON candidate into a disposable temporary directory; invoke `python scripts/validate_structural_epistemics_claim_graph.py <temporary-file>` once; capture return code and text.
- **C-INSTRUMENT:** **NOT IMPLEMENTED AND NOT TESTED**.

This checks matching **entry points to one validator**, not a comparison with a full configurable workflow, human usability, a learned agent, or a fair A/B/C agent trial. If A and B agree it means their structural plumbing agrees on the six synthetic cases; it does **not** establish functional independence or a unique Agent Instrument contribution.

## Source, provenance, and artifacts

| Role | Path | What the checks do |
| --- | --- | --- |
| Case definitions and source pin | `docs/research/fixtures/AGENT_INSTRUMENT_AB_SMOKE_MANIFEST_V0_1.json` | Six synthetic mutations and expected fail/pass fragments; pins existing source using Git SHA-1 **blob IDs**, not standalone raw SHA-1 or a security-authenticity signature |
| Exerciser | `tests/test_agent_instrument_ab_baseline_smoke.py` | One source-lock/safety classification check plus six parametrized A/B parity checks |
| Existing immutable source reference | `docs/research/fixtures/STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_REFERENCE.json` | Existing synthetic hypothesis with support and counterevidence; *not* blinded or independent |
| Existing validator | `scripts/validate_structural_epistemics_claim_graph.py` | Schema and epistemic-structure invariants; explicitly **not** claim truth, efficacy, permission or execution |
| Existing schema files | `docs/research/STRUCTURAL_EPISTEMICS_{CLAIM_RECORD,EVIDENCE_GRAPH}_SCHEMA.json` | Used by both A and B through the same validator |

Only two new files are introduced on this draft: the manifest and the smoke test. They are **not** a second graph, duplicate evaluator, or instrument runtime.

### Reproducible local command (proposal, executable where dependencies installed)

```bash
python -m pytest -q tests/test_agent_instrument_ab_baseline_smoke.py
```

Prerequisites: Python compatible with the repository, `pytest`, `jsonschema`, exact source files at the anchored Git blob identities. The test fails closed if either the graph fixture or validator bytes drift. It writes candidate graphs **only** in pytest-provided temporary directories, invokes no network, and does not operate on canonical governance/evidence artifacts. A Git blob SHA-1 identifies a file's Git contents for this bounded experiment; it is not an authenticity proof or a signed custody receipt.

## Synthetic case contract

| Case | Mutation | Expected structural result |
| --- | --- | --- |
| `AB-S0` | Unmodified reference fixture | PASS STRUCTURAL ONLY |
| `AB-S1` | Unsupported identifier references non-existent evidence | REJECT |
| `AB-S2` | Drop required `SUPPORTS` edge | REJECT |
| `AB-S3` | Trigger a defeater while leaving applicability `CURRENT` | REJECT |
| `AB-S4` | Add duplicate-root supporting evidence without a dependency edge | REJECT |
| `AB-S5` | Same duplicate-root support with explicit `SHARES_SOURCE_ROOT` edge | PASS STRUCTURAL ONLY; **not independent corroboration** |

These are a selected subset of existing validator semantics, designed to test entry-point parity. They do not implement the 11-family Agent Instrument study bank in the terminology candidate and must not be represented as 11 completed experiments, independent observations, or novel security controls. Do not conflate `PASS STRUCTURAL ONLY` with truth, independently verified source attribution, or action authorization.

## Test and audit acceptance boundaries

1. Manifest binds the exact reference graph and validator bytes through the source blob SHA checks.
2. The two surfaces return identical accept/reject outcomes for all six cases, with expected error substrings for failures.
3. Cases expecting structural pass preserve their uncertainty and non-authorizing claim class; they establish no real-world truth.
4. A CLI import/environment failure, missing dependencies, or source drift is a failed or blocked **test setup** and must not be counted as a graph rejection.
5. The CI report must bind to the *exact branch head* and enumerate passed, failed, skipped, and pending suites. Other workflow failures are not waived even if these seven checks pass.
6. A full B-FIXED interface and C-INSTRUMENT implementation remain separately scoped and cannot inherit this test's `PASS` as efficacy evidence.

## Unresolved decisions and next experiment design

- Are there other existing query/orchestration interfaces that make even the fixed-workflow proxy redundant? Inventory before any further code.
- Design fair **A-DIRECT vs B-FIXED full workflow** capability parity with equal feedback/branching and permissions. The CLI proxy does **not** satisfy this requirement.
- Before any C arm, lock synthetic test oracles, distinct held-out task structures, model/configuration, budget, randomization, history/no-history factors, adjudicator status, predeclared effect threshold and uncertainty/sampling plan. All are **UNSET**.
- A complete experiment must preserve the stronger prior-art/comparator and scientific claim ceiling in #1570 and the [general DGAF comparative governance benchmark](../qa/COMPARATIVE_GOVERNANCE_BENCHMARK_SPEC.md).

**Current expected claim ceiling:** internal engineering source-lock and validator-entry-point parity only, if and when tests run and report PASS for the exact commit. Before that, **TESTS NOT VERIFIED**. `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`; `HIGH_ASSURANCE=NOT_AUTHORIZED`; `AUTHORIZATION_EFFECT=NONE`.

**Admission:** DRAFT / NON-ADMITTING until signed commits, exact-head checks, protected-main policy and required reviews are satisfied. CI failures must stay visible.

## Existing fixed attribution-query pipeline — reuse-first expansion (2026-11-09)

**Discovery:** `scripts/claimgraph_attribution_query.py` already implements a bounded deterministic sequence: validate the ClaimGraph → validate caller-supplied attribution observations → classify supporting evidence attribution → emit an explicitly non-truth, non-authorizing result. It also has a CLI with three meaningful outcomes: `0=complete`, `2=partial`, and `1=invalid/error`. This is **not an independently implemented policy engine or a new Agent Instrument**.

Rather than build a second runtime, `tests/test_agent_instrument_existing_attribution_workflow.py` compares:

- **A direct:** existing `validate_claim_graph` then `query_attribution` called through Python (the query validates again).
- **B incumbent fixed query:** existing `claimgraph_attribution_query.py` CLI called on copied graph/observation fixtures using a temporary directory.
- **C instrument:** NOT IMPLEMENTED.

All tests pin the unmodified `claimgraph_attribution_query.py` Git blob `e3ed75a9e3a0eb6b4a01754894df32bf10985b2a` from protected main `1a95b94332dffb404c5a3ce026d70781a8c10b90`, and use the existing synthetic reference graph and its current validator contracts. This protects against silent query drift but is **not** an independently signed artifact or proof of source trust.

Nine new deterministic cases (`ATTR-01`–`ATTR-09`) cover: internally classified complete support; missing attribution with **partial exit 2, not PASS/admission**; external claimed/unverified evidence; externally *reported* independent evidence that remains `independence_effect=NONE`; forged internal independence; unknown evidence ID; graph lacking a support relation; duplicate attribution; and reported independent status without a required adjudication reference. Direct and fixed CLI outputs must agree byte-semantically as JSON, including error text and `truth_effect=authorization_effect=independence_effect=NONE` on accepted observations. Neither may mutate source inputs.

**Scope ceiling:** This is a *useful existing fixed-workflow baseline for read-only ClaimGraph attribution*, not a complete workflow for `add_claim`, `attach_evidence`, `challenge`, `fork` or `compare`. It does not match the proposed C arm on those unimplemented capabilities, and repeats the validator on A so **cost/latency parity is not established**. No model, agent, usability, transfer, or independent-performance trial has occurred. Prefer this existing workflow rather than cloning its logic.

**Focused command when dependencies are available:**

```bash
python -m pytest -q tests/test_agent_instrument_ab_baseline_smoke.py tests/test_agent_instrument_existing_attribution_workflow.py
```

**Verification gate:** the new source requires exact-head hosted lint/type and pytest readback before any claim of `TESTED`. A fixed-workflow behavioral parity PASS is a bounded deterministic engineering observation, not a justification for creating the C Agent Instrument interface. The unchanged root CI/security/signature/review blockers still apply.
