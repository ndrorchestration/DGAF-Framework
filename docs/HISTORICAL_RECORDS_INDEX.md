# DGAF Historical Records Index

DGAF preserves historical records because old evidence, candidate identities, experiments, terminology, and governance decisions remain useful for provenance. Historical preservation must not make an older record look like current authority.

## Reading rule

Before using an older DGAF record as evidence for a current claim, check:

1. the record's date and exact source identity;
2. whether a later record superseded its current-state interpretation;
3. whether the relevant candidate, protocol, artifact schema, treatment, deployment, or custody identity changed;
4. whether the evidence was engineering, diagnostic, empirical, self-attested, or independently verified;
5. whether the claim is still within the evidence ceiling of that record.

**Historical evidence does not silently transfer to current identities.**

For live state, use [`CURRENT_STATE.md`](CURRENT_STATE.md).

## Preserved status snapshots

| Record | Date | Classification | Use |
|---|---|---|---|
| [`historical/PROJECT_STATUS_2026-09-06.md`](historical/PROJECT_STATUS_2026-09-06.md) | 2026-09-06 | Historical current-state snapshot | Reconstruct the pre-Track-A-freeze project boundary and the then-current High-Assurance/P4/P7/P8/P9 sequence |

Additional dated governance and experiment records remain in their original directories. A dated filename or an older issue body should be treated as a snapshot unless it explicitly identifies itself as current authority.

## Important historical evidence classes

### Solo empirical epochs

The Solo track contains bounded developer/non-independent empirical evidence. Its results remain tied to the exact executed treatment and custody conditions.

- **Experiment 001** — retained primarily as apparatus-falsification evidence where intended treatment binding failed.
- **Epoch 003** — retained as negative evidence for its explicitly synthetic treatment variant.
- **Epoch 004** — retained as locked negative exact-treatment evidence; later source-bound audit found canonical seven-gate treatment fidelity was not established.

These records are not pooled into the prospective Track A experiment and do not establish canonical DGAF efficacy.

### Historical High-Assurance candidate evidence

Older runtime/candidate/deployment evidence remains valid only for the exact identities and predicates that produced it. Later candidate rotation, protocol repair, or apparatus changes do not inherit those results automatically.

### Dated governance drafts and checkpoints

Files with names such as `*_DRAFT_*`, `CURRENT_REPOSITORY_CHECKPOINT_<date>.md`, or dated closure plans should be read as their named checkpoint or design state unless a later governing record explicitly promotes them.

Examples include:

- [`governance/CURRENT_REPOSITORY_CHECKPOINT_2026-09-05.md`](governance/CURRENT_REPOSITORY_CHECKPOINT_2026-09-05.md)
- [`governance/P7_FINAL_BINDING_DRAFT_2026-09-05.md`](governance/P7_FINAL_BINDING_DRAFT_2026-09-05.md)
- [`governance/EVIDENCE_CHAIN_CLOSURE_PLAN_2026-09-07.md`](GOVERNANCE/EVIDENCE_CHAIN_CLOSURE_PLAN_2026-09-07.md)

Their historical statements must not override the current state merely because the files remain in the repository.

## Current-state hierarchy

For external readers, prefer this order:

1. [`../README.md`](../README.md) — public overview;
2. [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md) — industry-neutral terminology;
3. [`CURRENT_STATE.md`](CURRENT_STATE.md) — live project/evidence boundary;
4. exact gate, experiment, evidence, or governance artifact for the claim being reviewed;
5. historical snapshots only when reconstructing provenance.

## Preservation principle

DGAF documentation hygiene should normally **supersede or reclassify** historical evidence rather than rewrite it to match a newer state. Current-facing files should be updated; provenance-sensitive historical records should remain immutable or clearly marked as historical.

## Reader entrypoints after the README reorganization

The public [README](../README.md) presents the problem, governed-action mechanism, bounded demo, comparator result, release HOLD and known limits. Detailed experimental interpretation lives in the [research program explainer](RESEARCH_PROGRAM_EXPLAINER.md); implementation-versus-replay distinctions live in the [prototype maturity map](PROTOTYPE_MATURITY_MAP.md). Original issue/PR evidence remains source-authoritative at its exact identity and scope.

The migrated chronology below is preserved for **event-time provenance**. Descriptions of historical merged source are not statements that every later issue has been resolved, nor that a release or scientific claim has been authorized.

## Preserved selected repository engineering milestones (formerly in README)

### Selected historical engineering milestones

The following bullets are selected historical engineering milestones, not a complete list of current work. For the live gate and evidence state, use [`docs/CURRENT_STATE.md`](CURRENT_STATE.md); exact current protected-main identity is a Git fact and must be read at use time:

- **Decision Frontier — PR #776** is merged as a presentation-only Semantic Control Field component derived from canonical governance state.
- **Governance Map — PR #779** is merged and renders ordered escalation, explicitly named lateral relationships, and global field constraints without creating a second state engine.
- **State-Space Explorer V0 — PR #783** is merged and projects canonical stages into discrete `established`, `frontier`, and `blocked_by_predecessor` regions while preserving native predicate state and explicit model limits.
- **Bounded assurance catalog — PR #780** is merged with `coverage.status = PARTIAL_CORE_FAMILIES_ONLY`.
- **Workflow coverage-gap scanner — PR #782** is merged and reports workflow definitions not yet exactly bound by the catalog without inferring their role.
- **Recurring assurance expansion — PR #785** is merged and adds seven source-verified recurring assurance families while preserving partial coverage.
- **Current-facing authority/documentation reconciliation — PR #795** is merged; security, operations, pattern-registry, authority-matrix, bootstrap, and technical-reference surfaces now route current executable authority through functional `role.*` contracts while retaining personas as provenance.
- **Stage-1 retained-archive repair — PR #794** is merged and accepts the exact locked archive's harmless `./` flat-member representation without changing archive bytes or weakening unsafe-member rejection.
- **Stage-2 accepted-lineage rebind — PR #797** is merged and binds the operator bundle to accepted Stage-1 commit `cf32a62bbf08a1b8db39709f4989be1be800d64e` / blob `3a825b026423952c2844cb18664eb6395b72fdc1`.
- **AOSS Stage-A independent-validation handoff — PR #928** is merged and preserves the accepted historical external-review handoff without asserting that an independent review has occurred.
- **AOSS Stage-A current reviewer identity addendum — PR #1354** is merged and rebinds the current reviewer packet to evaluated implementation `9054fc14f4cb8ef7a1b627338b363ee3d9987bd1` while preserving the historical #928 handoff and all fail-closed acceptance predicates.

Those earlier engineering/presentation/assurance milestones did not establish materialization or primary-analysis authorization. Subsequent separately governed events advanced the lane: PR #824 admitted real non-secret materialization evidence, PR #826 established its immutable receipt, PR #831 accepted the fail-closed local analysis runner, PR #828 accepted bounded locked-analysis authorization, PR #835 accepted non-executing content-addressed result-admission tooling, PR #848 corrected the lifecycle-aware admission test, and PR #851 established the immutable locked-analysis result receipt. PR #872 separately established bounded interpretation admission at SAME_SYSTEM_NONINDEPENDENT scope. These events establish execution, result admission, and bounded interpretation at their exact scopes, but not canonical DGAF efficacy, independent validation, production certification, or High-Assurance authorization.

> **Canonical High-Assurance research status:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N = 0  
> **Track A Epoch 001:** PROSPECTIVE BLINDED COLLECTION COMPLETE · 50 paired inferential seed units · 2,250 blinded observations · DATASET LOCK ESTABLISHED  
> **Epoch 001 disposition:** protected mapping is **CRYPTOGRAPHICALLY UNRECOVERABLE** · primary analysis **UNANALYZABLE / NOT RUN**  
> **Successor Track A / Epoch 002:** custody, freeze, closure, bounded verification classification, collection authorization, dataset lock, bounded unblinding, materialization, immutable materialization receipt, locked-primary-analysis authorization, local locked analysis execution, and the content-addressed locked-result receipt are **ACCEPTED/ESTABLISHED AT THEIR EXACT SCOPES** · blinded collection **COMPLETE** at 50 paired seed units / 2,250 observations · interpretation/adjudication **EXECUTED / ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT**  
> **AOSS Stage-A external review:** HISTORICAL HANDOFF #928 + CURRENT IDENTITY ADDENDUM #1354 ACCEPTED · REVIEW NOT EXECUTED · ISSUE #929 OPEN · reviewer attribution / independence NOT VERIFIED · execution_allowed=false  
> **DGAF-on-DGAF self-application:** ISSUE #1022 OPEN · scaffold / same-system execution / same-system adjudication ACCEPTED THROUGH PR #1049 · independent replay under #929 OPEN · INTERNAL ENGINEERING VALIDATION ONLY · SCIENTIFIC_N_INCREMENT=0 · HIGH_ASSURANCE=NOT_AUTHORIZED  
> **Canonical DGAF efficacy:** NOT ESTABLISHED

