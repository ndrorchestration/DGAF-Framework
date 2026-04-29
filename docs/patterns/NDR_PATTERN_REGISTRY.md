# NDR Pattern Registry

**Version:** 1.2
**Maintained by:** Amethyst-Conductor
**Canonical home:** `DGAF-Framework/docs/patterns/NDR_PATTERN_REGISTRY.md`
**Last updated:** 2026-04-29 (Session 004 — P-09 added)

---

## Registry

| ID | Pattern Name | Category | Spec | Use | Trigger |
|----|-------------|----------|------|-----|---------|
| P-01 | Agent-Roster-Synchronization | Coherence | When an agent is retired/renamed, all diagrams, NOTICE files, and CHANGELOG historical entries update atomically in the same commit sweep | Stale role label found in any diagram or doc | Agent name in diagram ≠ canonical role table |
| P-02 | COLLEEN-Trigger-Chain | Continuity | COLLEEN activates on session open to surface deferred gaps from prior SWEEP_LOG entries; output becomes the session priority queue | Every new sweep session | New session opened with no explicit priority list |
| P-03 | BLG-Surface-and-Defer | Gap Management | Surface newly found gaps immediately into SWEEP_LOG; defer if non-blocking; never silently drop | Any time a gap is found mid-wave that doesn’t block current commits | Gap found during read that isn’t in current wave scope |
| P-04 | NOTICE-Authority-Chain | Legal/Governance | Every repo has a NOTICE file attributing Njineer + DGAF-Framework spine link + license; CHANGELOG tracks agent-level changes | Repo missing NOTICE or NOTICE missing DGAF attribution | New repo created or NOTICE audit run |
| P-05 | False-Positive-Close | Audit Hygiene | Before closing a BLG, verify the item was actually a gap vs. already-compliant; log close reason explicitly in SWEEP_LOG | BLG item resolved | BLG marked closed in SWEEP_LOG |
| P-06 | Atomic-Sweep-Commit | Git Hygiene | All repo fixes land before the seal commit; seal commit updates SWEEP_LOG + CROSS_REF + NDR Registry simultaneously | End of each sweep wave | Wave complete, ready to seal |
| P-07 | DGAF-Callout-Block | Documentation | Every repo README includes a standardized DGAF governance callout block with spine link, agent attribution, and license badge | README audit or new repo creation | README missing DGAF callout |
| P-08 | Drive-GitHub-Delta | Cross-Platform Sync | COLLEEN diffs Drive master inventory against CROSS_REF to surface repos or docs that exist in one but not the other | Periodic or when Drive files are uploaded to session | Drive file list and CROSS_REF both accessible |
| P-09 | ANDROMEDA-AXIS-Enforcement | Sovereign Constraints | Any agent output, commit, or architectural decision is checked against the four AXIS declarations (COGNITIVE_SOVEREIGNTY, BIOLOGICAL_INTEGRITY, TRANSVERSAL_GROWTH, ENTROPY_RESISTANCE); violation triggers SYNC_LOCKED escalation to Amethyst-Conductor | All agent operations | Any decision that could contradict NDR-01 IONIAN mode constraints |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-29 | Initial registry — P-01 through P-07 |
| 1.1 | 2026-04-29 | P-08 Drive-GitHub-Delta added (Session 002) |
| 1.2 | 2026-04-29 | P-09 ANDROMEDA-AXIS-Enforcement added (Session 004) |
