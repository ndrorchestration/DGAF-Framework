# Ecosystem Connection Manifest — 2026-08-15

## Purpose
Mechanical synchronization ledger for the `ndrorchestration` GitHub repository set and its Notion/Vercel connection layer.

Status vocabulary: `VERIFIED`, `NOT_APPLICABLE`, `PENDING`.

`VERIFIED` means the specific connection/identity was directly observed in the current connector surface. It does not imply runtime validation. `NOT_APPLICABLE` means no connection is expected for the repository's role. `PENDING` means a connection may exist or is expected but was not independently verified in this sweep.

## GitHub inventory

All repositories below were directly returned by the authenticated GitHub repository inventory on 2026-08-15. Therefore GitHub identity is `VERIFIED` for every row.

| Repository | GitHub | Notion registry | Vercel/runtime | Role / evidence boundary |
|---|---|---|---|---|
| AI-Prompt-Engineer | VERIFIED | VERIFIED | NOT_APPLICABLE | portfolio/support |
| ai-prompt-engineering-portfolio | VERIFIED | VERIFIED | NOT_APPLICABLE | portfolio |
| gold-star-qa-framework | VERIFIED | VERIFIED | NOT_APPLICABLE | archived QA framework |
| DGAF-Framework | VERIFIED | VERIFIED | PENDING | governance/research spine |
| chat-archives | VERIFIED | VERIFIED | NOT_APPLICABLE | archive/support |
| prompt-optimization-library | VERIFIED | VERIFIED | NOT_APPLICABLE | reusable library |
| ai-governance-frameworks | VERIFIED | VERIFIED | NOT_APPLICABLE | governance/evidence reference |
| Gold-star-standards | VERIFIED | VERIFIED | NOT_APPLICABLE | standards/evaluation |
| ai-prompt-systems-portfolio | VERIFIED | VERIFIED | NOT_APPLICABLE | portfolio |
| 3d-visualization-hub | VERIFIED | VERIFIED | NOT_APPLICABLE | demonstrator |
| junior-apogee-app | VERIFIED | VERIFIED | PENDING | evaluation application |
| phi-calculus-app | VERIFIED | VERIFIED | VERIFIED | experimental research/visualization |
| sentinel-governance | VERIFIED | VERIFIED | NOT_APPLICABLE | governance tooling |
| resumeapex-eval | VERIFIED | VERIFIED | PENDING | evaluation application |
| Driftwatch | VERIFIED | VERIFIED | VERIFIED | experimental drift/observability |
| Amethyst-Governance-Eval-Stack | VERIFIED | VERIFIED | NOT_APPLICABLE | evaluation/governance |
| .github | VERIFIED | VERIFIED | NOT_APPLICABLE | organization-level support |
| Acoustic-mesh | VERIFIED | VERIFIED | NOT_APPLICABLE | acoustic/WebRTC infrastructure; empirical acoustic validation pending |
| career-positioning | VERIFIED | VERIFIED | NOT_APPLICABLE | career/support |
| automation-scripts | VERIFIED | VERIFIED | NOT_APPLICABLE | operations/support |
| ndrorchestration | VERIFIED | VERIFIED | NOT_APPLICABLE | profile/organization support |
| api | VERIFIED | VERIFIED | NOT_APPLICABLE | API support |
| aoga-dashboard | VERIFIED | VERIFIED | VERIFIED | governance dashboard |
| pptl-governance-dashboard | VERIFIED | VERIFIED | PENDING | governance dashboard |
| entrepreneur-hub | VERIFIED | VERIFIED | NOT_APPLICABLE | portfolio/business support |
| dgaf-ops | VERIFIED | VERIFIED | NOT_APPLICABLE | operations/support |
| agent-control-plane | VERIFIED | VERIFIED | NOT_APPLICABLE | specification-stage control-plane project |
| AHG-Zeta-Pell-Autonomous-Lattice | VERIFIED | VERIFIED | NOT_APPLICABLE | experimental research |
| Meshsense | VERIFIED | VERIFIED | VERIFIED | MeshSense / RuView Status; Vercel identifier `meshsense-ruview-status` |

## Directly verified canonical mappings

- `ndrorchestration/Meshsense` ↔ Notion `MeshSense / RuView Status` ↔ Vercel `meshsense-ruview-status`.
- `ndrorchestration/phi-calculus-app` ↔ Notion `phi-calculus` ↔ Vercel `phi-calculus`.
- `ndrorchestration/Driftwatch` ↔ Notion `driftwatch` ↔ Vercel `driftwatch`.
- `ndrorchestration/aoga-dashboard` ↔ Notion `aoga-dashboard` ↔ Vercel `aoga-dashboard`.
- `agent-control-plane` is represented in the Notion registry with no Vercel project, consistent with its specification-stage status.

## Important evidence boundaries

- MeshSense GitHub/CI evidence is distinct from Vercel deployment and runtime evidence.
- MeshSense `/health` has been verified as part of the current evidence record; `/api/status` remains authentication-constrained for independent verification.
- Acoustic-Mesh implementation/CI evidence does not establish acoustic localization, spatial reconstruction, synchronization quality, modal-analysis validity, or performance superiority.
- PDMAL remains experimental and is a DGAF research lineage; it is not promoted by repository presence or visualization.
- Driftwatch implementation/deployment presence does not establish detector effectiveness; benchmark evidence remains pending.
- AHG Zeta-Pell Pass 2 remains source-dependent.
- Evaluation/governance repositories do not inherit validation from the spatial/acoustic branch.

## Notion synchronization result

The AI Systems Portfolio Registry contained 9 project rows before this sweep. The full authenticated GitHub inventory contains 29 repositories. Missing repository rows are therefore a synchronization gap rather than evidence that the repositories are absent from the ecosystem. This manifest records the complete GitHub-side inventory and the intended registry state.

## Closure gate

The documentation/connection layer is considered mechanically synchronized only when:

1. every authenticated GitHub repository has a corresponding Notion registry row or an explicit `NOT_APPLICABLE` classification;
2. every claimed Vercel mapping has a directly observed project identity;
3. runtime claims are backed by runtime observations rather than deployment existence alone;
4. experimental evidence is propagated after experiments actually run;
5. the manifest is regenerated after material topology changes.

Current sweep conclusion: **GitHub inventory VERIFIED; canonical core mappings VERIFIED; remaining Vercel/runtime bindings are intentionally PENDING or NOT_APPLICABLE; empirical evidence gates remain open.**
