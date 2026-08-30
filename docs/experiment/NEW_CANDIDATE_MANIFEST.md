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

## Next required steps (irreversible acts, explicit go-ahead)

1. Fresh candidate-scoped P2/P6a execution against `new_candidate_sha` (current VERIFIED scope is `303f4424`, does NOT extend).
2. Candidate-bound P3-P8 verification.
3. Independent P9 pass.
4. Freeze (separate, post-P9).
5. Authorization -> only then pilot.

Until step 3, the candidate is PRE-FREEZE. No pilot executes; N stays 0.

**Boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.
