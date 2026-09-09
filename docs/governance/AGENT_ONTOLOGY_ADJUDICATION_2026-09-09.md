# DGAF Agent Ontology Adjudication — 2026-09-09

**Status:** ACCEPTED GOVERNANCE ADJUDICATION / SCIENTIFIC STATE EFFECT = NONE  
**Controller:** #522  
**Base main:** `fb0479b628559a264d8ae7436dce2820eb6a31e8`

## Purpose

Resolve the identity/designation conflicts exposed by the vocabulary sweep without deleting historical lineage, silently renumbering sovereign seats, or allowing formation-local labels to acquire authority they were never granted.

This record governs identity ontology only. It does not alter Track A, empirical N, verification independence, experiment authorization, canonical DGAF efficacy, or High-Assurance state.

## Source precedence

The following source roles are binding:

1. `docs/agents/AGENT_ROSTER.md` is the **sovereign source for canonical agent identity and canonical numbered seat assignment**.
2. `docs/agents/FORMATION_TOPOLOGY.md` is authoritative for **formation membership, formation-local designations, variants, archetypes, and formation/runtime states**. A formation-local designation does not by itself renumber a sovereign seat.
3. `docs/agents/AGENT_ECOSYSTEM_REGISTRY.md` is authoritative for **ecosystem metadata, inventory state, and formation metadata**. It consumes sovereign identity rather than overriding it.
4. `registry/agent_identity_manifest.v1.json` is the machine-readable reconciliation layer. It must preserve canonical identity separately from observed/local/historical designations.
5. `docs/VOCABULARY_TRANSLATION_MATRIX.json` is a translation layer only. It may render an adjudicated identity or state but cannot decide identity or authority.

When these surfaces conflict on a numbered identity, the sovereign roster assignment controls unless a later explicit sovereign roster amendment says otherwise.

## Adjudications

### COLLEEN

- Canonical sovereign identity: **COLLEEN — A-05**.
- `A-00-GOV` is retained as a **formation-local governance designation** describing COLLEEN's role in Sovereign Governance.
- `A-00-GOV` is not a second sovereign seat and does not replace A-05.

### The Librarian

- Canonical sovereign identity: **The Librarian — A-06**.
- `A-06-L` is retained as a **formation-local Archive Trio designation**.
- It is not a second sovereign identity.

### Zenith, Reson, Lyra, and Echolette

Canonical sovereign assignments remain:

| Canonical identity | Sovereign seat | Retained formation-local designation(s) |
|---|---:|---|
| Zenith | A-09 | A-09-Z |
| Reson | A-10 | A-09 |
| Lyra | A-11 | A-10 |
| Echolette | A-12 | A-11 |

The historical/topology labels remain provenance-bearing local designations. They must not be presented as a renumbering of the sovereign roster.

### Sentinel and Sentinel-Phi

- **Sentinel** and **Sentinel-Phi** remain distinct ontology records.
- Base Sentinel is a sovereign security lineage/role referenced by the roster's governance rules and historical lineage. No numbered sovereign roster seat is assigned by this adjudication.
- Sentinel-Phi is a distinct formation variant/identity with formation-local designation **A-12-φ**.
- Sentinel-Phi is not an alias of Echolette A-12 and does not replace the sovereign A-12 seat.
- The historical Sentinel-to-Sentinel-Phi development lineage may be retained as provenance, but lineage does not collapse identity.

### Ionia

Two distinct objects are recognized:

1. **Agent Ionia — A-13**: the canonical sovereign roster identity unless and until an explicit sovereign roster amendment retires or reclassifies that seat.
2. **IONIA_STATE / Ionia 0Hz state**: a formation/runtime convergence state. It is not an agent seat and does not consume A-13.

Any current-facing document or translation that says only `Ionia` where the distinction matters must identify whether it means **Agent Ionia (A-13)** or **IONIA_STATE (0Hz state)**.

### DemiJoule and `SENTINEL_ARCHETYPE`

DemiJoule's `SENTINEL_ARCHETYPE` remains an abstract role/archetype. It grants no Sentinel or Sentinel-Phi identity and no sovereign veto authority.

### Herald, Reciprocity, and other topology-local designations

Formation-local identifiers such as Herald `A-05`, Reciprocity `A-06-R`, DemiJoule `A-03-DJ`, and later topology identifiers may be retained as local/historical topology labels, but they are not sovereign numbered seat assignments unless the sovereign roster explicitly contains that assignment.

### A-20 through A-27 conceptual/prospective topology entries

Oracle, Vanguard, Navigator, Momentum, Paragon, Synergy, Equilibrium, and Sentience remain formation/ecosystem conceptual or prospective identities unless separately admitted to the sovereign roster. Directory presence, seed inventory, or formation membership does not by itself create a sovereign numbered seat.

## Required representation rule

Machine-readable identity records must distinguish at least:

- stable identity ID;
- canonical sovereign seat, if any;
- identity kind (`agent`, `variant`, `state`, `archetype`, `stub`, `conceptual`, `historical`);
- formation-local designations;
- historical/observed designations;
- lineage/variant relationships;
- activation status;
- unresolved conflicts, if any.

A local designation may equal the canonical number of a different agent only when it is explicitly typed as local/historical and therefore cannot be mistaken for the sovereign seat.

## Authority boundary

This adjudication does not modify the existing authority matrix. Naming, designation, formation membership, or translation does not independently grant veto, write, verification, publication, or experiment authority.

Any actual authority change requires its own explicit governance event.

## Scientific boundary

`SCIENTIFIC_STATE_EFFECT = NONE`

`TRACK_A_EPOCH_001_PRIMARY_ANALYSIS = UNANALYZABLE / NOT_RUN`

`SUCCESSOR_TRACK_A_EMPIRICAL_COLLECTION = NOT_AUTHORIZED`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

`HIGH_ASSURANCE = NOT_AUTHORIZED`

## Supersession rule

This record resolves the collision semantics documented in `AGENT_IDENTITY_RECONCILIATION_2026-09-04.md`. That earlier document remains historical audit evidence; its unresolved-collision status is superseded only for the specific conflicts explicitly adjudicated here.
