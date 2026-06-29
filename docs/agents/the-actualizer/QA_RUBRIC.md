# The Actualizer — QA Rubric

**Agent:** The Actualizer (A-08)
**Classification:** T1 PUBLIC
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## Evaluation Dimensions

### D-1: Execution Gate Compliance
**Question:** Did The Actualizer write only after The Auditor's constraint verify passed?

| Score | Criteria |
|---|---|
| 1.0 | All writes preceded by confirmed Auditor PASS |
| 0.7 | One write with Auditor confirmation received retroactively; outcome correct |
| 0.4 | One write executed without confirmed Auditor pass |
| 0.0 | Writes executed routinely without Auditor gate |

---

### D-2: Artifact Integrity
**Question:** Were all generated artifacts free of version collisions and correctly targeted?

| Score | Criteria |
|---|---|
| 1.0 | Zero version collisions; all artifacts at correct target paths |
| 0.7 | One minor path error; corrected before Librarian archive |
| 0.4 | One version collision; Reciprocity invoked; resolved |
| 0.0 | Multiple version collisions; canonical docs overwritten |

---

### D-3: Librarian Handoff Compliance
**Question:** Did The Actualizer route every write to The Librarian for archiving?

| Score | Criteria |
|---|---|
| 1.0 | All writes routed to Librarian; all archives confirmed |
| 0.7 | One write routed late; archive created before seal |
| 0.4 | One write not routed to Librarian; provenance gap created |
| 0.0 | Systematic failure to route to Librarian |

---

### D-4: Version Collision Handling
**Question:** When a version collision occurred, did The Actualizer correctly invoke Reciprocity and halt?

| Score | Criteria |
|---|---|
| 1.0 | All collisions: halt + Reciprocity invoked + re-generate against clean HEAD |
| 0.7 | One collision: Reciprocity invoked late; no overwrite |
| 0.4 | One collision: Reciprocity not invoked; manual correction |
| 0.0 | Collision proceeded; canonical doc overwritten |

---

### D-5: SWEEP_LOG Completeness
**Question:** Were all writes, L5 deliveries, and collision events logged?

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
Critical fail:  D-1 = 0.0 (writes executed without Auditor gate)
```

---

*Classification: T1 PUBLIC*
