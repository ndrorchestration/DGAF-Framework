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
