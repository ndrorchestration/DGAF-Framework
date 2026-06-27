# P-LOCK-001 — Ionian Lock (Bounded Execution Seal)

**Family:** Concurrency & Consistency  
**Cadence type:** Seal-before-yield  
**Status:** Draft / pending Apogee Lens review  
**Session:** S067  
**Registered:** 2026-06-26

---

## Intent

Guarantee that at most one **resolution path** holds active write authority over a **bound resource** at any moment, by requiring every execution context to emit a **seal signal** before it yields, suspends, or delegates — and requiring every successor context to verify the seal before acquiring authority.

The pattern is named for the harmonic property of the Ionian mode: every step resolves back to tonic before progressing. No note is left hanging. No context is left open.

---

## Motivation

When an execution context suspends mid-operation — due to a handoff, an asynchronous wait, a checkpoint, or a failure recovery — there is a window in which two contexts can simultaneously believe they hold authority over the same bound resource. This is the **double-authority gap**. Conventional locking schemes close this gap for synchronous execution but leave it open across:

- Async yield points (awaited work units, deferred callbacks)
- Agent handoffs (one reasoning loop passing a task to another)
- Checkpoint/resume boundaries (durable execution restores)
- Cross-runtime delegation (one execution environment invoking another)

The Ionian Lock closes this gap by treating the seal signal as a **first-class causal artifact** — not a side effect of a lock release, but an explicit, observable, durable emission that downstream contexts must consume before proceeding.

---

## Structure

The cadence has four mandatory phases. Each phase has an observable artifact. No phase may be skipped.

| Phase | Name | Actor | Artifact emitted |
|---|---|---|---|
| 1 | **Claim** | Initiating context | `authority-token` (scoped to bound resource + session) |
| 2 | **Work** | Initiating context | Zero or more `state-delta` records (append-only) |
| 3 | **Seal** | Initiating context | `seal-record` (contains final-state hash, authority-token ref, yield reason) |
| 4 | **Acquire** | Successor context | `acquire-record` (references seal-record, asserts no gap) |

A **gap assertion failure** in Phase 4 means the successor found no valid seal-record from the prior authority holder — the work was not cleanly sealed. The successor must **halt and surface** rather than proceed with stale or ambiguous state.

---

## Substrate-Agnostic Vocabulary

The pattern deliberately avoids implementation-specific terms. Mappings for common substrates:

| DGAF term | Temporal/Workflow | Agent framework | Database/Queue | File/Git |
|---|---|---|---|---|
| Bound resource | Workflow instance | Agent task | Row / partition | Branch / file |
| Execution context | Activity function | Reasoning loop | Transaction | Commit session |
| Authority token | Workflow lock | Task assignment | Row lock / lease | Exclusive checkout |
| State delta | History event | Observation log | WAL entry | Diff/patch |
| Seal record | Checkpoint commit | Handoff emission | Commit record | Signed commit |
| Acquire record | Resume signal | Task acceptance | Lock acquisition | Pull / rebase |
| Gap assertion | Replay guard | Continuity check | Isolation check | Conflict detection |

---

## Invariants

Three invariants must hold throughout the cadence. Any system implementing this pattern must be able to assert all three at any point in time:

1. **Single-authority invariant** — For any bound resource, at most one authority token is active at any instant. A new token cannot be issued until the prior token's seal-record is durably committed.

2. **Causal-seal invariant** — Every seal-record contains a cryptographically or logically sufficient reference to the final state at seal time, such that any observer can verify the state has not been modified between seal emission and acquire.

3. **No-silent-yield invariant** — An execution context may not terminate, suspend, time out, or error without either emitting a valid seal-record or triggering a **contested-seal escalation** (see Failure Modes below).

---

## Failure Modes & Compensations

| Failure | Detection point | Compensation |
|---|---|---|
| **Missed seal** — context terminated without sealing | Phase 4 gap assertion | Contested-seal escalation: surface to HITL or trigger P-CB-001 |
| **Stale authority** — successor acquired before seal committed | Phase 4 causal-seal check | Reject acquire, force re-seal from last known good state |
| **Duplicate seal** — two contexts both sealed the same resource | Seal-record deduplication | Retain earlier seal by causal timestamp; invalidate later |
| **Phantom seal** — seal emitted but state delta is empty | Validation at Phase 3 | Warn, allow only if yield-reason is `no-op-confirmed` |
| **Gap under recovery** — context restored from checkpoint but seal predates latest delta | Replay guard | Reject restore, re-derive state from delta log before acquiring |

---

## Relationship to Other Patterns

- **P-CB-001 (Circuit Breaker / HITL)** — Contested-seal escalation routes through P-CB-001 when automatic resolution is not safe. The Ionian Lock surfaces the gap; the circuit breaker decides whether to halt or escalate to human authority.
- **P-DURABLE-001 (Append-Only Log)** — State deltas and seal-records are durable log entries. The Ionian Lock requires P-DURABLE-001 as its persistence substrate.
- **P-SAGA-001 (Stochastic-Deterministic Saga Boundary)** — In a saga, each saga step is itself a bound resource. The Ionian Lock governs the seal between saga steps; P-SAGA-001 governs the boundary between stochastic and deterministic phases within each step.
- **P-TX-001 (Transactional Tool Boundary / Atomix)** — Atomix defines the atomic boundary of a tool invocation. The Ionian Lock operates one level above Atomix: it governs the seal between tool invocations within an execution context, not the atomicity of a single invocation.
- **NDR_PHI_CLOSURE_GATE_v1 (P-32)** — Phi Closure Gate is the Ionian Lock applied specifically to Phi Knight reasoning loops. The Lock is the general pattern; Phi Closure is the NDR-scoped instance.

---

## Usage Note for DGAF Orchestration

Within the DGAF framework, every agent handoff — including Amethyst → DemiJoule, DemiJoule → Apogee Lens, and any CO_ORCH delegation — is a Phase 3 → Phase 4 transition. The handoff is only valid if:

1. The delegating agent has emitted a seal-record into the session's durable log
2. The receiving agent asserts the seal-record before accepting the task assignment
3. No other agent has issued an acquire-record against the same session

This is why the CO_ORCH_PROTOCOL requires explicit handoff acknowledgments rather than implicit task pickup — those acknowledgments are the acquire-records mandated by Phase 4 of this cadence.

---

## Apogee Lens Review

- [ ] Invariants formally verified against P-DURABLE-001 log guarantees
- [ ] Failure mode compensations cross-checked against P-CB-001 escalation paths
- [ ] Substrate mapping table validated against at least two live substrates
- [ ] Promotion to `STABLE` pending attestation
