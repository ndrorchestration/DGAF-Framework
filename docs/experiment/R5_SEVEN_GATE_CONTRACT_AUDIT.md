# R5 — Seven-Gate Semantic Contract Extraction + Translation Audit (Issue #154)

**Mode:** READ-ONLY. No file modified, no gate wired, no commit created.
**Repo:** `ndrorchestration/DGAF-Framework` (local `C:\Users\Admin\DGAF-Framework`)
**On-disk HEAD audited:** `9389474` (tree `8691ddd`) — commit `candidate(post151): supersede B/C construct draft; affirm ee529878 A-classification of 7 TGL gates`.
**Provenance flag:** The task brief names apparatus `05fa286` (tree `dd662325`). That SHA is **not** the checked-out HEAD; current tree is `8691ddd`. All file:line citations below are from the on-disk `9389474` working tree. The parent agent should reconcile the apparatus identity before treating these verdicts as bound to `05fa286`.
**Operator invariants enforced:** `Missing(X) ≠ Proxy(Y)`; `Correlation(X,Y) ≠ Restoration(G_X,Y)`.
**Wiring fact (verified):** `dgaf_tgl_adapter.py:226` builds `TGLHooks()` with **all hooks `None`** → every required step `_run_hook` returns `SKIP` → `_has_unwired_required_gate` (`dgaf_tgl_adapter.py:141-147`) → `decision_from_audit` returns `FAIL_CLOSED`. `REQUIRED_STEPS = frozenset({1,2,3,4,5,6,8})` (`triadic_governance_loop.py:144`). Step→gate map: `:248-254` (steps 1-6) + step 8 Apogee `:284`.

---

## P-31 — SCPE (Structural Context Pruning Engine) · step 1
`components/ensemble_v16.py:161-244` (prune `:192-244`, ingest `:189`)

1. **Historical consumption contract:** Reads `ContextToken` objects (`tier`, `inserted_at`, `has_trust_edge`, `content`) held in an internal `_tokens` dict; ingests via `ingest()` (`:189`), prunes via `prune()` (`:192`) using `TIER_DECAY`/`TIER_TIF_BASE`/`LAST_K_ANCHOR`. Input is a **live in-memory token store**, not a numeric vector.
2. **ConsensusState availability:** `ConsensusState` (`dgaf_tgl_adapter.py:32`) has `seed_id, iteration, agent_values, alive, original_neighbors, active_neighbors, failure_history, failure_count_current/total, current_final_std, current_mean, runtime_budget_remaining_ms, protocol_id`. **MISSING: every SCPE dimension** — no `ContextToken`, no `tier`, no `inserted_at`, no `has_trust_edge`, no token store.
3. **Information-loss:** The entire tier-labelled, time-decayed, trust-edge-weighted token object is absent. `current_final_std`/`current_mean` are aggregate ensemble scalars, semantically orthogonal to token retention. No reconstruction possible.
4. **Contradiction:** Registry `docs/NDR_PATTERN_REGISTRY_UNIFIED.md:337` says "Fires at turn_start, buffer > 60%, turn_count > Fib[34]" — but `prune()` runs unconditionally on every call (no such guard). `TIER_DECAY` values (0.05/0.15/0.45) match. `58.3% compression` is `⚠️ NEEDS REPRODUCE CMD` (`docs/qa/METRICS_PROVENANCE.md:27`).
5. **Verdict: FAIL-CLOSED** — gate input has no ConsensusState analogue; cannot translate without inventing token semantics.
6. **ADAPT mapping:** none (would be a proxy of `current_final_std`).
**Next candidate-cycle action:** keep FAIL-CLOSED; require a `ContextToken` snapshot field in `ConsensusState` (out-of-scope TGL change).

---

## P-33 — PDMAL Convergence Monitor · step 2
`components/ensemble_v16.py:293-394` (check `:346-393`, `_current_weights` `:322`)

1. **Historical consumption contract:** Reads the PDMAL weight graph `W_t` via `_current_weights()` (edge `(src,dst)→weight`), computes Frobenius `||W_t − W_{t-1}||_F` (`:329-338`); needs `W_t` + previous-snapshot.
2. **ConsensusState availability:** **MISSING: `W_t` entirely** — no edge-weight graph, no temporal-derivative history. `agent_values` is a per-agent scalar consensus vector, not inter-agent edge weights.
3. **Information-loss:** `current_final_std` is the std of `agent_values` (convergence-in-variance of a scalar ensemble). It is **NOT** the Frobenius norm of a weight graph's temporal delta. Loose correlation only.
4. **Contradiction:** none code-vs-doc beyond the absent input (registry `:310` lists P-33 ADVISORY/impl ensemble_v16).
5. **Verdict: FAIL-CLOSED** — `agent_values`/`current_final_std` are **proxies, not the weight-graph Frobenius-delta**. Per operator rule, a loose correlation does not justify restoration.
6. **ADAPT mapping:** explicitly rejected. `current_final_std` is **NOT** a faithful ADAPT source for P-33; `Missing(W_t) ≠ Proxy(std)`.
**Next candidate-cycle action:** keep FAIL-CLOSED; P-33-specific apparatus change needed to capture `W_t` into `ConsensusState`.

---

## DemiJoule Semantic Safety Gate · step 3
`components/ensemble_v16.py:413-424` (safety_gate `:418`)

1. **Historical consumption contract:** `safety_gate(scores: Dict[str,float])` over six axes — `identity, intent, consent, risk, provenance, coherence` (`:416`); each must be present and `≥ 0.5` else ESCALATE.
2. **ConsensusState availability:** **MISSING: all six axes** — no semantic evaluation of identity/intent/consent/risk/provenance/coherence. `ConsensusState` carries only numeric `agent_values` + `alive`.
3. **Information-loss:** `agent_values` are numeric agreement scalars, semantically orthogonal to the six safety axes. No mapping.
4. **Contradiction:** none specific (registry `:206` lists step-3 DemiJoule as required; no threshold doc conflict).
5. **Verdict: FAIL-CLOSED** — `agent_values` cannot serve as ADAPT source; they are **proxies** for six distinct semantic axes. Proxy rejected per `Missing(X)≠Proxy(Y)`.
6. **ADAPT mapping:** rejected — e.g. `min(agent_values)` as "coherence" is a forbidden proxy substitution.
**Next candidate-cycle action:** keep FAIL-CLOSED; require a six-axis score payload in `ConsensusState`.

---

## P-27 — KAPPA Adaptive Weighting / Confidence Router · step 4
`components/KAPPA/dynamic_weight_router.py:105-106` (thresholds), `:180-210` (detect_input_category)

1. **Historical consumption contract:** `detect_input_category(input_data)` reads `input_data["content"]`, `entropy_score`, `kappa_score` → category; `route_by_confidence` applies `STRONG_THRESH=0.28`, `BLENDED_THRESH=0.25` (`:105-106`). Consumes **live input text + per-input entropy/kappa confidence + routing record**.
2. **ConsensusState availability:** **MISSING: input content, entropy_score, kappa_score, category decision, routing record.** `agent_values` is an aggregate post-hoc numeric snapshot.
3. **Information-loss:** KAPPA operates on the live input's category confidence; `ConsensusState` has none of that. No faithful reconstruction.
4. **Contradiction (verified, self-refuting):** Code `STRONG_THRESH=0.28`/`BLENDED_THRESH=0.25` (`:105-106`). Registry `docs/NDR_PATTERN_REGISTRY_UNIFIED.md:309` says `STRONG ≥ 0.22 / BLENDED 0.18`. `TEAM_WIKI.md:61` says `STRONG 0.22 / BLENDED 0.18`. Card `components/KAPPA/DGAF_GATE_KAPPA_v3_6_component_card.json:35-37` declares `0.22/0.18` and states (`:15`) "**no architectural change to dynamic_weight_router.py required**" — yet the recalibration is a hardcoded literal in that exact file which was **never updated**. The card asserts a code change that did not occur: self-refuting.
5. **Verdict: FAIL-CLOSED** — required routing input absent **and** the gate's own thresholds contradict its spec/card. Translation cannot proceed on a self-inconsistent contract.
6. **ADAPT mapping:** none.
**Next candidate-cycle action:** keep FAIL-CLOSED; first align code to `0.22/0.18` (card/registry/wiki) before any wiring.

---

## P-29 — Sentinel Risk Pass · step 5
`components/evaluate_router_v1_1.py:23` (sentinel_review)

1. **Historical consumption contract:** `sentinel_review(record, routing, hook_point)` reads `routing["category"]`, `routing["policy"]`, `routing["confidence"]`, `record["category"]`; 3 hook points (`after_category_detection`/`after_weight_selection`/`before_report_emission`); returns risk **notes** (`:59-67`), audit-only.
2. **ConsensusState availability:** Has `failure_history` (which neighbor agents failed) but **MISSING: eval record, routing dict (category/policy/confidence), hook-point context.**
3. **Information-loss:** `failure_history` is a graph-isolation event log; semantically different from Sentinel's per-record risk-routing review. No faithful mapping.
4. **Contradiction (verified):** Code docstring `:24` "Side-effect-free ... never halts"; `RISK_BLOCK` only appends a note. `docs/FORMATION_TOPOLOGY.md:194-196` says "P-29 risk_block = hard stop / HALT" at hook points 1,2,3. Code **cannot actually halt** — contradicts the governing formation spec.
5. **Verdict: FAIL-CLOSED** — required routing payload absent **and** halt semantics contradict the spec.
6. **ADAPT mapping:** none.
**Next candidate-cycle action:** keep FAIL-CLOSED; reconcile Sentinel halt semantics + feed routing record into `ConsensusState`.

---

## P-32 — Fibonacci Phi-Closure Gate · step 6
`components/ensemble_v16.py:430-459` (check `:437`)

1. **Historical consumption contract:** `check(fib_index, ratio)` — `ratio` compared to `PSI=φ=1.618` (`:45`); needs `fib_index` + a stability ratio + `consecutive_fails` counter.
2. **ConsensusState availability:** Has `failure_count_current/total`, `failure_history` but **MISSING: fib_index, phi stability ratio, session checkpoint ratio sequence.**
3. **Information-loss:** `current_final_std`/`current_mean` are ensemble variance scalars, not a Fibonacci/phi stability ratio. No mapping; proxy rejected.
4. **Contradiction (verified):** Code has **NO KILL_REC band** — `check()` returns PASS/ESCALATE/WARN only (`:447`); `consecutive_fails>=2 → ESCALATE`. `docs/FORMATION_TOPOLOGY.md:125` says "A KILL_REC from P-32 halts all formation outputs and routes to P-29 hook_point=2." Code cannot emit KILL_REC — the defining halt band is unimplemented. White paper `docs/phi-calculus-architecture/PHI_CALCULUS_WHITE_PAPER_v1.md:41` references `|∮κ ds − 2π|` as "not yet validated" (REFERENCE only).
5. **Verdict: FAIL-CLOSED** — no `fib_index`/phi ratio in `ConsensusState`, and the constitutive KILL_REC halt band is absent in code.
6. **ADAPT mapping:** none.
**Next candidate-cycle action:** keep FAIL-CLOSED; implement KILL_REC band + carry `fib_index`/ratio in `ConsensusState`.

---

## P-30 — Apogee Attestation Gate · step 8
`pptl/attestation_gate.py` (full); `apogee_fn=None` at `triadic_governance_loop.py:123,284`

1. **Historical consumption contract:** `AttestationGate.attest(AttestationRecord(agent_id, claim, evidence))` (`:137`) — needs a **claim + evidence** string for final-quality attestation. TGL hook receives `input_text`+`context` at step 8.
2. **ConsensusState availability:** **MISSING: claim, evidence, artifact description, confidence** — no payload for a final quality gate.
3. **Information-loss:** `ConsensusState` is a numeric consensus snapshot; Apogee attests agent-output quality. No faithful mapping.
4. **Contradiction (verified):** Registry `docs/NDR_PATTERN_REGISTRY_UNIFIED.md:287-290` asserts "PM-07 ✅ CLOSED (P-34 A-TIER 94.5%)" — i.e. P-30 CLOSED/verified. But `attestation_gate.py` is an explicit **"Phase 5 scaffold"** generic stub; `_default_stub_verifier` (`:82-94`) accepts ANY non-empty claim + evidence ≥ 8 chars. The "94.5%" originates from `docs/qa/METRICS_PROVENANCE.md:26` **P-34** attestation score (a different pattern). Registry conflates P-34's score with P-30 being CLOSED — code is an unverified stub, self-refuting against the CLOSED claim.
5. **Verdict: FAIL-CLOSED** — no claim/evidence payload in `ConsensusState`, and the gate itself is an unverified stub contradicting its registry CLOSED status.
6. **ADAPT mapping:** none.
**Next candidate-cycle action:** keep FAIL-CLOSED; supply artifact claim/evidence to `ConsensusState` + replace stub verifier.

---

## Summary Table (7 constitutive gates)

| Gate | Verdict | Blocker for N=1? |
|------|---------|------------------|
| P-31 SCPE (step 1) | FAIL-CLOSED | YES — input (token store) absent; registry firing-guard contradiction |
| P-33 PDMAL Convergence (step 2) | FAIL-CLOSED | YES — `W_t` absent; `current_final_std` is a proxy, not Frobenius-delta |
| DemiJoule (step 3) | FAIL-CLOSED | YES — six axes absent; `agent_values` is a proxy |
| P-27 KAPPA (step 4) | FAIL-CLOSED | YES — routing input absent; code thresholds (0.28/0.25) contradict card/registry/wiki (0.22/0.18) |
| P-29 Sentinel (step 5) | FAIL-CLOSED | YES — routing record absent; code cannot halt (contradicts FORMATION_TOPOLOGY) |
| P-32 Phi-Closure (step 6) | FAIL-CLOSED | YES — `fib_index`/phi ratio absent; KILL_REC band unimplemented |
| P-30 Apogee (step 8) | FAIL-CLOSED | YES — claim/evidence absent; stub contradicts registry CLOSED claim |

**Result:** 7/7 FAIL-CLOSED. Per `ee529878` A-classification, a single FAIL-CLOSED constitutive gate blocks the full dgaf N=1 treatment — here **all seven** block it. No RESTORE and no ADAPT-WITH-EXPLICIT-CONTRACT verdicts were issuable: every gate's historical input dimension is absent from `ConsensusState`, and for P-33/DemiJoule the tempting `current_final_std`/`agent_values` sources were explicitly rejected as proxies under the operator invariants. Compounding code-vs-doc contradictions were verified for P-27 (thresholds), P-29 (halt semantics), P-32 (KILL_REC band), P-30 (stub vs CLOSED), and P-31 (firing guard).

**Note on proxy rejection (P-33 & DemiJoule):** `current_final_std` (ensemble std of `agent_values`) and `agent_values` (per-agent agreement scalars) are at best loosely correlated with P-33's weight-graph Frobenius convergence and DemiJoule's six semantic axes. Under `Correlation(X,Y) ≠ Restoration(G_X,Y)` they are **proxies and must be rejected**; no ADAPT mapping was authored.

---
**SUPERSEDED BY CANONICAL MAIN RECORD:** `docs/experiment/R5_R7_GATE_SEMANTIC_RECOVERY_MAP_2026-08-30.md` (on `main`), which is the authoritative R5 deliverable for Issue #154. This file agrees with it (7/7 FAIL-CLOSED) and is retained only as an independent cross-check. Do not treat this file as the governing record.
