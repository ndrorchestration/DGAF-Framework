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
