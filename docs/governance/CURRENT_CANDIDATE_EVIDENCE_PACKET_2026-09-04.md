# Current-Candidate Evidence Packet

**Originally opened:** 2026-09-04  
**Reconciled:** 2026-09-05  
**Control-plane reconciliation base:** `4382a7b745c1abde3a68eb7848611412f5bd34d7`  
**Designated runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

This packet is a control/evidence-index artifact. It does not establish efficacy, create a freeze, grant authorization, permit unblinding, or create empirical observations.

## Predicate matrix

| Predicate | Current state | Evidence / remaining boundary |
|---|---|---|
| P1 Candidate Integrity | CLOSED / VERIFIED | apparatus, candidate/tree, exact deployment identity |
| P2 Runtime Contract | CLOSED / VERIFIED | run `33730195621`; artifact `9883521704` |
| P3 Artifact Contract | CLOSED / VERIFIED | run `33939955138`; artifacts `9961526468` / `9961526662` |
| P4 Security / Blinding | OPEN / PROCEDURE ESTABLISHED / OPERATION NOT EXECUTED | synthetic controls pass; real distinct-human custody/access separation absent |
| P5 Provenance / Reproducibility | CLOSED / VERIFIED | candidate reproducibility evidence + exact analysis identities + signed authoritative merge `2e325acd…` + post-merge deep CI PASS |
| P6 Evidence Custody | CLOSED / VERIFIED | external archive → retrieval → SHA-256 equality for retained evidence set |
| P6a Runtime / CORS | CLOSED / VERIFIED | run `33728695806`; artifact `9882965299` |
| P7 Scientific Target | ADOPTED / FINAL BINDING OPEN | actual P4 custody and final freeze identities remain unresolved |
| P8 Analysis Lock | OPEN / FAIL-CLOSED | analysis identities bound; immutable freeze not created/verified |
| P9 Independent Verification | NOT EXECUTED / OPEN | final frozen-chain independent verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance decision |
| Empirical N | 0 | no empirical observations |

## Exact runtime evidence

### P2

Run `33730195621` completed successfully against candidate `7c1cc4bb…` and deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`. Artifact `9883521704` has digest:

`sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`

The valid request's expected HTTP 503 / `BLOCKED` outcome is fail-closed contract behavior because live audit state is not wired; it is not general application-health or efficacy evidence.

### P6a

Run `33728695806` completed successfully against the same candidate/deployment tuple. Artifact `9882965299` has digest:

`sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`

This CORS evidence is exact-endpoint/deployment/environment/origin scoped.

## P3 artifact contract

Run `33939955138` verifies candidate/tree identity, canonical matrix/schema constraints, deterministic contract behavior, duplicate rejection, and fail-closed unauthorized pilot behavior. P3 remains structural evidence only.

## P4 security / blinding

Synthetic run `33939574283` demonstrates mock-key bijection/leakage/freeze-order controls. The merged `docs/governance/P4_HUMAN_KEY_CUSTODY_PROCEDURE.md` defines the real-world custody procedure using distinct human principals and nonce-hardened commitments.

The procedure has not been performed. No real Key Custodian, distinct execution/analysis principal, real commitment digest, custody attestation, or no-access attestation has been accepted. P4 remains OPEN / NOT EXECUTED operationally.

## P5 provenance / reproducibility — CLOSED / VERIFIED

Exact analysis-control identities:

- analysis implementation blob `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`;
- deterministic analysis configuration SHA-256 `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`;
- pilot runner blob `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243`;
- pilot artifact schema blob `c620d3755a645c5f2ad14124f42ce07a1c670c5f`;
- protocol `0.7.5`.

The analysis configuration SHA-256 was independently recomputed and matched exactly.

Exact-candidate run `33939955138` provides candidate/tree, protocol/dependency, toolchain/environment, deterministic reproduction, environment fingerprint, RNG separation, and topology-determinism evidence.

PR #247 bound these identities into the authoritative control plane. Its exact PR head completed all returned workflows successfully and merged as signed commit `2e325acdde74dde50d3d4dc4f493a834fbd28eb2`.

Post-merge verification on exact `2e325acd…` includes:

- Control-State Consistency — PASS;
- HEAD Binding — PASS;
- Governance CI `33945464907` — PASS;
- PDMAL Pre-Authorization Security `33945464908` — PASS.

Those deep checks include locked P8 analysis tests, pilot artifact-schema tests, execution-contract tests, durable-retention tests, adversarial controls, formal-model checking, and explicit non-empirical contract-mode verification.

See `docs/experiment/P5_PROVENANCE_REPRODUCIBILITY_ATTESTATION_2026-09-05.md`.

P5 closure is bounded to provenance/reproducibility; it is not efficacy evidence.

## P6 evidence round trip

The finalized P3/P5 and P4 source/registry ZIPs were copied to separate archive custody, retrieved as raw bytes, and SHA-256 hashed. Retrieved digests matched the recorded source-artifact digests. This establishes the defined byte-integrity/retention contract only.

## Current-main operational boundary

Current repository source/deployment health is a separate operational question from the designated scientific candidate. The authoritative Vercel CLI production path is currently blocked by Vercel's 100-API-deployments-per-24-hours quota, tracked in Issue #250. No current-main deployment provenance or live health result should be inferred from the older READY candidate deployment.

## Remaining critical path

1. Perform and independently verify actual P4 human/key custody and access separation.
2. Complete P7 final scientific identity binding.
3. Construct and independently verify the P8 immutable freeze.
4. Execute independent P9 against the final frozen chain.
5. Record separate explicit pilot authorization.
6. Only then execute blinded empirical observations.

## Non-transfer rule

No historical candidate, deployment, artifact, runtime result, or experimental observation transfers to another identity without explicit provenance. Successful CI, synthetic evidence, deployment readiness, and documentation reconciliation are not empirical results.

Freeze: **NOT ESTABLISHED** · Pilot authorization: **NOT GRANTED** · Empirical N: **0**
