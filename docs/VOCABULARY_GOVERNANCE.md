# DGAF Vocabulary Governance

## Purpose

This document governs how project-local names, aliases, role classes, states, and public-facing labels are translated without changing underlying identity, authority, scientific state, or evidence status.

Machine-readable authority: `docs/VOCABULARY_TRANSLATION_MATRIX.json`.

## Five distinct vocabulary objects

1. **Canonical identity** — a named project-local agent identity.
2. **Alias** — a compatibility name whose relationship has been explicitly adjudicated.
3. **Abstract role/archetype** — a function class such as `VERIFY`, `GOVERN`, or `SENTINEL_ARCHETYPE`; it is not an identity and grants no authority.
4. **State** — a condition represented in the system; it is not an independent agent authority.
5. **External functional label** — plain-language explanation for public readers; it is translation only.

## Source and conflict rule

Vocabulary may not adjudicate conflicts that belong to identity or authority governance.

- `registry/agent_identity_manifest.v1.json` is the conflict register for observed identity relationships.
- `docs/agents/AGENT_AUTHORITY_MATRIX.md` records bounded authority relationships.
- `docs/agents/AGENT_ROSTER.md`, `FORMATION_TOPOLOGY.md`, and `AGENT_ECOSYSTEM_REGISTRY.md` remain underlying identity/formation sources within their stated scopes.
- `docs/CURRENT_STATE.md` remains scientific-state authority.

If these sources disagree, the translation matrix must preserve the disagreement using `resolution_status` or `unresolved_relations`; it must not select a winner merely to simplify public prose.

## Current explicit conflict handling

### Sentinel / Sentinel-Phi

The identity manifest preserves a separate Sentinel lineage and records Sentinel-Phi as a related/variant identity. Therefore:

- `Sentinel` is **not** an accepted alias of `Sentinel-Phi` in the translation registry;
- public prose may translate `Sentinel-Phi` when a source specifically names Sentinel-Phi;
- a source that says only `Sentinel` must not be silently rewritten as Sentinel-Phi;
- DemiJoule's `SENTINEL_ARCHETYPE` remains an abstract role and is neither identity.

### Ionia

Newer topology/ecosystem records classify Ionia as a state while the older sovereign roster describes an agent seat. Until that ontology conflict is formally reconciled, external translation uses **Convergence & Modal-Lock State (Ionia)** and assigns no independent agent authority.

## Coverage rule

Every identity with `activation_status=active` in the identity manifest must have a translation entry before this matrix can pass CI. This currently includes the previously omitted Reson, Lyra, and Echolette identities.

Conceptual/prospective identities do not need a public label merely because they exist internally. They require an entry before first meaningful appearance on a designated public surface.

## Public-surface rule

Designated public surfaces are declared in the matrix. On those surfaces:

- lead with function before codename on first meaningful use;
- do not present aliases as additional active seats;
- do not present role classes as identities;
- preserve independence, authorization, scientific-state, and efficacy ceilings;
- use project-local names as codenames, not as purported industry-standard terminology.

Internal specifications, traces, fixtures, and historical records may use canonical shorthand when the audience already shares the ontology.

## Change classes

### LABEL_ONLY

A public wording change may proceed through the vocabulary/documentation lane when identity binding, authority ceiling, and conflict status are unchanged.

### ALIAS_OR_IDENTITY

Adding/removing an alias, changing `identity_kind`, or changing `resolution_status` requires reconciliation against the identity manifest and the underlying authoritative identity sources. A translation PR cannot resolve a contested lineage by itself.

### AUTHORITY_RELATED

Any change that would alter veto, gate, verification, execution, publication, or other authority must be established in the relevant authority source first. The vocabulary registry can only describe the accepted boundary.

### PUBLIC_SURFACE

A new public-facing use must satisfy first-use translation and claim-ceiling rules.

### MOVING_STATE_PROHIBITED

Runtime status, CI status, deployment status, experiment lifecycle, scientific N, authorization state, and efficacy never belong in vocabulary entries. These change too frequently and must remain in their own authoritative state surfaces.

## Review checklist

A vocabulary-changing PR should answer:

1. Is this an identity, alias, role/archetype, state, or external label?
2. Does the identity manifest already contain a conflict involving the term?
3. Does the change imply authority that the authority matrix does not establish?
4. Does a public reader need the codename at all, or only the functional label?
5. Could the wording imply independent verification, certification, authorization, or efficacy?
6. Does the change accidentally embed moving runtime/scientific state?
7. Are all active identities still covered?
8. Are designated public surfaces still understandable without project lore?

## CI contract

The `Vocabulary Translation Matrix` workflow must fail closed when:

- required active identities are missing;
- an alias is duplicated or ambiguous;
- Sentinel is collapsed into Sentinel-Phi while the identity conflict remains unresolved;
- Ionia is promoted from state to agent by translation alone;
- DemiJoule loses the distinction between `SENTINEL_ARCHETYPE` and identity;
- translation claims scientific, authority, or identity-resolution effects;
- required external labels disappear from the public translation layer.

Passing this gate establishes vocabulary consistency only. It does not establish agent correctness, authority, independent verification, scientific validity, efficacy, or High-Assurance status.
