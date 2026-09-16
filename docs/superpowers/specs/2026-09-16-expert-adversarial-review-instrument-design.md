# DGAF Expert Adversarial Review Instrument (EARI) Design

**Date:** 2026-09-16  
**Status:** APPROVED DESIGN / NOT IMPLEMENTED  
**Base protected `main`:** `6525e242d198959bbba25472aaf375de03113eaa`  
**Scientific-state effect:** NONE  
**Authorization effect:** NONE  
**High-Assurance effect:** NONE  
**Scientific-N effect:** 0

## 1. Purpose

EARI is a repo-native, human-reviewer-first adversarial assurance instrument for DGAF. It is designed to make important transitions reconstructably challengeable before DGAF proceeds.

The instrument institutionalizes skeptical review without making criticism itself authoritative. It separates discovery, evidence status, severity, gate relevance, adjudication, and DGAF authorization so that none of those concepts silently substitutes for another.

EARI is intended to answer:

> Given this exact frozen evidence package, which independently attempted falsifications survived review, what evidence supports or defeats them, what dissent remains, and does any qualifying defect prevent the existing DGAF authority machinery from considering the transition?

EARI does not prove correctness. It does not establish scientific truth. It does not authorize a DGAF transition.

## 2. Non-effects and activation boundary

This design document does not activate EARI, create review authority, add a new source of truth, change current Track A Epoch 002 state, establish real materialization, admit a materialization receipt, authorize primary analysis, execute analysis, establish efficacy, establish independent validation, increment scientific N, or alter High-Assurance state.

EARI has **zero operational gate effect until a separate implementation and explicit prospective governance activation are reviewed and accepted**. Future activation must name the exact EARI specification/policy identities and the transitions to which negative gate effect applies.

Activation is prospective. It must not retroactively invalidate or reinterpret repository transitions that occurred before the activation boundary unless a separate existing DGAF authority explicitly requires such retrospective treatment.

After valid activation, EARI may withhold clearance only at the five formal checkpoints defined here. It may never grant positive DGAF authority.

## 3. Core authority invariant

The hard asymmetry is:

```text
EARI = REVIEW_CLEAR
        ↓
existing DGAF gate MAY independently consider the transition
```

Never:

```text
EARI = REVIEW_CLEAR
        ↓
AUTHORIZED
```

EARI may discover, challenge, report, or block an in-scope checkpoint after activation. It may not authorize analysis, establish efficacy, establish independent validation, increment scientific N, establish freeze, establish production readiness, or create any other positive scientific or operational authority.

At formal checkpoints, EARI therefore has bounded **negative authority only** after prospective activation.

## 4. Architectural model

EARI uses four layers.

### 4.1 Review specification layer

Versioned machine-readable specifications define:

- the fixed reviewer panel and charters;
- participation modes;
- independence rules;
- the five formal checkpoints;
- defect classes and subclasses;
- the three-axis finding model;
- evidence profiles and evidence roles;
- finding lifecycle;
- blocking predicates;
- calibration requirements;
- dissent semantics;
- checkpoint outcome rules;
- record lifecycle and lineage-integrity rules.

Specification changes occur through normal repository review and do not rewrite prior review runs.

### 4.2 Immutable review evidence layer

Every review execution receives a unique review ID and an append-only review package. Earlier review records are never rewritten to represent later consensus, remediation, or supersession.

Conceptual structure:

```text
docs/reviews/
  schemas/
  charters/
  policy/
  runs/
    EARI-R2-2026-001/
      manifest.json
      packet/
      assignments.json
      independence/
      calibration/
      first_pass/
      findings/
      cross_examination/
      supplements/
      secondary_appraisals/
      dissents/
      adjudication.json
      outcome.json
      attestation.json
      package.sha256
  generated/
    current_index.json
    current_index.md
```

Exact implementation paths may be refined during implementation planning, but canonical immutable records and generated projections must remain distinct.

### 4.3 Derived current-state layer

A generated index summarizes the latest review state, finding dispositions, checkpoint history, supersession, and remediation.

The generated index is a projection only. It is never manually authoritative and can always be regenerated from canonical review packages.

Core invariant:

> Review history is append-only. Current review state is derived. No projection may supersede, mutate, or substitute for its source review records.

### 4.4 Validation and policy layer

Repository tooling validates structure and process mechanics, including:

- schema conformance;
- packet and package digests;
- version bindings;
- append-only history;
- role participation completeness;
- reviewer independence predicates where machine-checkable;
- calibration eligibility;
- defect-class/checkpoint eligibility;
- blocking-predicate completeness;
- dissent preservation;
- process-validity rules;
- lineage-fork rules;
- deterministic checkpoint-outcome consistency;
- generation of non-authoritative current-state projections.

Automation does **not** decide whether a scientific criticism is substantively correct. Humans own findings and adjudication. Automation decides whether the review process and recorded disposition conform to declared rules.

## 5. Human authority and AI boundary

The formal panel consists of human reviewers. AI is a subordinate instrument available to those reviewers.

AI may assist with:

- evidence retrieval;
- exact-identity comparison;
- contradiction detection;
- counterexample generation;
- statistical and methodological probes;
- provenance tracing;
- reproduction attempts;
- claim/evidence comparison;
- candidate-finding generation;
- review drafting.

AI output cannot directly become a canonical EARI finding.

Every AI-generated candidate used in a formal review must receive a human disposition:

```text
ADOPTED
REJECTED
DEFERRED
```

The human reviewer records the rationale and owns any adopted judgment.

Formal AI invocation records bind the best available instrument/model identity, instrument version, calibration version, review phase, input evidence identities, task/procedure or prompt digest, output digest, invocation time, human disposition, and human rationale.

Material changes to the AI instrument trigger targeted or full recalibration according to the material-change policy.

## 6. Fixed 11-role panel

The panel is permanently defined by role so review coverage remains comparable across runs.

| ID | Reviewer role | Primary falsification mandate | Natural independent secondary |
|---|---|---|---|
| R01 | Statistical Methodologist | Determine whether inference could be invalid despite correct execution: estimand, paired structure, uncertainty, resampling, multiplicity, power, effect interpretation, missingness, assumptions, sensitivity. | Experimental Design / ML Evaluation |
| R02 | Experimental Design Reviewer | Determine whether the experiment can distinguish claimed alternatives: preregistration fidelity, controls, nulls, baselines, randomization, blinding, failure schedules, exclusions, confounding, researcher degrees of freedom. | Statistics / Reproducibility |
| R03 | Systems & Distributed-Systems Reviewer | Determine whether implementation faithfully instantiates the claimed system/topology: interactions, concurrency, propagation, failure injection, isolation, model/implementation mismatch, boundary conditions. | Skeptical Engineering / Security |
| R04 | Reproducibility & Provenance Reviewer | Determine whether an outsider can reconstruct the exact evidence chain without trusting undocumented project knowledge. | Governance / Independent Replication |
| R05 | Governance & Assurance Reviewer | Find routes by which authority or claims could be reached without satisfying prerequisites: circular authority, stale-parent acceptance, scope widening, SSoT conflicts, fail-open paths, exception misuse. | Reproducibility / Security |
| R06 | Security & Adversarial Reviewer | Assume an intelligent actor, compromised dependency, malformed artifact, or trust-boundary failure attempts to defeat controls. | Systems / Governance |
| R07 | Skeptical Engineering Reviewer | Determine whether complexity itself obscures or destabilizes the project: overengineering, duplication, hidden state, fragile coupling, maintenance burden, simpler alternatives. | Systems / Reproducibility |
| R08 | Claims & Scientific Communication Reviewer | Attempt to prove that wording says more than evidence establishes: causal language, efficacy, uncertainty, limitations, negative findings, figures/tables, terminology burden. | Statistics / External Validity |
| R09 | Independent Replication Reviewer | Behave as though the internal team is unavailable and attempt reconstruction/falsification from the admitted package alone. | Reproducibility / Skeptical Engineering |
| R10 | ML & Agent-Evaluation Reviewer | Determine whether evaluation measures the behavior attributed to the agentic system: evaluator leakage, stochasticity, prompt/config sensitivity, baseline fairness, metric gaming, contamination, correlated failures. | Statistics / Systems |
| R11 | Research Ethics & External-Validity Reviewer | Challenge whether conclusions remain responsible and meaningful outside the narrow apparatus: population/environment scope, transfer, representativeness, foreseeable misuse, human impact, ecological validity. | Claims / Experimental Design |

The roles are fixed. Their participation intensity is checkpoint-specific.

## 7. Participation model

Every formal checkpoint involves all 11 roles, but not all roles perform a full-domain review.

```text
PRIMARY
SECONDARY
AWARENESS
RECUSED
```

### PRIMARY

Performs a full charter-scoped falsification review and may propose a blocking finding where the taxonomy permits.

### SECONDARY

Performs independent appraisal of designated high-consequence classes or candidate blockers. A valid independent secondary appraisal can confirm or reject blocking eligibility.

### AWARENESS

Reviews designated cross-domain evidence and submits a scoped attestation or concern. Awareness participation cannot itself establish a blocking finding. It may trigger reassignment into an eligible primary/secondary appraisal path.

### RECUSED

Cannot participate in adjudication for the affected finding/object.

This model preserves mandatory panel involvement while avoiding ritualized eleven-way duplication.

## 8. Reviewer independence

A different person or discipline is not automatically independent.

Each required appraisal has one of:

```text
INDEPENDENT
SEPARATE_BUT_NONINDEPENDENT
ADVISORY
RECUSED
```

Disqualifying or contaminating relationships include, at minimum:

- author/co-author of the affected artifact;
- implementer or direct owner of the decision under review;
- direct reporting/control relationship relevant to the object;
- prior owner of the disputed claim;
- prior participant in remediation, unless explicitly reassigned to non-independent advisory status;
- unresolved financial, reputational, organizational, authorship, or comparable conflict;
- exposure to the primary reviewer's finding before the secondary appraisal was sealed;
- reliance on the same undisclosed generated rationale or shared draft judgment.

Only `INDEPENDENT` appraisal satisfies a mandatory dual-appraisal requirement.

A materially false or incomplete independence declaration may create a review-process-integrity defect.

## 9. Reviewer output contract

Reviewers are not rewarded for manufacturing objections.

The required primary output is the strongest **plausible, evidence-supported disconfirmation hypothesis** within the assigned scope. A valid outcome may instead be:

```text
NO_SUPPORTED_REJECTION_CASE_IDENTIFIED
```

Every substantive objection records:

- asserted proposition;
- exact evidence bindings;
- assumptions;
- best counterevidence;
- defect class/subclass;
- protected property affected;
- severity;
- evidence status;
- gate relevance;
- remediation or falsification criterion;
- residual uncertainty;
- revisit trigger.

A `NO_FINDING` result is never a bare checkbox. It records at minimum:

```yaml
review_scope:
  charter_version: "..."
  evidence_items_examined: []
  tests_or_queries_performed: []
  defect_classes_assessed: []
  limitations: []
  conclusion: NO_FINDING_ESTABLISHED
  residual_uncertainty: []
```

`NO_FINDING_ESTABLISHED` is bounded negative evidence. It does not mean `NO_DEFECT_EXISTS`.

## 10. Three-axis finding model

Finding classification separates three dimensions.

### Severity

```text
CRITICAL
MAJOR
MODERATE
MINOR
```

Severity describes consequence if the finding is true. It does not establish evidentiary sufficiency or gate effect.

### Evidence status

```text
VERIFIED
SUPPORTED
PLAUSIBLE
NOT_VERIFIED
```

Evidence status describes what the record currently establishes. It does not imply importance.

### Gate effect

```text
BLOCKING
REMEDIATION_REQUIRED
ADVISORY
NO_EFFECT
```

Gate effect is rule-bound. A reviewer cannot create blocking authority merely by assigning a high severity.

## 11. Checkpoint outcome and orthogonal state axes

Checkpoint outcomes are:

```text
REVIEW_CLEAR
REVIEW_BLOCKED
REVIEW_INCONCLUSIVE
REVIEW_ADVISORY_ONLY
```

These remain separate from process and record state.

### Process validity

```text
VALID
INVALID
```

### Record lifecycle

```text
CURRENT
SUPERSEDED
REVOKED
ARCHIVED
```

### Lineage integrity

```text
LINEAR
FORKED
```

Limitations are structured records, not a disguised clearance state.

A process-invalid review cannot have operational clearance effect regardless of its recorded checkpoint outcome.

## 12. Evidence governance

### 12.1 Evidence roles

Evidence role describes decision consequence, not trustworthiness:

```text
DECISION_CRITICAL
SUPPORTING
CONTEXTUAL
```

### 12.2 Typed provenance profiles

Evidence types use different provenance profiles rather than one misleading flat schema.

**Web evidence** may record canonical URI, acquisition time, response metadata, preserved raw snapshot digest, extraction procedure identity/status, and extracted-text digest.

**Repository evidence** may record repository/remote identity, immutable commit, path, blob identity, and capture method.

**Dataset evidence** may record content digest, schema/version identity, transformation lineage, and custody history.

**Execution evidence** may record environment image or lock identity, code commit, invocation parameters, inputs, outputs, timestamps, executor identity, logs, and exit status.

**Human-review evidence** may record reviewer identity or controlled pseudonym, charter version, packet identity, timestamp, sealed first-pass result, and conflict declaration.

A content hash proves continuity of captured bytes from capture onward. It does not establish that the bytes were truthful, complete, correctly interpreted, or acquired from the legitimate upstream source. Those remain separate evidence/provenance questions.

## 13. Immutable review packages and trust anchors

Every accepted formal review package records at minimum:

```yaml
review_package_digest:
parent_review_package_digest:
checkpoint_lineage_id:
admitted_repository_commit:
admission_authority_id:
signature_or_verifiable_attestation:
signed_at:
supersedes_package_digest:
revocation_status:
lineage_state:
```

Git history is part of the trust model but is not treated as sufficient by itself to prove package authority or completeness.

A review-lineage fork prevents formal clearance until an authorized reconciliation or supersession record establishes the accepted lineage.

## 14. Calibration and qualification

Human and AI calibration are assurance evidence only. They do not increment scientific N, establish efficacy, validate Epoch 002, or establish independent replication.

There is no single universal reviewer score.

Qualification is capability-specific:

```text
reviewer × role × defect class × permitted review action
```

Calibration records may include:

- per-class recall;
- per-class precision where meaningful;
- unsupported-block false-positive rate;
- evidence-binding precision;
- ambiguity handling;
- insufficient-evidence handling;
- rationale requirements;
- safety/validity-critical seeded defect recall;
- test-set version;
- protected holdout identity;
- item retirement policy.

Agreement statistics may be used diagnostically when multiple reviewers truly judge the same standardized items under the same rubric. They are not a universal quality gate and must not replace investigation of why judgments differ.

### 14.1 Qualification levels

A reviewer may be separately qualified for:

```text
ordinary finding detection
propose blocking
independent secondary appraisal
adjudication
```

### 14.2 Calibration-corpus controls

Calibration sets include clean cases, known defects, ambiguity cases, and insufficient-evidence cases. Protected holdouts and scenario rotation prevent the exercise from degrading into memorization.

## 15. Material-change and recalibration policy

Material changes are classified as:

```text
COSMETIC
PROCEDURE_AFFECTING
DECISION_AFFECTING
SCOPE_AFFECTING
SECURITY_OR_CUSTODY_AFFECTING
```

Typical effects:

- `COSMETIC`: record only; no invalidation;
- `PROCEDURE_AFFECTING`: targeted recalibration of affected capability;
- `DECISION_AFFECTING`: full recalibration for affected capability;
- `SCOPE_AFFECTING`: new calibration coverage required before use;
- `SECURITY_OR_CUSTODY_AFFECTING`: revalidate affected provenance/security controls and review procedure.

The same model applies to reviewer instructions, taxonomies, schemas, AI instruments, retrieval procedures, evidence pipelines, and review tools.

## 16. Review phases

Formal checkpoint review uses three epistemic phases plus deterministic packaging.

```text
BLIND FIRST PASS
        ↓
CROSS-EXAMINATION
        ↓
CONSENSUS ADJUDICATION
```

### 16.1 Blind first pass

Reviewers receive the same frozen packet, their charter, assigned defect classes, calibration status, and review scope.

They do not receive other reviewers' findings, provisional conclusions, aggregate severity counts, emerging consensus, or chair recommendations.

First-pass submissions are sealed and immutable. Later position changes are append-only `POSITION_REVISION` records referencing the original judgment.

### 16.2 Cross-examination

After all required first passes are sealed, findings become visible.

Structured cross-examination actions include:

```text
SUPPORT
CHALLENGE
COUNTEREVIDENCE
REQUEST_EVIDENCE
REQUEST_REPRODUCTION
SCOPE_CHALLENGE
SEVERITY_CHALLENGE
GATE_EFFECT_CHALLENGE
DUPLICATE_LINK
INDEPENDENCE_CHALLENGE
```

Each action binds a specific finding/object and evidence.

### 16.3 Finding deduplication

Multiple independent observations of the same underlying defect are preserved as linked observations under one canonical defect object. Deduplication does not erase independent detection paths.

### 16.4 Consensus adjudication

Consensus means no reviewer with adjudicative standing maintains an unresolved evidence-supported objection to the disposition. It does not require agreement on every preference or interpretation.

## 17. Formal dissent

Dissent is a first-class immutable object.

A dissent records:

- finding/object identity;
- agreed facts;
- disputed propositions;
- evidence on each side;
- competing rationale;
- consequence if the dissenter is correct;
- falsification/resolution path;
- escalation history;
- current status.

An unresolved evidence-backed blocking dissent cannot be administratively converted into `REVIEW_CLEAR`.

Not every disagreement is blocking. Taxonomy/policy must distinguish a blocking defect from an unresolved concern lacking sufficient evidence, a risk-tolerance disagreement, a compatible interpretive disagreement, or an issue outside the checkpoint decision boundary.

## 18. Five formal checkpoints

Outside these checkpoints the same instrument is advisory only.

### R1 — PRE_MATERIALIZATION

Primary question:

> Can the real operator-controlled materialization event occur without contaminating provenance, custody, blinding, or authority scope?

Minimum packet profile includes current protected repository state, accepted dataset-lock evidence, bounded-unblinding authority, materialization procedure/tool identities, operator handoff procedure, expected custody boundary, output schema, secret/non-disclosure constraints, and relevant prior review findings.

EARI may not perform materialization.

### R2 — PRE_PRIMARY_ANALYSIS_AUTHORIZATION

Primary question:

> Is the frozen evidence chain methodologically and procedurally ready for DGAF's separate authorization mechanism to consider allowing primary analysis?

Minimum packet profile includes accepted materialization receipt/provenance, frozen preregistration, frozen analysis implementation/configuration, dependency lock/environment, result schema, baseline/control definitions, prior R1 lineage, and authorization-policy identities.

### R3 — PRE_RESULT_ADMISSION

Primary question:

> Is this exact artifact admissible as the prospectively authorized locked primary-analysis result?

Minimum packet profile includes accepted analysis authorization, exact executed commit/config/environment, invocation, logs, result artifact/digest, execution receipt, expected-vs-observed execution comparison, and R2 review lineage.

### R4 — PRE_EXTERNAL_SCIENTIFIC_CLAIM

Primary question:

> Do the proposed scientific claims say no more than the admitted evidence establishes?

Minimum packet profile adds admitted result, statistical interpretation, null/baseline results, effect estimates and uncertainty, sensitivity results, limitations, proposed claims, figures/tables, competing explanations, and negative findings.

### R5 — PRE_PUBLICATION_RELEASE

Primary question:

> Can an informed outsider reconstruct, inspect, challenge, and correctly contextualize what DGAF releases?

Minimum packet profile adds proposed public package, reproduction instructions, released data/code scope, provenance manifest, security/redaction review, claim wording, external-validity statement, ethics/limitations statement, and relevant review lineage.

## 19. Defect taxonomy

EARI uses 13 top-level defect families.

| ID | Defect family | Primary owner | Independent secondary | Blocking checkpoints |
|---|---|---|---|---|
| D01 | PROVENANCE_INTEGRITY_BREAK | Reproducibility & Provenance | Governance & Assurance | R1–R5 |
| D02 | CUSTODY_OR_BLINDING_COMPROMISE | Reproducibility & Provenance | Security & Adversarial | R1–R3 |
| D03 | PROTOCOL_OR_PREREGISTRATION_DEVIATION | Experimental Design | Statistical Methodologist | R1–R4 |
| D04 | REPRODUCIBILITY_OR_RECONSTRUCTION_FAILURE | Independent Replication | Reproducibility & Provenance | R2–R5 |
| D05 | INVALID_INFERENCE_OR_STATISTICAL_DESIGN | Statistical Methodologist | Experimental Design | R2–R4 |
| D06 | BASELINE_CONTROL_OR_COMPARATOR_INVALIDITY | Experimental Design | ML & Agent Evaluation | R2–R4 |
| D07 | IMPLEMENTATION_MODEL_MISMATCH | Systems & Distributed Systems | Skeptical Engineering | R1–R4 |
| D08 | AUTHORIZATION_OR_GOVERNANCE_BYPASS | Governance & Assurance | Reproducibility & Provenance | R1–R5 |
| D09 | SECURITY_OR_TRUST_BOUNDARY_COMPROMISE | Security & Adversarial | Systems & Distributed Systems | R1–R5 |
| D10 | EVALUATION_CONTAMINATION_OR_METRIC_INVALIDITY | ML & Agent Evaluation | Statistical Methodologist | R2–R4 |
| D11 | CLAIM_EVIDENCE_OVERREACH | Claims & Scientific Communication | Statistical Methodologist | R3–R5 |
| D12 | EXTERNAL_VALIDITY_OR_SCOPE_MISREPRESENTATION | Research Ethics & External Validity | Claims & Scientific Communication | R4–R5 |
| D13 | REVIEW_PROCESS_INTEGRITY_FAILURE | Governance & Assurance | Independent Replication | R1–R5 |

`D13` means the review process itself cannot support a trustworthy operational outcome; it does not automatically establish that the underlying DGAF science or system is defective.

Evidence insufficiency, disagreement, dissent, unknown state, out-of-scope status, accepted risk, and `NO_FINDING_ESTABLISHED` are not defect classes. They are separate states/dispositions.

## 20. Finding lifecycle

```text
OBSERVATION
    ↓
CANDIDATE_FINDING
    ├── REFUTED
    ├── DUPLICATE
    ├── OUT_OF_SCOPE
    ├── INSUFFICIENT_EVIDENCE
    ├── SUPERSEDED
    ├── SUBSTANTIATED_NONBLOCKING
    └── PROPOSED_BLOCKING
            ↓
       independent secondary appraisal
            ↓
       CONFIRMED_BLOCKING
```

`PROPOSED_BLOCKING` prevents formal clearance while mandatory appraisal is unresolved, but it is not equivalent to a confirmed blocker.

A confirmed blocker may leave that state only through an explicit append-only disposition such as:

```text
REMEDIATED
REFUTED_BY_NEW_EVIDENCE
INVALIDATED_BY_SCOPE_CORRECTION
SUPERSEDED_BY_VALID_REVIEW
```

It may not be cleared by majority override, chair override, schedule pressure, or delivery exception.

## 21. Blocking predicate

Blocking is conjunctive rather than intuitive:

```text
BLOCKING(f) = C(f) AND E(f) AND I(f) AND S(f) AND G(f) AND D(f)
```

Where:

- `C(f)` — the defect class/subclass is blocking-eligible at the checkpoint;
- `E(f)` — admissible, sufficiently bound evidence supports the proposition;
- `I(f)` — material impact on a checkpoint-required protected property is established;
- `S(f)` — severity meets the checkpoint's predefined threshold;
- `G(f)` — the defect is not prospectively permitted by an applicable declared residual-risk policy;
- `D(f)` — required valid independent secondary appraisal is complete.

### 21.1 Evidence threshold

A `CONFIRMED_BLOCKING` finding requires evidence status at least:

```text
SUPPORTED or VERIFIED
```

A merely `PLAUSIBLE` concern may require investigation or produce inconclusive review, but cannot itself become confirmed blocking.

### 21.2 Protected properties

Findings bind an affected protected property such as:

```text
BLINDING_INTEGRITY
DATASET_IDENTITY
PREREGISTRATION_FIDELITY
ANALYSIS_REPRODUCIBILITY
INFERENTIAL_VALIDITY
AUTHORIZATION_CHAIN
CLAIM_ACCURACY
EXTERNAL_SCOPE
REVIEW_INDEPENDENCE
```

A true defect that does not affect a property required by the checkpoint is nonblocking for that checkpoint.

### 21.3 Severity eligibility

```text
CRITICAL → blocking-capable
MAJOR    → blocking-capable only where gate policy explicitly permits
MODERATE → never CONFIRMED_BLOCKING
MINOR    → never CONFIRMED_BLOCKING
```

### 21.4 Residual-risk policy

Accepted residual risk must be prospective and version-bound. It records applicable subclass, checkpoint, maximum severity, rationale, approval authority, and effective date.

A new exception may not be invented retroactively solely to remove an already discovered blocker.

## 22. Atomic finding record

The canonical machine-readable finding should include approximately:

```yaml
finding_id:
review_id:
checkpoint_id:
review_package_digest:
defect_class:
defect_subclass:
claim_or_control_affected:
protected_property:
scope_of_impact:
asserted_proposition:
assumptions: []
evidence_bindings: []
evidence_status:
provenance_status:
reproducibility_status:
severity:
plausibility:
primary_reviewer:
primary_review_mode:
secondary_appraiser:
secondary_independence_status:
gate_eligibility:
gate_effect:
best_counterevidence: []
remediation_or_falsification_criterion:
current_disposition:
disposition_history: []
dissent_links: []
created_at:
supersedes:
superseded_by:
```

Every substantive finding must include an explicit condition that would falsify, remediate, or materially narrow the objection.

## 23. Frozen packet and append-only supplements

A formal checkpoint reviews a frozen, identity-bound evidence packet.

The manifest binds exact specification, schema, charter, taxonomy, gate-policy, calibration-policy, repository, protected-branch, evidence-manifest, packet-digest, review-scope, protected-property, claim/transition, and exclusion identities.

Once `PACKET_FROZEN`, packet bytes do not change.

New evidence is admitted only as append-only supplements. Every supplement has independent provenance/digest, admission reason, requesting reviewer, acquisition method, and visibility time. All affected reviewers receive the same admitted supplement.

If a supplement materially changes the decision surface, affected first-pass work must be reopened through a recorded bounded process rather than silently updated.

## 24. Formal review state machine

Every formal checkpoint follows:

```text
REVIEW_CREATED
    ↓
PACKET_ASSEMBLED
    ↓
PACKET_FROZEN
    ↓
REVIEWERS_ASSIGNED
    ↓
INDEPENDENCE_VALIDATED
    ↓
FIRST_PASS_OPEN
    ↓
FIRST_PASS_SEALED
    ↓
CROSS_EXAMINATION_OPEN
    ↓
CROSS_EXAMINATION_SEALED
    ↓
ADJUDICATION_OPEN
    ↓
ADJUDICATION_SEALED
    ↓
OUTCOME_COMPUTED
    ↓
PACKAGE_ATTESTED
    ↓
REPOSITORY_ADMITTED
```

A prohibited phase skip or contaminated first-pass process may set `process_validity = INVALID`.

An invalid run is not rewritten. A later valid package may supersede it.

## 25. Secondary appraisal

Every `PROPOSED_BLOCKING` finding receives an independently sealed secondary appraisal that separately reconstructs the blocking predicate.

The appraiser records at least:

```yaml
finding_supported:
evidence_sufficient:
impact_supported:
severity_supported:
checkpoint_relevant:
blocking_policy_satisfied:
counterevidence_considered:
independence_status:
recommended_disposition:
```

The required output is not a bare `AGREE`/`DISAGREE` vote.

## 26. Deterministic checkpoint outcomes

Humans establish finding facts and dispositions. The policy engine computes which checkpoint outcome is permissible.

### REVIEW_BLOCKED

Required when at least one unresolved `CONFIRMED_BLOCKING` finding exists and `process_validity = VALID`.

### REVIEW_INCONCLUSIVE

Required when no confirmed blocker has been established but clearance cannot be justified, including unresolved proposed blocking, unresolved blocking-capable dissent, unavailable required decision-critical evidence, incomplete required reproduction, unavailable qualified independent appraisal, or unresolved ambiguity affecting a hard prerequisite.

### REVIEW_CLEAR

Allowed only when all of the following are true:

```text
process_validity = VALID
lineage_integrity = LINEAR
all mandatory participation is complete
all required appraisals are complete
zero unresolved CONFIRMED_BLOCKING findings
zero unresolved blocking-capable dissent
no hard evidence prerequisite is missing
consensus clearance is established
```

Meaning of `REVIEW_CLEAR`:

> EARI found no remaining review condition that prevents the existing DGAF authority machinery from independently considering the transition.

It does not mean `AUTHORIZED`.

### REVIEW_ADVISORY_ONLY

Used outside R1–R5. Findings may inform future work but have no formal gate effect.

## 27. Capacity, latency, and anti-bypass policy

An assurance system that cannot finish under plausible operating conditions will eventually be bypassed. EARI therefore uses explicit operating budgets.

Initial default targets:

| Stage | Default budget |
|---|---:|
| Packet completeness check | 1 working day |
| Blind first pass | 3 working days |
| Secondary appraisal | 2 working days |
| Cross-examination | 2 working days |
| Adjudication | 2 working days |
| Normal formal checkpoint | target ≤ 10 working days |

These are defaults, not scientific constants. A deployment may configure them prospectively.

Review effort ceilings are declared by role. If the evidence/time budget is insufficient for defensible clearance, the correct result is `REVIEW_INCONCLUSIVE`, not superficial approval.

Permitted pause reasons are enumerated, such as required external evidence unavailable, material supplement requested, bounded reproduction, reviewer recusal/replacement, security incident, or upstream canonical artifact change.

A project deadline alone is not a valid pause or clearance reason.

## 28. Emergency safety actions

No emergency exception may turn a confirmed scientific-validity blocker into `REVIEW_CLEAR`.

Operational emergency authority may take harm-reducing actions such as revoking credentials, disabling a release, quarantining corrupted evidence, or halting execution.

Emergency authority may not use urgency to authorize scientific analysis, result admission, efficacy claims, or publication clearance.

## 29. Review-system quality metrics

After sufficient review history exists, EARI may derive assurance-system metrics such as:

- independent multi-role defect detection;
- findings overturned during secondary appraisal;
- unsupported blocking proposals;
- late defects missed at earlier checkpoints;
- reviewer-specific defect-class detection;
- scoped `NO_FINDING_ESTABLISHED` frequency;
- dissent-resolution patterns;
- AI candidate adoption/rejection;
- recurring correlated blind spots.

These metrics evaluate EARI, not DGAF's scientific hypothesis. They never increment scientific N or establish efficacy.

## 30. Implementation direction

The approved architecture is **repo-native** rather than a separate review service.

The smallest implementation should create machine-readable semantics before UI or dashboard work.

Expected first implementation artifacts:

```text
docs/reviews/policy/defect_taxonomy.yaml
docs/reviews/schemas/finding.schema.json
docs/reviews/policy/gate_policy.yaml
docs/reviews/policy/calibration_policy.yaml
docs/reviews/charters/...
scripts/validate_eari_review.py
scripts/generate_eari_current_index.py
tests/test_eari_*.py
.github/workflows/eari-validation.yml
```

Exact file decomposition belongs in the implementation plan. No standalone database or separate authority service is required for the first implementation.

Any future UI is a projection over repository-authoritative records, not a parallel source of truth.

## 31. Required adversarial implementation fixtures

The implementation plan must include deterministic fixtures/tests for at least:

1. a genuine blocker;
2. an unsupported alarming claim;
3. a credible interpretive disagreement;
4. an evidence-custody failure;
5. a reviewer-independence failure;
6. an AI candidate rejected by the responsible human;
7. a forked review lineage;
8. an invalid review process that otherwise appears clear;
9. a scoped `NO_FINDING_ESTABLISHED` record;
10. a confirmed blocker later remediated and re-reviewed;
11. a true but checkpoint-irrelevant defect that remains nonblocking;
12. a merely `PLAUSIBLE` high-severity concern that cannot become confirmed blocking;
13. attempted retroactive residual-risk exception;
14. attempted administrative/chair override of a confirmed blocker;
15. attempted direct conversion of `REVIEW_CLEAR` into DGAF authorization.

## 32. Implementation acceptance constraints

Implementation is acceptable only if it preserves all of these invariants:

1. Human reviewers own canonical findings.
2. AI cannot create a canonical finding directly.
3. Blind first-pass records are preserved after later revisions.
4. `NO_FINDING_ESTABLISHED` is always scoped and evidence-bearing.
5. Independence is an operational predicate, not a role label.
6. Blocking is conjunctive and machine-checkable.
7. `PLAUSIBLE` evidence cannot become `CONFIRMED_BLOCKING` by severity alone.
8. A confirmed blocker cannot be removed by majority/chair/schedule override.
9. Dissent is append-only and reconstructable.
10. Review packages are immutable and lineage-aware.
11. Generated current-state indexes are projections only.
12. Process validity, checkpoint outcome, record lifecycle, and lineage integrity remain separate axes.
13. EARI clearance cannot establish positive DGAF authority.
14. EARI has no gate effect before explicit prospective activation.
15. Calibration and EARI operational metrics have zero scientific-N effect.
16. Current Track A Epoch 002 scientific and authorization state remains unchanged by implementation unless a separate legitimate DGAF transition explicitly changes it.

## 33. Design references and influences

The architecture was strengthened using established patterns from independent evidence appraisal, audit/data-integrity practice, formal dissent, safety-critical decision-making, and AI test/evaluation practice. These are design influences, not claims that DGAF or EARI is regulated by or equivalent to those frameworks.

Relevant sources discussed during design include:

- Cochrane Handbook guidance on independent duplicate appraisal, piloting, disagreement resolution, and preserving original judgments;
- NASA formal-dissent process concepts for documented facts, differing positions, rationales, impacts, escalation, and recorded decisions;
- FDA data-integrity / ALCOA+ concepts for attributable, original, complete, consistent, enduring, and available records;
- NIST AI RMF concepts for documented test/evaluation/verification/validation, human oversight, benchmarks, knowledge limits, and independent assessment.

## 34. Final invariant

> EARI is an append-only, evidence-bound, human-reviewer-first adversarial assurance instrument in which independent falsification precedes discussion, blocking requires predefined evidence and valid independent appraisal, dissent cannot be administratively erased, AI remains a calibrated subordinate instrument, and review clearance never constitutes scientific or operational authorization.

## 35. Design-to-plan gate

This document is the approved architecture, not an implementation plan.

Before implementation planning begins, the committed specification must receive a final human review for wording, scope, contradictions, and unintended authority. Only after that review is accepted should a detailed implementation plan be created and TDD implementation begin.
