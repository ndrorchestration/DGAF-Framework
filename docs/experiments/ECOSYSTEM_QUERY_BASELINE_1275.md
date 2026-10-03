# Experiment 1275 — Queryable Ecosystem State Baseline

Status: **BASELINE CHARACTERIZATION / HYPOTHESIS**

This record measures the current answerability of the fixed eight-question baseline before broader reconciliation automation. It does not establish live currentness, independent validation, efficacy, High Assurance, or any new execution authority.

## Fixed ceilings

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

The current `ECOSYSTEM_STATE_POINTER_V1` additionally fixes:

```text
LIVE_REPOSITORY_MUTATION=NOT_AUTHORIZED
PRODUCTION_EXECUTOR=NOT_ESTABLISHED
```

## Baseline source set

Primary machine-readable sources used in this pass:

- `registry/ecosystem_state_pointer.current.json`
- `registry/aoss_stage_a_readiness_semantic_source_v1.json`
- `registry/tektite_public_status_semantic_source_v1.json`
- `docs/architecture/DGAF_CORE_COMPONENT_REGISTRY.v1.json`
- `docs/CLAIM_EVIDENCE_INDEX.md`
- `docs/research/STRUCTURAL_EPISTEMICS_EVIDENCE_GRAPH_SCHEMA.json`
- `scripts/validate_structural_epistemics_claim_graph.py`
- `schemas/execution_receipt.schema.json`
- `docs/governance/ECOSYSTEM_STATE_POINTER_V1.md`
- Notion Capability Graph and current reconciliation records

The embedded pointer was observed at `2026-10-01T23:01:00Z` against DGAF source observation commit `c4f8fda24d2d44c47d7de8c77fcbbd3d478f5a91`. It is intentionally a `HISTORICAL_SNAPSHOT` and has `live_reconciliation.status=NOT_EMBEDDED`.

## Eight-question baseline

| # | Question | Current machine support | Baseline finding | Remaining gap |
|---|---|---|---|---|
| 1 | Which public-facing claims currently lack direct supporting evidence? | PARTIAL | `CLAIM_EVIDENCE_INDEX.md` and the Tektite evidence ledger encode support/non-support boundaries, but there is no single query that enumerates every public claim against evidence. | Cross-surface public-claim enumeration. |
| 2 | Which Tektite projections depend on ACP/DGAF capabilities that are not established? | PARTIAL | The Tektite semantic-source manifest and pointer bind DGAF/ACP source authorities and fixed claim ceilings. | Live external reconciliation and explicit query from projected claim to capability state. |
| 3 | Which current artifacts still describe superseded blockers or architecture? | PARTIAL | Notion search for ACP #117/#118 returns mixed historical/current records; several current records explicitly mark older blocker language as superseded, while historical records retain it for provenance. | Machine distinction between event-time history and current-answer eligibility across all Notion records. |
| 4 | Which active controls lack executable tests or retained verification? | PARTIAL / GAP | A heuristic scan of core-component primary artifacts found direct test mentions for all listed code/schema artifacts except `docs/EPISTEMIC_EVIDENCE_STANDARD.md`. This heuristic is not proof of coverage or absence. | First-class control→test/evidence registry rather than filename/reference heuristics. |
| 5 | Which claims rely only on internally produced evidence? | PARTIAL | Structural Epistemics records evidence class, source roots and dependency roots; external-result contracts separately require producer/reviewer attribution and an independence basis. | A normalized producer/independence field/query across all claim records. |
| 6 | Which execution receipts can be mistaken for follow-on authority? | STRONG | `execution_receipt.schema.json` fixes `authority_effect=NONE` and `follow_on_authority=FRESH_ADJUDICATION_REQUIRED`; runtime and tests enforce the boundary. | No material schema gap identified in this pass. |
| 7 | Which state transitions require fresh adjudication? | STRONG for execution follow-on | Receipt schema, admission contract and PEP tests require fresh adjudication before consequential follow-on action. | Broader transition-to-adjudication query across every governed profile is not yet unified. |
| 8 | Which current Notion records materially disagree with current repository state? | GAP for live currentness | The pointer defines the authority/freshness boundary and explicitly refuses to claim live repository-tip currentness from the embedded snapshot. Notion keyword search can reveal candidate disagreement but cannot itself establish current repository truth. | External live reconciliation evidence and consumer-specific currentness query. |

## Control-test heuristic

The initial direct-reference scan over `DGAF_CORE_COMPONENT_REGISTRY.v1.json` found direct test-file mentions for the registered primary code/schema artifacts in K1–K8, with one notable exception:

- `docs/EPISTEMIC_EVIDENCE_STANDARD.md`: no direct filename/stem mention found in the heuristic scan.

This is a **candidate coverage gap only**. Documentation contracts may be tested indirectly, and direct string mention is neither necessary nor sufficient evidence of meaningful test coverage.

## Minimal query layer added by this experiment

`scripts/query_ecosystem_state.py` is a read-only view over existing state. It:

- validates the existing ecosystem pointer before answering;
- reports embedded historical scope separately from live currentness;
- preserves the exact fixed claim ceiling;
- exposes declared consumer bindings and semantic digests;
- exposes receipt non-authority semantics directly from the receipt schema;
- reports required consumers that are missing instead of inventing them;
- marks reconciliation as required when live currentness is absent.

It does **not** create a new state store and does not determine scientific, external-validation, efficacy, or authorization promotion.

## Measurement status

Primary metric A — human-review survival rate: **UNMEASURED at baseline**.

Primary metric B — human operational workload: **UNMEASURED at baseline**.

For this pass, machine execution time is available from command/test logs, but it is not a substitute for human workload. Historical human minutes are not backfilled.

## Verification environment note

A repository-wide `python -m pytest -q` attempt stops during collection on eight unrelated import/dependency errors in `experiments/pdmal_topology` and `packages/governed-repo`. The same eight collection errors were reproduced in a separate untouched detached worktree at `origin/main` / `db0256859866605647e3c339ee3646a8f5007ed3`, so this experiment does not treat them as regressions and does not widen scope to repair them.

The bounded state/query verification suite is evaluated separately.

## Initial falsification posture

Experiment 1 should be stopped or redesigned if the query/reconciliation layer:

- requires maintaining duplicate state;
- produces current-state answers without external reconciliation;
- requires substantial human correction to generated relationships;
- increases maintenance effort without reducing cross-surface reconstruction effort.

## Next measured comparison

Rerun these same eight questions after adding only the smallest missing reconciliation/query features. Compare:

- number of source surfaces manually consulted;
- unresolved ambiguities;
- human corrections;
- operator intervention count;
- whether a question can be answered from machine-readable state without widening claim scope.

A favorable result permits continuation. Implementation alone does not.
