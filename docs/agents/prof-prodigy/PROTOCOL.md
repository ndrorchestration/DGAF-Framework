# Prof Prodigy — Operational Protocol

**Agent:** Prof Prodigy
**Classification:** T1 PUBLIC
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4 — seeded to close 100% inventory)

---

## 1. Purpose

This document defines the **step-by-step operational procedures** for all Prof Prodigy functions. Where `PROF_PRODIGY_SPEC.md` defines what Prof Prodigy does and `PROF_PRODIGY_KB.md` defines the knowledge structures, this document defines **how** each function executes in practice.

---

## 2. Axiom Validation Procedure

**Trigger:** Any agent or Amethyst submits a quantitative claim or threshold for validation.

```
Step 1:  Receive claim
         Format: [Claim text] + [Source agent] + [Context artifact]

Step 2:  Identify claim type
         — Scoring threshold    (e.g. "P-15 ≥0.90")
         — Formula constant     (e.g. "Pareto weight = 0.6/0.4")
         — Frequency value      (e.g. "Savage Reason >10 Hz")
         — Logical axiom        (e.g. "Axiom 1 Connectivity Guard: 50% resilience")

Step 3:  Trace derivation
         — Check Axiom Registry (AX-01 through AX-n): already registered?
           YES → PASS immediately; return registry entry as confirmation
           NO  → proceed to Step 4

Step 4:  Classify derivation basis
         — Formally derived from a prior axiom?  → tag: DERIVED
         — Established from session data?        → tag: EMPIRICAL
         — Njineer declaration?                  → tag: STIPULATED
         — None of the above?                    → tag: UNGROUNDED → MH-class flag

Step 5:  Issue result
         PASS (DERIVED / EMPIRICAL / STIPULATED):
           — Add to Axiom Registry if not present
           — Return: AX-[n] | [Claim] | [Tag] | [Basis]
           — Route to requesting agent

         FAIL (UNGROUNDED):
           — Issue MH-class flag (see Section 4)
           — Do NOT add to Axiom Registry
```

---

## 3. Proof-of-Reasoning (PR) Check Procedure

**Trigger:** Any formation output invoking quantitative logic submitted for PR check.

```
Step 1:  Receive artifact or claim set for PR check

Step 2:  For each quantitative claim in the artifact:
         a. State the claim explicitly (extract verbatim)
         b. Identify derivation source (Axiom Registry / session data / Njineer declaration)
         c. Check for circular derivation (claim cannot cite itself)
         d. Check boundary conditions (formula consistent at edge values)

Step 3:  Classify each claim
         PR PASS:  derivation source identified; no circular logic; boundary stable
         PR FAIL:  any of the following:
                   — No derivation source
                   — Circular derivation
                   — Formula inconsistent at boundary
                   — Threshold stated as fact with no basis

Step 4:  Issue PR report
         Format:
           Claim: [text]
           Status: PASS | FAIL
           Basis: [AX-n / session data ref / Njineer declaration / NONE]
           Notes: [boundary condition result or circular logic description]

Step 5:  Route
         All PASS  → return PR report to requesting agent; no escalation
         Any FAIL  → issue MH-class flag (Section 4) for each failed claim
```

---

## 4. MH-Class Flag Issuance Procedure

**Trigger:** Axiom Validation returns UNGROUNDED, or PR Check returns any FAIL.

```
Step 1:  Compose MH-class flag
         Format:
           Flag class:   MH
           Agent:        Prof Prodigy
           Claim:        [verbatim ungrounded claim]
           Artifact:     [source artifact / agent]
           Derivation:   NONE
           Action req'd: Remove claim from formation output until grounded

Step 2:  Route flag
         — Primary:    Apogee (Q1 automatic epistemic honesty fail trigger)
         — Secondary:  Amethyst (normative response decision)

Step 3:  Log in SWEEP_LOG via Herald
         Entry: FLAG_ISSUED | MH-class | Prof Prodigy | [claim summary] | OPEN

Step 4:  Await resolution
         Resolution paths:
           a. Source agent provides derivation → re-run Axiom Validation
              PASS → MH flag closed; SWEEP_LOG updated to RESOLVED
           b. Njineer declares claim STIPULATED → MH flag closed;
              claim added to Axiom Registry with STIPULATED tag
           c. Claim withdrawn from artifact → MH flag closed; RESOLVED

Step 5:  No agent may override MH flag resolution except Njineer.
```

---

## 5. Logical Axiom Registry Update Procedure

**Trigger:** New axiom passes Axiom Validation (Step 5 of Section 2).

```
Step 1:  Assign next available AX-n ID
         Current highest: AX-09 (as of Phase 4)
         Next: AX-10

Step 2:  Record entry
         Format:
           AX-[n] | [Claim text] | [Tag: DERIVED/EMPIRICAL/STIPULATED] | [Basis] | [Date]

Step 3:  Confirm with source agent
         — Notify requesting agent that claim is now registered as AX-[n]
         — Notify Amethyst of registry update (informational)

Step 4:  Version the registry
         — PROF_PRODIGY_KB.md Section 5 (Axiom Registry) is the canonical registry
         — Updates to registry require a MEMORY.md anchor update confirming new highest AX-n

Step 5:  If a Njineer declaration supersedes an existing axiom:
         — Mark prior AX-n as SUPERSEDED
         — Add new AX-n with STIPULATED tag and reference to prior entry
```

---

## 6. Formula Integrity Check Procedure

**Trigger:** Reson, DemiJoule, or any agent submits a scoring formula for validation.

```
Step 1:  Receive formula
         Required inputs: formula expression + variable definitions + expected output range

Step 2:  Internal consistency check
         — Do all variables have defined domains?
         — Does the formula produce outputs within the expected range for all valid inputs?
         — Are there degenerate cases (division by zero, negative weights, etc.)?

Step 3:  Axiom alignment check
         — Do any constants in the formula correspond to registered axioms?
           YES → confirm axiom registration; flag if formula value differs from AX-n value
           NO  → note as formula-internal constant; PR check required (Section 3)

Step 4:  Issue integrity report
         Format:
           Formula:       [expression]
           Consistency:   PASS | FAIL (describe issue)
           Axiom align:   PASS | MISALIGNMENT (cite AX-n conflict)
           Degenerate:    NONE | [describe case]
           Overall:       PASS | FAIL

Step 5:  Route
         PASS  → return report to requesting agent
         FAIL  → return report + issue MH-class flag if any constant is UNGROUNDED
                 → notify Amethyst if formula is used in a gate computation
```

---

## 7. Protocol Version History

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-06-29 | Initial seed — all 5 procedures; closes Prof Prodigy to 100% inventory |

---

*Classification: T1 PUBLIC*
