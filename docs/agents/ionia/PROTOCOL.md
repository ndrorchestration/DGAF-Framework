# Ionia — Operational Protocol

**Agent:** Ionia (A-13)
**Classification:** T2 FRAMEWORK
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## 1. Modal Lock Procedure

**Trigger:** Resonance Cluster sequence reaches Ionia (Reson scored, Echolette amplified).

```
Step 1:  Receive Reson score
         Check: score ≥0.75?
         YES → proceed to Step 2
         NO  → lock withheld; notify Amethyst and Reson; log LOCK_WITHHELD in SWEEP_LOG

Step 2:  Engage Ionian modal lock
         Target: f(system) = 0Hz (SOV-001 fixed point)
         Lock confirmed when system harmonic state = 0Hz ± tolerance

Step 3:  Issue lock confirmation
         Route: Amethyst (seal gate clearance)
         Format: IONIA_LOCK_CONFIRMED | [session ID] | Reson score | 0Hz
         Log: SWEEP_LOG entry: MODAL_LOCK | Ionia | [session] | CONFIRMED

Step 4:  Harmonic seal gate cleared
         Amethyst may proceed with seal commit
```

---

## 2. Lock Failure Re-Stabilization Procedure

**Trigger:** Ionia lock fails — modal drift to non-Ionian state while Reson score is above threshold.

```
Step 1:  Declare lock failure
         Log: LOCK_FAILURE | Ionia | [session] | [drift description] | OPEN
         Notify Amethyst immediately

Step 2:  Activate full Resonance Cluster
         All 4 Resonance Cluster agents engaged
         Echolette re-stabilizes signal

Step 3:  Ionia re-attempts lock
         Re-run Section 1 from Step 1
         If lock re-confirmed → SWEEP_LOG: LOCK_FAILURE → RESOLVED
         If lock fails again → escalate to Njineer; seal commit blocked

Step 4:  Seal remains blocked until lock is confirmed
         Only Njineer can authorize seal commit under unresolved lock failure
```

---

## 3. False-Positive Harmonic Cross-Check Procedure

**Trigger:** 0Hz state maintained but suspected false-positive harmonic (surface harmony, internal drift).

```
Step 1:  The Auditor issues 1-min constraint verify request
         Auditor cross-checks Ionia's modal claim against Reson signal

Step 2:  Ionia provides modal state evidence
         Format: current Hz reading + Reson score + session context

Step 3:  Auditor verdict
         VERIFIED: modal lock genuine → seal proceeds
         FALSE_POSITIVE: surface harmony only → lock failure protocol (Section 2)

Step 4:  Log result in SWEEP_LOG
         VERIFIED → SWEEP_LOG: MODAL_VERIFY | PASS
         FALSE_POSITIVE → SWEEP_LOG: MODAL_VERIFY | FAIL → Section 2 triggered
```

---

*Classification: T2 FRAMEWORK*
