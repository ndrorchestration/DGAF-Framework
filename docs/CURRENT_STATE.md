---
status: ACTIVE
authority: repository_current_state_entrypoint
owner: DGAF/PDMAL control plane
last_verified: 2026-09-26
checkpoint_source_pr: 1050
checkpoint_source_main: 0cc79245f30f01f0b2d98c870589318fc7c69494
checkpoint_parent_main: bda0f52dc97696fc95fbb93e10f5b945163bc181
current_status_addendum: docs/status/DGAF_CURRENT_RECONCILIATION_2026-09-26.md
current_status_pointer: docs/status/CURRENT.md
self_application_controller_issue: 1022
external_review_controller_issue: 929
canonical_high_assurance_empirical_n: 0
canonical_dgaf_efficacy: NOT_ESTABLISHED
independent_validation: NOT_ESTABLISHED
external_validation: NOT_ESTABLISHED
high_assurance: NOT_AUTHORIZED
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
---

# DGAF-Framework / PDMAL — Current State

This is the current-facing repository entrypoint for DGAF state. GitHub remains authoritative for source, commits, pull requests, CI, retained artifacts, and issue controllers. Notion remains a governance mirror and planning surface, not a replacement for protected-main Git evidence.

For the newest accepted status addendum, see [`docs/status/CURRENT.md`](status/CURRENT.md), which routes to [`docs/status/DGAF_CURRENT_RECONCILIATION_2026-09-26.md`](status/DGAF_CURRENT_RECONCILIATION_2026-09-26.md).

## Current hard boundary

| Area | Current state |
|---|---|
| Protected repository `main` | Read from Git at use time. The accepted #1050 checkpoint readback was `0cc79245f30f01f0b2d98c870589318fc7c69494`. |
| Canonical High-Assurance program | `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0` |
| Canonical DGAF efficacy | `NOT_ESTABLISHED` |
| Independent validation | `NOT_ESTABLISHED` |
| External validation | `NOT_ESTABLISHED` |
| High-Assurance authorization | `NOT_AUTHORIZED` |
| Scientific-N increment | `0` |
| Self-application controller | Issue #1022 remains open. |
| External-review controller | Issue #929 remains open. |

## Canonical High-Assurance provenance boundary

This section is retained for control-state consistency tooling. It binds the active High-Assurance apparatus lineage without promoting current DGAF efficacy or external-validation state.

- main: read from protected Git at use time; #1050 checkpoint readback was `0cc79245f30f01f0b2d98c870589318fc7c69494`
- apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- candidate identity: `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED`
- deployment identity: historical exact-scope runtime evidence only; not a current High-Assurance authorization or efficacy claim

## Accepted current checkpoint

PR #1050 accepted a bounded current-state reconciliation addendum after:

- PR #1049 accepted same-system cold-start adjudication for the DGAF-on-DGAF self-application lane;
- PR #1041's body was refreshed to its actual current head while preserving its prospective, draft, non-authorizing boundary;
- protected `main` was read back and verified at the #1050 checkpoint;
- the remaining large-entrypoint documentation debt was explicitly preserved rather than silently overwritten.

PR #1050 is documentation/routing evidence only. It does not create a new self-application execution, new artifact, independent replay, external validation, scientific efficacy evidence, scientific-N increment, High-Assurance authorization, or controller closure.

## Self-application lane status

The #1022 DGAF-on-DGAF self-application benchmark has advanced through internal same-system engineering checkpoints, including cold-start manifest/scaffold/schema/validator/builder/materializer, CI artifactization, same-system execution, retained execution artifactization, and same-system adjudication.

Current interpretation:

- implemented: yes, for the accepted same-system engineering slices;
- tested: yes, for exact accepted heads and CI gates associated with those slices;
- independently verified: no;
- externally validated: no;
- scientifically established efficacy: no;
- admissible next evidence-changing step: external or independently retained replay/evidence under the appropriate controller, not self-promotion from same-system evidence.

## Track A / PDMAL boundary

Track A Epoch 002 remains closed for its exact preregistered scope as bounded same-system, nonindependent work. Operator-local results and interpretation records do not establish canonical DGAF efficacy, independent validation, external validation, production certification, or High-Assurance authorization.

Historical Track A details remain evidence-bound to their exact accepted commits, receipts, artifacts, and issue records. They should not be read as current promotion evidence unless a later governed record explicitly authorizes that interpretation.

## AOSS / external-review frontier

AOSS Stage-A handoff apparatus exists, but external review remains not executed. Issue #929 controls reviewer engagement, independence disclosure, returned evidence, and any later admissible external-review interpretation.

Internal CI, same-system replay, owner review, draft packets, or documentation reconciliation do not satisfy #929.

## Active documentation surfaces

Use this order when reading DGAF status:

1. protected `main`, pull requests, CI, retained artifacts, and issue controllers;
2. [`docs/status/CURRENT.md`](status/CURRENT.md) for the latest accepted status addendum pointer;
3. this file for the repository-facing state boundary;
4. Notion Operational Control Center for interpreted planning/state mirrors;
5. historical pages only for their exact dated scope.

## Remaining documentation debt

The #1050 addendum is accepted, but additional repository entrypoints still require periodic reconciliation whenever protected `main`, controller issues, or evidence boundaries move. In particular, broad historical details should remain evidence-bound and should not be rewritten as current facts unless the exact source identity and claim ceiling are preserved.

## Non-transfer rule

Implementation, tests, CI success, artifact retention, documentation status, UI presentation, operator-local execution, same-system replay, independent review, external validation, scientific efficacy, production certification, and High-Assurance authorization are separate evidence states. None transfers to another without an explicit governed rule and supporting evidence.
