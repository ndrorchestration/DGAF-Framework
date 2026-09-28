# DGAF Architecture Mapping Method

**Status:** PROPOSED / ARCHITECTURE-GOVERNANCE METHOD / NON-AUTHORIZING

## Purpose

Define a repeatable method for mapping DGAF source, schemas, controllers, tests, evidence records, and governance documents to the canonical architecture without confusing historical provenance, profile specialization, adapters, or true duplicate authority.

## External practice basis

This method adapts, rather than wholesale imports, several established practices:

- **C4 abstraction-first architecture mapping:** maintain distinct system-landscape, system/component, and code views; automate long-lived component/code views where useful.
- **Architecture Decision Records (ADRs):** record significant structure, interface, dependency, security, and non-functional decisions; preserve accepted/rejected history and supersede rather than rewrite.
- **NIST SSDF:** track security requirements, risks, design decisions, and provenance as part of the development lifecycle.
- **NIST Zero Trust / PDP-PEP separation:** keep policy decision and policy enforcement responsibilities logically explicit, minimize implicit trust, and bind authorization to subjects/resources.
- **NIST AI RMF:** maintain an inventory, assign ownership/responsibility, monitor it periodically, and explicitly manage decommission/supersession.
- **SLSA / in-toto-style provenance:** record verifiable relationships among produced artifacts, source identities, execution/build context, and dependencies.

These sources inform process quality; they do not certify DGAF or establish equivalence with any standard.

## Mapping levels

### L0 — Ecosystem landscape
Question: **What systems exist and what authority relationship connects them?**

Examples: DGAF, AOSS, ACP, PDMAL, PPTL, RDC, n8n.

Primary artifact:
- `DGAF_SYSTEM_ARCHITECTURE_TAXONOMY.md`

### L1 — DGAF component architecture
Question: **Which first-class internal component owns each responsibility?**

Canonical owners:
- K1–K8 governance kernel;
- A1–A4 cross-cutting assurance.

Primary artifacts:
- `DGAF_CORE_COMPONENT_INVENTORY.md`
- `DGAF_CORE_COMPONENT_REGISTRY.v1.json`

### L2 — Profile architecture
Question: **Which domain lifecycle specializes the kernel and why?**

Profiles include Track/Epoch, AOSS Stage A, Mode-T, PDMAL, external review, and self-application.

A profile may add states, evidence requirements, custody, or stronger guards. It must not silently redefine kernel semantics.

### L3 — Artifact/code ownership
Question: **What source file, schema, controller, test, or record implements or evidences each component/profile?**

This level is machine-readable and should be validated automatically.

## Required artifact record

Each active architecture-sensitive artifact should record:

- `path` — repository-relative path;
- `artifact_type` — code, schema, policy, evidence, test, workflow, UI, record, or documentation;
- `primary_owner` — exactly one K-/A-/P-/X- architecture ID;
- `secondary_dependencies` — zero or more related architecture IDs;
- `role` — concise responsibility;
- `authority_effect` — what kind of authority/state/evidence effect the artifact can participate in;
- `profile` — optional governed profile;
- `lifecycle` — ACTIVE, HISTORICAL, SUPERSEDED, RETIRED, CANDIDATE;
- `evidence_scope` — what claim/evidence scope the artifact can support;
- `tests_or_validators` — linked checks where applicable;
- `source_binding` — how exact source identity is established;
- `decision_ref` — ADR/architecture decision when the placement is significant or contested;
- `classification_confidence` — HIGH/MEDIUM/LOW with rationale when interpretation is non-trivial.

### One-primary-owner rule

Every architecture-sensitive active artifact gets **one primary owner**.

Many secondary dependencies are allowed.

This prevents:
- dual authority;
- orphan controls;
- circular ownership;
- documentation claiming a control belongs everywhere.

Shared utility code may use a designated utility/support owner only when it has no independent authority effect.

## Authority-effect vocabulary

Use narrow, machine-checkable values:

- `NONE`
- `IDENTITY_BINDING`
- `AUTHORITY_BOUNDING`
- `ALLOW_DENY_ESCALATE`
- `STATE_TRANSITION_GATING`
- `REPLAY_OR_COMMIT_GATING`
- `EVIDENCE_BINDING`
- `RECOVERY_GATING`
- `CLAIM_PROMOTION_GATING`
- `CUSTODY_GATING`
- `ASSURANCE_ONLY`
- `PRESENTATION_ONLY`

An artifact may participate in a secondary effect through dependencies, but the registry records its primary architectural effect.

## Classification procedure

For each artifact:

1. **Identify behavior, not filename.** Read implementation/specification and determine what it actually controls or records.
2. **Identify the decision boundary.** Ask whether it can permit/deny execution, gate state, widen/narrow authority, bind evidence, constrain claims, or only observe/present.
3. **Assign exactly one primary owner.**
4. **Record secondary dependencies.**
5. **Determine profile specificity.** If semantics exist only because of a scientific/assurance lifecycle, assign the profile rather than creating a new kernel owner.
6. **Determine lifecycle state.** Preserve historical/superseded artifacts; do not delete or relabel event-time evidence.
7. **Bind tests and source identity.**
8. **Classify overlap using the overlap taxonomy below.**
9. **Create an ADR when ownership changes, a new authority engine is proposed, or a kernel/profile boundary changes.**
10. **Run architecture fitness checks before acceptance.**

## Overlap taxonomy

Never label two similar artifacts as duplicates until they are classified.

### O1 — TRUE_DUPLICATE_AUTHORITY
Two active mechanisms independently make materially equivalent authority decisions for the same scope without an explicit composition relationship.

**Default action:** block expansion; converge or formally compose via ADR.

### O2 — PROFILE_SPECIALIZATION
A domain lifecycle adds narrower/stronger states or evidence requirements on top of kernel semantics.

**Default action:** preserve; document mapping to kernel.

### O3 — ADAPTER_OR_IMPLEMENTATION_VARIANT
Multiple implementations realize the same contract for different runtime/language/provider contexts.

**Default action:** preserve if contract/conformance is explicit; test semantic parity where important.

### O4 — HISTORICAL_OR_SUPERSEDED
Old mechanism remains for provenance, evidence, compatibility, or historical reconstruction.

**Default action:** preserve; mark lifecycle and successor.

### O5 — ASSURANCE_OBSERVER
Artifact evaluates or records a control but does not own the underlying authority.

**Default action:** classify under A1/A2/A3 or assurance profile; prohibit authority inheritance.

### O6 — ORPHAN_OR_AMBIGUOUS
Active artifact has no clear owner or plausible multiple primary owners.

**Default action:** fail architecture review until adjudicated.

## Architecture fitness functions

Architecture rules should be executable where practical.

### Blocking fitness functions
- every registered path exists;
- every active architecture-sensitive artifact has one primary owner;
- owner IDs are canonical;
- no duplicate registry path;
- profile IDs use P- namespace and integrations X- namespace;
- active authority-bearing artifacts declare a non-NONE authority effect;
- superseded artifacts identify successor/decision reference where applicable.

### Advisory drift functions
- scan new/changed files for authority-sensitive terms;
- flag unregistered authorization/state/replay/revocation/custody/evidence controllers;
- flag new schemas containing authorization/status/decision fields;
- flag code that can dispatch/write/delete/privilege-change without a mapped K3/K4/K5 relationship;
- flag duplicate state/decision vocabulary introduced outside an existing namespace;
- flag current-facing docs using retired architecture terms.

Advisory findings become blocking only after false-positive behavior is understood and the rule is stable.

## Review matrix

Each candidate mapping should be reviewed from five perspectives:

| Lens | Question |
|---|---|
| Authority | Can this artifact change what may happen? |
| State | Can it move or interpret a governed lifecycle state? |
| Evidence | Can it bind, strengthen, weaken, or promote a claim? |
| Execution | Does it cause or mediate an external effect? |
| Provenance | Can we bind the mapping to exact source/tests/decision history? |

A sixth **profile** question asks whether the behavior is universal DGAF kernel behavior or exists only in a bounded research/assurance lifecycle.

## Drift and review cadence

Review mappings:
- on every architecture-sensitive PR;
- when a new schema/controller/action class/profile is introduced;
- when an ADR changes ownership/boundaries;
- after major source-tree moves;
- periodically as part of ecosystem/architecture audits.

Do not require manual review of unchanged historical evidence on every cycle.

## Decision discipline

Create or supersede an ADR when:
- adding/removing K1–K8 or A1–A4;
- changing a component's authority effect;
- moving an active authority-bearing artifact between primary owners;
- adding a new general-purpose authority/state/evidence engine;
- changing kernel-vs-profile boundaries;
- adopting a new external authority dependency.

Accepted ADRs are historical decisions. Replace them through supersession rather than silent editing.

## Mapping confidence

- **HIGH:** implementation/spec and tests clearly identify owner/effect.
- **MEDIUM:** evidence supports placement but responsibility spans boundaries.
- **LOW:** artifact is legacy, polymorphic, or insufficiently documented.

LOW-confidence active authority artifacts are architecture-review priorities.

## Completion criteria

The architecture map is complete enough for enforcement when:

1. all active authority-bearing code/schemas/controllers are mapped;
2. all profile state machines/authorization records are mapped;
3. all external execution adapters are mapped;
4. all mappings have source/test bindings;
5. no O1 or O6 finding remains unresolved;
6. architecture drift checks pass on the exact candidate;
7. accepted ADRs cover significant boundary decisions.

This is not a claim that every repository document must be individually registered.

## Non-effect

This method defines architecture-governance practice only. It changes no runtime authority, experiment state, scientific N, efficacy, independent-validation, or High-Assurance status.
