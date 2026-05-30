# CO_ORCH_QUEUE.md

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Last updated:** 2026-05-30  
> **Anchor:** S066

This file is the active experiment and work queue for the co-orchestration pipeline.
All items must have an owner, checks, artifacts, and metrics before execution.

---

## Queue — S066 Active

### [Q-S066-01] Router TC1/TC2/TC7/TC8 Shadow Bug Fix

- **Owner:** Reson
- **Priority:** P1
- **Status:** 🔲 Queued
- **Context:** Sequential and fan-out predicates in topology router are shadowed by hierarchical catch-all. TC1, TC2, TC7, TC8 currently fail (5/8 pass rate). Tracked from S043 Q-S043-04.
- **Checks:**
  - [ ] Reorder predicates so SEQUENTIAL and FAN-OUT match before HIERARCHICAL catch-all
  - [ ] All 8 TCs pass: TC1 SEQUENTIAL, TC2 SEQUENTIAL, TC3 REFLEXIVE, TC4 HIERARCHICAL, TC5 REJECTED, TC6 REJECTED, TC7 FAN-OUT, TC8 FAN-OUT
  - [ ] Regression: TC3–TC6 still pass after reorder
  - [ ] CI green on `tests/test_router_coverage.py`
- **Artifacts:** `components/topology_router.py`, `tests/test_router_coverage.py`
- **Metrics:** 8/8 TC pass rate (up from 5/8)

---

### [Q-S066-02] COLLEEN Stasis Audit P-12–P-26 (PM-05 — Merge Blocker)

- **Owner:** COLLEEN
- **Priority:** P1 — **MERGE BLOCKER**
- **Status:** 🔲 Queued
- **Context:** Before the unified registry merge (docs/NDR_REGISTRY_MERGE_PLAN.md Phase 1), COLLEEN must audit the 15 stasis patterns (P-12–P-26) for gaps, duplicates, and cross-reference completeness. These patterns were sealed pre-S033 and have not been formally reviewed since.
- **Checks:**
  - [ ] Review each P-12–P-26 entry in `docs/patterns/NDR_PATTERN_REGISTRY.md`
  - [ ] Confirm no duplicate pattern specs across registries
  - [ ] Confirm all cross-references to P-01–P-10 and P-27+ are by number (not prose only)
  - [ ] Flag any stasis pattern requiring ALTER or UPDATE before merge
  - [ ] Emit stasis audit report to `docs/qa/COLLEEN_STASIS_AUDIT_P12_P26.md`
  - [ ] Update PM-05 status in `docs/NDR_REGISTRY_MERGE_PLAN.md` to CLOSED
- **Artifacts:** `docs/qa/COLLEEN_STASIS_AUDIT_P12_P26.md`, `docs/NDR_REGISTRY_MERGE_PLAN.md` (PM-05 update)
- **Metrics:** 0 unresolved gaps, 0 duplicate specs, all cross-refs by number
- **Blocks:** Unified registry merge Phase 1

---

### [Q-S066-03] Apogee P-30 Attestation Pass on P-34 (PM-07 — Merge Blocker)

- **Owner:** Apogee
- **Priority:** P1 — **MERGE BLOCKER**
- **Status:** 🔲 Queued
- **Context:** P-34 (Empirical-Threshold-Sweep-over-ML-Classifier) was registered this session as COMPOSE. Per P-30 (Apogee-Attestation-Gate), any new pattern requires an 11Q scoring pass before canonical promotion. P-34 is currently PENDING attestation.
- **Checks:**
  - [ ] Run P-11 11Q scoring pass on P-34 spec
  - [ ] Gate: S-TIER (≥95%) or A-TIER (≥85%) with documented open BLGs
  - [ ] Q11 must score ≥9/10 for S-TIER attestation
  - [ ] Emit signed attestation JSON to `docs/qa/APOGEE_11Q_P34.json`
  - [ ] Update P-34 `attestation_status` in `patterns/ndr_patterns.json` from PENDING to ATTESTED (or CONDITIONAL with noted BLGs)
  - [ ] Update PM-07 status in `docs/NDR_REGISTRY_MERGE_PLAN.md` to CLOSED
  - [ ] Update P-34 entry in `docs/NDR_PATTERN_REGISTRY.md` v1.4 with attestation result
- **Artifacts:** `docs/qa/APOGEE_11Q_P34.json`, `patterns/ndr_patterns.json` (attestation_status update), `docs/NDR_REGISTRY_MERGE_PLAN.md` (PM-07 update)
- **Metrics:** 11Q score ≥85%, Q11 ≥9/10, signed JSON artifact present
- **Blocks:** P-34 canonical promotion; unified registry merge Phase 1

---

### [Q-S066-04] Lifecycle Harness — Phase 0–VI Executable (Carry-Forward)

- **Owner:** Amethyst + COLLEEN
- **Priority:** P1
- **Status:** 🔲 Queued (carry-forward from S043 Q-S043-05)
- **Checks:**
  - [ ] Executable phase harness produces `lifecycle_stability_report.json`
  - [ ] Stability index per phase ≥ 0.618
  - [ ] Time-to-convergence ≤ Fib[34] turns
  - [ ] COLLEEN archive ingest of all phase artifacts
- **Artifacts:** `registry/lifecycle_stability_report.json`, `docs/lifecycle_harness_v2.md`
- **Metrics:** Stability index ≥ 0.618 per phase, convergence ≤ Fib[34]

---

## Completed Queue Items — S066

| ID | Name | Owner | Status |
|----|------|-------|--------|
| Q-S066-P34-REG | Register P-34 COMPOSE entry | Amethyst | ✅ Done |
| Q-S066-JSON-SYNC | Sync ndr_patterns.json v0.3.0 | Amethyst | ✅ Done |
| Q-S066-DIFF | Create NDR_REGISTRY_DIFFERENTIATION.md | Amethyst | ✅ Done |
| Q-S066-MERGE-PLAN | Create NDR_REGISTRY_MERGE_PLAN.md | Amethyst | ✅ Done |
| Q-S066-PM01 | PM-01: Phi-Closure card P-29 cross-ref | Amethyst | ✅ Done |
| Q-S066-PM02 | PM-02: P-03 ALTER note P-30 ref | Amethyst | ✅ Done |

---

## Completed Queue Items — Prior Sessions

| ID | Name | Session | Status |
|---|---|---|---|
| Q-S043-01 | Intake Gate Hardening | S043 | ✅ Done |
| Q-S043-02 | Phi-Closure Gate — HPG Wiring | S043 | ✅ Done |
| Q-S043-03 | Orchestration Firewall | S043 | ✅ Done |
| Q-S043-06 | Archive and Registry Sync | S043 | ✅ Done |
| Q-S038-01 | SCPE threshold calibration | S038 | ✅ Done |
| Q-S039-01 | PDMAL convergence proof | S039 | ✅ Done |
| Q-S040-01 | HPG Ionian gate implementation | S040 | ✅ Done |
| Q-S041-01 | DGAF 6-axis semantic scoring | S041 | ✅ Done |
| Q-S042-01 | Amethyst dual-lock logic | S042 | ✅ Done |
