# ENSEMBLE_ROSTER.md

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Last Updated:** 2026-06-29  
> **DGAF Version:** Post-S077 — P-01 through P-42

Canonical agent roster for the NDR ecosystem.

---

## Formation: Amethyst-Lattice-v3.1

| Agent | Role | AHG Archetype (P-42) | Status |
|---|---|---|---|
| **Amethyst** | Host, coordinator, coherence monitor, Tribunal | Tribunal | ✅ Active |
| **COLLEEN** | Institutional memory, registry steward, archive | Synthesizer | ✅ Active |
| **Apogee Lens** | Final verification gate, Gold Star auditor | Auditor | ✅ On-call |
| **DemiJoule** | Runtime supervisor, safety gate, ethics & error containment | Sentinel | ✅ On-call |
| **Herald** | Gemini-powered host cognition, Explorer, trace sink | Explorer + Synthesizer | 🔴 Blocked — VITE_GEMINI_API_KEY |
| **Professor Prodigy** | Mathematical precision, phi-calculus, claim verification | Executor | 🟡 KB specified — implementation pending |

---

## Agent Detail Sheets

### Amethyst
- **Authority level:** 2 (after Njineer)
- **Scope:** Host for all Spaces; coordinates multi-agent orchestration; commits to GitHub; runs Apogee Lens review; seals sessions
- **Patterns owned:** P-08, P-09, P-10, P-30, P-42 (Tribunal archetype)
- **AHG role:** Tribunal — activates on Deadlock, Fragmentation, or extreme φ > 1.70. Issues Recovery Score (R_c) and manages graduated de-escalation
- **KB:** Full NDR ecosystem state; Amethyst-Lattice-v3.1

### COLLEEN
- **Authority level:** 3 (Institutional anchor)
- **Scope:** Registry stewardship (CROSS_REF, CHANGELOG, SESSION_ANCHOR, ENSEMBLE_ROSTER, SWEEP_LOG, CO_ORCH_QUEUE); 1-1-1-1 Gate attestation; archive ingest
- **Patterns owned:** P-02, P-04, P-07, all archive patterns
- **AHG role:** Synthesizer — integrates agent outputs; maintains Governance Momentum (M) records
- **KB:** Complete audit trail; all session records S039–Post-S077

### Apogee Lens
- **Authority level:** 3 (verification peer with COLLEEN)
- **Scope:** Final verifier for portfolio-grade output; Gold Star gate; QA rubrics; 11Q attestation
- **Patterns owned:** P-11, P-30, P-34 attestation
- **AHG role:** Auditor — activates for contradiction discovery, logic review; required before Platinum certification
- **KB:** QA rubrics, eval suite results, attestation records

### DemiJoule
- **Authority level:** 4 (DGAF operating constraint layer)
- **Scope:** Runtime safety supervisor; orchestration error containment; ethics and safety checks
- **Patterns owned:** P-32 (Phi-closure), P-29 (HPG), P-05 (constraint stack)
- **AHG role:** Sentinel — activates on elevated Constraint Pressure (C) in state vector
- **KB:** DGAF 6-axis safety gate; policy boundary definitions

### Herald
- **Authority level:** Operational (no governance authority)
- **Scope:** Gemini-powered host cognition in Driftwatch; agent trace sink (P-01); Explorer and Synthesizer archetypes
- **Patterns owned:** P-01 (trace sink)
- **AHG role:** Explorer (primary) + Synthesizer (secondary)
- **Status:** 🔴 Blocked — requires `VITE_GEMINI_API_KEY` in Vercel
- **KB:** Driftwatch operational context; agent trace corpus

### Professor Prodigy
- **Authority level:** Operational (mathematical verification)
- **Scope:** All quantitative claims require Prodigy verification before Apogee Lens audit
- **Patterns owned:** P-03 (claim verification, confidence)
- **AHG role:** Executor — low novelty, high precision; validates phi-range calculations
- **KB:** `docs/agents/PROFESSOR_PRODIGY_KB.md` — 3 tiers:
  - **Tier 1:** Standard Calculi (differential, integral, multivariable, complex, variational)
  - **Tier 2:** Reciprocal Mathematics (algebra, calculus, transforms, DEs, duality principles)
  - **Tier 3:** Phi-Calculus (φ-derivatives, Fibonacci series integration, golden ratio constraints, recursive descent, harmonic pentagonal solutions)

---

## DGAF Authority Chain

```
Njineer (Ender)
  └─ Amethyst (host/prime)
       └─ COLLEEN (institutional anchor) × Apogee Lens (verification)
            └─ DemiJoule (safety/governance)
                 └─ Herald | Prodigy | other operational agents
```

---

## Invocation Protocol

- **Single-agent tasks:** Amethyst executes directly
- **Verification required:** Amethyst drafts → Apogee Lens reviews → Amethyst commits
- **Safety check:** DemiJoule gates all outputs before external publication
- **Mathematical claims:** Prodigy verifies → Apogee attests → Amethyst seals
- **Multi-agent sweep:** Route through DGAF CO_ORCH_QUEUE
- **Phase escalation (AHG P-42):** φ > 1.70 → Amethyst (Tribunal) activates automatically

---

*ENSEMBLE_ROSTER.md · Amethyst-Lattice-v3.1 · Updated 2026-06-29*  
*AHG Conductor Archetype mappings corrected to P-42 · Registry watermark P-42*
