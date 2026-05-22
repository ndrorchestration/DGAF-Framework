# NDR Pattern Registry
## DGAF-Framework · Canonical Pattern Set
**Version:** 1.9  
**Maintained by:** COLLEEN (Archival Authority) | Amethyst (Meta-Orchestrator)  
**Updated:** 2026-05-22  
**Session:** S033

---

## Registry Status
- Patterns P-01 through P-26: Canonical (stasis — see prior commits)
- **P-27:** New — registered S033
- **P-28:** New — registered S033
- Total registered: 28 named patterns + 133 stasis patterns

---

## P-27 — Adaptive-Weighting-with-Confidence-Gates

**Name:** Adaptive-Weighting-with-Confidence-Gates  
**Spec:** Dynamically adjust evaluation weights per input record based on a confidence score derived from the routing model. Apply strong weights (w_adv, w_bias, w_cite) when confidence ≥ STRONG_THRESH; blend with balanced weights when BLENDED_THRESH ≤ confidence < STRONG_THRESH; fall back to balanced when confidence < BLENDED_THRESH.  
**Implementation reference:** `components/KAPPA/dynamic_weight_router.py` — `select_weights_with_confidence()`  
**Use:** Any evaluation pipeline where input quality or adversarial signal strength varies significantly across records; prevents over-penalization of low-signal inputs and under-penalization of adversarial inputs.  
**Trigger:** When static threshold evaluation produces high variance in governance scores across heterogeneous input batches.  
**Thresholds (v3.5 defaults):** STRONG_THRESH = 0.28 | BLENDED_THRESH = 0.25  
**Failure mode:** If confidence detection is biased, fallback_balanced may mask true adversarial inputs; Sentinel annotation required as guard.  
**Registered:** S033 | 2026-05-22

---

## P-28 — Pipeline-Composition-with-Confidence-Gated-Routing

**Name:** Pipeline-Composition-with-Confidence-Gated-Routing  
**Spec:** Compose an evaluation pipeline as: raw_batch → detect_categories → route_and_score (P-27 gated) → apply_weights → ranked_report. Each stage is independently auditable. The routing stage applies P-27 and emits a per-record routing decision alongside the score.  
**Implementation reference:** `components/evaluate_router.py` — `run_evaluation_pipeline()`  
**Use:** Multi-record governance evaluation pipelines where traceable per-record routing decisions are required for audit.  
**Trigger:** When a single-pass scoring approach lacks the per-record auditability required by governance compliance (DGAF gate, EU AI Act Article 9).  
**Failure mode:** If pipeline stages are not independently logged, a downstream audit cannot reconstruct the routing decision for a specific record.  
**Registered:** S033 | 2026-05-22

---

## Carry-Forward Notes (COLLEEN)
- P-01 through P-26 are stable. Full content in prior commits.
- P-27 and P-28 are the only additions this session.
- Next pattern candidate: P-29 — Sentinel-Annotated Risk Pass (deferred to S034 pending Sentinel integration completion).
