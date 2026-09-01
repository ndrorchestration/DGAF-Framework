# DGAF Publication and Provenance Spine

**Status:** Active publication architecture; not an empirical validation or absolute novelty claim  
**Updated:** 2026-09-01  
**Purpose:** Make DGAF and related research externally legible without overstating novelty, efficacy, maturity, or historical priority.

## 1. Publication principle

DGAF's public record should permit an external reader to determine what is **defined**, **implemented**, **tested**, **verified**, **empirically established**, and **historically supported** without relying on authorial authority. Publication is therefore treated as a provenance and audit mechanism, not as proof of correctness, priority, or effectiveness.

A public timestamp can establish that a particular formulation existed publicly at a particular time. It does not by itself establish novelty, exclusive priority, validity, or empirical effectiveness.

## 2. The public contribution stack

### Layer A — Conceptual specification

Publish stable definitions of:

- Dynamic Governance Agentic Formation (DGAF);
- Phi-Driven Multi-Agent Lattice (PDMAL/PDMA-L);
- the governance, provenance, and evaluation boundaries between them;
- assumptions, non-goals, and failure conditions;
- established prior art and explicitly bounded candidate distinctions.

Conceptual documents must distinguish original synthesis from established techniques and identify dependencies on prior work where known.

### Layer B — Reference implementation

The public repository is the inspectable implementation substrate. A cloneable implementation should be accompanied by enough configuration and documentation to reproduce the claimed repository-local behavior.

Implementation existence is not evidence of real-world efficacy or historical firstness.

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
| Historical provenance | A formulation is documented at a dated point | Name the exact source/date; do not infer firstness |
| Historical prior-art adjudication | A predecessor/composition has been compared | State the comparison universe and limitations |
| Hypothesis | A prediction or possible distinction awaiting stronger testing/comparison | Use conditional language |
| Unsupported | Evidence is absent or inadequate | Do not promote as a result |

Repository-wide adjectives such as “proven,” “validated,” “unique,” “first,” or “production-ready” must not be inferred from component-level evidence.

## 4. Canonical publication sequence

1. **Canonical technical overview** — problem, architecture, terminology, contribution boundaries.
2. **Versioned specification** — stable definitions/interfaces with changelog/provenance.
3. **Reproducibility packet** — dependencies, test commands, expected outputs, known limitations.
4. **Related-work/prior-art record** — dated primary-source comparison that separates primitives from architecture-level composition.
5. **Experimental paper or technical report** — only after protocol/evidence support the empirical claims made.
6. **Independent comparison and replication** — publish favorable, null, and unfavorable results under the same evidence policy.

The first four stages can proceed before empirical authorization. Stage five must not imply empirical findings that do not yet exist.

## 5. Priority and prior-art discipline

Prior-art review must compare both mechanisms and the **governed object/lifecycle**. The current review establishes substantial external prior art for multi-agent formation, organizational authority, governance gates, veto/escalation, idempotency, provenance, exact artifact identity, and independent verification.

The remaining historical question is narrower: whether an earlier public system implemented a materially equivalent cross-domain lifecycle coupling formation governance to candidate-bound experimental verification and authorization.

Use calibrated conclusions:

- “publicly documented by” is a provenance claim;
- “external prior” is a source-level adjudication;
- “near-composition prior” means major components overlap but the governed object or lifecycle differs;
- “potentially distinctive integration” means no equivalent predecessor has been located in the bounded review;
- none of these phrases establishes global firstness.

See `research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md` for the current adjudication baseline.

## 6. Recommended external-facing artifacts

### Immediate

- Repository landing page with problem statement and evidence boundary.
- `CITATION.cff` or equivalent citation metadata.
- Versioned release notes for meaningful milestones.
- Related-work/prior-art record with stable primary-source references.
- This publication/provenance spine linked from the documentation index.

### After candidate freeze and pilot authorization

- Archived protocol and freeze manifest.
- Reproducibility instructions tied to exact candidate SHA.
- Results report containing pre-specified analyses and complete result accounting.

### After evidence matures

- Formal technical white paper or preprint with related-work review and claim/evidence mapping.
- Independent replication package and comparative baseline results where feasible.

## 7. Authorship and provenance

The repository's provenance identifies Ndr / Ender Hensel (`ndrorchestration`) as developer. Public attribution should identify contribution roles precisely and preserve commit/release history rather than converting repository authorship into unsupported claims of sole conceptual priority.

For collaborative work, record authorship, contribution roles, review boundaries, and AI assistance where materially relevant to interpretation or reproducibility.

## 8. Publication quality gate

A public artifact is publication-ready when it answers:

1. What exactly is being proposed or claimed?
2. What problem and scope does it address?
3. What is implemented versus hypothesized?
4. What evidence supports each important claim?
5. What would falsify, narrow, or revise the claim?
6. How can another party inspect or reproduce the relevant behavior?
7. What prior work or adjacent concepts overlap?
8. What remains unknown?
9. Is any historical-priority language supported by a bounded, dated primary-source review?

Failure to answer one of these questions should result in narrowing the artifact's claims, not filling the gap with confidence language.

## 9. Current DGAF publication boundary

The public record supports publication of DGAF as an **open research and implementation framework for agent orchestration, formation governance, evaluation, provenance, and explicit claim/evidence management**.

The record does **not** support presenting DGAF as first in the individual mechanisms of agent governance, dynamic formation, authority, veto, escalation, idempotency, provenance, exact artifact identity, or independent verification.

A narrower architecture-level hypothesis remains under review: DGAF may have independently coupled formation-state governance with candidate-bound experimental evidence, verification, and authorization. This remains conditional on completion of a broader cross-domain prior-art comparison.

The current PDMAL research track remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.

## Cross-references

- [`../README.md`](../README.md)
- [`CLAIM_EVIDENCE_INDEX.md`](CLAIM_EVIDENCE_INDEX.md)
- [`CURRENT_STATE.md`](CURRENT_STATE.md)
- [`DGAF_RELATED_WORK_MATRIX.md`](DGAF_RELATED_WORK_MATRIX.md)
- [`research/DGAF_RELATED_WORK_SOURCE_ADJUDICATION.md`](research/DGAF_RELATED_WORK_SOURCE_ADJUDICATION.md)
- [`research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`](research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md)
- [`PRIOR_ART_AND_RELATED_WORK_SCOPE.md`](PRIOR_ART_AND_RELATED_WORK_SCOPE.md)
- [`PATTERN_COMMONS_ARCHITECTURE.md`](PATTERN_COMMONS_ARCHITECTURE.md)
- [`experiment/PDMAL_CURRENT_CONTROL_STATE.md`](experiment/PDMAL_CURRENT_CONTROL_STATE.md)
- [`experiment/PDMAL_EXPERIMENT_PROTOCOL.md`](experiment/PDMAL_EXPERIMENT_PROTOCOL.md)
- [`DGAF_EVIDENCE_AND_RELEASE_POLICY.md`](DGAF_EVIDENCE_AND_RELEASE_POLICY.md)
