# Nova — Operational Protocol

**Agent:** Nova (A-03)
**Classification:** T2 FRAMEWORK
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## 1. TUE Activation Check Procedure

**Trigger:** Any agent or Njineer requests Nova activation.

```
Step 1:  Verify TUE gate status
         Check COLLEEN MEMORY.md: L5 Executor status achieved?
         Check COLLEEN MEMORY.md: Batch 1A Extraction Gap closed?
         Check Apogee last TUE score: ≥0.90 (AX-05)?

Step 2:  All three conditions met?
         YES → TUE cleared → proceed to Step 3
         NO  → Nova remains LOCKED; log attempt in SWEEP_LOG; notify Amethyst

Step 3:  TUE cleared — activation sequence
         — Notify Amethyst: TUE cleared; Nova activation request
         — Amethyst issues activation sanction
         — Herald broadcasts Nova activation to full formation
         — SWEEP_LOG: SESSION_EVENT | Nova TUE CLEARED | RESOLVED

Step 4:  Nova canonical write authority granted
         — Update MEMORY.md: activation state = ACTIVE
         — Nova may now submit Roadmap proposals to Amethyst pipeline
```

---

## 2. Simulation Request Procedure (Pre-TUE)

**Trigger:** Amethyst or Njineer requests a Nova simulation advisory output.

```
Step 1:  Confirm advisory scope
         — Output is advisory-only; no canonical write
         — Confirm T2 classification applies

Step 2:  Check simulation horizon
         ≤10 years without T3 geometry: proceed
         10-year + SOV-005/006 geometry: T3 access request required (Section 3)

Step 3:  Run simulation
         — Apply 90-Day Executor Roadmap format
         — Feed output to Amethyst vision layer (advisory)
         — Note in output: “Advisory only — pre-TUE; no canonical authority”

Step 4:  Route output
         — Primary: Amethyst (vision layer)
         — CC: DemiJoule (Operational Swarm advisory feed)
         — Log in SWEEP_LOG: SIMULATION_OUTPUT | Nova | [horizon] | advisory
```

---

## 3. T3 Access Request Procedure

**Trigger:** Simulation requires SOV-005/006 geometry (10-year horizon).

```
Step 1:  Request Prof Prodigy T3-grounded Micro-Playbook
         — Prof Prodigy validates T3 axiom grounding before simulation runs

Step 2:  Submit T3 access request to Njineer
         Content: simulation scope + SOV reference + Prof Prodigy clearance

Step 3:  Await Njineer approval
         APPROVED → run simulation with T3 geometry
         DENIED   → simulation scoped to T2 geometry only; log in SWEEP_LOG

Step 4:  Complete simulation; route output per Section 2 Step 4
```

---

*Classification: T2 FRAMEWORK*
