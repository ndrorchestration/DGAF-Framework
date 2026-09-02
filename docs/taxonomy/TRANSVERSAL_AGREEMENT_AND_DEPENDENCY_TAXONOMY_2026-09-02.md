# Transversal Dependency & Agreement Taxonomy — 2026-09-02

**Status:** CANONICAL RECONCILIATION ADDENDUM
**Scope:** taxonomy, vocabulary, agent-role registries, evidence governance, pattern libraries, CI control surfaces, deployment provenance, and operational documentation.
**Applies to:** the current documentation/control-plane lineage and future candidate cycles.

## 1. Core distinction

A project state is **transversally coherent** only when the independently maintained projections of that state agree on the same identity tuple and do not assert incompatible status.

Required identity tuple:

`apparatus/source SHA + candidate SHA/tree + deployment identity/source SHA + workflow/evidence run + artifact identity + protocol/analysis binding + freeze identity + authorization state`

A shared repository, branch ancestry, deployment URL, workflow name, or behavioral similarity is not sufficient to establish identity.

## 2. Dependency classes

| Class | Meaning | Closure rule |
|---|---|---|
| `UPSTREAM_IDENTITY` | Source, apparatus, candidate, tree, deployment identity | Must resolve before downstream evidence can close |
| `EXECUTION_DEPENDENCY` | Runtime, artifact, custody, reproducibility, security controls | Re-run when an affected upstream identity changes |
| `GOVERNANCE_DEPENDENCY` | P7, P8, independent P9, freeze, authorization | Requires current-cycle evidence and explicit transition authority |
| `CROSS_SYSTEM_DEPENDENCY` | GitHub ↔ Vercel ↔ Notion ↔ retained artifacts | Each system must describe the same scoped state without contradiction |
| `HISTORICAL_REFERENCE` | Prior candidate/run/deployment retained for provenance | Must be explicitly historical/non-closing |

## 3. Transversal agreement rule

For every live candidate, the following projections must agree:

1. GitHub candidate manifest/control state;
2. GitHub CI/evidence artifacts;
3. Vercel deployment source/target metadata, when deployment is required;
4. Notion operational control state;
5. taxonomy/vocabulary classification;
6. pattern-library status and cross-references;
7. public/current documentation claims.

A discrepancy is classified as:

- **BENIGN HISTORICAL DIFFERENCE** — explicitly scoped to a prior identity;
- **ROLE DIFFERENCE** — distinct identities with clearly different semantic roles;
- **UNRESOLVED TRANSVERSAL DRIFT** — two live projections can reasonably be read as describing different current states;
- **BLOCKING CONTRADICTION** — one projection would cause an invalid downstream closure, transfer, or authorization.

## 4. Dependency propagation

A material change to any behavior-affecting dependency creates a new candidate cycle and invalidates affected downstream evidence. Documentation-only changes may preserve apparatus identity, but they still require current-state reconciliation before they are described as live.

## 5. P-35 / P-42 terminology boundary

`P-35` = **Procluding Premise Gate**, the canonical Layer-0 pre-admissibility pattern.

`P-42` = **Adaptive Harmonic Governance (AHG)**, the separate pattern created by renumbering AHG after the P-35 namespace collision.

The P-35 remediation currently under verification adds an **explicit premise-check dependency at the DGAF/TGL/ConsensusTask boundary**. This is an engineering wiring/integrity rule. It is not, by itself, a project-approved PDMAL constitutional premise policy.

The PDMAL-specific premise checker remains an explicit experimental-control dependency and must be supplied/approved before pilot execution.

## 6. Evidence-state vocabulary

Use these terms distinctly:

`DEFINED → IMPLEMENTED → TESTED → CANDIDATE-BOUND → VERIFIED → FROZEN → AUTHORIZED → EMPIRICAL`

Transitions are not implied by proximity. In particular:

`VERIFIED != FROZEN`
`FROZEN != AUTHORIZED`
`AUTHORIZED != EMPIRICAL`
`READY deployment != runtime verified`
`historical evidence != current evidence`

## 7. Taxonomy rule

Agent, formation, and role taxonomies describe intended identity and boundaries. They do not independently establish model capability, experimental efficacy, production readiness, or standards equivalence.

Authority claims require an authority source. External mappings are analogies unless equivalence is demonstrated. Numerical claims require reproducible measurement provenance.

## 8. Pattern-library rule

Pattern libraries must preserve:

- canonical identifier;
- namespace/alias history;
- dependency class;
- authority class;
- evidence status;
- implementation boundary;
- historical/superseded status where applicable;
- current cross-references to vocabulary and control documents.

A pattern entry must never promote a historical verification result to a current result merely because the pattern identifier is unchanged.

## 9. Current audit disposition

For candidate `edd3b5c8266e2680b9bb94301c2623a3f1ac0cf0`:

- GitHub CI: broad pass; PDMAL Pre-Freeze Runner Validation currently blocked by stale regression callers that do not inject the newly required P-35 checker.
- Governance CI: blocked by a pinned TLA+ Tools SHA mismatch; expected digest must be independently re-verified before modification.
- Pre-Authorization Security: PASS.
- Vercel: no exact-candidate deployment currently evidenced.
- Freeze: NOT CREATED.
- Authorization: NOT GRANTED.
- Empirical N: 0.

**Canonical disposition:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.
