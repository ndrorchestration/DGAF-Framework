---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-31
supersedes_sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
applies_to_sha: d56b5b3c44e39ddb8c883259584432ab39259306
scope_note: >-
  This index records evidence and gate state. Historical evidence remains
  scoped to the exact SHA/run that produced it. Candidate verification does
  not inherit historical verification automatically. The post-#170 restored
  apparatus (PR #170, `d56b5b3c…`) is the current designated evidence target;
  the prior post-#151 candidate `05fa286…` is now HISTORICAL. No freeze or
  authorization is implied.
---

# PDMAL Evidence Index

This is a control-plane registry, not empirical evidence and not a self-authorizing freeze record.

## Evidence inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Current documentation lineage | CURRENT | `main` | Active control/documentation lineage |
| Current restored apparatus (post-#170) | DESIGNATED / NOT FROZEN | `d56b5b3c…` | Exact target for the current candidate-scoped evidence cycle |
| Prior post-#151 apparatus candidate | SUPERSEDED / HISTORICAL | `05fa286…` | Historical candidate; no evidence transfers to `d56b5b3c…` |
| Candidate designation/control record | CONTROL RECORD | `02c146d1…` | Records designation only; not apparatus identity |
| Prior pre-remediation candidate | SUPERSEDED / HISTORICAL | `c6157158…` | Prior candidate cycle; evidence does not transfer |
| Candidate deployment provenance | VERIFY REQUIRED | post-#170 candidate | Exact deployment must be checked against `d56b5b3c…` before runtime closure |
| Production source provenance | CLOSED / VERIFIED | `303f4424…` → `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8` | Prior engineering/runtime boundary |
| Historical experimental verification boundary | HISTORICAL / CANDIDATE-SCOPED | `ac8ea267…` | Historical provenance only |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b868…` | Historical apparatus only |
| Corrected pilot runner | IMPLEMENTED / EVIDENCE GATED | runner/schema controls | Current candidate execution evidence still required |
| TGL contract | CURRENT ENGINEERING CONTROL / VERIFIED | post-#151 lineage | Engineering control evidence; not experimental authorization |
| Environment lock | VERIFY | CI dependency/runtime configuration | Final candidate must bind exact environment fingerprint |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Run `32112658368` | Operational characterization, not efficacy evidence |
| Blinding operational verification | CLOSED FOR SYNTHETIC VERIFICATION | Run `32113226935` | Synthetic/control evidence only |
| Artifact contract | IMPLEMENTED / OPEN | `pilot_artifact_schema.py` + tests | Fresh current-candidate execution evidence required |
| Security controls | VERIFIED FOR ENGINEERING SCOPE | current Governance/PDMAL security CI | Does not substitute for P4 operational custody |
| Topology provenance | VERIFY | `PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` | Recompute/bind against exact current candidate |
| Durable retention | OPEN | policy | Operational archive + independent retrieval/hash proof required |
| Primary contrast | ADJUDICATED / BINDING PENDING | `dgaf` vs `null`; FFCR; paired seed | Exact final candidate/freeze binding remains required |
| Analysis lock | OPEN / FAIL-CLOSED | P8 control plan | Exact final candidate/configuration binding required |
| P2 runtime | PRIOR VERIFIED / CURRENT CANDIDATE OPEN | Run `33300481208`; artifact `9728767844`; candidate `303f4424…` | Five-case authenticated runtime evidence; prior-candidate scope only |
| P6a CORS runtime | PRIOR VERIFIED / CURRENT CANDIDATE OPEN | Run `33302495240`; artifact `9729387603`; candidate `303f4424…` | Four-case authenticated CORS evidence; prior-candidate scope only |
| Independent verification | NOT EXECUTED | P9 design | Must verify the current candidate evidence chain independently |

## Candidate identity boundary

- `303f4424…` is the exact prior P2/P6a production/runtime evidence boundary.
- `c6157158…` is the superseded pre-remediation candidate.
- `05fa286…` is the post-#151 apparatus/source identity and is now HISTORICAL (superseded by `d56b5b3c…` via PR #170); its evidence does not transfer.
- `02c146d1…` is the designation/control record for `05fa286…`.
- `d56b5b3c…` is the current restored apparatus/source identity (PR #170) and the current designated candidate basis.
- `main` is the documentation/evidence lineage and is not itself the apparatus identity.

## Evidence inheritance rule

Historical P2/P6a evidence bound to `303f4424…` is not evidence for `d56b5b3c…`. Pre-#151 P3–P9 evidence bound to `c6157158…` is historical/pre-remediation evidence and is not closure for `d56b5b3c…`. Evidence bound to the historical `05fa286…` candidate does not transfer to `d56b5b3c…`.

A later documentation/control commit does not redefine the apparatus candidate unless executable apparatus behavior changes.

## Current candidate execution boundary

The current designated apparatus candidate is `d56b5b3c44e39ddb8c883259584432ab39259306` (PR #170, seven-gate restoration + provenance integration).

Before current-candidate P2/P6a closure, an exact deployment identity must be verified against this SHA. Deployment readiness is necessary provenance, not runtime verification.

## Remaining gate sequence

1. Verify exact current candidate/deployment identity.
2. Fresh P2 runtime verification.
3. Fresh P6a CORS verification.
4. Candidate-scoped P3 artifact evidence.
5. Issue #152 gate-contract reconciliation/adaptation work.
6. P4/P5/P6 current-cycle evidence.
7. P7 exact scientific/protocol/apparatus binding.
8. P8 analysis lock and closure.
9. Independent P9 verification.
10. New immutable freeze and independent verification.
11. Explicit pilot authorization.
12. Authorized blinded pilot execution.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
