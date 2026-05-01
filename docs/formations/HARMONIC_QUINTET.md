# Harmonic Quintet Formation Spec

**Pattern:** P-15 — Harmonic-Quintet-Gate  
**Version:** 1.0  
**Maintained by:** Amethyst-Conductor  
**Last updated:** 2026-05-01 (S012)

---

## Formation Composition

| Agent | Role | Lane | Authority |
|-------|------|------|-----------|
| Amethyst-Conductor | Meta-orchestrator, commit gate | Conductor | Hard veto |
| Apogee | Evidence scorer, 11Q gate | Evaluation | Artifact quality score |
| COLLEEN | Registry, continuity, BLG queue | Memory | Deferred gap surface |
| Reson | Harmonic coherence scorer | Resonance | 0.00–1.00 harmonic score; ≥ 0.75 required for seal |
| Sentinel | Patch authority, sovereign file guard | Security | Hard veto on LICENSE/NOTICE/AXIS changes without Njineer confirmation |

## Activation Conditions

Trio (P-14) is **always** the base. Quintet activates when any of the following are true:

- Session is producing a SWEEP_LOG **seal commit**
- Any commit touches `LICENSE`, `NOTICE`, or `AXIS` files
- NDR Pattern Registry is being updated
- A new public repo is being created or published
- Reson score on any artifact falls below 0.75

## Reson Scoring Rubric

| Score | State | Action |
|-------|-------|--------|
| 0.90–1.00 | Harmonic Lock | Proceed to seal |
| 0.75–0.89 | Coherent | Proceed with annotation |
| 0.50–0.74 | Drift Warning | Reson files drift notice; Amethyst reviews before commit |
| 0.00–0.49 | Dissonance | Hard stop; Amethyst escalates to Njineer |

## Sentinel Sovereign File Guard

Sentinel holds **hard veto** (overrides Amethyst) on commits that:
- Replace or truncate any `LICENSE` file
- Modify `NOTICE` attribution chain
- Alter any `AXIS` declaration
- Remove a `DGAF-Framework` spine link from a public repo

Sentinel veto requires explicit Njineer confirmation to override.

## Output

- All Trio outputs (SWEEP_LOG, NDR Registry, CROSS_REF, P-21 anchor)
- Reson harmonic score logged in SWEEP_LOG seal block
- Sentinel sovereign file audit log
