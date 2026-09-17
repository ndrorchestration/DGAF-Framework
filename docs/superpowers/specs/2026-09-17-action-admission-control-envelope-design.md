# Action Admission and Control-Envelope Enforcement Design

> **Status:** DESIGN SPECIFICATION / RUNTIME IMPLEMENTATION NOT STARTED BY THIS SPEC  
> **Date:** 2026-09-17  
> **Design lineage:** Structural Epistemics research + Alignment Constraint Ledger + DGAF ecosystem pattern review.

## Problem

DGAF has strong existing primitives for fail-closed state transition, exact identity, evidence separation, authorization boundaries, provenance, and adversarial verification. The Structural Epistemics work adds a prospective Alignment Constraint Ledger. The remaining architectural problem is to turn that ledger from documentation into an enforceable runtime admission mechanism without creating a second governance system or overstating current authority.

## Design decision

Use the ledger as a machine-readable **Action Admission Record (AAR)** inside the existing governance transition architecture.

The eventual enforced path is:

```text
untrusted planner/reasoner
  -> action proposal
  -> canonicalization + action digest
  -> AAR admissibility validation
  -> required verification/approval
  -> prepared action
  -> commit-time revalidation
  -> typed execution gateway
  -> external side effect
  -> execution receipt
  -> postcondition verification
  -> closed / rollback / compensation / containment / escalation
```

The reasoning plane may use one agent, triads, panels, or other orchestration patterns. The authority plane remains deterministic/policy-governed and does not delegate permission to conversational consensus.

## Architectural boundaries

### Existing primitives to reuse

- fail-closed guarded transition semantics;
- exact identity and non-transfer discipline;
- verification/authorization/execution separation;
- Evidence Card semantics;
- proposal/authorization/commit barriers;
- append-oriented provenance and audit records;
- negative-path governance tests.

### Ecosystem patterns to adapt

- digest-bound approval;
- single-use action authorization;
- attenuated delegation;
- revision-aware staleness;
- append-only validity/invalidation events;
- explicit defeaters;
- trust-anchored receipt lineage;
- failure-to-regression conversion;
- governance mutation, metamorphic, and verifier-mutation testing.

### New runtime components required

1. **Consequential Action Registry** — versioned list/rules identifying which action classes require AAR enforcement.
2. **Action Canonicalizer** — deterministic canonical representation and digest for action-specific approval.
3. **AAR Schema + Validator** — machine-readable structure and fail-closed static/dynamic validation.
4. **Authority Chain Validator** — validates delegation provenance, scope attenuation, separation-of-duties predicates, expiry/revocation.
5. **Commit Revalidator** — rechecks volatile predicates immediately before the side effect.
6. **Typed Execution Gateway Adapter** — refuses protected execution without a valid required AAR.
7. **Receipt/Lineage Handler** — emits exact execution evidence, replay/idempotency identity, supersession/revocation metadata.
8. **Postcondition/Recovery Coordinator** — manages closure, rollback, compensation, containment, and escalation states.
9. **Coverage Auditor** — reports action-registry coverage without implying completeness beyond the registry.

## Key invariants

```text
I1  consequential && AAR_required && !valid_AAR -> no protected execution
I2  authority(child) subseteq authority(parent)
I3  approval.action_digest == commit.action_digest
I4  verified -/-> authorized
I5  authorized -/-> executed
I6  authorized(A) && authorized(B) -/-> authorized(A then B)
I7  revoked/expired/superseded authority cannot be used at commit
I8  UNKNOWN required predicate != PASS
I9  receipt replay cannot create a second authorized effect
I10 historical execution is never erased by later postcondition failure
I11 weaker/staler evidence cannot increase authority
I12 correlated/duplicated evidence cannot increase independent-verification count
I13 discovery/evaluation findings cannot directly increase authority
```

## State model

The AAR workflow lifecycle is operational and separate from Evidence Card state:

```text
DRAFT
-> SPECIFIED
-> ADMISSIBILITY_PENDING
-> ADMISSIBLE | REJECTED | INCONCLUSIVE
-> APPROVAL_PENDING
-> AUTHORIZED | REJECTED
-> PREPARED
-> COMMIT_REVALIDATION
-> COMMIT_REVALIDATED | REJECTED
-> EXECUTING
-> EXECUTED | FAILED
-> POSTCONDITION_PENDING
-> POSTCONDITION_VERIFIED | POSTCONDITION_FAILED | POSTCONDITION_INCONCLUSIVE
-> CLOSED | CONTAINMENT | ROLLBACK | COMPENSATION | ESCALATED
```

The exact implementation may simplify labels if semantic distinctions and fail-closed transitions remain intact.

## Composition and recovery

A multi-action workflow is treated as a governed composition, not as implicit transitive authorization.

For a sequence `A -> B -> C`, failure after partial completion must select an explicit policy outcome:

- forward recovery/retry when idempotent and still authorized;
- rollback for genuinely reversible effects;
- compensating action when the original effect cannot be erased but can be remediated;
- containment/escalation for irreversible or uncertain effects;
- explicitly authorized partial completion only when policy permits it.

Compensating actions are new governed actions with their own identities and authority requirements.

## Validity and defeaters

Admission depends on both supporting predicates and absence/resolution of blocking defeaters.

Validity events preserve chronology using `ACTIVE`, `SUPERSEDED`, and `INVALIDATED` rather than rewriting old records.

Candidate defeaters include authority withdrawal, source/target mismatch, validator defects, policy incompatibility, replay, environment mismatch, material input drift, provenance tampering, and invalidated assumptions.

## Trust model

Hashing is necessary for identity/integrity but insufficient for authority.

A stronger receipt/admission chain binds:

```text
record digest
parent digest / lineage id
source/policy/environment identities
admission authority
signature or verifiable attestation where available
signed/observed time
supersession/revocation state
```

Forks remain explicit and block protected clearance when a unique accepted lineage is required.

## Testing design

Implementation uses TDD for behavior changes.

### Unit/state tests

- legal transition succeeds;
- illegal transition is rejected;
- missing required fields fail closed;
- delegation widening is rejected;
- stale/revoked authorization is rejected;
- digest substitution is rejected;
- replay is rejected/idempotently recognized as policy defines;
- postcondition failure preserves executed history.

### Property/metamorphic tests

- evidence removal cannot increase authority;
- provenance weakening cannot increase authority;
- evidence aging cannot increase authority;
- evidence duplication cannot increase independence;
- verifier de-independence cannot increase independent count;
- irrelevant metadata changes do not alter decision;
- tighter restrictions cannot expand authority.

### Mutation tests

Mutate high-risk governance semantics and require test failure:

- `DENY -> ALLOW`;
- `UNKNOWN -> PASS`;
- expiry ignored;
- revocation ignored;
- action digest comparison bypassed;
- delegation subset check inverted;
- required step omitted/reordered;
- same evidence duplicated and counted as independent;
- policy identity substituted.

### Integration/runtime tests

For the first enforced action class, prove at the actual gateway that:

- no valid required AAR means no protected side effect;
- exact authorized action succeeds only when all commit predicates remain valid;
- provider/runtime receipt binds to the intended target;
- postcondition behavior and recovery transitions match policy.

## Rollout strategy

Do not enforce every action class at once.

1. Implement schemas/validators without authority effect.
2. Select one narrow, reversible, non-scientific action class.
3. Run tests and shadow/advisory validation without changing existing authorization semantics.
4. Establish exact-scope evidence for the validator and gateway integration.
5. Explicitly authorize enforcement for that action class through the existing governance mechanism.
6. Expand only after negative/adversarial behavior is verified.

This avoids a big-bang permission migration and provides a falsifiable path to enforcement.

## Relationship to PR #747

PR #747 remains the research/specification tranche. It may contain this design and the prospective ledger specification, but it must not claim runtime enforcement.

Runtime code, schemas, validators, gateway changes, and tests belong in a separate implementation PR after this written design is reviewed.

## Non-effects

This design does not establish:

- current gateway enforcement;
- production certification;
- complete model alignment;
- P1-P9 closure;
- Track A materialization or primary-analysis authorization;
- scientific-N increase;
- DGAF/PDMAL efficacy;
- independent validation.

## Acceptance criteria for the later implementation tranche

The first runtime implementation is acceptable only when:

- the selected consequential action class is explicitly named;
- RED tests demonstrate the missing enforcement behavior before production code is added;
- all required guards and negative paths pass after implementation;
- gateway integration prevents the protected side effect under invalid/missing AAR conditions;
- replay, digest substitution, revocation, expiry, and delegation-widening tests pass;
- postcondition and recovery behavior is evidenced;
- no test/evidence claim is promoted beyond exact runtime scope;
- the implementation PR identifies remaining uncovered action classes and residual risks.
