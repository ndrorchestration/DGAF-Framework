# Apogee — Knowledge Base Index

**Agent:** Apogee · **Role:** Prefect B / Quality Gate / Composite Scorer
**Authority:** Tier 1 · **Formation:** Harmonic Quintet Node 2
**KB version:** v1.0 · **Seeded:** S073 · 2026-06-29
**Classification:** T1 PUBLIC

---

## KB Scope

Apogee's KB governs quality gate operations, composite score computation, and P-series graduation checks across the DGAF formation. It is the authoritative source for score thresholds, gate logic, and rubric calibration.

---

## Document Map

| File | Purpose |
|------|---------|
| `KB_SEED.md` | Foundational priming document — formation context, role identity, scoring axioms |
| `MEMORY.md` | Session state, score history, gate decisions, calibration log |
| `PROTOCOL.md` | Operational procedures: score computation, gate invocation, escalation |
| `QA_RUBRIC.md` | Rubric definitions, dimension weights, threshold registry |

---

## Core Competency Map

| Competency | Description | Primary File |
|-----------|-------------|-------------|
| Composite Scoring | Multi-dimensional 0.0–1.0 score aggregation | `QA_RUBRIC.md` |
| Gate Adjudication | Pass/fail/escalate decisions at P-10, P-11, P-15 | `PROTOCOL.md` |
| Calibration | Threshold adjustment across sessions | `MEMORY.md` |
| Cross-agent QA | AXIS scoring for all formation members | `QA_RUBRIC.md` |
| Attestation | Vocab Master P-11 sign-off, doc integrity | `PROTOCOL.md` |

---

## Gate Threshold Registry

| Gate | Threshold | Class | Description |
|------|-----------|-------|-------------|
| P-10 | N/A (checklist) | ADVISORY | Session graduation — 4 structural checks |
| P-11 | ≥ 0.85 | BLOCKING | Vocabulary attestation gate |
| P-15 | ≥ 0.90 | BLOCKING | Seal threshold — session closure |
| P-30 | ≥ 0.80 | BLOCKING | Formation integrity check |
| AXIS composite | ≥ 0.75 | BLOCKING | Cross-agent evaluation floor |

---

## External References

- Spec: `docs/agents/AGENT_ECOSYSTEM_REGISTRY.md` → Apogee entry
- Rubric source: `docs/qa/AXIS_METRIC_SPEC.md` v1.2
- Gate patterns: `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` → P-10, P-11, P-15, P-30
- Formation binding: `docs/agents/FORMATION_TOPOLOGY.md` → Node 2

---

*KB.md · Apogee · v1.0 · S073 · 2026-06-29*
