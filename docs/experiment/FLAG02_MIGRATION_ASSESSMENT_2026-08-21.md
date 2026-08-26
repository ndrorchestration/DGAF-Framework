# FLAG-02 Migration Assessment

**Established:** 2026-08-21  
**Status:** ASSESSMENT — MIGRATION NOT YET DONE  
**Step:** 8 of 28 (Gate 3: Engineering and Evidence Closure)

---

## What FLAG-02 Is

FLAG-02 refers to a qualified-claim flag in the DGAF/PDMAL governance system. A "qualified claim" is a claim that is explicitly scoped, verified, and attributed — as opposed to an unqualified assertion that anyone can make without evidence.

The FLAG-02 mechanism exists to mark certain claims as "qualified" — meaning they carry explicit evidence, scope, attribution, and expiration semantics. This is part of the broader governance architecture that distinguishes "this claim has been verified" from "this claim is being asserted."

---

## Why Migration Matters

The control needs to be represented consistently throughout the system so that:

1. **An old representation cannot bypass the new governance semantics.** If FLAG-02 is defined in one way in the protocol but interpreted differently in the runner, artifacts, or analysis, the governance semantics are subtly broken.

2. **All components agree on what "qualified" means.** The runner, the artifact schema, the analysis pipeline, and the evidence graph should all use the same definition of what constitutes a qualified claim.

3. **The evidence chain is consistent.** A reviewer tracing a claim backward should find the same FLAG-02 semantics at every link.

---

## Current State

From the available source files, FLAG-02 is referenced in:

- **`PDMAL_CURRENT_CONTROL_STATE.md`** — mentions FLAG-02 in the gate board context
- **`FREEZE_MANIFEST.md`** — references governance controls including FLAG-02
- **`PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md`** — may define FLAG-02 semantics

However, the exact current representation of FLAG-02 and whether it needs migration is not fully documented in the available source files. The sprint fragment (sections 10.5-13) mentions FLAG-02 migration as a recommended action but does not detail what the migration entails.

---

## Migration Path (Proposed)

The migration should:

1. **Define the canonical representation.** What exactly does FLAG-02 mean? What are its fields? What qualifies a claim as FLAG-02?
2. **Audit all usages.** Where is FLAG-02 currently referenced? In code, documentation, configuration?
3. **Migrate each usage.** Update each reference to use the new canonical representation.
4. **Verify consistency.** After migration, verify that all components agree on the semantics.

---

## Is This Cosmetic or Substantive?

The migration is **potentially substantive** depending on what the current vs. new representations are:

- **If cosmetic:** The change is only in naming or formatting — the semantics are the same. Migration is low-risk but should still be done for consistency.
- **If substantive:** The change alters what counts as a qualified claim — this affects the governance semantics and must be carefully audited.

Without a detailed specification of the current and target representations, the assessment cannot determine which case applies.

---

## Gap

PR #77 does NOT address FLAG-02 migration. The `PDMAL_ANALYSIS_CONTROL_PLAN.md` at PR #77 does not mention FLAG-02. The catalog of what needs migrating and what the target representation is does not exist in the available source files.

This assessment identifies that FLAG-02 migration is a required step (per the sprint fragment and the 28-step path) but cannot complete the migration without:

1. A specification of the current FLAG-02 representation
2. A specification of the target FLAG-02 representation
3. An inventory of all current FLAG-02 usages

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This assessment identifies a gap but does NOT close it. No migration has been performed.
