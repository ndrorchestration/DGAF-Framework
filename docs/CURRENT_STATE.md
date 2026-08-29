---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-29
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` is the documentation/evidence lineage. The experimental verification boundary remains candidate-scoped at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. P7 is scientifically adopted in substance but formally open pending exact freeze binding; P8 remains open/fail-closed; empirical N = 0; authorization is not granted.

## Canonical engineering lane — 2026-08-29

PR #139 (`feat/dgaf-v1-control-plane-finalize-20260829`) is the canonical combined engineering candidate for the governed recursive control plane and TGL contract remediation. It is based on current `main` and remains non-authorizing.

The candidate includes `GovernanceEnvelope`, deterministic `ControlPlane`/`TaskState`, `StateRegistry`, `BudgetLedger`, `BranchRegistry`, `CommitGate`, hardened TGL status/sealing semantics, adversarial regression tests, and dedicated CI lanes. It does not rebind PDMAL, create a freeze, authorize a pilot, unblind data, or increase empirical N.

### TGL contract boundary

- required unwired gates are `SKIP` and reduce the turn to `ESCALATE`;
- `WARN` propagates to `TurnStatus.WARN` unless a stronger failure state applies;
- conditional HPG `SKIP` does not itself escalate when Phi-Closure did not pass;
- terminal `KILL` stops downstream gate execution;
- the final audit seal covers the complete gate set, including Herald;
- invalid gate outcomes do not silently become PASS.

### Canonical agent-role boundary

The current Notion agent registry is authoritative for role identity/intent, while GitHub remains implementation/evidence truth.

- Sentinel-Phi — canonical governance/security identity; `Sentinel` is historical alias only.
- Professor Prodigy — formalization/proof/category discipline; non-orchestrating.
- DemiJoule — advisory resource/constraint analysis; no independent normative authorization.
- Reciprocity — fairness, affected-party, reciprocal-impact, perspective-equity, and asymmetry analysis.
- Herald — evidence/public-surface publication and classification; cannot manufacture evidence or approval.
- Amethyst — meta-orchestration/lifecycle coordination.
- COLLEEN — continuity, archive, provenance, durable-state, and routing integrity.
- Apogee — independent evidence/integrity review and loop validation.

Generic v1 roles are execution contracts and do not create or elevate agent authority.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` | CURRENT DOCUMENTATION/EVIDENCE LINEAGE | Resolve `main` directly for latest repository state |
| Experimental verification boundary | CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| P7 scientific specification | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Exact freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped closure incomplete |
| P2 runtime verification | NOT EXECUTED | Authenticated exact deployment matrix required |
| P6a CORS verification | NOT EXECUTED | Authenticated exact deployment matrix required |
| New immutable freeze | NOT CREATED | No candidate has crossed freeze boundary |
| Pilot authorization | NOT GRANTED | Explicit separate governance transition required |
| Empirical data | N = 0 | No authorized pilot has executed |

## Deployment identity boundary

The observed READY Vercel production deployment remains historical/supporting evidence because its source SHA `42346ecc34565502ebff02ead55a33b0d74246b8` does not equal the current GitHub `main` SHA. Issue #137 remains the canonical deployment-provenance tracker. A READY preview does not establish exact-current-main production identity.

## Engineering-lane consolidation

PR #132/#133 are historical diagnostic/remediation records. PR #134 is superseded by PR #139. PR #139 is the single current engineering lane for the v1 recursive control plane plus the TGL contract remediation.

## Evidence boundary

CI success, deterministic tests, deployment readiness, synthetic evaluator results, governance documentation, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Historical evidence remains exact-SHA/run/deployment scoped.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
