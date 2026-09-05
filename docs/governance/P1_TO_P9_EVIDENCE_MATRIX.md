# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-05  
**Current main at reconciliation:** `9cf9fcdd3454ce7309efdcbbe4ef29f802a7c97e`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Runtime candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT ESTABLISHED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Identity roles

- `2a54a67d…` — corrected apparatus provenance anchor.
- `89be386b…` — consolidated control-state lineage anchor.
- `7c1cc4bb…` / tree `586c00d6…` — designated executable runtime candidate.
- `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` — exact READY production deployment bound to candidate `7c1cc4bb…`.
- `9cf9fcdd…` — current documentation/control-plane main lineage; it is not the runtime candidate.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact apparatus/source identity, executable candidate identity, deployment identity, and complete provenance | **CLOSED / VERIFIED** | satisfied: exact apparatus/candidate/tree + self-bound provenance + deployment-to-candidate binding retained/reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **CLOSED / VERIFIED** | satisfied by exact-candidate run `33730195621`, artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d` |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **CLOSED / VERIFIED** | satisfied by exact-candidate main run `33939955138`, artifacts `9961526468` / `9961526662`, and retained P3 attestation |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT** | synthetic controls pass; real human/key custody and access separation still required |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints, reproduction, and final provenance binding | **OPEN / FINAL IDENTITY BINDING RECORDED FOR REVIEW** | exact analysis/configuration/runner/schema identities are recorded in `P8_ANALYSIS_LOCK.md`; closure requires authoritative merge and consistency review |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **CLOSED / VERIFIED** | satisfied by candidate-scoped Google Drive archive and independent raw retrieval/SHA-256 equality recorded 2026-09-05 |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **CLOSED / VERIFIED** | satisfied by exact-candidate run `33728695806`, artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f` |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / FINAL BINDING OPEN** | exact apparatus/candidate/protocol/analysis/freeze binding after P4/P5 prerequisites |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | final identities accepted together and immutable freeze constructed/verified |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED / OPEN** | fresh independent verification against the final bound evidence |

## Current-candidate closure evidence

### P1 — candidate/deployment identity

The Vercel deployment record resolves `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` as READY, production-targeted, and sourced from exact Git SHA `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`.

### P2 — authenticated runtime matrix

Run `33730195621` completed successfully against the exact candidate/deployment tuple. All five predeclared runtime cases matched their required HTTP/decision outcomes. Artifact `9883521704` is unexpired and digest-bound as above. The valid request's expected HTTP 503 / `BLOCKED` result is fail-closed contract behavior because live audit state is not wired; it is not general application-health or efficacy evidence.

### P3 — artifact contract

Run `33939955138` checked out the designated candidate/tree and verified the canonical pre-freeze and pilot artifact schema/integrity contract, including candidate/record identity, canonical coordinates, four-condition balance, duplicate rejection, deterministic contract behavior, and fail-closed unauthorized pilot behavior.

### P4 — synthetic operational evidence, not closure

Run `33939574283` produced candidate-bound synthetic blinding evidence. Mock-key bijection, no cleartext/key leakage, and mock freeze-before-unblinding checks pass. Actual human/key custody/access separation is not established; P4 remains OPEN.

### P5 — reproducibility plus final identity binding record

Run `33939955138` verifies exact candidate/tree, protocol and dependency identities, hash-locked toolchain, deterministic contract reproduction, independently recomputed environment fingerprint, RNG child-stream separation, and topology determinism.

The designated candidate's final analysis-control identities are now explicitly recorded in `docs/governance/P8_ANALYSIS_LOCK.md`:

- analysis implementation Git blob SHA: `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`;
- deterministic analysis configuration SHA-256: `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`;
- pilot runner Git blob SHA: `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243`;
- pilot artifact schema Git blob SHA: `c620d3755a645c5f2ad14124f42ce07a1c670c5f`;
- protocol version encoded by runner: `0.7.5`.

P5 is not promoted to CLOSED until this binding lands on the authoritative branch and passes the normal consistency/review checks.

### P6 — durable custody

The finalized P3/P5 and P4 evidence ZIPs were archived in independent Google Drive custody, retrieved as raw bytes, and independently SHA-256 hashed. Every retrieved digest matched its original GitHub artifact digest exactly.

### P6a — authenticated CORS matrix

Run `33728695806` completed successfully against the same exact candidate/deployment tuple. The allowed-origin POST, disallowed-origin POST, allowed preflight, and disallowed preflight all matched the predeclared policy. Artifact `9882965299` is unexpired and digest-bound as above. This evidence is scoped to the tested endpoint, deployment, environment, and origins.

## Historical completion evidence — non-transferable

Earlier completion candidates and their P2/P3/P6a/P9 records remain historical unless explicitly exact-bound to the designated candidate. The historical failed P6a record for `48c12c…` remains preserved and is not rewritten as a pass.

## Anti-transfer / fail-closed rule

No historical candidate, deployment, artifact, runtime result, or experimental observation may be transferred to another candidate merely because code or documentation appears equivalent. Identity must be explicit and exact.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Remaining critical path

1. P4 actual operational human/key custody and access separation.
2. Land and verify P5 final analysis implementation/configuration identity binding.
3. P7 final exact apparatus/candidate/protocol/analysis/freeze binding.
4. P8 analysis lock and immutable freeze construction/verification.
5. P9 independent verification of the final bound chain.
6. Separate explicit pilot authorization.
7. Only then blinded pilot execution.
