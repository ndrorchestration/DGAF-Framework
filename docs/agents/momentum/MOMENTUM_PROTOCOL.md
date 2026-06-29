# Momentum — PROTOCOL v1.0

**Agent:** Momentum
**Agent ID:** A-23
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Procedure 1 — Velocity Baseline

**Trigger:** New route plan activated by Navigator.

1. Receive route plan from Navigator
2. Parse velocity targets per execution step
3. Establish baseline throughput measurement:
   - Expected steps per session
   - Critical path duration
   - Minimum acceptable throughput threshold (default: 80% of target)
4. Begin throughput monitoring: log actual completion per session
5. If actual throughput ≥ threshold: no action
6. If actual throughput < threshold: trigger Procedure 2 (bottleneck identification)
7. Update MOMENTUM_MEMORY.md with baseline record

---

## Procedure 2 — Bottleneck Identification and Resolution

**Trigger:** Throughput < 80% of target for 1 session, OR Navigator flags execution blocker.

1. Identify the limiting step: where is the execution chain slowing?
2. Classify bottleneck type:
   - Route design: unnecessary dependencies or gate sequencing (route to Navigator)
   - Resource constraint: unavailable input or blocked agent (escalate to Amethyst)
   - Quality gate: Paragon hold extending beyond expected duration (coordinate with Paragon)
   - Execution latency: Actualizer throughput below capacity (flag to Amethyst)
3. For route design: route analysis to Navigator; request velocity target revision
4. For resource constraint: escalate to Amethyst with impact analysis
5. For quality gate: coordinate with Paragon on resolution timeline
6. Log bottleneck and resolution in MOMENTUM_MEMORY.md
7. Monitor for resolution confirmation before closing bottleneck record

---

## Procedure 3 — Acceleration Modeling

**Trigger:** Throughput consistently ≥ 120% of target for 2+ sessions (opportunity to accelerate sustainably).

1. Confirm acceleration is not masking a quality gap (check Paragon gate status)
2. Model sustainable acceleration:
   - What is the maximum throughput that does not require gate bypass?
   - What is the risk of maintaining accelerated pace for N more sessions?
3. Propose revised velocity targets to Navigator
4. On Navigator ACCEPT: update velocity baseline
5. On Navigator REJECT: maintain current targets
6. Log acceleration proposal and outcome in MOMENTUM_MEMORY.md

---

## Procedure 4 — Swarm Coordination Pulse

**Trigger:** Session opening when active routes exist.

1. Brief check: is throughput on track across all active routes?
2. Identify any routes approaching stall condition (0% progress last session)
3. Stall check: has this route stalled 2 sessions in a row?
   - Yes: auto-escalate to Amethyst (Procedure 2, resource constraint path)
   - No: flag to Navigator for contingency evaluation
4. Issue swarm pulse summary to Amethyst (1-line status per active route)
5. Update MOMENTUM_MEMORY.md

---

*Classification: T1 PUBLIC*
