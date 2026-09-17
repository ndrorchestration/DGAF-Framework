# Agent Governance Transition Specification

> **Status:** PROSPECTIVE FORMAL SPECIFICATION / NON-AUTHORIZING  
> **Scientific-state effect:** NONE  
> **Established:** 2026-09-17

## Purpose

This specification formalizes a governance pattern for agentic workflows in which evidence, authorization, execution, side effects, rollback, and audit must remain distinguishable states.

It is intentionally compatible with DGAF's fail-closed evidence discipline, but it does not alter any existing DGAF gate, accepted record, Track A state, or authorization.

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
  -> EVIDENCE_GATHERING
  -> VERIFICATION_PENDING
  -> VERIFIED or REJECTED
  -> APPROVAL_PENDING
  -> AUTHORIZED or REJECTED
  -> EXECUTION_PENDING
  -> EXECUTING
  -> EXECUTED or FAILED
  -> VERIFIED_POSTCONDITION
  -> CLOSED
```

Optional recovery transitions:

```text
EXECUTING or EXECUTED
  -> CONTAINMENT
  -> ROLLBACK_PENDING
  -> ROLLED_BACK or ROLLBACK_FAILED
  -> ESCALATED
```

The named states are a reusable reference model. A concrete system may use different labels if their semantics remain explicit.

## Required identities

A governed action SHOULD bind, where applicable:

- task/request identity;
- requesting agent or human identity;
- executing agent/tool identity;
- policy/rule-set identity and version;
- model and prompt/configuration identity;
- evidence-set identity;
- verifier identity;
- approving authority identity;
- target resource identity;
- resulting artifact or side-effect identity;
- audit-event identity.

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

and, for high-risk actions, SHOULD also bind relevant artifact/evidence identities.

Authorization for one target, epoch, deployment, data set, or action class does not transfer by adjacency.

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

Escalation to a separately authorized human or controller is permitted if the policy defines that path.

### G9 — Revocation invalidates future use

If authorization `q` is revoked at `t_r`:

```text
UseAuthorization(q, t > t_r) = FORBIDDEN
```

Already completed actions remain historical facts and should not be rewritten as if they had not occurred.

### G10 — Auditability must survive success and failure

A protected execution SHOULD emit or atomically bind an immutable/non-ambiguous event record containing:

- input/task identity;
- policy and authorization identity;
- executor/tool identity;
- time;
- action class and target;
- outcome;
- resulting artifact/side-effect identity when available;
- failure/rollback state.

Audit logging must avoid leaking protected secrets.

## Transition guards

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
- no unresolved blocking failure.

### Approval pending -> authorized

Required guards may include:

- verification state accepted;
- policy version identified;
- approver has authority for action and scope;
- requester/approver separation satisfied where required;
- authorization record created and bound to action scope.

### Execution pending -> executing

Required guards may include:

- authorization still valid;
- target identity unchanged;
- artifact/configuration hashes unchanged where locked;
- environment/tool identity admitted;
- rate/cost/risk limits satisfied.

### Executing -> executed

Required evidence includes an execution receipt or equivalent provider/tool evidence. A local intention or queued request is not execution.

### Executed -> verified postcondition

Postconditions MAY include:

- target reflects intended state;
- no prohibited side effect observed;
- runtime identity matches authorized identity;
- output/artifact hash matches receipt;
- rollback capability remains intact where required.

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
  -> policy evaluator
  -> authorization verifier
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
  -> publishing gateway
  -> external publication receipt
```

Required example invariants:

- every material claim has linked evidence or explicit unsupported status;
- a failed required verifier blocks publication or escalates;
- agents cannot self-approve policy exceptions;
- publishing gateway verifies a valid approval record;
- final publication identity is captured after execution.

## Security considerations

The transition system SHOULD account for:

- confused-deputy failures;
- stale/replayed authorization tokens;
- identity substitution;
- prompt/tool injection;
- policy-version drift;
- approval-target mismatch;
- race conditions between validation and execution;
- partial execution and rollback failure;
- audit-log tampering;
- secret exposure through logs or evidence records.

## Standards alignment

NIST's 2026 agent identity/authorization work identifies agent identification, authorization, auditing, non-repudiation, and controls against indirect prompt-injection risk as active standards concerns. This specification uses those areas as external alignment targets, not as certification of DGAF.

Reference: https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd

## Verification strategy

A concrete implementation SHOULD test this specification at multiple layers:

1. state-machine/unit tests for legal and illegal transitions;
2. property-based tests for malformed or missing evidence;
3. model checking for small finite authorization/state models where practical;
4. integration tests proving the tool gateway rejects unauthorized actions;
5. adversarial tests for replay, target substitution, stale policy, and self-approval;
6. provider/runtime readback proving successful actions occurred on the intended target.

## Non-transfer rule

Passing a formal-model or implementation test for this generic specification does not establish DGAF efficacy, PDMAL topology advantage, independent validation, production certification, or any current Track A transition. Those require their own exact-scope evidence.
