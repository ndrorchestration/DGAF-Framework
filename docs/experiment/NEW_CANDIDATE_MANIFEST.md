# NEW CANDIDATE MANIFEST — post-#170 restoration cycle

```yaml
manifest_version: 4
designation_event: NEW_CANDIDATE
state: PRE-FREEZE / FAIL-CLOSED
apparatus_source_sha: d56b5b3c44e39ddb8c883259584432ab39259306
apparatus_source_tree_sha: 8c13900c4ce2a503414f9dddf1d7ef7debead57e
candidate_designation: PROVISIONAL / POST-RESTORE
candidate_designation_rule: exact restored apparatus source; no prior empirical evidence transfers
prior_candidate:
  sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
  status: HISTORICAL / SUPERSEDED BY #170 RESTORATION
  note: prior P3-P9 package is NOT transferred
restoration_source:
  pr: 170
  pr_state: MERGED
  merge_commit: d56b5b3c44e39ddb8c883259584432ab39259306
  merged_at: 2026-08-31T07:03:16Z
provenance_source:
  pr: 169
  state: ABSORBED INTO #170
  head: 9123dc4a2b5b9859e3cf0ebde4d18202ba6b01d7
deployment_binding:
  deployment_id: dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
  deployment_url: https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app
  deployment_target: production
  deployment_state: READY
  source_sha_match: true
  allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
  provenance_basis: Vercel deployment metadata + prior successful P6a CORS record for configured allowed origin
  prior_p6a_evidence: HISTORICAL / NON-TRANSFERABLE
  prior_p6a_candidate_sha: 303f4424d2198f0d0cf76305c589263dd1e417dc
assurance:
  control_state: docs/governance/CONTROL_STATE_2026-08-31.yaml
  adversarial_matrix: docs/governance/ADVERSARIAL_PRE_FREEZE_ASSURANCE_MATRIX_2026-08-31.md
  consistency_validator: scripts/validate_control_state.py
  drift_guard_workflow: .github/workflows/control-state-consistency.yml
gate_ledger:
  P31_SCPE: RESTORED_ON_APPARATUS
  P27_KAPPA: RESTORED_ON_APPARATUS
  P29_SENTINEL: RESTORED_ON_APPARATUS
  P32_PHI: RESTORED_ON_APPARATUS
  P30_APOGEE: RESTORED_ON_APPARATUS
  P33_CONVERGENCE: RESTORED_ON_APPARATUS
  DEMIJOULE: RESTORED_ON_APPARATUS
  P2_RUNTIME: NOT_VERIFIED_FOR_THIS_CANDIDATE
  P6a_CORS: NOT_VERIFIED_FOR_THIS_CANDIDATE
  P3_P9: NOT_VERIFIED_FOR_THIS_CANDIDATE
  P9: NOT_EXECUTED
authorization: NOT GRANTED
empirical_n: 0
```

## Identity roles

- `d56b5b3c…` — current restored apparatus source and provisional candidate designation basis.
- `9123dc4a…` — provenance-integration head absorbed into #170; not the final apparatus identity.
- `05fa2866…` — superseded historical post-#151 candidate; no empirical package transfers.
- `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb` — exact current production deployment for the restored apparatus source.
- `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app` — exact current deployment URL.
- `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app` — configured allowed CORS origin recovered from the prior successful P6a contract execution; it is an input value, not new evidence.
- Any subsequent documentation-only commit changes `main` documentation lineage, not `apparatus_source_sha`.
- Deployment identity remains separate from both `main` tip and apparatus source SHA.

## Assurance controls

The candidate is subject to the machine-readable control state, adversarial pre-freeze assurance matrix, and automated control-state consistency validator named above. Core identity, null-integrity, blinding, artifact-integrity, protocol, analysis, independence, and authorization failures remain fail-closed.

## Promotion rule

This manifest designates the exact restored apparatus source for the new candidate cycle. It does **not** create a freeze, authorize the pilot, or promote prior P2/P6a/P3-P9 evidence. All runtime and experimental predicates must be freshly established against this exact apparatus and its candidate-bound deployment.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
