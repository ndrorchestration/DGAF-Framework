# Solo Pilot QC Adjudication — 2026-09-07

> **Current-authority note — 2026-09-07:** `HISTORICAL PROSPECTIVE DECISION — SUPERSEDED FOR FUTURE EXECUTION AUTHORITY`. The blinded-QC decision below correctly records the evidence available before Solo final experiment 001. The subsequent 50-seed experiment exposed the missing P-30 treatment binding and is retained as apparatus-falsification evidence. Therefore the historical instruction to continue to the 50-seed final experiment has been consumed and does not authorize any fresh empirical epoch. See `SOLO_P30_REMEDIATION_EPOCH_002_ADJUDICATION.md`, `SOLO_FINAL_EXPERIMENT_001_RETIREMENT.md`, and Issue #369.

## Scope

This record adjudicates only the blinded structural/QC evidence from Solo Pilot run 001. No condition mapping was released and no blinded outcome field was inspected for this decision.

## Bound evidence

- Validation track: `SOLO_DEVELOPER`
- GitHub Actions run: `34121633864`
- Exact run SHA: `45070734434b19520c0855a136a5eaaff88766ff`
- Evidence artifact: `10018546764`
- Evidence artifact digest: `sha256:58510cd0e35b21435d2b6e4dd0b1a345d6d5596dd748d76ec0dd2b1c5be2b463`
- Recoverable blinding-key artifact: `10018547263`
- Key artifact digest: `sha256:5e414c47060ef37c8a9dd52b936dec66d9d8ad04723e26610dfe98d0d3ed74fc`
- Seeds: `20260819`, `20260820`
- Records per seed: `180`
- Retained empirical observations: `360`
- Collection workflow outcome inspection: `false`

## Blinded QC findings

The retained collection manifest and seed artifacts establish, without reading outcome values:

1. both expected seed artifacts are present;
2. each seed artifact contains the canonical 180-cell matrix;
3. both seed SHA-256 sidecars match the retained JSON bytes;
4. the run is exact-SHA-bound and reports `protocol_status=FROZEN` for the Solo track;
5. the evidence and recoverable-key artifacts were retained separately;
6. the collection workflow records `outcomes_inspected_by_collection_workflow=false`;
7. no independent verification or independent custody is claimed.

**QC adjudication: PASS_STRUCTURAL_BLINDED_SOLO.**

This means the apparatus was acceptable, based on the evidence then available, for the subsequently executed Solo empirical collection. It is not an efficacy result, statistical result, independent validation result, or High-Assurance acceptance. Later apparatus-falsification evidence supersedes this record as future execution authority without rewriting the historical QC finding.

## Sample-size adjudication

The scientific protocol defines the primary point estimator over the **50-seed panel**. The 2-seed Solo Pilot was therefore insufficient for the locked primary analysis and was not to be unblinded or interpreted as the final experiment.

**Historical decision at this checkpoint: CONTINUE TO FRESH 50-SEED SOLO FINAL EXPERIMENT.**

That decision was subsequently exercised by Solo final experiment 001 and is now consumed. It must not be reused as authorization for epoch 003 or any other fresh empirical run.

The final Solo experiment requirements recorded at this checkpoint were:

- use a fresh single protected blinding key for the complete 50-seed collection;
- execute exactly 50 root seeds beginning with the protocol runner's deterministic seed sequence;
- retain exactly `50 × 180 = 9,000` blinded observations;
- bind all artifacts to one exact run SHA;
- perform structural validation without inspecting outcome fields;
- retain the recoverable blinding key separately under the explicitly limited same-system Solo custody model;
- lock the completed dataset before any authorized key release or outcome analysis.

Run 001 remains retained as pilot/QC evidence and is not pooled into the final 50-seed analysis dataset.

## Claim boundary

At the time of this QC adjudication:

- Solo Pilot: `EXECUTED / BLINDED QC PASS / N=360`
- Solo final experiment: `AUTHORIZED NEXT / NOT YET EXECUTED / N=0`
- High-Assurance track: unchanged; `NOT AUTHORIZED / N=0`

Current authority after the later final experiment and P-30 diagnostic is recorded elsewhere and is controlling for future action:

- Solo final experiment 001: `EXECUTED / APPARATUS_FALSIFICATION_EVIDENCE / NOT EFFICACY EVIDENCE`
- P-30 diagnostic epoch 002: `PASS / NON_EMPIRICAL / SCIENTIFIC_N_INCREMENT=0`
- Fresh Solo empirical epoch: `NOT AUTHORIZED`
- Canonical High-Assurance track: `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`

No unblinding or fresh empirical execution is authorized by this record.
