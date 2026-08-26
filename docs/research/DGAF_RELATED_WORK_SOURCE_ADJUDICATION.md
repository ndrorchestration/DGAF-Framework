# DGAF Related-Work Source Adjudication

**Status:** Preliminary source-level adjudication; not a novelty determination  
**Date:** 2026-08-25  
**Purpose:** Compare concrete prior work against DGAF mechanisms and identify where overlap is established, where distinctions are plausible, and where further review is required.

## Method

This document applies the mechanism-level comparison rule in the publication and provenance spine. A source is not treated as equivalent merely because it uses terms such as *governance*, *orchestration*, or *provenance*.

Comparison dimensions:

1. orchestration architecture;
2. runtime control/enforcement;
3. evaluation and verification;
4. provenance and evidence custody;
5. claim/evidence discipline;
6. reproducibility and experimental governance.

Classifications are **overlap**, **partial overlap**, **candidate distinction**, or **unresolved**. Candidate distinctions are hypotheses for review, not novelty claims.

## Source adjudications

### A. Trace-based assurance for agentic orchestration (Paduraru, Bouruc, Stefanescu, 2026)

**Established overlap:** Multi-agent orchestration, runtime governance, machine-checkable contracts, deterministic replay, fault injection, and reproducible comparison are explicitly addressed.

**DGAF implication:** DGAF must not claim that combining orchestration with governance, testing, or traceability is itself novel.

**Candidate distinction:** DGAF's repository-level epistemic controls and explicit lifecycle linking of public claims to claim-specific evidence may represent a different layer from trace instrumentation, but this requires direct artifact comparison.

**Status:** Strong overlap; distinction unresolved.

### B. Evaluation and regulation survey for agentic AI (Farooq et al., 2026)

**Established overlap:** Evaluation, governance, reliability, transparency, auditable systems, and multi-agent coordination are established research concerns.

**DGAF implication:** The problem space is independently recognized; broad claims that DGAF uniquely identifies these needs would be unsupported.

**Candidate distinction:** DGAF operationalizes an internal claim/evidence ladder and repository gate structure alongside implementation artifacts. Whether this operational integration is distinctive requires comparison with concrete governance frameworks.

**Status:** Broad conceptual overlap; implementation distinction unresolved.

### C. Runtime action-boundary governance (Mazzocchetti, 2026)

**Established overlap:** Trusted action mediation, provenance, fail-closed execution, and non-unilateral authorization are concrete runtime-governance mechanisms already articulated and evaluated in a sandbox.

**DGAF implication:** These mechanisms cannot be represented as newly invented by DGAF without narrower, mechanism-specific evidence.

**Candidate distinction:** DGAF's contribution, if any, must be sought in architecture, evidence governance, or orchestration integration rather than generic action-boundary control.

**Status:** Strong overlap in runtime-governance direction.

### D. Validation beyond component testing (Mirto et al., 2026)

**Established overlap:** Trajectory-level validation, runtime evidence, multi-agent assurance, bounded autonomy, and audit-ready evidence structures are active cross-domain research directions.

**DGAF implication:** The distinction between component tests and system-level evidence is not unique to DGAF.

**Candidate distinction:** DGAF's concrete evidence-state vocabulary and propagation controls may be an implementation-specific contribution, pending source and implementation comparison.

**Status:** Conceptual overlap; mechanism-level distinction unresolved.

### E. TRiSM review for agentic multi-agent systems (2026)

**Established overlap:** Trust, risk, security, governance, provenance, explainability, lifecycle controls, and multi-agent coordination have a substantial existing literature.

**DGAF implication:** A general "governed multi-agent framework" is insufficiently specific as a contribution claim.

**Candidate distinction:** A reproducible governance/evidence substrate spanning code, experimental protocols, and public claim discipline remains a narrower candidate formulation to investigate.

**Status:** Broad overlap; candidate synthesis distinction.

## Provisional contribution statement

The evidence currently supports describing DGAF as an **open research and implementation framework that integrates agent orchestration, governance controls, evaluation, provenance, and explicit claim/evidence management**.

The following statement is a **research hypothesis**, not an established novelty claim:

> DGAF may provide a distinctive integration in which epistemic status and evidence requirements are treated as operational governance concerns across repository artifacts, implementation controls, and experimental decision gates rather than solely as documentation or post hoc reporting.

This statement must be narrowed, revised, or rejected as the source review expands.

## Explicit non-claims

This review does not establish that DGAF is:

- the first governance framework for agentic AI;
- the first multi-agent orchestration framework;
- the first system to provide runtime assurance or provenance;
- empirically better than alternative approaches;
- novel in an absolute sense.

## Research questions opened by the adjudication

1. Which DGAF controls are technically executable rather than documentary?
2. Which controls link claim language to machine-checkable evidence or gates?
3. Do comparable systems provide an equivalent end-to-end evidence lifecycle?
4. Is the integration reproducibly useful, or merely a collection of existing practices?
5. What measurable outcome would distinguish DGAF from a conventional orchestration-plus-testing stack?

A defensible contribution requires answers grounded in artifacts and comparative evidence, not architectural description alone.

## Next actions

1. Expand the bibliography with primary sources and standards.
2. Inspect implementation-level mechanisms for the strongest comparators.
3. Produce a feature/claim comparison matrix with citations.
4. Define falsifiable comparative hypotheses for DGAF and PDMAL separately.
5. Keep conceptual publication claims independent from the pending PDMAL empirical program.

## Cross-references

- [`PUBLICATION_AND_PROVENANCE_SPINE.md`](../PUBLICATION_AND_PROVENANCE_SPINE.md)
- [`DGAF_RELATED_WORK_MATRIX.md`](DGAF_RELATED_WORK_MATRIX.md)
- [`CLAIM_EVIDENCE_INDEX.md`](../CLAIM_EVIDENCE_INDEX.md)
- [`EPISTEMIC_EVIDENCE_STANDARD.md`](../EPISTEMIC_EVIDENCE_STANDARD.md)
