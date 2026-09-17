# Alignment Constraint Ledger / Action Admission Record

> **Status:** PROSPECTIVE NORMATIVE SPECIFICATION / NOT YET ENFORCED  
> **Established:** 2026-09-17  
> **Scientific-state effect:** NONE  
> **Runtime-authority effect:** NONE until a separately reviewed implementation is enforced at the execution boundary.

## Purpose

This specification defines a reusable control-envelope record for consequential agentic actions. The human-facing name is **Alignment Constraint Ledger**; the machine-facing unit is an **Action Admission Record (AAR)**.

The target invariant is:

```text
ConsequentialAction(a) AND MissingOrInvalidAdmissionRecord(a)
  -> execution forbidden
```

That invariant is a **prospective normative target**, not a claim about current DGAF runtime behavior. This document does not establish that any existing executor or tool gateway already enforces the ledger.

The ledger is constraint engineering, not a proof of complete model alignment. It governs specified actions, authority, evidence, execution, and recovery under declared assumptions.

## Control-envelope definition

A **control envelope** is the set of consequential actions for which the governing system can establish, for the exact action identity and declared scope:

- an enforceable precondition set;
- an admissible authority chain;
- the verifier set required by the applicable risk policy;
- an explicit authorization record when policy requires authorization;
- commit-time revalidation of volatile predicates;
- an execution receipt or equivalent runtime evidence;
- a postcondition verification rule;
- a recovery classification and response;
- a fail-closed response for missing, false, stale, unknown, or identity-mismatched prerequisites;
- and a declared assumption/coverage boundary.

Actions outside this set are outside the envelope. The boundary must be explicit rather than implied.

## Consequential-action boundary

A concrete implementation MUST define a versioned consequential-action registry. An action is presumptively consequential when it can materially alter one or more of:

- external or shared persistent state;
- authority, roles, capabilities, permissions, credentials, or policy;
- production deployment or executable code state;
- money, purchasing, billing, or resource commitments;
- publication or communication to a shared/public audience;
- protected data disclosure, retention, deletion, or movement;
- experiment authorization, unblinding, materialization, analysis, or evidence state;
- irreversible or difficult-to-reverse real-world effects.

Private drafting, read-only reasoning, or reversible local computation may be classified as non-consequential only by explicit policy. The registry, not model discretion, owns that classification.

## Canonical action identity

Before approval or execution, a consequential action SHOULD be canonicalized into a stable representation and bound to a digest.

At minimum, identity SHOULD bind:

```text
action_id
request_id
actor_id
action_class
target_scope
canonical_parameters
intended_effect
policy_identity
material_input_identities
```

Where digest binding is used:

```text
approval.action_digest == execution.action_digest
```

A materially changed action is a new action identity. Approval for action `A` does not transfer to `A'` merely because the change appears small.

## Required record domains

A complete AAR SHOULD contain the following domains. A machine-readable implementation MAY split these into linked records if identity and referential integrity remain exact.

### 1. Identity

```yaml
identity:
  action_id: <stable id>
  request_id: <request id>
  action_class: <registry class>
  target: <exact target scope>
  canonical_action_digest: <digest>
  intended_effect: <description>
```

### 2. Authority and delegation

```yaml
authority:
  principal: <originating authority>
  execution_principal: <executor identity>
  authority_scope: <scope>
  delegation_chain: []
  separation_of_duties: <policy result>
```

Delegation MUST be scope-preserving or scope-reducing:

```text
Authority(child) subseteq Authority(parent)
```

A child delegation MUST NOT add an action class, target, data domain, privilege, budget, duration, exception right, or recovery privilege not held by its parent.

Unknown delegation provenance fails closed where delegated authority is required.

### 3. Policy and prohibitions

```yaml
policy:
  policy_id: <id>
  policy_version: <digest/version>
  prohibited_outcomes: []
  mandatory_preconditions: []
  applicable_risk_tier: <tier>
  assumptions: []
```

Policy identity is part of the admission decision. Substituting another policy after approval requires re-adjudication unless the governing policy explicitly proves compatibility.

### 4. Validity and staleness

```yaml
validity:
  valid_from: <timestamp>
  valid_until: <timestamp or null>
  bound_model_identity: <identity or null>
  bound_tool_identity: <identity or null>
  bound_environment_identity: <identity or null>
  invalidation_triggers: []
  validity_state: ACTIVE | SUPERSEDED | INVALIDATED
```

Material changes SHOULD be classified rather than treated as an undifferentiated reset:

- cosmetic/non-decision-affecting: record without automatic invalidation;
- procedure-affecting: targeted revalidation;
- decision-affecting: revalidate the affected admission decision;
- scope-affecting: require new coverage/admission for the added scope;
- security/custody-affecting: revalidate relevant identity, provenance, and authority controls.

Historical records are preserved. `INVALIDATED` means no longer admissible for the affected use; it does not erase what occurred.

### 5. Admissibility and verification

```yaml
admissibility:
  preconditions: []
  evidence_refs: []
  verifier_requirements: []
  verifier_results: []
  independence_requirements: []
  blocking_defeaters: []
  decision: ADMISSIBLE | REJECTED | INCONCLUSIVE
```

`INCONCLUSIVE` is not permission. When policy requires a fact to be established, `UNKNOWN`, missing evidence, stale evidence, or verifier unavailability fails closed or enters an explicitly authorized escalation path.

### 6. Specification-gaming analysis

```yaml
specification_gaming_analysis:
  proxy_specification: <what is actually checked>
  intended_norm: <what the control is intended to protect>
  potential_omissions: []
  exploit_scenarios: []
  mitigations: []
  residual_risk: []
```

Formal compliance with a proxy does not establish that the intended norm is satisfied outside the proxy's coverage.

### 7. Defeaters

Controls that support admission and facts that defeat admission MUST be representable separately.

Example defeaters include:

- authority revoked;
- validator/verifier defect established;
- source or target identity mismatch;
- policy superseded or incompatible;
- material input changed;
- environment/tool identity outside admitted scope;
- replay or nonce reuse;
- receipt or provenance tampering;
- required assumption invalidated;
- dependency failure where policy requires live verification.

An active blocking defeater prevents protected execution unless the governing policy defines a separately authorized resolution path.

### 8. Composition

Authorization is not closed under arbitrary composition.

```text
Authorized(A) AND Authorized(B) -/-> Authorized(A then B)
```

A materially consequential composition SHOULD be assigned its own workflow/action identity unless a policy explicitly establishes safe closure for the composition.

```yaml
composition:
  workflow_id: <id>
  predecessor_action_ids: []
  composition_policy: <policy ref>
  cross_action_invariants: []
  partial_completion_policy: <policy ref>
  composition_authorization: <ref or null>
```

Composition checks SHOULD account for cross-action side effects, ordering, stale assumptions, cumulative budgets, and authority scope.

### 9. Execution authorization and replay protection

```yaml
execution:
  authorization_id: <id>
  authorization_digest: <digest>
  single_use: <boolean>
  nonce: <nonce>
  idempotency_key: <key>
  prepared_at: <timestamp>
  committed_at: <timestamp or null>
  executor_identity: <identity>
```

High-impact authorizations SHOULD be action-specific and single-use unless policy explicitly requires a reusable capability grant.

### 10. Commit-time revalidation

Approval at time `t1` does not by itself establish admissibility at execution time `t2`.

Immediately before the protected side effect, the execution boundary SHOULD revalidate volatile predicates such as:

- authorization not expired, revoked, superseded, or consumed;
- action digest unchanged;
- delegation chain still valid;
- actor/executor identity still admitted;
- target identity and scope unchanged;
- policy identity still admitted;
- required environment/tool identities still admitted;
- applicable rate, budget, and risk limits still satisfied;
- no active blocking defeater;
- required verifier dependencies available or explicitly resolved by policy.

Failure at the commit barrier produces no new protected side effect.

### 11. Recovery and reversibility

The ledger MUST distinguish literal rollback from compensation.

```text
reversibility_class = REVERSIBLE | COMPENSATABLE | IRREVERSIBLE
```

- `REVERSIBLE`: a tested rollback path restores the governed state within declared scope.
- `COMPENSATABLE`: the original event remains historical; a separately governed compensating action reduces or repairs its effects.
- `IRREVERSIBLE`: rollback is unavailable; stronger pre-execution review, narrower scope, simulation/preflight, explicit residual-risk acceptance, and containment/escalation requirements SHOULD apply.

A claim that rollback exists requires tested evidence appropriate to the target environment. Compensation MUST NOT be described as erasure of the original event.

### 12. Postcondition verification

```yaml
postcondition:
  expected: <description>
  verification_method: <method>
  verification_timing: immediate | delayed | sampled
  verification_result: PASS | FAIL | INCONCLUSIVE | NOT_RUN
  verification_evidence: <reference or null>
```

An executed action with an unverified postcondition remains executed. The system MUST NOT rewrite history by treating it as unexecuted.

A failed or inconclusive required postcondition SHOULD transition to containment, compensation/rollback where applicable, or escalation and SHOULD block dependent actions where policy requires closure first.

### 13. Provenance and receipt lineage

```yaml
provenance:
  request_ref: <ref>
  approval_ref: <ref>
  execution_receipt_ref: <ref>
  receipt_digest: <digest>
  parent_receipt_digest: <digest or null>
  lineage_id: <id>
  admission_authority_id: <id>
  signature_or_attestation_ref: <ref or null>
  signed_at: <timestamp or null>
  supersedes: <digest or null>
  revocation_status: <status>
```

Digest chaining can provide tamper evidence but does not by itself establish who authorized a record, whether the chain is complete, whether timestamps are trustworthy, or whether an entire chain was replaced. Trust-anchor semantics must be explicit.

A lineage fork MUST be represented rather than silently choosing one branch. A protected transition SHOULD remain blocked when required lineage is `FORKED` until an authorized reconciliation or supersession record resolves it.

### 14. Residual risk

Every consequential action class SHOULD disclose what remains uncertain after declared controls succeed.

```yaml
residual_risk:
  known_limitations: []
  unresolved_assumptions: []
  out_of_scope_hazards: []
  accepted_by: <authority or null>
  acceptance_basis: <policy ref or null>
```

Residual-risk acceptance cannot waive a hard prohibition unless the governing policy explicitly permits such an exception and records the authority for it.

### 15. Coverage

Coverage is meaningful only relative to a versioned action registry.

```yaml
coverage:
  registry_version: <version>
  consequential_action_count: <count>
  actions_with_required_admission_spec: <count>
  uncovered_actions: []
  known_registry_gaps: []
  reviewed_at: <timestamp>
```

A reported percentage MUST state its denominator and registry identity. `100%` of an incomplete or unreviewed registry is not system-wide assurance.

## Four-question audit mapping

| Audit question | Primary ledger domains |
|---|---|
| What can the system observe, infer, communicate, and do? | identity, action registry, target scope, authority, permissions |
| Which harms or authority violations must be impossible? | policy, prohibited outcomes, preconditions, commit barrier, fail-closed rule |
| What evidence could falsify the assurance claim? | verifier requirements, evidence refs, defeaters, specification-gaming analysis, coverage |
| Who can stop, investigate, and remediate failure? | authority, revocation, containment, recovery, escalation, incident ownership |

## Relationship to DGAF evidence semantics

The AAR lifecycle MUST NOT replace DGAF Evidence Card semantics.

An action record may have operational states such as:

```text
DRAFT
-> SPECIFIED
-> ADMISSIBILITY_PENDING
-> ADMISSIBLE
-> AUTHORIZED
-> PREPARED
-> COMMIT_REVALIDATED
-> EXECUTED
-> POSTCONDITION_VERIFIED
-> CLOSED
```

with failure/recovery states such as `REJECTED`, `INCONCLUSIVE`, `FAILED`, `CONTAINED`, `ROLLED_BACK`, `COMPENSATED`, `POSTCONDITION_UNVERIFIED`, or `ESCALATED`.

Those are workflow states. They do **not** automatically promote a claim class, evidence maturity, validation status, scientific state, or authorization elsewhere.

Evidence Cards remain evidence-bearing claim records. A future implementation SHOULD link AAR predicates to Evidence Cards or other authoritative evidence objects where a material claim requires evidence, without requiring one generic Evidence Card to impersonate the whole workflow.

## Relationship to P1-P9 and experimental gates

This specification does not redefine P1-P9.

A concrete AAR implementation may produce evidence relevant to an execution/runtime predicate or security predicate, but relevance must be established case by case. No ledger field silently becomes P2, P4, freeze, authorization, materialization, primary analysis, independent validation, or efficacy evidence.

## Failure-oriented verification requirements

A future enforcement implementation SHOULD include negative, mutation, property-based, metamorphic, integration, and runtime tests.

High-value required relations include:

```text
remove evidence             -> authority cannot increase
age evidence                -> authority cannot increase
weaken provenance           -> authority cannot increase
duplicate evidence          -> independence count cannot increase
mark verifiers correlated   -> independence count cannot increase
lose required verifier      -> cannot become auto-allow
tighten a control           -> authority cannot expand
change action digest        -> prior action-specific approval invalid
revoke parent grant         -> dependent delegated authority invalid
replay consumed receipt     -> no additional authorized effect
UNKNOWN required predicate  -> not PASS
DENY exception path         -> must not mutate to ALLOW unnoticed
```

The implementation SHOULD also mutate verifier/control logic and demonstrate that controlled corruption is detected, not merely that the original rule passes.

## Dependency circuit breaking

Runtime dependency protection MAY use an execution-layer circuit breaker with states such as `CLOSED`, `OPEN`, and `HALF_OPEN` to prevent repeated calls to a failing verifier, policy service, or target.

Circuit-breaker state is operational reliability state, not governance/scientific evidence. Opening the circuit MUST NOT create permission to bypass the failed dependency.

## Out-of-scope dependencies

The ledger can constrain specified action pathways; it does not resolve:

- normative legitimacy or value aggregation;
- inner alignment or learned-objective mismatch;
- complete deceptive-intent detection;
- general mechanistic interpretability;
- scalable oversight for arbitrarily stronger systems;
- corrigibility under unrestricted self-modification;
- safety outside declared environment and threat assumptions.

These may be recorded as dependencies or residual-risk boundaries, but the absence of a solution must not be represented as a solved ledger predicate.

## Implementation boundary

This document deliberately separates **specification** from **enforcement**.

The next implementation tranche requires a separate reviewed design and SHOULD include, at minimum:

1. a versioned consequential-action registry;
2. a machine-readable AAR schema;
3. a deterministic admissibility validator;
4. authority/delegation attenuation checks;
5. commit-time revalidation;
6. gateway rejection for missing/invalid required AARs;
7. replay/idempotency controls;
8. action receipts and lineage verification;
9. postcondition state handling;
10. recovery/compensation semantics;
11. coverage checks relative to the action registry;
12. failure-oriented tests demonstrating fail-closed behavior.

Until that tranche is implemented and independently verified for an exact runtime scope, the correct status remains **SPECIFIED / NOT YET ENFORCED**.

## External methodology anchors

These references provide design precedent, not DGAF certification or empirical evidence:

- [NIST — Accelerating the Adoption of Software and AI Agent Identity and Authorization](https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd)
- [W3C PROV Overview](https://www.w3.org/TR/prov-overview/)
- [in-toto documentation](https://in-toto.io/)
- [SLSA Source requirements v1.2](https://slsa.dev/spec/v1.2/source-requirements)
- [AWS Prescriptive Guidance — Saga orchestration pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-orchestration.html)
- [Azure Architecture Center — Circuit Breaker pattern](https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker)

## Non-transfer rule

Creating, reviewing, or implementing this specification does not establish DGAF/PDMAL efficacy, production certification, scientific-N increase, independent validation, Track A materialization, primary-analysis authorization, or High-Assurance authorization.
