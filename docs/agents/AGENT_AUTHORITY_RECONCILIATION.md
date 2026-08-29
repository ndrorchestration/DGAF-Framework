# DGAF Agent Authority Reconciliation

**Invariant:** DGAF-AUTH-001  
**Status:** ACTIVE — RECONCILIATION RECORD  
**Version:** 1.0.0  
**Purpose:** Record cross-source authority discrepancies discovered while adopting the authority-separation invariant. This document does not supersede guarded canonical sources.

## 1. Current Source Hierarchy

1. `AGENT_ROSTER.md` — sovereign SSoT for current named operational-layer role assignments; guarded and requires Amethyst sign-off + Njineer confirmation for changes.
2. `FORMATION_TOPOLOGY.md` — canonical formation composition, topology, activation, and sealed formation changes.
3. `AGENT_ECOSYSTEM_REGISTRY.md` — ecosystem metadata and amendment history.
4. Individual agent SPEC / KB / PROTOCOL / INTEGRATION artifacts — domain-specific contracts.
5. `AGENT_AUTHORITY_MATRIX.md` — descriptive derivative; never grants authority.
6. `AGENT_AUTHORITY_INVARIANT.md` — constitutional rule for authority separation.

## 2. Confirmed Reconciliation Findings

### R-001 — Roster/topology generation mismatch

`AGENT_ROSTER.md` still presents the older A-00 through A-13 operational roster and identifies Sentinel in a legacy formation arrangement, while `FORMATION_TOPOLOGY.md` records the later 27-agent taxonomy, Sentinel-Phi strategic seat, Ethics Bridge, Harmonic Pentagonal Cluster, Resonance extensions, and dissolved Compliance Dyad.

**Disposition:** Do not silently overwrite the guarded roster. Require formal topology/roster reconciliation under the sealed-change process.

### R-002 — Layer-0 attribution is distributed

The current documentation assigns Layer-0 responsibilities in more than one place: the roster names Perigee as Layer-0 Legitimacy Filter; the topology identifies Apogee as the Layer-0 gate and Sentience as ETHICAL_HOLD; the authority invariant intentionally defines Layer 0 as a shared constitutional substrate.

**Disposition:** Preserve specialist gate ownership while treating Layer 0 as cross-cutting constitutional constraints. Do not create a single "ethics agent" abstraction that erases existing gate contracts.

### R-003 — Sentinel / Sentinel-Phi identity continuity

`FORMATION_TOPOLOGY.md` identifies Sentinel-Phi (A-12-φ) as the strategic security seat, while older individual `sentinel/SPEC.md` material uses Sentinel and legacy formation language. The repository's amendment history records the Sentinel-Phi transition.

**Disposition:** Treat naming continuity and authority continuity as separate fields. Formalize lineage without collapsing the contracts until reconciled.

### R-004 — ID / formation drift

Older agent IDs and newer formation-specific IDs coexist (for example A-03-DJ, A-06-R, A-09-Z, A-12-φ, A-00-GOV). This is useful for provenance but creates risk if consumers treat IDs as globally interchangeable.

**Disposition:** IDs require an explicit canonical lineage/alias model before automated joins or authorization checks depend on them.

### R-005 — Individual contracts contain legacy role language

DemiJoule, Herald, and Reciprocity have individual specs that were registered earlier than the later formation topology. Their current responsibilities remain useful but must be interpreted against the newer authority separation invariant.

**Disposition:** Do not rewrite all individual specs in one pass. Reconcile one agent contract at a time, preserving historical provenance and requiring the governing sign-off for material authority changes.

### R-006 — Public/IP visibility is already a governed concern

`PROPRIETARY.md` explicitly separates T1 PUBLIC, T2 FRAMEWORK, and T3 SOVEREIGN content, with NDR-133 firewall behavior and Drive-only handling for sovereign material.

**Disposition:** Treat classification, disclosure, public comprehension, and IP/security boundaries as intersecting but distinct controls.

## 3. Canonical Non-Substitution Rule

No reconciliation document, matrix, evaluator, or agent may resolve the above discrepancies by inventing an authority assignment.

Until a discrepancy is formally reconciled:

- preserve the conflicting source records;
- label the conflict;
- prevent automated inference of new authority;
- escalate consequential ambiguity;
- retain exact provenance.

## 4. Next Reconciliation Sequence

1. Reconcile roster vs topology.
2. Establish explicit agent lineage/alias semantics for legacy and formation-specific IDs.
3. Reconcile Layer-0 gate attribution and ETHICAL_HOLD without collapsing shared constitutional constraints.
4. Reconcile Sentinel → Sentinel-Phi authority continuity.
5. Normalize each active agent's required authority-contract fields.
6. Expand deterministic tests from presence checks to source-consistency checks.
7. Only then consider automated CI enforcement for authority drift.

## 5. Non-Claims

This record does not claim:

- legal compliance;
- real-world ethical adequacy;
- production authorization;
- that the current roster is fully synchronized with the topology;
- that any synthetic evaluator establishes agent competence.

**Reconciliation state:** OPEN / CONTROLLED / NO AUTHORITY TRANSFER.
