# NDR Pattern Registry
## DGAF-Framework · Canonical Pattern Set
**Version:** 2.0  
**Maintained by:** COLLEEN (Archival Authority) | Amethyst (Meta-Orchestrator)  
**Updated:** 2026-05-22  
**Session:** S034

---

## Registry Status
- Patterns P-01 through P-26: Canonical (stasis — see prior commits)
- **P-27:** Registered S033
- **P-28:** Registered S033
- **P-29:** Registered S034
- Total registered: 29 named patterns + 133 stasis patterns

---

## P-27 — Adaptive-Weighting-with-Confidence-Gates

**Name:** Adaptive-Weighting-with-Confidence-Gates  
**Spec:** Dynamically adjust evaluation weights per input record based on a confidence score. Apply strong weights when confidence ≥ STRONG_THRESH; blend when BLENDED_THRESH ≤ confidence < STRONG_THRESH; fall back to balanced when confidence < BLENDED_THRESH.  
**Implementation reference:** `components/KAPPA/dynamic_weight_router.py` — `select_weights_with_confidence()`  
**Use:** Any evaluation pipeline where input quality or adversarial signal strength varies significantly across records.  
**Trigger:** When static threshold evaluation produces high variance in governance scores across heterogeneous input batches.  
**Thresholds (v3.6 defaults):** STRONG_THRESH = 0.22 | BLENDED_THRESH = 0.18  
**Failure mode:** If confidence detection is biased, fallback_balanced may mask adversarial inputs; Sentinel annotation (P-29) required as guard.  
**Registered:** S033 | Updated S034 (thresholds recalibrated)

---

## P-28 — Pipeline-Composition-with-Confidence-Gated-Routing

**Name:** Pipeline-Composition-with-Confidence-Gated-Routing  
**Spec:** Compose evaluation pipeline as: raw_batch → detect_categories → route_and_score (P-27 gated) → apply_weights → ranked_report. Each stage independently auditable.  
**Implementation reference:** `components/evaluate_router.py` — `run_evaluation_pipeline()`  
**Use:** Multi-record governance evaluation pipelines requiring traceable per-record routing decisions for audit.  
**Trigger:** When a single-pass scoring approach lacks per-record auditability required by governance compliance.  
**Failure mode:** If pipeline stages are not independently logged, a downstream audit cannot reconstruct routing decisions.  
**Registered:** S033

---

## P-29 — Sentinel-Annotated Risk Pass

**Name:** Sentinel-Annotated Risk Pass  
**Spec:** After category detection and weight selection, invoke sentinel_review(record, routing, hook_point) at three defined hook points. Sentinel emits per-record audit log entries with risk classification (risk_ok / risk_warn / risk_block). Only risk_block halts pipeline emission. Integrates P-10 deontic gate at hook point 1.  
**Implementation reference:** `components/evaluate_router_v1_1.py` — `sentinel_review()`, `p10_deontic_gate()`  
**Use:** Any governance evaluation pipeline requiring per-record audit trails for regulatory compliance. Prevents adversarial inputs from silently reaching fallback_balanced routing.  
**Trigger:** When pipeline must produce auditable per-record risk annotation alongside each governance score, or when Sentinel must veto an output without refactoring routing logic.  
**Ethical cognition alignment:** Integrates P-10 Normative Constraint gate; enforces deontic boundary (permitted / obligated / forbidden) before weight selection.  
**NIST AI RMF:** Measure (audit log), Govern (deontic gate)  
**EU AI Act:** Article 9 (risk management), Article 13 (transparency)  
**Failure mode:** If sentinel_review is made stateful or side-effectful, it risks corrupting routing math; must remain a pure annotation layer.  
**Registered:** S034 | 2026-05-22

---

## Carry-Forward Notes (COLLEEN)
- P-01 through P-26: Canonical (stasis)
- P-27, P-28: Registered S033
- P-29: Registered S034
- Next pattern candidate: P-30 — Apogee-Attestation-Gate (deferred to S035)
