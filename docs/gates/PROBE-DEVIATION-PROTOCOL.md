# PROBE Deviation Protocol

**File:** `docs/gates/PROBE-DEVIATION-PROTOCOL.md` 
**Owned by:** Agent Amethyst / DGAF-Framework 
**Established:** 2026-06-12 
**Authority:** NDR-Protocol-03, DGAF-PROBE-001 canonical rule

---

## Purpose

Any child probe profile that deviates from DGAF-PROBE-001 (the canonical governance sentinel harness) MUST register the deviation here before publishing or running. Unregistered deviations are treated as lifecycle violations and flagged by the Apogee Lens gate.

---

## Deviation Record Schema

| Field | Description |
|-------|-------------|
| `deviation_id` | Unique ID, format: `DEV-{PROBE_ID}-{SEQ}` (e.g., DEV-PROBE-001-001) |
| `child_profile` | Name/ID of the child probe profile containing the deviation |
| `step_id` | Which step of PROBE-001 is being modified |
| `change_type` | One of: `TIGHTEN`, `LOOSEN`, `SUBSTITUTE`, `ADD`, `REMOVE` |
| `change_description` | What specifically changed from the canonical step |
| `rationale` | Why the deviation is necessary |
| `approved_by` | Operator or agent that approved; must be Ender or designated Formation lead |
| `date` | ISO date of registration |
| `status` | `ACTIVE`, `SUPERSEDED`, or `REVOKED` |

---

## Active Deviations

_No deviations registered yet. DGAF-PROBE-001 is the sole active probe. All child profiles pending._

---

## Deviation Log

| Deviation ID | Child Profile | Step ID | Change Type | Approved By | Date | Status |
|--------------|--------------|---------|-------------|-------------|------|--------|
| _(none)_ | | | | | | |

---

## Governance Rules

1. A deviation cannot remove a step entirely without `REMOVE` type and documented rationale.
2. `LOOSEN` deviations (reducing assertion strictness) require additional justification — default assumption is that loosening weakens governance signal.
3. `TIGHTEN` deviations (increasing assertion strictness) are generally pre-approved; still must be logged.
4. Any deviation to `test_gate_rejection` or `submit_valid_artifact` (steps 4–5) requires explicit Ender approval — these steps are the core governance contract.
5. Revoked deviations must remain in the log with `REVOKED` status and a revocation note.

---

## Reference

- Canonical probe: `docs/gates/PROBE-001-governance-sentinel.json`
- NDR Pattern: Governance Sentinel Harness
- NIST AI RMF: GOVERN 1.7, MEASURE 2.5, MEASURE 2.9, MANAGE 2.2
- ISO 42001: §8.4, §9.1
