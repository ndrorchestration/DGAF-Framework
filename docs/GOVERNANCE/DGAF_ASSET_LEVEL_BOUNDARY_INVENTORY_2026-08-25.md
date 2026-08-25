# DGAF Ecosystem Asset-Level Boundary Inventory — 2026-08-25

**Status:** PRELIMINARY GOVERNANCE INVENTORY v0.2  
**Purpose:** Repository- and selected path-level asset boundary triage across the accessible `ndrorchestration` GitHub ecosystem, separating access classification from epistemic status and identifying assets requiring deeper provenance/IP/security review.

> This inventory is a governance control, not a legal opinion and not an assertion that private material is proprietary. Repository visibility is an access property. Epistemic status, provenance, licensing, security sensitivity, and commercial differentiation are independently assessed.

## Confirmed path-level findings

### A. AOGA Dashboard

`aoga-dashboard` explicitly labels its implementation boundary **PRIVATE — proprietary AOGA implementation** and exposes a production-deployed serverless API surface. Its README separately states that deployment and endpoint availability do not establish correctness, safety, evaluation quality, or end-to-end runtime behavior.

Decision:

- **Boundary:** PROPRIETARY / COMMERCIAL CANDIDATE.
- **Epistemic status:** IMPLEMENTED/DEPLOYED for the documented API surface; evaluation claims remain separately bounded.
- **Reproducibility:** public DGAF claims must not depend on undisclosed AOGA internals unless the claim is specifically about the private product.
- **Security review required:** authentication, secrets, upstream service exposure, and deployment configuration.
- **Commercial differentiation remains unproven:** the private boundary is established, but the specific implementation choices that create durable customer value still need to be isolated.

### B. Amethyst Governance Eval Stack

Selected path inspection shows that major directories are still scaffolds rather than mature hidden mechanisms:

- `guardrails/README.md`: **Scaffold — content pending Sprint 1**.
- `eval_stack/protocols/README.md`: **Scaffold — content pending Sprint 1**.
- `eval_stack/tiers/README.md`: describes project-local Bronze/Silver/Gold/Autodiagnostic thresholds, including certification-like terminology, but the repository README explicitly states these are not external certifications.

Decision:

- **Boundary:** PRIVATE / RESEARCH; do not classify as proprietary solely because it is private.
- **Epistemic status:** substantial content is DEFINED/PLANNED rather than IMPLEMENTED.
- **Commercial value:** presently unproven at the mechanism level.
- **Terminology control:** certification-like labels must remain explicitly project-local until independently defensible.

### C. Gold Star Standards

`Gold-star-standards` identifies itself as an internal evaluation/rubric repository. It contains project-defined standards, evaluation criteria, benchmark definitions, and process standards and explicitly states that internal tier labels are not third-party certification.

Decision:

- **Boundary:** PRIVATE / RESEARCH.
- **Epistemic status:** DEFINED/EXPERIMENTAL, with individual metrics requiring source and derivation evidence.
- **Pattern Commons:** general governance concepts should remain candidates for provenance/commons analysis instead of being presumed proprietary.
- **Commercial decision:** unresolved until concept → mechanism → implementation → evidence → customer value is mapped.

### D. `dgaf-ops`

The repository contains operational sweep history, session snapshots, agent formation/manifests, boot protocol, live co-orchestration protocol and queue state, milestone reports, and deployment configuration.

Decision:

- **Boundary:** PRIVATE / OPERATIONAL.
- **Security/privacy:** potentially high depending on specific deployment/session contents.
- **Commercial differentiation:** plausible but not established.
- **Public-evidence rule:** public DGAF reproducibility must not silently depend on this repository.

## Public evidence boundary

`DGAF-Framework` remains deliberately evidence-preserving and states that the public reference implementation should be sufficiently complete for independent cloning, inspection, execution, and evaluation. Its current experimental state remains PRE-FREEZE with no new freeze, no pilot authorization, and empirical N = 0.

`evidence/PDMAL_LATTICE_CORRECTIONS_2026-08-15.md` documents corrected constants and reproducible computations while explicitly excluding stronger claims such as general convergence, global contraction, production performance, security, baseline superiority, or a valid operational Forman-Ricci signal on the current unweighted graph. Those artifacts remain OPEN / REPRODUCIBILITY.

## Repository-level inventory remains valid

The connected GitHub inventory returned **32 repositories** for `ndrorchestration`: **18 public** and **14 private**. Repository visibility is treated as an access property only.

The priority classes remain:

- **OPEN / RESEARCH:** DGAF evidence, public harnesses, public protocols, public tests, public governance mappings, public portfolio examples.
- **PRIVATE / RESEARCH:** Gold Star Standards and most of Amethyst Eval Stack until implementation maturity and commercial differentiation are demonstrated.
- **PROPRIETARY / COMMERCIAL CANDIDATE:** AOGA implementation and selected future product/service components.
- **PRIVATE / OPERATIONAL:** `dgaf-ops`, private automation, service/API internals.
- **PRIVATE / CONFIDENTIAL:** chat archives and personal operational material.
- **THIRD-PARTY / PROVENANCE REVIEW:** `unsloth` until upstream/licensing/local-modification status is established.

## Deep-review queue

1. `DGAF-Framework` — path-level evidence, schemas, harnesses, protocol, registries, patterns.
2. `aoga-dashboard` — implementation, deployment, interfaces, and security boundaries.
3. `dgaf-ops` — operational internals and deployment/session material.
4. `Amethyst-Governance-Eval-Stack` — reusable mechanisms after separating scaffolds from implemented code.
5. Private prompt archives — methodology lineage and candidate differentiators.
6. `automation-scripts` and `api` — security-sensitive operational capabilities.
7. `Gold-star-standards` — concept/mechanism/evidence separation.
8. `entrepreneur-hub` — public service packaging versus private delivery assets.
9. `unsloth` — provenance, license, upstream relationship, and local modifications.

## Candidate-proprietary decision gates

Every candidate must independently establish:

- **Reproducibility:** whether public access is required for a public claim.
- **Commercial differentiation:** whether withholding creates legitimate product/service differentiation.
- **Security/privacy:** whether disclosure creates material risk.
- **IP/provenance:** independent authorship and compatible licensing/provenance.
- **Epistemic maturity:** claims actually supported by evidence.

**Access classification and epistemic classification remain orthogonal.** The target state is evidence-preserving openness with legitimate controlled boundaries.

**Inventory status:** Repository triage plus selected path-level review completed. Further deep file-level classification remains open for the prioritized queue.
