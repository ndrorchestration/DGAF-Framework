---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-05
control_plane_reconciliation_base: 4382a7b745c1abde3a68eb7848611412f5bd34d7
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
runtime_candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# PDMAL Current Control State

This is the current pre-authorization control record. Documentation/control-plane descendants do not replace the designated runtime candidate unless the canonical candidate identity is explicitly changed.

## Current gate state

| Control | State | Evidence / scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Runtime candidate lineage | VERIFIED | candidate `7c1cc4bb…`; tree `586c00d6…` |
| Candidate deployment | VERIFIED | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`, READY production, exact Git source `7c1cc4bb…` |
| P1 Candidate Integrity | CLOSED / VERIFIED | exact apparatus/source, candidate/tree, provenance, deployment identity |
| P2 Runtime | CLOSED / VERIFIED | run `33730195621`; artifact `9883521704`; five-case authenticated matrix |
| P3 Artifact Contract | CLOSED / VERIFIED | run `33939955138`; artifacts `9961526468` / `9961526662`; structural scope |
| P4 Security / Blinding | OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED | canonical procedure now supports Mode H human, Mode I institutional, or Mode T independently enforced technical custody; no custody mode has yet been instantiated or verified |
| P5 Provenance / Reproducibility | CLOSED / VERIFIED | exact analysis/config/runner/schema identities bound by merge `2e325acd…`; post-merge Governance CI `33945464907` and Pre-Authorization Security `33945464908` PASS |
| P6 Durable Evidence Custody | CLOSED / VERIFIED | independent archive/retrieval/SHA-256 equality for retained evidence set |
| P6a CORS | CLOSED / VERIFIED | run `33728695806`; artifact `9882965299`; four-case authenticated matrix |
| P7 Scientific Target | ADOPTED / FINAL BINDING OPEN | final binding blocked by actual P4-A custody evidence and final pre-freeze identities |
| P8 Analysis Lock | OPEN / FAIL-CLOSED | analysis identities bound; immutable freeze not created/verified |
| P9 Independent Verification | NOT EXECUTED / OPEN | final independent frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance decision |
| Empirical data | N = 0 | no authorized pilot observation |

## P5 closure basis

The designated candidate's analysis-control identities are fixed as:

- analysis implementation blob `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`;
- deterministic analysis configuration SHA-256 `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`;
- pilot runner blob `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243`;
- pilot artifact schema blob `c620d3755a645c5f2ad14124f42ce07a1c670c5f`;
- protocol version `0.7.5`.

The analysis configuration digest was independently recomputed and matched exactly. Exact-candidate run `33939955138` supplies candidate/tree, protocol/dependency, toolchain/environment, deterministic reproduction, environment fingerprint, RNG separation, and topology-determinism evidence. PR #247 bound these identities to the authoritative control plane and merged as signed commit `2e325acdde74dde50d3d4dc4f493a834fbd28eb2`.

Post-merge Governance CI `33945464907` completed successfully, including isolated hash-pinned E2b/M6 evidence, compilation, P8 analysis/artifact tests, authority tests, provenance artifacts, pinned TLA+ retrieval, and bounded model checking. PDMAL Pre-Authorization Security `33945464908` also completed successfully, including adversarial controls, locked P8 analysis tests, artifact-schema tests, execution-contract tests, retention tests, and explicit non-empirical contract-mode verification.

Accordingly, P5 is CLOSED / VERIFIED for provenance/reproducibility only. This is not efficacy evidence.

## P4 boundary

`docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md` is now the canonical P4 procedure. P4 is defined by effective control separation rather than a mandatory two-human topology.

Permitted modes are:

- **H:** genuinely distinct human Key Custodian;
- **I:** institutional/third-party custody outside the analyst's unilateral control;
- **T:** independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

The requirement is unchanged in substance: before the predeclared release condition, the execution/analysis principal must be unable to recover the raw key, cleartext mapping, commitment nonces, or equivalent recovery material by unilateral action.

No mode has yet been instantiated. P4 remains OPEN / NOT EXECUTED operationally.

## Remaining closure sequence

`real independently enforceable P4-A custody → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

No completed gate above authorizes empirical execution or changes empirical N.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
