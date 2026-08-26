# DGAF Publication and Provenance Spine

**Status:** Active publication architecture; not an empirical validation claim  
**Created:** 2026-08-25  
**Purpose:** Make DGAF and related research externally legible without overstating novelty, efficacy, or maturity.

## 1. Publication principle

DGAF's public record should permit an external reader to determine what is **defined**, **implemented**, **tested**, and **not yet established** without relying on authorial authority. Publication is therefore treated as a provenance and audit mechanism, not as proof of correctness or priority.

A public timestamp can establish that a particular formulation existed publicly at a particular time. It does not by itself establish novelty, exclusive priority, validity, or empirical effectiveness.

## 2. The public contribution stack

### Layer A — Conceptual specification

Publish stable definitions of:

- Dynamic Governance Agentic Formation (DGAF);
- Phi-Driven Multi-Agent Lattice (PDMAL/PDMA-L);
- the governance, provenance, and evaluation boundaries between them;
- explicit assumptions, non-goals, and failure conditions.

Conceptual documents must distinguish original synthesis from established techniques and identify dependencies on prior work where known.

### Layer B — Reference implementation

The public repository is the inspectable implementation substrate. A cloneable implementation should be accompanied by enough configuration and documentation to reproduce the claimed repository-local behavior.

Implementation existence is not evidence of real-world efficacy.

### Layer C — Experimental record

Experimental claims require version-bound protocols, candidate identity, retained artifacts, analysis rules, and explicit null/negative-result handling. The current PDMAL track remains pre-freeze with empirical N = 0; publication must preserve that boundary.

### Layer D — Independent scrutiny

The strongest claims should become progressively more dependent on independent reproduction, comparison, critique, and verification rather than self-attestation.

## 3. Claim taxonomy for public communication

Every significant public statement should be classified before publication:

| Class | Meaning | Public wording rule |
|---|---|---|
| Definition | A proposed or specified concept | “DGAF defines…” |
| Implementation | Code or artifact exists | “The repository implements…” |
| Verification | A bounded test or check passed | Name the exact scope and evidence |
| Empirical result | A protocol produced data | State N, comparator, endpoint, and limitations |
| Hypothesis | A prediction awaiting testing | Use conditional language |
| Unsupported | Evidence is absent or inadequate | Do not promote as a result |

Repository-wide adjectives such as “proven,” “validated,” or readiness for production must not be inferred from component-level evidence.

## 4. Canonical publication sequence

1. **Canonical technical overview** — a concise entry point explaining the problem, architecture, terminology, and evidence boundaries.
2. **Versioned specification** — stable definitions and interfaces with changelog/provenance.
3. **Reproducibility packet** — instructions, dependencies, test commands, expected outputs, and known limitations.
4. **Experimental paper or technical report** — only after the relevant protocol and evidence support the claims made.
5. **Independent comparison and replication** — publish favorable, null, and unfavorable results under the same evidence policy.

The first three stages may proceed now. Stage four must not imply empirical findings that do not yet exist.

## 5. Priority and prior-art discipline

Before claiming novelty, perform and retain a scoped prior-art review across relevant disciplines, including multi-agent orchestration, distributed systems, AI governance, evaluation, control theory, and related research.

Use calibrated conclusions:

- “We are not aware of…” is not “this has never existed.”
- “This formulation is publicly documented as of…” is a provenance claim, not a priority verdict.
- Similarity of terminology does not establish conceptual equivalence; mechanism, scope, and evidence must be compared.

Where overlap exists, describe DGAF as a synthesis, implementation, adaptation, or distinct formulation as supported by the comparison.

## 6. Recommended external-facing artifacts

### Immediate

- Repository landing page with a one-paragraph problem statement and evidence boundary.
- `CITATION.cff` or equivalent citation metadata identifying the software/research artifact and version.
- Versioned release notes for meaningful public milestones.
- This publication/provenance spine linked from the documentation index.

### After candidate freeze and pilot authorization

- Archived protocol and freeze manifest.
- Reproducibility instructions tied to the exact candidate SHA.
- Results report containing pre-specified analyses and complete result accounting.

### After evidence matures

- A formal technical white paper or preprint with related-work review and precise claim/evidence mapping.
- Independent replication package and comparative baseline results where feasible.

## 7. Authorship and provenance

The repository's existing provenance identifies Ndr / Ender Hensel (`ndrorchestration`) as developer. Public attribution should identify contribution roles precisely and preserve commit/release history rather than attempting to convert repository authorship into unsupported claims of sole conceptual priority.

For collaborative work, record authorship, contribution roles, review boundaries, and AI assistance where materially relevant to interpretation or reproducibility.

## 8. Publication quality gate

A public artifact is publication-ready when it answers:

1. What exactly is being proposed or claimed?
2. What problem and scope does it address?
3. What is implemented versus hypothesized?
4. What evidence supports each important claim?
5. What would falsify, narrow, or revise the claim?
6. How can another party inspect or reproduce the relevant behavior?
7. What prior work or adjacent concepts may overlap?
8. What remains unknown?

Failure to answer one of these questions should result in narrowing the artifact's claims, not filling the gap with confidence language.

## 9. Current DGAF publication boundary

As of this document's creation, the public record supports publication of DGAF as an **open research and implementation framework for agent orchestration, evaluation, provenance, and governance controls**. It does not support presenting the current PDMAL research track as empirically effective, independently validated, production-proven, or novel in an absolute sense.

The immediate objective is therefore **discoverability with epistemic integrity**: create a durable, navigable record that lets others inspect the framework now and evaluate stronger claims as evidence becomes available.

## Cross-references

- [`README.md`](../README.md)
- [`CLAIM_EVIDENCE_INDEX.md`](CLAIM_EVIDENCE_INDEX.md)
- [`CURRENT_STATE.md`](CURRENT_STATE.md)
- [`PATTERN_COMMONS_ARCHITECTURE.md`](PATTERN_COMMONS_ARCHITECTURE.md)
- [`experiment/PDMAL_CURRENT_CONTROL_STATE.md`](experiment/PDMAL_CURRENT_CONTROL_STATE.md)
- [`experiment/PDMAL_EXPERIMENT_PROTOCOL.md`](experiment/PDMAL_EXPERIMENT_PROTOCOL.md)
- [`DGAF_EVIDENCE_AND_RELEASE_POLICY.md`](DGAF_EVIDENCE_AND_RELEASE_POLICY.md)
