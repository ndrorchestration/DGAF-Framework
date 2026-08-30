# P9 Independent Verification — Second Pass Report

**Report date:** 2026-08-30
**Pass:** 2nd independent adversarial verification (required follow-up to `P9_INDEPENDENT_AUDIT_REPORT.md`)
**Candidate SHA:** `c6157158bf0ee4840e99a381a4b99bd2febe2302`
**Candidate Tree SHA:** `6195063e2e6e01069ddef8a25e90bfe9d8a3283c`
**Freeze Commit SHA (new frozen X):** `4b62916eb136005351a74d82d3c973be1cc79777`
**Freeze branch:** `experimental-candidate/2026-08-30-reconciled`
**Auditor role:** P9 independent verification — second pass, independent of candidate self-validation and of the 1st pass.
**Authorization state:** NOT GRANTED. Empirical N = 0. Pre-freeze.

---

## 1. Freeze Commit Verification (`git show 4b62916`)

The freeze commit `4b62916` ("freeze(candidate): bind c6157158 evidence chain + PDMAL freeze manifest") was read in full. Verification:

| Check | Result |
|---|---|
| Manifest names designated candidate `c6157158bf0ee4840e99a381a4b99bd2febe2302` | **PASS** — `freeze_candidate_sha: c6157158…` and `freeze_candidate_tree_sha: 6195063e…` |
| Manifest names the freeze commit itself | **PASS** — `freeze_commit_sha: THIS_COMMIT` |
| Evidence chain lists P3–P8 (candidate-scoped) | **PASS** — table present for P3/P4/P5/P6/P7/P8 |
| Evidence chain candidly marks P2/P6a as production-boundary and P9 as OPEN | **PASS** — residual-risk section carried, not hidden |

The freeze manifest explicitly states the candidate is documentation/lineage-only at commit time and its executable apparatus is the ancestral engineering source `303f4424…`. All evidence is bound to the exact candidate SHA named above. No value in the manifest authorizes pilot execution.

---

## 2. Evidence Artifact Existence (read via `git show 4b62916:<path>`)

| Required artifact | Task-specified path | Actual freeze-tree path | Status |
|---|---|---|---|
| P3 runtime evidence | `p3_runtime_evidence_c6157158.json` | same | **EXISTS** |
| P3 SHA256 record | `p3_runtime_evidence_c6157158.sha256` | same | **EXISTS** |
| P4 blinding attestation | `P4_Security_Blinding_Attestation.md` | same | **EXISTS** |
| P5 reproducibility record | `docs/experiment/P5_REPRODUCIBILITY_RECORD.md` | same | **EXISTS** |
| P6 durable custody attestation | `docs/experiment/P6_DURABLE_CUSTODY_ATTESTATION.md` | same | **EXISTS** |
| P7 binding record | `docs/governance/P7_BINDING_RECORD_2026-08-30.md` | `docs/GOVERNANCE/P7_BINDING_RECORD_2026-08-30.md` | **PATH-CASE MISMATCH (see §2.1)** |
| P8 analysis lock record | `docs/governance/P8_ANALYSIS_LOCK_RECORD_2026-08-30.md` | `docs/GOVERNANCE/P8_ANALYSIS_LOCK_RECORD_2026-08-30.md` | **PATH-CASE MISMATCH (see §2.1)** |

### 2.1 Path-casing discrepancy (new finding, minor)

The task brief and the freeze manifest's own Evidence-chain table reference the **lowercase** `docs/governance/...` paths. The artifacts are actually stored in the freeze tree under **uppercase** `docs/GOVERNANCE/...`. Git tree objects are case-sensitive, so the literal lowercase paths are **MISSING** in the freeze tree; the artifacts exist only at the uppercase paths.

- Functional impact: **none on a case-insensitive filesystem** (Windows/NTFS) — the files resolve and bind `c6157158`.
- Provenance impact: the freeze manifest's internal references do **not** exactly match the recorded tree paths. For a frozen, hash-bound tree this is a minor provenance defect: the manifest does not point at the byte-exact path it claims. Carried as residual risk R4.

### 2.2 P3 SHA256 integrity (independent recompute)

- Computed SHA256 of `p3_runtime_evidence_c6157158.json` as stored in tree `4b62916`: `60f9f4f7f670ca61ad4f3493808aa58d18c7dded162f107bbeb941c5d7d0ce3d`
- Recorded in `p3_runtime_evidence_c6157158.sha256`: `60f9f4f7f670ca61ad4f3493808aa58d18c7dded162f107bbeb941c5d7d0ce3d`
- **MATCH: PASS.** P3 content is internally consistent and tamper-evident.

### 2.3 Candidate binding of every artifact

Each artifact was grepped for `c6157158bf0ee4840e99a381a4b99bd2febe2302`:
- `p3_runtime_evidence_c6157158.json` → 1 mention (candidate field) + references designated deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` (distinct from production `dpl_FbPSc3K9…`) → genuinely **candidate-scoped**.
- `P4_Security_Blinding_Attestation.md` → 1 mention.
- `P5_REPRODUCIBILITY_RECORD.md` → 1 mention.
- `P6_DURABLE_CUSTODY_ATTESTATION.md` → 1 mention.
- `docs/GOVERNANCE/P7_BINDING_RECORD_2026-08-30.md` → 1 mention (tree `6195063e…`); binds 12 adjudication fields + P8 impl/config SHAs.
- `docs/GOVERNANCE/P8_ANALYSIS_LOCK_RECORD_2026-08-30.md` → 2 mentions; locks analysis impl `463c70ee…` and config `6cab3f1e…` to `c6157158`.

**All six evidence artifacts exist in the freeze tree and bind the designated candidate.** P3–P8 candidate-scoped evidence chain is complete and internally consistent.

---

## 3. Re-examination of the 6 Prior Findings

### Finding 1 — Candidate is documentation-only / SHA-manifest mismatch
**Status: RESOLVED.** At the 1st-pass candidate tree, `FREEZE_MANIFEST.md` said `freeze_candidate_sha: NONE`. The freeze commit `4b62916` now records `freeze_candidate_sha: c6157158…` and `freeze_commit_sha: THIS_COMMIT`, with the exact candidate tree `6195063e…` named. The exact-tree binding is preserved: the manifest is the authoritative freeze artifact, and it explicitly names the candidate rather than denying it.

### Finding 2 — Post-candidate commits on `origin/main` (retroactive documentation)
**Status: RESOLVED / ACKNOWLEDGED.** The temporal retroactive-doc pattern is closed by the creation of a dedicated, authoritative freeze commit (`4b62916`) that explicitly binds the candidate and transparently records the documentation-only lineage and the ancestral engineering source `303f4424…`. The freeze manifest documents rather than hides the lineage. The pattern risk is mitigated by the explicit freeze boundary.

### Finding 3 — P9 had never been executed
**Status: RESOLVED by this pass.** The 1st adversarial pass (`P9_INDEPENDENT_AUDIT_REPORT.md`) is retained. This 2nd independent pass is now complete. P9 has received two independent adversarial passes; the "never executed" gap is closed (verdict below remains conditional on residual risks, not on P9 execution itself).

### Finding 4 — Evidence monoculture (P2/P6a/E2b/M6 all GitHub Actions)
**Status: OPEN — explicitly carried.** The freeze manifest's Residual-risks section states verbatim: *"P9 Finding 4 (evidence monoculture): ... No independent second canonicalization+hash path exists. P9 closure requires that path; recorded as OPEN until established."* No independent second evidence path was introduced by the freeze. **This finding remains OPEN.**

### Finding 5 — Authority-matrix historical-alias test not candidate-scoped
**Status: OPEN — not addressed by freeze.** The freeze adds P7 scientific-field binding and P8 analysis-implementation/config SHA locks, but does **not** include candidate-scoped verification of authority-identity (the historical-alias vs active-seat regression test `58a6964` remains an ancestor of the engineering source, not exercised against the exact `c6157158` tree). Authority-identity coherence is asserted, not independently verified for the candidate boundary.

### Finding 6 — P1–P9 matrix references post-candidate SHAs / circular reference
**Status: RESOLVED / ADDRESSED.** The new freeze manifest replaces the ambiguous matrix references with explicit exact-SHA bindings (`freeze_candidate_sha`, `freeze_candidate_tree_sha`, `freeze_commit_sha`, `historical_freeze_sha`, `production_engineering_source`, `mainline_tip_at_reconciliation`). The circular "current lineage: main" reference is superseded by a dedicated freeze artifact. (Minor carry: `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md` at the candidate tree may still point at older SHAs — cosmetic, non-binding.)

---

## 4. Per-Gate Resolution Snapshot

| Gate | 1st-pass status | 2nd-pass status |
|---|---|---|
| P1 Candidate Integrity | OPEN | **RESOLVED** (manifest now names candidate) |
| P2 Execution contract | VERIFIED (production only) | **PARTIAL / OPEN** (bound to `303f4424`, not candidate — see R2) |
| P3 Artifact contract | IMPLEMENTED/OPEN | **CLOSED** (candidate-scoped JSON + SHA256 verified) |
| P4 Security / blinding | OPEN | **CLOSED** (role separation + HMAC-SHA256 attested) |
| P5 Provenance / reproducibility | OPEN | **CLOSED** (seed/RNG separation + determinism verified) |
| P6 Durable evidence custody | BLOCKED/OPEN | **CLOSED** (hash round-trip proof; no external archive — see R3) |
| P6a Runtime / CORS | VERIFIED (production only) | **PARTIAL / OPEN** (bound to `303f4424`, not candidate — see R2) |
| P7 Scientific target | ADOPTED / binding pending | **CLOSED** (12 fields + impl/config SHAs bound) |
| P8 Analysis lock | OPEN / fail-closed | **CLOSED** (impl + config SHA locked to candidate) |
| P9 Independent verification | NOT EXECUTED | **2nd pass complete; VERDICT OPEN (see §5)** |
| E2b Verifier toolchain | CLOSED (historical) | **CLOSED** (historical exact boundary; monoculture carried) |
| M6 Negative-state observability | CLOSED (historical) | **CLOSED** (historical exact boundary; monoculture carried) |
| Production provenance | CLOSED | **CLOSED** |

---

## 5. Residual Risks (carried, not hidden)

- **R1 — Evidence monoculture (Finding 4): OPEN.** P2/P6a/E2b/M6 all derive from GitHub Actions infrastructure (same engine, artifacts, secrets, runner). No independent second canonicalization+hash path exists. A single infrastructure compromise would corrupt all four predicates simultaneously. **This is the binding blocker for P9 closure.**
- **R2 — P2/P6a boundary: OPEN.** Runtime/CORS execution evidence is bound to production `303f4424…` / `dpl_FbPSc3K9…`, **not** the designated candidate `c6157158…` / `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`. Fresh candidate-scoped P2/P6a execution is required before those gates are treated as verified for the candidate.
- **R3 — No external durable archive.** P6 closure uses a hash round-trip proof against retained artifacts; `PDMAL_ARCHIVE_ROOT` is unset. Long-term archive is a separate governance decision.
- **R4 — Manifest path-casing defect.** The freeze manifest references `docs/governance/...` (lowercase) but the artifacts live at `docs/GOVERNANCE/...` (uppercase). Exact-path reference does not match the recorded tree path. Cosmetic on case-insensitive FS; a provenance defect on a strict/hash-bound reading.
- **R5 — Authority identity (Finding 5): OPEN.** No candidate-scoped authority-identity verification is present in the freeze evidence.
- **R6 — Authorization invariant.** Pilot authorization NOT GRANTED; Empirical N = 0; pre-freeze. No freeze commit authorizes execution.

---

## 6. P9 Verdict

**P9 STATUS: OPEN** (not CLOSED).

**What the freeze achieved (genuine progress):**
- Resolved the core integrity/lineage defects (Findings 1, 2, 6) with a dedicated authoritative freeze commit.
- Delivered a complete, internally consistent, candidate-scoped evidence chain for P3–P8; P3 JSON SHA256 independently verified to match its record.
- Executed the required 2nd independent adversarial pass (Finding 3 closed).

**Why P9 cannot be CLOSED at this time:**
1. **Finding 4 (evidence monoculture) remains OPEN** — explicitly carried by the freeze manifest itself; no independent second canonicalization+hash path exists. This is the decisive blocker.
2. **P2/P6a runtime/CORS boundary remains OPEN** — evidence is bound to the production source `303f4424…`, not the candidate `c6157158…`; required fresh candidate-scoped execution is absent.
3. **Finding 5 (authority identity) remains OPEN** — no candidate-scoped authority-identity verification in the freeze evidence.

**Conditions for P9 closure (in order):**
1. Establish an independent second canonicalization+hash evidence path to break the GitHub Actions monoculture (R1 / Finding 4).
2. Produce fresh candidate-scoped P2/P6a runtime/CORS execution evidence bound to `c6157158…` / `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` (R2).
3. Verify authority identity (historical-alias vs active-seat) against the exact `c6157158` tree (R5 / Finding 5).
4. Correct the manifest path-casing references to the actual `docs/GOVERNANCE/...` tree paths (R4).
5. Separate governance decision: grant pilot authorization (currently NOT GRANTED; N=0).

**Independence statement:** This 2nd pass was conducted by reading the exact freeze tree `4b62916` via `git show`, independently recomputing the P3 SHA256, and re-examining each of the 6 prior findings without relying on apparatus self-validation. The verdict reflects the freeze's own admitted residual risks, not a presumption of closure.

**P9 hard constraint (unchanged):** N=0, PRE-FREEZE, pilot NOT GRANTED. No push/merge without explicit authorization.
