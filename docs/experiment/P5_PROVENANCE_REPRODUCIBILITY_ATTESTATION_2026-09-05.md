# P5 Provenance / Reproducibility Attestation — 2026-09-05

**Status:** CLOSED / VERIFIED for designated candidate provenance/reproducibility scope  
**Designated runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Authoritative binding merge:** `2e325acdde74dde50d3d4dc4f493a834fbd28eb2`  
**Experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

## Claim being closed

P5 asks whether the designated candidate's reproducibility/provenance-critical identities are explicit, candidate-scoped, deterministic where required, and verified by retained executable checks. This attestation closes that bounded claim. It does not establish efficacy, P4 human custody, final P7/P8/P9 closure, freeze, authorization, unblinding, or empirical execution.

## Exact analysis-control identities

| Object | Exact identity |
|---|---|
| Analysis implementation | `experiments/pdmal_pilot/analysis.py` |
| Analysis implementation Git blob | `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` |
| Analysis configuration SHA-256 | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` |
| Pilot runner Git blob | `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243` |
| Pilot artifact schema Git blob | `c620d3755a645c5f2ad14124f42ce07a1c670c5f` |
| Protocol version encoded by runner | `0.7.5` |
| Bootstrap resamples | `10000` |
| Bootstrap seed | `20260823` |
| Alpha | `0.05` |

The analysis configuration SHA-256 was independently recomputed from the deterministic configuration serialization and matched the recorded value exactly.

## Candidate-scoped reproducibility evidence

Exact-candidate run `33939955138` verifies the designated candidate/tree and records the protocol/dependency identity, hash-locked dependency environment, deterministic contract reproduction, environment fingerprint, RNG child-stream separation, and topology fingerprint determinism. Its retained P3/P5 artifacts are:

- artifact `9961526468`, digest `sha256:ed947f8a2f21a1e1122a6e8950240ea4a3ebdec7aad04c4231698de2f250285b`;
- registry artifact `9961526662`, digest `sha256:d7f592b45e76978600b6f1a4f22cac4b97dfe5f60605accbd99b61c50e149e93`.

P6 separately verifies durable archive/retrieval/hash equality for the retained evidence set.

## Authoritative control-plane binding

PR #247 bound the exact analysis implementation/configuration/runner/schema identities into the canonical control plane. Its exact PR head `9d97cb21a4514a79d3cd86f39973c47cc1a6e177` completed all 17 returned workflow runs successfully before merge, including Governance CI and PDMAL Pre-Freeze Runner Validation.

PR #247 then merged as signed commit `2e325acdde74dde50d3d4dc4f493a834fbd28eb2`.

Post-merge verification on exact `2e325acd…` includes:

- Control-State Consistency — PASS;
- Validate Control-State HEAD Binding — PASS;
- Governance CI run `33945464907` — PASS, including isolated hash-pinned E2b/M6 evidence, Python compilation, P-42 tests, P8 pilot artifact/analysis tests, agent authority/Layer-0 governance tests, evaluation provenance, pinned TLA+ download, bounded model check, and evidence uploads;
- PDMAL Pre-Authorization Security run `33945464908` — PASS, including adversarial controls, locked P8 analysis tests, pilot artifact schema tests, execution-contract tests, durable-retention tests, and explicit verification that contract mode remains non-empirical.

These post-merge checks satisfy the previously outstanding authoritative-merge/consistency-review condition.

## P5 disposition

**P5 Provenance / Reproducibility: CLOSED / VERIFIED** for the designated candidate and the bounded provenance/reproducibility contract described above.

This closure means the exact analysis/reproducibility identities and deterministic evidence chain are established for the designated candidate. It does not mean the experiment has been frozen or run.

## Explicit non-claims

P5 closure does not:

- establish actual P4 human/key custody or access separation;
- close P7's final scientific identity binding;
- close P8 or create an immutable freeze;
- execute or close final independent P9 verification;
- authorize a pilot;
- authorize unblinding;
- establish DGAF/PDMAL efficacy;
- increase empirical N.

**P4 real custody: OPEN / NOT EXECUTED.**  
**P7: ADOPTED / FINAL BINDING OPEN.**  
**P8: OPEN / FAIL-CLOSED.**  
**P9: NOT EXECUTED.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
