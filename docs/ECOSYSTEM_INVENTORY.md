# ECOSYSTEM_INVENTORY.md

> **Purpose:** canonical repository inventory for the ndrorchestration ecosystem. This document is an inventory, not a validation registry.
> **Last Updated:** 2026-08-15

## Evidence boundary

Repository presence, naming, deployment labels, historical benchmark values, and cross-repository relationships do not establish implementation or validation. Use the evidence ladder maintained by `docs/ECOSYSTEM_AUDIT_STATUS.md` and the engineering audit matrix at `docs/REPOSITORY_QUALITY_AUDIT_MATRIX_2026-08-15.md`.

## Live GitHub inventory

29 repositories were enumerated from the live `ndrorchestration` account on 2026-08-15.

| Repository | Visibility | Classification |
|---|---|---|
| `ndrorchestration` | Public | Canonical portfolio/control surface |
| `DGAF-Framework` | Public | Governance/evaluation research spine |
| `ai-governance-frameworks` | Public | Governance research/mapping |
| `Driftwatch` | Public | Drift detection/evaluation engineering |
| `resumeapex-eval` | Public | Evaluation protocol/benchmark |
| `junior-apogee-app` | Public | Evaluation/QA workbench |
| `sentinel-governance` | Public | Integrity/CI governance |
| `Acoustic-mesh` | Public | Acoustic/WebRTC engineering |
| `Meshsense` | Public | MeshSense/RuView runtime/status surface |
| `3d-visualization-hub` | Public | Visualization |
| `ai-prompt-systems-portfolio` | Public | Public prompt-systems portfolio |
| `aoga-dashboard` | Private | Production dashboard/API |
| `phi-calculus-app` | Public | Mathematical research/application |
| `AHG-Zeta-Pell-Autonomous-Lattice` | Public | Control/simulation research |
| `agent-control-plane` | Public | Control-plane architecture |
| `entrepreneur-hub` | Public | Business/template track |
| `AI-Prompt-Engineer` | Private | Historical portfolio |
| `ai-prompt-engineering-portfolio` | Private | Historical portfolio |
| `prompt-optimization-library` | Private | Historical/research library |
| `gold-star-qa-framework` | Private / archived | Archived framework |
| `Gold-star-standards` | Private | Standards/archive support |
| `Amethyst-Governance-Eval-Stack` | Private | Governance/evaluation stack |
| `.github` | Public | Account-wide GitHub configuration |
| `chat-archives` | Private | Archive |
| `career-positioning` | Private | Career/portfolio support |
| `automation-scripts` | Private | Automation support |
| `api` | Private | API support surface |
| `pptl-governance-dashboard` | Private | Governance dashboard |
| `dgaf-ops` | Private | DGAF operations/support |

## Canonical project boundaries

### DGAF

`DGAF-Framework` is the canonical governance/evaluation research spine. DGAF terminology does not validate other repositories.

### PDMAL / lattice work

PDMAL is a separate topology/lattice research track. The corrected lattice artifacts establish the current mathematical boundary; empirical validation remains open. The corrected plastic constant and dodecahedral Cheeger result must not be conflated with runtime proof. Unweighted Forman-Ricci curvature remains a research item until useful weighted-edge definitions and evidence exist.

### ASIS / Acoustic-Mesh

ASIS means **Acoustic Spatial Insight System**. `Acoustic-mesh` is the acoustic/WebRTC engineering track. Acoustic performance claims require acoustic/signal-processing/network evidence and are not validated by DGAF, PDMAL, or other ecosystem relationships.

### MeshSense / RuView Status

`ndrorchestration/Meshsense` is the canonical GitHub source repository. `meshsense-ruview-status` is the associated Vercel project identifier. GitHub/CI state is documented separately from Vercel runtime verification, which remains pending.

### AHG Zeta-Pell

`AHG-Zeta-Pell-Autonomous-Lattice` is a separate control/simulation track. Pass 1 audit findings remain active; Pass 2 is outstanding.

### Agent Control Plane

`agent-control-plane` is a separate experimental control-plane architecture track with a minimal executable kernel. It is not a production autonomous control plane and does not inherit DGAF validation.

## Historical repositories

The following repositories remain useful for provenance but are not current authorities merely because they contain older benchmark, certification, or governance language:

- `AI-Prompt-Engineer`
- `ai-prompt-engineering-portfolio`
- `prompt-optimization-library`
- `gold-star-qa-framework`

## Current normalization work

The engineering quality audit is tracked in:

- `docs/ECOSYSTEM_AUDIT_STATUS.md`
- `docs/REPOSITORY_QUALITY_AUDIT_MATRIX_2026-08-15.md`
- `docs/EPISTEMIC_SUPERSESSION_REGISTER.md`

Current high-priority unresolved work includes PDMAL empirical validation, Driftwatch detector/benchmark validation, Acoustic-Mesh acoustic evidence, AHG Zeta-Pell Pass 2, MeshSense/RuView runtime verification, weighted Forman-Ricci definition, real-trace `D_a` calibration, and reconstruction of the missing TLA+ containment specification.

## Provenance

Developed and maintained by Ndr / Ender Hensel (`ndrorchestration`).

*Inventory reconciliation: 2026-08-15.*
