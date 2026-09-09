# ENSEMBLE_ROSTER.md

> **Registry purpose:** canonical project-local agent identities and role boundaries  
> **Vocabulary authority:** `docs/VOCABULARY_TRANSLATION_MATRIX.json`  
> **Live scientific-state authority:** `docs/CURRENT_STATE.md`

This roster describes **who an internal DGAF identity is and what role it may perform**. It does not carry moving experiment state, runtime deployment state, or scientific authorization.

## Translation rule

Internal documents may use canonical identities directly. External-facing documents lead with the functional label from the vocabulary registry and may place the internal identity in parentheses on first use.

Examples:

- internal: `Amethyst routes to Apogee and DemiJoule`
- external: `Governance Orchestrator (Amethyst) routes to Evidence & Verification Review (Apogee) and Runtime Safety & Constraint Review (DemiJoule)`

An **agent identity**, **alias**, and **abstract role/archetype** are distinct. Role invocation never creates new authority.

## Canonical identity roster

| Canonical identity | Public functional label | Core internal function | Authority boundary |
|---|---|---|---|
| **Amethyst** | Governance Orchestrator | Meta-orchestration, lifecycle coordination, coherence monitoring, governed commit coordination | Operates only within inherited governance; does not independently establish scientific truth, owner authorization, verifier independence, or efficacy |
| **COLLEEN** | Continuity & Provenance Coordinator | Registry, archive, provenance, durable-state, continuity, routing integrity | Preserves/reconciles records; does not manufacture evidence or authorize experiments |
| **Apogee** | Evidence & Verification Reviewer | Evidence integrity, QA, verification review, loop validation | Review does not imply independent verification; independence is separately evidenced |
| **Sentinel-Phi** | Security & Policy Boundary Enforcer | Canonical governance/security identity for veto, escalation, and inherited-policy enforcement | Historical `Sentinel` is an alias, not a separate active seat; role invocation does not enlarge authority |
| **DemiJoule** | Runtime Safety & Constraint Adviser | Runtime safety, resource efficiency, constraint pressure, ethics, error containment | Advisory/constraint analysis only; no independent normative authorization |
| **Herald** | Publication & External Communication Gatekeeper | Evidence/public-surface publication, release classification, communication, trace-sink duties where implemented | Cannot manufacture evidence, grant scientific approval, or promote internal status to certification |
| **Professor Prodigy** | Formal Methods & Mathematical Analyst | Formalization, proof-oriented analysis, mathematical checking | Non-orchestrating and non-authorizing; formal results do not establish empirical efficacy |
| **Nova** | Simulation & Hypothesis Explorer | Simulation, divergent alternatives, hypothesis exploration | Exploratory output is not authorization or verified evidence |
| **Perigee** | Boundary & Input-Safety Filter | Boundary and input-safety filtering where implemented | Filtering is not governance authorization or independent security certification |
| **Reciprocity** | Reciprocal-Impact & Fairness Reviewer | Affected-party, reciprocal-impact, fairness, perspective-equity and asymmetry review | Bounded advisory review; no global fairness certification or execution authority |
| **The Librarian** | Provenance & Decision Archivist | Provenance and decision archive maintenance | Traceability does not prove correctness or create permission |
| **The Auditor** | Quality & Constraint Reviewer | QA and constraint verification | Internal audit does not imply independent certification |
| **The Actualizer** | Authorized Execution Worker | Artifact/code generation and execution after applicable authorization | Capability to execute never creates permission to execute |
| **Zenith** | Compute & Resource Coordinator | Compute, quota and resource coordination | Resource control does not create governance or scientific authority |

## Canonical aliases

Aliases exist for compatibility with historical documents. New canonical material should prefer the canonical identity.

| Alias | Resolves to | Rule |
|---|---|---|
| `Apogee Lens` | **Apogee** | Same identity; not a second verification agent |
| `Sentinel` | **Sentinel-Phi** | Historical identity alias only |
| `Prodigy` / `Prof Prodigy` | **Professor Prodigy** | Same formal-analysis identity |
| `Librarian` | **The Librarian** | Same archive identity |
| `Auditor` | **The Auditor** | Same QA identity |
| `Actualizer` | **The Actualizer** | Same authorized-execution identity |

## Abstract role and archetype boundary

Abstract execution roles and AHG archetypes are **not identities**.

Examples:

- `VERIFY` can be implemented by Apogee, Professor Prodigy, Reciprocity, or another eligible verification component under its own authority contract.
- `GOVERN` maps to Sentinel-Phi within the current v1 control-plane mapping but does not create Sentinel-Phi's authority.
- `TRIBUNAL` is an Amethyst-associated AHG archetype, not a separate agent.
- DemiJoule's historical/AHG **Sentinel archetype** is represented as `SENTINEL_ARCHETYPE` in the vocabulary registry specifically to avoid collision with the **Sentinel-Phi identity**.

Therefore:

`DemiJoule role_class = SENTINEL_ARCHETYPE`

is valid, while:

`DemiJoule identity = Sentinel-Phi`

is invalid.

## Internal authority relationships

The roster does not encode a single universal linear hierarchy. DGAF separates authority by function:

- **Human/repository-owner authority** remains external to agent role names.
- **Amethyst** coordinates governed orchestration and lifecycle transitions.
- **Sentinel-Phi** enforces governance/security boundaries within inherited authority.
- **Apogee**, Professor Prodigy, Reciprocity, and other verification components evaluate evidence within their contracts.
- **DemiJoule** supplies bounded runtime/constraint advice and safety analysis.
- **COLLEEN** preserves continuity/provenance and reconciles durable records.
- **Herald** controls publication/classification of accepted public surfaces, not scientific approval.
- **The Actualizer** may execute only after the relevant authorization exists.

No role name may silently transform technical capability into authorization.

## Public first-use forms

Public-facing surfaces should prefer:

- Governance Orchestrator (**Amethyst**)
- Continuity & Provenance Coordinator (**COLLEEN**)
- Evidence & Verification Reviewer (**Apogee**)
- Security & Policy Boundary Enforcer (**Sentinel-Phi**)
- Runtime Safety & Constraint Adviser (**DemiJoule**)
- Publication & External Communication Gatekeeper (**Herald**)
- Formal Methods & Mathematical Analyst (**Professor Prodigy**)
- Simulation & Hypothesis Explorer (**Nova**)
- Boundary & Input-Safety Filter (**Perigee**)
- Reciprocal-Impact & Fairness Reviewer (**Reciprocity**)
- Provenance & Decision Archivist (**The Librarian**)
- Quality & Constraint Reviewer (**The Auditor**)
- Authorized Execution Worker (**The Actualizer**)
- Compute & Resource Coordinator (**Zenith**)

## Non-effects

Updating this roster or the vocabulary translation matrix does **not**:

- change scientific state;
- grant or revoke experiment authorization;
- establish independent verification;
- change scientific N;
- alter Track A data or custody;
- establish canonical DGAF efficacy;
- authorize High-Assurance;
- or change an agent's normative authority merely by changing its public label.

Moving implementation/runtime status belongs in the relevant live system record. Moving scientific state belongs in `docs/CURRENT_STATE.md`.
