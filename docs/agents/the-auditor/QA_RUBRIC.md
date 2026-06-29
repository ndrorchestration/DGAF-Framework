# The Auditor — QA Rubric

**Agent:** The Auditor (A-07 / Beta / The Pulse)
**Classification:** T1 PUBLIC
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## Evaluation Dimensions

### D-1: Constraint Verify Accuracy
**Question:** Did The Auditor correctly pass clean artifacts and block all artifacts failing logic coherence, phi-bounded iteration, or write order checks?

| Score | Criteria |
|---|---|
| 1.0 | All pass/block decisions correct; zero missed fails |
| 0.7 | One edge-case artifact passed with minor ambiguity; outcome clean |
| 0.4 | One structurally failing artifact passed to Actualizer |
| 0.0 | Systematic passes of failing artifacts; Actualizer writing without valid constraint verify |

---

### D-2: H-Neuron Suppression Accuracy
**Question:** Did The Auditor correctly detect over-compliance and hallucination signals (α ≥ 1) and suppress them before Actualizer write?

| Score | Criteria |
|---|---|
| 1.0 | All H-Neuron signals detected; none passed to Actualizer |
| 0.7 | One marginal signal detected late; caught before write |
| 0.4 | One H-Neuron signal passed to Actualizer |
| 0.0 | Systematic hallucination signals passed through |

---

### D-3: Savage Reason / Jitter Detection
**Question:** Did The Auditor identify all internal Savage Reason (>10 Hz) or hallucinatory jitter signals and route them correctly?

| Score | Criteria |
|---|---|
| 1.0 | All signals detected; correctly routed to Apogee/Prof Prodigy |
| 0.7 | One signal detected; routing delayed |
| 0.4 | One signal missed; caught by downstream agent |
| 0.0 | Multiple signals missed; entered Actualizer write chain |

---

### D-4: Ionia Cross-Check Compliance
**Question:** Did The Auditor correctly execute the Ionia false-positive cross-check when requested?

| Score | Criteria |
|---|---|
| 1.0 | All cross-checks executed promptly; verdicts accurate |
| 0.7 | One delayed cross-check; verdict accurate |
| 0.4 | Cross-check executed; verdict inaccurate (false-positive missed) |
| 0.0 | Cross-check not executed; Ionia false-positive passed to Amethyst seal |

---

### D-5: SWEEP_LOG Completeness
**Question:** Were all constraint verify, H-Neuron, jitter, and Ionia cross-check events logged?

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
Critical fail:  D-1 = 0.0 (Actualizer writing without valid constraint verify)
```

---

*Classification: T1 PUBLIC*
