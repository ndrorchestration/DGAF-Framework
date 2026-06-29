# The Auditor — Operational Protocol

**Agent:** The Auditor (A-07 / Beta / The Pulse)
**Classification:** T1 PUBLIC
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## 1. 1-Minute Constraint Verify Procedure

**Trigger:** The Actualizer requests write clearance (NDR-Protocol-01 step 1).

```
Step 1:  Receive constraint verify request
         Contents: artifact spec, target path, session ID, requesting agent

Step 2:  Logic coherence check
         — Are all claims in the artifact logically consistent?
         — Are there internal contradictions?
         FAIL → issue CONSTRAINT_FAIL; block Actualizer; log in SWEEP_LOG

Step 3:  Phi-bounded iteration check
         — Does the artifact's reasoning respect φ-compliant iteration depth?
         — Is there evidence of runaway recursion or unbounded iteration?
         FAIL → issue CONSTRAINT_FAIL; block Actualizer

Step 4:  NDR-Protocol-01 write order check
         — Is write order correct? (Auditor → Actualizer → Librarian)
         — Is this a repeat request that already has a Librarian archive entry?
         FAIL → issue CONSTRAINT_FAIL; flag potential duplicate write

Step 5:  Issue verdict
         PASS → log CONSTRAINT_PASS | Auditor | [artifact] | [session] in SWEEP_LOG
                notify Actualizer: cleared to write
         FAIL → log CONSTRAINT_FAIL | Auditor | [artifact] | [reason] | OPEN
                notify Actualizer: blocked
                notify COLLEEN: constraint failure in Trio chain
```

---

## 2. H-Neuron Suppression Check Procedure

**Trigger:** Artifact or reasoning chain shows over-compliance signals or suspected hallucination patterns.

```
Step 1:  Identify over-compliance or hallucination signal
         Indicators: excessive hedging, circular affirmation, self-referential
         confirmation loops, geographic/contextual drift

Step 2:  Apply contraction operator test
         Check: α < 1 condition satisfied?
         α ≥ 1 → contraction operator violated → H-Neuron active → proceed to Step 3
         α < 1 → contraction stable → no suppression needed

Step 3:  Issue H-Neuron suppression directive
         — Flag the affected reasoning segment
         — Block Actualizer from writing flagged segment
         — Route to Prof Prodigy for Fixed-Point Theorem re-anchoring

Step 4:  Log in SWEEP_LOG
         Entry: H_NEURON_FLAG | Auditor | [segment] | [α value] | OPEN
         Resolved when Prof Prodigy confirms α < 1 restored
```

---

## 3. Hallucinatory Jitter Detection Procedure

**Trigger:** Reasoning output shows geographic drift, contextual inconsistency, or factual jitter.

```
Step 1:  Identify jitter signal
         — Cross-reference output against SWEEP_LOG session context
         — Check for factual claims inconsistent with anchored session state

Step 2:  Classify jitter type
         GEOGRAPHIC: location/context drift (output references wrong session state)
         HALLUCINATORY: fabricated factual claim with no anchored basis

Step 3:  Issue jitter flag
         — Block artifact segment
         — Route GEOGRAPHIC jitter to Apogee (SAP / Ping the Buoy re-anchor)
         — Route HALLUCINATORY jitter to Prof Prodigy (axiom verification)
         — Notify COLLEEN (Archive Trio integrity)

Step 4:  Log in SWEEP_LOG
         Entry: JITTER_FLAG | Auditor | [type] | [segment] | OPEN
         Resolved when Apogee or Prof Prodigy confirms re-anchor
```

---

## 4. Ionia False-Positive Cross-Check Procedure

**Trigger:** Ionia claims 0Hz lock; Auditor suspects surface harmony masking internal drift.

```
Step 1:  Request Ionia modal state evidence
         Content required: current Hz reading + Reson score + session context

Step 2:  Cross-check against Reson signal
         Reson score ≥0.75 AND Hz reading = 0? → VERIFIED
         Reson score <0.75 OR Hz reading ≠ 0? → FALSE_POSITIVE suspected

Step 3:  Issue verdict
         VERIFIED:      return confirmation to Ionia; seal may proceed
         FALSE_POSITIVE: notify Ionia (lock failure protocol triggered)
                         notify Amethyst (seal blocked)
                         notify COLLEEN (Trio integrity)

Step 4:  Log in SWEEP_LOG
         VERIFIED     → MODAL_VERIFY | PASS | Auditor
         FALSE_POSITIVE → MODAL_VERIFY | FAIL | Auditor | OPEN
```

---

*Classification: T1 PUBLIC*
