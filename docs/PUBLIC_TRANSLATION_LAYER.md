# DGAF Public Translation Layer

This document translates DGAF's internal vocabulary into plain, industry-neutral language for engineers, researchers, governance reviewers, hiring managers, and other external readers.

The goal is **translation, not renaming**. Internal names can remain canonical inside DGAF while public documentation explains what function each term actually serves.

## One-sentence description

**DGAF is an experimental governed-agent framework in which evidence, verification, authority, and permission to act are tracked separately so that an AI system cannot silently promote capability into authorization or testing into proof.**

## Core concepts

| DGAF term | Public translation | What it means | What it does **not** mean |
|---|---|---|---|
| **DGAF** | Governed multi-agent orchestration and evaluation framework | Coordinates agents under explicit evidence, authority, provenance, and execution rules | Complete-framework empirical validation or production certification |
| **Formation** | Governed agent configuration | Which agents participate, how they are connected, and what authority each has | More agents automatically improve performance |
| **Agent authority** | Role-bounded decision rights | What an agent may decide, verify, veto, escalate, or execute | General model capability |
| **Governance Envelope** | Inherited policy and authority boundary | Limits downstream tool, data, risk, resource, and decision scope | A generic content filter |
| **Control Plane** | Lifecycle and orchestration controller | Enforces legal state transitions, resource bounds, provenance, recursion, and execution rules | The scientific experiment itself |
| **TGL / P-35** | Per-turn governance kernel | Evaluates required governance state for an action and propagates project-defined control semantics | An industry-standard protocol name |
| **P-* gate** | Project-specific checkpoint | A defined evidence, quality, security, policy, verification, or authorization predicate | Certification merely because a gate passes |
| **CommitGate** | Explicit commit/action authorization boundary | Separates proposed work from permission to commit a consequential state change | Permission inferred from technical ability |
| **PDMAL** | Experimental topology and robustness substrate | Graph/topology apparatus used in DGAF's numeric robustness work | The whole DGAF framework |
| **Fail closed** | Deny progression when prerequisites are not proven | Missing, malformed, stale, ambiguous, or mismatched evidence blocks transition | Treating unknown as proof that the underlying hypothesis failed |
| **Provenance** | Source and decision lineage | Records what code, evidence, artifact, state, and authority produced a result | Proof that a result is correct merely because it is traceable |
| **Evidence binding** | Exact identity binding | Ties a claim or authorization to specific commits, trees, blobs, artifacts, protocol identities, and retained evidence | Automatic transfer of evidence to later versions |
| **Claim promotion** | Evidence-based change in epistemic status | Moves a statement toward verified or empirically demonstrated only when required evidence exists | Marketing promotion |
| **Verification classification** | Verifier-independence record | Records whether verification was developer self-attested/same-system or independently produced | A guarantee of correctness from self-validation |
| **Freeze** | Immutable experimental candidate binding | Locks the exact candidate and protected experiment inputs | Permission to collect data |
| **Closure** | Pre-authorization completeness proof | Shows required frozen prerequisites and blockers have been reconciled | Permission to collect data |
| **Collection authorization** | Permission to execute the prospective collection | Allows the exact locked prospective data collection after prerequisites pass | Evidence that collection already happened or that efficacy is established |
| **Dataset lock** | Immutable collected-dataset receipt | Binds the accepted collected dataset and retained artifact identities | Analysis or efficacy evidence by itself |
| **Unblinding authorization** | Controlled permission to release protected treatment identity | Allows mapping/key release and protected-artifact decryption for the exact locked dataset | Permission to run the primary analysis |
| **Materialization** | Deterministic construction of analysis-ready unblinded input | Joins the protected topology mapping back to the blinded records under the authorized path | Outcome aggregation or primary analysis |
| **Primary-analysis authorization** | Separate permission to run the locked confirmatory analysis | Allows only the preregistered locked estimator after the unblinded-input receipt is established | Permission for exploratory pooling or a canonical efficacy claim |
| **High-Assurance** | Stricter canonical assurance program | Separate evidence/authorization program with higher custody and verification requirements | The same thing as Track A freeze or Track A collection |

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

Project-specific names, thresholds, scores, or metaphors should not be presented as established industry constructs unless external evidence supports that interpretation.

## Research-track translation

| Track | Plain-English scope | Current public interpretation |
|---|---|---|
| **Track A** | Numeric topology robustness experiment | Prospective blinded collection complete under the locked protocol; 50 paired inferential seed units / 2,250 blinded raw observations retained; dataset lock and unblinding authorization established; custody-key handoff and unblinded-input materialization pending; primary analysis not authorized/run |
| **Track B1** | Semantic routing and safety behavior | Standalone non-empirical engineering/evaluation lane complete |
| **Track B2** | Persistent context and closure behavior | Standalone non-empirical engineering/evaluation lane complete |
| **Track B3** | Persistent graph-convergence monitoring | Standalone non-empirical engineering/evaluation lane complete |
| **Track C** | Integrated DGAF composition | Non-empirical composition proposal only; empirical execution not authorized |
| **Solo Epochs** | Historical developer-run bounded experiments | Exact-scope historical evidence; not automatically canonical DGAF evidence |

## Evidence-state translation

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
| **COLLECTION AUTHORIZED** | The exact prospective collection may run; this does not mean it already ran |
| **COLLECTION COMPLETE** | The authorized prospective collection executed and its admitted observations were retained |
| **DATASET LOCK ESTABLISHED** | The accepted dataset and retained artifact identities are immutably receipted |
| **UNBLINDING AUTHORIZED** | Protected mapping release/decryption may occur under the exact authorized path |
| **NOT AUTHORIZED** | The named execution remains prohibited regardless of technical readiness |
| **NOT ESTABLISHED** | Required evidence for the claim does not currently exist or has not satisfied its predicate |
| **EMPIRICALLY DEMONSTRATED** | Supported by an executed experiment within the exact stated scope |

## Scientific-unit wording

For Track A, avoid using a bare `N=2250` because the inferential unit and raw record count are different:

- **50 paired inferential seed units**;
- **2,250 blinded raw observations** across the fixed seed × topology × failure matrix.

The canonical High-Assurance program remains separately at **empirical N=0**.

## Public explanation of the current boundary

A concise external explanation is:

> **DGAF has substantial engineering and governance implementation evidence. Track A's locked prospective experiment has completed blinded collection under its governed protocol, producing 50 paired inferential seed units and 2,250 blinded raw observations with an established dataset lock. Unblinding is authorized only for controlled mapping release/decryption, but the matching custody-key handoff and unblinded-input materialization have not yet been established. Primary analysis has not been authorized or run, and canonical DGAF efficacy remains not established.**

This preserves four separate facts:

1. **Track A has legitimately completed governed prospective collection.**
2. **Collection is not primary analysis.**
3. **Unblinding authorization is not primary-analysis authorization.**
4. **The canonical High-Assurance program remains PRE-FREEZE / NOT AUTHORIZED / N=0.**

## Preferred external wording

Prefer statements such as:

- "DGAF mechanically separates technical capability from authorization."
- "The framework binds governance and evidence states to exact system identities."
- "Track A completed its governed prospective blinded collection, but its locked primary analysis has not run."
- "Track A verification is developer self-attested/non-independent, not independent validation."
- "The repository contains prospective Track A collection evidence, but canonical DGAF efficacy is not established."
- "Internal qualification and CI results are scoped engineering evidence, not independent certification."

Avoid statements such as:

- "DGAF is proven."
- "DGAF is independently validated" unless an independent verification record establishes that claim.
- Unqualified claims of production readiness without an explicit production-readiness criterion and supporting evidence.
- "Track A scientific N is 2250" without clarifying inferential units versus raw observations.
- "Track A has a positive/negative primary result" before the locked primary analysis runs.
- "Unblinding authorization means analysis is authorized."
- "Collection proves efficacy."
- "Freeze means authorized."
- "A passing internal score is an industry certification."

## Public documentation rule

When an internal DGAF term first appears on a public-facing surface:

1. state the **plain-English function first**;
2. give the internal name second when useful;
3. identify whether the statement is architecture, engineering evidence, empirical evidence, verification class, or authorization state;
4. preserve the claim ceiling;
5. link to the exact technical/governance record for readers who need the internal ontology.

This translation rule is intended to make DGAF easier to understand without weakening its internal governance semantics.
