# Agent Governance Transition Specification

> **Status:** PROSPECTIVE FORMAL SPECIFICATION / NON-AUTHORIZING  
> **Scientific-state effect:** NONE  
> **Established:** 2026-09-17

## Purpose

This specification formalizes a governance pattern for agentic workflows in which evidence, authorization, execution, side effects, recovery, and audit remain distinguishable states.

It is intentionally compatible with DGAF's fail-closed evidence discipline, but it does not alter any existing DGAF gate, accepted record, Track A state, or authorization.

The associated prospective action-admission specification is `../governance/ALIGNMENT_CONSTRAINT_LEDGER.md`.

## State model

Represent a governed workflow state at time `t` as:

```text
S_t = (
  identity,
  task,
  evidence_state,
  verification_state,
  policy_state,
  authorization_state,
  artifact_state,
  execution_state,
  recovery_state,
  audit_state
)
```

A proposed transition is:

```text
S_(t+1) = T(S_t, action_t, evidence_t, authority_t)
```

`T` is permitted only when all required guards hold. Missing required evidence is treated as guard failure rather than permission.

## Canonical workflow phases

```text
PROPOSED
  -> CANONICALIZED
  -> EVIDENCE_GATHERING
  -> VERIFICATION_PENDING
  -> VERIFIED or REJECTED or INCONCLUSIVE
  -> APPROVAL_PENDING
  -> AUTHORIZED or REJECTED
  -> PREPARED
  -> COMMIT_REVALIDATION
  -> COMMIT_REVALIDATED or REJECTED
  -> EXECUTING
  -> EXECUTED or FAILED
  -> POSTCONDITION_PENDING
  -> VERIFIED_POSTCONDITION or POSTCONDITION_FAILED or POSTCONDITION_INCONCLUSIVE
  -> CLOSED
```

Optional recovery transitions:

```text
EXECUTING or EXECUTED or POSTCONDITION_*
  -> CONTAINMENT
  -> ROLLBACK_PENDING or COMPENSATION_PENDING or ESCALATED
  -> ROLLED_BACK or COMPENSATED or RECOVERY_FAILED
  -> CLOSED or ESCALATED
```

The named states are a reusable reference model. A concrete system may use different labels if their semantics remain explicit.

## Required identities

A governed action SHOULD bind, where applicable:

- task/request identity;
- canonical action identity and digest;
- requesting agent or human identity;
- executing agent/tool identity;
- policy/rule-set identity and version;
- model and prompt/configuration identity;
- evidence-set identity;
- verifier identity;
- approving authority identity;
- authority/delegation-chain identity;
- target resource identity;
- environment/runtime identity;
- resulting artifact or side-effect identity;
- audit-event/receipt identity.

Unknown identities must remain `UNKNOWN`; absence must not silently become equivalence or approval.

## Core invariants

### G1 — No side effect without admissible authorization

```text
ExternalSideEffect(a) -> ValidAuthorization(a)
```

An application-layer statement that authorization exists is insufficient if the tool gateway can execute without checking it.

### G2 — Authorization precedes execution

```text
Execute(a, t_e) -> exists t_a < t_e : AuthorizationGranted(a, t_a)
```

Retrospective approval cannot convert an unauthorized action into an authorized one.

### G3 — Authorization is scoped

A valid authorization binds at minimum:

```text
(subject, action_class, target_scope, policy_version, validity_window)
```

and, for high-risk actions, SHOULD also bind the canonical action digest and relevant artifact/evidence identities.

Authorization for one target, epoch, deployment, data set, workflow composition, or action class does not transfer by adjacency.

### G4 — Self-approval of policy exceptions is prohibited

```text
RequestsException(x, actor) -> Approver(x) != actor
```

A multi-agent implementation using the same effective authority for requester and approver does not satisfy separation merely because two process labels exist.

### G5 — Verification is not authorization

```text
Verified(x) -/-> Authorized(x)
```

Passing validation establishes only the validated predicate. A separate authorization event is required where policy demands one.

### G6 — Authorization is not execution

```text
Authorized(x) -/-> Executed(x)
```

Execution requires its own receipt or observable side-effect evidence.

### G7 — Evidence provenance is preserved

For every material decision-driving claim `c`:

```text
Material(c) -> ProvenanceLinked(c)
```

If provenance is unavailable, the workflow must label the claim accordingly rather than fabricate a source relation.

### G8 — Failed required verification blocks the protected transition

```text
RequiredVerifierFailed(x) -> not ProtectedTransition(x)
```

Verifier unavailability is not auto-approval. Escalation to a separately authorized human or controller is permitted if the policy defines that path.

### G9 — Revocation invalidates future use

If authorization `q` is revoked at `t_r`:

```text
UseAuthorization(q, t > t_r) = FORBIDDEN
```

Already completed actions remain historical facts and should not be rewritten as if they had not occurred.

### G10 — Auditability survives success and failure

A protected execution SHOULD emit or atomically bind a non-ambiguous event record containing:

- input/task identity;
- canonical action identity/digest;
- policy and authorization identity;
- executor/tool identity;
- time;
- action class and target;
- outcome;
- resulting artifact/side-effect identity when available;
- postcondition state;
- recovery/compensation state.

Audit logging must avoid leaking protected secrets.

### G11 — Delegation cannot widen authority

```text
DelegatedAuthority(child) subseteq DelegatedAuthority(parent)
```

Delegation cannot mint new capabilities, scope, budget, duration, exception rights, or recovery authority.

### G12 — Action-specific approval is digest-bound

Where policy uses action-specific approval:

```text
ApprovalDigest(a) == CommitDigest(a)
```

Material substitution invalidates the approval.

### G13 — Commit-time revalidation is required for volatile predicates

An authorization may be valid when issued but invalid at commit. Immediately before the side effect, required volatile predicates must still hold.

```text
Commit(a) -> RevalidatedAtCommit(a)
```

### G14 — Authorization is not automatically compositional

```text
Authorized(A) AND Authorized(B) -/-> Authorized(A then B)
```

Composition requires explicit policy closure or a separately governed workflow/action identity.

### G15 — Postcondition failure does not erase execution

```text
Executed(a) AND PostconditionFailed(a) -> Executed(a)
```

The response is containment, rollback, compensation, or escalation—not historical rewriting.

### G16 — Weaker evidence cannot increase authority

For required evidence under the same policy and scope:

```text
EvidenceStrength(e2) <= EvidenceStrength(e1)
  -> Authority(e2) <= Authority(e1)
```

This is a governance monotonicity requirement for future concrete policy definitions, not a universal numeric evidence metric.

## Transition guards

### Proposed -> canonicalized

Required guards SHOULD include:

- action class selected from the accepted registry where applicable;
- target scope explicit;
- material parameters canonicalized;
- canonical action digest recorded where approval/receipt binding requires it.

### Evidence gathering -> verification pending

Required guards may include:

- task identity fixed;
- source/evidence identifiers recorded;
- retrieval/tool failures recorded;
- material claims enumerable.

### Verification pending -> verified

Required guards may include:

- required verifier set completed;
- verifier dependency requirements satisfied or explicitly waived by authorized policy;
- contradictions recorded;
- required provenance checks passed;
- no unresolved blocking defeater.

### Approval pending -> authorized

Required guards may include:

- verification state accepted;
- policy version identified;
- approver has authority for action and scope;
- requester/approver separation satisfied where required;
- delegation chain valid and non-widening where used;
- authorization record created and bound to action scope/digest as policy requires.

### Authorized -> prepared

Preparation MAY stage data, build a provider request, or reserve resources, but it MUST NOT perform the protected side effect unless the policy explicitly defines preparation itself as the protected action and authorizes it.

### Prepared -> commit revalidation

Required guards may include:

- authorization not expired, revoked, superseded, or consumed;
- canonical action digest unchanged;
- target identity unchanged;
- policy identity still admitted;
- delegation chain still valid;
- artifact/configuration hashes unchanged where locked;
- environment/tool identity admitted;
- rate/cost/risk limits satisfied;
- no active blocking defeater;
- required dependency/verifier availability satisfied.

### Commit revalidation -> executing

Every required volatile predicate must be `TRUE`. `FALSE`, `UNKNOWN`, missing, stale, or identity-mismatched required predicates do not permit execution unless a separately authorized policy path explicitly resolves the condition.

### Executing -> executed

Required evidence includes an execution receipt or equivalent provider/tool evidence. A local intention or queued request is not execution.

### Executed -> verified postcondition

Postconditions MAY include:

- target reflects intended state;
- no prohibited side effect observed within the declared observation boundary;
- runtime identity matches authorized identity;
- output/artifact hash matches receipt;
- recovery mechanism remains available where policy requires it.

A failed/inconclusive required postcondition blocks closure or dependent actions where policy so specifies; it does not retroactively erase execution.

## Recovery semantics

Recovery MUST distinguish:

```text
REVERSIBLE
COMPENSATABLE
IRREVERSIBLE
```

- `REVERSIBLE` effects may use a tested rollback that restores the governed state within scope.
- `COMPENSATABLE` effects use a new governed action to remediate without pretending the original event never happened.
- `IRREVERSIBLE` effects require stronger pre-execution controls and containment/escalation because rollback is unavailable.

For composed workflows, partial completion MUST have an explicit policy: forward recovery/retry, rollback, compensation, containment/escalation, or accepted partial state under separately recorded authority.

## Fail-closed decision rule

For a protected transition requiring predicates `p_1 ... p_n`:

```text
permit = all(p_i == TRUE)
```

`FALSE`, `UNKNOWN`, missing, stale beyond policy, or identity-mismatched predicates do not satisfy the transition unless the governing policy explicitly defines a separate escalation path.

## Provenance-aware verification extension

Where independent verification is required, a quorum SHOULD be evaluated against evidence-path requirements, not raw agent count alone.

Example policy shape:

```text
required_verifiers: 3
required_distinct_provenance_roots: 2
peer_outputs_hidden_until_first_pass: true
counterevidence_attempt_required: true
final_adjudicator_may_reject_consensus: true
```

This is an illustrative policy pattern, not a claim that those thresholds are universally sufficient.

## Runtime enforcement boundary

A governance invariant is strongest when enforced at the narrowest component capable of causing the protected side effect.

Preferred layering:

```text
model/agent proposal
  -> action canonicalizer
  -> policy/admissibility evaluator
  -> authorization verifier
  -> commit-time revalidator
  -> typed tool gateway
  -> external system
  -> provider/runtime receipt
  -> postcondition verifier
```

Prompt text alone is not an enforcement boundary for real permissions.

## Example: publishing workflow

```text
Research agent
  -> evidence verifier
  -> synthesizer
  -> human/separate approval authority
  -> commit-time action digest / authority revalidation
  -> publishing gateway
  -> external publication receipt
  -> postcondition/currentness check
```

Required example invariants:

- every material claim has linked evidence or explicit unsupported status;
- a failed required verifier blocks publication or escalates;
- agents cannot self-approve policy exceptions;
- publishing gateway verifies a valid approval record for the exact action;
- final publication identity is captured after execution;
- later source revision may mark the publication's inputs stale/currentness-affected without rewriting the original provenance.

## Security considerations

The transition system SHOULD account for:

- confused-deputy failures;
- stale/replayed authorization tokens;
- identity substitution;
- prompt/tool injection;
- policy-version drift;
- approval-target/digest mismatch;
- authority revocation races;
- race conditions between validation and execution;
- delegation laundering or scope widening;
- partial execution and rollback/compensation failure;
- lineage fork/supersession ambiguity;
- audit-log/receipt tampering;
- secret exposure through logs or evidence records.

## Standards alignment

NIST's 2026 agent identity/authorization work identifies agent identification, authorization, auditing, non-repudiation, and controls against indirect prompt-injection risk as active standards concerns. This specification uses those areas as external alignment targets, not as certification of DGAF.

Reference: [NIST — Accelerating the Adoption of Software and AI Agent Identity and Authorization](https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd)

## Verification strategy

A concrete implementation SHOULD test this specification at multiple layers:

1. state-machine/unit tests for legal and illegal transitions;
2. property-based tests for malformed or missing evidence;
3. metamorphic tests for authority/evidence monotonicity;
4. governance mutation tests, including mutation of verifier/control logic;
5. model checking for small finite authorization/state models where practical;
6. integration tests proving the tool gateway rejects unauthorized or stale actions;
7. adversarial tests for replay, target substitution, stale policy, revocation race, delegation widening, and self-approval;
8. provider/runtime readback proving successful actions occurred on the intended target;
9. postcondition and recovery tests proving history is preserved across failure.

## Non-transfer rule

Passing a formal-model or implementation test for this generic specification does not establish DGAF efficacy, PDMAL topology advantage, independent validation, production certification, or any current Track A transition. Those require their own exact-scope evidence.
