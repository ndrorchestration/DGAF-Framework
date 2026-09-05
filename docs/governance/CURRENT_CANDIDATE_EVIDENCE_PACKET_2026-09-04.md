# Current-Candidate Evidence Packet

**Originally opened:** 2026-09-04  
**Reconciled:** 2026-09-05  
**Repository main at reconciliation:** `8ae37faee637d3992dfec2f635ea4d1d9252ef2d`  
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
| `8ae37faee637d3992dfec2f635ea4d1d9252ef2d` | later documentation/control-plane reconciliation commit |

Documentation/control-plane descendants do not automatically replace the runtime candidate or inherit its runtime evidence.

## Predicate matrix

| Predicate | Current state | Evidence and remaining boundary |
|---|---|---|
| P1 Candidate Integrity | CLOSED / VERIFIED | apparatus, candidate/tree, self-bound provenance, and live deployment identity |
| P2 Runtime Contract | CLOSED / VERIFIED | exact candidate/deployment five-case runtime predicates; run `33730195621`, artifact `9883521704` |
| P3 Artifact Contract | CLOSED / VERIFIED | run `33939955138`, artifacts `9961526468` and `9961526662` |
| P4 Security / Blinding | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | synthetic behavior passes; real human/key custody and access separation remain unestablished |
| P5 Provenance / Reproducibility | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | candidate/environment/determinism evidence present; final analysis implementation/configuration binding remains open |
| P6 Evidence Custody | CLOSED / VERIFIED | defined external archive → retrieval → SHA-256 equality contract |
| P6a Runtime / CORS | CLOSED / VERIFIED | exact candidate/deployment four-case CORS predicates; run `33728695806`, artifact `9882965299` |
| P7 Scientific Target | ADOPTED / FINAL BINDING OPEN | final apparatus/candidate/protocol/analysis/freeze binding required |
| P8 Analysis Lock | OPEN / FAIL-CLOSED | prerequisites and final analysis identity incomplete |
| P9 Independent Verification | OPEN | final bound-chain verification not executed |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance decision |
| Empirical N | 0 | no empirical observations |

## P2 — authenticated runtime matrix

Run `33730195621` completed successfully against candidate `7c1cc4bb…` and deployment `dpl_8Msuf…`. Candidate identity, protected bypass availability, the five-case runtime matrix, and provenance upload all passed.

The candidate-bound artifact `9883521704` was freshly resolved on 2026-09-05 and was unexpired. Its recorded digest is:

`sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`

This supersedes the earlier retrieval-unconfirmed observation. It does not constitute a new execution or establish behavior beyond the declared five predicates.

## P6a — authenticated CORS matrix

Run `33728695806` completed successfully against the same candidate/deployment tuple. Candidate identity, protected bypass availability, the four-case live CORS matrix, and provenance upload all passed.

The candidate-bound artifact `9882965299` was freshly resolved on 2026-09-05 and was unexpired. Its recorded digest is:

`sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`

This supersedes the earlier retrieval-unconfirmed observation. It is not a new execution and does not establish general security, health, or efficacy.

## P3 — artifact contract

Mainline run `33939955138` checked out the designated candidate/tree and reported successful structural, identity, matrix, determinism, and specified adversarial-substitution checks. Its source artifact is `9961526468`; its source-bound registry is `9961526662`.

P3 closure is structural/contract evidence only. The 180-record-per-seed fixture is synthetic and is not empirical data.

## P4 — security and blinding

Run `33939574283` provides current-candidate synthetic mock-key evidence for deterministic bijection, leakage checks, and freeze-order behavior.

P4 remains OPEN because actual human/key custody and access separation have not been established. CI cannot infer those operational facts.

## P5 — provenance and reproducibility

Run `33939955138` binds candidate/tree, protocol/dependency identity, deterministic reproduction, environment fingerprints, RNG child-stream separation, and topology fingerprints.

P5 remains OPEN because the final analysis implementation SHA and configuration SHA are not yet bound at the analysis-lock boundary.

## P6 — evidence round trip

The finalized P3/P5 and P4 source/registry ZIPs were copied to a separate Google Drive archive, retrieved as raw bytes, and SHA-256 hashed. The retrieved digests matched their recorded source-artifact digests.

P6 is CLOSED / VERIFIED within that defined contract. Digest equality establishes equality of the compared bytes at retrieval time; it does not establish immutable storage, independent human custody, authenticity against a compromised producer, or a tamper-proof chain.

## Current-main CI and deployment boundary

The current repository-main SHA `8ae37fa…` passed governance, regression, security/schema, evidence, truth-layer, consistency, coverage, claim-hygiene, IP-hygiene, PPTL, and documentation checks.

Its Vercel production deployment was NOT CREATED because the free-plan daily deployment quota was exceeded. Deployment identity, deployment provenance, health, and live regression were therefore NOT EXECUTED for `8ae37fa…`. The `7c1cc4bb…` deployment evidence must not be transferred to current repository main.

The post-fix Completion Controller has not yet completed a new producer → controller validation cycle. Its post-fix operational state remains NOT EXECUTED / UNKNOWN.

## Remaining critical path

1. Establish actual P4 human/key custody and access separation.
2. Bind the final P5 analysis implementation and configuration.
3. Complete the exact P7 scientific identity binding.
4. Close P8 only after its prerequisites are exact-bound.
5. Execute independent P9 against the final bound chain.
6. Establish and independently verify an immutable freeze.
7. Record separate explicit pilot authorization.
8. Only then execute a blinded pilot.

## Non-transfer rule

No historical candidate, deployment, artifact, runtime result, or experimental observation transfers to another identity without an explicit provenance relationship. Successful CI, synthetic evidence, deployment readiness, and documentation reconciliation are not empirical results.

**Freeze: NOT ESTABLISHED · Pilot authorization: NOT GRANTED · Empirical N: 0**
