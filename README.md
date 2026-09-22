# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** is an experimental framework for governed multi-agent AI systems. It treats **capability, evidence, verification, authority, and permission to act as separate machine-relevant states** rather than assuming that one implies another.

In plain English: an agent may be able to do something and still be blocked from doing it; a system may pass engineering tests and still be blocked from claiming that it is empirically validated.

## Five-minute evaluator orientation

If you are evaluating DGAF as an AI-systems, governance, or research-engineering portfolio artifact, use this path before reading the full control history.

**1. Start with the problem.** DGAF asks whether an AI system's current evidence and authority actually support the claim or action it is about to make. Capability alone does not grant permission, and passing engineering checks does not establish empirical efficacy.

**2. Inspect what is implemented.** The repository contains governance logic, provenance/source binding, deterministic validators, negative controls, CI, experimental tooling, custody machinery, blinded-data infrastructure, a decomposed Governance Command Center, and a machine-readable partial assurance catalog. For implementation detail, start with [`README.technical.md`](README.technical.md) and [`README.governance.md`](README.governance.md).

**3. Read the current state from its owning record.** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) is the live project/evidence entrypoint. The status block immediately below is a public summary, not a substitute for exact-bound evidence records.

**4. Understand the current Track A frontier.** Epoch 002 blinded collection is complete at 50 paired inferential seed units / 2,250 observations; dataset lock, bounded unblinding, real materialization evidence (#824), the immutable materialization receipt (#826), and locked-primary-analysis authorization (#828) are accepted. The frozen primary analysis has now executed locally, and PR #851 established the creation-only content-addressed locked-result receipt on protected `main`. The bounded Epoch 002 lifecycle is now **CLOSED_FOR_EXACT_PREREGISTERED_SCOPE** through the creation-only post-interpretation disposition accepted via PR #881. Scientific-N increment remains 0, and canonical DGAF efficacy and independent validation are not established.

**5. Understand the AOSS Stage-A external-validation frontier.** The non-collecting Stage-A assurance apparatus is accepted through PR #925. PR #928 adds the accepted independent-validation handoff, so an external review is now operationally requestable. Issue #929 controls actual reviewer engagement and returned evidence. No reviewer has yet been established as independent, no external review has been executed, and collection execution readiness remains not established.

**6. Evaluate the separation discipline.** The central engineering/research claim is not that DGAF is already proven. It is that the repository makes state transitions, evidence classes, provenance, authorization, assurance coverage, and non-claims explicit and machine-checkable enough to prevent one category from silently substituting for another.

### What this demonstrates

Within the evidence boundaries documented in this repository, DGAF demonstrates practical work in:

- multi-agent governance and explicit authority/state-transition design;
- provenance, source/evidence binding, and custody controls;
- deterministic validation, negative controls, and fail-closed CI;
- prospective/blinded experiment infrastructure and reproducibility tooling;
- separation of implementation, verification, independent verification, authorization, execution, and empirical support;
- documentation and public translation of a complex technical control system without upgrading its evidence state;
- operator/auditor UI design that exposes blockers and reachable transitions without inventing readiness percentages;
- machine-readable assurance inventorying that distinguishes mapped controls, required branch contexts, and unclassified coverage gaps.

### Current repository engineering milestones

For this reconciliation, the accepted source lineage through PR #797 was read from protected `main` `40d301583048e0c47e8bf38154ac40fa023b4f5e`. Exact current protected-main identity is a Git fact and must be read at use time:

- **Decision Frontier — PR #776** is merged as a presentation-only Semantic Control Field component derived from canonical governance state.
- **Governance Map — PR #779** is merged and renders ordered escalation, explicitly named lateral relationships, and global field constraints without creating a second state engine.
- **State-Space Explorer V0 — PR #783** is merged and projects canonical stages into discrete `established`, `frontier`, and `blocked_by_predecessor` regions while preserving native predicate state and explicit model limits.
- **Bounded assurance catalog — PR #780** is merged with `coverage.status = PARTIAL_CORE_FAMILIES_ONLY`.
- **Workflow coverage-gap scanner — PR #782** is merged and reports workflow definitions not yet exactly bound by the catalog without inferring their role.
- **Recurring assurance expansion — PR #785** is merged and adds seven source-verified recurring assurance families while preserving partial coverage.
- **Current-facing authority/documentation reconciliation — PR #795** is merged; security, operations, pattern-registry, authority-matrix, bootstrap, and technical-reference surfaces now route current executable authority through functional `role.*` contracts while retaining personas as provenance.
- **Stage-1 retained-archive repair — PR #794** is merged and accepts the exact locked archive's harmless `./` flat-member representation without changing archive bytes or weakening unsafe-member rejection.
- **Stage-2 accepted-lineage rebind — PR #797** is merged and binds the operator bundle to accepted Stage-1 commit `cf32a62bbf08a1b8db39709f4989be1be800d64e` / blob `3a825b026423952c2844cb18664eb6395b72fdc1`.
- **AOSS Stage-A independent-validation handoff — PR #928** is merged and binds the external-review package to exact DGAF/ACP identities, reviewer-independence disclosure, verification procedure, returned-evidence requirements, and claim ceiling without asserting that an independent review has occurred.

Those earlier engineering/presentation/assurance milestones did not establish materialization or primary-analysis authorization. Subsequent separately governed events advanced the lane: PR #824 admitted real non-secret materialization evidence, PR #826 established its immutable receipt, PR #831 accepted the fail-closed local analysis runner, PR #828 accepted bounded locked-analysis authorization, PR #835 accepted non-executing content-addressed result-admission tooling, PR #848 corrected the lifecycle-aware admission test, and PR #851 established the immutable locked-analysis result receipt. PR #872 separately established bounded interpretation admission at SAME_SYSTEM_NONINDEPENDENT scope. These events establish execution, result admission, and bounded interpretation at their exact scopes, but not canonical DGAF efficacy, independent validation, production certification, or High-Assurance authorization.

> **Canonical High-Assurance research status:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N = 0  
> **Track A Epoch 001:** PROSPECTIVE BLINDED COLLECTION COMPLETE · 50 paired inferential seed units · 2,250 blinded observations · DATASET LOCK ESTABLISHED  
> **Epoch 001 disposition:** protected mapping is **CRYPTOGRAPHICALLY UNRECOVERABLE** · primary analysis **UNANALYZABLE / NOT RUN**  
> **Successor Track A / Epoch 002:** custody, freeze, closure, bounded verification classification, collection authorization, dataset lock, bounded unblinding, materialization, immutable materialization receipt, locked-primary-analysis authorization, local locked analysis execution, and the content-addressed locked-result receipt are **ACCEPTED/ESTABLISHED AT THEIR EXACT SCOPES** · blinded collection **COMPLETE** at 50 paired seed units / 2,250 observations · interpretation/adjudication **EXECUTED / ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT**  
> **AOSS Stage-A external review:** HANDOFF ACCEPTED VIA PR #928 · REVIEW NOT EXECUTED · ISSUE #929 OPEN · reviewer attribution / independence NOT VERIFIED · execution_allowed=false  
> **Canonical DGAF efficacy:** NOT ESTABLISHED

## What problem DGAF is trying to solve

Most agent frameworks focus on what an agent can do: reason, call tools, hand work to another agent, retain state, or complete a workflow.

DGAF focuses on an additional question:

> **Given the evidence and authority that exist right now, what is this system actually entitled to claim, authorize, and execute?**

DGAF explores this through:

- **Governed orchestration** — specialized agents operate under explicit roles, boundaries, and escalation rules.
- **Evidence-aware authorization** — technical capability does not automatically grant permission.
- **Provenance** — outputs, decisions, evidence, and state are tied to the identities that produced them.
- **Evaluation integrity** — implementation, testing, verification, independent verification, and empirical demonstration remain distinct.
- **Fail-closed controls** — missing or ambiguous prerequisites block promotion rather than silently becoming approval.
- **Experimental reproducibility** — prospective experiments bind protocols, code, analysis, artifacts, custody, and authorization to exact identities.
- **Inspectable reachability** — operator-facing presentation makes blocked and admissible transitions explicit without converting categorical authority into a score.
- **Assurance coverage accounting** — machine-readable mappings record what recurring controls are classified and what remains unclassified.

## The core model

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

## Current research program

DGAF separates prospective evaluation by workload instead of treating one experiment as proof of the entire framework.

| Track | Plain-English purpose | Current boundary |
|---|---|---|
| **A — Epoch 001** | Numeric topology robustness | Prospective blinded collection complete and dataset locked; protected mapping is cryptographically unrecoverable; primary analysis unanalyzable/not run; retained as historical blinded evidence plus custody-design failure evidence |
| **A — Epoch 002 successor** | Replacement prospective topology robustness | Collection COMPLETE at 50 paired seed units / 2,250 observations; dataset lock ESTABLISHED; bounded unblinding AUTHORIZED; materialization and immutable receipt ESTABLISHED; locked-primary-analysis authorization ACCEPTED; primary analysis EXECUTED locally under the frozen contract; content-addressed locked-result receipt ESTABLISHED via #851; interpretation/adjudication EXECUTED / ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT |
| **B1** | Semantic routing and safety | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B2** | Persistent context and closure | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B3** | Persistent weighted-graph convergence monitoring | Standalone non-empirical lane complete; no empirical efficacy claim |
| **C** | Integrated DGAF composition | Non-empirical composition proposal merged; empirical execution NOT AUTHORIZED |

Epoch 001's prospective panel was fixed at **50 seeds × 5 topologies × 9 failure counts = 2,250 observations**. The accepted scientific unit count is **50 paired inferential seed units / 2,250 blinded raw observations**.

That collection remains valid evidence that the blinded panel was executed and retained. It cannot produce its preregistered primary result because the retained encrypted topology mapping cannot be recovered: the matching private key was not durably recoverable in the solo operating model. Regenerating a different key cannot decrypt the retained ciphertext, and guessing or reconstructing the hidden assignment is prohibited.

## Successor Track A custody and gate design

Issue #523 controls the replacement path. Epoch 002 uses a distinct protocol identity, fresh seeds and blinding, and recoverable solo custody without presenting same-system custody as independent.

Repository custody, precollection preflight, immutable freeze, final closure, bounded non-independent verification classification, separate collection authorization, retained-evidence admission/QC, dataset lock, and bounded unblinding have advanced through separate governed events. The authorized operator-executed Codespace collection is complete at **50 paired seed units / 2,250 blinded observations**.

The Epoch 002 lifecycle is **closed for its exact preregistered scope** via PR #881. No rerun, historical pooling, claim promotion, or new empirical epoch is authorized by that closure. The accepted apparatus now includes:

- a PASS content-addressed dataset-lock receipt;
- a separate PASS unblinding decision bounded to `CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`;
- the accepted local materialization chain through PRs #713/#715/#794/#797/#806/#809/#813;
- real non-secret materialization evidence admitted through PR #824;
- an immutable creation-only materialization receipt accepted through PR #826;
- fail-closed local locked-analysis runner tooling accepted through PR #831;
- the separate primary-analysis authorization event accepted through PR #828 with exact scope `LOCKED_PRIMARY_ANALYSIS_ONLY`;
- non-executing content-addressed result-admission tooling accepted through PR #835;
- lifecycle-aware result-admission tests accepted through PR #848;
- the creation-only locked-analysis result receipt accepted through PR #851 as `c0690e599d25304f1d920d5235adff04ba76094a`.

Current boundary:

- `TRACK_A_EPOCH_002_DATASET_LOCK = ESTABLISHED`;
- `UNBLINDING = AUTHORIZED / BOUNDED TO CONTROLLED MAPPING RELEASE OR DECRYPTION`;
- `TRACK_A_EPOCH_002_MATERIALIZATION = ESTABLISHED`;
- `TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT = ESTABLISHED`;
- `PRIMARY_ANALYSIS_AUTHORIZATION = ACCEPTED / LOCKED_PRIMARY_ANALYSIS_ONLY`;
- `PRIMARY_ANALYSIS = EXECUTED_LOCKED / RETAINED`;
- `LOCKED_ANALYSIS_RESULT = ESTABLISHED`;
- `INTERPRETATION_ADJUDICATION = EXECUTED / ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT`;
- `SCIENTIFIC_N_INCREMENT = 0`;
- `CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`;
- `INDEPENDENT_VALIDATION = NOT_ESTABLISHED`;
- `HIGH_ASSURANCE = PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`.

The remaining ordered sequence is:

`closed Epoch 002 lifecycle → separate future proposal/preregistration/authorization if new empirical work is pursued`

No private key, passphrase, blinding secret, protected plaintext mapping, decrypted protected data, or other recoverable secret material belongs in GitHub, Notion, chat, CI inputs, workflow logs, or committed files.

## Governance Command Center

The accepted presentation layer is designed to answer five operator questions without becoming an independent source of truth:

1. Where are we?
2. Why are we here?
3. What is blocking us?
4. What can happen next?
5. What would change if we did it?

The **Decision Frontier**, **Governance Map**, and **State-Space Explorer V0** consume normalized governance/current-state data. They may display evidence, blockers, reachability, provenance, coupling, field constraints, and explicit representation limits, but they cannot grant authority or promote a scientific state.

State-Space Explorer V0 is current accepted source state only as a **discrete categorical reachability projection**. Continuous manifold/tensor metaphors remain conceptual unless exact formal semantics are implemented and verified; DGAF does not currently assign readiness distance, authorization probability, scalar evidence quality, efficacy gradients, inferred consequence, or inferred reversibility.

## Repository assurance catalog

`registry/audit_catalog.v1.json` is a versioned repository-local map of selected recurring assurance families. It remains explicitly **partial**.

Current protected-main behavior includes:

- deterministic catalog validation;
- exact implementation-path bindings;
- deterministic discovery of current workflow definitions not yet mapped by the catalog;
- explicit non-effects and bounded verdict semantics for mapped families.

Current protected-main branch-protection required contexts are separately read as **PPTL CI**, **Governance CI**, and **PR Issue-State Keyword Guard**. A workflow can be cataloged as a recurring assurance family without being a required merge context, and an unmapped workflow remains **unclassified**, not automatically “non-assurance.”

## What is established — and what is not

The repository contains substantial engineering evidence: governance logic, provenance controls, deterministic validators, CI, negative controls, source binding, custody/security machinery, experimental tooling, runtime evidence, vocabulary governance, presentation controls, a partial recurring-assurance inventory, and blinded-data infrastructure.

Track A Epoch 001 also contains genuine prospective blinded collection evidence. That evidence is **not a primary efficacy result** and is explicitly **unanalyzable** under the retained protected-mapping evidence.

Track A Epoch 002 has advanced further: collection is complete; dataset lock and bounded unblinding are established at their exact scopes; materialization and its immutable receipt are accepted; the bounded locked-primary-analysis authorization event is accepted; the frozen primary analysis has executed locally; and the content-addressed locked-result receipt is established. PR #872 separately established bounded interpretation/adjudication at SAME_SYSTEM_NONINDEPENDENT scope. These transitions still do **not** establish canonical DGAF efficacy, independent validation, production certification, or High-Assurance authorization.

A separate Solo research track produced bounded historical empirical evidence. Epoch 004 completed 50 seeds / 9,000 observations and produced negative evidence for its exact executed treatment. A later source audit found that canonical treatment fidelity was not established, so that result remains exact-treatment historical evidence rather than a claim about canonical DGAF efficacy.

DGAF is **not** currently presented as:

- empirically validated as a complete framework;
- independently validated;
- production-certified;
- High-Assurance authorized;
- having established canonical DGAF efficacy;
- having exhaustive repository assurance coverage;
- having deployment health established merely because source/CI verification passed.

## Internal terms in plain English

| Internal term | Public / industry-neutral translation |
|---|---|
| **Formation** | The set and structure of agents selected for a governed task |
| **TGL / P-35** | Per-turn governance and state-transition kernel |
| **P-* gate** | Project-specific evidence, policy, or authorization checkpoint |
| **PDMAL** | Experimental multi-agent topology / robustness substrate |
| **Freeze** | Immutable binding of the candidate and protected experimental inputs; **not execution authorization** |
| **Closure** | Proof that required pre-authorization prerequisites are complete; **not execution authorization** |
| **Verification classification** | Records what kind of verifier produced the evidence and whether it is independent |
| **Dataset lock** | Immutable receipt binding an accepted collected dataset and retained artifact identities; **not unblinding or analysis authorization** |
| **Unblinding decision** | Separate human-controlled permission for bounded treatment-identity release/decryption; **not materialization or analysis authorization** |
| **Materialization** | Deterministic construction of analysis-ready unblinded input; **not outcome aggregation or analysis** |
| **Primary-analysis authorization** | Separate permission to run the locked confirmatory analysis |
| **Decision Frontier** | Presentation-only view of current state, blocker, reachable next action, and consequences |
| **Governance Map** | Presentation-only structural view of vertical escalation, named lateral coupling, and global constraints |
| **State-Space Explorer V0** | Presentation-only discrete reachability projection; not a continuous manifold or readiness score |
| **Assurance catalog** | Partial machine-readable mapping of selected recurring repository assurance families |
| **Fail closed** | Missing, stale, malformed, ambiguous, unrecoverable, or unclassified required evidence blocks promotion rather than being guessed |

See **[`docs/PUBLIC_TRANSLATION_LAYER.md`](docs/PUBLIC_TRANSLATION_LAYER.md)** for the full public terminology map and vocabulary governance.

## Where to start

- **Live project/evidence state:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **Compatibility status entrypoint:** [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md)
- **Plain-English terminology:** [`docs/PUBLIC_TRANSLATION_LAYER.md`](docs/PUBLIC_TRANSLATION_LAYER.md)
- **Technical architecture:** [`README.technical.md`](README.technical.md)
- **Governance model:** [`README.governance.md`](README.governance.md)
- **Partial assurance catalog:** [`registry/audit_catalog.v1.json`](registry/audit_catalog.v1.json)
- **Historical records:** [`docs/HISTORICAL_RECORDS_INDEX.md`](docs/HISTORICAL_RECORDS_INDEX.md)

## Research boundary

Results remain scoped to the exact system identities, treatment definitions, protocols, evidence classes, and custody conditions that produced them. A green test, merged PR, internal qualification score, mathematical property, authorization record, completed collection, UI projection, catalog entry, or historical result does not automatically establish current empirical efficacy.

Epoch 001 demonstrates an additional governance lesson: **a successful blinded collection is not sufficient if the protected mapping required for the preregistered analysis cannot later be recovered.** The successor design therefore treats precollection recovery testing as a prerequisite rather than an operational afterthought.

---

Dynamic Governance Agentic Formation  
Governed multi-agent orchestration · provenance · evaluation · authorization · experimental integrity
