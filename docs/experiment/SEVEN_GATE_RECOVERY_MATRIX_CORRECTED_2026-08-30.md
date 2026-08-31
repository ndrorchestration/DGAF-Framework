# Seven-Gate Recovery Matrix — Consolidated (2026-08-30)

**Boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0
**Apparatus:** unchanged. `05fa286…` still designated post-#151 candidate; Phase A restore (P-31/P-33) is a separate unmerged proposal (PR #160).
**Source standard:** dated/versioned normative contract + historical implementation CO-LOCATED at one provenance boundary (the bar that qualified P-31/P-33).

## Status table (verified this session, agent findings corrected)

| Gate       | Contract source                                                        | Impl source                                                        | Qualification        | Pilot substrate | Disposition (pre-RESTORE) |
|------------|------------------------------------------------------------------------|--------------------------------------------------------------------|----------------------|----------------|---------------------------|
| P-31 SCPE  | `patterns/NDR_SCPE_v1.md` (Prod v1.0 @49854ea)                        | `ensemble_v16.StructuralContextPruningEngine` @49854ea             | CONTRACT-QUALIFIED   | MISSING        | RESTORED (PR #160)        |
| P-33 Conv  | `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` (Prod v1.0 @49854ea)   | `ensemble_v16.PDMALConvergenceMonitor` @49854ea                    | CONTRACT-QUALIFIED   | MISSING        | RESTORED (PR #160)        |
| P-32 Phi   | `patterns/NDR_PHI_CLOSURE_GATE_v1.md` (Prod v1.0 @49854ea)            | `ensemble_v16.FibonacciPhiClosureGate` @49854ea (faithful)        | CONTRACT-QUALIFIED   | MISSING        | pending RESTORE           |
| P-27 KAPPA | `components/KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` (@66b79e24) | `components/KAPPA/dynamic_weight_router.py` (v3.6)                | CONTRACT-QUALIFIED*  | MISSING        | pending RESTORE           |
| P-29 Sentinel | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md:326` (canonical registry entry) | `components/evaluate_router_v1_1.py:sentinel_review()`            | REGISTRY-QUALIFIED (lead-grade) | MISSING | pending extraction        |
| P-30 Apogee | `docs/specs/attestation_gate_spec.md` + `docs/qa/APOGEE_11Q_*.json` + `d786731f`: `normative_constraint.py` (deontic states + audit) + P-30 gate registration (NDR v2.1, S-TIER) | `components/ensemble_v17.py:ApogeeReviewer` (grade thresholds)    | LEAD (schema+deontic-impl, below RESTORE-ready) | MISSING | pending extraction |
| DemiJoule  | NONE (role specs only; no dated gate contract)                        | `ensemble_v16.DemiJouleGate` & `ensemble_v17.DemiJouleGate` (CONTRADICTORY) | LEAD            | MISSING        | pending extraction        |

*P-27 caveat: card is v3.5.0; code is v3.6.0 with new categories (sequential/fan_out) absent from the card. Thresholds (0.28/0.25) and formula are consistent card↔code. RESTORE should pin to v3.5 card as the normative source.

## Correction log (agent findings retracted/re-anchored)
1. **P-32 "never emits KILL_REC / uses PSI"** — FALSE for the historical impl at `49854ea`. The historical `check()` uses `PHI_STAR` and emits `KILL_REC` (consecutive≥3 / Fib[55]). The PSI bug exists only in **current `main` line 441** (`delta = abs(ratio - PSI)`), a regression in the pilot's copy. RESTORE anchors to `49854ea`, not `main`.
2. **P-29 "contract-qualified"** — downgraded to REGISTRY-QUALIFIED. The registry entry is canonical but not a standalone dated/versioned gate contract; the implementation `evaluate_router_v1_1.py` is side-effect-free (halt is orchestrator-side). Stays a lead per our bar.
3. **P-27 "contradiction 0.22/0.18 vs 0.28/0.25"** — that was cross-document drift (registry/wiki vs component card), NOT card↔code. Card↔code thresholds match. Not a blocking contradiction for RESTORE.

## Substrate gaps (ConsensusState @ main has NONE of these)
- P-31: token/tier/retention/trust-edge/inserted_at substrate → ADDED in PR #160.
- P-33: weighted graph W_t + W_{t-1} + Frobenius + consec counters → ADDED in PR #160.
- P-32: rolling `stable_turns/total_turns` counters + Fibonacci checkpoint index + phi* target → MISSING.
- P-27: per-input category + confidence + entropy/kappa scores + policy output → MISSING.
- P-29: routing record (category/policy/confidence) + hook_point + deontic classification → MISSING.
- P-30: attestation grade/confidence + artifact description + gold-star flag → MISSING.
- DemiJoule: six-axis score carrier (identity/intent/consent/risk/provenance/coherence) → MISSING.

## Sequencing (operator-set)
Phase A (P-31/P-33) DONE → unmerged PR #160.
Phase B: reconcile+RESTORE P-27/P-32 (both contract-qualified) → new candidate.
Phase C: extract exact contracts for P-29/P-30/DemiJoule (currently leads) → reconcile or mark FAIL-CLOSED-with-rationale.
Phase D: 7-gate candidate → P2/P6a → P3–P9 → freeze → authorization → N=1.

## Honesty note
- 4/7 are now at contract-or-registry qualification (P-31,P-33,P-32,P-27). 3/7 remain leads (P-29,P-30,DemiJoule).
- Until ALL seven are RESTORE or governed-ADAPT, the constitutive treatment is incomplete and N stays 0.
- No apparatus on `main` changed; no freeze; no authorization; no empirical execution.

---
*Amethyst-governed · fail-closed enforced · no empirical claim while N=0*
