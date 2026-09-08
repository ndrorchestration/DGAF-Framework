# DGAF Public Translation Layer

This document translates DGAF's internal vocabulary into plain, industry-neutral language for engineers, researchers, governance reviewers, hiring managers, and other external readers.

The goal is **translation, not renaming**. Internal names can remain canonical inside DGAF while public documentation explains what function each term actually serves.

## One-sentence description

**DGAF is an experimental governed-agent framework in which evidence, verification, authority, and permission to act are tracked separately so that an AI system cannot silently promote capability into authorization or testing into proof.**

## Core concepts

| DGAF term | Public translation | What it means | What it does **not** mean |
|---|---|---|---|
| **DGAF** | Governed multi-agent orchestration and evaluation framework | A system for coordinating agents under explicit evidence, authority, provenance, and execution rules | Evidence of complete-framework empirical validation or production certification |
| **Formation** | Governed agent configuration | Which agents participate, how they are connected, and what authority each has for a task | A claim that more agents automatically improve performance |
| **Agent authority** | Role-bounded decision rights | What an agent may decide, verify, veto, escalate, or execute | General model capability |
| **Governance Envelope** | Inherited policy and authority boundary | Limits downstream tool, data, risk, resource, and decision scope | A generic content filter |
| **Control Plane** | Lifecycle and orchestration controller | Enforces legal state transitions, resource bounds, provenance, recursion, and execution rules | The scientific experiment itself |
| **TGL / P-35** | Per-turn governance kernel | Evaluates required governance state for an individual turn/action and propagates PASS/WARN/SKIP/ESCALATE/KILL semantics | An industry-standard protocol name |
| **P-* gate** | Project-specific checkpoint | A defined evidence, quality, security, policy, verification, or authorization predicate | Certification merely because a gate passes |
| **CommitGate** | Explicit commit/action authorization boundary | Separates proposed work from permission to commit a consequential state change | Permission inferred from technical ability |
| **PDMAL** | Experimental topology and robustness substrate | The graph/topology research apparatus used in DGAF's numeric robustness work | The whole DGAF framework |
| **Fail closed** | Deny progression when prerequisites are not proven | Missing, malformed, stale, ambiguous, or mismatched required evidence blocks the transition | Treating unknown as failure of the underlying hypothesis |
| **Provenance** | Source and decision lineage | Records what code, evidence, artifact, system state, and authority produced a result | Proof that the result is correct merely because it is traceable |
| **Evidence binding** | Exact identity binding | Ties a claim or authorization to specific commits, trees, blobs, artifacts, protocol identities, and retained evidence | Automatic transfer of evidence to later versions |
| **Claim promotion** | Evidence-based change in epistemic status | Moves a statement from proposed/implemented/tested toward verified or empirically demonstrated only when its required evidence exists | Marketing promotion |
| **Verification classification** | Verifier-independence record | Records whether verification was developer self-attested, same-system/non-independent, or independently produced | A guarantee of correctness from self-validation |
| **Freeze** | Immutable experimental candidate binding | Locks the exact candidate and protected experiment inputs before later authorization | Permission to collect data |
| **Closure** | Pre-authorization completeness proof | Shows required frozen prerequisites and blockers have been reconciled | Permission to collect data |
| **Collection authorization** | Explicit permission to execute the prospective experiment | A distinct governed event that permits the locked prospective data collection after prior gates are valid | Evidence that collection already happened, unblinding, efficacy, or production approval |
| **Unblinding** | Controlled release of protected treatment identity | Reveals protected labels/keys only after the required dataset-lock and authorization sequence | Something allowed during ordinary collection |
| **Scientific N** | Number of authorized prospective experimental observations actually collected | Counts observations admitted under the governing scientific protocol | Number of tests, commits, CI jobs, historical records, or merely authorized observations |
| **High-Assurance** | Stricter canonical assurance program | A separate evidence/authorization program with higher custody and verification requirements | The same thing as Track A freeze or Track A collection authorization |

## Agent-role translation

DGAF uses named agents as role identifiers. Public explanations should lead with the role, then optionally include the internal name.

| Internal agent | Public role description |
|---|---|
| **Amethyst** | Meta-orchestration and final governance/commit authority |
| **Apogee** | Evidence and verification governance |
| **Perigee** | Boundary and security filtering |
| **Nova** | Simulation and exploratory innovation |
| **Professor Prodigy** | Formalization and proof-oriented analysis |
| **COLLEEN** | Operational continuity, archival coordination, and gap tracking |
| **The Librarian** | Provenance and decision archive |
| **The Auditor** | QA and constraint verification |
| **The Actualizer** | Authorized execution and artifact/code generation |
| **Zenith** | Compute/resource coordination |
| **Reson** | Coherence-scoring/advisory role within the project ontology |
| **Lyra** | Synthesis and narrative integration |
| **Echolette** | Pattern/temporal-coherence advisory role |
| **Ionia** | Modal/state-coherence advisory role |

Public documentation should avoid presenting project-specific agent names, thresholds, scores, or metaphors as established industry constructs unless an external standard or empirical result actually supports that interpretation.

## Research-track translation

| Track | Plain-English scope | Current public interpretation |
|---|---|---|
| **Track A** | Numeric topology robustness experiment | Prospective scientific lane; preregistered, frozen, closed, developer-self-attested/non-independently verified, and authorized for prospective collection; collection has not started and unblinding remains prohibited |
| **Track B1** | Semantic routing and safety behavior | Standalone non-empirical engineering/evaluation lane complete |
| **Track B2** | Persistent context and closure behavior | Standalone non-empirical engineering/evaluation lane complete |
| **Track B3** | Persistent graph-convergence monitoring | Standalone non-empirical engineering/evaluation lane complete |
| **Track C** | Integrated DGAF composition | Non-empirical composition proposal only; empirical execution not authorized |
| **Solo Epochs** | Historical developer-run bounded experiments | Exact-scope historical evidence; not automatically canonical DGAF evidence |

## Evidence-state translation

DGAF should explain evidence status using ordinary language first.

| Internal / formal state | Plain-English meaning |
|---|---|
| **PROPOSED** | Designed but not yet implemented or demonstrated |
| **IMPLEMENTED** | Exists in code/artifacts |
| **TESTED** | Covered by the stated tests in the stated environment |
| **PASS** | The exact defined predicate passed; scope does not automatically widen |
| **VERIFIED** | Supporting evidence satisfied the defined verification predicate |
| **DEVELOPER SELF-ATTESTED / NONINDEPENDENT** | Checked by the same developer/system lineage; useful but not independent validation |
| **INDEPENDENTLY VERIFIED** | Verified through a separately defined independent authority/evidence path |
| **FREEZE ESTABLISHED** | Exact experiment identity is immutably bound |
| **CLOSURE ESTABLISHED** | Required pre-authorization closure conditions are satisfied |
| **COLLECTION AUTHORIZED** | The exact prospective collection may now run; this does not mean it already ran |
| **NOT AUTHORIZED** | The named execution remains prohibited regardless of technical readiness |
| **NOT ESTABLISHED** | The evidence required for the claim does not currently exist or has not satisfied the required predicate |
| **EMPIRICALLY DEMONSTRATED** | Supported by an executed experiment within the exact stated scope |

## Public explanation of the current boundary

A concise external explanation of the present state is:

> **DGAF has substantial engineering and governance implementation evidence. Its Track A prospective experiment has been preregistered, analysis-locked, preflighted, frozen, closed, classified as developer self-attested/non-independent verification, and explicitly authorized for prospective collection. The authorized 2,250-observation panel has not yet been collected, scientific N remains 0, unblinding remains prohibited, and canonical DGAF efficacy remains not established.**

This preserves three separate facts:

1. **Track A has legitimately advanced through collection authorization.**
2. **Authorization is not execution or empirical support.**
3. **The canonical High-Assurance program remains PRE-FREEZE / NOT AUTHORIZED / N=0.**

Those statements are not contradictory because they refer to different research/assurance boundaries and evidence states.

## Preferred external wording

Prefer statements such as:

- "DGAF mechanically separates technical capability from authorization."
- "The framework binds governance and evidence states to exact system identities."
- "Track A is authorized for its locked prospective collection, but the fresh panel has not run yet."
- "Track A verification is developer self-attested/non-independent, not independent validation."
- "The repository contains substantial engineering evidence, but canonical DGAF efficacy is not established."
- "Internal qualification and CI results are scoped engineering evidence, not independent certification."

Avoid statements such as:

- "DGAF is proven."
- "DGAF is independently validated" unless an independent verification record actually establishes that claim.
- "DGAF is production-ready" unless production-readiness evidence exists under an explicit criterion.
- "Track A is pre-freeze" after its immutable freeze has been established.
- "Track A has empirical results" before the authorized prospective panel is actually collected.
- "Collection authorization proves efficacy."
- "Freeze means authorized."
- "A passing internal score is an industry certification."
- "The named agent ontology is an industry-standard taxonomy."

## Public documentation rule

When an internal DGAF term first appears on a public-facing surface:

1. state the **plain-English function first**;
2. give the internal name second when useful;
3. identify whether the statement is architecture, engineering evidence, empirical evidence, verification class, or authorization state;
4. preserve the claim ceiling;
5. link to the exact technical/governance record for readers who need the internal ontology.

Example:

> **Evidence verifier (Apogee)** checks whether the required source and evidence predicates are satisfied. Its internal verification does not count as independent validation unless the governing verification classification explicitly says so.

This translation rule is intended to make DGAF easier to understand without weakening its internal governance semantics.
