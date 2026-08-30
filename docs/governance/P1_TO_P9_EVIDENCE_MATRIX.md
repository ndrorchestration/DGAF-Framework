# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Current documentation/evidence lineage:** `main`  
**Engineering/production source:** `303f4424d2198f0d0cf76305c589263dd1e417dc`  
**Designated pre-freeze candidate:** `c6157158bf0ee4840e99a381a4b99bd2febe2302` (`experimental-candidate/2026-08-30-reconciled`)  
**Candidate deployment:** `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` — `READY`, Vercel Git SHA exact match  
**Historical experimental verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` (HISTORICAL)  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface for P1–P9. It does not constitute executed experimental evidence. Historical evidence remains scoped to the exact SHA/run/artifact that produced it. The designated pre-freeze candidate is a new evidence target and does not inherit prior candidate verification automatically.

## Identity roles

- `2a80f819…` — P8 checklist ancestor; not a competing apparatus identity.
- `303f4424…` — integrated DGAF v1 engineering/production source; P2/P6a evidence boundary.
- `255d76f6…` — mainline documentation/evidence tip observed during reconciliation.
- `ac8ea267…` — prior experimental verification boundary; historical.
- `c6157158…` — **designated current pre-freeze candidate**; not frozen and not yet runtime-verified.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact final apparatus/source identity and provenance | **OPEN / CANDIDATE DESIGNATED** | candidate manifest and exact component identities reconciled and retained |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **PRIOR VERIFIED / CURRENT CANDIDATE OPEN** | fresh run bound to `c6157158…` and deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`; prior run `33300481208` remains scoped to `303f4424…` |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **IMPLEMENTED / OPEN** | fresh `c6157158…` candidate-scoped execution evidence retained |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | candidate-scoped operational evidence retained and independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | current candidate evidence retained and independently reproducible |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **BLOCKED / OPEN** | current candidate evidence archived, retrieved independently, and hash-verified |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **PRIOR VERIFIED / CURRENT CANDIDATE OPEN** | fresh run bound to `c6157158…` and deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / BINDING PENDING** | adopted record bound to exact candidate protocol/apparatus/analysis/freeze identity |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all applicable P8 predicates evidenced against `c6157158…` and inspected |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED** | independent verifier passes without verifier/candidate monoculture |

## P2 evidence record

P2 remains **VERIFIED** for run `33300481208`, job `99227568599`, artifact `9728767844`, digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`, candidate `303f4424…`, and deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`. All five required cases passed and the artifact records `all_pass = true`.

This is exact prior-candidate evidence. It is not current-candidate evidence for `c6157158…`.

## P6a evidence record

P6a remains **VERIFIED** for run `33302495240`, artifact `9729387603`, digest `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c`, candidate `303f4424…`, and deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`. It remains exact prior-candidate evidence and does not silently transfer to `c6157158…`.

## Current candidate execution boundary

The designated candidate is `c6157158bf0ee4840e99a381a4b99bd2febe2302`. Vercel deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` is now `READY` and reports Git source SHA exactly matching the designated candidate. This satisfies the deployment-provenance prerequisite for candidate-scoped runtime tests, but does not itself execute P2 or P6a.

No current-candidate P2 or P6a completion is recorded yet. The existing workflow-dispatch evidence remains bound to `303f4424…`.

## P7 adoption

The scientific decision remains adopted in substance: `dgaf` vs `null`, FFCR primary endpoint, paired root-seed estimand, two-sided 95% percentile bootstrap, 10,000 resamples, deterministic bootstrap seed `20260823`, α=`0.05`. Exact cryptographic binding to the designated candidate remains open.

## Remaining critical path

1. Fresh P2 runtime verification on `c6157158…` using deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`.
2. Fresh P6a CORS verification on the same exact candidate/deployment boundary.
3. Candidate-scoped P3 artifact-contract execution evidence.
4. P4 blinding/custody verification.
5. P5 environment/topology/RNG reproducibility verification.
6. P6 durable archive/retrieval/hash verification.
7. P7 exact scientific/protocol/apparatus/analysis binding.
8. P8 candidate-scoped analysis lock and closure.
9. Independent P9 verification.
10. New immutable freeze and independent freeze verification.
11. Separate explicit pilot authorization.
12. Authorized blinded pilot execution.

**Prior P2/P6a VERIFIED at `303f4424…`. Current candidate `c6157158…` has READY exact-source deployment provenance but is not yet runtime-verified. P3–P6 evidence-gated. P8 OPEN / FAIL-CLOSED. P9 NOT EXECUTED. No freeze. No pilot authorization. Empirical N = 0.**
