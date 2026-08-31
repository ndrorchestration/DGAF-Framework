---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-31
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** the current `main` ref is the documentation/control-plane lineage. The **current apparatus source** is `02e4c958e435f1faaa6fbf15909f9141ed2a6e39`, the verified merge of PR #160, which restored P-31 SCPE and P-33 Convergence historical substrate with parity tests. This apparatus source is the identity boundary for the current post-restore candidate. Do not treat later documentation-only commits as a new apparatus candidate.
>
> Prior P2/P6a evidence remains exact to its original source/deployment scope and is not transferred to the post-#151 or post-#160 apparatus. No freeze or experimental authorization follows from merge, CI success, or deployment readiness.

## Identity roles

- `2a80f819…` — historical P8 checklist ancestor.
- `303f4424…` — integrated DGAF v1 engineering/production source and prior P2/P6a evidence boundary.
- `ac8ea267…` — prior historical experimental verification boundary.
- `c6157158…` — superseded pre-remediation candidate; retained for provenance only.
- `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` — post-#151 apparatus commit / prior candidate boundary.
- `02c146d1…` — prior candidate-designation/control record.
- `02e4c958e435f1faaa6fbf15909f9141ed2a6e39` — current apparatus source after PR #160 P-31/P-33 restoration.
- PR #162 head `cdb63ca138cf6a60727f91067fe8f7338f19f4a6` — unmerged draft provenance-binding candidate; not part of `main`.

## Current engineering/control-plane source

PR #160 restored P-31 SCPE and P-33 Convergence historical substrate and parity tests. The merge commit `02e4c958…` is therefore a substantive apparatus change and starts the current candidate cycle. PR #162 further binds restored P-31/P-33 state into canonical provenance identity, but remains a draft and is not part of `main`.

Documentation-only commits may advance the `main` tip without changing the apparatus source. Candidate identity changes only when apparatus-defining content changes and a new candidate boundary is intentionally established.

The remaining constitutive gates are intentionally fail-closed. P-31/P-33 restoration does not imply completion of P-27, P-29, P-30, P-32, or DemiJoule, and does not advance empirical N.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` ref | CURRENT CONTROL-PLANE LINEAGE | Resolve `main` directly in GitHub for the latest documentation/control state. The literal tip SHA is deliberately not embedded here to prevent self-staleness after doc-only commits. |
| Current apparatus source | CURRENT POST-RESTORE APPARATUS | `02e4c958…`; P-31/P-33 restored; remaining constitutive gates incomplete |
| Prior engineering/runtime source | VERIFIED / HISTORICAL SCOPE | `303f4424…`; prior production deployment and P2/P6a evidence |
| Prior pre-remediation candidate | SUPERSEDED / HISTORICAL | `c6157158…`; evidence does not transfer post-#151 |
| Post-#151 apparatus candidate | HISTORICAL / SUPERSEDED | `05fa286…`; prior candidate boundary |
| PR #162 provenance-binding change | DRAFT / NOT MERGED | head `cdb63ca…`; successful validation runs; Live Regression (Vercel) remains skipped |
| P-31 | RESTORED / IMPLEMENTED | Historical substrate restored in PR #160; candidate-scoped verification remains required |
| P-33 | RESTORED / IMPLEMENTED | Historical substrate restored in PR #160; candidate-scoped verification remains required |
| P-27 | OPEN / FAIL-CLOSED | Contract-qualified restoration still pending |
| P-29 | OPEN / FAIL-CLOSED | Normative contract and halt-enforcement semantics unresolved |
| P-30 | OPEN / FAIL-CLOSED | Acceptance-schema contradiction unresolved |
| P-32 | OPEN / FAIL-CLOSED | Historical restoration prepared but not implemented on current candidate |
| DemiJoule | OPEN / FAIL-CLOSED | Constitutive contract unresolved: SPEC efficiency advisory vs implemented six-axis semantic-safety gate |
| P2 runtime verification | NEW CANDIDATE OPEN | Prior successful runs remain source-bound; fresh execution required for the current apparatus/candidate |
| P6a CORS verification | NEW CANDIDATE OPEN | Prior successful runs remain source-bound; fresh execution required for the current apparatus/candidate |
| P3–P6 | OPEN / FAIL-CLOSED | Candidate-scoped evidence required |
| P7 | ADOPTED / BINDING PENDING | Must bind to the final candidate/freeze |
| P8 | OPEN / FAIL-CLOSED | New candidate analysis/apparatus binding required |
| P9 | NOT EXECUTED FOR CURRENT CANDIDATE | Independent verification required |
| Freeze | NOT CREATED | No freeze identity is currently authoritative |
| Authorization | NOT GRANTED | Separate governance transition required |
| Empirical N | 0 | No authorized pilot execution |

## Documentation and provenance control rule

This document distinguishes four identities: **`main` tip, apparatus source, candidate identity, and deployment identity**. Documentation-only changes advance the first but do not automatically alter the second or create the third. Runtime evidence is valid only when its deployment and source identity are explicitly bound to the candidate under evaluation.

## Evidence boundary

CI success, deterministic tests, deployment readiness, synthetic evaluator results, governance documentation, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Historical evidence remains exact-SHA/run/deployment scoped.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
