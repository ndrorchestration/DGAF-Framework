# Equilibrium / Synergy Placeholder Closure — 2026-09-04

**Status:** CLOSED — resolved, not a QA_RUBRIC gap  
**Registry cross-reference:** M-001 §4.3 (cohort measurement, gap findings)  
**Source:** live filesystem scan `docs/agents/equilibrium/`, `docs/agents/synergy/` (2026-09-04)

## Finding

The Notion Master Rubric Registry's initial scan marked `equilibrium/` and `synergy/` as "TBD — folder present, layer completeness not scanned," as if they might be agent seats with a missing QA_RUBRIC layer.

## Determination

Both folders are **partial KB_SEED seeds, not agent seats**.

| Folder | Files present | Layers present | Interpretation |
|---|---|---|---|
| `docs/agents/equilibrium/` | `EQUILIBRIUM_KB_SEED.md` (1 file) | 1 of 6 (KB_SEED only) | Partial seed — not an agent seat |
| `docs/agents/synergy/` | `SYNERGY_KB_SEED.md` (1 file) | 1 of 6 (KB_SEED only) | Partial seed — not an agent seat |

Neither folder contains a SPEC, PROTOCOL, QA_RUBRIC, INTEGRATION, or MEMORY file. A single KB_SEED file does not constitute an agent seat under the six-layer standard (spec requires SPEC + KB_SEED + PROTOCOL + QA_RUBRIC + INTEGRATION + MEMORY as the standard agent inventory).

## Closure

1. **Equilibrium** and **Synergy** are not agent seats with a missing QA_RUBRIC. They are partial KB_SEED seeds that have not been built out into agent seats.
2. The registry's "TBD — folder present, layer completeness not scanned" flag for these two folders is **closed** with this determination: they are not missing a QA_RUBRIC because they are not agent seats. They are incomplete seeds.
3. The registry should record these two as **partial seeds (KB_SEED only, 1 of 6 layers)**, not as agent seats with a gap. They are out of scope for the agent-QA_RUBRIC inventory unless and until they are built out into full agent seats.
4. If and when Equilibrium or Synergy are promoted to agent seats, a QA_RUBRIC file becomes a required layer at that time, and the registry should then track it as a gap until present.

## Cross-reference

- Cohort measurement **M-001** §4.3 (gap findings) — carries this closure.
- Six-layer standard: `docs/agents/AGENT_ECOSYSTEM_REGISTRY.md` (27 agents / 162 files; standard inventory = SPEC + KB_SEED + PROTOCOL + QA_RUBRIC + INTEGRATION + MEMORY).
- Registry required fields: MASTER RUBRIC REGISTRY & AUDIT — 2026-09-04 (Notion page).

Classification: T1 PUBLIC — closure determination from live filesystem scan, not a claim of exhaustive completeness.
