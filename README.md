# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** is an experimental framework for governed multi-agent AI systems. It treats **capability, evidence, verification, authority, and permission to act as separate machine-relevant states** rather than assuming one implies another.

In plain English: an agent may be able to do something and still be blocked from doing it; a system may pass engineering tests and still be blocked from claiming that it is empirically validated.

## Current status entrypoints

Read current DGAF state in this order:

1. protected GitHub `main`, pull requests, CI runs, artifacts, and issue controllers;
2. [`docs/status/CURRENT.md`](docs/status/CURRENT.md), which points to the latest accepted status addendum;
3. [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md), the repository-facing state boundary;
4. Issue #1022 for DGAF-on-DGAF self-application status;
5. Issue #929 for the external-review controller.

The latest accepted documentation checkpoint is PR #1050, which added [`docs/status/DGAF_CURRENT_RECONCILIATION_2026-09-26.md`](docs/status/DGAF_CURRENT_RECONCILIATION_2026-09-26.md). That addendum is documentation/routing evidence only; it does not promote scientific, independent, external, production, or High-Assurance state.

## Current hard boundary

DGAF remains:

```text
PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
SCIENTIFIC_N_INCREMENT=0
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
EXTERNAL_VALIDATION=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

Internal same-system engineering evidence has advanced materially, especially through the #1022 cold-start/self-application chain ending most recently in the accepted #1049 same-system adjudication record and #1050 documentation reconciliation checkpoint. That evidence is useful engineering assurance, but it is not independent validation or external validation.

Human-readable boundary: canonical DGAF efficacy, independent validation, and external validation remain NOT ESTABLISHED. High-Assurance remains NOT AUTHORIZED; scientific-N increment remains 0. These are current boundary summaries, with `docs/status/CURRENT.md` pointing to the accepted detailed record.

## Five-minute evaluator orientation

If you are evaluating DGAF as an AI-systems, governance, or research-engineering portfolio artifact, use this path before reading the full control history.

**1. Start with the problem.** DGAF asks whether an AI system's current evidence and authority actually support the claim or action it is about to make. Capability alone does not grant permission, and passing engineering checks does not establish empirical efficacy.

**2. Inspect what is implemented.** The repository contains governance logic, provenance/source binding, deterministic validators, negative controls, CI, experimental tooling, custody machinery, blinded-data infrastructure, presentation/control-center surfaces, and a partial machine-readable assurance catalog. For implementation detail, start with [`README.technical.md`](README.technical.md) and [`README.governance.md`](README.governance.md).

**3. Read the current state from its owning record.** [`docs/status/CURRENT.md`](docs/status/CURRENT.md) and [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) are the current repository-facing entrypoints. Historical records are authoritative only for the exact scope, identity, and date they bind.

**4. Understand the self-application frontier.** DGAF has internal same-system tests, retained artifacts, and adjudication records for the DGAF-on-DGAF self-application lane. These show controlled engineering progress. They do not establish same-system independence, independent validation, external validation, canonical efficacy, or High-Assurance authorization. Issue #1022 remains open.

**5. Understand the external-validation frontier.** The external-review handoff apparatus exists, but external reviewer engagement and independently retained evidence remain unexecuted. Issue #929 controls actual reviewer engagement and returned evidence.

**6. Evaluate the separation discipline.** The central engineering/research claim is not that DGAF is already proven. It is that the repository makes state transitions, evidence classes, provenance, authorization, assurance coverage, and non-claims explicit and machine-checkable enough to prevent one category from silently substituting for another.

## What this demonstrates

Within the evidence boundaries documented in this repository, DGAF demonstrates practical work in:

- multi-agent governance and explicit authority/state-transition design;
- provenance, source/evidence binding, and custody controls;
- deterministic validation, negative controls, and fail-closed CI;
- prospective/blinded experiment infrastructure and reproducibility tooling;
- separation of implementation, testing, verification, independent verification, authorization, execution, and empirical support;
- documentation and public translation of a complex technical control system without upgrading its evidence state;
- operator/auditor UI design that exposes blockers and reachable transitions without inventing readiness percentages;
- machine-readable assurance inventorying that distinguishes mapped controls, required branch contexts, and unclassified coverage gaps;
- same-system self-application scaffolding, execution, artifactization, and adjudication with explicit non-promotion boundaries.

## Core model

A simplified DGAF control loop is:

```text
Evidence + provenance
        ↓
Epistemic / verification state
        ↓
Claim and action authority
        ↓
Governed agent formation
        ↓
Execution
        ↓
New evidence + trace
        └────────────→ updated governance state
```

The intended invariant is that **capability, evidence, verification, and authorization cannot silently substitute for one another**.

The same rule applies to presentation and assurance inventory: **UI state does not create authority, and catalog membership does not create branch-protection requiredness or scientific evidence**.

## Research program boundary

DGAF separates prospective evaluation by workload instead of treating one experiment as proof of the entire framework.

Track A Epoch 002 is closed for its exact preregistered same-system/nonindependent scope. AOSS Stage-A external review remains controlled by #929 and is not executed. The #1022 self-application benchmark remains open and internal unless and until externally retained evidence is produced and adjudicated.

## How to review safely

When reviewing or extending DGAF:

- distinguish implemented, tested, verified, independently verified, externally validated, and scientifically established;
- do not infer efficacy from CI, same-system execution, documentation, UI, or operator-local results;
- bind every claim to exact commits, PRs, issues, artifacts, and workflow runs;
- treat missing evidence as a blocker, not as permission to promote;
- preserve `N=0`, `NOT_ESTABLISHED`, and `NOT_AUTHORIZED` states unless a governed record explicitly changes them.

## Project structure

- `docs/status/` — current status addenda and routing pointers.
- `docs/CURRENT_STATE.md` — repository-facing current-state boundary.
- `README.technical.md` — technical orientation.
- `README.governance.md` — governance/control-plane orientation.
- `registry/` — machine-readable schemas, manifests, catalogs, and evidence contracts.
- `scripts/` — deterministic validators, builders, materializers, and audit helpers.
- `tests/` — regression, contract, governance, self-application, and assurance tests.

## Non-transfer rule

Implementation, tests, CI success, artifact retention, documentation status, UI presentation, operator-local execution, same-system replay, independent review, external validation, scientific efficacy, production certification, and High-Assurance authorization are separate evidence states. None transfers to another without an explicit governed rule and supporting evidence.
