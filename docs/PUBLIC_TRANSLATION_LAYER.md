# DGAF Public Translation Layer

This document translates DGAF's project-local vocabulary into plain, industry-neutral language for engineers, researchers, governance reviewers, hiring managers, and other external readers.

The goal is **translation, not renaming**. Internal names remain useful inside DGAF, while public documentation leads with the function an external reader needs to understand.

Machine-readable translation authority: `docs/VOCABULARY_TRANSLATION_MATRIX.json`. Process rules: `docs/VOCABULARY_GOVERNANCE.md`. Identity disputes are resolved by `docs/agents/AGENT_ROSTER.md` plus `registry/agent_ontology_adjudication.v1.json`; the translation layer does not decide sovereign identity.

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
| **Dataset lock** | Immutable collected-dataset receipt | Non-authorizing; not unblinding or analysis permission |
| **Unblinding decision** | Separate human-controlled permission for bounded treatment-identity release/decryption | Not materialization or primary-analysis authorization |
| **Materialization** | Deterministic construction of analysis-ready unblinded input | Not outcome aggregation or analysis |
| **Materialization receipt** | Immutable record binding the materialized input and retained identity | Non-authorizing; requires a separate primary-analysis decision |
| **Primary-analysis authorization** | Separate permission to run the locked confirmatory analysis | Not exploratory pooling or canonical efficacy adjudication |
| **High-Assurance** | Separate stricter assurance program | Not synonymous with Track A |

## Vocabulary model

Keep these objects distinct:

1. **Canonical identity** — project-local named agent identity.
2. **Accepted alias** — compatibility name whose relationship has been adjudicated.
3. **Formation-local identity/designation** — a formation-scoped variant or seat that does not silently renumber sovereign identity.
4. **Abstract role/archetype** — a function class; not an identity and not authority.
5. **State** — a system/formation condition; not an independent agent authority.
6. **External functional label** — plain-language explanation for public readers.

Translation must consume the accepted ontology rather than reopen it through shorthand.

## Named-identity translation matrix

| Internal term | Kind / status | External-facing label | Boundary |
|---|---|---|---|
| **Amethyst** | Agent | **Governance Orchestrator** | Coordinates governed lifecycle; does not independently establish scientific truth, owner authorization, independent verification, or efficacy |
| **COLLEEN** | Agent; designation history retained | **Continuity & Provenance Coordinator** | Preserves continuity/provenance; does not manufacture evidence or authorization |
| **Apogee** | Agent; alias `Apogee Lens` | **Evidence & Verification Reviewer** | Verification role does not establish verifier independence |
| **Sentinel** | Distinct sovereign security lineage/role | **Security Lineage / Policy Boundary Role** | Distinct from Sentinel-Phi; do not collapse the two identities |
| **Sentinel-Phi** | Distinct formation variant/identity; formation-local `A-12-φ` | **Security & Policy Boundary Enforcer** | Formation-local designation does not create or replace a sovereign numbered seat |
| **DemiJoule** | Agent | **Runtime Safety & Constraint Adviser** | Historical/AHG `SENTINEL_ARCHETYPE` is a role class, not Sentinel or Sentinel-Phi identity |
| **Herald** | Agent | **Publication & External Communication Gatekeeper** | Cannot manufacture evidence, approval, or scientific status |
| **Professor Prodigy** | Agent; aliases `Prodigy`, `Prof Prodigy` | **Formal Methods & Mathematical Analyst** | Formal analysis is non-orchestrating and non-authorizing |
| **Nova** | Agent | **Simulation & Hypothesis Explorer** | Exploration is not authorization or verified evidence |
| **Perigee** | Agent | **Boundary & Input-Safety Filter** | Filtering is not governance authorization or independent security certification |
| **Reciprocity** | Agent | **Reciprocal-Impact & Fairness Reviewer** | Does not globally certify fairness |
| **The Librarian** | Agent; designation history retained | **Provenance & Decision Archivist** | Traceability is not correctness or permission |
| **The Auditor** | Agent | **Quality & Constraint Reviewer** | Internal QA is not independent certification |
| **The Actualizer** | Agent | **Authorized Execution Worker** | Technical ability never creates permission |
| **Zenith** | Agent; designation history retained | **Compute & Resource Coordinator** | Resource control creates no scientific/governance authority |
| **Reson** | Agent; designation history retained | **Coherence & Drift Reviewer** | Domain coherence scores do not create general governance or empirical authority |
| **Lyra** | Agent; designation history retained | **Synthesis & Narrative Adviser** | Narrative/synthesis quality cannot change governance or evidence state |
| **Echolette** | Agent; designation history retained | **Pattern & Temporal-Coherence Reviewer** | Pattern/coherence review remains domain-scoped |
| **Agent Ionia** | Sovereign agent identity **A-13** | **Convergence & Modal-Lock Agent** | Distinct from `IONIA_STATE`; agent identity does not make 0Hz metaphors empirical control evidence |
| **IONIA_STATE / Ionia 0Hz** | Formation/runtime convergence state; no sovereign seat | **Convergence & Modal-Lock State** | A state, not Agent Ionia A-13 and not an authority-bearing agent seat |

## Required first-use forms

When the identity matters to an external reader, lead with the function and preserve the resolved object type:

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
- **Convergence & Modal-Lock Agent (Ionia)** when the agent identity is intended
- **Convergence & Modal-Lock State (IONIA_STATE)** when the runtime/formation state is intended

After first use, the codename may be used when the referent remains unambiguous.

## Adjudicated ontology distinctions

### Sentinel / Sentinel-Phi

Accepted issue #522 adjudication preserves **Sentinel** and **Sentinel-Phi** as distinct ontology records. Base Sentinel is a sovereign security lineage/role. Sentinel-Phi is a distinct formation variant/identity with formation-local designation `A-12-φ`. Formation-local designation does not silently create, replace, or renumber a sovereign seat.

This is also separate from DemiJoule's historical/AHG **Sentinel archetype**, which is a role class only.

### Agent Ionia / IONIA_STATE

Accepted issue #522 adjudication resolves the prior ambiguity:

- **Agent Ionia — A-13** is the canonical sovereign roster identity unless a later explicit roster amendment changes it.
- **`IONIA_STATE` / Ionia 0Hz state** is a formation/runtime convergence state. It is not an agent seat and consumes no sovereign seat.

Any current-facing text that says only `Ionia` where the distinction matters must state which object is intended.

## Naming and authority rules

- Codename is identity, not capability.
- Role class is not identity.
- Formation-local designation is not sovereign seat authority.
- Alias is accepted only after the underlying relationship is established.
- State is not an agent seat.
- Independence is evidence, not branding.
- Named agents are project-local constructs, not industry standards.
- Translation has `scientific_state_effect = NONE`, `authority_effect = NONE`, and `identity_resolution_effect = NONE`.
- Runtime, CI, deployment, experiment, authorization, and efficacy status do not belong in identity definitions.

## Research-track translation

| Track | Plain-English scope | Current public interpretation |
|---|---|---|
| **Track A — Epoch 001** | Historical prospective numeric topology-robustness collection | Blinded collection complete; 50 paired inferential seed units / 2,250 blinded raw observations retained; dataset lock established; protected mapping cryptographically unrecoverable; primary analysis unanalyzable / not run |
| **Track A — Epoch 002 successor** | Replacement prospective numeric topology-robustness experiment | Operator-local custody-v2 recovery passed as self-attested/non-independent; repository custody NOT ESTABLISHED; empirical collection NOT AUTHORIZED; dataset lock NOT ESTABLISHED; unblinding NOT AUTHORIZED; materialization NOT ESTABLISHED; primary analysis NOT AUTHORIZED / NOT RUN |
| **Track B1** | Semantic routing and safety behavior | Standalone non-empirical engineering/evaluation lane complete |
| **Track B2** | Persistent context and closure behavior | Standalone non-empirical engineering/evaluation lane complete |
| **Track B3** | Persistent graph-convergence monitoring | Standalone non-empirical engineering/evaluation lane complete |
| **Track C** | Integrated DGAF composition | Non-empirical composition proposal only; empirical execution not authorized |
| **Solo Epochs** | Historical developer-run bounded experiments | Historical exact-scope evidence; not automatically canonical DGAF evidence |

Accepted Epoch 002 tooling through #627 is preparation/validation evidence only. It does not promote any successor experiment predicate.

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

For the historical Track A Epoch 001 collection, use **50 paired inferential seed units / 2,250 blinded raw observations** rather than a bare `N=2250`.

For successor Epoch 002, no empirical collection has occurred and no scientific N is promoted. The separate canonical High-Assurance program remains at empirical **N=0**.

## Current external boundary

**DGAF has substantial engineering and governance implementation evidence. Track A Epoch 001 completed a governed prospective blinded collection, but its protected mapping is cryptographically unrecoverable and its primary analysis is unanalyzable/not run. The replacement Epoch 002 path has passed an operator-local, self-attested/non-independent custody-recovery drill and has prospective tooling through dataset-lock and separate unblinding-decision validation, but repository custody is not established, empirical collection is not authorized, no successor dataset lock or unblinding decision exists, primary analysis is not authorized or run, canonical DGAF efficacy is not established, and High-Assurance remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Public documentation rule

When a project-local term first appears on a designated public surface:

1. classify it as canonical identity, accepted alias, formation-local identity/designation, role/archetype, state, or external label;
2. check the vocabulary registry and accepted ontology adjudication;
3. lead with the plain-English function;
4. preserve identity and authority distinctions rather than silently collapsing them;
5. preserve verification, authorization, scientific-state, and efficacy ceilings;
6. link to technical/governance evidence when the distinction matters.

The dedicated Vocabulary Translation Matrix CI workflow checks registry structure, active-identity coverage, conflict/adjudication handling, authority/scientific non-effects, and this public layer.
