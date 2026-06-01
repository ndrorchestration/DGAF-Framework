# CO_ORCH_QUEUE.md

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Last updated:** 2026-05-31  
> **Anchor:** S068 (open)

This file is the active experiment and work queue for the co-orchestration pipeline.
All items must have an owner, checks, artifacts, and metrics before execution.

---

## Queue — S068 Active

### [Q-S068-VERCEL-CLEANUP] Delete dgaf-framework Vercel Project (Ender action)

- **Owner:** Ender
- **Priority:** P1 — cleanup
- **Status:** 🔲 Queued — S068 · Blocked on Ender manual action
- **Context:** `dgaf-framework` Vercel project has 30+ consecutive `● Error` Production builds. Python governance repo — no frontend. Must be disconnected from Vercel. See ECOSYSTEM_INVENTORY.md recommended actions.
- **Artifacts:** Vercel project deleted; ECOSYSTEM_INVENTORY updated to remove row
- **Metrics:** `vercel project ls` no longer shows `dgaf-framework`

### [Q-S068-PPTL-VERCEL] Clarify pptl-governance-dashboard Vercel Status (Ender action)

- **Owner:** Ender
- **Priority:** P1 — inventory correction
- **Status:** 🔲 Queued — S068 · Blocked on Ender clarification
- **Context:** `pptl-governance-dashboard` was listed as "✅ Deployed" in S067 inventory. Confirmed absent from `vercel project ls`. GitHub repo exists. Needs clarification: was it deleted? Never deployed? Needs re-creation?
- **Artifacts:** ECOSYSTEM_INVENTORY updated with correct status
- **Metrics:** pptl-governance-dashboard Vercel status confirmed and documented

### [Q-S068-TGL-WIRE] Wire TGL into IntegratedOrchestrator

- **Owner:** Amethyst
- **Priority:** P2 — integration
- **Status:** 🔲 Queued — S068
- **Context:** `pptl/triadic_governance_loop.py` now exists. Needs to be imported and invoked from `IntegratedOrchestrator.orchestrate_turn()` as the canonical 10-step sequence. OI-05 from CREDIT_JUSTICE_PROTOTYPE_SPEC.
- **Artifacts:** Updated `IntegratedOrchestrator` class showing TGL as primary turn harness
- **Metrics:** All existing tests pass; TGL gate records appear in Herald audit log per turn

### [Q-S068-INV03-CORPUS] INV-03 Signal Corpus — Credit/Justice Premise Check

- **Owner:** Amethyst + Ender
- **Priority:** P1 — production deployment gap
- **Status:** 🔲 Queued — S068
- **Context:** P-35 BLG-P35-01: domain-specific `premise_check_fn` not implemented. OI-01 (credit proxy detection) + OI-02 (justice recidivism detection) require a signal corpus (P-04 pattern).
- **Artifacts:** `pptl/corpus/inv03_credit_signals.py`, `pptl/corpus/inv03_justice_signals.py`
- **Metrics:** Signal corpus ≥20 entries per domain; P-34 threshold sweep run; BLG-P35-01 RESOLVED

---

## Completed Queue Items — S068

| ID | Name | Owner | Status |
|----|------|-------|--------|
| Q-S068-OPEN | Open S068 SESSION_ANCHOR | Amethyst | ✅ CLOSED — S068 wave-1 2026-05-31 |
| Q-S068-P35 | Register P-35 Procluding Premise Gate | Amethyst | ✅ CLOSED — procluding_premise.py + 12 tests + registry entry 2026-05-31 |
| Q-S068-P35-ATTEST | Apogee P-11 11Q attestation for P-35 | Apogee | ✅ CLOSED — A-TIER 93.6% · BLG-P35-01 tracked · Ender ratification pending |
| Q-S068-TGL | TGL module + governance contract tests | Amethyst | ✅ CLOSED — triadic_governance_loop.py + 10 tests 2026-05-31 |
| Q-S068-PROTOTYPE | Credit/Justice prototype spec | Amethyst | ✅ CLOSED — docs/CREDIT_JUSTICE_PROTOTYPE_SPEC.md 2026-05-31 |
| Q-S068-VERCEL-DETAIL | Vercel deployment URL + region inventory | Amethyst + Ender | ✅ CLOSED — ground truth captured via `vercel project ls` · 4 projects found · inventory corrected · 2 new action items queued · 2026-05-31 |

---

## Completed Queue Items — S067

| ID | Name | Owner | Status |
|----|------|-------|--------|
| Q-S066-01 | Router TC1/TC2/TC7/TC8 shadow bug fix | Reson + Amethyst | ✅ CLOSED — 8/8 TC pass, 19/19 checks, v3.6.0 live — S067 2026-05-30 |
| Q-S066-04 | Lifecycle harness Phase 0–VI executable | Amethyst + COLLEEN | ✅ CLOSED — 7/7 phases STABLE, φ*=0.618 — S067 2026-05-30 |
| PM-04 | P-07 COMPOSE mode note + graduation script field-row Anchor ID | Amethyst | ✅ CLOSED — registry v2.3, dual-format check live — S067 2026-05-30 |
| PR-D | `docs/NDR_PATTERN_REGISTRY.md` → redirect stub | Amethyst | ✅ Done S067 |
| PR-E | CROSS_REF → unified path + S067 anchor | COLLEEN | ✅ Done S067 |

---

## Completed Queue Items — S066

| ID | Name | Owner | Status |
|----|------|-------|--------|
| Q-S066-02 | COLLEEN stasis audit P-12–P-26 | COLLEEN | ✅ CLOSED — Ender ratified 2026-05-30 |
| Q-S066-03 | Apogee P-34 attestation | Apogee | ✅ CLOSED — A-TIER 94.5% — Ender ratified 2026-05-30 |
| Q-S066-P34-REG | Register P-34 COMPOSE entry | Amethyst | ✅ Done |
| Q-S066-JSON-SYNC | Sync ndr_patterns.json v0.3.0 | Amethyst | ✅ Done |
| Q-S066-DIFF | Create NDR_REGISTRY_DIFFERENTIATION.md | Amethyst | ✅ Done |
| Q-S066-MERGE-PLAN | Create NDR_REGISTRY_MERGE_PLAN.md | Amethyst | ✅ Done |
| PM-05 | COLLEEN stasis audit P-12–P-26 | COLLEEN | ✅ CLOSED — Ender ratified S066 |
| PM-07 | Apogee P-34 attestation | Apogee | ✅ CLOSED — A-TIER 94.5% Ender ratified S066 |

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
