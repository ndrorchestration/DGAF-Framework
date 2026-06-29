# Ionia — QA Rubric

**Agent:** Ionia (A-13)
**Classification:** T2 FRAMEWORK
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## Evaluation Dimensions

### D-1: Lock Accuracy
**Question:** Did Ionia correctly lock to 0Hz when Reson score ≥0.75, and correctly withhold the lock when score <0.75?

| Score | Criteria |
|---|---|
| 1.0 | All lock/withhold decisions correct |
| 0.7 | One marginal withhold at edge threshold; corrected |
| 0.4 | Lock issued at Reson score <0.75 |
| 0.0 | Lock consistently issued regardless of Reson score |

---

### D-2: Reson Coupling Integrity
**Question:** Did Ionia correctly receive and process Reson scores before issuing lock confirmations?

| Score | Criteria |
|---|---|
| 1.0 | All lock confirmations traceable to a Reson score ≥0.75 |
| 0.7 | One lock confirmation with minor Reson score ambiguity; resolved |
| 0.4 | Lock confirmation issued without traceable Reson score |
| 0.0 | Systematic lock confirmations with no Reson coupling |

---

### D-3: Seal Gate Compliance
**Question:** Did Ionia provide lock confirmation before every harmonic-sensitive seal commit?

| Score | Criteria |
|---|---|
| 1.0 | Lock confirmation issued before every qualifying seal |
| 0.7 | One seal proceeded without explicit confirmation; retroactively confirmed |
| 0.4 | One seal proceeded without any lock confirmation |
| 0.0 | Seal commits routinely bypassed Ionia lock gate |

---

### D-4: False-Positive Harmonic Detection
**Question:** Did Ionia cooperate with The Auditor's cross-check and respond accurately?

| Score | Criteria |
|---|---|
| 1.0 | All Auditor cross-checks responded to promptly with complete evidence |
| 0.7 | One delayed response; evidence complete |
| 0.4 | Incomplete evidence provided to Auditor |
| 0.0 | Auditor cross-check ignored or refused |

---

### D-5: SWEEP_LOG Completeness
**Question:** Were all lock events, withhold events, and failure events logged?

| Score | Criteria |
|---|---|
| 1.0 | All events logged with required fields |
| 0.7 | One entry missing |
| 0.4 | Multiple entries missing |
| 0.0 | No SWEEP_LOG entries |

---

## Composite Score

```
Composite = (D-1 × 0.35) + (D-2 × 0.25) + (D-3 × 0.20) + (D-4 × 0.15) + (D-5 × 0.05)
Pass threshold: ≥0.80
Critical fail:  D-3 = 0.0 (seal commits routinely bypassed lock gate)
```

---

*Classification: T2 FRAMEWORK*
