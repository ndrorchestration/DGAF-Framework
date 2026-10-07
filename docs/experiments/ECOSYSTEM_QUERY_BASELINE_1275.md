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
| --- | --- | --- | --- | --- |
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

## External reconciliation tranche

Experiment 1 now accepts an externally supplied, non-authorizing reconciliation observation with the following exact fields:

```json
{
  "schema_version": "ECOSYSTEM_LIVE_RECONCILIATION_V1",
  "observed_at": "<observation timestamp>",
  "pointer_source_observation_commit": "<embedded pointer source SHA>",
  "live_repository_commit": "<observed DGAF repository tip SHA>",
  "container_commit": "<commit containing/using the pointer>",
  "evidence_url": "<provenance reference>"
}
```

The contract is intentionally scoped to **DGAF repository-tip reconciliation only**. A successful match does not establish freshness for ACP, Notion, Tektite projections, Drive, runtime state, or any independent-validation claim.

The query therefore reports both:

- `requires_dgaf_repository_reconciliation`; and
- `cross_surface_reconciliation_not_established`.

It also accepts UTF-8 JSON with or without a BOM so Windows/PowerShell-generated observations remain portable.

### Real observation — 2026-10-03

A Remote Desktop Commander observation of `origin/main` supplied:

- embedded pointer source: `c4f8fda24d2d44c47d7de8c77fcbbd3d478f5a91`;
- observed `origin/main`: `db0256859866605647e3c339ee3646a8f5007ed3`;
- experiment container/head at observation: `6b06e4cfad22bbd30226abe1d0069ee92dddf1f4`.

The query returned:

```text
scope=DGAF_REPOSITORY_TIP_ONLY
state=STALE_SOURCE_ADVANCED
requires_dgaf_repository_reconciliation=true
cross_surface_reconciliation_not_established=true
exit=2
```

This is the expected fail-closed outcome: the embedded pointer is not current for the observed DGAF repository tip.

No scientific, efficacy, independent-validation, High-Assurance, mutation-authority, or production-executor status changed.

## Post-tranche comparison

The reconciliation tranche improves machine answerability for a narrow subset of the eight baseline questions:

- Question 2 gains an explicit machine-readable indication that Tektite/AOSS consumer bindings are historical relative to the observed DGAF tip rather than silently current.
- Question 6 remains strongly machine-answerable from receipt schema semantics.
- Question 8 can now distinguish a concrete DGAF repository-tip mismatch from the broader unresolved Notion/cross-surface comparison problem.

The tranche does **not** yet solve Questions 1, 3, 4, or 5, and does not fully solve Questions 2, 7, or 8.

Therefore Experiment 1 has demonstrated a bounded reduction in ambiguity around repository-tip freshness, but **program-level benefit remains NOT ESTABLISHED**. Human operational-time and human-review-survival baselines remain unmeasured.

## Public-claim evidence enumeration tranche

The query layer now exposes the existing Tektite v0.1 evidence-ledger seed as a bounded public-claim evidence view.

The output is explicitly labeled:

```text
scope=TEKTITE_V0_1_EVIDENCE_LEDGER_SEED_ONLY
completeness=NOT_ESTABLISHED
```

This prevents the presence of three ledger rows from being interpreted as a complete inventory of every public-facing claim.

The current seed contains three entries, each preserving:

- artifact;
- source surface;
- supported claim;
- explicitly unsupported claim;
- authorization effect;
- public link when one exists.

The current seed also exposes one discoverability gap:

```text
AI Evidence Audit positioning → public_link missing
```

A missing public link is **not** classified as missing evidence or a false claim. It is reported only as missing public evidence discoverability from this seed.

### Baseline Question 1 update

Question 1 — “Which public-facing claims currently lack direct supporting evidence?” — improves from a manual ledger read to machine enumeration of the **Tektite seed subset**, but remains **PARTIAL** because:

- completeness across all public surfaces is not established;
- the seed does not prove that every public claim has been registered;
- public-link presence is not equivalent to evidence validity;
- broader claim/evidence reconciliation still requires the owning claim/evidence authorities.

Program-level benefit remains NOT ESTABLISHED.

## Control-to-test reference heuristic tranche

The query layer now automates the same direct-reference heuristic used during the original baseline characterization of core-component primary artifacts.

The output is explicitly labeled:

```text
scope=DIRECT_TEST_REFERENCE_HEURISTIC_ONLY
coverage=NOT_ESTABLISHED
```

The scan:

- reads registered K1–K8 primary artifacts from `DGAF_CORE_COMPONENT_REGISTRY.v1.json`;
- searches root-level `tests/test_*.py` files for either the full artifact path or artifact stem;
- reports direct test-file mentions;
- reports artifacts with no direct mention;
- excludes `tests/test_query_ecosystem_state.py` so the measurement tool cannot create its own evidence merely by naming an artifact in its tests.

Current result:

```text
artifacts_without_direct_mentions:
  docs/EPISTEMIC_EVIDENCE_STANDARD.md
```

This remains a **candidate coverage gap only**. A direct textual reference is neither necessary nor sufficient proof of meaningful test coverage, and absence of a direct reference is not proof that an artifact is untested.

### Baseline Question 4 update

Question 4 — “Which active controls lack executable tests or retained verification?” — improves from a one-off manual reference scan to repeatable machine output for the registered core-component primary-artifact subset.

It remains **PARTIAL / GAP** because:

- the scan is reference-based, not semantic coverage analysis;
- assurance components and every governed profile are not yet mapped to executable verification evidence;
- retained CI/run evidence is not normalized into the same query;
- no “tested” or “untested” claim is produced from this heuristic alone.

Program-level benefit remains NOT ESTABLISHED.

## Notion current-answer routing tranche

Q3 characterization confirmed that page-level currentness is too coarse: a current Notion page may intentionally preserve historical statements for provenance. The experiment therefore does not classify entire pages as current or historical.

The query now accepts an external record-level observation:

```text
schema=ECOSYSTEM_NOTION_ROUTING_OBSERVATION_V1
scope=EXTERNAL_NOTION_ROUTING_OBSERVATION_ONLY
completeness=NOT_ESTABLISHED
```

Each observed record carries an explicit classification, a current-answer eligibility boolean, a routing basis, and the current authority route. Historical and superseded classifications are forbidden from being marked current-answer eligible.

The observation remains external input rather than a checked-in mirror of Notion. This avoids creating another SSOT and preserves Notion as the registry/control-plane source for its own routing semantics.

### Real Notion characterization — 2026-10-04

The connected Notion workspace explicitly states:

- ACP #117/#118 "active blocker" language is retained as event-time history but is no longer the current interpretation for the bounded lower-assurance disposable-repository profile;
- the current routing matrix establishes the bounded local-test executor only for its tested opt-in disposable-repository scope;
- stronger guarantees remain not established;
- "current beats historical" and Historical & Superseded Records remains the archive/router for provenance.

The external observation therefore classifies:

```text
acp-117-118-old-blocker-language
  classification=SUPERSEDED_PROVENANCE
  current_answer_eligible=false

acp-bounded-local-test-executor
  classification=CURRENT_BOUNDED_STATE
  current_answer_eligible=true
```

These two records are a bounded sample, not a complete Notion inventory.

### Baseline Question 3 update

Question 3 — "Which current artifacts still describe superseded blockers or architecture?" — now has a machine-enforceable distinction between sampled superseded provenance and sampled current bounded state.

It remains **PARTIAL** because:

- the observation covers selected records, not every Notion assertion;
- page-level labels are intentionally insufficient;
- current repository truth still requires the owning GitHub/runtime authority where applicable;
- observation completeness remains `NOT_ESTABLISHED`.

Program-level benefit remains NOT ESTABLISHED.

## Public claim evidence linkage tranche

Q1 uses a read-only derived receipt rather than a canonical public-claim registry.

Contract:

```text
schema=PUBLIC_CLAIM_LINKAGE_OBSERVATION_V0
receipt=public-claim.evidence-linkage.v0-candidate
observation_authority=CALLER_SUPPLIED_NOT_REVERIFIED
```

The current frozen `github.profile` observation is:

`docs/experiments/fixtures/PUBLIC_CLAIM_LINKAGE_GITHUB_PROFILE_2026-10-04.json`

Current surface binding:

- profile source version: `4bfd33093b3a2875101d8dd687f6647183538d7b`;
- README blob: `63b2836f19f03a2c9203c10e798e74c9e27f9114`;
- public-surface manifest state: `RECONCILED / PASS`;
- `surface_release_gate_effect=NONE`.

The bounded current-profile sample contains eight material observed claim families:

- 6 `DIRECT_EVIDENCE_LINKED`;
- 2 `INDIRECT_OR_SUMMARY_ONLY`;
- 0 `NO_DIRECT_EVIDENCE_LINK`;
- `direct_linkage_complete=false`;
- `linkage_state=OBSERVED_WITH_LINKAGE_GAPS`.

The two summary-only claims are:

- absence of an accepted live CEP paired provider result;
- Tektite callback current-remediation versus historical-exposure state.

Those statements currently depend on issue/deployment state that is not representable by the existing project-file-only evidence-reference contract. The experiment therefore preserves them as summary-only rather than manufacturing a direct file link. A typed issue-state reference must be designed and governed separately if later evidence justifies extending the contract.

The directly linked sample covers bounded DGAF Epoch 002 state and claim ceilings, AOSS external-review status, ACP bounded-executor boundaries, the frozen CEP 89→1 / 32,471→268 catalog characterization, and Tektite projection/non-authority boundaries.

All receipt effects remain:

```text
truth_effect=NONE
authorization_effect=NONE
scientific_state_effect=NONE
evidence_authority_effect=NONE
```

### Baseline Question 1 update

Question 1 — "Which public-facing claims currently lack direct supporting evidence?" — now has a reproducible bounded answer for the sampled current `github.profile` claim families.

It remains **PARTIAL** because:

- the observation is a bounded material-claim sample, not complete public-profile enumeration;
- surface `PASS` does not imply claim-evidence completeness;
- issue/deployment-backed current-state claims remain summary-only under the path-only direct-linkage contract;
- caller-supplied claim extraction is not itself evidence truth;
- other public surfaces are not covered by this observation.

Program-level benefit remains NOT ESTABLISHED.
