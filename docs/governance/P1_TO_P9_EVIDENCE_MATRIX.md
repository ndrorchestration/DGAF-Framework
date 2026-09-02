# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-02  
**Documentation baseline:** `main` / `275756fd81c975f17ae3d16d24e599db0617cf85`  
**Selected experimental candidate:** PR `#192` / `58ba9a072f40e94638b0332eeec19dd882a7ff95`  
**Selected candidate tree:** `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`  
**Corrected apparatus provenance anchor:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
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
- `edd3b5c…` — predecessor of the selected candidate; its CI failures are superseded by the clean corrections incorporated into `58ba9a…`.

## Predicate matrix

| Predicate | Current state | Current evidence / gap |
|---|---|---|
| P1 Candidate Integrity | **OPEN — substantially evidenced** | Exact candidate SHA/tree/base and candidate-bound workflow artifacts are retained. Exact deployment identity is not established. |
| P2 Execution Contract / Runtime | **OPEN — deployment-bound** | No authenticated five-case runtime matrix exists for `58ba9a…`; prior `92ff830b…` evidence does not transfer. |
| P3 Artifact Contract | **VERIFIED — current candidate engineering/control scope** | Current candidate instrumentation/schema/integrity checks passed in the September 2 workflow wave. Full experimental execution remains separately gated. |
| P4 Security / Blinding | **OPEN — operational closure** | Pre-auth/security and negative-state controls passed; end-to-end operational custody/access-separation closure is not independently established. |
| P5 Provenance / Reproducibility | **VERIFIED — verifier/toolchain scope; final closure open** | Current candidate hashes, environment/dependency fingerprints, and deterministic instrumentation are retained; final reproduction chain remains open. |
| P6 Durable Evidence Custody | **OPEN / FAIL-CLOSED** | GitHub Actions artifacts exist, but durable independent archive/retrieval/hash verification is not yet established. |
| P6a Runtime/CORS | **OPEN — deployment-bound** | No authenticated four-case CORS matrix exists for `58ba9a…`; prior mainline evidence does not transfer. Vercel currently reports provider build/deployment rate limiting. |
| P7 Scientific Target | **ADOPTED / exact-candidate binding pending** | Existing scientific specification remains authoritative; a September 2 exact-candidate provenance binding record is to be maintained separately from freeze/authorization. |
| P8 Analysis Lock | **OPEN / FAIL-CLOSED** | Exact candidate CI prerequisites now pass, but P2/P6a, P4/P6, final P7 binding, and fresh P9 remain open. |
| P9 Independent Verification | **OPEN — fresh final-candidate verification required** | Prior scoped P9 belongs to `a43219b…`/`562753b…`; it cannot certify `58ba9a…`. |

## September 2 exact-candidate CI evidence

All 18 GitHub Actions workflows associated with `58ba9a…` completed successfully:

- Governance CI — run `33616403706`
- PDMAL Pre-Freeze Runner Validation — run `33616403754`
- PDMAL Pre-Authorization Security — run `33616403843`
- Truth Layer Tests — run `33616403712`
- DGAF Regression Suite — run `33616403733`
- PDMAL Instrumentation Dry Run — run `33616403724`
- PDMAL Harness Validation — run `33616403784`
- Doc Lint (PR Scope) — run `33616403765`
- Claim Hygiene Audit — run `33616403827`
- IP Hygiene Sweep — run `33616403700`
- Full Repository Coverage Audit — run `33616403757`
- Validate Control-State HEAD Binding — run `33616403850`
- Truth Layer Validation — run `33616403771`
- PPTL CI — run `33616403803`
- Control-State Consistency — run `33616403858`
- Propagation Consistency (Advisory) — run `33616403828`
- Epistemic Evidence Validation — run `33616403749`
- Doc Lint — run `33616403696`

The Pre-Freeze Runner Validation job also passed its fail-closed runner/provenance, default-negative-state, artifact-schema/integrity, manifest, and artifact-upload checks.

## Current candidate-bound artifacts

- Pre-freeze runner artifact `9841238710`; ZIP digest `sha256:4948b6889b2e691d794a6d7dd3b8d600f15b16ccabebec330b44380120dbcf5e`.
- Governance evaluation artifact `9841231335`; ZIP digest `sha256:0658a9c35acde62fcb9d5634d7ccd7f90d1a209b403bd9db8331f9ac020e962`.
- Governance freeze-control artifact `9841228966`; ZIP digest `sha256:14585aae73c232ab8a927623dee3971d4c6e5cfb8abb63dd2907fc522aeaed09`.
- PDMAL instrumentation artifact `9841100424`; ZIP digest `sha256:7cfb548a48105571c8a61e27a3af4b579d9d875cfcd94b11d45d8893f9d09841`.

The current freeze-control evidence explicitly records `58ba9a…`, authorization `NOT_GRANTED`, freeze `NOT_CREATED`, and empirical N `0`. Workflow payloads may separately record GitHub's PR merge-ref execution identity; that is retained as execution metadata and is not substituted for the candidate head.

## Historical evidence boundaries

P2/P6a runtime evidence bound to `92ff830b…` and its historical deployment remains useful only as historical evidence. Prior completion-candidate P3/P4/P5/P6 and P9 results bound to `a43219b…`/`562753b…` remain historical. No result transfers merely because code or workflow definitions are shared.

## Vercel boundary

The combined status for `58ba9a…` currently reports `Vercel: failure` at the provider build/deployment-rate-limit target. No READY deployment with independently confirmed Git SHA `58ba9a…` is currently established. This blocks deployment-bound runtime closure but does not invalidate the successful GitHub Actions wave.

## P-35 boundary

The selected candidate contains the reviewed P-35 production-boundary remediation and the reconciled test callers/TLA+ release digest. The remediation still does not silently define an approved PDMAL-specific constitutional premise policy. Pilot execution remains fail-closed until that policy and all downstream predicates are satisfied.

## Remaining critical path

1. Establish an exact Vercel deployment/runtime identity for `58ba9a…` and execute authenticated P2/P6a.
2. Complete operational P4 and durable-custody P6 evidence.
3. Record the exact-candidate P7 provenance binding without changing the already-adopted scientific values.
4. Execute fresh final-candidate P9 and close P8 only from current evidence.
5. Create and independently verify the immutable freeze.
6. Obtain separate explicit pilot authorization.
7. Only then execute the blinded pilot; empirical N remains `0` until that point.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
