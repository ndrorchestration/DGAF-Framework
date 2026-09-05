# P8 Analysis Lock

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Authority:** DGAF/PDMAL experimental-design control  
**Purpose:** Bind the executable primary analysis and its artifact contract to the designated runtime candidate before unblinding or empirical interpretation.

## Current authoritative boundary

The `main` branch is a living documentation/evidence lineage and is not itself the experimental runtime identity. The reconciliation base below is an anchor, not a perpetual current-tip claim.

| Binding | Value | State |
|---|---|---|
| Control-plane reconciliation base | `4382a7b745c1abde3a68eb7848611412f5bd34d7` | DOCUMENTATION / CONTROL-PLANE LINEAGE |
| Designated runtime candidate | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | CURRENT / PRE-FREEZE |
| Runtime candidate tree | `586c00d6dedb589e52108279f9759be3c4f927e1` | CURRENT |
| Exact candidate Vercel deployment | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | READY / PRODUCTION / EXACT-CANDIDATE VERIFIED |
| Candidate deployment URL | `https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app` | CANDIDATE RUNTIME SURFACE |
| P5 authoritative binding merge | `2e325acdde74dde50d3d4dc4f493a834fbd28eb2` | VERIFIED |
| P4 original human procedure merge | `4382a7b745c1abde3a68eb7848611412f5bd34d7` | HISTORICAL PROCEDURE ANCHOR |

Historical candidate evidence remains non-transferable unless an explicit provenance relation binds it.

## P7 scientific inputs selected

- Primary contrast: full `dgaf` versus `null`.
- Primary endpoint: FFCR.
- Statistical unit: seed, paired by root seed identity.
- Seed-level effect: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`.
- Primary estimand: equal-weight mean of complete paired seed effects.
- FFCR: proportion of complete topology × failure-count cells whose recorded `ffcr_success` is true.
- No outcome-dependent weighting, exclusion, or silent imputation.
- Bootstrap: 10,000 paired-seed percentile resamples.
- Deterministic bootstrap seed: `20260823`.
- Confidence interval: two-sided 95%, `alpha=0.05`.
- Directional support rule: estimate > 0 and CI lower bound > 0.

These are selected pre-freeze design inputs, not empirical results.

## P5 analysis implementation/configuration — CLOSED / VERIFIED

The designated candidate contains the locked primary-analysis implementation and deterministic configuration.

| Analysis object | Exact identity | State |
|---|---|---|
| Analysis implementation | `experiments/pdmal_pilot/analysis.py` | BOUND |
| Analysis implementation Git blob | `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` | VERIFIED |
| Analysis configuration SHA-256 | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | VERIFIED / INDEPENDENTLY RECOMPUTED |
| Pilot runner Git blob | `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243` | VERIFIED |
| Pilot artifact schema Git blob | `c620d3755a645c5f2ad14124f42ce07a1c670c5f` | VERIFIED |
| Protocol version encoded by runner | `0.7.5` | SELECTED / PRE-FREEZE |

Exact-candidate run `33939955138` supplies deterministic reproduction, environment/toolchain, dependency, RNG-stream, and topology-fingerprint evidence. PR #247 bound the identities into the authoritative control plane and merged as signed commit `2e325acd…`.

Post-merge Governance CI `33945464907` and PDMAL Pre-Authorization Security `33945464908` both completed successfully, including locked P8 analysis tests, artifact-schema tests, execution-contract tests, durable-retention tests, adversarial controls, formal-model verification, and explicit confirmation that contract mode remains non-empirical.

Accordingly, P5 is CLOSED / VERIFIED for provenance/reproducibility. See `docs/experiment/P5_PROVENANCE_REPRODUCIBILITY_ATTESTATION_2026-09-05.md`.

## P4 custody boundary — still OPEN

The canonical control is now `docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md`.

P4-A requires effective control separation, not a mandatory two-human topology. The permitted modes are:

- `H`: genuinely distinct human Key Custodian;
- `I`: institutional/third-party custody outside the analyst's unilateral control;
- `T`: independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

Every mode requires nonce-hardened commitments, timestamp ordering, a complete control-path inventory, evidence that the execution/analysis principal cannot recover protected material by unilateral action before release, and independently inspectable review evidence.

No custody mode has been instantiated or accepted. P4 remains **OPEN / NOT EXECUTED** operationally.

## Verified runtime/artifact context

- **P2 — CLOSED / VERIFIED:** run `33730195621`, artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- **P3 — CLOSED / VERIFIED:** run `33939955138`, artifacts `9961526468` / `9961526662`; structural/contract evidence only.
- **P6 — CLOSED / VERIFIED:** independent archive/retrieval/hash equality for retained evidence set.
- **P6a — CLOSED / VERIFIED:** run `33728695806`, artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

The P2 valid-request HTTP 503 / `BLOCKED` outcome is expected fail-closed contract behavior because live audit state is not wired; it is not general application-health evidence.

## P7/P8/P9 boundary

P7's scientific target is adopted, and P5 is closed, but P7 final exact binding remains blocked by actual P4-A custody evidence plus final protocol/control-plane identities.

P8 remains **OPEN / FAIL-CLOSED**. Exact analysis identities are bound, but an immutable freeze has not been constructed or independently verified.

P9 remains **NOT EXECUTED** for the final frozen chain. It must be independently produced after the final pre-freeze evidence tuple is complete.

## Remaining closure blockers

1. Instantiate and independently verify one acceptable P4-A custody mode.
2. Complete P7 exact final binding, including actual P4 custody evidence and final protocol/control-plane identities.
3. Construct the immutable P8 freeze and independently verify it.
4. Execute final independent P9 verification of the frozen chain.
5. Record separate pilot authorization.
6. Only then permit blinded empirical execution.

## Protocol/candidate separation rule

The executable apparatus, protocol, control-plane documentation, deployment state, synthetic evidence, custody mechanism, and empirical artifacts are separate provenance objects. A green CI run, READY deployment, procedure document, preregistration, custody product, or synthetic blinding result does not constitute empirical data or authorization.

## Explicit non-claims

P5 closure and this reconciliation do **not** create a freeze, authorize a pilot, execute P4 custody, authorize unblinding, establish efficacy, or increase empirical N.

**P4-A custody: OPEN / NOT EXECUTED.**  
**P7: ADOPTED / FINAL BINDING OPEN.**  
**P8: OPEN / FAIL-CLOSED.**  
**P9: NOT EXECUTED.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
