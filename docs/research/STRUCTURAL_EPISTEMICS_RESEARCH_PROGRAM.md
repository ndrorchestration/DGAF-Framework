# Structural Epistemics for Agentic Systems — Research Program

> **Status:** EXPLORATORY / NON-AUTHORIZING / NO SCIENTIFIC-STATE EFFECT  
> **Date established:** 2026-09-17  
> **Repository baseline:** `4aa867ce92d4a4561b8d67639cdebca222815647`  
> **Scope:** DGAF/PDMAL research formalization and cross-project methodological guidance.

## Authority boundary

This document is a research program, not a control-state authority, experiment amendment, authorization record, efficacy result, or production certification.

The live DGAF/PDMAL state remains controlled by `docs/CURRENT_STATE.md` and the exact accepted governance/evidence records. At establishment of this program:

- canonical High-Assurance DGAF remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**;
- Track A Epoch 002 collection is complete and its dataset lock is **ESTABLISHED**;
- Epoch 002 bounded unblinding is **AUTHORIZED** only for controlled mapping release/decryption;
- real Epoch 002 materialization is **NOT ESTABLISHED**;
- primary analysis is **NOT AUTHORIZED / NOT RUN**;
- `SCIENTIFIC_N_INCREMENT = 0`;
- canonical DGAF efficacy and independent validation remain **NOT ESTABLISHED**.

Nothing in this document changes those predicates. New constructs below are prospective research objects unless an already-accepted artifact explicitly says otherwise.

## Research thesis

Reliable agentic behavior depends not only on model capability but on the structure through which evidence, messages, authority, and feedback propagate.

The central research question is:

> **How do communication topology, evidence dependence, authorization structure, and feedback dynamics determine whether an agentic system corrects errors or amplifies them?**

A useful research decomposition is:

```text
Reliable agentic behavior = f(
    communication topology,
    evidence independence,
    provenance structure,
    authorization constraints,
    uncertainty,
    feedback and containment
)
```

This is a research framing, not a claim that a single closed-form function has been established.

## Alignment and assurance boundary

Mathematical/formal constraint methods are one layer of AI assurance, not a complete solution to alignment.

A useful systems decomposition is:

```text
alignment / trustworthy-operation outcome =
  normative values and specification
  + training dynamics / learned behavior
  + model internals
  + runtime control and security
  + evaluation and assurance
  + deployment environment
  + institutional governance
```

Each layer can fail independently. Strong tool-boundary controls do not prove that a model is honest or internally aligned; a behaviorally aligned model does not establish operator legitimacy; a successful evaluation does not establish safety under every novel environment.

DGAF's strongest current design domain is **runtime control, evidence/provenance, authorization, evaluation/assurance structure, and explicit governance state**. It interfaces with but does not claim to solve normative legitimacy, inner alignment, mechanistic interpretability, scalable oversight, corrigibility, or value aggregation.

For operational evaluation, the relevant object is normally the **deployed system** rather than the bare model:

```text
model + prompts + memory + retrieval + tools + permissions
+ human workflow + network/runtime environment + monitoring
```

The prospective Alignment Constraint Ledger therefore defines a **control envelope** over bounded consequential actions. It does not imply complete model alignment.

## Scope and non-scope

### In scope

1. Correlated epistemic failure across apparently independent agents.
2. Provenance overlap and effective verification diversity.
3. Communication-topology effects on fault propagation and correction.
4. Formal governance state transitions and authorization invariants.
5. Runtime feedback, containment, rollback/compensation, and escalation.
6. Action-admission control envelopes with explicit assumptions and residual risk.
7. Spectral or harmonic methods where the underlying object is genuinely a graph, signal, time series, geometric field, or dynamical system.

### Out of scope without separate evidence

1. Treating harmonic, musical, geometric, phi-derived, or other mathematically elegant structure as a universal mechanism for LLM agents.
2. Inferring empirical robustness from a graph property alone.
3. Treating repeated agent agreement as independent corroboration without provenance analysis.
4. Retrofitting newly discovered predictors or endpoints into a locked confirmatory experiment.
5. Promoting an analogy into a mechanism claim without a model and test capable of falsifying it.
6. Treating formal compliance with a specified policy as proof that the policy fully represents legitimate human values.
7. Treating runtime governance as proof of inner alignment, general corrigibility, or complete deceptive-intent detection.

## Core constructs

### 1. Communication graph

Let an agent communication structure be represented as a graph

```text
G = (V, E)
```

where vertices are agents or controlled processing roles and edges represent permitted information flow. Direction, weight, timing, and message class must be included when materially relevant.

Graph structure is an experimental factor or predictor. A structural property does **not** by itself establish an agentic outcome.

### 2. Evidence-provenance graph

Let a provenance graph

```text
H = (C, S, A, T, P, R)
```

represent claims `C`, sources `S`, agents/models `A`, tools `T`, prompts/policies `P`, and review/approval events `R`, with typed edges indicating derivation, retrieval, transformation, delegation, review, or authorization.

The purpose of `H` is to distinguish multiple outputs from multiple genuinely distinct evidence paths.

### 3. Dependency signature

For verifier or agent `v_i`, define a dependency signature:

```text
d_i = {
  model/provider lineage,
  prompt/policy lineage,
  retrieved source identifiers,
  upstream agent outputs,
  tool outputs,
  memory/context snapshot,
  adjudicator dependencies
}
```

This is an audit representation. It does not imply statistical independence can be inferred from metadata alone.

### 4. Apparent consensus vs evidence diversity

Agent count and independent verification-path count are distinct quantities:

```text
N_agents != N_independent_verification_paths
```

Five agents deriving the same claim from one erroneous source create five outputs but may still share a single critical provenance root.

### 5. Epistemic amplification

For a claim `c`, define a prospective amplification statistic:

```text
A_c = post_interaction_prevalence_or_confidence(c)
      / max(pre_interaction_prevalence_or_confidence(c), epsilon)
```

and track independent evidence gain separately as `DeltaE_c`.

A candidate failure pattern is:

```text
A_c >> 1  AND  DeltaE_c ~= 0
```

This is an operational definition for future evaluation, not a validated universal metric. Confidence aggregation must not be used unless the component confidence values are themselves meaningful and calibrated.

### 6. Control envelope

For a consequential action class, define the control envelope as the actions for which exact preconditions, authority, verification requirements, authorization, execution evidence, postcondition checks, recovery semantics, and declared assumptions can be bound and enforced.

The prospective specification is `../governance/ALIGNMENT_CONSTRAINT_LEDGER.md`.

The design target is normative—actions requiring a ledger entry should eventually be prevented from execution when the entry is missing or invalid—but **that enforcement is not established by this research PR**.

## Research questions

### RQ1 — Correlated verification

When does apparent multi-agent consensus cease to provide additional evidential value because agents share models, sources, prompts, upstream outputs, tools, or adjudicators?

### RQ2 — Topology and fault propagation

Which structural graph properties, if any, prospectively predict resilience, correction latency, false-consensus persistence, communication cost, or blast radius under controlled failure?

### RQ3 — Provenance-aware verification

Can claim-to-source and claim-to-agent provenance detect false consensus more reliably than raw agreement counts?

### RQ4 — Governance as a transition system

Can identity, evidence, approval, execution, recovery, and revocation be represented as enforceable state-transition invariants that fail closed at the tool boundary?

### RQ5 — Spectral methods under literal applicability

When the system is genuinely graph-, signal-, or time-dependent, do spectral representations explain or predict behavior beyond simpler non-spectral baselines?

### RQ6 — Constraint-envelope assurance

For bounded consequential actions, can a typed action-admission record plus exact identity binding, authority attenuation, commit-time revalidation, receipts, postcondition checks, and failure-oriented tests reduce unauthorized or incorrectly authorized side effects under controlled attack/fault conditions?

This is an empirical/engineering research question. The specification itself does not answer it.

## Workstreams

### Workstream A — Correlated Verification Threat Model

Formalize shared-source monoculture, inherited-output contamination, model-family correlation, judge/verifier correlation, provenance aliasing, and synthetic consensus. See `../governance/CORRELATED_VERIFICATION_THREAT_MODEL.md`.

### Workstream B — Governed Transition System

Specify the state machine and invariants separating evidence, authorization, execution, side effects, recovery, and audit. See `../formalism/AGENT_GOVERNANCE_TRANSITION_SPEC.md`.

### Workstream C — PDMAL Structural Predictor Registry

Predeclare graph measures that may later be investigated as predictors while quarantining them from the currently locked primary analysis. See `../experiment/PDMAL_STRUCTURAL_PREDICTOR_REGISTRY.md`.

### Workstream D — Critical-Edge / Ablation Research

Define a separate prospective protocol for estimating the causal importance of communication edges. See `../experiment/PDMAL_CRITICAL_EDGE_ABLATION_PROTOCOL.md`.

### Workstream E — Mathematical Claim Classification

Require mathematical language to be labeled as analogy, design heuristic, mathematical property, empirical hypothesis, or empirically supported claim. See `MATHEMATICAL_CLAIM_CLASSIFICATION_STANDARD.md`.

### Workstream F — Bounded Action Assurance

Specify a prospective normative Alignment Constraint Ledger / Action Admission Record, preserve the existing DGAF evidence semantics, trace reusable ecosystem patterns, and define a separate implementation tranche rather than claiming documentation is runtime enforcement.

See:

- `../governance/ALIGNMENT_CONSTRAINT_LEDGER.md`;
- `CONTROL_ENVELOPE_PATTERN_ADOPTION_MATRIX.md`;
- `../superpowers/specs/2026-09-17-action-admission-control-envelope-design.md`.

## Prospective correlated-verification experiment

A future experiment may manipulate verifier independence without using or altering the locked Epoch 002 primary analysis.

| Condition | Model composition | Evidence acquisition | Prior agent outputs visible |
|---|---|---|---|
| A | Same or closely related | Shared | Yes |
| B | Same or closely related | Independent | No |
| C | Heterogeneous | Shared | No |
| D | Heterogeneous | Independent | No |

Possible controlled intervention: introduce known misleading evidence at a preregistered rate and measure:

- unsupported-claim acceptance;
- false acceptance conditional on apparent consensus;
- source concentration and source diversity;
- pairwise evidence overlap;
- minority correction success;
- contradiction survival;
- claim amplification without novel evidence;
- latency, tool cost, and escalation rate.

Any such experiment requires a separate protocol, fresh prospective data, explicit authorization, and a declared analysis plan before execution.

## PDMAL relationship

PDMAL supplies an experimental setting for topology/failure research, but structural mathematics remains predictor-level or mechanism-hypothesis evidence until empirical testing supports more.

A future structural model may examine:

```text
Topology
  -> structural predictors {connectivity, algebraic connectivity, expansion,
                            centralization, path redundancy, curvature, ...}
  -> observed resilience / correction / cost outcomes
```

The direction arrows above denote a research model, not demonstrated causation.

## Cross-project applicability

| Project/domain | Highest-value mathematical framing | Status of harmonic/spectral use |
|---|---|---|
| DGAF | formal logic, provenance graphs, statistics, authorization/state transitions, control | analogy unless a dynamical model is explicitly built |
| PDMAL | graph theory, network science, experimental design, stochastic robustness | spectral graph methods are literal graph methods; outcome claims remain empirical |
| ASIS | signal processing, estimation, control, time-frequency analysis | directly applicable |
| Orbit-Driftwatch | time series, changepoints, periodicity, anomaly detection | applicable only if periodic/spectral models beat suitable baselines |
| MeshSense | graph Laplacians, diffusion, spectral embedding, geometry | directly applicable to graph/mesh structure |
| Semantic Entropy Detector | information theory, probability, calibration | classical harmonics generally secondary |
| Collabration | identity, provenance, delegation, authorization, graph structure | mostly metaphorical unless interaction dynamics are explicitly modeled |
| AHG / Phi-Calculus | hypothesis generation and controlled comparison | mathematical motifs require non-special baselines before mechanism claims |
| Morse-Orchestration | scheduling, control, recurrence, operations research | frequency/timescale analysis can be tested prospectively |

## Out-of-scope dependency registry

These domains are relevant but not solved by the control-envelope work:

| Domain | Relevance | DGAF role in this program | Current research boundary |
|---|---|---|---|
| Normative legitimacy / value aggregation | determines what policies should represent | out of scope; consume explicit policies/requirements | unresolved general problem |
| Inner alignment / learned objectives | concerns model behavior beyond specified interface rules | out of scope for ledger guarantees | unresolved general problem |
| Mechanistic interpretability | may provide evidence about internal mechanisms | optional supporting evidence only | incomplete coverage |
| Deceptive/situational behavior detection | affects trust in planner/verifier behavior | adversarial evaluation input, not solved property | unresolved |
| Scalable oversight | matters when supervised systems exceed human capability | research interface only | unresolved |
| Corrigibility | concerns persistence of human correction authority under optimization/self-modification | bounded runtime controls may assist but do not establish general corrigibility | unresolved |

The table records boundaries, not external ownership claims.

## Literature and standards anchors

These sources provide methodology or external context. They are **not evidence that DGAF or PDMAL has achieved the corresponding outcomes**.

- Garg, A., Kim, E., Peng, K., & Garg, N. (2025), *Correlated Errors in Large Language Models*, arXiv:2506.07962 / ICML 2025. [arXiv:2506.07962](https://arxiv.org/abs/2506.07962)
- Wu, H., Li, Z., & Li, L. (2025), *Can LLM Agents Really Debate? A Controlled Study of Multi-Agent Debate in Logical Reasoning*, arXiv:2511.07784. [arXiv:2511.07784](https://arxiv.org/abs/2511.07784)
- Li, J. et al. (2026), *Discovering Efficient and Explainable Communication Topologies for LLM-based Multi-Agent Systems via Causal Inference*, arXiv:2608.12921. [arXiv:2608.12921](https://arxiv.org/abs/2608.12921)
- NIST, *Accelerating the Adoption of Software and AI Agent Identity and Authorization* (2026 concept paper). [NIST concept paper](https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd)
- NIST, *Building Evaluation Probes into Agentic AI*. [NIST project page](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai)
- W3C, *PROV Overview*. [W3C PROV](https://www.w3.org/TR/prov-overview/)
- in-toto, software supply-chain provenance/verification framework. [in-toto](https://in-toto.io/)
- SLSA v1.2 source provenance requirements. [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)

## Falsification discipline

This program should be considered useful only to the extent that it produces hypotheses that can lose.

Examples of disconfirming outcomes include:

- evidence-overlap measures add no predictive value beyond raw agent count;
- graph structural predictors fail to predict resilience out of sample;
- edge-ablation importance is unstable across seeds/tasks;
- spectral metrics do not improve prediction over simpler graph statistics;
- additional verifier diversity increases cost but not correction or calibration;
- a governance invariant documented at the application layer is bypassable at the tool gateway;
- a proposed action-admission rule does not prevent the targeted unauthorized/stale/replay failure under an exact runtime test;
- a simpler baseline produces equivalent control behavior at lower complexity.

Negative results must be retained as evidence rather than reframed as success.

## Epistemic state and claim-evidence model

The research program now treats epistemic state as a **typed, auditable object** rather than a scalar confidence score. This extension is prospective and non-authorizing; it does not amend the locked PDMAL primary analysis or alter any current governance/scientific predicate.

### Claim object

For each material claim `c`, record at minimum:

```text
ClaimRecord(c) = {
  claim_id,
  proposition,
  claim_class,
  scope,
  population_or_system,
  time_valid_from,
  time_valid_until_or_review_by,
  source_roots,
  derivation_steps,
  dependency_signature,
  supporting_evidence,
  contradicting_evidence,
  defeaters,
  uncertainty,
  calibration_status,
  verification_status,
  authorization_relevance,
  supersedes,
  superseded_by,
  retraction_state
}
```

A claim is not promoted merely because multiple agents repeat it, a source is prestigious, a model assigns high confidence, or a mathematical property is exact.

### Evidence graph and independence

Extend the provenance graph `H` with typed evidence relations:

```text
SUPPORTS
CONTRADICTS
DERIVED_FROM
REPLICATES
SHARES_SOURCE_ROOT
SHARES_MODEL_LINEAGE
SHARES_PROMPT_OR_POLICY
SHARES_TOOL_OUTPUT
DEFEATS
SUPERSEDES
RETRACTS
VALID_DURING
```

Evidence diversity must be estimated from dependency structure rather than raw evidence count. Unknown dependence remains `UNKNOWN_DEPENDENCE`; it must not be silently treated as independence.

A future effective-evidence quantity may be evaluated as a research metric, but no universal weighting formula is assumed in advance. Any proposed aggregation rule must be calibrated and compared against simpler baselines.

### Uncertainty decomposition

Do not collapse uncertainty into one confidence number. Track separable sources where observable:

```text
U(c) = {
  aleatoric,
  model_or_parameter,
  structural_or_model_form,
  data_coverage,
  provenance,
  dependency,
  measurement,
  temporal,
  adversarial,
  decision_or_consequence
}
```

`UNKNOWN` is categorical when the system lacks a justified estimate. A missing estimate is not zero uncertainty.

### Contradiction, defeasibility, and belief revision

For any material contradiction:

1. retain both claim/evidence paths;
2. classify whether the conflict is logical, empirical, temporal, definitional, scope-related, or source-identity related;
3. identify explicit defeaters rather than averaging incompatible claims;
4. recompute admissibility only through declared dependency edges;
5. record supersession or retraction without deleting historical provenance.

A later claim may supersede an earlier claim only for an explicitly declared scope and time interval. Historical truth must remain reconstructable.

### Temporal validity

Every externally contingent claim should declare either a validity interval or a review condition. Evidence that was valid at `t0` must not be assumed current at `t1` when the underlying system, model, policy, dataset, deployment, or source can change.

### Causal-claim discipline

Distinguish at least:

- association;
- predictive relationship;
- intervention effect;
- mechanism hypothesis;
- causal effect supported by an identified design.

Graph structure, correlation, salience, or feature importance alone does not establish causal effect. Edge-ablation work remains the prospective causal-intervention lane for communication-edge importance.

### Adversarial evidence handling

Future evaluation should include evidence attacks as first-class perturbations:

- source poisoning or fabricated citations;
- many-agent repetition of one false root;
- provenance aliasing;
- selective omission of counterevidence;
- stale evidence presented as current;
- judge/verifier correlation;
- confidence inflation without evidence gain;
- tool-output substitution or replay;
- contradictory high-prestige sources.

The system should be evaluated on whether it preserves uncertainty, detects dependence, surfaces contradictions, and fails closed when required evidence becomes inadmissible.

### Calibration and scoring rules

Where probabilistic confidence is used, evaluate it with proper scoring rules and calibration diagnostics rather than confidence accuracy alone. Candidate measures include Brier score, log score, calibration curves, and selective-risk/coverage behavior. Calibration must be measured on the same claim class and operating regime for which the probability is interpreted.

### Epistemic evaluation battery

A future separately authorized evaluation lane should measure:

| Property | Candidate test |
|---|---|
| provenance completeness | reconstruct every material claim to immutable source/derivation roots |
| dependency awareness | distinguish repeated evidence from genuinely independent paths |
| contradiction survival | preserve and surface incompatible evidence until resolved |
| defeater sensitivity | withdraw or downgrade claims when preregistered defeaters are introduced |
| temporal validity | reject or quarantine stale evidence after a validity boundary |
| calibration | proper scoring rules plus reliability/selective-risk analysis |
| robustness to source poisoning | controlled misleading-evidence intervention |
| update correctness | reproduce belief/state changes from an append-only event history |
| retraction integrity | retract present applicability without erasing historical provenance |
| causal discipline | prevent observational predictors from being promoted to causal claims |
| unknown-state fidelity | preserve `UNKNOWN` / `INSUFFICIENT_EVIDENCE` instead of forced scoring |
| cross-agent diversity | compare agent count against independent provenance-root count |

### Promotion and retraction protocol

A material claim should move between epistemic states only through explicit events:

```text
PROPOSED
 -> SUPPORTED
 -> VERIFIED
 -> EMPIRICALLY_SUPPORTED
```

with orthogonal transitions such as:

```text
CHALLENGED
DEFEATED
SUPERSEDED
RETRACTED
STALE
OUT_OF_SCOPE
```

These states are not an authorization ladder. Verification, empirical support, authorization, execution, and deployment remain separate dimensions.

### State-of-the-art target

The program's state-of-the-art epistemic target is therefore not maximal agent agreement. It is a system that can answer, for any consequential claim:

1. **What exactly is asserted, and for what scope/time?**
2. **What evidence supports and contradicts it?**
3. **How independent are those evidence paths?**
4. **What uncertainty remains, and what kind is it?**
5. **What would defeat, supersede, or retract the claim?**
6. **Can the complete update history be replayed?**
7. **Was any causal or authorization inference made beyond the evidence?**

This target is testable and falsifiable. Failure on these properties should remain visible evidence against the corresponding design hypothesis.

## Promotion rule

No construct in this program may be promoted to a DGAF/PDMAL scientific result solely because it is mathematically plausible, externally published, implemented, or documented. Promotion requires an exact-scope evidence chain appropriate to the claim class, as defined in `MATHEMATICAL_CLAIM_CLASSIFICATION_STANDARD.md`.
