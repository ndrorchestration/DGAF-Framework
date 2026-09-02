# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-02  
**Documentation baseline:** `main` / `275756fd81c975f17ae3d16d24e599db0617cf85`  
**Selected experimental candidate:** PR `#192` / `58ba9a072f40e94638b0332eeec19dd882a7ff95`  
**Selected candidate tree:** `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`  
**Corrected apparatus provenance anchor:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Exact candidate deployment:** **NOT ESTABLISHED**  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This is the current planning/control surface. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

| Predicate | Current state | Current evidence / gap |
|---|---|---|
| P1 Candidate Integrity | **OPEN — substantially evidenced** | Candidate SHA/tree/base and workflow artifacts retained; exact candidate deployment identity not established. |
| P2 Execution Contract / Runtime | **OPEN — deployment-bound** | No authenticated five-case runtime matrix for `58ba9a…`; historical runtime evidence does not transfer. |
| P3 Artifact Contract | **VERIFIED — exact candidate engineering/control scope** | September 2 candidate CI/instrumentation/harness/artifact checks passed. |
| P4 Security / Blinding | **WORKFLOW EVIDENCE PRESENT / OPERATIONAL CLOSURE OPEN** | Operational custody/access separation, blinded bijection, and no-premature-unblinding evidence remain open. |
| P5 Provenance / Reproducibility | **VERIFIED — verifier/toolchain scope; final closure open** | Candidate-bound CI, deterministic instrumentation, hashes, and environment/toolchain checks pass; final independent reproduction-chain evidence remains open. |
| P6 Durable Evidence Custody | **OPEN / FAIL-CLOSED** | CI artifacts exist, but durable independent archive/retrieval/hash verification is not established. |
| P6a Runtime/CORS | **OPEN — deployment-bound** | No authenticated four-case CORS matrix for `58ba9a…`. |
| P7 Scientific Target | **EXACT-CANDIDATE BINDING RECORDED / PRE-FREEZE** | Scientific specification is bound to `58ba9a…`; immutable frozen-apparatus identity remains pending. |
| P8 Analysis Lock | **OPEN / FAIL-CLOSED** | P2/P6a, P4/P6, final frozen-state P7, and fresh P9 remain open. |
| P9 Independent Verification | **OPEN — fresh final-candidate verification required** | Prior P9 belongs to superseded candidates and cannot certify `58ba9a…`. |

## Deployment finding

A READY Vercel deployment exists for superseded candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29` (`dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17`). Vercel records its Git SHA as `a43219b…`; this is historical evidence only and cannot satisfy `58ba9a…` P2/P6a. No READY deployment with recorded Git SHA `58ba9a…` has been established.

## Support-lane disposition

PR #197 and PR #198 contain clean support diffs already incorporated into selected candidate `58ba9a…`; they are redundant support lanes rather than separate candidate lineage.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
