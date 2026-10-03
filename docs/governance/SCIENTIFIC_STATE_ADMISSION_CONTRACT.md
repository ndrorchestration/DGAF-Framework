# Canonical Scientific-State Admission Contract

Status: **PROSPECTIVE CROSS-LANE GOVERNANCE CONTRACT / NO SCIENTIFIC-STATE EFFECT**

Controller: issue #1259

Current authority for project state remains `docs/CURRENT_STATE.md`. Existing lane-specific protocols, evidence validators, admission records, and adjudication rules remain authoritative for their exact scopes.

This contract does not replace those mechanisms. It defines the additional boundary that must be crossed before any evidence from any lane may change canonical scientific state.

## Purpose

DGAF already fails closed against scientific-state promotion in many individual components. Same-system runs, synthetic assurance, discovery tooling, AOSS apparatus, public demos, usability trials, and other non-promoting surfaces repeatedly fix `scientific_n_increment=0` or `scientific_state_effect=NONE`.

The remaining cross-lane risk is **promotion by implication**: treating a successful run, an outside participant, a reviewer, a repeated replay, a row count, or a verification result as if it automatically changes canonical scientific state.

This contract prohibits that inference.

## State dimensions are separate

The following dimensions MUST remain independently represented:

1. **Lane statistical units** — units used by a particular frozen experiment for its own analysis.
2. **Canonical scientific N** — the project-level governed scientific-N state reported by `docs/CURRENT_STATE.md`.
3. **Empirical outcome generation** — whether an authorized protocol actually generated empirical outcomes.
4. **Evidence independence** — whether evidence satisfies the exact independence definition required by its governing protocol.
5. **Independent validation** — whether a separately governed claim has been independently validated at its declared scope.
6. **Usability / receiver evidence** — evidence about whether an outside user can understand or use a surface.
7. **Engineering assurance** — CI, replay, simulation, mutation testing, self-tests, architecture checks, and related technical evidence.
8. **Canonical DGAF efficacy** — the project-level efficacy state.
9. **Runtime / High-Assurance authorization** — authority to perform consequential execution under the applicable runtime policy.

A change in one dimension MUST NOT silently change another.

In particular:

```text
lane sample size != canonical scientific N
reviewer count != canonical scientific N
operator count != canonical scientific N
agent count != canonical scientific N
replay count != canonical scientific N
workflow count != canonical scientific N
observation-row count != canonical scientific N
```

## Sole promotion mechanism

No evidence object, workflow result, issue comment, CI run, interpretation note, receipt, review, or public-facing status may directly promote canonical scientific state.

A promotion requires a separately admitted **Scientific State Transition Record (Scientific State Transition Record)**.

Absence of a valid Scientific State Transition Record means:

```text
SCIENTIFIC_STATE_EFFECT=NONE
```

for the candidate evidence under consideration.

## Scientific State Transition Record

An Scientific State Transition Record MUST bind at least:

```yaml
transition_id: <stable id>
controller_issue: <governed controller>
created_at: <timestamp>

prior_state:
  current_state_ref: <exact authority ref>
  current_state_digest: <digest or immutable revision>
  canonical_scientific_n: <integer>
  independent_validation: <state>
  canonical_dgaf_efficacy: <state>
  high_assurance: <state>

candidate_transition:
  transition_class: <class>
  proposed_scientific_n_delta: <integer>
  proposed_independent_validation_effect: <explicit effect>
  proposed_efficacy_effect: <explicit effect>
  proposed_authorization_effect: <explicit effect>
  exact_claim_scope: <bounded scope>

protocol:
  protocol_id: <id>
  protocol_revision: <immutable identity>
  preregistration_or_freeze_ref: <ref>
  countable_unit_definition: <definition or NOT_APPLICABLE>
  protocol_explicitly_allows_requested_transition: <boolean>

evidence:
  raw_evidence_refs: []
  exact_source_identities: []
  environment_identities: []
  custody_refs: []
  outcome_generation_established: <boolean>
  duplicate_or_replay_of: <ref or null>
  validity_state: <VALID | INVALID | INCONCLUSIVE>
  blocking_defeaters: []

independence:
  independence_required_for_transition: <boolean>
  attribution_verified: <boolean>
  relationship_disclosure_ref: <ref or null>
  independence_adjudication_ref: <ref or null>
  independence_state: <ESTABLISHED | NOT_ESTABLISHED | NOT_APPLICABLE | INCONCLUSIVE>

adjudication:
  adjudicator_authority_ref: <ref>
  decision: <ADMIT | REJECT | INCONCLUSIVE>
  rationale: <text>
  adjudicated_at: <timestamp>

result:
  resulting_scientific_n: <integer>
  resulting_independent_validation: <state>
  resulting_canonical_dgaf_efficacy: <state>
  resulting_high_assurance: <state>
```

The exact machine schema may be introduced separately. This document defines the semantic contract.

## Transition classes

### 1. Engineering assurance

Examples:

- CI;
- unit/integration tests;
- synthetic replay;
- simulation;
- mutation testing;
- architecture scans;
- same-owner agent review;
- operator self-tests performed by the implementation side;
- local reproducibility checks.

Default effects:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION_EFFECT=NONE
CANONICAL_EFFICACY_EFFECT=NONE
AUTHORIZATION_EFFECT=NONE
```

Engineering assurance may detect defects, strengthen confidence in implementation behavior, or satisfy a prerequisite. It does not become scientific N.

### 2. Same-system or same-owner empirical evidence

A lane may generate real outcomes and have its own frozen statistical units while still being non-independent at the project level.

Examples include evidence explicitly classified `SAME_SYSTEM_NONINDEPENDENT`.

Default canonical effects:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION_EFFECT=NONE
CANONICAL_EFFICACY_EFFECT=NONE
```

The experiment's own sample size remains a valid lane-local fact. It must not be relabeled as canonical scientific N.

### 3. Outside-operator usability evidence

Current Governed Repo issue #1210 is in this class.

A successful run may establish only the usability claim permitted by its frozen controller and packet.

For the current #1210 protocol:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_SCIENTIFIC_VALIDATION_EFFECT=NONE
CANONICAL_EFFICACY_EFFECT=NONE
HIGH_ASSURANCE_EFFECT=NONE
```

Externality of the operator does not convert a usability observation into a scientific replicate.

### 4. Unfamiliar-user HCI / receiver evidence

Current Tektite issue #1224 is in this class.

For the current #1224 protocol:

```text
SCIENTIFIC_N_INCREMENT=0
DGAF_INDEPENDENT_VALIDATION_EFFECT=NONE
CANONICAL_EFFICACY_EFFECT=NONE
HIGH_ASSURANCE_EFFECT=NONE
```

A participant may provide bounded usability/transfer evidence without becoming a scientific replicate.

### 5. Independent review of existing evidence

An independent reviewer may establish a bounded review or validation predicate for the exact claim and evidence package governed by the review protocol.

Review of existing evidence does not, by reviewer count alone, create a new empirical outcome or scientific unit.

Default:

```text
SCIENTIFIC_N_INCREMENT=0
```

An independent-validation state may change only if the exact governing protocol defines that predicate, independence is established, returned evidence is retained/reverified as required, and an explicit Scientific State Transition Record admits that state effect.

### 6. Independent empirical replication

This is the only general class that may be **eligible** for positive canonical scientific-N admission.

Eligibility is not admission.

A positive delta requires all of the following:

- the frozen protocol explicitly defines the countable empirical unit;
- the run is authorized for empirical outcome generation;
- the exact source, protocol, environment, and material identities satisfy the lane's rules;
- raw evidence is retained with required custody/provenance;
- the candidate unit is not a duplicate, replay, reanalysis, or correlated copy of an already counted unit;
- all protocol validity checks pass;
- required independence is explicitly adjudicated, not inferred from branding, account count, model count, or physical location;
- no blocking defeater is active;
- the lane-specific result/admission process accepts the empirical unit;
- a separate Scientific State Transition Record explicitly admits the proposed canonical-N delta.

Even then, efficacy and High-Assurance remain separate effects.

## Positive-N admission rule

For a candidate positive delta `d > 0`:

```text
ALLOW_N_INCREMENT(d) only if

protocol_explicitly_allows_requested_transition
AND countable_unit_definition_is_exact
AND empirical_outcome_generation_established
AND exact_identity_binding_passes
AND raw_evidence_retained
AND custody_and_provenance_pass
AND duplicate_check_passes
AND protocol_validity == VALID
AND required_independence == ESTABLISHED
AND no_blocking_defeater
AND lane_specific_admission == ACCEPTED
AND Scientific State Transition Record_adjudication == ADMIT
```

If any required predicate is false, missing, stale, or inconclusive:

```text
SCIENTIFIC_N_INCREMENT=0
```

for that candidate transition.

## Explicit non-counting rules

Canonical scientific N MUST NOT increase because:

- another model or agent independently produced a similar answer;
- the same evidence was replayed multiple times;
- the same raw outcomes were analyzed by additional tools;
- multiple reviewers inspected one existing result;
- an outside operator completed a usability task;
- multiple user accounts or credentials were used by the same owner;
- CI passed on multiple operating systems or Python versions;
- more observation rows exist inside a statistical unit;
- a dataset was materialized, locked, unblinded, analyzed, interpreted, or published;
- a result was merged to protected `main`;
- an evidence packet was cryptographically reverified;
- a system passed a security, architecture, HCI, or governance review;
- a prior result was reformatted or re-admitted without creation of a new countable unit.

These events may be valuable evidence. Their default canonical-N effect is zero.

## Independence rules

Independence is a property of the governed evidence relationship, not a property of a product name, model provider, account, or person merely being external to the repository.

Where independence is required, the governing protocol SHOULD evaluate relevant relationships such as:

- implementation authorship;
- protocol authorship;
- prior access to expected answers or hidden context;
- coaching;
- shared custody or same-owner control;
- shared outcome generation;
- shared adjudication authority;
- commercial or contractual conflicts where material;
- common failure modes or correlated verifier dependencies.

Multiple nominally different agents under the same owner/context do not establish independence by count.

## Independent validation is not N

An independent validation event and a scientific-N increment are separate transitions.

It is valid for an Scientific State Transition Record to admit:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=<bounded established predicate>
```

when a protocol independently validates an existing claim without creating a new empirical unit.

It is also possible for an empirical unit to be generated while canonical independent validation remains not established.

Neither state is inferred from the other.

## Efficacy is not N

A positive scientific-N delta does not establish canonical DGAF efficacy.

Canonical efficacy requires its own declared estimand/success criterion, valid evidence aggregation, applicable analysis/adjudication, and explicit efficacy-state transition.

Therefore:

```text
N > 0 -/-> CANONICAL_DGAF_EFFICACY=ESTABLISHED
```

## Authorization is not N or efficacy

Scientific evidence does not silently grant runtime authority.

```text
SCIENTIFIC_N_INCREMENT > 0 -/-> HIGH_ASSURANCE=AUTHORIZED
INDEPENDENT_VALIDATION=ESTABLISHED -/-> HIGH_ASSURANCE=AUTHORIZED
CANONICAL_DGAF_EFFICACY=ESTABLISHED -/-> HIGH_ASSURANCE=AUTHORIZED
```

Runtime authorization remains separately governed.

## Duplicate and correlation rule

No evidence item may be counted twice merely because it has multiple wrappers, receipts, reviewers, analyses, replays, storage locations, or presentation surfaces.

If two candidate units share the same underlying outcome-generating event, the default is that they are one candidate unit unless the frozen protocol establishes otherwise.

When correlation or shared provenance creates material uncertainty about independence, the candidate transition is `INCONCLUSIVE` or non-independent rather than optimistically counted.

## Invalidation and retraction

Scientific history must be append-only in meaning.

A later defect may invalidate the current admissibility of a prior unit or claim, but the system MUST NOT silently rewrite the historical event as if it never occurred.

Invalidation requires an explicit governed record that identifies:

- the affected transition/unit;
- the defect or defeater;
- scope of invalidation;
- resulting current-state effect;
- whether reanalysis/retest is possible;
- whether any downstream claim must be re-adjudicated.

A decrease, exclusion, or replacement in any current count must be represented as an explicit transition under the applicable protocol rather than editing old evidence in place.

## Current named gates

### Governed Repo #1210

Current permitted claim ceiling: bounded outside-operator usability for the tested operator/path/environment.

Current canonical scientific-state effect:

```text
NONE
```

### Governed Repo adjudication companion #1256

May adjudicate the bounded #1210 usability claim after raw operator evidence exists.

It does not create an empirical scientific replicate.

Current canonical scientific-N effect:

```text
0
```

### Tektite HCI #1224

May establish bounded unfamiliar-user/receiver evidence under the frozen HCI protocol.

Current canonical scientific-N effect:

```text
0
```

### AOSS Stage-A #929

May establish independently reviewed predicates at the scope authorized by the frozen handoff and downstream acceptance rules.

Independent review of existing apparatus/evidence is not automatically a scientific replicate. Any proposed N effect would require a separate empirical protocol and Scientific State Transition Record.

## Current project ceiling

At adoption of this contract, no evidence is being newly admitted.

The controlling project state therefore remains:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

## Relationship to existing mechanisms

- `docs/CURRENT_STATE.md` remains the current-facing scientific-state authority.
- Lane-specific validators remain authoritative for whether their exact evidence satisfies their protocols.
- `docs/governance/EVIDENCE_GATE_V0.md` governs reusable evidence-admission semantics but does not itself authorize scientific-state promotion.
- `docs/governance/ALIGNMENT_CONSTRAINT_LEDGER.md` provides broader consequential-action/admission principles and explicitly rejects independence inflation from duplicated or correlated evidence.
- This contract adds the missing cross-lane rule: **lane evidence can change canonical scientific state only through an explicit admitted Scientific State Transition Record**.

## Non-effects

Creating, reviewing, testing, or merging this contract:

- does not increment scientific N;
- does not establish independent validation;
- does not establish canonical DGAF efficacy;
- does not authorize collection, analysis, mutation, or runtime execution;
- does not establish High-Assurance;
- does not retroactively reclassify historical evidence.

Its scientific-state effect is `NONE`.
