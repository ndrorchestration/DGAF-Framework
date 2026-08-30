# Candidate Reconciliation Record — PR #151 Remediation Cycle

**Authoritative provenance marker for PR #151 (`83f93c6`, tree `eb40c67…`).**
This record is the R6 required-remediation: it declares the pre-existing `c6157158…`-bound
evidence package as **HISTORICAL / PRE-REMEDIATION**, not as evidence for the post-#151 apparatus.

**Boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0. No freeze, merge, or candidate designation performed here.

---

## 1. Provenance structure (canonical)

```text
c6157158…   (designated pre-remediation candidate)
   ├── P3–P9 evidence package (BELOW) — scoped to c6157158, HISTORICAL
   └── PR #151 remediation (83f93c6, tree eb40c67)
             ↓ merge onto main (da1f948…)
       NEW candidate SHA  (post-#151 main tree)
             ↓ designate (separate manifest commit, requires explicit go-ahead)
       candidate-bound R5 implementation → P3–P8 → independent P9 → freeze → auth
```

## 2. Stale candidate-bound records (declared HISTORICAL, do NOT bind new candidate)

These artifacts exist on the PR #151 branch and reference `c6157158bf0ee4840e99a381a4b99bd2febe2302`.
They are **pre-remediation evidence** and MUST NOT be promoted as closure for the post-#151 candidate:

|Artifact|Binding line|Status|
|---|---|---|
|`p3_runtime_evidence_c6157158.json`|`:2 candidate: c6157158…`|HISTORICAL|
|`P4_Security_Blinding_Attestation.md`|`:3 Candidate SHA c6157158…`|HISTORICAL|
|`docs/experiment/P5_REPRODUCIBILITY_RECORD.md`|`:1,:4,:10 c6157158…`|HISTORICAL|
|`docs/experiment/P6_DURABLE_CUSTODY_ATTESTATION.md`|`:5 c6157158…`|HISTORICAL|
|`docs/GOVERNANCE/P7_BINDING_RECORD_2026-08-30.md`|`:3,:15 c6157158…`|HISTORICAL|
|`docs/GOVERNANCE/P8_ANALYSIS_LOCK_RECORD_2026-08-30.md`|`:3,:13 c6157158…`|HISTORICAL|
|`docs/GOVERNANCE/P9_SECOND_PASS_2026-08-30.md`|`:5,:16,:20,:33–34,:50–51,:56–57,:62,:71,:83,:113,:132,:137–138 c6157158…`|HISTORICAL|

**Note on P9 (`4b62916`):** the prior freeze commit `4b62916` named `c6157158` as its candidate.
Per the corrected state, `4b62916` is a **candidate-binding evidence checkpoint**, NOT an authoritative experiment freeze
(freeze manifest self-declared `freeze_candidate_sha: NONE` at that point; P9 was OPEN; auth NOT granted). It is retained here as historical.

## 3. R6 preflight result (live GitHub, 2026-08-30)

- PR #151 head `83f93c6`, tree `eb40c67`. Base `main` `da1f948`. Open/DRAFT/MERGEABLE.
- Remediation head ≠ eventual post-merge main tree → `83f93c6` is **NOT** the new candidate.
- `c6157158` = merge base of remediation and prior main (per earlier reconciliation); cannot absorb #151.
- Vercel success status on `83f93c6` = deployment status, NOT experimental candidate verification.
- **Preflight: PASS WITH REQUIRED REMEDIATION** (this record satisfies the remediation).

## 4. P2 / P6a re-scope

P2 (runtime) and P6a (CORS) VERIFIED within scope `303f4424…` / `dpl_FbPSc3K9…` only.
That scope does **not** extend to `c6157158…` nor to the post-#151 candidate. Fresh candidate-scoped
P2/P6a execution is required before those gates are claimed VERIFIED for the new cycle.

## 5. Required next governance acts (irreversible — explicit operator go-ahead)

1. Reconcile the 7 HISTORICAL records in #151 so they read as pre-remediation (this record supplies the marker).
2. Merge PR #151 onto `main` (`da1f948…`).
3. Inspect resulting main tree; designate that exact tree as NEW candidate via a manifest commit
   (`freeze_candidate_sha` = NEW SHA, `state: PRE-FREEZE` until P9 passes).
4. Produce candidate-bound P3–P8 verification against NEW SHA.
5. Independent P9 pass.
6. Freeze (separate, post-P9).
7. Authorization (separate).

Until act 3, no candidate is designated; all subject gates remain FAIL-CLOSED per `R1_R4_GATE_RECOVERY_MATRIX.md`.
