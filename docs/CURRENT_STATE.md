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

The viable implementation-oriented subset of the Governed Recursive Lattice / compiler-trace proposal is now **mapped and implemented as a candidate engineering layer** in the existing `pptl/` tree.

Candidate modules:

- `pptl/governance_envelope.py`
- `pptl/control_plane.py`
- `pptl/state_identity.py`
- `pptl/budget_ledger.py`
- `pptl/branch_registry.py`
- `pptl/commit_gate.py`
- `pptl/tests/test_v1_control_plane.py`
- `.github/workflows/control-plane-contract.yml`

The canonical architecture and placement records are:

- `docs/architecture/DGAF_V1_CONTROL_PLANE_INTEGRATION.md`
- `docs/architecture/DGAF_V1_FILE_TREE_PLAN.md`

These modules remain implementation candidates pending exact-head CI and adversarial review; source presence is not equivalent to verified merge-level capability.

The v1 control plane does not alter PDMAL candidate identity, protocol, freeze state, authorization state, or empirical N.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| Current `main` | CURRENT DOCUMENTATION/EVIDENCE LINEAGE | Resolve `main` directly; not apparatus identity |
| Experimental verification boundary | CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| Current-boundary E2b | OPEN / VERIFICATION REQUIRED | Exact executing boundary required for later freeze admissibility |
| M6 | CLOSED / VERIFIED (candidate exact-tree scope) | `ac8ea267…`; run `33050398324` |
| TGL contract | REMEDIATION IMPLEMENTATION CANDIDATE | PR #134 current-main repair; exact-head CI/adversarial validation required |
| DGAF v1 control-plane | IMPLEMENTATION CANDIDATE / NON-AUTHORIZING | PR #136 contains candidate contracts, tests, CI, and architecture mapping |
| P7 scientific specification | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Exact freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped verification remains incomplete |
| P2 formal runtime verification | NOT EXECUTED | Authenticated five-case matrix required |
| P6a formal CORS verification | NOT EXECUTED | Authenticated CORS matrix required |
| New immutable freeze | NOT CREATED | No current candidate crossed freeze boundary |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized empirical pilot executed |

## Architectural relationship

```text
DGAF governance / evidence plane
            |
            v
     v1 Control Plane
            |
     +------+------+
     |      |      |
   TGL    Budget  Evidence
     |      |      |
     +------+------+
            |
     governed adapter
            |
      PDMAL or other
       execution substrate
```

TGL remains the per-turn governance kernel. The v1 control plane governs task lifecycle, scope inheritance, bounded recursion, state identity, resources, branch provenance, and consequential-action authorization around it.

## Experimental boundary

The v1 control-plane lane is a separate engineering path. It does not establish PDMAL efficacy, topology superiority, production reliability, freeze eligibility, pilot authorization, or empirical evidence.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
