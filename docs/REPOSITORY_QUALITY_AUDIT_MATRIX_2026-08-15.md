# Repository Quality Audit Matrix — 2026-08-15

## Purpose

Operational matrix for the repository-normalization phase. This is an engineering audit index, not a production-readiness certification.

The audit distinguishes repository metadata from evidence about implementation. `UNKNOWN` means the current pass has not inspected enough evidence to classify the property; it does not mean the property is absent.

## Evidence ladder

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

Cross-repository relationships never transfer validation status.

## Initial inventory

29 repositories were enumerated from the live `ndrorchestration` account on 2026-08-15.

| Repository | Visibility | Role / class | README boundary | Code/test audit | CI audit | Runtime audit | Security/provenance | Priority |
|---|---|---|---|---|---|---|---|---|
| `DGAF-Framework` | Public | Governance/evaluation research spine | VERIFIED | IN PROGRESS | IN PROGRESS | N/A / research | IN PROGRESS | P1 |
| `ai-governance-frameworks` | Public | Governance research/mapping | VERIFIED | UNKNOWN | UNKNOWN | N/A | UNKNOWN | P2 |
| `Driftwatch` | Public | Drift detection/evaluation engineering | VERIFIED | IN PROGRESS | UNKNOWN | UNKNOWN | IN PROGRESS | P1 |
| `resumeapex-eval` | Public | Evaluation protocol/benchmark | VERIFIED | UNKNOWN | UNKNOWN | N/A | UNKNOWN | P1 |
| `junior-apogee-app` | Public | Evaluation/QA workbench | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P1 |
| `sentinel-governance` | Public | Integrity/CI governance | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P1 |
| `Acoustic-mesh` | Public | Acoustic/WebRTC engineering | VERIFIED | IN PROGRESS | UNKNOWN | UNKNOWN | IN PROGRESS | P1 |
| `Meshsense` | Public | MeshSense/RuView runtime/status surface | VERIFIED | UNKNOWN | UNKNOWN | PENDING | UNKNOWN | P1 |
| `3d-visualization-hub` | Public | Visualization | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |
| `ai-prompt-systems-portfolio` | Public | Public prompt-systems portfolio | VERIFIED | UNKNOWN | UNKNOWN | N/A | UNKNOWN | P2 |
| `aoga-dashboard` | Private | Production dashboard/API | VERIFIED | UNKNOWN | UNKNOWN | PARTIAL | IN PROGRESS | P1 |
| `phi-calculus-app` | Public | Mathematical research/application | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P1 |
| `AHG-Zeta-Pell-Autonomous-Lattice` | Public | Control/simulation research | VERIFIED | IN PROGRESS | UNKNOWN | N/A | IN PROGRESS | P1 |
| `agent-control-plane` | Public | Control-plane architecture | VERIFIED | VERIFIED PARTIAL | VERIFIED PARTIAL | N/A | IN PROGRESS | P1 |
| `entrepreneur-hub` | Public | Business/template track | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |
| `ndrorchestration` | Public | Canonical portfolio/control surface | VERIFIED | IN PROGRESS | UNKNOWN | N/A | IN PROGRESS | P1 |
| `AI-Prompt-Engineer` | Private | Historical portfolio | HISTORICAL | NOT TARGETED | NOT TARGETED | N/A | UNKNOWN | P3 |
| `ai-prompt-engineering-portfolio` | Private | Historical portfolio | HISTORICAL | NOT TARGETED | NOT TARGETED | N/A | UNKNOWN | P3 |
| `prompt-optimization-library` | Private | Historical/research library | UNKNOWN | UNKNOWN | UNKNOWN | N/A | UNKNOWN | P3 |
| `gold-star-qa-framework` | Private / archived | Archived framework | HISTORICAL | NOT TARGETED | NOT TARGETED | N/A | UNKNOWN | P3 |
| `Gold-star-standards` | Private | Standards/archive support | VERIFIED | UNKNOWN | UNKNOWN | N/A | UNKNOWN | P3 |
| `Amethyst-Governance-Eval-Stack` | Private | Governance/evaluation stack | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |
| `.github` | Public | Account-wide GitHub configuration | UNKNOWN | UNKNOWN | UNKNOWN | N/A | UNKNOWN | P2 |
| `chat-archives` | Private | Archive | UNKNOWN | NOT TARGETED | NOT TARGETED | N/A | UNKNOWN | P3 |
| `career-positioning` | Private | Career/portfolio support | UNKNOWN | NOT TARGETED | NOT TARGETED | N/A | UNKNOWN | P3 |
| `automation-scripts` | Private | Automation support | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |
| `api` | Private | API support surface | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |
| `aoga-dashboard` | Private | Production dashboard/API | VERIFIED | UNKNOWN | UNKNOWN | PARTIAL | IN PROGRESS | P1 |
| `pptl-governance-dashboard` | Private | Governance dashboard | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |
| `dgaf-ops` | Private | DGAF operations/support | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |

## Inventory correction

The repository list above is the live account inventory, but duplicate `aoga-dashboard` rows are not intended. The canonical matrix entry is the first `aoga-dashboard` row; the later duplicate is retained only as a detection note and must be removed in the next matrix edit.

## Detailed evidence established in this pass

### DGAF-Framework

The README now explicitly limits claims to repository-local evidence and separates DGAF, PDMAL, Acoustic-Mesh, and other tracks. The repository also contains an ecosystem audit status document and synchronization records. Current audit work is therefore moving from terminology correction into implementation/test/CI verification.

### Agent Control Plane

The repository contains a minimal executable kernel, unit tests, and GitHub Actions CI. Its quality baseline identifies dependency reproducibility, security/coverage gates, broader failure-mode tests, and integration tests as current gaps. This makes ACP a useful reference implementation for the normalization standard rather than a completed production control plane.

### Driftwatch

The repository has a lockfile, but the lockfile root metadata currently identifies the package as `react-example`/`0.0.0` while `package.json` identifies it as `driftwatch`/`0.1.0`. This is a concrete reproducibility/provenance inconsistency requiring correction. The package scripts expose build and TypeScript checking, but a test script is not currently declared in `package.json`.

### Acoustic-Mesh

The README correctly limits claims to acoustic/WebRTC engineering and explicitly rejects unsupported physical-performance guarantees. The next evidence pass must inspect actual signal-processing implementation, WebRTC behavior, tests, instrumentation, and any retained acoustic measurements.

### AHG-Zeta-Pell-Autonomous-Lattice

Pass 1 is documented and correctly quarantines historical benchmark claims. Pass 2 remains outstanding for the chaos/FML mitigation section, Three-Regime Governor, recovery trace, and assembled documentation.

### Meshsense

The canonical GitHub repository is `ndrorchestration/Meshsense`. The associated Vercel project remains `meshsense-ruview-status`. GitHub/CI evidence is documented as verified; Vercel deployment/runtime verification remains pending.

## Immediate P1 actions

1. Remove the duplicate `aoga-dashboard` row in this matrix.
2. Complete code/test/CI inspection for `DGAF-Framework`, `Driftwatch`, `Acoustic-mesh`, `AHG-Zeta-Pell-Autonomous-Lattice`, `Meshsense`, and `agent-control-plane`.
3. Correct Driftwatch lockfile package identity before treating dependency reproducibility as clean.
4. Establish runtime evidence for Meshsense/RuView.
5. Complete AHG Zeta-Pell Pass 2.
6. Audit PDMAL implementation and empirical harness evidence.
7. Audit non-README documentation for inherited unsupported claims.
8. Add security/provenance checks to the quality baseline where repository technology makes them applicable.

## Normalization rule

A repository does not receive a higher evidence status because its README, benchmark table, generated report, deployment label, or another repository says that it is verified. Each claim must point to an inspectable implementation, method, test, trace, benchmark, or external attestation appropriate to the claim.

*Created 2026-08-15 during the repository quality normalization pass.*
