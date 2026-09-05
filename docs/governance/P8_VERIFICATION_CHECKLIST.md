# P8 Verification Checklist

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-05  
**Purpose:** Track only the evidence still required to construct and independently verify the immutable P8 freeze for the designated PDMAL candidate.

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

Canonical procedure: `docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md`.

P4 no longer requires a personal relationship or a mandatory second-human topology. It requires **effective control separation**.

- [ ] Exactly one custody mode is selected: `H` distinct-human, `I` institutional/third-party, or `T` independently enforced technical custody.
- [ ] A unique custody-instance ID and attributable execution/analysis principal are recorded.
- [ ] The custody authority/system identity is recorded in non-secret form.
- [ ] Non-secret key and mapping commitment digests are published under `sha256-domain-separated-secret-nonce-v1` before empirical execution.
- [ ] A complete control-path inventory covers owner/admin, IAM/policy, recovery/reset, backup/restore, export/decrypt, break-glass, alternate credentials, and equivalent recovery paths.
- [ ] Evidence establishes that the execution/analysis principal cannot use any inventoried path unilaterally to recover protected material before the predeclared release condition.
- [ ] Independent review evidence supports the selected custody mode without revealing key, mapping, nonces, or recovery material.
- [ ] No contradictory access record is known.

Mode H additionally requires genuinely distinct humans and attributable role/no-access attestations. Mode I requires external custody/release-policy evidence and lack of unilateral analyst administration/recovery. Mode T requires independently inspectable or machine-verifiable enforcement evidence and absence of analyst-controlled admin/recovery/export/break-glass paths.

AI agents, aliases, same-operator accounts, ordinary repository secrets, analyst-recoverable password vaults, analyst-administered KMS/HSM configurations, and preregistration alone cannot satisfy P4.

Active operational handoff: `docs/governance/P4_INDEPENDENT_CUSTODY_EXECUTION_RECORD_2026-09-05.md` and Issue #285. Issue #255 remains historical context for the earlier human-only checkpoint.

P4 remains **OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED** until one real custody mode is instantiated and verified.

## P7 final-binding prerequisite

- [x] Scientific target is adopted: `dgaf` versus `null`, FFCR, paired root-seed estimand, 10,000 paired percentile bootstrap resamples, deterministic seed `20260823`, two-sided 95% interval.
- [x] Candidate/deployment/protocol/analysis/runner/schema/P2/P3/P5/P6/P6a identities are assembled in `docs/governance/P7_FINAL_BINDING_DRAFT_2026-09-05.md`.
- [ ] Actual P4 custody mode, instance, commitments, control-path evidence, and independent review are inserted without inference.
- [ ] Final protocol blob/content identity is selected for freeze.
- [ ] Final accepted pre-freeze control-plane commit is selected for freeze.
- [ ] Final P9 verifier script/workflow identities are bound before freeze.
- [ ] P7 contains no unresolved **pre-freeze** closure-blocking placeholders and is formally closed.

P7 remains **ADOPTED / FINAL BINDING OPEN**. Freeze/P8/P9/auth identities are downstream outputs and must not be required to close P7.

## P8 immutable-freeze construction — object F

The following items must not be checked until P4 and P7 are legitimately complete.

- [ ] Construct the immutable freeze object from the exact closed P7 tuple without inference.
- [ ] Commit that object in an exact immutable freeze commit **F**.
- [ ] Bind the final protocol blob/content identity.
- [ ] Bind the final accepted pre-freeze control-plane commit.
- [ ] Bind exact candidate SHA/tree and candidate deployment identity.
- [ ] Bind exact analysis implementation/configuration/runner/schema identities.
- [ ] Bind P1/P2/P3/P4/P5/P6/P6a evidence identities and digests required by the final tuple.
- [ ] Bind P4 custody mode, instance identity, commitments, control-path evidence, and independent-review evidence without exposing secret material.
- [ ] Confirm selected P9 verifier script/workflow definitions are present in F.
- [ ] Compute the byte SHA-256 of `docs/experiment/PDMAL_IMMUTABLE_FREEZE.json` at F and retain it externally.
- [ ] Confirm the immutable freeze object does **not** contain post-freeze verification evidence or a self-hash of its complete bytes.

At this point the freeze object exists, but P8 does not close until independent verification succeeds.

## Independent P8 freeze verification — separate record V

- [ ] Independently retrieve exact commit F rather than a mutable branch tip.
- [ ] Recompute the freeze-object byte SHA-256 and verify equality with the externally retained digest.
- [ ] Independently verify the frozen candidate/P7/control tuple and expected freeze path.
- [ ] Produce `docs/experiment/PDMAL_P8_FREEZE_VERIFICATION.json` as a separate verification record V.
- [ ] V records PASS, exact freeze commit F, exact freeze path, expected/retrieved equal SHA-256 values, verifier identity, verification method, and timestamp.
- [ ] Store V in a descendant verification commit distinct from F.
- [ ] Retain V's byte SHA-256 externally.
- [ ] Do not write V or its digest back into F.

Until every applicable item above is complete, **P8 remains OPEN / FAIL-CLOSED and Freeze remains NOT ESTABLISHED as a verified freeze**.

## P9 final independent verification

Historical/scoped P9 runs are provenance only and do not transfer to the final frozen chain.

- [x] A manual-only fail-closed final-P9 verifier/workflow exists in the pre-freeze control plane.
- [x] The final-P9 workflow is designed to resolve candidate/P7/freeze bytes from exact freeze commit F rather than trusting a later mutable copy.
- [x] The final-P9 workflow verifies its script/workflow definitions did not drift between F and the P8 verification-record commit.
- [ ] Final P9 verifier identity is fixed in closed P7 and frozen at F.
- [ ] Final P9 dispatch occurs from the exact descendant P8 verification-record commit.
- [ ] Final P9 validates external byte digests of both immutable freeze object F and separate verification record V.
- [ ] Final P9 independently verifies all required candidate/protocol/analysis/custody/evidence identities.
- [ ] Final P9 evidence artifact/digest is retained and independently reviewable.
- [ ] Final P9 concludes PASS for the complete final frozen chain.

P9 remains **NOT EXECUTED / OPEN** for the current final chain.

## Authorization boundary

- [ ] Separate explicit pilot authorization is recorded **after** P8 and P9 closure.
- [ ] Empirical execution remains disabled until that authorization exists.

Current state: **Freeze NOT ESTABLISHED · Pilot authorization NOT GRANTED · Empirical N = 0**.

## Closure rule

P8 may close only after P4-A independently enforceable custody is verified, P7 is exact and final, immutable freeze object F is constructed, F is independently retrieved/re-hashed, and separate verification record V proves that verification without modifying F. P9 is then executed from the exact V commit against F. No historical candidate result, green CI run, READY deployment, synthetic blinding result, preregistration, or documentation-only update may substitute for these events.
