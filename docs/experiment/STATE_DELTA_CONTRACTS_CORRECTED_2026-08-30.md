# State-Delta Contracts — P-27 / P-29 / P-30 / P-32 / DemiJoule

**Date:** 2026-08-30 · READ-ONLY analysis artifact (no apparatus change)

**Boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0

**Companion:** SEVEN_GATE_RECOVERY_MATRIX_2026-08-30.md

Format per gate: `historical required field → current ConsensusState field → missing state → required addition → semantic-preservation test`.

---

## P-32 Phi Closure (CONTRACT-QUALIFIED — anchor: 49854ea historical impl)

| Historical required field | Current field | Missing | Required addition | Preservation test |
|---|---|---|---|---|
| `record_turn(is_stable)` rolling counters | NONE | stable/total counters | Add `phi_stable_count`, `phi_total_count` | ratio = stable/total reproduces after N turns |
| `R = stable/total` vs `φ* = 0.618` | NONE | ratio + target | Add `phi_ratio: float` (+ use `PHI_STAR`, NOT `PSI`) | ratio converges near 0.618 over stable run |
| Fibonacci checkpoints 13/21/34/55 + tolerances 0.07/0.05/0.04/0.03 | NONE | checkpoint index | Add `phi_checkpoint_index` derived from `iteration` | check() fires only at Fib turns; tolerance narrows |
| Decision ladder PASS/WARN/ESCALATE/KILL_REC | NONE | decision enum carry | Hook returns `GateResult` mapped: PASS→PASS, WARN→WARN, ESCALATE→WARN, KILL_REC→KILL | 2+ consec fails → KILL_REC; Fib[55]→KILL_REC+human |
| HPG bypass rule (PASS only) | NONE | gating signal | Surface decision to TGL step 7 | HPG runs only when Phi PASS |

**CRITICAL:** current `main` `ensemble_v16.py:441` uses `abs(ratio - PSI)` (bug). RESTORE must use `PHI_STAR` from the historical contract. Reference oracle = `49854ea` `FibonacciPhiClosureGate`.

---

## P-27 KAPPA (CONTRACT-QUALIFIED — anchor: 66b79e24 v3.5 card)

| Historical required field | Current field | Missing | Required addition | Preservation test |
|---|---|---|---|---|
| per-input `category` (adversarial/ambiguous/governance_clear/creative_clear/balanced) | NONE | input category | Add `kappa_category: str` | category detection matches regex priority list |
| `confidence` (0.60·pattern + 0.40·continuous + length_boost) | NONE | confidence score | Add `kappa_confidence: float` + `kappa_breakdown` | conf reproduces card formula on known input |
| `entropy_score`, `kappa_score` | NONE | entropy/kappa inputs | Add `kappa_entropy`, `kappa_kappa` | heuristic band matches |
| policy thresholds 0.28/0.25 (strong/blended/fallback) | NONE | threshold decision | Add thresholds (pin v3.5 card) | conf≥0.28→strong, 0.25–0.28→blended, <0.25→fallback |
| output `selected_weights`, `detected_category`, `policy` | NONE | routing output | Emit weight-set for HPG step 6 | output dict schema matches card `output_fields` |

**CAVEAT:** pin to v3.5 card; v3.6 code added categories (sequential/fan_out) not in card. RESTORE substrate to v3.5 semantics.

---

## P-29 Sentinel (REGISTRY-QUALIFIED / lead — anchor: registry:326 + evaluate_router_v1_1.py)

| Historical required field | Current field | Missing | Required addition | Preservation test |
|---|---|---|---|---|
| `record.category` | NONE | record category | Add `sentinel_record_category` | sentinel_review reads it |
| `routing.policy` / `routing.confidence` | NONE | routing state | Add `sentinel_routing_policy`, `sentinel_routing_confidence` | routing passed to review |
| `hook_point` (after_category_detection / after_weight_selection / before_report) | NONE | hook point | Add `sentinel_hook_point` | P-10 deontic gate at hook_point=1 only |
| decision `risk_ok`/`risk_warn`/`risk_block` (only risk_block halts) | NONE | decision + halt | Hook returns `GateResult`; `risk_block`→KILL | risk_block halts emission; warn/ok continue |

**NOTE:** `evaluate_router_v1_1.py` is side-effect-free; the halt is orchestrator-enforced. RESTORE must define where the pilot enforces the halt. Registry entry is canonical but NOT a standalone v1.0 gate contract → remains lead-grade until a dated contract is extracted.

---

## P-30 Apogee (LEAD / schema-grade — anchor: attestation_gate_spec.md + APOGEE_11Q_*.json + ensemble_v17.ApogeeReviewer)

| Historical required field | Current field | Missing | Required addition | Preservation test |
|---|---|---|---|---|
| `confidence` (attestation grade input) | NONE | confidence | Add `apogee_confidence: float` | grade computed from confidence |
| `artifact_description` | NONE | artifact text | Add `apogee_artifact: str` | gold-star requires len>5 |
| grade thresholds (S≥0.90, A≥0.75, B≥0.60, C≥0.45, D≥0.0) | NONE | grade ladder | Add thresholds | review() returns correct grade |
| `gold_star` (S + desc>5) | NONE | gold-star flag | Add `apogee_gold_star: bool` | gold-star logic matches |
| attestation decision (GRANTED/CONDITIONAL/DENIED per APOGEE_11Q) | NONE | decision | Map to `GateResult` | decision vocabulary matches QA schema |

**NOTE:** `ApogeeReviewer` (v17) uses S/A/B/C/D cutoffs 0.90/0.75/0.60/0.45 — these do NOT match the `APOGEE_11Q` (≥0.95/≥0.85) nor `attestation_gate.py` (ATTESTED/REJECTED/PENDING/REVOKED). **Internal contradiction** — must resolve which is normative before RESTORE. Currently lead.

---

## DemiJoule (LEAD — NO dated contract; two contradictory impls)

| Historical required field | Current field | Missing | Required addition | Preservation test |
|---|---|---|---|---|
| six-axis scores: identity/intent/consent/risk/provenance/coherence | NONE | full six-axis carrier | Add `demijoule_axes: Dict[str,float]` | all six axes present |
| scoring function (v16: payload['safety'] precomputed; v17: keyword/regex) | NONE | scorer | RESOLVE contradiction — pick ONE normative scorer | scorer reproducible |
| decision PASS/REPROMPT/WARN/ESCALATE | NONE | decision | Hook returns `GateResult` (PASS→PASS, else→WARN/ESCALATE) | decision ladder matches chosen impl |

**BLOCKER:** No dated/versioned normative contract exists; v16 and v17 `DemiJouleGate` contradict each other (input type, axes handling, thresholds). **Cannot RESTORE faithfully until a single authoritative contract is designated.** Currently lead; if none can be designated, DemiJoule stays FAIL-CLOSED-with-rationale (allowed per Issue #152).

---

## Summary

| Gate | Qualification | RESTORE ready? | Blocker |
|---|---|---|---|
| P-31 | contract | YES (PR #160) | — |
| P-33 | contract | YES (PR #160) | — |
| P-32 | contract | YES (pending impl) | use 49854ea impl, not main (PSI bug) |
| P-27 | contract* | YES (pending impl) | pin v3.5 card |
| P-29 | registry/lead | NO | extract dated contract; define halt enforcement |
| P-30 | lead/schema | NO | resolve S/A/B/C/D vs 11Q vs ATTESTED contradiction |
| DemiJoule | lead | NO | no authoritative contract; v16≠v17 |

4/7 ready-or-done for RESTORE (P-31,P-33 done; P-32,P-27 ready pending impl). 3/7 blocked on extraction/resolution.

N remains 0 until all seven RESTORE/ADAPT and the full candidate verifies.

## Governance boundary

Amethyst-governed · fail-closed enforced · no empirical claim while N=0
