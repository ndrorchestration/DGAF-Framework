# Candidate Dependency Graph — 2026-08-30

**Current apparatus/source candidate:** `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`
**Designation/control commit:** `02c146d1e0cdc423948ac0dfa11e98f812edfb44`
**Current main documentation lineage:** `c7288f88655851e273f46ebf52db789791fcaa76`
**Prior runtime evidence source:** `303f4424d2198f0d0cf76305c589263dd1e417dc`
**Prior pre-remediation candidate:** `c6157158bf0ee4840e99a381a4b99bd2febe2302`

## Directed dependencies

`05fa286 apparatus`
→ candidate designation `02c146d`
→ exact deployment identity
→ P2/P6a current-candidate runtime evidence
→ P3 artifact execution evidence
→ P4 custody/blinding evidence
→ P5 provenance/reproducibility evidence
→ P6 durable custody
→ P7 exact scientific binding
→ P8 analysis lock
→ independent P9
→ new immutable freeze
→ explicit authorization
→ pilot

Historical P2/P6a evidence at `303f4424` is an upstream historical evidence node only; it cannot satisfy current-candidate P2/P6a.

## Change propagation rule

Any substantive change to apparatus, protocol, runner, analysis, artifact schema, security/custody, retention, or executable governance creates a new candidate cycle and invalidates affected downstream candidate-scoped evidence.

Documentation-only changes update control lineage but do not change apparatus identity.

## Non-equivalence

- apparatus SHA != designation/control commit
- apparatus SHA != documentation lineage
- workflow head SHA != apparatus identity
- deployment READY != runtime verification
- implementation != wiring
- candidate-bound != verified
- verified != frozen
- frozen != authorized
- historical evidence != current evidence

## Current state

P2/P6a: prior verified only; current candidate open.
P3–P8: evidence-gated.
P9: not executed for current candidate.
Freeze: not created.
Authorization: not granted.
Empirical N: 0.

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0**
