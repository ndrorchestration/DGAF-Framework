# Current-Candidate Evidence Packet

**Originally opened:** 2026-09-04  
**Reconciled:** 2026-09-05  
**Repository main at reconciliation:** `9cf9fcdd3454ce7309efdcbbe4ef29f802a7c97e`  
**Designated runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

This packet is a control and evidence-index artifact. It does not establish efficacy, create a freeze, grant authorization, permit unblinding, or create empirical observations.

## Identity roles

| Identity | Role |
|---|---|
| `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | corrected apparatus provenance anchor |
| `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` | immutable P-35 validation boundary |
| `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58` | consolidated control-state anchor |
| `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | designated executable runtime candidate |
| `586c00d6dedb589e52108279f9759be3c4f927e1` | runtime candidate tree |
| `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | READY production deployment sourced from the runtime candidate |
| `9cf9fcdd3454ce7309efdcbbe4ef29f802a7c97e` | current documentation/control-plane main lineage |

Documentation/control-plane descendants do not automatically replace the runtime candidate or inherit its runtime evidence.

## Predicate matrix

| Predicate | Current state | Evidence and remaining boundary |
|---|---|---|
| P1 Candidate Integrity | CLOSED / VERIFIED | apparatus, candidate/tree, self-bound provenance, and live deployment identity |
| P2 Runtime Contract | CLOSED / VERIFIED | exact candidate/deployment five-case runtime predicates; run `33730195621`, artifact `9883521704` |
| P3 Artifact Contract | CLOSED / VERIFIED | run `33939955138`, artifacts `9961526468` and `9961526662` |
| P4 Security / Blinding | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | synthetic behavior passes; real human/key custody and access separation remain unestablished |
| P5 Provenance / Reproducibility | OPEN / FINAL IDENTITY BINDING RECORDED FOR REVIEW | candidate/environment/determinism evidence present; exact analysis/configuration/runner/schema identities recorded in `P8_ANALYSIS_LOCK.md`; authoritative merge/review remains |
| P6 Evidence Custody | CLOSED / VERIFIED | external archive → retrieval → SHA-256 equality contract satisfied for retained evidence set |
| P6a Runtime / CORS | CLOSED / VERIFIED | exact candidate/deployment four-case CORS predicates; run `33728695806`, artifact `9882965299` |
| P7 Scientific Target | ADOPTED / FINAL BINDING OPEN | final apparatus/candidate/protocol/analysis/freeze binding required |
| P8 Analysis Lock | OPEN / FAIL-CLOSED | analysis identities recorded; prerequisite acceptance and immutable freeze remain |
| P9 Independent Verification | NOT EXECUTED / OPEN | final bound-chain verification not executed |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance decision |
| Empirical N | 0 | no empirical observations |

## P2 — authenticated runtime matrix

Run `33730195621` completed successfully against candidate `7c1cc4bb…` and deployment `dpl_8Msuf…`. Candidate identity, protected bypass availability, the five-case runtime matrix, and provenance upload all passed.

The candidate-bound artifact `9883521704` was resolved on 2026-09-05 and was unexpired. Its digest is:

`sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`

The valid request's expected HTTP 503 / `BLOCKED` result is fail-closed contract behavior because live audit state is not wired into `/api/orchestrate`. It is not general application-health or efficacy evidence.

## P6a — authenticated CORS matrix

Run `33728695806` completed successfully against the same candidate/deployment tuple. Candidate identity, protected bypass availability, the four-case live CORS matrix, and provenance upload all passed.

The candidate-bound artifact `9882965299` was resolved on 2026-09-05 and was unexpired. Its digest is:

`sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`

This evidence applies only to the exact endpoint, deployment, environment, and origins tested. It does not establish general security, health, or efficacy.

## P3 — artifact contract

Run `33939955138` checked out the designated candidate/tree and reported successful structural, identity, matrix, determinism, and specified adversarial-substitution checks. Its source artifact is `9961526468`; its source-bound registry is `9961526662`.

P3 closure is structural/contract evidence only. Synthetic fixture output is not empirical data.

## P4 — security and blinding

Run `33939574283` provides current-candidate synthetic mock-key evidence for deterministic bijection, leakage checks, and freeze-order behavior.

P4 remains OPEN because actual human/key custody and access separation have not been established. CI cannot infer those operational facts.

## P5 — provenance, reproducibility, and analysis identity

Run `33939955138` binds candidate/tree, protocol/dependency identity, deterministic reproduction, environment fingerprints, RNG child-stream separation, and topology fingerprints.

The designated candidate's analysis-control identities are now recorded in `docs/governance/P8_ANALYSIS_LOCK.md`:

- analysis implementation Git blob SHA: `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`;
- deterministic analysis configuration SHA-256: `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`;
- pilot runner Git blob SHA: `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243`;
- pilot artifact schema Git blob SHA: `c620d3755a645c5f2ad14124f42ce07a1c670c5f`;
- protocol version encoded by runner: `0.7.5`.

P5 remains OPEN until this exact binding lands on the authoritative branch and passes the normal consistency/review checks. No new analysis implementation is required merely to satisfy provenance bookkeeping.

## P6 — evidence round trip

The finalized P3/P5 and P4 source/registry ZIPs were copied to a separate Google Drive archive, retrieved as raw bytes, and SHA-256 hashed. The retrieved digests matched their recorded source-artifact digests.

P6 is CLOSED / VERIFIED within that defined contract. Digest equality establishes equality of compared bytes at retrieval time; it does not establish immutable storage, independent human custody, producer authenticity against compromise, or a tamper-proof chain.

## Current-main boundary

Current `main` at this reconciliation is `9cf9fcdd…`. It is a documentation/control-plane descendant of the designated runtime candidate and must not inherit candidate-scoped P2/P3/P6a evidence merely because those records are documented on `main`.

Current-main deployment and runtime health remain separate operational questions from designated-candidate scientific evidence.

## Remaining critical path

1. Establish actual P4 human/key custody and access separation.
2. Land and verify the exact P5 analysis implementation/configuration binding.
3. Complete the exact P7 scientific identity binding.
4. Close P8 only after its prerequisites are exact-bound and an immutable freeze is constructed/verified.
5. Execute independent P9 against the final bound chain.
6. Record separate explicit pilot authorization.
7. Only then execute a blinded pilot.

## Non-transfer rule

No historical candidate, deployment, artifact, runtime result, or experimental observation transfers to another identity without an explicit provenance relationship. Successful CI, synthetic evidence, deployment readiness, and documentation reconciliation are not empirical results.

Freeze: **NOT ESTABLISHED** · Pilot authorization: **NOT GRANTED** · Empirical N: **0**
