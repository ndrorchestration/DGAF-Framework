# NEW CANDIDATE DESIGNATION MANIFEST — TEMPLATE (do not apply without explicit go-ahead)

This template is filled in ONLY after PR #151 is merged onto `main` and the resulting tree is inspected.
It is the designation act (irreversible governance event). Until then it stays a template.

```yaml
# ALL FIELDS BELOW ARE PLACEHOLDERS — populate from the post-merge main tree.
manifest_version: 1
designation_event: NEW_CANDIDATE  # created by reconciled remediation cycle (PR #151)
state: PRE-FREEZE / FAIL-CLOSED    # until independent P9 passes
new_candidate_sha: <POST-MERGE-MAIN-SHA>
new_candidate_tree_sha: <POST-MERGE-MAIN-TREE-SHA>
remediation_source:
  pr: 151
  head: 83f93c6725672c8c1bf6e687e454403456ea8c21
  tree: eb40c67d9b06a171a8f6f01d2bfe482e54d5098e
prior_candidate:
  sha: c6157158bf0ee4840e99a381a4b99bd2febe2302
  status: HISTORICAL / PRE-REMEDIATION  # its P3–P9 package is NOT transferred
historical_evidence_marker: docs/experiment/CANDIDATE_RECONCILIATION_RECORD.md
recovery_basis:
  r1_r4_matrix: .hermes/work/R1_R4_GATE_RECOVERY_MATRIX.md
  issue: 152
gate_ledger:
  P31_SCPE: FAIL_CLOSED
  P27_KAPPA: FAIL_CLOSED
  P29_SENTINEL: FAIL_CLOSED
  P32_PHI: FAIL_CLOSED
  P30_APOGEE: FAIL_CLOSED (partial recovery)
  P33_CONVERGENCE: FAIL_CLOSED
  DEMIJOULE: FAIL_CLOSED
  P2_RUNTIME: VERIFIED (scope 303f4424 — re-execute for new candidate)
  P6a_CORS: VERIFIED (scope 303f4424 — re-execute for new candidate)
  P3_P8: OPEN / FAIL_CLOSED (require candidate-bound verification)
  P9: NOT EXECUTED (require independent pass post-designation)
authorization: NOT GRANTED
empirical_n: 0
```

## Application procedure (explicit go-ahead required)

1. Merge PR #151 onto `main` (`da1f948…`).
2. `git rev-parse HEAD` (post-merge main) → fill `new_candidate_sha`.
3. `git rev-parse HEAD^{tree}` → fill `new_candidate_tree_sha`.
4. Write a frozen `NEW_CANDIDATE_MANIFEST.md` on a new branch `experimental-candidate/<date>-post151`.
5. Present for operator approval; push only after explicit approval.
6. Then proceed to candidate-bound R5 implementation / P3–P8 / P9.

No pilot executes; N stays 0 until authorization.
