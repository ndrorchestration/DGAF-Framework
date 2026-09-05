# P8 Verification Checklist

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-05  
**Purpose:** Track only the evidence that is still required to construct and independently verify the immutable P8 freeze for the designated PDMAL candidate.

This checklist is a control surface, not a freeze record. Documentation/control-plane descendants do not replace the designated runtime candidate unless the canonical candidate identity is explicitly changed.

## Current authoritative identity

| Binding | Exact value | State |
|---|---|---|
| Corrected apparatus source | `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | KNOWN |
| Immutable P-35 validation boundary | `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` | VALIDATED |
| Designated runtime candidate | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | VERIFIED |
| Candidate tree | `586c00d6dedb589e52108279f9759be3c4f927e1` | VERIFIED |
| Candidate production deployment | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | VERIFIED FOR CANDIDATE |
| Protocol version | `0.7.5` | SELECTED / PRE-FREEZE |
| Analysis implementation blob | `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` | BOUND |
| Analysis configuration SHA-256 | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | VERIFIED / INDEPENDENTLY RECOMPUTED |
| Pilot runner blob | `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243` | BOUND |
| Pilot artifact schema blob | `c620d3755a645c5f2ad14124f42ce07a1c670c5f` | BOUND |

## Pre-freeze predicates already satisfied

- [x] **P1 Candidate Integrity — CLOSED / VERIFIED.** Exact apparatus/candidate/tree/deployment provenance is retained.
- [x] **P2 Runtime — CLOSED / VERIFIED.** Run `33730195621`; artifact `9883521704`; five-case authenticated runtime matrix.
- [x] **P3 Artifact Contract — CLOSED / VERIFIED.** Run `33939955138`; artifacts `9961526468` / `9961526662`; exact-candidate schema, canonical matrix/cardinality, identity/hash, duplicate-rejection, and adversarial checks.
- [x] **P5 Provenance / Reproducibility — CLOSED / VERIFIED.** Exact analysis/configuration/runner/schema identities are bound; Governance CI `33945464907` and Pre-Authorization Security `33945464908` passed.
- [x] **P6 Durable Evidence Custody — CLOSED / VERIFIED.** Retained candidate evidence completed independent archive → retrieval → SHA-256 equality.
- [x] **P6a CORS — CLOSED / VERIFIED.** Run `33728695806`; artifact `9882965299`; four-case authenticated CORS matrix.
- [x] Exact-candidate deterministic reproduction, environment/toolchain fingerprinting, RNG-stream separation, and topology determinism are retained through run `33939955138` and the P5 closure chain.
- [x] Unauthorized pilot execution remains fail-closed and empirical collection remains disabled in pre-freeze verification.

These closures are predicate-scoped engineering/governance evidence. They are not efficacy evidence and do not authorize execution.

## P4 prerequisite — still blocking

- [ ] A genuinely distinct human Key Custodian is selected.
- [ ] A distinct execution/analysis principal is identified.
- [ ] Non-secret key and mapping commitment digests are published under `sha256-domain-separated-secret-nonce-v1`.
- [ ] Custodian and no-access attestations are attributable and retained.
- [ ] Independent custody review confirms actual role/access separation without revealing key, mapping, or nonces.

Authoritative operational checkpoint: Issue #255 and `docs/governance/P4_HUMAN_CUSTODY_EXECUTION_RECORD_2026-09-05.md`.

P4 remains **OPEN / PROCEDURE ESTABLISHED / OPERATION NOT EXECUTED** until these real-world events occur. Repository automation, AI agents, aliases, or invented principals cannot satisfy this predicate.

## P7 final-binding prerequisite

- [x] Scientific target is adopted: `dgaf` versus `null`, FFCR, paired root-seed estimand, 10,000 paired percentile bootstrap resamples, deterministic seed `20260823`, two-sided 95% interval.
- [x] Candidate/deployment/protocol/analysis/runner/schema/P2/P3/P5/P6/P6a identities are assembled in `docs/governance/P7_FINAL_BINDING_DRAFT_2026-09-05.md`.
- [ ] Actual P4 custody evidence is inserted without inference.
- [ ] Final protocol blob/commit identity is selected for freeze.
- [ ] Final accepted control-plane commit is selected for freeze.
- [ ] P7 contains no unresolved closure-blocking placeholders and is formally closed.

P7 remains **ADOPTED / FINAL BINDING OPEN**.

## P8 immutable-freeze construction

The following items must not be checked until P4 and P7 are legitimately complete.

- [ ] Construct the immutable freeze manifest from the exact P7 tuple without inference.
- [ ] Bind the final protocol blob/commit identity.
- [ ] Bind the final accepted control-plane commit.
- [ ] Bind exact candidate SHA/tree and candidate deployment identity.
- [ ] Bind exact analysis implementation/configuration/runner/schema identities.
- [ ] Bind P1/P2/P3/P4/P5/P6/P6a evidence identities and digests required by the final tuple.
- [ ] Bind the blinding-custody commitments/attestations without exposing secret material.
- [ ] Compute and retain an immutable freeze-manifest digest.
- [ ] Independently retrieve/recompute the freeze representation and verify the digest/identity tuple.
- [ ] Record the independent freeze-verification evidence and verifier identity.

Until every applicable item above is complete, **P8 remains OPEN / FAIL-CLOSED and Freeze remains NOT ESTABLISHED**.

## P9 final independent verification

Historical/scoped P9 runs are provenance only and do not transfer to the final frozen chain.

- [x] Historical independent-verification mechanisms exist and previously exercised alternate canonicalization/hash and authority-identity checks on superseded candidates.
- [ ] Final P9 verifier identity is selected independently of the producing evidence path.
- [ ] Final P9 re-resolves the immutable freeze and exact candidate/protocol/analysis/custody/evidence tuple.
- [ ] Final P9 independently verifies all required digests and candidate/freeze identities.
- [ ] Final P9 evidence artifact/digest is retained and independently reviewable.
- [ ] P9 concludes PASS for the complete final frozen chain.

P9 remains **NOT EXECUTED / OPEN** for the current final chain.

## Authorization boundary

- [ ] Separate explicit pilot authorization is recorded **after** P8 and P9 closure.
- [ ] Empirical execution remains disabled until that authorization exists.

Current state: **Freeze NOT ESTABLISHED · Pilot authorization NOT GRANTED · Empirical N = 0**.

## Closure rule

P8 may close only after real P4 custody is verified, P7 is exact and final, the immutable freeze is constructed from that tuple, and an independent freeze verification succeeds. P9 is then executed against that frozen chain. No historical candidate result, green CI run, READY deployment, synthetic blinding result, or documentation-only update may substitute for these events.
