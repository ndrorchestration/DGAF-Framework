# DGAF Core Component Inventory

**Status:** PROPOSED / ARCHITECTURE-CLASSIFICATION / NON-AUTHORIZING  
**Companion:** `DGAF_SYSTEM_ARCHITECTURE_TAXONOMY.md`

## Purpose

Identify the first-class internal DGAF components that constitute the governance kernel, distinguish them from assurance/support layers and domain-specific governance profiles, and expose convergence opportunities without deleting valid scope-specific controls.

## Core governance kernel

### K1 — Action canonicalization & effect identity

**Responsibility:** convert a requested consequential action into a stable, inspectable identity before authority is evaluated.

Current implementation evidence includes:

- canonical action envelopes;
- exact action digests;
- distinction between record identity and effect identity;
- exact capability/resource/parameter/principal/policy/state-guard binding.

**Primary artifacts:** `dgaf_capability_canonicalize.py`, Action Admission design contracts.

**Architectural rule:** authorization must bind to an exact action/effect identity rather than mutable caller narration.

### K2 — Policy, delegation & effective authority

**Responsibility:** determine the maximum authority available after requester, delegation, executor, and policy constraints are intersected.

Current implementation evidence includes:

- capability/resource authority sets;
- budget attenuation;
- non-widening delegation checks;
- active-time authorization checks;
- commit-digest approval matching;
- policy/effective-authority intersection.

**Primary artifacts:** `dgaf_capability_policy.py`, capability/delegation schemas.

**Architectural rule:** delegation may attenuate authority; it must not silently widen it.

### K3 — Admission & enforcement

**Responsibility:** convert policy/evidence/authorization state into an allow/deny/escalate decision immediately before consequential execution.

Current implementation evidence includes:

- Policy Decision Point / Policy Enforcement Point separation;
- Action Admission Record concepts;
- governed dispatch;
- commit-time guard revalidation;
- fail-closed refusal.

**Primary artifacts:** `dgaf_capability_pep.py`, `ACTION_ADMISSION_AUTHORITY_CONTRACT.md`, authorization schemas.

**Architectural rule:** verification does not manufacture authorization; execution requires independent admissible authority.

### K4 — Governed state-transition control

**Responsibility:** define legal workflow states, transitions, guards, and terminal/ambiguous conditions.

Current implementation evidence includes:

- finite transaction-state modeling;
- execution/postcondition states;
- guarded legal and illegal transitions;
- Track/Epoch state validators and control-state checks.

**Primary artifacts:** `dgaf_capability_state_machine.py`, `dgaf_capability_workflow.py`, control-state validators.

**Architectural rule:** state progression must be explicit and fail closed; evidence of one state cannot be silently promoted into another.

### K5 — Replay, idempotency, revocation & trust safeguards

**Responsibility:** prevent unsafe duplicate effects and ensure authorization/trust remains valid at commit time.

Current implementation evidence includes:

- idempotency reservation/completion/outcome-unknown states;
- action-digest conflict detection;
- replay blocking;
- provider-neutral replay authority contract;
- prospective revocation states;
- trust-anchor lifecycle vocabulary.

**Primary artifacts:** `dgaf_capability_idempotency.py`, SQLite idempotency adapter, `ACTION_ADMISSION_AUTHORITY_CONTRACT.md`.

**Architectural rule:** at-most-once authorized effect is the target bounded guarantee; exactly-once is not established.

### K6 — Execution evidence, receipts & provenance binding

**Responsibility:** retain machine-readable evidence linking identity, authority, execution, postconditions, runtime/adapter identity, and source evidence.

Current implementation evidence includes:

- execution receipts;
- audit events;
- provider receipt binding;
- evidence/verifier IDs;
- provenance/custody parity controls;
- exact-source and artifact identity.

**Primary artifacts:** `execution_receipt.schema.json`, `capability_audit_event.schema.json`, `dgaf_capability_reference_transaction.py`, provenance standards.

**Architectural rule:** narrative success is insufficient; consequential claims must bind to retained evidence and exact identities.

### K7 — Postcondition, ambiguity, recovery & reconciliation

**Responsibility:** determine whether an admitted effect actually achieved its intended state and safely handle failed or unknown outcomes.

Current implementation evidence includes:

- postcondition VERIFIED/FAILED/INCONCLUSIVE distinctions;
- EXECUTION_OUTCOME_UNKNOWN;
- recovery state;
- reconciliation-required outputs;
- explicit no-automatic-retry behavior after ambiguous replay consumption;
- retained recovery-composition controls.

**Primary artifacts:** reference transaction, workflow states, reconciliation schemas, recovery controls.

**Architectural rule:** unknown outcome is not failure and not success; it requires explicit reconciliation before retry/promotion.

### K8 — Epistemic & claim-state governance

**Responsibility:** govern what claims may be made from available evidence and prevent implementation/testing/deployment from being confused with validation or efficacy.

Current implementation evidence includes:

- canonical evidence ladder;
- claim-specific scope;
- evidence-strength monotonicity;
- verification/authorization non-equivalence;
- negative findings and uncertainty preservation;
- structural-epistemics claim validation.

**Primary artifacts:** `EPISTEMIC_EVIDENCE_STANDARD.md`, `dgaf_capability_evidence.py`, claim/evidence indexes and validators.

**Architectural rule:** evidence strength and authority are related but non-equivalent; weaker evidence must not widen authority.

## First-class assurance/support components

These are internal DGAF capabilities but should not be confused with the transactional governance kernel.

### A1 — Audit & quality governance

Owns audit inventory, meta-audit, claim hygiene, IP hygiene, regression/coverage controls, propagation consistency, and quality criteria.

### A2 — Provenance & custody assurance

Owns source/artifact identity, custody records, protected-lane controls, freeze evidence, evidence retention, and provenance parity.

### A3 — Documentation / semantic authority

Owns canonical vocabulary, architecture routing, current-state projection, document lifecycle, and stale/superseded-state handling.

### A4 — Operator / review control surfaces

Owns current-state, evidence, governance, state-space, and review presentation. These surfaces consume authority; they do not create it.

## Governed profiles built on the kernel

The following should be treated as **profiles / domain lifecycles**, not additional copies of DGAF itself:

- Track A / Epoch experimental lifecycles;
- AOSS Stage-A collection/replay/admission lifecycle;
- Mode-T assurance/deployment lifecycle;
- PDMAL experimental governance;
- external-review / independent-reproduction handoffs;
- self-application / cold-start validation;
- workload-specific evaluation tracks.

A profile may legitimately define stronger or domain-specific records, states, custody requirements, or transition guards.

## Convergence / duplication findings

### C1 — Authorization record proliferation: CONVERGENCE TARGET, not duplicate deletion

DGAF currently has generic authorization/action-admission concepts plus domain-specific authorization schemas for Track A and AOSS.

**Interpretation:** this is not automatically harmful duplication. Domain records encode different scientific/custody semantics.

**Desired convergence:** shared kernel fields and invariants should route through K1–K3 where semantics match; profiles should add only domain-specific fields/guards.

Do not replace profile-specific authorization records with AAR merely for uniformity.

### C2 — State-machine proliferation: SHARED ENGINE + PROFILE STATES

The generic capability state machine and Track/Epoch/AOSS lifecycle validators solve related but differently scoped problems.

**Desired convergence:** maintain one common transition vocabulary/invariant layer where possible; retain profile-specific state graphs where lifecycle semantics differ.

Do not flatten scientific lifecycle states into runtime transaction states.

### C3 — Evidence vocabulary overlap: NEEDS EXPLICIT MAPPING

The repository has the canonical evidence ladder plus narrower implementation-level evidence-strength enums.

**Desired convergence:** document a mapping/relationship rather than silently treating the enums as equivalent.

For example, `EvidenceStrength.VERIFIED` in one bounded module must not automatically mean repository-wide canonical `VERIFIED` without the required retained evidence record.

### C4 — Custody/freeze controls: PROFILE CAPABILITY, NOT UNIVERSAL KERNEL STEP

Track/Epoch and review workflows contain extensive custody/freeze machinery.

**Interpretation:** custody is first-class assurance infrastructure, but immutable dataset freeze is not a prerequisite for every DGAF-governed action.

**Desired convergence:** core custody primitives + profile-defined custody/freeze policies.

### C5 — Legacy persona/agent governance: RETIRED FROM CORE AUTHORITY

Named persona/agent identities have been migrated toward functional roles and retained provenance.

**Desired state:** role/capability identity remains orthogonal to runtime authority. Historical personas must not become an alternate authorization system.

### C6 — Historical framework/control-plane labels: DO NOT REVIVE AS PEER KERNELS

Historical labels such as NDR-SACP and other recovered architecture concepts should route useful mechanisms into the owning current component rather than recreate parallel control planes.

## Recommended internal architecture

```text
DGAF Governance Kernel
  K1 Action Canonicalization & Effect Identity
        ↓
  K2 Policy / Delegation / Effective Authority
        ↓
  K3 Admission & Enforcement
        ↓
  K4 Governed State-Transition Control
        ↓
  K5 Replay / Idempotency / Revocation / Trust
        ↓
  External Executor / Runtime (e.g. ACP)
        ↓
  K6 Execution Evidence & Provenance
        ↓
  K7 Postcondition / Recovery / Reconciliation
        ↓
  K8 Epistemic & Claim-State Governance

Cross-cutting assurance:
  A1 Audit & Quality
  A2 Provenance & Custody
  A3 Semantic / Documentation Authority
  A4 Operator / Review Surfaces
```

The arrows are explanatory ordering, not a claim that every profile executes every component in a single linear call chain.

## Immediate architecture work

1. Define a machine-readable **DGAF Core Component Registry** with stable IDs `K1–K8`, ownership, inputs/outputs, authority effects, and profile dependencies.
2. Map every current schema/script/controller to exactly one primary component and optional secondary dependencies.
3. Add explicit mapping between the repository evidence ladder and bounded implementation-level evidence enums.
4. Inventory authorization schemas and state machines for shared-kernel fields versus profile-specific fields.
5. Mark historical/retired mechanisms as aliases, provenance, or superseded rather than deleting evidence.
6. Use the registry to prevent new parallel authority engines from being added without an Architecture Decision Record.

## Non-effect

This inventory is architecture classification only. It does not merge components, modify runtime authority, authorize execution/collection, change scientific N, establish efficacy/independent validation, or authorize High-Assurance.
