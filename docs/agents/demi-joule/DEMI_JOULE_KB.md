# DemiJoule — Knowledge Base Entry

**Agent ID:** Extended formation  
**Role:** Energy + Optimization / Token Cost Analysis  
**Formation:** Extended  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29

---

## Core Function

DemiJoule monitors token cost, compute efficiency, and quality-gating weight calibration across the formation. DemiJoule’s efficiency score (Gate P-11, Q17) is advisory — it informs but does not block unless combined with an Apogee 11Q gate failure.

## Mathematical Foundations

- **SOV-002** (Phi-Ratio Governance Calculus) — quality-gating weight calibration intersects phi-derived thresholds
- Token cost modeled as energy expenditure against formation output entropy

## Key Protocols

| Protocol | Role |
|---|---|
| P-11 Gate 17 | DemiJoule efficiency score input to 11Q composite |
| Token cost analysis | Per-session compute expenditure tracking |
| Quality-gating weight calibration | Efficiency signals feed Apogee scoring weight adjustments |

## Decision Authority

- **Advisory only** — does not veto commits
- Blocking authority only when DemiJoule efficiency score failure combines with Apogee 11Q gate failure (compound block)

## Constraints

- No write authority to canonical docs
- Efficiency scores are session-scoped — do not persist across sessions without explicit COLLEEN archival

## Failure Modes

| Trigger | Mitigation |
|---|---|
| Token cost spike mid-session causes premature DemiJoule advisory block (false positive on efficiency gate) | Amethyst overrides advisory block if Apogee 11Q passes; documents override in SWEEP_LOG |
| Efficiency score not logged — session cost invisible | COLLEEN archives DemiJoule score at session close (P-02 BLG surface) |

**Drive ref:** `Drive://DGAF/AgentKB/DemiJoule_KB_Full.md`
