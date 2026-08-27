# Repository Structure Contract

**Status:** Canonical structural map  
**Baseline:** `chore/repository-structure-normalization`  
**Structural baseline:** `main` at `49a6c32c87918702071b1f1fcdca88d51cc950ea`

This document defines the repository's intended file-system boundaries. It is a navigation and governance contract; it does not change epistemic status, experimental authorization, licensing, or scientific claims.

## Top-level boundaries

| Path | Responsibility | Rule |
|---|---|---|
| `.github/` | CI/CD, automation, repository workflows | Workflow definitions only |
| `.operations/` | Repository-operational controls and checklists | Operational tooling, not research evidence |
| `api/` | Small Python/API integration surface | Keep distinct from Next.js route handlers |
| `app/` | Next.js App Router application | UI/application surface |
| `components/` | Shared application/framework components | Reusable implementation components |
| `dashboard/` | Dashboard-specific UI assets | Keep separate from App Router surface unless intentionally consolidated |
| `docs/` | Human-readable governance, research, architecture, evidence, and project documentation | Organize by concern; avoid new root-level documentation sprawl |
| `evidence/` | Machine- or human-readable evidence artifacts | Evidence is not equivalent to validation |
| `evaluations/` | Evaluation implementations and fixtures | Evaluation code belongs with its fixtures |
| `experiments/` | Executable research apparatus | Experiment-specific code and tests stay together |
| `lib/` | Small TypeScript shared library surface | Application/library utilities only |
| `pages/` | Legacy/Pages Router surface and route handlers | Preserve until migration is explicitly verified |
| `patterns/` | Pattern artifacts intended for repository-level pattern surface | Do not silently promote experimental patterns to canonical status |
| `pptl/` | Python PPTL implementation and its tests/corpus/experiments | Keep implementation, tests, and local experimental data bounded here |
| `references/` | External/reference material | Reference material, not source-of-truth implementation |
| `registry/` | Repository registries/manifests | Registry membership does not imply truth or validation |
| `repos/` | Embedded portfolio/repository governance stubs | Cross-repository boundary only |
| `resonant_decay/` | Resonant-decay implementation | Package-local code and simulations |
| `schemas/` | Shared machine-readable schemas | Canonical schema surface |
| `scripts/` | Repository maintenance/audit scripts | Executable maintenance tooling |
| `specs/` | Formal verification specifications | Formal models, not ordinary documentation |
| `src/` | General Python source surface | Keep distinct from specialized `pptl/` and package surfaces |
| `tests/` | Cross-project test suite | Tests that do not belong to a specialized package |
| `tools/` | User/operator-facing validation utilities | Tooling, not canonical runtime implementation |

## Documentation hierarchy

`docs/` is organized by semantic concern rather than chronology:

- `docs/agents/` — agent identity, specifications, protocols, memory/KB, integration, and QA material.
- `docs/architecture/` — architecture assessments and convergence documentation.
- `docs/evidence/` — evidence standards, indexes, matrices, and reproducibility controls.
- `docs/experiment/` — experimental protocols, candidate/freeze controls, runtime verification, and PDMAL apparatus documentation.
- `docs/formalism/` — mathematical/formal derivations and constants.
- `docs/formations/` — formation definitions.
- `docs/gates/` — gate definitions and gate-specific controls.
- `docs/governance/` — current governance decisions, readiness, adjudication, and operating policy.
- `docs/governance/boundaries/` — asset, commercialization, openness, trademark, and ecosystem-boundary policies.
- `docs/ops/` — operational runbooks, drive/sweep controls, and runtime-hardening documentation.
- `docs/patterns/` — pattern documentation and registries.
- `docs/qa/` — QA artifacts and audits.
- `docs/registry/` — registry-specific documentation.
- `docs/research/` — research-related source adjudication and related-work material.
- `docs/specs/` — focused technical specifications.
- `docs/stasis/` — stasis/draft research material.
- `docs/substrate/` — substrate/autoinit documentation.
- `docs/sync/` — synchronization policies and records.
- `docs/taxonomy/` — taxonomy and vocabulary controls.
- `docs/theory/` — theoretical architecture and analysis.

## Normalization decisions made in this branch

### Governance boundary documents

The former uppercase `docs/GOVERNANCE/` directory duplicated the semantic namespace of `docs/governance/` on case-sensitive file systems. Its four boundary documents are now canonical under:

`docs/governance/boundaries/`

This removes case-sensitive namespace ambiguity without changing their substantive content.

### Runtime operations documentation

The former `docs/operations/` directory contained a single P6a runtime-hardening document while `docs/ops/` already served as the operational documentation namespace. The P6a document is now canonical under:

`docs/ops/runtime/P6A_ESSENTIAL_RUNTIME_HARDENING.md`

This avoids maintaining two near-synonymous operational namespaces.

## Agent-document rule

Per-agent directories under `docs/agents/<agent>/` are the canonical home for agent-specific material. Named artifacts such as `<AGENT>_SPEC.md`, `<AGENT>_INTEGRATION.md`, and agent-specific KB/protocol/rubric files should be preferred over undifferentiated duplicate stubs when both exist.

Legacy `SPEC.md` files are not automatically deleted by this structural pass because some may contain lineage information. Their supersession status must be verified before removal.

## Structural safety rules

1. Do not move a file solely because its name looks redundant; inspect references and semantic role first.
2. Preserve historical evidence rather than rewriting it to match the current state.
3. Never make a historical commit appear to be the current experimental candidate.
4. Do not use directory placement as evidence of epistemic validity.
5. Any path move that affects imports, CI, deployment, or documentation links requires a reference sweep.
6. Empty/obsolete namespaces should be removed only after confirming no external or internal references remain.
7. Current-state documents must identify their applicability boundary and commit/version where material.
8. Scientific artifacts and operational artifacts must remain distinguishable even when both concern the same system.
