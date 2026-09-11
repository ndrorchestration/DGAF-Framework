# DGAF Vocabulary Governance

## Purpose

This document governs how project-local names, aliases, formation-local designations, role classes, states, and public-facing labels are translated without changing underlying identity, authority, scientific state, or evidence status.

Machine-readable translation authority: `docs/VOCABULARY_TRANSLATION_MATRIX.json`.
Accepted ontology adjudication: `registry/agent_ontology_adjudication.v1.json`.

## Six distinct vocabulary objects

1. **Canonical identity** — a named project-local agent identity governed by the accepted identity/ontology sources.
2. **Alias** — a compatibility name whose relationship has been explicitly adjudicated.
3. **Formation-local identity/designation** — a formation-scoped variant or identifier that cannot silently create or renumber a sovereign seat.
4. **Abstract role/archetype** — a function class such as `VERIFY`, `GOVERN`, or `SENTINEL_ARCHETYPE`; it is not an identity and grants no authority.
5. **State** — a condition represented in the system; it is not an independent agent authority.
6. **External functional label** — plain-language explanation for public readers; it is translation only.

## Source and adjudication rule

Vocabulary may not adjudicate identity or authority conflicts on its own. It must consume the accepted ontology state.

- `docs/agents/AGENT_ROSTER.md` is the canonical sovereign numbered-seat source.
- `registry/agent_ontology_adjudication.v1.json` is the accepted reconciliation/adjudication layer from completed issue #522.
- `registry/agent_identity_manifest.v1.json` remains the historical conflict register for observed identity relationships and source disagreement; it is not the post-#522 authority-resolution source.
- `docs/agents/FORMATION_TOPOLOGY.md` and `docs/agents/AGENT_ECOSYSTEM_REGISTRY.md` govern formation-local structures within their scopes.
- `docs/agents/AGENT_AUTHORITY_MATRIX.md` records bounded authority relationships.
- `docs/CURRENT_STATE.md` remains scientific-state authority.

Translation may describe an accepted adjudication, but `scientific_state_effect`, `authority_effect`, and `identity_resolution_effect` remain `NONE`.

## Current explicit ontology handling

### Sentinel / Sentinel-Phi

Completed issue #522 establishes that Sentinel and Sentinel-Phi are **distinct ontology records**:

- base Sentinel is a sovereign security lineage/role with no canonical numbered seat assigned by the accepted adjudication;
- Sentinel-Phi is a distinct formation variant/identity with formation-local designation `A-12-φ`;
- `Sentinel` is **not** an alias of `Sentinel-Phi`;
- a source that says only `Sentinel` must not be silently rewritten as Sentinel-Phi;
- DemiJoule's `SENTINEL_ARCHETYPE` remains an abstract role and is neither identity.

The base Sentinel lineage/seat remains a bounded unresolved relation, but the non-collapse rule is adjudicated.

### Agent Ionia / IONIA_STATE

Completed issue #522 resolves the previous agent-vs-state conflict:

- **Agent Ionia — A-13** is the canonical sovereign roster identity unless a later explicit sovereign-roster amendment changes it;
- **`IONIA_STATE` / Ionia 0Hz** is a separate formation/runtime convergence state;
- `IONIA_STATE` consumes no sovereign numbered seat;
- current-facing text must identify which object is intended whenever `Ionia` would otherwise be ambiguous.

The translation matrix therefore carries **two distinct entries**: Agent Ionia as `AGENT` and `IONIA_STATE` as `STATE`.

### Canonical seats and formation-local designations

The same accepted adjudication establishes sovereign-roster precedence for COLLEEN, The Librarian, Zenith, Reson, Lyra, Echolette, and Agent Ionia. Formation-local designations remain preserved as local metadata; they do not replace the canonical sovereign identities.

## Coverage rule

Every identity with `activation_status=active` in the historical identity manifest must have a translation entry before this matrix can pass CI. The accepted ontology may additionally require translated objects, such as `IONIA_STATE`, even when they are not active agent identities in the historical manifest.

Conceptual/prospective identities do not need a public label merely because they exist internally. They require an entry before first meaningful appearance on a designated public surface.

## Public-surface rule

Designated public surfaces are declared in the matrix. On those surfaces:

- lead with function before codename on first meaningful use;
- do not present aliases as additional active seats;
- do not present formation-local designations as sovereign seats;
- do not present role classes or states as agent identities;
- preserve independence, authorization, scientific-state, and efficacy ceilings;
- use project-local names as codenames, not as purported industry-standard terminology.

Internal specifications, traces, fixtures, and historical records may use canonical shorthand when their temporal/source scope is explicit.

## Change classes

### LABEL_ONLY

A public wording change may proceed through the vocabulary/documentation lane when identity binding, authority ceiling, and adjudicated object type remain unchanged.

### ALIAS_OR_IDENTITY

Adding/removing an alias, changing `identity_kind`, or changing `resolution_status` requires reconciliation against the accepted ontology adjudication and underlying authoritative identity sources. A translation PR cannot invent a new ontology decision.

### AUTHORITY_RELATED

Any change that would alter veto, gate, verification, execution, publication, or other authority must be established in the relevant authority source first. The vocabulary registry can only describe the accepted boundary.

### PUBLIC_SURFACE

A new public-facing use must satisfy first-use translation and claim-ceiling rules.

### MOVING_STATE_PROHIBITED

Runtime status, CI status, deployment status, experiment lifecycle, scientific N, authorization state, and efficacy never belong in vocabulary entries. These change too frequently and must remain in their own authoritative state surfaces.

## Review checklist

A vocabulary-changing PR should answer:

1. Is this a canonical identity, alias, formation-local designation/variant, role/archetype, state, or external label?
2. What does the accepted ontology adjudication say about the object?
3. Does the historical conflict register contain provenance that must remain visible without overriding the adjudication?
4. Does the change imply authority that the authority matrix does not establish?
5. Does a public reader need the codename at all, or only the functional label?
6. Could the wording imply independent verification, certification, authorization, or efficacy?
7. Does the change accidentally embed moving runtime/scientific state?
8. Are all required active/adjudicated objects still covered?
9. Are designated public surfaces still understandable without project lore?

## CI contract

The `Vocabulary Translation Matrix` workflow must fail closed when:

- required active/adjudicated objects are missing;
- an alias is duplicated or ambiguous;
- Sentinel is collapsed into Sentinel-Phi;
- Agent Ionia A-13 and `IONIA_STATE` are collapsed or assigned the wrong object kinds;
- DemiJoule loses the distinction between `SENTINEL_ARCHETYPE` and identity;
- translation claims scientific, authority, or identity-resolution effects;
- required external labels disappear from the public translation layer.

Passing this gate establishes vocabulary consistency only. It does not establish agent correctness, authority, independent verification, scientific validity, efficacy, or High-Assurance status.
