# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-02  
**Documentation baseline:** `main` / `275756fd81c975f17ae3d16d24e599db0617cf85`  
**Selected experimental candidate:** PR `#192` / `58ba9a072f40e94638b0332eeec19dd882a7ff95`  
**Selected candidate tree:** `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`  
**Corrected apparatus provenance anchor:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Exact candidate deployment:** **NOT ESTABLISHED**  
**Historical runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a`  
**Historical runtime deployment:** `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Identity roles

- `58ba9a…` — selected September 2 experimental candidate.
- `abdbc9b…` — selected candidate tree.
- `2a54a67d…` — corrected seven-gate apparatus/source provenance anchor.
- `92ff830b…` — historical mainline runtime candidate; P2/P6a evidence remains scoped to that identity only.
- `a43219b…` — historical controlled completion candidate; prior P3/P9 results remain scoped to that identity.
- `562753b…` — superseded historical completion candidate.
- `edd3b5c…` — predecessor of the selected candidate; its CI blockers are superseded by the clean corrections incorporated into `58ba9a…`.

## Predicate matrix

| Predicate | Current state | Current evidence / gap |
|---|---|---|
| P1 Candidate Integrity | **OPEN — substantially evidenced** | Exact candidate SHA/tree/base and candidate-bound workflow artifacts are retained. Exact candidate deployment identity is not established. |
| P2 Execution Contract / Runtime | **OPEN — deployment-bound** | No authenticated five-case runtime matrix exists for `58ba9a…`; prior `92ff830b…` evidence does not transfer. |
| P3 Artifact Contract | **VERIFIED — exact candidate engineering/control scope** | September 2 candidate CI/instrumentation/harness/artifact checks passed. No empirical efficacy observation is implied. |
| P4 Security / Blinding | **WORKFLOW EVIDENCE PRESENT / OPERATIONAL CLOSURE OPEN** | Candidate pre-auth/security and negative-state controls pass; operational custody/access-separation, bijection, and no-premature-unblinding evidence remain open. |
| P5 Provenance / Reproducibility | **VERIFIED — verifier/toolchain scope; final closure open** | Candidate-bound CI, deterministic instrumentation, hashes, and environment/toolchain checks pass; final independent reproduction-chain evidence remains open. |
| P6 Durable Evidence Custody | **OPEN / FAIL-CLOSED** | GitHub Actions artifacts exist, but durable independent archive/retrieval/hash verification is not established. |
| P6a Runtime/CORS | **OPEN — deployment-bound** | No authenticated four-case CORS matrix exists for `58ba9a…`; prior mainline evidence does not transfer. |
| P7 Scientific Target | **EXACT-CANDIDATE BINDING RECORDED / PRE-FREEZE** | Adopted scientific specification is bound to `58ba9a…` / `abdbc9b…`; immutable frozen-apparatus identity remains pending. |
| P8 Analysis Lock | **OPEN / FAIL-CLOSED** | P2/P6a, P4/P6, final frozen-state P7, and fresh P9 remain open. |
| P9 Independent Verification | **OPEN — fresh final-candidate verification required** | Prior P9 belongs to superseded candidate `a43219b…`/`562753b…`; it cannot certify `58ba9a…`. |

## September 2 exact-candidate CI evidence

All 18 GitHub Actions workflows associated with `58ba9a…` completed successfully, including Governance CI, PDMAL Pre-Freeze Runner Validation, Pre-Authorization Security, Truth Layer Tests/Validation, DGAF Regression Suite, PDMAL Instrumentation Dry Run, PDMAL Harness Validation, control-state checks, epistemic validation, coverage, claim/IP/documentation hygiene, PPTL CI, and propagation consistency.

Pre-Freeze Runner Validation run `33616403754` emitted artifact `9841238710`. The artifact manifest records `status=PRE-FREEZE`, `empirical_data_collection=false`, and `hash_locked_environment_present=true`. Its `commit` field is the workflow merge-ref execution identity `fb1f4669…` and is not substituted for candidate head `58ba9a…`.

## Current candidate-bound artifact set

- Pre-freeze runner artifact `9841238710`; ZIP digest `sha256:4948b6889b2e691d794a6d7dd3b8d600f15b16ccabebec330b44380120dbcf5e`.
- Governance evaluation artifact `9841231335`; ZIP digest `sha256:0658a9c35acde62fcb9d5634d7ccd7f90d1a209b403bd9db8331f9ac020e962`.
- Governance freeze-control artifact `9841228966`; ZIP digest `sha256:14585aae73c232ab8a927623dee3971d4c6e5cfb8abb63dd2907fc522aeaed09`.
- PDMAL instrumentation artifact `9841100424`; ZIP digest `sha256:7cfb548a48105571c8a61e27a3af4b579d9d875cfcd94b11d45d8893f9d09841`.

The freeze-control evidence records candidate `58ba9a…`, authorization `NOT_GRANTED`, freeze `NOT_CREATED`, and empirical N `0`.

## Deployment finding

A READY Vercel deployment was independently located for superseded candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29` (`dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17`). Vercel records its Git SHA as `a43219b…`, so this deployment is useful historical evidence only and cannot satisfy `58ba9a…` P2/P6a. No READY deployment with recorded Git SHA `58ba9a…` has been established.

## Support-lane disposition

PR #197 contains the two P-35 test-caller changes now present in the selected candidate. PR #198 contains the TLA+ v1.8.0 digest correction now present in the selected candidate. Their diffs are therefore redundant support lanes rather than additional candidate lineage.

## Remaining critical path

1. Establish an exact Vercel deployment/runtime identity for `58ba9a…` and execute authenticated P2/P6a.
2. Complete operational P4 and durable-custody P6 evidence.
3. Complete final independent P5 reproduction checks.
4. Maintain exact-candidate P7 binding and later bind the immutable frozen apparatus.
5. Execute fresh final-candidate P9 and close P8 only from current evidence.
6. Create and independently verify the immutable freeze.
7. Obtain separate explicit pilot authorization.
8. Only then execute the blinded pilot; empirical N remains `0` until that point.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
