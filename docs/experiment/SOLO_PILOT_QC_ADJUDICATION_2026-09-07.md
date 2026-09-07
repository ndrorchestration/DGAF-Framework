# Solo Pilot QC Adjudication — 2026-09-07

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

This means the apparatus is acceptable for continued Solo empirical collection. It is not an efficacy result, statistical result, independent validation result, or High-Assurance acceptance.

## Sample-size adjudication

The scientific protocol defines the primary point estimator over the **50-seed panel**. The 2-seed Solo Pilot is therefore insufficient for the locked primary analysis and must not be unblinded or interpreted as the final experiment.

**Decision: CONTINUE TO FRESH 50-SEED SOLO FINAL EXPERIMENT.**

The final Solo experiment must:

- use a fresh single protected blinding key for the complete 50-seed collection;
- execute exactly 50 root seeds beginning with the protocol runner's deterministic seed sequence;
- retain exactly `50 × 180 = 9,000` blinded observations;
- bind all artifacts to one exact run SHA;
- perform structural validation without inspecting outcome fields;
- retain the recoverable blinding key separately under the explicitly limited same-system Solo custody model;
- lock the completed dataset before any authorized key release or outcome analysis.

Run 001 remains retained as pilot/QC evidence and is not pooled into the final 50-seed analysis dataset.

## Claim boundary

After this adjudication:

- Solo Pilot: `EXECUTED / BLINDED QC PASS / N=360`
- Solo final experiment: `AUTHORIZED NEXT / NOT YET EXECUTED / N=0`
- High-Assurance track: unchanged; `NOT AUTHORIZED / N=0`

No unblinding is authorized by this record.
