# Ecosystem Connection Manifest — 2026-08-15

## Purpose
Mechanical synchronization ledger for the `ndrorchestration` GitHub repository set and its Notion/Vercel connection layer.

Status vocabulary: `VERIFIED`, `NOT_APPLICABLE`, `PENDING`.

`VERIFIED` means the specific connection/identity was directly observed in the current connector surface. It does not imply capability validation. `NOT_APPLICABLE` means no connection is expected for the repository's role. `PENDING` means a connection may exist or is expected but was not independently verified in this sweep.

## Current Vercel observations

- Vercel team `ndrorchestration` is directly accessible.
- Eight Vercel projects are currently exposed: `phiknightverticalcorridor`, `driftwatch`, `meshsense-ruview-status`, `ndrorchestration`, `phi-calculus`, `aoga-dashboard`, `dgaf-ruview-mitigation`, and `quintet-hardening-report`.
- `meshsense-ruview-status` project identity is directly verified as `prj_YrGkdQLGlLAK7aizvz7uPufWokMM`.
- Its latest production deployment `dpl_uZdP6uzH1puxtZkPPdq5pwfEjJWJ` is `READY` and its build logs show a successful `server.js` root entrypoint build.
- MeshSense runtime observations are mixed: Vercel runtime logs recorded `/health` HTTP 200, but direct current requests to `/`, `/health`, and `/api/status` returned HTTP 404. Therefore runtime is **PENDING**, not VERIFIED.
- The latest MeshSense deployment is therefore deployment-verified, but endpoint behavior requires reconciliation before runtime closure.
- `driftwatch` has current READY production deployments tied directly to `ndrorchestration/Driftwatch` commits; Vercel project identity and Git binding are VERIFIED. No runtime errors were reported for the preceding 24 hours. This does not validate detector effectiveness.

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
| Driftwatch | VERIFIED | VERIFIED | VERIFIED | Vercel project/Git binding verified; detector effectiveness remains unvalidated |
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
| Meshsense | VERIFIED | VERIFIED | PENDING | MeshSense / RuView Status; Vercel identity and READY deployment verified, endpoint/runtime reconciliation pending |

## Directly verified canonical mappings

- `ndrorchestration/Meshsense` ↔ Notion `MeshSense / RuView Status` ↔ Vercel `meshsense-ruview-status`.
- `ndrorchestration/phi-calculus-app` ↔ Notion `phi-calculus` ↔ Vercel `phi-calculus`.
- `ndrorchestration/Driftwatch` ↔ Notion `driftwatch` ↔ Vercel `driftwatch`.
- `ndrorchestration/aoga-dashboard` ↔ Notion `aoga-dashboard` ↔ Vercel `aoga-dashboard`.
- `agent-control-plane` is represented in the Notion registry with no Vercel project, consistent with its specification-stage status.

## Important evidence boundaries

- MeshSense GitHub/CI evidence is distinct from Vercel deployment and runtime evidence.
- MeshSense deployment is currently READY, but direct endpoint checks returned 404 while runtime logs include a `/health` 200 observation. This discrepancy is explicitly unresolved.
- Acoustic-Mesh implementation/CI evidence does not establish acoustic localization, spatial reconstruction, synchronization quality, modal-analysis validity, or performance superiority.
- PDMAL remains experimental and is a DGAF research lineage; it is not promoted by repository presence or visualization.
- Driftwatch implementation/deployment presence does not establish detector effectiveness; benchmark evidence remains pending.
- AHG Zeta-Pell Pass 2 remains source-dependent.
- Evaluation/governance repositories do not inherit validation from the spatial/acoustic branch.

## Notion synchronization result

The AI Systems Portfolio Registry now contains 36 project records, covering the authenticated GitHub inventory plus existing Vercel/system records. The authenticated GitHub inventory contains 29 repositories. No duplicate project-name rows were found in the current registry query.

## Closure gate

The documentation/connection layer is considered mechanically synchronized when:

1. every authenticated GitHub repository has a corresponding Notion registry row or an explicit `NOT_APPLICABLE` classification;
2. every claimed Vercel mapping has a directly observed project identity;
3. runtime claims are backed by runtime observations rather than deployment existence alone;
4. experimental evidence is propagated after experiments actually run;
5. the manifest is regenerated after material topology changes.

Current sweep conclusion: **GitHub inventory VERIFIED; Notion coverage synchronized; canonical Vercel mappings VERIFIED where directly observed; MeshSense runtime reconciliation remains PENDING; empirical evidence gates remain open.**
