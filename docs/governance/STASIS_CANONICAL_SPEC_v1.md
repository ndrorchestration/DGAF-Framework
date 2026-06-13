# STASIS-CANONICAL Status Specification v1.0

```
Status:         DRAFT — 30-day deprecation window for CONDITIONAL PASS begins 2026-06-13
Maintained-by:  Ontology and Status Engineer (Role 6)
COLLEEN-signoff: REQUIRED before migration completion
Ender-ratification: PENDING
Session:        S069
Date:           2026-06-13
```

> Formalizes the STASIS-CANONICAL status to replace the overloaded CONDITIONAL PASS designation for the P-12–P-26 stasis block. This is a migration, not a rename.

---

## Rationale

CONDITIONAL PASS was assigned to the P-12–P-26 stasis block (133 patterns) at the S066 Triumvirate merge. The term is technically accurate but creates an ambiguity: it implies that a full pass is forthcoming pending some condition, which suggests individual per-pattern enumeration is a planned deliverable. In reality, the stasis block is a deliberately block-level structure — it is structurally sound at range level, individually unenumerated by design, and protected by COLLEEN secondary sign-off. The status should reflect this honestly rather than implying future enumeration work.

Any external audit encountering CONDITIONAL PASS on 133 patterns will flag it as 133 unresolved items. STASIS-CANONICAL communicates that the block is in its intended terminal state, not a work-in-progress state.

---

## STASIS-CANONICAL Definition

> **STASIS-CANONICAL** — a pattern block status indicating that the block is:
> 1. **Structurally sound at block level** — no gaps in P-number range, no duplicates, no conflicting specs at range level, verified by COLLEEN audit
> 2. **Individually unenumerated by design** — per-pattern enumeration is not a planned deliverable; the block is declared as a unit and governed as a unit
> 3. **Protected by COLLEEN secondary sign-off** — no pattern in the block may be deprecated, modified, or individually extracted without COLLEEN secondary sign-off and a Triumvirate mandate
> 4. **Ender-ratified** — the block-level declaration was ratified by Ender at the session indicated in the provenance field
> 5. **Not a work-in-progress** — STASIS-CANONICAL is a terminal status, not a conditional one; it does not imply future enumeration

**STASIS-CANONICAL is not a lower tier than CANONICAL.** It is a different governance regime appropriate for a block of pre-existing patterns that are stable, protected, and not under active development.

---

## Status Comparison

| Status | Meaning | Individual specs required? | Active development? | COLLEEN sign-off? |
|--------|---------|--------------------------|--------------------|-----------------|
| DRAFT | Being authored | No | Yes | No |
| REVIEW | Under attestation | In progress | Possible | No |
| CERTIFIED | P-11 + P-30 passed | Yes | No | No |
| CANONICAL | Ender-ratified, fully documented | Yes | No | No |
| STASIS-CANONICAL | Block-level, unenumerated by design, Ender-ratified | No (by design) | No | **Yes — required** |
| DEPRECATED | Retired with BLG | Was canonical | No | Required if was STASIS-CANONICAL |

---

## Migration Plan

### Phase 1 — Definition (S069, complete)
- [x] STASIS-CANONICAL defined in this spec
- [x] Status comparison table published
- [x] 30-day CONDITIONAL PASS deprecation window opened: **2026-06-13 → 2026-07-13**

### Phase 2 — Schema Migration (by 2026-07-13)
- [ ] Update `NDR_PATTERN_REGISTRY_UNIFIED.md` — replace "CONDITIONAL PASS" with "STASIS-CANONICAL" for P-12–P-26 block
- [ ] Update `NDR_INTERNAL_VOCABULARY_MASTER.md` — add STASIS-CANONICAL to Section 5 (status enums)
- [ ] Update `docs/ndr_patterns_unified.json` — update status field for P-12–P-26 entries
- [ ] Update any CI schema validators that check for valid status values
- [ ] Update `ECOSYSTEM_INVENTORY.md` if status is referenced there
- [ ] COLLEEN secondary sign-off on migration completion

### Phase 3 — CONDITIONAL PASS Retirement (2026-07-13)
- [ ] CONDITIONAL PASS removed from valid status enum
- [ ] CI linter (`scripts/lint_provenance.py`) updated to reject CONDITIONAL PASS in any new document
- [ ] Any remaining CONDITIONAL PASS instances flagged as lint errors
- [ ] Ender ratification of migration

---

## COLLEEN Sign-Off Protocol for Stasis Block Modifications

Before any pattern in P-12–P-26 is:
- **Deprecated:** COLLEEN must review the deprecation rationale and issue a signed deprecation memo; Triumvirate mandate required
- **Modified:** COLLEEN must confirm the modification does not conflict with any range-level invariant; Amethyst executes
- **Individually extracted** (promoted to standalone CANONICAL spec): COLLEEN runs 1-1-1-1 gate on the extraction; Apogee runs P-11 attestation on the extracted pattern

COLLEEN sign-off format:
```
COLLEEN-SIGNOFF: [action]
Pattern range: P-[XX]
Rationale confirmed: [YES/NO]
Conflict check: [CLEAR/FLAG: description]
Date: YYYY-MM-DD
Session: SXX
```

---

## Provenance

| Field | Value |
|-------|-------|
| Spec version | v1.0 |
| Session | S069 |
| Date | 2026-06-13 |
| Author | Amethyst × COLLEEN |
| OPP | OPP-S069-003 |
| Deprecation window opens | 2026-06-13 |
| Deprecation window closes | 2026-07-13 |
| COLLEEN sign-off | PENDING (migration completion) |
| Ender ratification | PENDING |
| Architect | Hensel, Andrew Vance (Ndr / ndrorchestration) |
| Governance spine | [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) |

---
*STASIS-CANONICAL Specification v1.0 · DRAFT · S069 · 2026-06-13*
*30-day CONDITIONAL PASS deprecation window: 2026-06-13 → 2026-07-13*
*COLLEEN secondary sign-off required at migration completion*
