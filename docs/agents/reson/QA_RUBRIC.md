# Reson — QA Rubric

**Agent:** Reson · **Role:** Augmenter 1 / Harmonic Integrity Monitor
**Rubric version:** v1.1-DRAFT (construct clarification; non-authorizing) · **Original:** v1.0, S073, 2026-06-29
**Classification:** T1 PUBLIC

---

## Composite Process Integrity Score (legacy alias: Harmonic Scoring Rubric)

The composite score is computed from four sub-dimensions. Each is scored 0.0–1.0. Composite = weighted average. The legacy `harmonic_score` field name is preserved for compatibility.

**Evidence boundary:** These names describe proposed constructs, not established psychometric validity. The historical v1.0 scoring anchors below are retained for traceability and still contain metaphoric phi-lattice and musical-mode language. They must not be interpreted as experimentally calibrated metrics. The weights, thresholds, and actions are unchanged pending independent review and owner ratification. The 0.80–0.84 'proceed' / 0.85 seal-floor ambiguity remains open in issue #1559; this draft does not resolve it.

---

## Expert-lens line-by-line QA findings (provisional, not independent attestation)

| Scope | Finding | Disposition |
|---|---|---|
| Header/version | Version and provenance must distinguish a draft from an adopted instrument | Keep v1.0 on main; v1.1-DRAFT is non-authorizing |
| Construct labels | New names describe candidate observable properties more directly | Adopt names in draft only; legacy aliases retained |
| H1 anchors | “φ-lattice”, “density”, “phase”, and “overload” lack operational units, denominator, and justified target distribution | Historical anchors only; do not infer numerical precision |
| H2 anchors | Musical modes label states but do not specify observable transition events or allowable states | Require versioned state-transition inventory and violation evidence |
| H3 anchors | Contradiction severity and canonical/noncanonical source authority are not defined; consistency is not factual correctness | Require authority-bound contradiction annotation and adjudication |
| H4 anchors | Opened/closed/anchored counts do not define issue severity, owner, deadline, or observation window | Require issue ledger, provenance, severity, and regression criteria |
| Composite | Weighted average permits compensating a critical failure with unrelated high scores | Test noncompensatory vetoes separately before any decision use |
| Numerical weights | Weights are specified but lack calibration or sensitivity analysis | Retain for compatibility; label unvalidated |
| Threshold/action map | Dorian “proceed” at 0.80–0.84 conflicts with 0.85 seal floor under seal interpretation | Preserve issue #1559; no implicit seal authorization |
| Missing data | No production scorer or provenance/freshness contract established here | Treat missing/invalid evidence as unscored, not passing |

### Proposed operationalization protocol (not yet an adopted scoring algorithm)

- **Observation unit:** One explicitly identified session or run with immutable start/end timestamps and source revisions.
- **H1:** Record the set of expected output categories, each observed count or quantity, and a task-justified target distribution. Without a justified target and denominator, return **NOT_SCORED** rather than assume evenness or a golden-ratio target.
- **H2:** Record expected and observed workflow states, transition events, permitted transition table version, and unresolved violations. Without a versioned transition contract, return **NOT_SCORED**.
- **H3:** Compare claims against each other and against a versioned authoritative reference set; record contradiction IDs, severity, reviewer disagreements, and corrections. Do not conflate consistency with truth.
- **H4:** Record issue IDs, creation/disposition events, owners, deadlines, regression indicators, and observation window. A documented carry-forward is not automatically equivalent to resolution.
- **Scoring:** Anchor descriptions below are historical **ordinal exemplars**, not a validated interval scale. Do not calculate or use a decision-bearing composite until scoring units, missing-data handling, noncompensatory failures, and calibration are ratified.
- **Review evidence:** Require at least two independent blinded raters, disagreement adjudication, inter-rater reliability, and a held-out comparator against a simpler checklist before claiming validation.

---

### H1 — Structural Distribution Balance (legacy: Phi-Alignment; weight: 0.30)

| Score | Criteria |
|-------|----------|
| 1.0 | Session output density and distribution is proportionally balanced per φ-lattice heuristic; no overload or sparsity |
| 0.9 | Minor density imbalance (1 phase overloaded); no structural phi violations |
| 0.8 | 2–3 density imbalances; formation outputs still internally coherent |
| 0.7 | Significant phi drift — one formation node dominates output disproportionately |
| < 0.7 | Lattice geometry broken — outputs cannot be mapped to φ-structure |

---

### H2 — Workflow State Consistency (legacy: Modal Alignment; weight: 0.25)

| Score | Criteria |
|-------|----------|
| 1.0 | Session maps cleanly to Ionian mode — stable, resolved, no unresolved tensions |
| 0.9 | Minor unresolved element; resolves within session |
| 0.8 | Dorian shift detected; tension present but bounded |
| 0.7 | Mixolydian tension — requires advisory flag |
| < 0.7 | Phrygian dissonance — escalation required |

---

### H3 — Semantic Consistency and Contradiction Control (legacy: Semantic Coherence; weight: 0.25)

| Score | Criteria |
|-------|----------|
| 1.0 | Zero internal contradictions; all session outputs mutually consistent |
| 0.9 | 1 minor inconsistency; corrected within session |
| 0.8 | 1–2 inconsistencies noted; no contradiction in canonical docs |
| 0.7 | Contradiction in non-canonical doc; advisory flag |
| < 0.7 | Contradiction in canonical doc — escalation required |

---

### H4 — Issue Resolution and State Integrity (legacy: Resolution Cadence; weight: 0.20)

| Score | Criteria |
|-------|----------|
| 1.0 | Session ends in higher integrity state than it started; all opened items closed or properly anchored |
| 0.9 | 1 item opened and not closed (anchored for next session with clear owner) |
| 0.8 | 2 items anchored; no regression |
| 0.7 | Regression on 1 item (state worse at end than start) |
| < 0.7 | Multiple regressions or orphaned items |

---

## Composite Formula

```
harmonic_score = (H1 × 0.30) + (H2 × 0.25) + (H3 × 0.25) + (H4 × 0.20)
```

**Seal floor:** 0.85 · **Ionian sustained target:** ≥ 0.90
**Phrygian block threshold:** < 0.70 (emits ESCALATE, blocks seal)

---

## Modal State → Action Map

| Score | Modal State | Reson Action | Amethyst Action |
|-------|-------------|-------------|----------------|
| ≥ 0.90 | Ionian sustained | Emit score | Proceed to seal |
| 0.80–0.89 | Dorian shift | Emit score + advisory | Note in SESSION_ANCHORS; proceed |
| 0.70–0.79 | Mixolydian tension | Emit ALERT | Review before seal |
| < 0.70 | Phrygian dissonance | Emit ESCALATE | Remediate; re-score before seal |

---

*QA_RUBRIC.md · Reson · v1.1-DRAFT construct-clarity proposal; original v1.0 preserved on main.*
