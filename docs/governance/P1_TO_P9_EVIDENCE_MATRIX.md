# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-01  
**Current documentation/evidence lineage:** `main`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Corrected apparatus tree:** `973c92335caf84f37fc2b3c4df6dd83b3b855087`  
**Current runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a`  
**Current runtime candidate tree:** `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`  
**Current production deployment:** `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`  
**Pre-correction apparatus source:** `d56b5b3c44e39ddb8c883259584432ab39259306` — historical/invalidated  
**Pre-correction deployment:** `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb` — historical/non-closing  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus source and canonical provenance anchor.
- `973c9233…` — corrected apparatus tree.
- `92ff830b…` — current production/runtime candidate.
- `73cf3ad…` — exact runtime candidate tree.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — current production deployment recorded by current P2/P6a runtime evidence.
- `4e345c03…` — pre-merge #174 head; validation lineage only.
- `d56b5b3c…` — pre-correction apparatus source; invalidated current candidate.
- `dpl_76UU8mCm…` — deployment bound to invalidated `d56b5b3c…`; historical/non-closing.
- `303f4424…` — prior integrated engineering/runtime boundary.
- `ac8ea267…` — historical experimental verification boundary.
- `c6157158…` — superseded pre-remediation candidate.
- `05fa286…` — superseded post-#151 candidate; no evidence transfers.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact final apparatus/source identity, candidate identity, tree, deployment identity, and complete provenance | **CURRENT-CANDIDATE EVIDENCE OPEN** | exact final candidate/provenance/deployment binding retained and reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **VERIFIED** | Run `33509348174`; artifact `9800942933`; five required cases passed |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **IMPLEMENTED / OPEN** | current-candidate execution evidence retained and provenance-linked |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | current-cycle operational evidence retained and independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | current-candidate reproducibility evidence retained/checked |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **OPEN / FAIL-CLOSED** | current candidate evidence archived, independently retrieved, and hash-verified |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **VERIFIED** | Run `33509416955`; artifact `9800972819`; four required checks passed |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / FINAL BINDING OPEN** | exact corrected apparatus/candidate/protocol/analysis/freeze binding |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | candidate and analysis identities evidenced and TGL/P-35 predicates verified |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED** | independent verifier passes after current candidate formation |

## Provenance correction closure

PR #174 merged the bounded correction after independent review found that #170's canonicalization bound P-31/P-33 but omitted Sentinel, Apogee, DemiJoule, KAPPA, and Phi state. The corrected apparatus at `2a54a67d…` includes all seven gate-state blocks and regression tests proving each affects canonical identity, plus substrate-driven P-29 tests.

The current runtime candidate is a distinct successor identity: `92ff830b…`, tree `73cf3ad…`. Git history establishes `2a54a67d…` as its lineage basis. These identities must remain separate in all scientific and evidentiary binding.

## Runtime identity and evidence rule

Current P2/P6a execution evidence is bound to candidate `92ff830b…`, exact tree `73cf3ad…`, and production deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`.

P2 artifact digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`.  
P6a artifact digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`.

P2's required five-case matrix passed, including its fail-closed missing-audit case. P6a's required four-check matrix passed, including allowed-origin preflight 204 and disallowed-origin preflight 403. These are runtime predicate results only and do not constitute efficacy evidence.

## Seven-gate restoration status

All seven constitutive gates are **implemented, provenance-complete, and pre-freeze validated**. This is engineering/provenance status, not experimental efficacy evidence.

## Stale documentation classification

Older audit records stating that inline artifact validation is missing are historical/stale observations, not current implementation defects. The current implementation performs inline artifact validation. Historical records remain preserved and exact in their original scope; current-state documents carry the present implementation and current evidence status.

## Remaining critical path

1. Complete current-candidate P3 artifact-contract evidence.
2. Complete P4 operational blinding/custody evidence.
3. Complete P5 environment/topology/RNG reproducibility evidence.
4. Complete P6 durable archive/retrieval/hash evidence.
5. Finalize P7 exact candidate/protocol/analysis/freeze binding.
6. Verify P8 TGL/P-35 predicates against the current candidate.
7. Execute independent P9 verification.
8. Create and independently verify the immutable freeze.
9. Obtain separate explicit pilot authorization.
10. Only then execute the blinded pilot and allow empirical N to advance from 0.

## Anti-transfer / fail-closed rule

No historical candidate, deployment, artifact, runtime result, or experimental observation may be transferred to the corrected candidate merely because code or documentation appears equivalent. Identity must be explicit and exact. P2/P6a verification does not imply P3–P9 completion.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
