# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Current documentation/evidence lineage:** `main`  
**Prior engineering/production source:** `303f4424d2198f0d0cf76305c589263dd1e417dc`  
**Prior pre-remediation candidate:** `c6157158bf0ee4840e99a381a4b99bd2febe2302` (historical/superseded)  
**Current post-#151 apparatus candidate:** `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`  
**Candidate designation/control commit:** `02c146d1e0cdc423948ac0dfa11e98f812edfb44`  
**Historical experimental verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface. It does not constitute executed experimental evidence. Historical evidence remains exact-SHA/run/artifact scoped. The post-#151 apparatus candidate is a new evidence target and does not inherit prior candidate verification automatically.

## Identity roles

- `2a80f819…` — historical P8 checklist ancestor.
- `303f4424…` — prior integrated engineering/production source and P2/P6a evidence boundary.
- `ac8ea267…` — prior historical experimental verification boundary.
- `c6157158…` — superseded pre-remediation candidate.
- `05fa286…` — current post-#151 apparatus candidate.
- `02c146d1…` — candidate-designation/control commit; not the apparatus identity.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact final apparatus/source identity and provenance | **OPEN / CANDIDATE DESIGNATED** | exact candidate tree/component identities reconciled and retained |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **PRIOR VERIFIED / NEW CANDIDATE OPEN** | fresh run bound to `05fa286…` and exact deployment; prior run `33300481208` remains scoped to `303f4424…` |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **IMPLEMENTED / OPEN** | fresh `05fa286…` candidate-scoped execution evidence retained |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | current-cycle operational evidence retained and independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | current candidate evidence retained and independently reproducible |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **BLOCKED / OPEN** | current candidate evidence archived, retrieved independently, and hash-verified |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **PRIOR VERIFIED / NEW CANDIDATE OPEN** | fresh run bound to `05fa286…` and exact deployment |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / BINDING PENDING** | adopted record bound to exact final candidate/protocol/analysis/freeze identity |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all applicable P8 predicates evidenced against `05fa286…` and inspected |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED FOR NEW CANDIDATE** | independent verifier passes without candidate/verifier monoculture |

## Evidence inheritance rule

P2/P6a evidence from `303f4424…` remains valid for that exact source/deployment boundary. It is not evidence for `05fa286…`. Likewise, P3–P9 records produced before PR #151 are historical/pre-remediation evidence and are not closure for the post-#151 apparatus.

## Current candidate boundary

The designated apparatus candidate is `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`. The designation/control record is `02c146d1…`. These identities must remain distinct.

Before current-candidate P2/P6a closure, the exact Vercel deployment bound to `05fa286…` must be verified. Deployment readiness is necessary provenance, not runtime verification.

## Issue #152 dependency

The seven historical TGL gate contracts remain governed by the R1–R4 recovery matrix and Issue #152. Historical recovery does not establish current restoration. Missing substrate dimensions, unresolved contradictions, or absent wiring keep the gates FAIL-CLOSED.

## Remaining critical path

1. Verify exact `05fa286…` candidate/deployment identity.
2. Fresh P2 runtime verification.
3. Fresh P6a CORS verification.
4. Complete P3 candidate-scoped artifact evidence.
5. Reconcile and explicitly specify/adapt recovered historical gate contracts under Issue #152.
6. Complete P4/P5/P6 current-cycle evidence.
7. Bind P7 to final candidate/protocol/analysis/freeze identity.
8. Close P8 from current-candidate evidence.
9. Execute independent P9 verification.
10. Create and independently verify a new immutable freeze.
11. Obtain separate explicit pilot authorization.
12. Only then execute the blinded pilot.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
