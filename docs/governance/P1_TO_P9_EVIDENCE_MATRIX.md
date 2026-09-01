# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-01  
**Current documentation/evidence lineage:** `main`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Corrected apparatus tree:** `973c92335caf84f37fc2b3c4df6dd83b3b855087`  
**Current runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a`  
**Current runtime candidate tree:** `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`  
**Current production deployment:** `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`  
**Latest completion candidate:** `562753b3053b3566b0fcad1b0b1df151d7de119a` on `completion/2026-09-01-exact-candidate`  
**Pre-correction apparatus source:** `d56b5b3c44e39ddb8c883259584432ab39259306` — historical/invalidated  
**Pre-correction deployment:** `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb` — historical/non-closing  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus source and canonical provenance anchor.
- `973c9233…` — corrected apparatus tree.
- `92ff830b…` — current production/runtime candidate on mainline state.
- `73cf3ad…` — exact runtime candidate tree.
- `562753b3…` — latest controlled completion-candidate SHA used for scoped P9 verification; not the current mainline runtime candidate unless separately selected and rebound.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — current production deployment recorded by current P2/P6a runtime evidence.
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
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **VERIFIED** | Run `33509348174`; artifact `9800942933`; five required cases passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **IMPLEMENTED / OPEN** | current-candidate execution evidence retained and provenance-linked |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | current-cycle operational evidence retained and independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | current-candidate reproducibility evidence retained/checked |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **OPEN / FAIL-CLOSED** | current candidate evidence archived, independently retrieved, and hash-verified |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **VERIFIED** | Run `33509416955`; artifact `9800972819`; four required checks passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / FINAL BINDING OPEN** | exact corrected apparatus/candidate/protocol/analysis/freeze binding |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | candidate and analysis identities evidenced and TGL/P-35 predicates verified |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **SCOPED PASS / BROADER CLOSURE OPEN** | current candidate undergoes the complete P9 evidence-chain review; run `33567199896` separately verifies exact candidate identity, alternate canonicalization/hash path, and authority identity for `562753b…` |

## Latest P9 evidence

Run `33567199896` completed successfully on 2026-09-01 for exact candidate `562753b3053b3566b0fcad1b0b1df151d7de119a`.

Verified predicates in that run:

- checkout `HEAD` matched `GITHUB_SHA`;
- independent `jq -S -c` canonicalization plus `sha256sum` matched the DGAF/Python digest;
- `tests/test_agent_authority_matrix.py` returned `4 passed` against the exact candidate;
- independent P9 JSON and SHA-256 sidecar were uploaded with `if-no-files-found: error`.

Independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.  
P9 artifact ID: `9823570326`.  
P9 artifact ZIP digest: `sha256:8e3435a3af0dc5de7376d970b9f1665a18db8ff04b26a2c0eaae8acf8b095d85`.

This result is **scoped** to `562753b…`. It does not transfer to `92ff830b…`, `c6157158…`, or `main` merely because the repository and workflows are shared.

## Provenance correction closure

PR #174 merged the bounded correction after independent review found that #170's canonicalization bound P-31/P-33 but omitted Sentinel, Apogee, DemiJoule, KAPPA, and Phi state. The corrected apparatus at `2a54a67d…` includes all seven gate-state blocks and regression tests proving each affects canonical identity, plus substrate-driven P-29 tests.

The mainline runtime candidate is a distinct successor identity: `92ff830b…`, tree `73cf3ad…`. Git history establishes `2a54a67d…` as its recorded lineage basis. The separate completion candidate `562753b…` is independently tracked and must not be silently substituted.

## Runtime identity and evidence rule

Current P2/P6a execution evidence is bound to candidate `92ff830b…`, exact tree `73cf3ad…`, and production deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`.

P2 artifact digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`.  
P6a artifact digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`.

P2's required five-case matrix passed, including its fail-closed missing-audit case. P6a's required four-check matrix passed, including allowed-origin preflight 204 and disallowed-origin preflight 403. These are runtime predicate results only and do not constitute efficacy evidence.

## Seven-gate restoration status

All seven constitutive gates are **implemented, provenance-complete, and pre-freeze validated**. This is engineering/provenance status, not experimental efficacy evidence.

## Stale documentation classification

Older audit records stating that inline artifact validation is missing are historical/stale observations, not current implementation defects. Historical records remain preserved and exact in their original scope; current-state documents carry the present implementation and current evidence status.

## Historical-priority boundary

The historical-priority adjudication dated 2026-09-01 establishes substantial external prior art for the individual DGAF mechanisms. The remaining historical question is the narrower cross-domain integration connecting formation-state governance to candidate-bound experimental verification and authorization. No absolute firstness claim is established.

Primary record: `docs/research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`.

## Remaining critical path

1. Select/rebind the intended current completion candidate for the pilot cycle.
2. Complete current-candidate P3 artifact-contract evidence.
3. Complete P4 operational blinding/custody evidence.
4. Complete P5 environment/topology/RNG reproducibility evidence.
5. Complete P6 durable archive/retrieval/hash evidence.
6. Finalize P7 exact candidate/protocol/analysis/freeze binding.
7. Verify P8 TGL/P-35 predicates against the exact selected candidate.
8. Complete broader P9 evidence-chain closure using exact selected candidate evidence.
9. Create and independently verify the immutable freeze.
10. Obtain separate explicit pilot authorization.
11. Only then execute the blinded pilot and allow empirical N to advance from 0.

## Anti-transfer / fail-closed rule

No historical candidate, deployment, artifact, runtime result, or experimental observation may be transferred to another candidate merely because code or documentation appears equivalent. Identity must be explicit and exact.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
