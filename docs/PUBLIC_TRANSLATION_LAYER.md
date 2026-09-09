# DGAF Public Translation Layer

This document translates DGAF's project-local vocabulary into plain, industry-neutral language for engineers, researchers, governance reviewers, hiring managers, and other external readers.

The goal is **translation, not renaming**. Internal names remain useful inside DGAF, while public documentation leads with the function an external reader needs to understand.

Machine-readable authority: `docs/VOCABULARY_TRANSLATION_MATRIX.json`. Process rules: `docs/VOCABULARY_GOVERNANCE.md`.

## One-sentence description

**DGAF is an experimental governed-agent framework in which evidence, verification, authority, and permission to act are tracked separately so that capability cannot silently become authorization or testing become proof.**

## Core concepts

| DGAF term | Public translation | Important boundary |
|---|---|---|
| **DGAF** | Governed multi-agent orchestration and evaluation framework | Engineering/governance implementation is not complete-framework empirical validation |
| **Formation** | Governed agent configuration | More agents do not imply better performance |
| **Agent authority** | Role-bounded decision rights | Capability is not permission |
| **Governance Envelope** | Inherited policy and authority boundary | Not a generic content filter |
| **Control Plane** | Lifecycle and orchestration controller | Not the scientific experiment itself |
| **P-* gate** | Project-specific checkpoint | A passing gate is not industry certification |
| **CommitGate** | Explicit commit/action authorization boundary | Feasibility does not imply authorization |
| **PDMAL** | Experimental topology and robustness substrate | Not the whole DGAF framework |
| **Fail closed** | Deny progression when prerequisites are not proven | Unknown does not mean the hypothesis is false |
| **Provenance** | Source and decision lineage | Traceability alone does not prove correctness |
| **Evidence binding** | Exact identity binding | Evidence does not automatically transfer to later versions |
| **Claim promotion** | Evidence-based change in epistemic status | Not marketing promotion |
| **Verification classification** | Verifier-independence record | Internal review is not independent validation by default |
| **Freeze** | Immutable experimental candidate binding | Not collection authorization |
| **Closure** | Pre-authorization completeness proof | Not collection authorization |
| **Collection authorization** | Permission for the exact prospective collection | Not evidence that collection happened or efficacy exists |
| **Dataset lock** | Immutable collected-dataset receipt | Not analysis or efficacy evidence |
| **Unblinding authorization** | Permission for controlled treatment-identity release | Not primary-analysis authorization |
| **Materialization** | Deterministic construction of analysis-ready unblinded input | Not outcome aggregation or analysis |
| **Primary-analysis authorization** | Separate permission to run the locked confirmatory analysis | Not exploratory pooling or canonical efficacy adjudication |
| **High-Assurance** | Separate stricter assurance program | Not synonymous with Track A |

## Vocabulary model

Five different things must remain separate:

1. **Canonical identity** — project-local named agent identity.
2. **Alias** — compatibility name whose relationship has actually been adjudicated.
3. **Abstract role/archetype** — function class such as `VERIFY`, `GOVERN`, or `SENTINEL_ARCHETYPE`; not an identity and not authority.
4. **State** — a system condition; not an independent agent authority.
5. **External functional label** — plain-language explanation for public readers.

Translation does not resolve underlying identity conflicts. When identity sources disagree, public language preserves the conflict rather than inventing a simpler ontology.

## Named-identity translation matrix

| Internal term | Kind / status | External-facing label | Boundary |
|---|---|---|---|
| **Amethyst** | Agent | **Governance Orchestrator** | Coordinates governed lifecycle; does not independently establish scientific truth, owner authorization, independent verification, or efficacy |
| **COLLEEN** | Agent; designation conflict retained | **Continuity & Provenance Coordinator** | Preserves continuity/provenance; does not manufacture evidence or authorization |
| **Apogee** | Agent; alias `Apogee Lens` | **Evidence & Verification Reviewer** | Verification role does not establish verifier independence |
| **Sentinel-Phi** | Agent; Sentinel lineage unresolved | **Security & Policy Boundary Enforcer** | Translate only when the source specifically names Sentinel-Phi; do not silently collapse `Sentinel` into it |
| **DemiJoule** | Agent | **Runtime Safety & Constraint Adviser** | `SENTINEL_ARCHETYPE` is a role class, not Sentinel or Sentinel-Phi identity |
| **Herald** | Agent | **Publication & External Communication Gatekeeper** | Cannot manufacture evidence, approval, or scientific status |
| **Professor Prodigy** | Agent; aliases `Prodigy`, `Prof Prodigy` | **Formal Methods & Mathematical Analyst** | Formal analysis is non-orchestrating and non-authorizing |
| **Nova** | Agent | **Simulation & Hypothesis Explorer** | Exploration is not authorization or verified evidence |
| **Perigee** | Agent | **Boundary & Input-Safety Filter** | Filtering is not governance authorization or independent security certification |
| **Reciprocity** | Agent | **Reciprocal-Impact & Fairness Reviewer** | Does not globally certify fairness |
| **The Librarian** | Agent; designation conflict retained | **Provenance & Decision Archivist** | Traceability is not correctness or permission |
| **The Auditor** | Agent | **Quality & Constraint Reviewer** | Internal QA is not independent certification |
| **The Actualizer** | Agent | **Authorized Execution Worker** | Technical ability never creates permission |
| **Zenith** | Agent; designation conflict retained | **Compute & Resource Coordinator** | Resource control creates no scientific/governance authority |
| **Reson** | Agent; designation conflict retained | **Coherence & Drift Reviewer** | Domain coherence scores do not create general governance or empirical authority |
| **Lyra** | Agent; designation conflict retained | **Synthesis & Narrative Adviser** | Narrative/synthesis quality cannot change governance or evidence state |
| **Echolette** | Agent; designation conflict retained | **Pattern & Temporal-Coherence Reviewer** | Pattern/coherence review remains domain-scoped |
| **Ionia** | **State pending ontology reconciliation** | **Convergence & Modal-Lock State** | Newer records classify Ionia as state; translation does not rewrite the older roster or grant independent authority |

## Required first-use forms

When the identity matters to an external reader, lead with the function:

- **Governance Orchestrator (Amethyst)**
- **Continuity & Provenance Coordinator (COLLEEN)**
- **Evidence & Verification Reviewer (Apogee)**
- **Security & Policy Boundary Enforcer (Sentinel-Phi)**
- **Runtime Safety & Constraint Adviser (DemiJoule)**
- **Publication & External Communication Gatekeeper (Herald)**
- **Formal Methods & Mathematical Analyst (Professor Prodigy)**
- **Simulation & Hypothesis Explorer (Nova)**
- **Boundary & Input-Safety Filter (Perigee)**
- **Reciprocal-Impact & Fairness Reviewer (Reciprocity)**
- **Provenance & Decision Archivist (The Librarian)**
- **Quality & Constraint Reviewer (The Auditor)**
- **Authorized Execution Worker (The Actualizer)**
- **Compute & Resource Coordinator (Zenith)**
- **Coherence & Drift Reviewer (Reson)**
- **Synthesis & Narrative Adviser (Lyra)**
- **Pattern & Temporal-Coherence Reviewer (Echolette)**
- **Convergence & Modal-Lock State (Ionia)**

After first use, the codename may be used when the referent remains unambiguous.

## Important unresolved vocabulary

### Sentinel / Sentinel-Phi

The current identity conflict register preserves a distinct Sentinel lineage and a related Sentinel-Phi identity. Therefore **Sentinel is not treated as an alias of Sentinel-Phi by the translation matrix**. Public material should preserve the source term when only `Sentinel` is known and explain ambiguity when it matters.

This is separate from DemiJoule's historical/AHG **Sentinel archetype**, which is a role class only.

### Ionia

The older sovereign roster describes Ionia as an agent seat, while newer topology/ecosystem records classify Ionia as a 0Hz/modal state. Public translation uses **Convergence & Modal-Lock State (Ionia)** until that ontology conflict is formally adjudicated. This wording does not alter the underlying sovereign source.

## Internal versus external example

Internal shorthand may remain compact:

> `Amethyst → Apogee → DemiJoule → Herald`

External prose should translate the functions:

> The **Governance Orchestrator (Amethyst)** routes a candidate through **Evidence & Verification Review (Apogee)** and **Runtime Safety & Constraint Review (DemiJoule)** before the **Publication & External Communication Gatekeeper (Herald)** may release an accepted public artifact.

## Naming and authority rules

- Codename is identity, not capability.
- Role class is not identity.
- Alias is accepted only after the underlying identity relationship is established.
- Independence is evidence, not branding.
- Named agents are project-local constructs, not industry standards.
- Translation has `scientific_state_effect = NONE`, `authority_effect = NONE`, and `identity_resolution_effect = NONE`.
- Runtime, CI, deployment, experiment, authorization, and efficacy status do not belong in vocabulary entries.

## Research-track translation

| Track | Plain-English scope | Current public interpretation |
|---|---|---|
| **Track A** | Numeric topology robustness experiment | Prospective blinded collection complete; 50 paired inferential seed units / 2,250 blinded raw observations retained; dataset lock and unblinding authorization established; custody-key handoff/materialization pending; primary analysis not authorized/run |
| **Track B1** | Semantic routing and safety behavior | Standalone non-empirical engineering/evaluation lane complete |
| **Track B2** | Persistent context and closure behavior | Standalone non-empirical engineering/evaluation lane complete |
| **Track B3** | Persistent graph-convergence monitoring | Standalone non-empirical engineering/evaluation lane complete |
| **Track C** | Integrated DGAF composition | Non-empirical composition proposal only; empirical execution not authorized |
| **Solo Epochs** | Historical developer-run bounded experiments | Historical exact-scope evidence; not automatically canonical DGAF evidence |

## Evidence-state translation

| State | Plain-English meaning |
|---|---|
| **PROPOSED** | Designed but not demonstrated |
| **IMPLEMENTED** | Exists in code/artifacts |
| **TESTED** | Covered by stated tests in stated environment |
| **PASS** | Exact predicate passed; scope does not widen automatically |
| **VERIFIED** | Defined verification predicate passed |
| **DEVELOPER SELF-ATTESTED / NONINDEPENDENT** | Same developer/system lineage; not independent validation |
| **INDEPENDENTLY VERIFIED** | Separate accepted independence/evidence path established |
| **NOT AUTHORIZED** | Named execution remains prohibited |
| **NOT ESTABLISHED** | Required evidence does not currently satisfy the claim |
| **EMPIRICALLY DEMONSTRATED** | Supported by executed experiment in exact stated scope |

## Scientific-unit wording

For Track A, use **50 paired inferential seed units / 2,250 blinded raw observations** rather than a bare `N=2250`. The separate High-Assurance program remains at empirical N=0.

## Current external boundary

**DGAF has substantial engineering and governance implementation evidence. Track A completed governed prospective blinded collection and established a dataset lock. Controlled unblinding is authorized, but matching custody-key handoff and unblinded-input materialization remain pending. Primary analysis has not been authorized or run, canonical DGAF efficacy is not established, and High-Assurance is not authorized.**

## Public documentation rule

When a project-local term first appears on a designated public surface:

1. classify it as identity, alias, role/archetype, state, or external label;
2. check the vocabulary registry and unresolved relations;
3. lead with the plain-English function;
4. preserve identity and authority conflicts rather than silently resolving them;
5. preserve verification, authorization, scientific-state, and efficacy ceilings;
6. link to technical/governance evidence when the distinction matters.

The dedicated `Vocabulary Translation Matrix` CI workflow checks registry structure, active-identity coverage, conflict retention, authority/scientific non-effects, and this public layer.
