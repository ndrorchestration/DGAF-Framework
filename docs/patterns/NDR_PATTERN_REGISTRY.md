# NDR Pattern Registry
## DGAF-Framework · Canonical Pattern Set
**Version:** 2.1  
**Maintained by:** COLLEEN (Archival Authority) | Amethyst (Meta-Orchestrator)  
**Updated:** 2026-05-22  
**Session:** S035

---

## Registry Status
- Patterns P-01 through P-26: Canonical (stasis)
- **P-27:** S033 — Adaptive-Weighting-with-Confidence-Gates
- **P-28:** S033 — Pipeline-Composition-with-Confidence-Gated-Routing
- **P-29:** S034 — Sentinel-Annotated Risk Pass
- **P-30:** S035 — Apogee-Attestation-Gate
- Total registered: 30 named patterns + 133 stasis patterns

---

## P-27 — Adaptive-Weighting-with-Confidence-Gates
**Spec:** Dynamically adjust evaluation weights per input record based on a confidence score. Apply strong weights when confidence ≥ STRONG_THRESH; blend when BLENDED_THRESH ≤ confidence < STRONG_THRESH; fall back to balanced when confidence < BLENDED_THRESH.  
**Ref:** `components/KAPPA/dynamic_weight_router.py`  
**Thresholds (v3.6):** STRONG=0.22 | BLENDED=0.18  
**NIST:** Measure | **EU AI Act:** Art.9  
**Registered:** S033 | Updated S034

---

## P-28 — Pipeline-Composition-with-Confidence-Gated-Routing
**Spec:** Compose evaluation pipeline: raw_batch → detect → route_and_score (P-27) → apply_weights → ranked_report. Each stage independently auditable.  
**Ref:** `components/evaluate_router.py`  
**NIST:** Measure | **EU AI Act:** Art.9  
**Registered:** S033

---

## P-29 — Sentinel-Annotated Risk Pass
**Spec:** Invoke sentinel_review(record, routing, hook_point) at 3 hook points. Emits per-record audit log with risk classification (risk_ok / risk_warn / risk_block). Only risk_block halts pipeline. Integrates P-10 deontic gate at hook point 1.  
**Ref:** `components/evaluate_router_v1_1.py` — `sentinel_review()`, `p10_deontic_gate()`  
**Ethical cognition:** P-10 Normative Constraint gate — permitted / obligated / forbidden  
**NIST:** Measure, Govern | **EU AI Act:** Art.9, Art.13  
**Registered:** S034

---

## P-30 — Apogee-Attestation-Gate
**Spec:** Before any component is declared governance-ready, Apogee runs a P-11 11Q scoring pass. Gate passes when: (a) S-TIER (≥95%), or (b) A-TIER (≥85%) with open BLGs. Q11 must score ≥9/10 for S-TIER attestation. Attestation emitted as signed JSON artifact in docs/qa/.  
**Ref:** `docs/qa/APOGEE_11Q_*.json`  
**Use:** Any component being promoted to canonical status. Prevents silent A-TIER → canonical promotions without quality attestation.  
**Trigger:** CPU card submission or NDR pattern registration.  
**Ethical cognition:** Q11 gate enforces no component claims governance compliance without normative constraint wiring. Intellectual honesty: A-TIER components must disclose gaps as BLGs.  
**NIST:** Measure, Govern | **EU AI Act:** Art.9, Art.17  
**Failure mode:** If attestation is skipped under time pressure, unverified components enter registry with no quality anchor.  
**Registered:** S035 | 2026-05-22

---

## Carry-Forward Notes (COLLEEN)
- P-01 through P-26: Canonical stasis
- P-27, P-28: S033 | P-29: S034 | P-30: S035
- Next candidate: P-31 — TBD (S036)
- SWEEP_LOG: S033+S034 wave sealed
