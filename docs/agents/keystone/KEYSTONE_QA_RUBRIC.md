# Keystone — QA Rubric v1.0

**Agent:** Keystone
**Agent ID:** A-31
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-09-04

---

## Evaluation Dimensions

### D1 — Inspection Coverage (weight: 0.25)

| Criterion | Pass condition |
|---|---|
| All in-scope workflows inspected | Every workflow YAML file in the specified scope is read and parsed |
| All in-scope pins inspected | Every pinned artifact in the specified scope is identified and assessed |
| All in-scope permissions audited | Every permissions block and GITHUB_TOKEN usage in the specified scope is assessed |
| All in-scope fail-closed gates inspected | Every gate designed to fail closed is assessed for correct structure |

**Critical fail:** A workflow, pin, permission, or gate in the specified scope is not inspected.

### D2 — Finding Accuracy (weight: 0.30)

| Criterion | Pass condition |
|---|---|
| File paths correct | Every file path cited in a finding actually exists at the specified SHA |
| Line references correct | Every line reference points to the content Keystone claims it points to |
| Defect classification correct | Each finding is classified into the correct defect type based on the inspected content |
| Severity assessment reasonable | Each severity assessment is justified by the potential impact of the defect on fail-closed posture, evidence integrity, or reproducibility |

**Critical fail:** A cited file path or line reference does not match the actual file content.

### D3 — Evidence Citation (weight: 0.20)

| Criterion | Pass condition |
|---|---|
| Findings cite specific content | Each finding includes the specific workflow content (trigger entry, permission block, pin entry, gate step) that supports the finding |
| No fabricated content | No finding cites content that does not exist in the inspected file |
| Download URLs accurate | Pin-management findings cite the actual download URL from the workflow, not an inferred or incorrect URL |

**Critical fail:** A finding cites content that does not exist in the inspected file.

### D4 — Boundary Respect (weight: 0.15)

| Criterion | Pass condition |
|---|---|
| No CI execution claimed | Keystone does not claim to have executed CI or triggered runs |
| No fix implementation claimed | Keystone does not claim to have edited files or implemented fixes |
| No gate closure claimed | Keystone does not claim to have closed a gate or authorized a fix |
| Runtime vs structure distinguished | Keystone distinguishes between structural assessment and runtime verification |

**Critical fail:** Keystone claims to have performed an action outside its lane.

### D5 — Integration Quality (weight: 0.10)

| Criterion | Pass condition |
|---|---|
| Cross-agent findings connected | When a structural finding has provenance implications, Keystone notes that Continuum should assess it |
| Cross-agent findings connected | When a structural finding has a CI-execution correlation, Keystone notes that Clarion's runtime diagnosis may be relevant |
| Cross-agent findings connected | When a structural defect is in a workflow that Cadence may sequence, Keystone notes the sequencing implication |

---

## Composite Score

```
Keystone QA Score = D1×0.25 + D2×0.30 + D3×0.20 + D4×0.15 + D5×0.10
Pass threshold: ≥ 0.75
Critical fail (D1 or D2 or D4): automatic rubric fail regardless of composite
```

---

*Classification: T1 PUBLIC*
