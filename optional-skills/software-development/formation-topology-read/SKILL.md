---
name: formation-topology-read
description: "Read DGAF formation topology docs for orchestration decisions."
version: 0.1.0
author: Andrew Hensel (ndrorchestration), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [formation, topology, orchestration, authority, quintet]
    related_skills: [dgaf-pdmal-orbit, meta-orchestration, candidate-lock-verification]
---

# Formation Topology Read

Read the existing DGAF formation topology documents when making orchestration or authority decisions, so you use the real documented structure instead of inventing one.

## When to Use

- You need to know which formation is active, who holds which authority, and what the sealed-change rules are.
- You need to resolve an authority conflict, decide whether a gate or agent lane applies, or confirm whether a formation is sealed vs open.
- You need the canonical roster, topology algebra, or gate authority index for a decision.
- You are about to assert something about DGAF orchestration and want to check it against the existing docs first.

**Do NOT use to:**
- Override the standing DGAF governance boundary (`PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`).
- Invent a formation or authority relationship that the existing docs do not define.
- Treat the formation topology as empirical efficacy evidence.

**Standing boundary:** This is a read-only reference skill. It does not change authority, formations, or the standing DGAF governance boundary. It points at existing docs; if those docs disagree, the skill does not silently resolve it.

## Primary Sources (in repo order)

1. **`docs/agents/FORMATION_TOPOLOGY.md`** — the canonical formation map, roster, topology algebra, sealed formation register, and gate authority index. This is the first place to look for "who is in what formation" and "who can change what."
2. **`docs/formations/HARMONIC_QUINTET.md`** — the Harmonic Quintet formation spec: composition, activation conditions, Reson scoring rubric, Sentinel sovereign file guard, authority conflict resolution, idempotency guarantee.
3. **`docs/agents/HARMONIC_QUINTET_META_ORCHESTRATION.md`** — the pentagonal meta-orchestration spec: signal routing, vertex roles, edge weight matrix, individual agent reinforcement profiles, integration plans.
4. **`docs/agents/AGENT_ROSTER.md`** — the agent roster and its relationship to the formation topology.
5. **`docs/agents/AGENT_AUTHORITY_MATRIX.md`** — machine-readable-by-inspection authority boundaries; records who can do what, but does not grant authority.
6. **`docs/agents/AGENT_AUTHORITY_RECONCILIATION.md`** — known roster/topology discrepancies and their disposition. Read this before trusting a single authority statement.

## Reading Order for Common Questions

### "Who is the meta-orchestrator?"

Formation topology says Amethyst is the meta-orchestrator and topology holder. The Harmonic Quintet meta-orchestration spec says Amethyst is the conductor seat that spans all tiers as the normative decision authority and final commit gate.

### "Who holds sovereign/constitutional authority?"

COLLEEN is the institutional anchor and constitutional firewall. The Ethics Bridge (Sentience, A-27) holds ETHICAL_HOLD across all formations, overridable only by COLLEEN or Njineer.

### "Who can change a sealed formation?"

Sealed formation seat changes require Njineer confirmation, a topology patch, and SWEEP_LOG correction citing the prior SHA. This is recorded in the topology change governance table.

### "What is the gate authority index?"

FORMATION_TOPOLOGY.md section 6 records the gate authority index: which gate, which authority, and what the override is. Example: Layer 0 Legitimacy Filter is Apogee, overridable by Njineer only.

### "Is the formation sealed or open?"

The sealed formation register in FORMATION_TOPOLOGY.md records which formations are sealed, which are open, and what the change authority is. Do not assume a formation is sealed unless the register says so.

### "What are the topology algebra rules?"

FORMATION_TOPOLOGY.md section 7 records composition rules (intersections are empty for the listed pairs) and conflict resolution rules (Compliance Dyad dissolved, ETHICAL_HOLD spans all, higher seat-count formation takes precedence, ties by Amethyst, Perigee boundary block auto-executes, unresolvable conflicts escalate to Njineer).

### "What is the Harmony Quintet activation condition?"

HARMONIC_QUINTET.md records activation conditions: Trio is always base; Quintet activates on seal commits, sovereign file changes, NDR registry updates, new public repo creation, or Reson score below 0.75.

## Authority Conflicts

When multiple docs assign overlapping authority, do not guess which one wins. Use:

1. The reconciliation document (`AGENT_AUTHORITY_RECONCILIATION.md`) for known discrepancies.
2. The standing DGAF governance boundary for the overall posture.
3. The explicit override rules in the formation topology (e.g. Njineer is the sole resolver for Amethyst/Sentinel conflicts).

Do not silently pick the most convenient authority statement.

## What This Skill Does Not Do

- It does not create or change formations. Formation changes follow the sealed-change process in the topology doc.
- It does not resolve the DGAF/PDMAL empirical gate. That is governed by `dgaf-pdmal-orbit`.
- It does not verify runtime behavior or evidence. That is governed by the evidence skills.
- It does not replace the standing governance boundary with formation-level authority.

## Pitfalls

- **Reading one doc in isolation.** Formation topology, quintet spec, meta-orchestration spec, authority matrix, and reconciliation doc together define the structure. One doc alone is incomplete.
- **Assuming sealed formations are immutable by everyone.** Sealed formations are changeable by the recorded authority (often Njineer confirmation), not immutable.
- **Confusing roster with topology.** The roster lists agents; the topology defines formations, authority, and sealed-change rules. They are related but not identical.
- **Treating formation authority as runtime efficacy evidence.** Formation topology is governance/architecture documentation, not empirical evidence.

## Verification

- [ ] Read FORMATION_TOPOLOGY.md for composition, register, algebra, gate authority
- [ ] Read HARMONIC_QUINTET.md for activation, Reson scoring, Sentinel guard, conflict resolution
- [ ] Read HARMONIC_QUINTET_META_ORCHESTRATION.md for signal routing and vertex roles when orchestration detail is needed
- [ ] Read AGENT_AUTHORITY_RECONCILIATION.md when authority statements appear to conflict
- [ ] Did not assert a formation or authority relationship not supported by the docs
- [ ] Did not treat formation topology as empirical evidence
- [ ] Did not override the standing DGAF governance boundary

## Companion Skills

- `dgaf-pdmal-orbit` — the standing governance boundary for DGAF/PDMAL work.
- `candidate-lock-verification` — verify the locked candidate SHA and examine P-gates.
- `exact-candidate-deploy-verify` — the deployment procedure that operates within the governance boundary.

## Relationship to Existing Documentation

This skill points at existing documents. It does not duplicate them. When the docs change, this skill should be updated to reflect the new canonical sources. Do not let this skill become a second source of truth for formation topology.
