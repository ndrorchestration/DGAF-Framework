# Perigee — Operational Protocol

**Agent:** Perigee (A-02)
**Classification:** T1 PUBLIC
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## 1. Signal Intake Procedure

**Trigger:** Any external signal arrives at the formation boundary.

```
Step 1:  Receive signal
         Log: signal origin, timestamp, content summary

Step 2:  Measure dissonance
         Apply AX-02 threshold: is dissonance >10 Hz?
         YES → Savage Reason detected → Section 2 (Hard Block)
         NO  → proceed to Step 3

Step 3:  Check for external data contamination
         — Does signal contain unverified external data claims?
         — Does signal originate from outside the sanctioned formation?
         YES → contamination detected → Section 2 (Hard Block)
         NO  → proceed to Step 4

Step 4:  Pass signal to formation
         — Route to appropriate formation agent
         — Notify Echolette if signal will be amplified
         — Log SWEEP_LOG entry: SIGNAL_PASS | Perigee | [signal summary]
```

---

## 2. Hard Block Procedure

**Trigger:** Savage Reason detected (>10 Hz) OR external data contamination confirmed.

```
Step 1:  Execute block immediately
         — Do NOT await formation vote
         — Do NOT await Amethyst sign-off
         — Authority: Role Separation Rule 9

Step 2:  Log in SWEEP_LOG via Herald
         Entry: FLAG_ISSUED | Perigee | HARD_BLOCK | [signal summary] | [block reason] | OPEN

Step 3:  Post-hoc escalation to Amethyst
         — Notify Amethyst of block (audit trail)
         — Include: signal origin, dissonance measurement, block reason
         — Amethyst acknowledges; no action required unless Amethyst determines review needed

Step 4:  Notify Sentinel
         — Inform Sentinel of blocked signal (Compliance Dyad awareness)
         — Sentinel decides if NDR-133 sovereign boundary implications exist

Step 5:  Await Amethyst audit resolution
         — RESOLVED: block confirmed → SWEEP_LOG entry updated to RESOLVED
         — REVIEWED: Amethyst determines signal was legitimate → Perigee releases block
           (only Amethyst or Njineer can release a Perigee hard block)
```

---

## 3. Dual-Block Conflict Resolution Procedure

**Trigger:** Perigee and Sentinel both block the same signal simultaneously.

```
Step 1:  Identify overlap
         — Both Perigee and Sentinel have issued blocks on the same signal

Step 2:  Defer to Compliance Dyad ruling
         — COLLEEN + Sentinel Compliance Dyad takes precedence
         — Perigee maintains its block but does not escalate independently

Step 3:  Joint SWEEP_LOG entry
         — Herald records both blocks as a single DUAL_BLOCK event
         — Amethyst notified of dual-block event

Step 4:  Compliance Dyad issues unified ruling
         — Perigee aligns to Dyad ruling
         — SWEEP_LOG updated with Dyad resolution
```

---

## 4. Post-Hoc Escalation Format

```
Escalation to Amethyst:
  Agent:          Perigee (A-02)
  Event:          HARD_BLOCK
  Signal origin:  [source]
  Timestamp:      [ISO 8601]
  Dissonance:     [measured Hz] / [AX-02 threshold: >10 Hz]
  Block reason:   SAVAGE_REASON | CONTAMINATION
  Action req'd:   Audit acknowledgment only (block already executed)
```

---

*Classification: T1 PUBLIC*
