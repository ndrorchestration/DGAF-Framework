---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-30
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` is the current documentation/evidence lineage. The integrated DGAF v1 engineering/production source is `303f4424d2198f0d0cf76305c589263dd1e417dc`. The designated PDMAL pre-freeze candidate is `c6157158bf0ee4840e99a381a4b99bd2febe2302`; its Vercel production deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` is READY and exact SHA-bound. Prior P2/P6a runtime evidence remains exact for `303f4424…` and has not been transferred to `c6157158…`. P7 is adopted in substance but formally open pending exact freeze binding; P8 remains open/fail-closed; empirical N = 0; authorization is not granted.

## Current engineering/control-plane source

`303f4424d2198f0d0cf76305c589263dd1e417dc` is the integrated DGAF v1 engineering/production source. It remains the exact source identity for the prior verified production deployment and prior P2/P6a runtime evidence. This engineering identity is not itself a freeze declaration.

The earlier PR #139 engineering candidate records remain useful implementation provenance. They must not be interpreted as replacing the current mainline or as experimental freeze evidence unless an exact current predicate is re-established.

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
- invalid gate outcomes do not silently become PASS;
- final status is reduced again after Herald, so a Herald `WARN`/`KILL` cannot be hidden by an earlier `PASS`.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` | CURRENT DOCUMENTATION/EVIDENCE LINEAGE | `0ced2b0126a89c80acb89228e9a1b4478c276289`; resolve `main` directly for latest repository state |
| Engineering/production source | VERIFIED | `303f4424…`; integrated DGAF v1 source and exact source of prior production deployment |
| Designated pre-freeze PDMAL candidate | DESIGNATED / NOT FROZEN | `c6157158…` on `experimental-candidate/2026-08-30-reconciled` |
| Candidate deployment provenance | VERIFIED | `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`; READY; Vercel Git SHA exactly matches `c6157158…` |
| P2 runtime verification | PRIOR VERIFIED / CURRENT CANDIDATE OPEN | Run `33300481208` is exact evidence for `303f4424…`; fresh current-candidate execution remains required |
| P6a CORS verification | PRIOR VERIFIED / CURRENT CANDIDATE OPEN | Run `33302495240` is exact evidence for `303f4424…`; fresh current-candidate execution remains required |
| P3 Artifact Contract | IMPLEMENTED / OPEN | Fresh candidate-scoped execution evidence required |
| P4 Security / Blinding | OPEN | Operational custody/separation evidence required |
| P5 Provenance / Reproducibility | OPEN | Candidate-bound environment/topology/RNG evidence required |
| P6 Durable Evidence Custody | BLOCKED / OPEN | End-to-end archive/retrieval/hash proof required |
| P7 Scientific Target | ADOPTED / BINDING PENDING | Exact protocol/apparatus/analysis/freeze binding required |
| P8 Analysis Lock | OPEN / FAIL-CLOSED | Candidate-scoped closure incomplete |
| P9 Independent Verification | NOT EXECUTED | Independent reproduction/audit required |
| New immutable freeze | NOT CREATED | No candidate has crossed the freeze boundary |
| Pilot authorization | NOT GRANTED | Separate explicit governance transition required |
| Empirical data | N = 0 | No authorized pilot has executed |

## Candidate identity and evidence boundary

The historical identity discrepancy among `2a80f819…`, `303f4424…`, and the `main` lineage has been reconciled. `2a80f819…` is an earlier P8 checklist ancestor; `303f4424…` is the integrated engineering/production source; `ac8ea267…` is a prior experimental verification boundary; and `c6157158…` is the explicitly designated current pre-freeze candidate.

P2 run `33300481208` and P6a run `33302495240` remain exact, valid evidence for `303f4424…` and deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`. They do not become evidence for `c6157158…` merely because the candidate is a descendant or shares the same engineering lineage.

## Deployment identity boundary

The designated candidate deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` is READY and records exact Vercel Git source SHA `c6157158…`. This closes candidate deployment/source provenance only. It does not close P2/P6a runtime predicates, P3–P6, P8, or P9, and it does not authorize experimental execution.

## Candidate-scoped N=1 gate

A bounded N=1 operational-characterization gate is defined for `c6157158…`. The gate is explicitly non-authorizing. It is intended to produce at most an operational characterization and cannot establish DGAF efficacy. N=1 remains unexecuted and empirical N remains 0.

## Canonical agent-role boundary

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

## Evidence boundary

CI success, deterministic tests, deployment readiness, synthetic evaluator results, governance documentation, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Historical evidence remains exact-SHA/run/deployment scoped.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
