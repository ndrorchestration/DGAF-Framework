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
| `DGAF-Framework` | Public | Governance/evaluation research spine | VERIFIED | IN PROGRESS | VERIFIED PARTIAL | N/A / research | IN PROGRESS | P1 |
| `ai-governance-frameworks` | Public | Governance research/mapping | VERIFIED | UNKNOWN | UNKNOWN | N/A | UNKNOWN | P2 |
| `Driftwatch` | Public | Drift detection/evaluation engineering | VERIFIED | IN PROGRESS | VERIFIED BUILD/TYPE | UNKNOWN | IN PROGRESS | P1 |
| `resumeapex-eval` | Public | Evaluation protocol/benchmark | VERIFIED | UNKNOWN | UNKNOWN | N/A | UNKNOWN | P1 |
| `junior-apogee-app` | Public | Evaluation/QA workbench | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P1 |
| `sentinel-governance` | Public | Integrity/CI governance | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P1 |
| `Acoustic-mesh` | Public | Acoustic/WebRTC engineering | VERIFIED | IN PROGRESS | VERIFIED BUILD | UNKNOWN | IN PROGRESS | P1 |
| `Meshsense` | Public | MeshSense/RuView runtime/status surface | VERIFIED | VERIFIED SOURCE | VERIFIED CONFIG | PENDING | UNKNOWN | P1 |
| `3d-visualization-hub` | Public | Visualization | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |
| `ai-prompt-systems-portfolio` | Public | Public prompt-systems portfolio | VERIFIED | UNKNOWN | UNKNOWN | N/A | UNKNOWN | P2 |
| `aoga-dashboard` | Private | Production dashboard/API | VERIFIED | UNKNOWN | UNKNOWN | PARTIAL | IN PROGRESS | P1 |
| `phi-calculus-app` | Public | Mathematical research/application | VERIFIED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P1 |
| `AHG-Zeta-Pell-Autonomous-Lattice` | Public | Control/simulation research | VERIFIED | IN PROGRESS | UNKNOWN | N/A | IN PROGRESS | P1 |
| `agent-control-plane` | Public | Control-plane architecture | VERIFIED | VERIFIED PARTIAL | VERIFIED | N/A | IN PROGRESS | P1 |
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
| `pptl-governance-dashboard` | Private | Governance dashboard | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |
| `dgaf-ops` | Private | DGAF operations/support | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | P2 |

## Detailed evidence established in this pass

### DGAF-Framework

The repository has a Next.js application package (`1.7.0`) with build/start scripts and a substantial GitHub Actions surface. The Python quality workflow runs deterministic tests, a Python-version matrix, coverage generation, integration tests, and security scans. However, several quality gates are explicitly non-blocking (`continue-on-error`), integration tests are allowed to pass with `|| true`, and coverage is configured with `--cov-fail-under=0`. Therefore CI is **VERIFIED PARTIAL**, not a strong release gate. The root `requirements.txt` is intentionally empty because current API routes are TypeScript/Next.js handlers, so Python CI installs its test tooling directly and should not be interpreted as a fully reproducible Python dependency environment.

### PDMAL mathematical correction

The current mathematical authority is `docs/formalism/PDMAL_MATH_CORRECTION_2026-08-15.md`. The previously titled `PDMAL_MATH_VERIFIED_v1.md` is explicitly superseded and retained only for provenance. The correction establishes plastic constant `1.3247179572447454`, dodecahedral graph Cheeger constant `0.6`, and unweighted Forman-Ricci curvature `-2` on every edge of the current topology. Because the Forman-Ricci value is constant, it is not currently a useful discriminating audit signal. The correction also explicitly classifies `ContractionMonitor` as an empirical runtime proxy rather than proof of contraction and places `D_a` admission calibration with DGAF Quintet discipline.

A direct search of the current DGAF repository did not locate `lattice_harness.py` or an independently inspectable PDMAL computational harness. Therefore the corrected values are **documented current authority**, but the current GitHub repository state does not by itself establish independent harness reproduction. This remains an empirical-validation gap rather than an absence claim.

### Agent Control Plane

The repository contains a minimal executable kernel, unit tests, and GitHub Actions CI. Its quality baseline identifies dependency reproducibility, security/coverage gates, broader failure-mode testing, and integration tests as current gaps. This makes ACP a useful reference implementation for the normalization standard rather than a completed production control plane.

### Driftwatch

The repository has a lockfile. The root package metadata was found inconsistent with `package.json`: the lockfile identified `react-example`/`0.0.0` while the package identified `driftwatch`/`0.1.0`. `package.json` was normalized and the lockfile root metadata was corrected in commits `be2354dd` and `ef3276c`. The package exposes build and TypeScript checking but no test script. The current audit establishes CI build/type intent; full dependency-install/build execution and detector behavioral validation remain open.

### Acoustic-Mesh

The README correctly limits claims to acoustic/WebRTC engineering and explicitly rejects unsupported physical-performance guarantees. Workspace/package/CI structure is present. No inspected evidence establishes acoustic performance, localization accuracy, or a conventional automated behavioral test gate. Physical/acoustic evidence remains open.

### AHG-Zeta-Pell-Autonomous-Lattice

Pass 1 is documented and correctly quarantines historical benchmark claims. Pass 2 remains outstanding for the chaos/FML mitigation section, Three-Regime Governor, recovery trace, and assembled documentation. The current audit did not establish independently inspectable Pass-2 source artifacts.

### Meshsense

The canonical GitHub repository is `ndrorchestration/Meshsense`. The associated Vercel project remains `meshsense-ruview-status`. Source and deployment configuration are inspectable; Vercel production runtime/source equivalence remains pending.

## Immediate P1 actions

1. Complete code/test/CI inspection for the remaining P1 repositories.
2. Verify Driftwatch dependency installation/build after lockfile correction; add meaningful automated tests before elevating its CI status.
3. Strengthen DGAF CI only after establishing which currently non-blocking checks are intended to be advisory versus release-blocking.
4. Establish runtime evidence for Meshsense/RuView.
5. Complete AHG Zeta-Pell Pass 2.
6. Reconstruct or recover the PDMAL empirical harness and reproduce the corrected topology calculations from executable source.
7. Audit non-README documentation for inherited unsupported claims.
8. Add security/provenance checks to the quality baseline where repository technology makes them applicable.

## Normalization rule

A repository does not receive a higher evidence status because its README, benchmark table, generated report, deployment label, or another repository says that it is verified. Each claim must point to an inspectable implementation, method, test, trace, benchmark, or external attestation appropriate to the claim.

*Updated 2026-08-15 during the repository quality normalization pass.*
