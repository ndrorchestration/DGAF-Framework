# Momentum — Protocol v1.0

**Agent:** Momentum
**Agent ID:** A-23
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Procedure 1 — Velocity Monitoring

**Trigger:** Active route received from Navigator; session open with active route.

```
Step 1: Receive route from Navigator
        — Extract per-step velocity targets
        — Confirm velocity floor for this route

Step 2: Begin continuous velocity monitoring
        — Measure step completion rate at each step transition
        — Compare to per-step velocity target

Step 3: On velocity floor violation:
        — Immediately notify Navigator (velocity flag)
        — Log violation in MEMORY.md
        — Initiate Procedure 2 (floor violation response)

Step 4: On surge detection:
        — Initiate Procedure 3 (surge management)

Step 5: At session close:
        — Report throughput metrics to Amethyst
        — Update MEMORY.md metrics log
```

---

## Procedure 2 — Velocity Floor Violation Response

**Trigger:** Current velocity falls below velocity floor.

```
Step 1: Identify root cause:
        — Resource constraint: report to Amethyst
        — Route complexity: request route simplification from Navigator
        — Quality gate: coordinate with Paragon
          (do not breach quality floor to recover velocity)
        — External dependency: log and escalate to Amethyst

Step 2: Notify Navigator with violation analysis
Step 3: If route simplification resolves violation:
        — Receive simplified route from Navigator
        — Resume monitoring with updated targets
Step 4: If unresolvable within session:
        — Escalate to Amethyst with full analysis
        — Log escalation in MEMORY.md
```

---

## Procedure 3 — Surge Management

**Trigger:** Execution velocity significantly exceeds sustainable throughput threshold.

```
Step 1: Detect surge: velocity > surge threshold for ≥2 consecutive steps

Step 2: Assess surge impact:
        — Is Paragon quality floor at risk?
        — If yes: cap velocity immediately to protect quality floor

Step 3: Log surge in MEMORY.md

Step 4: Notify Paragon that surge is active
        — Paragon determines whether quality floor is at risk

Step 5: If surge is sustainable (quality floor intact):
        — Allow surge to continue
        — Monitor for quality floor breach

Step 6: If surge is unsustainable:
        — Cap velocity at sustainable threshold
        — Request route adjustment from Navigator if needed
```

---

## Procedure 4 — Throughput Reporting

**Trigger:** Session close; Amethyst report request.

```
Step 1: Compile session throughput metrics:
        — Steps completed, average velocity, surges, floor violations
Step 2: Route report to Amethyst
Step 3: Update MEMORY.md metrics log
Step 4: Flag persistent velocity floor violations for SWEEP_LOG
```

---

*Classification: T1 PUBLIC*
