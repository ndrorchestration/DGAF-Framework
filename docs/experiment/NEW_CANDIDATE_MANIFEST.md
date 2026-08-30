# NEW CANDIDATE MANIFEST — post-#151 reconciliation cycle

```yaml
manifest_version: 1
designation_event: NEW_CANDIDATE
state: PRE-FREEZE / FAIL-CLOSED   # until independent P9 passes
new_candidate_sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
new_candidate_tree_sha: dd662325149c42843d5ca99178ca4399fde6f440
remediation_source:
  pr: 151
  pr_state: MERGED
  merge_commit: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
  merged_at: 2026-08-30T19:55:05Z
prior_candidate:
  sha: c6157158bf0ee4840e99a381a4b99bd2febe2302
  status: HISTORICAL / PRE-REMEDIATION
  note: its P3-P9 package is NOT transferred; see docs/experiment/CANDIDATE_RECONCILIATION_RECORD.md
historical_evidence_marker: docs/experiment/CANDIDATE_RECONCILIATION_RECORD.md
designation_control_commit: 02c146d1e0cdc423948ac0dfa11e98f812edfb44
designation_control_commit_role: CONTROL RECORD ONLY; NOT APPARATUS IDENTITY
recovery_basis:
  r1_r4_matrix: .hermes/work/R1_R4_GATE_RECOVERY_MATRIX.md
  issue: 152
  operator_corroboration: measurement-identity != statistical-association; FAIL-CLOSED preferred over false restoration
gate_ledger:
  P31_SCPE: FAIL-CLOSED
  P27_KAPPA: FAIL-CLOSED (contradiction: code 0.28/0.25 vs docs 0.22/0.18)
  P29_SENTINEL: FAIL-CLOSED (contradiction: doc HALT vs audit-only code)
  P32_PHI: FAIL-CLOSED (missing KILL_REC band; phi anchor consistent conjugate)
  P30_APOGEE: FAIL-CLOSED (partial recovery; stub insufficient)
  P33_CONVERGENCE: FAIL-CLOSED (W_t substrate absent; current_final_std != proxy)
  DEMIJOULE: FAIL-CLOSED (six-axis substrate absent)
  P2_RUNTIME: VERIFIED (scope 303f4424 — re-execute for this candidate)
  P6a_CORS: VERIFIED (scope 303f4424 — re-execute for this candidate)
  P3_P8: OPEN / FAIL-CLOSED (require candidate-bound verification)
  P9: NOT EXECUTED (require independent pass post-designation)
authorization: NOT GRANTED
empirical_n: 0
```

## Identity roles

- `05fa2866…` — post-#151 apparatus/candidate source identity.
- `02c146d1…` — designation/control record; not the apparatus identity.
- `291b2adb…` — current `main` documentation/evidence lineage; documentation-only relative to the designated apparatus unless executable apparatus changes occur.

## Promotion rule

This manifest records candidate designation only. It does not create a freeze, authorize the pilot, or promote prior P2/P6a evidence. Any substantive apparatus change after `05fa2866…` requires candidate re-identification.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
