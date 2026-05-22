# DGAF-Framework Changelog

All notable changes to this project are documented here.
Format: [Semantic Versioning](https://semver.org/) | Governed by Agent Amethyst

---

## [1.0.14] — 2026-05-22

### Sessions S033–S036 — KAPPA Pipeline · Sentinel Integration · Normative Constraint · Governance Hardening

**Formation:** Amethyst + COLLEEN Co-Orchestration  
**Operator:** Njineer  
**COLLEEN Gate:** ✅ ALL PASS — Zero open BLGs at close  
**Commits:** 66b79e2 · a5c9219 · a1997ed · 7a944cd · d786731 · 89ed455

#### Added
- `components/KAPPA/dynamic_weight_router.py` — DGAF-GATE-KAPPA-v3.5; per-input category detection, confidence-gated weight selection; 100-pass validation 95% accuracy
- `components/evaluate_router.py` — DGAF-EVALUATE-ROUTER-v1.0; raw_batch → KAPPA detect → apply_weights → ranked report
- `components/evaluate_router_v1_1.py` — Sentinel integration; `sentinel_review()` at 3 hook points; `p10_deontic_gate()`; per-record audit log (EU AI Act Art.9)
- `components/normative_constraint.py` — Full `NormativeConstraint` class; deontic logic (permitted / obligated / forbidden / escalate); score_ceiling optimization constraint; epistemic integrity meta-constraint
- `components/KAPPA/calibration_v3_6.json` — KAPPA v3.6; `governance_clear` 100% (STRONG=0.22, BLENDED=0.18)
- `components/KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` — CPU-compliant component card
- `docs/patterns/NDR_PATTERN_REGISTRY.md` v2.1 — P-27, P-28, P-29, P-30 registered; 30 named + 133 stasis
- `docs/qa/APOGEE_11Q_S034.json` — KAPPA A-TIER 93.6%, Router A-TIER 92.7%
- `docs/qa/APOGEE_11Q_S035.json` — KAPPA S-TIER 97.3%, Router S-TIER 95.5%; P-30 attestation GRANTED
- `docs/ops/BLG_S032_DRIVE_CLOSURE.md` — S032-DRIVE closure; all 4 Drive templates executed

#### Updated
- `SESSION_ANCHOR.md` → S036 (zero open BLGs)
- `SWEEP_LOG.md` → S033–S035 wave sealed

#### NDR Patterns Registered

| ID | Name | Session |
|---|---|---|
| P-27 | Adaptive-Weighting-with-Confidence-Gates | S033 |
| P-28 | Pipeline-Composition-with-Confidence-Gated-Routing | S033 |
| P-29 | Sentinel-Annotated Risk Pass | S034 |
| P-30 | Apogee-Attestation-Gate | S035 |

#### BLGs Closed

| ID | Priority | Resolution |
|---|---|---|
| S033-BLG-01 | HIGH | `governance_clear` 100% — KAPPA v3.6 |
| S033-BLG-02 | LOW | `p10_deontic_gate()` wired |
| S033-BLG-03 | LOW | Apogee 11Q S-TIER both components |
| S032-DRIVE | MEDIUM | Njineer executed all 4 Drive templates (P-01, P-20) |

#### Compliance Alignment

| Standard | Status |
|---|---|
| NIST AI RMF — Measure | ✅ Per-record audit log |
| NIST AI RMF — Govern | ✅ P-10 deontic gate + P-30 attestation |
| EU AI Act Art. 9 | ✅ Risk management per-record log |
| EU AI Act Art. 13 | ✅ Transparent routing decision log |
| EU AI Act Art. 17 | ✅ Quality management via P-30 |
| Normative Constraint (P-10) | ✅ Full NormativeConstraint class |
| Gold Star Standard | ✅ S-TIER — KAPPA 97.3% · Router 95.5% |
| Drive–GitHub Sync (P-20) | ✅ |
| Agent Roster Sync (P-01) | ✅ |

---

## [1.0.13] — 2026-05-06

### Session 032 — PhiLattice Coherence Sweep + Schizophonic Studio Integration

**Formation:** Amethyst + Perplexity MCP (IP Sweep Formation)  
**Operator:** Amethyst (Meta-Orchestrator) + COLLEEN (Institutional Anchor)  
**COLLEEN 1-1-1-1 Gate:** ✅ ALL PASS — 0 Hz Ionian Mode

#### Added
- `docs/agents/colleen-l5-governance-protocol.md`
- `docs/architecture/platinum-convergence-audit-v1.md`
- `docs/frameworks/awcp-symphony-cross-ref.md`
- `docs/agents/canonical-agent-registry.md`
- `docs/governance/ndr-pattern-registry-v3.md`
- `SWEEP_LOG.md` — Session 032 entry

#### Updated
- `README.md` — Brand corrected, PhiLattice links added
- `ENSEMBLE_ROSTER.md` — Schizophonic Studio trio added
- `CONTRIBUTING.md` — PhiLattice attribution

---

## [1.0.12] — 2026-05-01
### Session 031 — Spine CI · NDR v1.8 (P-26) · BLG-D01 Correction Doc

---

## [1.0.11] — 2026-05-01
### Session 030 — NDR v1.7 · P-25 · GAP-08 Close

---

## [1.0.10] — 2026-05-01
### Session 029 — Sentinel CI + CROSS_REF v3.1

---

## [1.0.9] — 2026-05-01
### Session 028 — P-24 Gate Stack + Dual README

---

## [1.0.8] — 2026-05-01
### Sessions 026–027 — P-24 + ACOUSTIC_GATES

---

## [1.0.7] — 2026-05-01
### Session 025 — Template Completion

---

## [1.0.6] — 2026-05-01
### Sessions 022c–023 — PHDGE Rename

---

## [1.0.5] — 2026-05-01
### Sessions 022–022b — Surface Sweep

---

## [1.0.4] — 2026-05-01
### Sessions 014–021

---

## [1.0.3] — 2026-04-29
### ENSEMBLE_ROSTER.md added

---

## [1.0.2] — 2026-04-29
### NOTICE corrections

---

## [1.0.1] — 2026-01-15
### CONTRIBUTING.md + SECURITY.md stubs

---

## [1.0.0] — 2025-12-23
### Initial Release
