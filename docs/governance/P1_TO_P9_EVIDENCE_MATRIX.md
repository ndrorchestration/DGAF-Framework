# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-02  
**Current documentation/evidence lineage:** `main`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Corrected apparatus tree:** `973c92335caf84f37fc2b3c4df6dd83b3b855087`  
**Current runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a`  
**Current runtime candidate tree:** `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`  
**Current production deployment:** `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`  
**Latest completion candidate:** `a43219b4ed91fff8615f6c655ab3d17ca871fc29` on `completion/2026-09-01-exact-candidate`  
**Exact completion deployment:** `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` (READY / PREVIEW; Git-SHA confirmation pending)  
**Active P-35 remediation:** PR `#188`, branch `remediation/p35-premise-hook-2026-09-01`  
**Prior completion candidate:** `562753b3053b3566b0fcad1b0b1df151d7de119a` — superseded/historical  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus source and canonical provenance anchor.
- `973c9233…` — corrected apparatus tree.
- `92ff830b…` — current production/runtime candidate on mainline state.
- `73cf3ad…` — exact runtime candidate tree.
- `a43219b…` — latest controlled completion-candidate SHA and current exact-candidate verification target.
- `562753b…` — superseded completion-candidate SHA with historical scoped P9 evidence.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — current production deployment recorded by current P2/P6a runtime evidence.
- `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` — exact-candidate preview deployment; candidate Git-SHA confirmation pending.
- `c6157158…` — superseded pre-remediation candidate; its P6 attestation is historical/non-closing.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact final apparatus/source identity, candidate identity, tree, deployment identity, and complete provenance | **CURRENT-CANDIDATE EVIDENCE OPEN** | exact final candidate/provenance/deployment binding retained and reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **VERIFIED — MAINLINE ONLY** | Run `33509348174`; artifact `9800942933`; five required cases passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`; fresh exact-candidate run required |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **VERIFIED — COMPLETION CANDIDATE WORKFLOW SCOPE** | Run `33572123862`; artifact `9825740072`; exact-candidate dry-run contract passed |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **WORKFLOW-LEVEL VERIFIED / OPERATIONAL CLOSURE OPEN** | current-cycle operational blinding/custody evidence independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **WORKFLOW-LEVEL VERIFIED / FULL CLOSURE OPEN** | Run `33572123862`; exact candidate/artifact binding, RNG separation, deterministic digest, environment fingerprint retained; final candidate rebind still required |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **WORKFLOW-LEVEL VERIFIED / DURABLE ARCHIVE OPEN** | durable current-candidate archive plus independent retrieval/hash proof |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **VERIFIED — MAINLINE ONLY** | Run `33509416955`; artifact `9800972819`; four required checks passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`; fresh exact-candidate run required |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / FINAL BINDING OPEN** | exact corrected apparatus/candidate/protocol/analysis/freeze binding |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | current selected candidate passes P-35/TGL, runtime, reproducibility, custody, P7, and final P9 prerequisites |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **SCOPED PASS / REMEDIATION REVERIFY REQUIRED** | fresh exact-candidate P9 after material remediation and candidate rebinding |

## Current completion-candidate evidence

### PDMAL dry run — Run `33572123862`

Exact candidate: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

Result: **SUCCESS**.

- Blinding secret was present; value withheld.
- Deterministic smoke cases matched.
- P5 RNG stream-separation and deterministic-digest checks passed.
- Structural/artifact test suite: `19 passed`.
- Masked one-seed CSV schema validation passed.
- CSV SHA-256 sidecar matched recomputation.
- Uploaded artifact was downloaded and inner CSV checksum reverified.
- Evidence registry marked P3/P4/P5/P6 `VERIFIED` at workflow scope for the exact candidate.

Artifact ID: `9825740072`.  
Artifact ZIP digest: `sha256:1a9f520bac2bf12ca8386c5c050489620028657866e4fee66e64905507ec31ae`.  
Evidence registry artifact: `9825740649`; ZIP digest `sha256:c6c2fda4ce18d476ef95927a1430193ef34631dcce928c15695d43826678a205`.  
Inner CSV digest: `c12098da63ae1508edbb350799360e1edccfebb16c9d0faf0db4d593ffea8ce2`.

P4 and P6 above are deliberately qualified: they establish workflow-level/synthetic evidence, not the full operational closure predicates.

### P9 independent verification — Run `33572123857`

Exact candidate: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

Result: **SUCCESS / SCOPED PASS**.

Verified:

- checkout `HEAD` matched `GITHUB_SHA`;
- independent `jq -S -c` canonicalization plus `sha256sum` matched the deterministic-case digest;
- `tests/test_agent_authority_matrix.py`: `4 passed`;
- evidence declared authorization external and empirical execution not requested;
- P9 evidence JSON and SHA-256 sidecar were uploaded successfully.

Independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.  
P9 artifact ID: `9825660346`.  
P9 artifact ZIP digest: `sha256:cf5e475c31bd9258731dcec3e6f36588f9fbfa80c3bb787419b54770ccae7976`.

Because PR #188 materially changes the P-35 adapter/task boundary, this scoped pass does not certify the remediated tree. It also does not close P2/P6a for the completion candidate, P7, P8, durable archive, freeze, authorization, empirical execution, or the broader P9 evidence-chain predicate.

## P-35 remediation boundary

The exact candidate `a43219b…` was found to omit an explicit `premise_check_fn` at the DGAF adapter boundary, while the underlying P-35 gate permits a missing checker to pass through. The pilot task path likewise instantiated the DGAF condition without a premise checker.

PR #188 (`remediation/p35-premise-hook-2026-09-01`) addresses this by requiring an explicit callable checker, propagating it into `TGLHooks`, requiring it for `ConsensusTask(condition="dgaf")`, converting unexpected checker exceptions into sealed P-35 KILLs, and adding adapter/task/TGL regression tests.

This remediation does **not** invent or silently select a PDMAL-specific constitutional policy. Until the experimental-control design supplies an approved checker, pilot execution remains fail-closed. The remediation branch is engineering evidence only and is not the current experimental candidate.

The post-remediation candidate must receive fresh PDMAL/P3–P6, P9, and any affected deployment/runtime verification before it can replace `a43219b…` as the selected exact candidate.

## Historical P9 evidence

Run `33567199896` successfully verified superseded candidate `562753b3053b3566b0fcad1b0b1df151d7de119a` with independent canonical digest `f235fc…`, authority regression `4 passed`, and artifact `9823570326` (`sha256:8e3435a3af0dc5de7376d970b9f1665a18db8ff04b26a2c0eaae8acf8b095d85`). This remains historical and does not transfer to `a43219b…`.

## Runtime identity and evidence rule

Current P2/P6a execution evidence is bound to candidate `92ff830b…`, exact tree `73cf3ad…`, and deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`.

P2 artifact digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`.  
P6a artifact digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`.

No runtime evidence transfers to `a43219b…` merely because the repository/workflow is shared.

## Exact completion deployment

`dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` is the exact-candidate preview deployment created from `deploy/exact-candidate-a43219b`. It is READY, but its recorded Git source SHA still requires independent Vercel confirmation. Its SSO redirects are authentication behavior, not runtime health evidence. Authenticated P2/P6a remain outstanding for this deployment.

## Seven-gate restoration status

All seven constitutive gates remain implemented, provenance-complete, and pre-freeze validated. This is engineering/provenance status, not experimental efficacy evidence. The P-35 adapter boundary is separately under remediation because the completion candidate did not supply the premise checker required to exercise the constitutional gate.

## Historical-priority boundary

The historical-priority adjudication dated 2026-09-01 establishes substantial external prior art for the individual DGAF mechanisms. The remaining historical question is the narrower cross-domain integration connecting formation-state governance to candidate-bound experimental verification and authorization. No absolute firstness claim is established.

## Remaining critical path

1. Complete PR #188 remediation review and candidate-bound tests.
2. Select the resulting exact candidate only after verifying the remediation and its approved PDMAL premise policy.
3. Rerun current-candidate PDMAL/P3–P6 and fresh P9 against the resulting exact candidate.
4. Independently confirm the exact Vercel deployment Git SHA and execute authenticated P2/P6a against that same candidate/deployment.
5. Finalize P7 exact scientific/protocol/apparatus binding.
6. Close P8 only from current-candidate evidence.
7. Create and independently verify the immutable freeze.
8. Obtain separate explicit pilot authorization.
9. Only then execute the blinded pilot and allow empirical N to advance from 0.

## Anti-transfer / fail-closed rule

No historical candidate, deployment, artifact, runtime result, or experimental observation may be transferred to another candidate merely because code or documentation appears equivalent. Identity must be explicit and exact.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
