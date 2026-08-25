# DGAF Ecosystem Asset-Level Boundary Inventory — 2026-08-25

**Status:** PRELIMINARY GOVERNANCE INVENTORY v0.1  
**Purpose:** Repository-level asset boundary triage across the accessible `ndrorchestration` GitHub ecosystem, separating access classification from epistemic status and identifying assets requiring file-level provenance/IP/security review.

> This inventory is a governance control, not a legal opinion and not an assertion that private material is proprietary. Repository visibility is an access property. Epistemic status, provenance, licensing, security sensitivity, and commercial differentiation are independently assessed.

## Boundary model

Every asset is evaluated on independent dimensions:

1. **Asset Boundary Class** — OPEN / RESEARCH-EXPERIMENTAL / PROPRIETARY-COMMERCIAL / PRIVATE-CONFIDENTIAL / SECURITY-SENSITIVE / TRADEMARK-CERTIFICATION-GOVERNED.
2. **Epistemic Status** — DEFINED / IMPLEMENTED / COMPUTED / VERIFIED / ATTESTED / HISTORICAL / HYPOTHESIS / METAPHOR / UNSUPPORTED / DEPRECATED.
3. **Functional Role** — implementation, evidence, research instrument, portfolio/demo, operations, archive, service packaging, etc.
4. **Public-Reproducibility Requirement** — whether withholding would prevent an independent user from reproducing or evaluating a public claim.
5. **Security/Privacy Sensitivity** — whether disclosure itself creates material risk.
6. **Commercial Role** — whether the asset is evidence, adoption surface, service-enablement, operational differentiation, or a candidate proprietary capability.
7. **License Constraint** — actual repository/file license and provenance, not inferred from visibility.
8. **Trademark/Certification Role** — whether the asset can create implied officiality or certification claims.

No single dimension controls the others.

## Current ecosystem coverage

The connected GitHub inventory returned **32 repositories** for `ndrorchestration`: **18 public** and **14 private**. This is the current repository-level survey surface available to the connected GitHub account; it is not a claim that every file inside each repository has been classified.

## Repository-level triage

| Repository | Access | Preliminary boundary | Epistemic / lifecycle | Functional role | Public reproducibility | Commercial role | Immediate review |
|---|---|---|---|---|---|---|---|
| `DGAF-Framework` | Public | OPEN + RESEARCH | PRE-FREEZE; mixed evidence states | Governance/evaluation substrate | **Required** | Credibility/adoption substrate; services around it | **Deep file review** |
| `ai-governance-frameworks` | Public | OPEN + RESEARCH | Experimental | Governance mappings/templates | Required for public mapping claims | Adoption/service enablement | File/license review |
| `ai-prompt-systems-portfolio` | Public | OPEN | Active WIP; mixed artifact maturity | IP-safe public portfolio | Required for portfolio examples | Recruiter/adoption/lead generation | Confirm per-artifact provenance |
| `3d-visualization-hub` | Public | OPEN + RESEARCH | Project-dependent | Visualization utility/research | Required for public demos | Demo/service enablement | License/content provenance |
| `junior-apogee-app` | Public | OPEN + RESEARCH | Experimental/application | Evaluation application | Required for claims about public app | Product/demo/service enablement | File-level IP scan |
| `phi-calculus-app` | Public | OPEN + RESEARCH | Research instrument | Mathematical/research application | Required where used as public evidence | Primarily credibility/adoption | Validate claims and provenance |
| `sentinel-governance` | Public | OPEN + RESEARCH | Governance/CI track | Guardrail/integrity tooling | Required for public control claims | Possible service integration | Security + license review |
| `resumeapex-eval` | Public | OPEN + RESEARCH | Experimental | Evaluation benchmark/protocol | Required | Benchmark/service enablement | Dataset/provenance review |
| `Driftwatch` | Public | OPEN + RESEARCH | Active experimental | Drift detection/evaluation instrument | Required | Service/integration candidate | Calibration/evidence review |
| `.github` | Public | OPEN | Operational metadata | Org/repository templates | Not a scientific dependency | Ecosystem adoption | Low priority |
| `Acoustic-mesh` | Public | OPEN + RESEARCH | Research/application | Spatial/acoustic intelligence | Required for public research claims | Future product research | IP/provenance + hardware/data review |
| `ndrorchestration` | Public | OPEN | Portfolio/index | Public ecosystem map | Useful for discovery | Lead generation | Keep synchronized |
| `agent-control-plane` | Public | OPEN + RESEARCH | Experimental; minimal kernel implemented | Reusable orchestration/control infrastructure | **Required** for public capability claims | Service/integration enablement | License + architecture review |
| `AHG-Zeta-Pell-Autonomous-Lattice` | Public | OPEN + RESEARCH | Research/hypothesis unless evidenced | Mathematical/structural research | Required for public research claims | Credibility/adoption | Evidence/provenance review |
| `Meshsense` | Public | OPEN + RESEARCH | Experimental | Runtime/deployment observation simulation | Required for public claims | Service/demo enablement | License + claim review |
| `orbit-everyday` | Public | OPEN | Application/utility | Separate product/app track | Depends on claims | Potentially commercial app surface | Scope isolation |
| `unsloth` | Public | THIRD-PARTY / DERIVATIVE / PROVENANCE-REVIEW | External dependency/mirror status to be established | External codebase reference | Not a DGAF evidence asset | Not owned differentiator | **High provenance/license review before reuse/branding** |
| `AI-Prompt-Engineer` | Private | PRIVATE / ARCHIVE | Historical archive | Prompt portfolio lineage | Not required; public lineage already separated | IP/provenance archive | File/IP lineage review |
| `ai-prompt-engineering-portfolio` | Private | PRIVATE / ARCHIVE | Historical archive | Benchmark/submission/IP archive | Not required for current public portfolio | Provenance/IP record | Preserve; do not silently publish |
| `gold-star-qa-framework` | Private / archived | PRIVATE / RETIRED | Archived | Legacy QA framework | Not required | Historical lineage only unless extracted intentionally | Archive/provenance review |
| `chat-archives` | Private | PRIVATE / CONFIDENTIAL | Historical conversation records | Source/provenance material | **Not required** | No commercial publication by default | **Privacy review** |
| `prompt-optimization-library` | Private | PRIVATE / ARCHIVE | Historical v0 baseline | Prompt optimization archive | Not required for current public implementation | Potential methodology/IP lineage | File-level IP audit |
| `Gold-star-standards` | Private | PRIVATE / RESEARCH | Project-local standards/rubrics | Evaluation/rubric material | Some concepts may belong in Pattern Commons | Candidate methodology asset; not yet shown proprietary | Separate concept/mechanism/evidence review |
| `Amethyst-Governance-Eval-Stack` | Private | PRIVATE / RESEARCH-COMMERCIAL CANDIDATE | Active experimental | Evaluation/orchestration stack | Public reproduction dependency not yet established | Candidate specialized tooling/integration | **Deep IP + license review** |
| `career-positioning` | Private | PRIVATE / OPERATIONAL | Current operational | Career/job strategy | None | Personal operations | Keep private |
| `automation-scripts` | Private | PRIVATE / OPERATIONAL; potentially SECURITY-SENSITIVE | Utility scripts | Workflow/CI automation | Not normally required | Operational differentiation if independently developed | **Secret/access/security scan** |
| `api` | Private | PRIVATE / OPERATIONAL; potentially SECURITY-SENSITIVE | Current implementation unknown from metadata alone | API/service layer | Depends on public claims | Potential managed-service boundary | **Highest-priority technical review** |
| `aoga-dashboard` | Private | PROPRIETARY / COMMERCIAL CANDIDATE | Deployed implementation; claims independently bounded | Private AOGA implementation | Public evidence must not depend on undisclosed essentials | **Direct product/service differentiation candidate** | **Highest-priority IP + security review** |
| `pptl-governance-dashboard` | Private | PRIVATE / COMMERCIAL CANDIDATE | Implementation status requires artifact review | Governance dashboard | Public reproducibility dependency TBD | Product/managed-service candidate | Deep review |
| `entrepreneur-hub` | Public | OPEN + COMMERCIAL SERVICE PACKAGING | Active project/business plan | Public templates + service packaging | Core public template content should remain reproducible | **Primary service/revenue surface** | Separate public templates from private customer data/operations |
| `dgaf-ops` | Private | PRIVATE / OPERATIONAL; potentially PROPRIETARY | Live operational internals | Sessions, formation, deployment state | Must not be required to clone public DGAF | **Operational differentiation candidate** | Deep operational/IP/security review |

## Confirmed high-value boundary findings

### 1. DGAF public evidence is intentionally an adoption asset

`DGAF-Framework` explicitly states that the public reference implementation should be sufficiently complete for independent cloning, inspection, execution, and evaluation. Its current status remains PRE-FREEZE with no new experimental freeze, no pilot authorization, and empirical N = 0. These facts make the public evidence layer a credibility asset rather than material that should be hidden merely because it is sophisticated.

### 2. PDMAL correction artifacts belong in the public evidence layer

`evidence/PDMAL_LATTICE_CORRECTIONS_2026-08-15.md` records corrected constants and reproducible computations while explicitly denying stronger claims such as general convergence, global contraction, production performance, security, baseline superiority, or a valid operational Forman-Ricci signal on the current unweighted graph. It therefore belongs with public reproducibility/evidence rather than inside a commercial boundary.

The documented results include the corrected plastic constant, the dodecahedral graph properties, `h(G)=0.6`, uniform unweighted Forman-Ricci `-2`, and the explicit statement that contraction monitoring is only an empirical local proxy.

### 3. AOGA is the clearest currently identified proprietary implementation candidate

The private `aoga-dashboard` README explicitly labels its IP boundary **PRIVATE — proprietary AOGA implementation** while separately acknowledging that deployment and endpoint availability do not establish correctness, safety, evaluation quality, or end-to-end runtime behavior. This is a useful model for maintaining a commercial implementation boundary without allowing proprietary status to become an evidence shortcut.

### 4. `dgaf-ops` is operationally private, not automatically proprietary

The private operations repository contains session state, agent formation/manifests, live co-orchestration state, deployment configuration, and operational sweep history. Those are appropriately private by default. Whether any component represents durable commercial differentiation remains a separate IP/provenance assessment.

### 5. Entrepreneur Hub demonstrates the preferred commercialization pattern

`entrepreneur-hub` is public but packages paid services, templates, retainers, and licensing as offerings. This supports the strategic model in which public evidence and public examples remain inspectable while revenue is generated through services, implementation, support, managed operations, and appropriately controlled commercial offerings.

### 6. Private prompt archives are primarily provenance/IP records

`AI-Prompt-Engineer`, `ai-prompt-engineering-portfolio`, and `prompt-optimization-library` are explicitly described as historical/private archives. Their private status should not be interpreted as proof that the underlying concepts are proprietary. Any candidate methodology must still pass provenance, independent authorship, license, and commercial-differentiation review.

## PDMAL-specific inventory decision

The following are **OPEN / REPRODUCIBILITY** unless later evidence establishes a legitimate confidentiality or security boundary:

- corrected lattice formalization;
- `lattice_harness.py` and equivalent public reproducibility harness material;
- reproducibility/evidence notes documenting corrections and negative findings;
- experimental protocol definitions needed to reproduce public claims;
- public tests and schemas necessary to evaluate the reference implementation.

The following are **not** automatically evidence assets merely because they relate to PDMAL:

- private operational state;
- credentials, secrets, or deployment material;
- customer/private telemetry;
- future commercial service tooling;
- unpublished implementation accelerators.

## Asset-level deep-review queue

The next pass should move from repository-level triage to exact file/path classification for:

1. `DGAF-Framework` — evidence, schemas, harnesses, protocol, registries, patterns, and commercial-boundary documents.
2. `aoga-dashboard` — proprietary implementation, deployment code, interfaces, and exposed endpoint assumptions.
3. `dgaf-ops` — operational internals, formation protocols, deployment manifests, and session/state records.
4. `Amethyst-Governance-Eval-Stack` — protocols, guardrails, tier definitions, thresholds, and reusable mechanisms.
5. Private prompt archives — methodology lineage and candidate differentiators.
6. `automation-scripts` and `api` — security-sensitive operational capabilities and access boundaries.
7. `Gold-star-standards` — concept/mechanism/evidence separation before deciding whether patterns belong in Pattern Commons.
8. `entrepreneur-hub` — identify which artifacts are public service packaging versus future private delivery assets.
9. `unsloth` — establish provenance, upstream relationship, license obligations, and whether any local modifications exist before treating it as part of the owned ecosystem.

## Required decision gates for every candidate proprietary asset

An asset should not be marked PROPRIETARY merely because it is private or commercially interesting. The evidence record should establish:

- **Reproducibility:** whether public access is required to reproduce a stated public claim.
- **Commercial differentiation:** whether withholding creates legitimate product/service differentiation rather than artificial scarcity.
- **Security/privacy:** whether disclosure creates material risk.
- **IP/provenance:** whether the asset is independently authored, properly licensed, and free of third-party restrictions inconsistent with the intended boundary.
- **Epistemic maturity:** what claims the asset can honestly support.

## Governance rule

**Access classification and epistemic classification remain orthogonal.** A private asset can be weakly supported. A public asset can contain strong evidence. A proprietary implementation can coexist with an open reproducibility harness. A public research artifact can still contain security-sensitive sub-assets requiring controlled disclosure.

The goal is not maximal openness or maximal secrecy. The goal is **evidence-preserving openness with legitimate controlled boundaries**.

## Evidence references

- `README.md` — current DGAF project state, licensing, evidence boundary, and commercialization posture.
- `CROSS_REF.md` — cross-repository and Pattern Commons boundaries.
- `docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md` — decision framework and commercial boundary.
- `evidence/PDMAL_LATTICE_CORRECTIONS_2026-08-15.md` — corrected PDMAL evidence boundary.
- Related repository READMEs reviewed during this inventory pass, including `Driftwatch`, `agent-control-plane`, `ai-prompt-systems-portfolio`, `ai-prompt-engineering-portfolio`, `prompt-optimization-library`, `ai-governance-frameworks`, `resumeapex-eval`, `Amethyst-Governance-Eval-Stack`, `aoga-dashboard`, `entrepreneur-hub`, `automation-scripts`, and `dgaf-ops`.

**Inventory status:** Repository-level pass completed. File-level classification remains open for the deep-review queue above.
