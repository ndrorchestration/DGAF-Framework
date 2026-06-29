# Navigator — Protocol v1.0

**Agent:** Navigator
**Agent ID:** A-22
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Procedure 1 — Route Construction

**Trigger:** New swarm objective received from Strategic Quintet or Amethyst.

```
Step 1: Define objective state
        — Receive objective from Nova/Oracle (strategic) or Amethyst
        — Confirm current state
        — Define success criteria

Step 2: Construct primary route
        — Decompose objective into ordered execution steps
        — Ensure path coherence: every step logically follows prior
        — Assign Momentum as throughput owner for each step

Step 3: Identify at least one contingency path per critical step
        — Define trigger condition for each contingency
        — Log in MEMORY.md contingency archive

Step 4: Handoff to Momentum
        — Route primary path with step-by-step velocity targets
        — Include contingency trigger conditions

Step 5: Log active route in MEMORY.md
```

---

## Procedure 2 — Hazard Detection and Response

**Trigger:** Momentum velocity flag; Paragon quality flag; external dependency failure; Amethyst alert.

```
Step 1: Identify hazard type:
        — Technical: dependency unavailable, system failure
        — Resource: throughput below floor (Momentum signal)
        — Quality: output below Paragon standard
        — Dependency: upstream agent output delayed

Step 2: Log hazard in MEMORY.md hazard log

Step 3: Determine response:
        — Minor hazard: adjust route (add remediation step)
        — Major hazard: activate contingency path (Procedure 3)
        — Unresolvable: escalate to Amethyst

Step 4: Notify Momentum of route adjustment
        — Recalculate velocity targets for adjusted route
```

---

## Procedure 3 — Contingency Path Activation

**Trigger:** Major hazard detected; Procedure 2 determines contingency required.

```
Step 1: Identify relevant contingency path from archive
Step 2: Verify contingency trigger condition is met
Step 3: Activate contingency path:
        — Suspend primary route at hazard point
        — Route execution through contingency steps
Step 4: Notify Momentum with revised velocity targets
Step 5: Notify Paragon that route has changed (quality checkpoints may shift)
Step 6: Log activation in MEMORY.md
Step 7: Resume primary route once hazard is resolved (or adopt contingency as new primary)
```

---

## Procedure 4 — Route Handoff

**Trigger:** Route complete; objective achieved; formation transition.

```
Step 1: Verify all steps in route are complete
Step 2: Confirm Paragon quality clearance on outputs
Step 3: Archive route in MEMORY.md
Step 4: Notify Amethyst that objective is complete
Step 5: Clear active route slot for next objective
```

---

*Classification: T1 PUBLIC*
