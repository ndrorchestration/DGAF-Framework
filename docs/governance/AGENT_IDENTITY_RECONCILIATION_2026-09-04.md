# DGAF Agent Identity Reconciliation — 2026-09-04

**Status:** Audit control / conflict register; no identity authority changed
**Base:** `4ac8937f5b8f3358655a06ee7f9d8cd83b87106c`

## Purpose

Prevent agent counts, IDs, directories, variants, historical seeds, and system states from being collapsed into a single taxonomy value before authority is explicitly resolved.

## Observed authority surfaces

| Source | Declared role | Material state observed |
|---|---|---|
| `docs/agents/AGENT_ROSTER.md` v1.2 | Sovereign identity/role SSoT | 20 seats A-00→A-19; A-14→A-19 T3 stubs |
| `docs/agents/FORMATION_TOPOLOGY.md` v1.2 | Formation topology | 27 named seats/entries in Phase E model; includes A-20→A-27 and Sentinel-Phi A-12-φ |
| `docs/agents/AGENT_ECOSYSTEM_REGISTRY.md` v2.1 | Ecosystem metadata | 27-agent ecosystem; Ionia explicitly classified as STATE; Sentinel-Phi A-12-φ |
| `docs/AGENT_ARCHITECTURE_ASSESSMENT.md` | Architecture assessment | 25 physical agent directories; 26 conceptual/historical named entries when historical Sentience is counted |

## Confirmed collision classes

### A-09

- Roster: **Zenith A-09**.
- Formation topology: **Reson A-09** and **Zenith A-09-Z**.
- Ecosystem registry: **Reson A-09** and **Zenith A-09-Z**.

### A-10 / A-11 / A-12

- Roster: A-10 Reson, A-11 Lyra, A-12 Echolette.
- Formation topology/ecosystem: A-10 Lyra, A-11 Echolette, A-12-φ Sentinel-Phi; Reson is A-09.

This is a direct identifier collision, not merely a naming preference.

### Sentinel / Sentinel-Phi

- Base Sentinel has its own sovereign lineage.
- Sentinel-Phi is explicitly described as an A-12-φ strategic variant in the formation/ecosystem documents.
- The base roster still contains a non-variant A-12 assignment that conflicts with the topology/ecosystem lineage.

### Ionia

- Ionia carries A-13 in the roster and rubric.
- Formation/ecosystem sources explicitly classify Ionia as a **0 Hz system STATE**, not a functional agent seat.
- Treat `A-13` as an observed historical/documentation identity until authority is reconciled.

### A-20–A-27

Oracle, Vanguard, Navigator, Momentum, Paragon, Synergy, Equilibrium, and Sentience are present in current topology/ecosystem documentation, but are absent from the older 20-seat roster. Presence in directories or rubrics does not by itself make them canonical live seats.

## Counting model

Keep these quantities separate:

1. **Canonical roster seats:** 20 (current claim of `AGENT_ROSTER.md`).
2. **Physical agent directories:** 25 (architecture assessment).
3. **Named conceptual/historical entries:** 26 when historical Sentience is included.

These are different measures and must not be used interchangeably.

## Proposed target identity schema

```json
{
  "agent_id": "stable-unique-id",
  "display_name": "human-readable name",
  "directory": "physical/path",
  "seat_status": "canonical|variant|conceptual|historical|state|stub|conflicted",
  "variant_of": null,
  "formation_ids": [],
  "activation_status": "active|inactive|prospective|historical",
  "canonical_source": "path-or-registry-id",
  "source_commit": "40-char SHA",
  "rubric_ids": [],
  "supersedes": [],
  "superseded_by": [],
  "conflicts": []
}
```

## Resolution protocol

1. Record all observed identities without deletion.
2. Assign stable identity records independent of display name and seat number.
3. Mark collisions explicitly.
4. Obtain an explicit authority decision for canonical seat allocation.
5. Update dependent topology and rubric references atomically.
6. Preserve supersession and historical lineage.
7. Run deterministic drift checks before considering the reconciliation complete.

## Prohibited shortcuts

- Do not choose the newest document automatically.
- Do not choose the highest-completeness source automatically.
- Do not infer canonical authority from directory presence.
- Do not delete historical/variant artifacts to make counts agree.
- Do not convert Ionia from STATE to agent merely to satisfy a count.

## Scientific boundary

This reconciliation is documentation/control work only. It does not authorize freeze, pilot execution, unblinding, production certification, or empirical claims.

**Current DGAF boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
