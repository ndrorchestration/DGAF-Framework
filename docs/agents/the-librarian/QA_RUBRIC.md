# The Librarian — QA Rubric

**Agent:** The Librarian (A-06)
**Classification:** T1 PUBLIC
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## Evaluation Dimensions

### D-1: Archive Completeness
**Question:** Does every canonical decision have a corresponding Librarian archive entry?

| Score | Criteria |
|---|---|
| 1.0 | Zero gaps; every canonical decision archived |
| 0.7 | One gap detected and backfilled before seal |
| 0.4 | One gap not backfilled before seal |
| 0.0 | Multiple gaps; Provenance Traceability guarantee broken |

---

### D-2: Provenance Accuracy
**Question:** Are all archive entries accurate — correct agent, protocol, timestamp, and commit?

| Score | Criteria |
|---|---|
| 1.0 | All entries accurate; no Apogee corrections required |
| 0.7 | One field error corrected by Apogee cross-check |
| 0.4 | Multiple field errors requiring Apogee correction |
| 0.0 | Systematic provenance contamination |

---

### D-3: Gap Response Timeliness
**Question:** Did The Librarian backfill detected gaps before the session seal?

| Score | Criteria |
|---|---|
| 1.0 | All gaps backfilled and Apogee-verified before seal |
| 0.7 | One gap backfilled but Apogee verification pending at seal |
| 0.4 | One gap not addressed before seal |
| 0.0 | No gap response; seal proceeded with known provenance gap |

---

### D-4: Apogee Cross-Check Alignment
**Question:** Did Librarian entries pass Apogee evidence scoring cross-check?

| Score | Criteria |
|---|---|
| 1.0 | All entries pass Apogee cross-check |
| 0.7 | One entry flagged; corrected |
| 0.4 | Multiple entries flagged |
| 0.0 | Systematic Apogee cross-check failures |

---

### D-5: SWEEP_LOG Completeness
**Question:** Were all archive, backfill, and amendment events logged?

| Score | Criteria |
|---|---|
| 1.0 | All events logged with required fields |
| 0.7 | One entry missing |
| 0.4 | Multiple entries missing |
| 0.0 | No SWEEP_LOG entries |

---

## Composite Score

```
Composite = (D-1 × 0.40) + (D-2 × 0.25) + (D-3 × 0.20) + (D-4 × 0.10) + (D-5 × 0.05)
Pass threshold: ≥0.80
Critical fail:  D-1 = 0.0 (Provenance Traceability guarantee broken)
```

---

*Classification: T1 PUBLIC*
