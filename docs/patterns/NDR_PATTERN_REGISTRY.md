# NDR Pattern Registry
## DGAF-Framework · Canonical Pattern Set
**Version:** 2.2
**Maintained by:** COLLEEN (Archival Authority) | Amethyst (Meta-Orchestrator)
**Updated:** 2026-05-30
**Session:** S066 (base: S035)

---

## Registry Status
- Patterns P-01 through P-26: Canonical (stasis)
- **P-27:** S033 — Adaptive-Weighting-with-Confidence-Gates
- **P-28:** S033 — Pipeline-Composition-with-Confidence-Gated-Routing
- **P-29:** S034 — Sentinel-Annotated Risk Pass
- **P-30:** S035 — Apogee-Attestation-Gate
- **P-31–P-33:** S042 — Runtime cards (SCPE / Phi-Closure / PDMAL) — `patterns/` directory
- **P-34:** S066 — Empirical-Threshold-Sweep-over-ML-Classifier — `docs/NDR_PATTERN_REGISTRY.md`
- Total registered: 34 named patterns (P-01–P-34) + 133 stasis (P-12–P-26 block)

> **Registry differentiation and merge pre-plan:**
> See `docs/NDR_REGISTRY_DIFFERENTIATION.md` and `docs/NDR_REGISTRY_MERGE_PLAN.md`.
> This file holds full specs for P-27–P-30. P-01–P-10 full specs are in
> `docs/NDR_PATTERN_REGISTRY.md`. P-31–P-33 cards are in `patterns/`. P-34
> full spec is in `docs/NDR_PATTERN_REGISTRY.md`.

---

## P-27 — Adaptive-Weighting-with-Confidence-Gates
**Spec:** Dynamically adjust evaluation weights per input record based on a confidence score. Apply strong weights when confidence ≥ STRONG_THRESH; blend when BLENDED_THRESH ≤ confidence < STRONG_THRESH; fall back to balanced when confidence < BLENDED_THRESH. Adversarial category always routes to apply_strong regardless of confidence (hard override).
**Ref:** `components/KAPPA/dynamic_weight_router.py`
**Thresholds (v3.6, empirical via P-34):** STRONG=0.22 | BLENDED=0.18
**Calibration method:** P-34 Empirical-Threshold-Sweep (14×12 grid, S034)
**NIST:** Measure | **EU AI Act:** Art.9
**Registered:** S033 | Updated S034, S066

---

## P-28 — Pipeline-Composition-with-Confidence-Gated-Routing
**Spec:** Compose evaluation pipeline: raw_batch → detect → route_and_score (P-27) → apply_weights → ranked_report. Each stage independently auditable. No stage may read from a stage it did not receive output from.
**Ref:** `components/evaluate_router.py`
**NIST:** Measure | **EU AI Act:** Art.9
**Registered:** S033

---

## P-29 — Sentinel-Annotated Risk Pass
**Spec:** Invoke sentinel_review(record, routing, hook_point) at 3 hook points. Emits per-record audit log with risk classification (risk_ok / risk_warn / risk_block). Only risk_block halts pipeline. Integrates P-10 deontic gate at hook point 1.
**Cross-ref (pending PM-01):** P-32 Phi-Closure Gate KILL_REC action should trigger risk_block at hook point 2. Cross-ref note to be added to P-32 card before merge.
**Ref:** `components/evaluate_router_v1_1.py`
**Ethical cognition:** P-10 Normative Constraint gate — permitted / obligated / forbidden
**NIST:** Measure, Govern | **EU AI Act:** Art.9, Art.13
**Registered:** S034

---

## P-30 — Apogee-Attestation-Gate
**Spec:** Before any component is declared governance-ready, Apogee runs a P-11 11Q scoring pass. Gate passes when: (a) S-TIER (≥95%), or (b) A-TIER (≥85%) with open BLGs. Q11 must score ≥9/10 for S-TIER attestation. Attestation emitted as signed JSON artifact in docs/qa/.
**Pending (PM-07):** P-34 (Empirical-Threshold-Sweep-over-ML-Classifier) requires Apogee attestation pass before canonical promotion.
**Ref:** `docs/qa/APOGEE_11Q_*.json`
**Use:** Any component being promoted to canonical status.
**Trigger:** CPU card submission or NDR pattern registration.
**NIST:** Measure, Govern | **EU AI Act:** Art.9, Art.17
**Registered:** S035 | Updated S066

---

## P-31–P-33 — Cross-Reference Index (Runtime Cards)

| Pattern | Name | Card |
|---------|------|------|
| P-31 | SCPE — Structural Context Pruning Engine | `patterns/NDR_SCPE_v1.md` |
| P-32 | Phi-Closure Gate | `patterns/NDR_PHI_CLOSURE_GATE_v1.md` |
| P-33 | PDMAL Convergence Monitor | `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` |

---

## P-34 — Cross-Reference (Full Spec in Primary Registry)

| Pattern | Name | Location |
|---------|------|----------|
| P-34 | Empirical-Threshold-Sweep-over-ML-Classifier | `docs/NDR_PATTERN_REGISTRY.md` · S066 COMPOSE |

---

## Carry-Forward Notes (COLLEEN)
- P-01 through P-26: Canonical stasis
- P-27, P-28: S033 | P-29: S034 | P-30: S035
- P-31–P-33: S042 runtime cards | P-34: S066 COMPOSE
- **Next candidate:** P-35 — TBD (next CO_ORCH_QUEUE COMPOSE entry)
- **Open pre-merge actions:** PM-01 through PM-08 — see `docs/NDR_REGISTRY_MERGE_PLAN.md`
- SWEEP_LOG: S033+S034 wave sealed | S066 wave: KAPPA training data resolved, P-34 registered
