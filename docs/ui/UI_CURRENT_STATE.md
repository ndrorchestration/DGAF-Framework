# DGAF UI / Interface Current State

**Status:** CURRENT DOCUMENTATION / RECONCILED 2026-09-19  
**Authority class:** PRESENTATION / DOCUMENTATION ONLY  
**Reconciliation input:** protected signed/verified `main` `28e5591115899408463278b034571671173a4c83`  
**Scientific/control effect:** NONE  
**Canonical High-Assurance boundary:** `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`

This file is the current-facing documentation index for the DGAF interface workstream. It does not replace `docs/CURRENT_STATE.md`, `app/lib/governance.ts`, repository evidence, or the DGAF Operational Control Center. It records which interface concepts are accepted, which candidates are stale-lineage, and what must be reconciled before further UI implementation.

## Current truth the interface must project

Track A Epoch 002 has advanced beyond the state used when PR #849 was authored:

- collection: COMPLETE;
- dataset lock: ESTABLISHED;
- bounded unblinding: AUTHORIZED;
- controlled materialization + immutable receipt: ESTABLISHED;
- primary-analysis authorization: ACCEPTED / `LOCKED_PRIMARY_ANALYSIS_ONLY`;
- locked primary analysis: EXECUTED / RETAINED;
- `LOCKED_ANALYSIS_RESULT_RECORD`: ESTABLISHED via PR #851;
- interpretation/adjudication tooling: ACCEPTED via PR #855;
- interpretation execution: NOT RUN;
- `INTERPRETATION_NOTE`: NOT ESTABLISHED;
- canonical DGAF efficacy: NOT ESTABLISHED;
- independent validation: NOT ESTABLISHED;
- scientific-N increment: 0.

The active scientific frontier is therefore **interpretation/adjudication**, not primary-analysis execution.

## Accepted interface foundation

The following presentation architecture is accepted on protected main:

- Decision Frontier semantic control field;
- Governance Map;
- State-Space Explorer;
- semantic visual token system and non-color state grammar;
- public/external claim-ceiling treatment;
- accessibility foundations including skip-to-content, focus restoration, touch targets, responsive identity wrapping, reduced-motion handling, and forced-colors support;
- evidence-first Overview routing from merged PR #845: users are directed to Evidence before Governance interpretation.

These surfaces are projections only. They cannot create evidence, authorize a transition, establish efficacy, increment scientific N, or alter High-Assurance state.

## Closed provenance requiring current-main reconstruction

### PR #849 — Evidence provenance spine

Implementation intent remains accepted:

- derive the Evidence Spine from canonical `GOVERNANCE_STAGES`;
- show `EVIDENCE BOUNDARY` beside `DOES NOT ESTABLISH`;
- route explicitly from Verify / Evidence to Inspect / Governance;
- preserve responsive and forced-colors semantics.

Its exact historical head completed 19/19 returned repository workflow families successfully. PR #849 is now **CLOSED / UNMERGED / STALE-LINEAGE / DO NOT MERGE AS-IS** because protected main advanced through changes to `app/lib/governance.ts`, Decision Frontier, Governance Map, current-state records, and the Track A locked-result/interpretation frontier. The old candidate text that primary analysis had not yet run is no longer admissible.

Reconstruction requirement: replay only the presentation delta onto current protected main and consume the current canonical stage model, where locked analysis is established and interpretation/adjudication is the open frontier.

### PR #850 — Audience journey groups + mobile containment

Implementation intent remains accepted:

- **UNDERSTAND** — Overview;
- **VERIFY** — Evidence & Research;
- **INSPECT** — Governance, State Space, Agents & Formations;
- **OPERATE** — Control Room, Tools;
- closed mobile navigation must be removed from pointer/focus interaction;
- runtime status must remain explicitly scoped as observability, not governance authority.

Its stacked exact head completed all 10 returned workflow families successfully. PR #850 is now **CLOSED / UNMERGED / STACKED / STALE-LINEAGE / DO NOT MERGE AS-IS** because its base is #849. It must be reconstructed only after the Evidence tranche is rebound to current protected main.

## Provider/deployment boundary

Vercel preview creation for the recent UI candidates is currently blocked by the account daily deployment quota. This is provider/runtime evidence only. It is not a repository test failure, governance failure, authorization event, scientific-state change, or proof of deployment readiness.

## Required order before further UI expansion

1. Reconcile documentation across repository, Notion, and Drive mirrors.
2. Reconstruct the Evidence provenance-spine delta on current protected main.
3. Update all Evidence copy to the current interpretation/adjudication frontier.
4. Run fresh exact-head UI/build, regression, governance, truth-layer, and applicable repository checks.
5. Accept/merge only from current evidence.
6. Reconstruct the audience-journey/mobile-containment delta on the resulting accepted main.
7. Revalidate.
8. Only then resume new UI capability or visual refinement.

## Remaining design work after reconciliation

After the two stale-lineage candidates are resolved, the design workstream should move primarily into:

- progressive disclosure across public / professional / operator / scientific / auditor densities;
- skeptical first-time-user, hiring-reviewer, researcher, auditor, operator, and adversarial-safety testing;
- truth-bound stale/missing/ambiguous authority-data behavior;
- provenance traversal deeper than the current stage summary;
- final responsive, typography, spacing, and interaction refinement;
- current-production visual QA when provider deployment capacity is available.

Do not add new feature lanes while the current documentation or projection lineage is known to be stale.
