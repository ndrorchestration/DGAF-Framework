---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-06
live_source_boundary: 972edd41f16c69c6912af08c7d6c3aa627fdd8a9
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
historical_runtime_evidence_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
historical_runtime_evidence_candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
historical_runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
final_candidate_status: NOT_DESIGNATED
final_candidate_tracker: 309
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# PDMAL Current Control State

This is the current pre-authorization control record. PR #308 advanced the apparatus to protocol v0.7.6 / artifact schema 1.1 at `972edd41f16c69c6912af08c7d6c3aa627fdd8a9`. The prior runtime candidate `7c1cc4bb…` retains valid exact-scope evidence but is now historical provenance only for final-candidate purposes. **Final v0.7.6 candidate is NOT DESIGNATED; Issue #309 is authoritative for reconstruction and evidence regeneration.**

The consolidated control-state anchor `89be386b…` remains valid for its control/provenance role and does not itself designate the final candidate. Neither `main`, a PR head, a deployment, nor a documentation checkpoint becomes the final candidate merely by recency.

## Current gate state

| Control | State | Evidence / scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Historical runtime-evidence lineage | VERIFIED AT EXACT SCOPE | candidate `7c1cc4bb…`; tree `586c00d6…`; evidence remains provenance-valid |
| Historical candidate deployment | VERIFIED AT EXACT SCOPE | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`, READY production, exact Git source `7c1cc4bb…` |
| Final v0.7.6 candidate | NOT DESIGNATED | Issue #309; exact immutable SHA/tree still pending |
| Historical P1/P2/P3/P5/P6/P6a closure | CLOSED / VERIFIED AT RECORDED SCOPE | does not automatically transfer to future final candidate; classification/reverification pending #309 |
| P4 Security / Blinding | OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED | canonical procedure supports Mode H, I, or T; no real custody mode has yet been instantiated or verified |
| P7 Scientific Target | ADOPTED / FINAL BINDING OPEN | blocked by final candidate identity, actual P4-A custody evidence, and final pre-freeze identities |
| P8 Analysis Lock | OPEN / FAIL-CLOSED | immutable freeze not created/verified |
| P9 Independent Verification | NOT EXECUTED / OPEN | final independent frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance decision |
| Empirical data | N = 0 | no authorized pilot observation |

## Historical P5 closure basis

For the `7c1cc4bb…` evidence boundary, the analysis-control identities were fixed as:

- analysis implementation blob `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`;
- deterministic analysis configuration SHA-256 `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`;
- pilot runner blob `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243`;
- pilot artifact schema blob `c620d3755a645c5f2ad14124f42ce07a1c670c5f`;
- protocol version `0.7.5`.

Those records remain valid evidence for that exact historical candidate. They are not silently promoted to protocol v0.7.6 or to the future final candidate. Issue #309 determines which identities/evidence require fresh binding, rerun, or archive/retrieval proof.

## P4 boundary

`docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md` is the canonical P4 procedure. P4 is defined by effective control separation rather than a mandatory two-human topology.

Permitted modes are:

- **H:** genuinely distinct human Key Custodian;
- **I:** institutional/third-party custody outside the analyst's unilateral control;
- **T:** independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

No mode has yet been instantiated. P4 remains OPEN / NOT EXECUTED operationally. Current Mode-T synthetic/mechanism CI does not establish real Confidential Space admission or P4 custody.

## Candidate reconstruction and remaining closure sequence

Issue #309 requires an explicit immutable v0.7.6-descended candidate after candidate-relevant P4 apparatus changes are settled. Historical evidence must then be classified as transferable by construct, historical only, source/structure re-verifiable, runtime/deployment re-verifiable, re-archive/rebind, or not yet executable.

`complete candidate-relevant P4 apparatus work → explicitly designate final v0.7.6 candidate → classify/regenerate identity-dependent evidence → close real P4-A custody → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

No completed engineering gate authorizes empirical execution or changes empirical N.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
