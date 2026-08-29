# DGAF v1 Control-Plane Integration

**Status:** PLANNING / NON-AUTHORIZING  
**Date:** 2026-08-29  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Base planning boundary:** `main` @ `f61f01eee0c1edf33a70a95e6dc3447847e244f3`  
**Purpose:** Consolidate the viable portions of the Governed Recursive Lattice / compiler-trace proposal into the DGAF v1 architecture without rebinding the PDMAL experimental apparatus or changing authorization state.

## 1. Architectural decision

DGAF v1 should absorb the **governance-execution primitives** of the proposed system, not the speculative or experimentally unvalidated topology logic.

The v1 control plane therefore adds five concrete capabilities around the existing DGAF/TGL stack:

1. **Governance Envelope** — explicit authority, tool, data, risk, side-effect, and resource limits.
2. **Lifecycle State Machine** — deterministic task/branch states above the TGL per-turn gate sequence.
3. **Bounded Recursive Dispatch** — depth, node, round, concurrency, tool-call, token, and elapsed-time ceilings.
4. **Evidence/Provenance Branch Records** — durable branch identity, claims, evidence, assumptions, uncertainty, policy result, resource usage, and lineage.
5. **Plan/Commit Separation** — consequential actions remain proposals until a separately authorized commit phase.

These are control-plane features. PDMAL remains a selectable execution substrate / experimental topology and is not redefined by this planning document.

## 2. Existing DGAF assets to reuse

DGAF already provides the strongest parts of the required foundation:

| Existing asset | v1 reuse |
|---|---|
| `pptl/triadic_governance_loop.py` | Per-turn governance kernel / status reduction / audit seal boundary |
| `pptl/procluding_premise.py` | Layer-0 constitutional admission and fail-closed P-35 behavior |
| `pptl/orchestrator.py` | Existing orchestration integration point; extend rather than replace |
| `pptl/co_orchestration_schema.py` | Existing multi-agent/co-orchestration schema surface to reconcile with branch records |
| `pptl/herald_agent.py` + sinks | Evidence fan-out / operational publication boundary |
| `docs/CLAIM_EVIDENCE_INDEX.md` | Claim-to-evidence governance spine |
| `docs/CURRENT_STATE.md` | Authoritative current-state narrative, not apparatus identity |
| `docs/DGAF_RECURSIVE_REFINEMENT_ANALYSIS.md` | Historical/design source for recursion concepts; does not define executable v1 by itself |
| `docs/DGAF_RELATED_WORK_MATRIX.md` | Prior-art and overlap boundary |
| Existing CI/evidence controls | Verification and provenance rather than narrative assertion |

## 3. v1 control-plane model

```text
DGAF GOVERNANCE ENVELOPE
        |
        v
TASK LIFECYCLE CONTROLLER
 RECEIVED -> PREFLIGHT -> ADMITTED
        |                  |
        |                  +--> BLOCKED / ESCALATED
        v
  EXPANDING
        |
        v
BOUNDED BRANCH DISPATCH
  |      |      |      |
  v      v      v      v
EXPLOIT DIVERGE VERIFY GOVERN
  |      |      |      |
  +------+------+------+
         |
         v
     EVALUATING
         |
         +------> TGL / governance gates
         |
         +------> evidence/provenance records
         |
         +------> resource accounting
         |
         v
 MERGE_READY / ESCALATED / TERMINATED
         |
         v
  COMMIT GATE (separate)
```

### TGL relationship

The lifecycle controller and TGL have different scopes:

- **Lifecycle controller:** governs whether a task may exist, expand, recur, merge, escalate, terminate, or enter commit.
- **TGL:** governs the ordered gate evaluation inside an execution turn.
- **P-35:** remains the constitutional Layer-0 gate.
- **Herald:** remains evidence/fan-out infrastructure and must remain on the correct side of the sealed audit boundary.

No replacement of TGL is proposed.

## 4. Governance Envelope

The envelope is the canonical inherited contract for every root task and child branch.

Minimum v1 fields:

```json
{
  "trace_id": "...",
  "task_id": "...",
  "parent_task_id": null,
  "authority_scope": [],
  "permitted_tools": [],
  "data_classes": [],
  "risk_tier": "low|medium|high|critical",
  "side_effect_mode": "PROPOSE_ONLY|AUTHORIZED_COMMIT",
  "limits": {
    "max_depth": 0,
    "max_nodes": 0,
    "max_rounds": 0,
    "max_concurrency": 0,
    "max_tool_calls": 0,
    "max_input_tokens": 0,
    "max_output_tokens": 0,
    "max_elapsed_ms": 0
  },
  "policy_version": "...",
  "escalation_target": "..."
}
```

### Inheritance invariants

```text
authority_child ⊆ authority_parent
tools_child    ⊆ tools_parent
data_child     ⊆ data_parent
budget_child   ≤ budget_parent.remaining
```

A v1 implementation must reject an attempted child expansion that violates any inherited scope constraint.

## 5. Lifecycle state machine

Required v1 states:

```text
RECEIVED
PREFLIGHT
ADMITTED
EXPANDING
EVALUATING
MERGE_READY
ESCALATED
TERMINATED
COMMIT_READY
COMMITTED
```

The transition relation must be explicit. Illegal transitions fail closed.

### Terminal rules

- `ESCALATED` is terminal for the current ordinary execution branch unless an explicit re-entry policy exists.
- `TERMINATED` cannot be revived by a child branch.
- `COMMIT_READY` does not execute an external side effect.
- `COMMITTED` is reserved for the separately authorized commit mechanism.
- A hard governance veto cannot be converted into ordinary recursive refinement by a sibling or synthesis agent.

## 6. Bounded recursive dispatch

v1 recursion is deterministic and quota-driven.

Required controls:

- maximum depth;
- maximum total nodes;
- maximum rounds;
- maximum concurrent branches;
- maximum tool calls;
- maximum input/output tokens;
- maximum elapsed time;
- canonical state identity / repeated-state detection;
- explicit progress criterion.

A child requires all of the following:

```text
purpose
success condition
termination condition
parent trace
inherited governance envelope
reserved budget
```

No branch may be created solely because a model requests another round.

## 7. Typed v1 roles

The first implementation should use four role contracts:

| Role | V1 objective | Required output focus |
|---|---|---|
| `EXPLOIT` | Improve the current candidate | incremental improvement + rationale |
| `DIVERGE` | Produce a materially different alternative | alternative hypothesis/plan + difference declaration |
| `VERIFY` | Challenge premises and evidence | verification findings + evidence links + uncertainty |
| `GOVERN` | Test authority, policy, safety, and resource constraints | policy verdict + veto/escalation rationale |

These are role contracts, not guarantees of independent reasoning.

## 8. Evidence and provenance model

Every branch should produce one durable `BranchRecord` conceptually containing:

```text
branch_id
parent_branch_id
trace_id
role
input_refs
tool_refs
claims
evidence_ids
assumptions
uncertainty
policy_verdict
resource_usage
state_transition_refs
merge_status
provenance
seal
```

The system must retain rejected, correlated, incomplete, and vetoing branches rather than retaining only the synthesized winner.

### Independence metadata

v1 may record:

```text
source_overlap
dependency_overlap
prompt_lineage_overlap
model_identity
toolchain_identity
common_assumption_refs
```

It must **not** convert these fields into an unvalidated mathematical independence score that is then treated as proof.

## 9. Plan / commit boundary

All action-capable tooling should be split into:

```text
PROPOSE
  -> GOVERN
  -> VERIFY
  -> AUTHORIZE
  -> COMMIT
```

A proposal may be inspected, rejected, revised, or escalated without performing the side effect.

The commit mechanism must require an explicit authorization artifact or policy condition distinct from ordinary model output.

## 10. v1 status semantics

The orchestration controller and TGL should share a common fail-closed ordering without collapsing their meanings:

```text
KILL > ESCALATE > WARN > PASS
```

`SKIP` is not a terminal lifecycle status; it is a gate/result condition whose effect depends on whether the gate is required or conditionally suppressed.

This matches the current TGL remediation direction: required unwired gates cannot silently yield PASS, dependency-caused HPG SKIP is distinguishable from unwired required gates, and the returned audit object must be sealed after the complete gate set exists.

## 11. Resource accounting

v1 resource control should use **actual telemetry**, not estimated dollar values.

Minimum ledger dimensions:

```text
input_tokens
output_tokens
tool_calls
elapsed_ms
active_branches
```

The reservation model should be conservative:

```text
requested <= parent.remaining
reservation is atomic
consumption is recorded
unspent reservation is releasable
overrun is terminal/escalating
```

Provider-specific pricing can be added later as reporting metadata and must not become the core safety boundary.

## 12. What is explicitly deferred

The following are not v1 control-plane primitives:

- semantic-diversity metrics used as independence proof;
- learned sycophancy classifiers as authoritative gates;
- adaptive topology optimization;
- automatic confidence increases from branch consensus;
- autonomous policy learning;
- geometry/harmonic features as authorization signals;
- PDMAL topology selection as a governance decision;
- empirical claims that a particular topology improves intelligence or reliability.

These may be separate research lanes after the control substrate is executable.

## 13. DGAF greater file tree placement

The intended future layout is:

```text
DGAF-Framework/
├── .github/
│   └── workflows/
│       ├── pptl-ci.yml
│       └── [future control-plane verification workflows]
├── docs/
│   ├── architecture/
│   │   ├── DGAF_V1_CONTROL_PLANE_INTEGRATION.md        # this document
│   │   ├── DGAF_V1_FILE_TREE_PLAN.md                   # implementation placement map
│   │   └── [later architecture decisions]
│   ├── governance/
│   │   ├── P1_TO_P9_EVIDENCE_MATRIX.md
│   │   ├── CURRENT_STATE.md (rooted at docs/)
│   │   └── [existing governance records]
│   ├── experiment/
│   │   └── [PDMAL protocol/evidence; remains experimentally scoped]
│   └── evidence/
│       └── [claim/evidence artifacts]
├── pptl/
│   ├── orchestrator.py                                 # lifecycle integration point
│   ├── triadic_governance_loop.py                      # per-turn gate kernel
│   ├── procluding_premise.py                           # constitutional gate
│   ├── co_orchestration_schema.py                      # schema reconciliation point
│   ├── [future control_plane.py]                       # lifecycle state machine
│   ├── [future governance_envelope.py]                 # inherited scope contract
│   ├── [future branch_registry.py]                     # branch/provenance ledger
│   ├── [future budget_ledger.py]                       # resource accounting
│   ├── [future commit_gate.py]                         # plan/commit barrier
│   └── [future state_identity.py]                      # cycle/repeated-state control
├── scripts/
│   └── [future deterministic control-plane validators]
└── tests/
    └── [future integration tests, where repository conventions permit]
```

### Placement rule

Do not create a parallel `pdmall/`, `recursive_lattice/`, or separate governance runtime tree inside DGAF merely to house this concept. The v1 architecture belongs in the existing `pptl/` control plane with documentation under `docs/architecture/`. PDMAL experimental machinery remains under its existing `experiments/` / `docs/experiment/` boundaries.

## 14. Implementation order

### Phase A — schemas and contracts

Create:

1. `GovernanceEnvelope`
2. `TaskState` / transition definitions
3. `BranchRecord`
4. `BudgetLedger`
5. `CommitRequest` / authorization contract

No LLM dependency.

### Phase B — deterministic controller

Implement:

1. admission/preflight;
2. legal state transitions;
3. inherited scope validation;
4. branch creation;
5. cycle detection;
6. terminal veto propagation;
7. bounded resource accounting.

### Phase C — TGL integration

Route lifecycle evaluation through the existing TGL without changing PDMAL experimental treatment semantics.

Required assertions:

- lifecycle cannot bypass P-35;
- TGL KILL propagates upward;
- required TGL SKIP prevents successful merge;
- audit/provenance records retain branch lineage;
- Herald fan-out occurs only at the defined evidence boundary.

### Phase D — deterministic mock harness

Build the following five fixtures:

1. normal four-role single-round execution;
2. correlated VERIFY/EXPLOIT branches;
3. GOVERN veto;
4. budget overrun;
5. repeated-state recursion.

Each fixture must produce an inspectable trace.

### Phase E — real model/tool adapters

Only after A–D pass should LLM and real-tool adapters be introduced.

## 15. Acceptance criteria for v1

The control plane is not v1-complete until it can demonstrate:

- child authority never exceeds parent authority;
- child tools/data never exceed parent scope;
- branch budgets cannot exceed remaining parent reservation;
- illegal state transitions fail closed;
- hard vetoes terminate ordinary recursion and remain visible in the final trace;
- repeated states terminate rather than recurse indefinitely;
- all branch artifacts remain reconstructable;
- correlated agreement is recorded as correlated rather than automatically amplified;
- no external action crosses from proposal to commit without the separate commit gate;
- the complete run can be reconstructed from its trace and retained branch records;
- all of the above are tested deterministically before live-model integration.

## 16. Experimental boundary

This architecture plan is **not experimental PDMAL evidence**.

It does not:

- create a new PDMAL apparatus candidate;
- alter the existing experimental candidate identity;
- change the PDMAL protocol or statistical plan;
- grant pilot authorization;
- create a freeze;
- generate empirical observations;
- promote conceptual topology properties to validated claims.

The existing experimental evidence and authorization boundaries remain authoritative.

## 17. Documentation hygiene rule

This document is the canonical v1 integration map. Future changes should update it rather than creating another overlapping architecture essay.

Use existing documents for their existing jobs:

- current state → `docs/CURRENT_STATE.md`;
- P1–P9 evidence → `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md`;
- prior art → `docs/DGAF_RELATED_WORK_MATRIX.md`;
- historical recursive-refinement rationale → `docs/DGAF_RECURSIVE_REFINEMENT_ANALYSIS.md`;
- implementation/test truth → repository code and CI.

Add a new document only when it introduces a distinct control artifact, API contract, experiment protocol, or independent evidence class.
