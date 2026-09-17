# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** is an experimental framework for governed multi-agent AI systems. It treats **capability, evidence, verification, authority, authorization, execution, and empirical support as separate machine-relevant states** rather than assuming that one implies another.

In plain English: an agent may be technically capable of an action and still be blocked from taking it; a system may pass engineering checks and still be blocked from claiming empirical validation.

## Five-minute evaluator orientation

1. **Start with the problem.** DGAF asks whether the evidence and authority that exist now actually support the claim or action a system is about to make.
2. **Inspect what is implemented.** The repository contains governance logic, provenance/source binding, deterministic validators, negative controls, CI, experimental tooling, custody machinery, blinded-data infrastructure, a Governance Command Center, and a machine-readable partial assurance catalog.
3. **Read current state from its owner.** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) is the live project/evidence entrypoint.
4. **Understand the scientific frontier.** Track A Epoch 002 collection is complete at 50 paired inferential seed units / 2,250 observations; dataset lock is established and bounded unblinding is authorized for controlled mapping release/decryption. Materialization tooling exists, but real materialization and its immutable receipt are not established; primary analysis is not authorized or run; scientific-N increment remains 0.
5. **Evaluate the separation discipline.** The project does not claim that DGAF is already proven. It demonstrates explicit, testable boundaries among implementation, evidence, verification, authorization, execution, presentation, and assurance coverage.

## Current repository engineering state

Protected signed/verified `main` is **`b1d91621bd73e70866d5ff8fd38fb98e440b30e9`**.

### Semantic Control Field / Governance Command Center

Three presentation-only tranches are accepted on protected `main`:

- **Decision Frontier — PR #776:** current governed state → evidence/provenance → blocking boundary → nearest admissible transition → unreachable transitions → consequence preview → receipt semantics.
- **Governance Map — PR #779:** ordered vertical escalation, explicitly named lateral relationships, and global field constraints derived from the canonical governance model.
- **State-Space Explorer V0 — PR #783:** discrete/categorical reachability over canonical stages, keeping native predicate state separate from derived `established`, `frontier`, and `blocked_by_predecessor` regions.

State-Space V0 deliberately does **not** assign continuous/manifold coordinates, readiness percentages, distance-to-authorization, success probability, scalar evidence quality, efficacy gradients, or inferred consequence/reversibility values. The tensor/manifold work remains a conceptual/formalization direction until exact continuous semantics exist.

These views are explanatory projections. They do not create governance authority or upgrade evidence.

### Repository assurance inventory

The repository also contains a bounded machine-readable assurance inventory:

- **PR #780:** `registry/audit_catalog.v1.json` plus deterministic validation;
- **PR #782:** deterministic discovery of current workflow definitions not exactly bound by accepted catalog implementation paths;
- **PR #785:** seven additional source-verified recurring assurance families.

The catalog remains explicitly **`PARTIAL_CORE_FAMILIES_ONLY`**. Current protected-main required status contexts are separately **PPTL CI**, **Governance CI**, and **PR Issue-State Keyword Guard**.

A cataloged recurring-assurance family is not automatically a required merge context. An `UNMAPPED` or `UNCLASSIFIED` workflow is an unadjudicated coverage gap, not proof that the workflow is non-assurance. **PR #784** was closed unmerged and its proposed workflow-role census is not accepted implementation.

## What DGAF demonstrates

Within the evidence boundaries documented in this repository, DGAF demonstrates practical work in:

- multi-agent governance and explicit authority/state-transition design;
- provenance, source/evidence binding, and custody controls;
- deterministic validation, negative controls, and fail-closed CI;
- prospective/blinded experiment infrastructure and reproducibility tooling;
- separation of implementation, verification, independent verification, authorization, execution, and empirical support;
- operator/auditor UX that exposes blockers and reachable transitions without converting categorical authority into a score;
- structural presentation of vertical escalation, lateral coupling, and global constraints without silently adding new semantics;
- machine-readable assurance inventorying that distinguishes mapped controls, merge-required contexts, and unclassified coverage gaps.

> **Canonical High-Assurance research status:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N = 0  
> **Track A Epoch 001:** prospective blinded collection complete · 50 paired inferential seed units · 2,250 blinded observations · dataset lock established · protected mapping cryptographically unrecoverable · primary analysis unanalyzable/not run  
> **Track A Epoch 002:** collection complete · dataset lock established · bounded unblinding authorized · materialization tooling accepted · real materialization not established · primary analysis not authorized/not run  
> **Canonical DGAF efficacy:** NOT ESTABLISHED  
> **Independent validation:** NOT ESTABLISHED

## Core model

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

The intended invariant is that **capability, evidence, verification, authorization, execution, presentation, and assurance classification cannot silently substitute for one another**.

## Current Track A scientific program

DGAF separates prospective evaluation by workload rather than treating one experiment as proof of the entire framework.

| Track | Current boundary |
|---|---|
| **A — Epoch 001** | Prospective blinded collection complete and dataset locked; protected mapping cryptographically unrecoverable; primary analysis unanalyzable/not run; retained as historical blinded evidence plus custody-design failure evidence. |
| **A — Epoch 002 successor** | Collection COMPLETE at 50 paired seed units / 2,250 observations; dataset lock ESTABLISHED; bounded unblinding AUTHORIZED for controlled mapping release/decryption only; materialization tooling ACCEPTED; real materialization and receipt NOT ESTABLISHED; primary analysis NOT AUTHORIZED / NOT RUN. |
| **B1 / B2 / B3** | Bounded non-empirical workload tracks; no framework-wide efficacy claim. |
| **C** | Non-empirical composition work; empirical execution remains separately governed. |

The current Epoch 002 scientific transition is:

`controlled real materialization`
`→ validated non-secret evidence admission`
`→ immutable materialization receipt`
`→ separate primary-analysis authorization`
`→ locked analysis`
`→ interpretation/adjudication`

No private key, passphrase, blinding secret, protected plaintext mapping, decrypted protected data, or other recoverable secret material belongs in GitHub, Notion, chat, CI inputs, workflow logs, or committed files.

## Internal terms in plain English

| Internal term | Public / industry-neutral translation |
|---|---|
| **Formation** | The set and structure of agents selected for a governed task |
| **P-* gate** | Project-specific evidence, policy, or authorization checkpoint |
| **PDMAL** | Experimental multi-agent topology / robustness substrate |
| **Freeze** | Immutable binding of a candidate and protected inputs; **not execution authorization** |
| **Dataset lock** | Immutable binding of an accepted collected dataset; **not unblinding or analysis authorization** |
| **Unblinding decision** | Bounded permission for treatment-identity release/decryption; **not materialization or analysis authorization** |
| **Materialization** | Construction of analysis-ready unblinded input; **not outcome aggregation or analysis** |
| **Primary-analysis authorization** | Separate permission to run the locked confirmatory analysis |
| **Decision Frontier** | Presentation-only view of current state, blocker, reachable next action, consequences, and receipt semantics |
| **Governance Map** | Presentation-only structural view of escalation, named lateral coupling, and global constraints |
| **State-Space Explorer V0** | Presentation-only discrete reachability projection; not continuous readiness or authorization geometry |
| **Assurance catalog** | Partial machine-readable mapping of selected recurring repository assurance families |
| **Fail closed** | Missing, stale, malformed, ambiguous, unrecoverable, or unclassified required evidence blocks promotion rather than being guessed |

## What is not established

DGAF is **not** currently presented as:

- empirically validated as a complete framework;
- independently validated;
- production-certified;
- High-Assurance authorized;
- supported by a completed Track A primary analysis;
- having established canonical DGAF efficacy;
- having exhaustive repository assurance coverage;
- having deployment health established merely because source/CI verification passed;
- having a meaningful continuous “distance” to authorization or readiness.

## Where to start

- **Live state:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **Compatibility status entrypoint:** [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md)
- **Technical architecture:** [`README.technical.md`](README.technical.md)
- **Governance model / standards crosswalk:** [`README.governance.md`](README.governance.md)
- **Plain-English terminology:** [`docs/PUBLIC_TRANSLATION_LAYER.md`](docs/PUBLIC_TRANSLATION_LAYER.md)
- **Partial assurance catalog:** [`registry/audit_catalog.v1.json`](registry/audit_catalog.v1.json)
- **Historical/provenance index:** [`docs/HISTORICAL_RECORDS_INDEX.md`](docs/HISTORICAL_RECORDS_INDEX.md)

---

Dynamic Governance Agentic Formation  
Governed multi-agent orchestration · provenance · evaluation · authorization · experimental integrity
