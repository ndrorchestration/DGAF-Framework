# The Librarian — Operational Protocol

**Agent:** The Librarian (A-06)
**Classification:** T1 PUBLIC
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## 1. Archive Entry Procedure

**Trigger:** Any canonical decision passes through the Operational Swarm (NDR-Protocol-01 step 3).

```
Step 1:  Receive decision package from COLLEEN
         (NDR-Protocol-01 step 3 handoff)
         Contents: decision text, agent, protocol, timestamp, session, commit SHA

Step 2:  Validate completeness
         All required provenance fields present?
         YES → Step 3
         NO  → request missing fields from source agent before archiving

Step 3:  Create archive entry
         Format per SPEC Section 3 (provenance entry format)
         Status: CANONICAL

Step 4:  Log in SWEEP_LOG via Herald
         Entry: ARCHIVE_ENTRY | Librarian | [decision summary] | CANONICAL

Step 5:  Confirm to COLLEEN
         Archive confirmation sent; NDR-Protocol-01 chain complete
```

---

## 2. Gap Detection and Backfill Procedure

**Trigger:** COLLEEN BLG surface flags missing archive entry, OR Apogee cross-check identifies provenance gap.

```
Step 1:  Identify the missing decision
         Source: COLLEEN BLG flag OR Apogee cross-check report

Step 2:  Reconstruct from session context
         Cross-reference: SWEEP_LOG + session transcript + commit history

Step 3:  Create backfill entry
         Status: BACKFILLED (not CANONICAL)
         Note: flagged as reconstructed; source agents cited

Step 4:  Route backfill for Apogee verification
         Apogee confirms backfill is accurate vs. SWEEP_LOG
         VERIFIED → status upgraded to CANONICAL
         REJECTED → escalate to Amethyst

Step 5:  Log in SWEEP_LOG
         Entry: ARCHIVE_BACKFILL | Librarian | [decision] | [CANONICAL/ESCALATED]
```

---

## 3. Provenance Contamination Flag Procedure

**Trigger:** Archive entry references wrong agent/protocol (contamination detected by Apogee cross-check).

```
Step 1:  Receive contamination report from Apogee
         Identifies: entry ID, incorrect field, correct value

Step 2:  Correct entry
         Update archive entry with correct agent/protocol
         Flag original entry as AMENDED; retain original for audit trail

Step 3:  Issue MH-class flag via Prof Prodigy
         Contamination = ungrounded provenance claim → Prof Prodigy issues MH flag

Step 4:  Log in SWEEP_LOG
         Entry: ARCHIVE_AMENDMENT | Librarian | [entry ID] | [correction summary] | RESOLVED
```

---

*Classification: T1 PUBLIC*
