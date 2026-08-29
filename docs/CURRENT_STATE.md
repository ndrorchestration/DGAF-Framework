---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-29
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` remains the documentation/evidence lineage. PR #139 is the current engineering candidate at `250de1c76e4dfd105207523ae2e46aa83b5a5153`. The experimental verification boundary remains candidate-scoped; P7 is scientifically adopted in substance but formally open pending exact freeze binding; P8 remains open/fail-closed; empirical N = 0; authorization is not granted.

## Canonical engineering lane — 2026-08-29

PR #139 (`feat/dgaf-v1-control-plane-finalize-20260829`) is the canonical combined engineering candidate for the governed recursive control plane and TGL contract remediation.

**Current PR #139 head:** `250de1c76e4dfd105207523ae2e46aa83b5a5153`

The candidate includes `GovernanceEnvelope`, deterministic `ControlPlane`/`TaskState`, `StateRegistry`, `BudgetLedger`, `BranchRegistry`, `CommitGate`, hardened TGL status/sealing semantics, adversarial regression tests, capability-boundary tests, and dedicated CI lanes. It does not rebind PDMAL, create a freeze, authorize a pilot, unblind data, or increase empirical N.

### Current engineering invariants

- governance scope can only remain equal or narrow across child derivation;
- task identity and controller-managed runtime state cannot be externally reassigned;
- public task/ledger/registry/event surfaces are read-only;
- merge readiness requires a current sealed TGL `PASS`;
- terminal/escalated tasks cannot consume additional resources;
- child state identity is observed after successful `PREFLIGHT` submission;
- failed child creation cannot pollute the state registry;
- branch provenance preserves distinct branch identities when state IDs coincide;
- CommitGate remains a separate explicit authorization boundary;
- safe terminal abort does not create an authorization path.

### TGL contract boundary

- required unwired gates are `SKIP` and reduce the turn to `ESCALATE`;
- `WARN` propagates to `TurnStatus.WARN` unless a stronger failure state applies;
- conditional HPG `SKIP` does not itself escalate when Phi-Closure did not pass;
- terminal `KILL` stops downstream gate execution;
- the final audit seal covers the complete gate set, including Herald;
- invalid gate outcomes do not silently become PASS.

### Exact-head engineering verification

The dedicated `DGAF v1 Control-Plane Contract` run `33246694071` completed **SUCCESS** on the implementation checkpoint `7807d956e90d4e5fec79fcbe2146618c815fed51`. Exact candidate checkout passed, pinned CI dependency installation passed, and the deterministic control-plane/TGL/adversarial/capability-boundary suite passed **40/40**.

Subsequent branch commits through the current PR head are documentation/governance reconciliation commits; no claim is made that the 40/40 result verifies a later code SHA unless that later SHA contains only those non-code changes.

Additional successful engineering/evidence lanes included Truth Layer Tests/Validation, Full Repository Coverage Audit, PDMAL Instrumentation Dry Run, Epistemic Evidence Validation, and CodeQL. These are engineering/evidence controls, not experimental efficacy evidence.

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
| PR #139 engineering candidate | VERIFIED ENGINEERING CANDIDATE | `250de1c76e4dfd105207523ae2e46aa83b5a5153`; last substantive code verification checkpoint `7807d956…` |
| P7 scientific specification | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Exact freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped closure incomplete |
| P2 runtime verification | OPEN / NOT EXECUTED | Exact-source deployment and authenticated runtime matrix still required |
| P6a CORS verification | OPEN / NOT EXECUTED | Exact-source deployment and authenticated runtime matrix still required |
| New immutable freeze | NOT CREATED | No candidate has crossed freeze boundary |
| Pilot authorization | NOT GRANTED | Explicit separate governance transition required |
| Empirical data | N = 0 | No authorized pilot has executed |

## Deployment identity boundary

The observed READY Vercel production deployment remains historical/supporting evidence because its source SHA `42346ecc34565502ebff02ead55a33b0d74246b8` does not equal current `main`. Issue #137 is the canonical deployment-provenance tracker.

For the verified implementation checkpoint `7807d956…`, GitHub reported the Vercel status context **success**; available GitHub-side evidence does not expose deployment metadata proving exact source-SHA identity. For the later current PR head, deployment provenance remains open and is not inherited from the earlier status.

## Engineering-lane consolidation

PR #132/#133/#134 are historical diagnostic/remediation records. PR #139 is the single current engineering lane for the v1 recursive control plane plus the TGL contract remediation.

## Evidence boundary

CI success, deterministic tests, deployment readiness, synthetic evaluator results, governance documentation, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Historical evidence remains exact-SHA/run/deployment scoped.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
