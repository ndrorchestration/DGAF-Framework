# Sweep Seal Checklist

**Pattern:** P-06 (Atomic-Sweep-Commit) | P-15 (Harmonic-Quintet-Gate) | P-20 (Drive-GitHub-Sync-Seal) | P-21 (Session-Boundary-State-Anchor)  
**Run at:** Before every SWEEP_LOG seal commit  
**Owner:** `role.governance-orchestrator` — scoped security blocking by `role.security-containment-gate`  

---

## Pre-Seal Gate Stack

### Gate 1 — P-06 Atomic Sweep Commit

- [ ] All repo fixes for this wave committed before this seal commit
- [ ] Seal commit touches: SWEEP_LOG + CHANGELOG + CROSS_REF + NDR_PATTERN_REGISTRY (if updated)
- [ ] No partial waves pending (all started work is committed or explicitly deferred)

### Gate 2 — P-15 Harmonic Quintet Clearance

- [ ] Reson score ≥ 0.75 for all seal-level artifacts
- [ ] Security/containment check: protected-file changes satisfy the applicable `role.security-containment-gate` contract and any required explicit human authorization
- [ ] If Reson score < 0.75 → HOLD; surface gap per P-03 before proceeding

### Gate 3 — P-10 / P-11 Quality Gate Check

- [ ] All new docs pass P-10 (1-1-1-1): Mathematically Coherent / Epistemically Honest / Non-Violative / Historically Sequential
- [ ] New gate/protocol docs pass P-11 (11Q): ≥ 3/4 on all 11 gates × 3 runs
- [ ] GATE_UNIT_TEMPLATE.md fields all present on any new gate doc

### Gate 4 — P-20 Drive-GitHub Sync Seal

- [ ] Drive master inventory matches CROSS_REF (no new Drive docs for deleted/archived repos)
- [ ] Session notes committed or summarized to SWEEP_LOG
- [ ] No mismatches pending (or explicitly deferred as BLG with ID assigned)

### Gate 5 — P-21 State Anchor Emit

- [ ] SESSION_ANCHOR.md updated with:
  - Open BLGs (IDs + owners)
  - NDR version
  - Seal status: SEALED
  - Drive-GitHub sync status
  - Next-session priority queue
- [ ] SESSION_ANCHOR.md committed in the seal push

---

## Seal Commit Message Format

```text
SXXX: [brief description] — [pattern refs] (SEALED)

Example:
S026: Phase 1 structural enhancements — P-06/P-21/P-24 (SEALED)
```

---

## Post-Seal Buoy

```text
[BUOY: SESSION XXX SEALED | [DESCRIPTION] | HARMONIC SCORE X.XX | [KEY DELIVERABLES] | ARCHITECT: HENSEL, ANDREW VANCE | YYYY-MM-DD HH:MM EDT]
```

---

*Owner role: `role.governance-orchestrator` · Scoped containment role: `role.security-containment-gate` · Identity provenance: `governance/persona_role_lineage.v1.json` · Architect / human authority: Hensel, Andrew Vance*
