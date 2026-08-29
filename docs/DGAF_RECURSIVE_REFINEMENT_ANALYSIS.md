# DGAF Framework — Recursive Refinement Analysis

**Document Version:** v3 (v1 control-plane alignment)  
**Original Draft Date:** 2026-02-15  
**Correction Date:** 2026-08-29  
**Authority:** Agent Amethyst  
**Reviewer lineage:** Apogee Lens + current DGAF control-plane architecture review  
**Status:** Working Design Reference — Gold Tier; executable v1 implementation remains pending

> **Scope correction:** This document is the design/rationale record for recursive refinement. The canonical executable v1 integration boundary is `docs/architecture/DGAF_V1_CONTROL_PLANE_INTEGRATION.md`. This file must not be treated as the runtime contract.

---

## DGAF Acronym Resolution

| Letter | Term | Function |
|---|---|---|
| **D** | Defense | Integrity protection, adversarial resistance, constraint enforcement |
| **G** | Governance | Authority ordering, protocol compliance, audit chain |
| **A** | Agentic | Multi-agent orchestration, role separation, delegation |
| **F** | Formation | Structural arrangement, agent topology |

Framework is a meta-level descriptor. No harmonic or geometric interpretation in this document changes the operational governance boundary.

---

## v1 recursive-refinement interpretation

The viable operational interpretation of recursion is **bounded adaptive refinement**.

A branch is created only when a governance envelope permits it and the branch has:

- a defined purpose;
- an evidence or uncertainty-reduction objective;
- a reserved budget;
- a legal inherited authority/tool/data scope;
- a progress criterion;
- a terminal condition.

The practical rule is:

```text
recursion is an available control-plane operation,
not a default right of an agent.
```

This supersedes earlier descriptions in this file that implied fixed repeated interchange loops or topology-specific recursion as the normal runtime behavior.

---

## Operational telescope

The earlier Macro/Mid/Tactical/Quantum terminology is retained only as historical conceptual framing. The v1 implementation uses a simpler control hierarchy:

```text
SYSTEM
  -> TASK
      -> BRANCH
          -> TURN
              -> GATE
                  -> ARTIFACT
```

The existing TGL operates at the **TURN/GATE** layer. The new v1 lifecycle controller operates at the **TASK/BRANCH** layer. PDMAL remains an optional execution topology beneath the branch/turn boundary.

---

## v1 bounded refinement loop

```text
RECEIVED
  |
  v
PREFLIGHT
  |
  +---- policy/authority failure ----> BLOCKED
  |
  v
ADMITTED
  |
  v
EXPANDING
  |
  +--> create bounded child branches
  |
  v
EVALUATING
  |
  +--> TGL gate evaluation
  +--> evidence reconciliation
  +--> resource accounting
  +--> progress test
  |
  +---- sufficient evidence ----> MERGE_READY
  |
  +---- hard veto -------------> ESCALATED / TERMINATED
  |
  +---- non-progress ----------> TERMINATED / ESCALATED
  |
  +---- evidence gap ----------> bounded next round, if budget remains
```

No recursive loop is valid without a remaining budget and a legal next state.

---

## Typed branch roles

The v1 default role set is:

| Role | Function | Failure condition |
|---|---|---|
| **EXPLOIT** | Improve the current candidate | Produces no meaningful improvement or violates scope |
| **DIVERGE** | Produce a materially different alternative | Repeats the same candidate or exceeds budget |
| **VERIFY** | Challenge claims, premises, and evidence | Fails to provide inspectable verification output |
| **GOVERN** | Test authority, policy, safety, and resource constraints | Detects a terminal violation or missing authorization |

Role labels do not imply independent reasoning. Independence must be assessed from provenance, source overlap, dependency overlap, and common assumptions.

---

## Recursion invariants

The operational recursion model must preserve:

```text
I1  child authority <= parent authority
I2  child tools    <= parent tools
I3  child data     <= parent data scope
I4  child budget   <= parent remaining budget
I5  every child has a progress criterion
I6  repeated/equivalent states cannot recurse indefinitely
I7  hard vetoes are terminal for ordinary recursion
I8  rejected/correlated branches remain inspectable
I9  consequential action remains behind the commit gate
I10 recursion cannot bypass TGL/P-35 governance
```

These are implementation invariants, not projected performance metrics.

---

## Resource-bounded recursion

The minimum runtime ceilings are:

```text
max_depth
max_nodes
max_rounds
max_concurrency
max_tool_calls
max_input_tokens
max_output_tokens
max_elapsed_ms
```

Resource measurement should use observed telemetry. Provider pricing may be reported separately but must not be the safety boundary.

The resource lifecycle is:

```text
REQUEST -> RESERVE -> CONSUME -> RELEASE/SETTLE
```

A failed atomic reservation prevents branch creation.

---

## State identity and cycle control

Each state should have a canonical identity derived from the governed state representation, including the relevant parent/branch context and policy version.

The identity mechanism is for:

- repeated-state detection;
- duplicate branch suppression;
- deterministic trace reconstruction.

It is **not** a semantic truth score.

---

## Evidence-preserving convergence

The system should not reduce the recursive lattice to one winner too early.

The convergence object should retain:

```text
accepted
corroborative
correlated
rejected
escalated
incomplete
```

A synthesis result therefore becomes a conclusion about retained artifacts rather than a replacement for them.

---

## Independence handling

The following metadata are appropriate for v1:

```text
source_overlap
dependency_overlap
prompt_lineage_overlap
model_identity
toolchain_identity
common_assumption_refs
```

A future statistical model may use these fields, but v1 must not claim that a numerical diversity score establishes independence.

---

## Relationship to PDMAL

PDMAL can inhabit the execution layer beneath this recursive controller:

```text
DGAF control plane
      |
      +--> governed branch
                |
                +--> PDMAL topology
```

The recursive controller must remain useful when PDMAL is absent. PDMAL remains an experimental substrate and does not define generic recursion semantics.

---

## Historical quantitative claims

Earlier versions of this document contained projected figures for throughput, phase coherence, refinement iterations, and scaling modes. Those figures are not runtime measurements and are not v1 acceptance criteria. They remain historical design targets only and should not be reused as evidence.

The previously corrected coordination-path calculation remains:

```text
n(n-1)/2
5 agents -> 10 unordered pairwise paths
4 agents -> 6 unordered pairwise paths
increase -> 66.7% (approximately 67%)
```

This combinatorial fact does not imply better orchestration quality.

---

## Deprecated v1 interpretations

The following are explicitly non-canonical for executable v1:

- fixed 10-cycle recursive interchange as a mandatory runtime loop;
- branch entropy as the admission condition;
- cosine distance as evidence independence;
- harmonic/geometric alignment as authorization logic;
- fixed pentagonal agent counts as a safety requirement;
- recursive depth as a quality metric by itself;
- consensus count as a truth estimator.

---

## Verification posture

The recursive-refinement subsystem should first be proven with deterministic mock branches. Required initial adversarial fixtures include:

1. normal four-role single-round execution;
2. correlated branches with overlapping sources;
3. GOVERN veto propagation;
4. budget reservation failure/overrun;
5. repeated-state recursion;
6. child authority escalation attempt;
7. tool-scope escalation attempt;
8. commit attempt without authorization;
9. partial branch failure with evidence retention;
10. TGL/P-35 failure propagation.

Only after these are verified should live-model/provider adapters be introduced.

---

## Canonical v1 reference

See:

- `docs/architecture/DGAF_V1_CONTROL_PLANE_INTEGRATION.md`
- `docs/architecture/DGAF_V1_FILE_TREE_PLAN.md`

Those files define the current v1 control-plane contract and file placement. This document supplies historical and conceptual rationale for recursive refinement only.
