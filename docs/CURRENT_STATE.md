---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-29
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **Current boundary:** `main` is the current documentation/evidence lineage boundary. The experimental verification boundary remains candidate-scoped at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. P7 is scientifically adopted in substance but formally open pending exact freeze binding; P8 remains open/fail-closed; empirical N = 0; authorization is not granted.

## DGAF v1 control-plane lane

The viable implementation-oriented subset of the Governed Recursive Lattice / compiler-trace proposal is now **implemented as a candidate engineering layer** in the existing `pptl/` tree.

Candidate modules:

- `pptl/governance_envelope.py`
- `pptl/control_plane.py`
- `pptl/state_identity.py`
- `pptl/budget_ledger.py`
- `pptl/branch_registry.py`
- `pptl/commit_gate.py`
- `pptl/tests/test_v1_control_plane.py`
- `pptl/tests/test_v1_tgl_integration.py`
- `.github/workflows/control-plane-contract.yml`

The current implementation includes inherited authority/tool/data/resource constraints, explicit recursion depth bounds, deterministic lifecycle transitions, exact-state cycle detection, branch provenance retention, explicit plan/commit separation, and optional TGL invocation from the lifecycle evaluation state.

The canonical architecture and placement records are:

- `docs/architecture/DGAF_V1_CONTROL_PLANE_INTEGRATION.md`
- `docs/architecture/DGAF_V1_FILE_TREE_PLAN.md`

The implementation is still a candidate pending exact-head CI and adversarial review. Source presence and authored tests do not by themselves establish verified merge-level capability.

The v1 control plane does not alter PDMAL candidate identity, protocol, freeze state, authorization state, or empirical N.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b868…` remains provenance only |
| Current `main` | CURRENT DOCUMENTATION/EVIDENCE LINEAGE | Resolve `main` directly; not apparatus identity |
| Experimental verification boundary | CANDIDATE-SCOPED | `ac8ea267…` |
| TGL contract | REMEDIATION CANDIDATE | PR #134; exact-head validation pending |
| DGAF v1 control-plane | IMPLEMENTATION CANDIDATE | PR #136; deterministic contracts + TGL integration coverage added |
| P7 scientific specification | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Exact freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped closure pending |
| P2 formal runtime verification | NOT EXECUTED | Authenticated five-case matrix required |
| P6a formal CORS verification | NOT EXECUTED | Authenticated matrix required |
| New immutable freeze | NOT CREATED | No current candidate has crossed freeze boundary |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## Verification boundary

The v1 control-plane CI workflow is a deterministic engineering-validation lane. It is not an experimental authorization mechanism, and it does not close P1–P9 merely by passing.

The separate `ndrorchestration/agent-control-plane` repository remains an external reference/integration asset rather than an implicit dependency.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
