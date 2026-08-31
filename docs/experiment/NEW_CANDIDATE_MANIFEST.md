# NEW CANDIDATE MANIFEST — post-#151 reconciliation cycle (HISTORICAL)

```yaml
manifest_version: 1
designation_event: HISTORICAL_CANDIDATE_SUPERSEDED
state: HISTORICAL / SUPERSEDED
new_candidate_sha: null
new_candidate_tree_sha: null
remediation_source:
  pr: 151
  pr_state: MERGED
  merge_commit: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
  merged_at: 2026-08-30T19:55:05Z
superseded_by:
  reason: authorized P-31/P-33 RESTORE and subsequent preflight hardening change the apparatus lineage; a fresh candidate must be derived after the complete seven-gate treatment is assembled
  apparatus_restore_base: 02e4c958e435f1faaa6fbf15909f9141ed2a6e39
prior_candidate:
  sha: c6157158bf0ee4840e99a381a4b99bd2febe2302
  status: HISTORICAL / PRE-REMEDIATION
  note: its P3-P9 package is NOT transferred
historical_evidence_marker: docs/experiment/CANDIDATE_RECONCILIATION_RECORD.md
designation_control_commit: 02c146d1e0cdc423948ac0dfa11e98f812edfb44
designation_control_commit_role: CONTROL RECORD ONLY; NOT APPARATUS IDENTITY
current_main_documentation_lineage: documentation/control-plane lineage; resolve from git ref
recovery_basis:
  issue: 152
  operator_corroboration: measurement-identity != statistical-association; FAIL-CLOSED preferred over false restoration
historical_gate_ledger:
  P31_SCPE: SUPERSEDED_BY_RESTORE
  P27_KAPPA: FAIL-CLOSED
  P29_SENTINEL: FAIL-CLOSED
  P32_PHI: FAIL-CLOSED
  P30_APOGEE: FAIL-CLOSED
  P33_CONVERGENCE: SUPERSEDED_BY_RESTORE
  DEMIJOULE: FAIL-CLOSED
historical_runtime_evidence:
  P2_RUNTIME: VERIFIED (scope 303f4424 — historical only)
  P6a_CORS: VERIFIED (scope 303f4424 — historical only)
  P3_P8: OPEN / FAIL-CLOSED
  P9: NOT EXECUTED
new_candidate_required: true
authorization: NOT GRANTED
empirical_n: 0
```

## Identity roles

- `05fa2866…` — historical post-#151 apparatus/candidate source identity; no longer the active candidate.
- `02e4c958…` — restored P-31/P-33 apparatus source boundary from PR #160; not itself the final candidate for the completed seven-gate treatment.
- `02c146d1…` — historical designation/control record; not an apparatus identity.
- `c6157158…` — superseded pre-remediation candidate; provenance only.
- `303f4424…` — prior production/runtime evidence boundary for P2/P6a; non-transferable.

## Promotion rule

This document is historical and must not be used to infer the identity of the next candidate. After the authorized restoration work is complete, derive one fresh immutable candidate source identity from the complete apparatus and bind all candidate-scoped evidence to it.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
