# Owner-private DGAF Governance Console Companion

**Status:** ACTIVE / OWNER-PRIVATE / READ-ONLY  
**Lifecycle:** DERIVATIVE  
**Scientific-state effect:** NONE  
**Authority effect:** NONE  
**Reconciliation input:** protected `main` at `9ef99ac7ed803609b4a7a4eb2b98bab328f853cc`  
**Reconciliation event:** post-#851/#854/#855 Epoch 002 locked-result and interpretation-tooling reconciliation

## Purpose

The owner-private DGAF Governance Console is a companion presentation surface for inspecting governance state, evidence boundaries, blockers, and admissible next actions. It provides creator and external-reader depths over one fact model, gate filtering, per-gate scope inspection, evidence-source search, and live GitHub freshness with a timestamped fallback.

This companion is a derivative projection of its named sources. Because it is versioned in the same repository, the reconciliation input above is provenance for this revision rather than a standing claim about the current protected-main SHA; exact current protected-main identity must be read from Git at use time.

The private console is not a governance authority, evidence store, authorization surface, or scientific transition mechanism. The private URL and access identifiers are intentionally omitted from this public repository.

## Truth boundary

The console must preserve the canonical High-Assurance boundary:

`PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 / CANONICAL DGAF EFFICACY NOT ESTABLISHED`

It separately represents the Track A Epoch 002 state:

- collection authorization: ACCEPTED;
- blinded collection: COMPLETE at 50 paired seed units / 2,250 observations;
- dataset lock: ESTABLISHED;
- bounded unblinding: AUTHORIZED for controlled mapping release/decryption only;
- Stage-1 predecessor materializer: ACCEPTED via PR #713;
- Stage-2 predecessor operator materialization bundle: ACCEPTED via PR #715;
- Stage-1 locked-archive representation repair: ACCEPTED via PR #794;
- Stage-2 accepted-lineage rebind: ACCEPTED via PR #797, bound to materializer commit `cf32a62bbf08a1b8db39709f4989be1be800d64e` / blob `3a825b026423952c2844cb18664eb6395b72fdc1`;
- real materialization evidence: ESTABLISHED / ACCEPTED via PR #824;
- materialization receipt: ESTABLISHED via creation-only PR #826;
- locked-analysis runner tooling: ACCEPTED via PR #831;
- primary-analysis authorization: ACCEPTED / LOCKED_PRIMARY_ANALYSIS_ONLY via PR #828;
- primary analysis: EXECUTED_LOCAL under the bounded accepted authorization;
- locked-analysis result receipt: ESTABLISHED via creation-only PR #851;
- repository/current-state reconciliation: ACCEPTED via PR #854;
- interpretation/adjudication tooling: ACCEPTED / NON-EXECUTING via PR #855;
- interpretation execution: NOT RUN;
- `INTERPRETATION_NOTE`: NOT ESTABLISHED;
- independent validation: NOT ESTABLISHED.

Track A completion counts must never be rendered as canonical High-Assurance scientific N.

## Integration contract

- `app/lib/governance.ts` is the public application's bounded presentation-state model.
- `docs/CURRENT_STATE.md` is the primary current-facing repository summary.
- `docs/PROJECT_STATUS.md` is a compatibility entrypoint only.
- The DGAF Operational Control Center in Notion is the interpreted governance mirror.
- GitHub remains authoritative for repository, commit, issue, PR, and CI identity.
- Runtime reachability remains operational evidence only.
- Missing or failed live refresh retains the last timestamped snapshot and must not promote or negate a governance predicate.

## Current next action

The console should present **bounded interpretation/adjudication** as the next frontier. The locked primary analysis has executed locally and the creation-only content-addressed `LOCKED_ANALYSIS_RESULT_RECORD` is accepted. PR #855 accepted the fail-closed interpretation tooling, but interpretation itself has not run and no `INTERPRETATION_NOTE` exists. The numerical estimate, interval, and classification remain operator-local; the next state-changing action must revalidate the retained result bytes and frozen preregistration before preparing a separate content-addressed interpretation-note candidate.

## Access and validation

The hosted companion is owner-only with no external viewers or groups. Unauthenticated access returns HTTP 401. The deployed HTML, JavaScript, and CSS assets were successfully retrieved through authenticated owner access; invariant tests preserve PRE-FREEZE, FAIL-CLOSED, NOT AUTHORIZED, canonical N=0, efficacy NOT ESTABLISHED, live-refresh/fallback separation, and read-only operation.

No public deployment or repository visibility change is authorized by this record.
