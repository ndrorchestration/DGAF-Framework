# DGAF Public Translation Layer

This document translates DGAF's internal vocabulary into plain, industry-neutral language for engineers, researchers, governance reviewers, hiring managers, and other external readers.

The goal is **translation, not renaming**. Internal names remain useful canonical identities inside DGAF, while public documentation leads with the function an external reader needs to understand.

The machine-readable authority for named-identity translation is `docs/VOCABULARY_TRANSLATION_MATRIX.json`. This document is its human-readable public surface.

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

## Vocabulary model: identity, role, alias, and public label are different things

DGAF vocabulary has four distinct layers. Public and internal documents should not collapse them:

1. **Canonical internal identity** — the stable project-local name, such as `Amethyst`, `Apogee`, `DemiJoule`, or `Sentinel-Phi`.
2. **Alias** — a historical or convenience name that resolves to one canonical identity, such as `Apogee Lens` → `Apogee` or historical `Sentinel` → `Sentinel-Phi`.
3. **Abstract role class** — an execution/archetype label such as `VERIFY`, `GOVERN`, `TRIBUNAL`, or `SENTINEL_ARCHETYPE`. A role class is not an agent identity and grants no authority by itself.
4. **External-facing functional label** — the industry-readable phrase used before the internal codename on public surfaces.

This distinction resolves a previously ambiguous case: **DemiJoule may occupy the AHG `Sentinel` archetype, but DemiJoule is not the canonical `Sentinel-Phi` governance/security identity.** Public documentation must not use the word `Sentinel` alone to imply DemiJoule and Sentinel-Phi are the same agent.

## Canonical agent vocabulary translation matrix

Public explanations lead with the external label and place the internal identity second on first use.

| Canonical internal identity | Accepted aliases | External-facing functional label | Authority / claim ceiling |
|---|---|---|---|
| **Amethyst** | — | **Governance Orchestrator** | Coordinates lifecycle/orchestration within inherited governance; does not independently establish scientific truth, owner authorization, independent verification, or efficacy |
| **COLLEEN** | — | **Continuity & Provenance Coordinator** | Preserves continuity, registry, provenance, durable state, and routing integrity; does not manufacture evidence or authorize experiments |
| **Apogee** | `Apogee Lens` | **Evidence & Verification Reviewer** | Performs evidence/verification review; the role name itself does not establish verifier independence |
| **Sentinel-Phi** | historical `Sentinel` | **Security & Policy Boundary Enforcer** | Canonical governance/security identity for veto/escalation inside inherited authority; alias is not a second active seat |
| **DemiJoule** | — | **Runtime Safety & Constraint Adviser** | Runtime-safety, efficiency, constraint, ethics, and error-containment analysis; advisory role does not independently authorize action |
| **Herald** | — | **Publication & External Communication Gatekeeper** | Publishes/classifies accepted evidence and external surfaces; cannot manufacture evidence or approval |
| **Professor Prodigy** | `Prodigy`, `Prof Prodigy` | **Formal Methods & Mathematical Analyst** | Formalization and mathematical checking; non-orchestrating and non-authorizing |
| **Nova** | — | **Simulation & Hypothesis Explorer** | Generates/explores alternatives; exploratory output is not authorization or verified evidence |
| **Perigee** | — | **Boundary & Input-Safety Filter** | Boundary/input filtering; not a substitute for governance authorization or independent security certification |
| **Reciprocity** | — | **Reciprocal-Impact & Fairness Reviewer** | Reviews affected-party/fairness/asymmetry concerns within its contract; does not certify fairness globally |
| **The Librarian** | `Librarian` | **Provenance & Decision Archivist** | Maintains traceability; traceability alone is not correctness or permission |
| **The Auditor** | `Auditor` | **Quality & Constraint Reviewer** | Internal QA/constraint review; not independent certification by default |
| **The Actualizer** | `Actualizer` | **Authorized Execution Worker** | Executes only after authorization predicates pass; capability never creates permission |
| **Zenith** | — | **Compute & Resource Coordinator** | Coordinates compute/resources; resource control creates no scientific/governance authority |

### Required first-use forms on public surfaces

Use these forms the first time the identity matters to an external reader:

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

After first use, either the functional label or the codename may be used when the referent is unambiguous.

### Internal versus external examples

Internal shorthand is allowed when the audience already shares the ontology:

> `Amethyst → Apogee → DemiJoule → Herald`

External prose should translate the same sequence functionally:

> The **Governance Orchestrator (Amethyst)** routes the candidate through **Evidence & Verification Review (Apogee)** and **Runtime Safety & Constraint Review (DemiJoule)** before the **Publication & External Communication Gatekeeper (Herald)** may release an accepted public artifact.

Avoid externally presenting a sentence such as “Amethyst invokes DemiJoule before Herald passes to Sentinel” without functional labels. It makes project-local identities look like unexplained technical standards and obscures which entity actually holds which authority.

## Naming and authority rules

- **Codename is identity, not capability.** `Amethyst` is not synonymous with “all orchestration,” and `Apogee` is not synonymous with “truth.”
- **Role class is not identity.** A `VERIFY`, `GOVERN`, `Explorer`, `Auditor`, or `Sentinel` archetype does not create a new agent or change normative authority.
- **Alias is one-way compatibility.** `Apogee Lens` resolves to `Apogee`; historical `Sentinel` resolves to `Sentinel-Phi`. New public material should prefer the canonical identity.
- **Independence is evidence, not branding.** No label containing “review,” “audit,” or “verification” implies independent verification unless a separate accepted independence record establishes it.
- **Named agents are project-local constructs.** Their names must not be presented as established industry protocols, certifications, or standard roles.
- **Translation has no scientific-state effect.** Changing the public label or explanatory wording cannot change experiment state, authorization, verification class, scientific N, or efficacy.

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
- "The Governance Orchestrator (Amethyst) coordinates the transition, while evidence review and authorization remain separately bounded."
- "The Evidence & Verification Reviewer (Apogee) performs internal verification review; verifier independence is recorded separately."
- "The Runtime Safety & Constraint Adviser (DemiJoule) provides bounded constraint analysis and does not independently authorize the action."
- "Track A completed its governed prospective blinded collection, but its locked primary analysis has not run."
- "Track A verification is developer self-attested/non-independent, not independent validation."
- "The repository contains prospective Track A collection evidence, but canonical DGAF efficacy is not established."
- "Internal qualification and CI results are scoped engineering evidence, not independent certification."

Avoid statements such as:

- "DGAF is proven."
- "DGAF is independently validated" unless an independent verification record establishes that claim.
- Unqualified claims of production readiness without an explicit production-readiness criterion and supporting evidence.
- "Amethyst approved the science" when the actual event was orchestration or commit coordination.
- "Apogee independently verified" unless an accepted independent-verification record exists.
- Using `Sentinel` ambiguously for both Sentinel-Phi and DemiJoule's AHG archetype.
- "Track A scientific N is 2250" without clarifying inferential units versus raw observations.
- "Track A has a positive/negative primary result" before the locked primary analysis runs.
- "Unblinding authorization means analysis is authorized."
- "Collection proves efficacy."
- "Freeze means authorized."
- "A passing internal score is an industry certification."

## Public documentation rule

When an internal DGAF term first appears on a public-facing surface:

1. resolve the identity through `docs/VOCABULARY_TRANSLATION_MATRIX.json` when it is a named agent;
2. state the **plain-English function first**;
3. give the canonical internal identity second in parentheses when useful;
4. do not substitute an alias or abstract role class for the canonical identity;
5. identify whether the statement is architecture, engineering evidence, empirical evidence, verification class, or authorization state;
6. preserve the claim and authority ceiling;
7. link to the exact technical/governance record for readers who need the internal ontology.

The dedicated `Vocabulary Translation Matrix` CI workflow validates the registry, required aliases, key external labels, Sentinel/DemiJoule disambiguation, and this document's first-use forms.

This translation rule is intended to make DGAF easier to understand without weakening its internal governance semantics.
