# Perigee — QA Rubric

**Agent:** Perigee (A-02)
**Classification:** T1 PUBLIC
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## Evaluation Dimensions

### D-1: Block Accuracy
**Question:** Did Perigee correctly identify and block all signals exceeding AX-02 (>10 Hz dissonance) or confirmed contamination?

| Score | Criteria |
|---|---|
| 1.0 | All qualifying signals blocked; zero missed blocks |
| 0.7 | One marginal signal passed through below threshold; no Savage Reason missed |
| 0.4 | One Savage Reason signal passed through to formation |
| 0.0 | Multiple Savage Reason signals entered formation unblocked |

---

### D-2: False Positive Rate
**Question:** Did Perigee block any legitimate signals (dissonance ≤10 Hz; no contamination)?

| Score | Criteria |
|---|---|
| 1.0 | Zero false positives |
| 0.7 | One false positive; released promptly by Amethyst |
| 0.4 | Multiple false positives requiring Amethyst review |
| 0.0 | Systematic false positive pattern blocking formation function |

---

### D-3: Escalation Timeliness
**Question:** Did Perigee complete post-hoc escalation to Amethyst within the session in which the block occurred?

| Score | Criteria |
|---|---|
| 1.0 | Escalation sent immediately post-block in same session |
| 0.7 | Escalation sent within session but delayed |
| 0.4 | Escalation sent in subsequent session |
| 0.0 | No escalation sent |

---

### D-4: Compliance Dyad Alignment
**Question:** In dual-block scenarios, did Perigee correctly defer to the Compliance Dyad ruling?

| Score | Criteria |
|---|---|
| 1.0 | Correct deference; Dyad ruling followed without independent escalation |
| 0.7 | Minor procedural gap but outcome aligned |
| 0.4 | Perigee escalated independently despite Dyad ruling |
| 0.0 | Perigee overrode Dyad ruling |

---

### D-5: SWEEP_LOG Completeness
**Question:** Did Perigee produce complete SWEEP_LOG entries for all block and pass-through events?

| Score | Criteria |
|---|---|
| 1.0 | All events logged with required fields (origin, timestamp, reason, resolution) |
| 0.7 | Minor field omission in one entry |
| 0.4 | Multiple entries missing required fields |
| 0.0 | No SWEEP_LOG entries produced |

---

## Composite Score

```
Composite = (D-1 × 0.35) + (D-2 × 0.25) + (D-3 × 0.15) + (D-4 × 0.15) + (D-5 × 0.10)
Pass threshold: ≥0.80
Critical fail:  D-1 = 0.0 (Savage Reason passed to formation)
```

---

*Classification: T1 PUBLIC*
