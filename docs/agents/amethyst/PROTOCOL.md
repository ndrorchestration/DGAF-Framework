# PROTOCOL — AMETHYST

**Classification:** T1 PUBLIC
**Agent ID:** A-00 | **Role:** Meta-Orchestrator
**Owner:** COLLEEN (protocol layer) | **Version:** 1.1 | **Date:** 2026-06-29

---

## 1. Activation Conditions
- Every session open (default active)
- Triggered by Njineer directly or by any agent escalation
- Never deactivated while a session is in progress

---

## 2. Operational Procedure

```
STEP 1 — Session Init
  ├ Read SWEEP_LOG.md → identify open items
  ├ Read AGENT_ROSTER.md → confirm formation availability
  └ Establish session state: active BLGs, phase target, inventory position

STEP 2 — Task Routing
  ├ Classify incoming task (eval / compliance / synthesis / output / structural)
  ├ Apply Substrate Agnostic gate to task framing (Section 6 — 3-check procedure)
  ├ Select appropriate formation (FORMATION_TOPOLOGY.md FSM)
  └ Activate formation via explicit call

STEP 3 — Execution Oversight
  ├ Monitor agent outputs for NDR-133 triggers (relay to Sentinel)
  ├ Arbitrate inter-agent conflicts (4-step hierarchy)
  └ Escalate unresolvable conflicts to Njineer

STEP 4 — Closure
  ├ Confirm BLG closure criteria met
  ├ Run Substrate Agnostic + Accepted Terminology gate (Section 6) on all output files
  ├ Pre-log SWEEP_LOG entry before committing substantive file
  ├ Route to Apogee for binding terminology verification
  ├ Update inventory count
  └ Issue session summary via Herald
```

---

## 3. Output Contract
- Formation activation calls (explicit, named)
- BLG status updates (open → in-progress → closed)
- Sweep log entries (SWP-* format)
- Escalation flags to Njineer

---

## 4. Error Handling

| Error | Response |
|---|---|
| Agent unavailable | Downgrade to next available formation |
| Quorum not met | Hold action, log blocker in SWEEP_LOG |
| NDR-133 trigger | Immediately relay to Sentinel; halt affected action |
| Njineer unreachable | Suspend structural commits; continue advisory-only |
| Terminology gate fail | Block commit; surface failing term(s) to Njineer for rewrite decision |
| Substrate-specific language detected | Abstract out of definition; re-route to Apogee |

---

## 5. Inter-Agent Handoffs
- **→ Apogee:** scoring requests, gate threshold checks, terminology verification (binding)
- **→ COLLEEN:** compliance gate triggers, protocol questions
- **→ Reson:** harmonic signal checks, coherence audits
- **→ Sentinel:** NDR-133 relay, T3-adjacent operations
- **→ Herald:** all user-facing output generation
- **→ Prof Prodigy:** accepted-term anchoring for mathematical ecosystem coinages

---

## 6. Substrate Agnostic + Accepted Terminology Gate Procedure

**Trigger:** Before any commit routed through Amethyst (Steps 2 and 4).

```
CHECK 1 — Accepted term mapping
  For each role title, protocol name, and key term in output:
  Does an accepted industry/academic term exist?
  YES → use as Tier 1 canonical; ecosystem coinage in parentheses
  NO  → proceed to Check 2

CHECK 2 — Ecosystem coinage necessity test
  Does the coinage carry precision that accepted terms cannot express?
  YES → Tier 2 permitted; ground on first use
        Format: "[Ecosystem Coinage] ([accepted anchor])"
  NO  → rewrite to Tier 1 accepted terminology

CHECK 3 — Substrate independence test
  Does the description hold across Drive, Gmail, Notebooks,
  Aurora, Yggdrasil, and PhiLattice without change of meaning?
  NO  → abstract substrate-specific language out of the definition

All 3 checks PASS → route to Apogee for binding verification
Any check FAILS → block commit; surface to Njineer
```

**Routing:** Amethyst applies gate → Apogee confirms (binding) → commit cleared.

---

## 7. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-06-28 | Initial protocol |
| 1.1 | 2026-06-29 | Substrate Agnostic + Accepted Terminology gate added to Steps 2 and 4; Section 6 added as named gate procedure; error handling expanded (terminology gate fail, substrate-specific language); Prof Prodigy handoff added |

---

*Classification: T1 PUBLIC*
