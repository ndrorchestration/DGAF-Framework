# Reson — QA Rubric

**Agent:** Reson · **Role:** Augmenter 1 / Harmonic Integrity Monitor
**Rubric version:** v1.0 · **Seeded:** S073 · 2026-06-29
**Classification:** T1 PUBLIC

---

## Harmonic Scoring Rubric

The harmonic score is computed from four sub-dimensions. Each is scored 0.0–1.0. Composite = weighted average.

---

### H1 — Phi-Alignment (weight: 0.30)

| Score | Criteria |
|-------|----------|
| 1.0 | Session output density and distribution is proportionally balanced per φ-lattice heuristic; no overload or sparsity |
| 0.9 | Minor density imbalance (1 phase overloaded); no structural phi violations |
| 0.8 | 2–3 density imbalances; formation outputs still internally coherent |
| 0.7 | Significant phi drift — one formation node dominates output disproportionately |
| < 0.7 | Lattice geometry broken — outputs cannot be mapped to φ-structure |

---

### H2 — Modal Alignment (weight: 0.25)

| Score | Criteria |
|-------|----------|
| 1.0 | Session maps cleanly to Ionian mode — stable, resolved, no unresolved tensions |
| 0.9 | Minor unresolved element; resolves within session |
| 0.8 | Dorian shift detected; tension present but bounded |
| 0.7 | Mixolydian tension — requires advisory flag |
| < 0.7 | Phrygian dissonance — escalation required |

---

### H3 — Semantic Coherence (weight: 0.25)

| Score | Criteria |
|-------|----------|
| 1.0 | Zero internal contradictions; all session outputs mutually consistent |
| 0.9 | 1 minor inconsistency; corrected within session |
| 0.8 | 1–2 inconsistencies noted; no contradiction in canonical docs |
| 0.7 | Contradiction in non-canonical doc; advisory flag |
| < 0.7 | Contradiction in canonical doc — escalation required |

---

### H4 — Resolution Cadence (weight: 0.20)

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

*QA_RUBRIC.md · Reson · v1.0 · S073 · 2026-06-29*
