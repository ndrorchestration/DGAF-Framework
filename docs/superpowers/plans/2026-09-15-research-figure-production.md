# Research Figure Production System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic, evidence-bound generator for the five highest-priority DGAF/PDMAL research figures without consuming governed outcome data.

**Architecture:** A JSON manifest defines figure contracts. A Python generator reads canonical repository sources, imports the existing topology harness, renders SVG using only the standard library plus existing NetworkX, and writes stable outputs. Tests enforce topology invariants, source binding, deterministic generation, and fail-closed outcome boundaries.

**Tech Stack:** Python 3.12-compatible standard library, NetworkX 3.6.1, pytest.

**Spec:** `docs/superpowers/specs/2026-09-15-research-figure-production-design.md`

## Global Constraints

- Do not change experiment execution, analysis, custody, blinding, authorization, or governance state.
- Do not read protected mapping material, secrets, or empirical outcome datasets.
- Use `experiments/pdmal_topology/graph_harness.py` as the topology source of truth.
- Use `docs/CURRENT_STATE.md` as the current-facing state/transition source.
- Keep generated output under `docs/research_figures/generated/`.
- Generation must be deterministic and fail closed on missing or conflicting required sources.

---

### Task 1: Manifest and parser contract

**Files:**
- Create: `tools/research_figures/figure_manifest.json`
- Create: `tools/research_figures/generate_research_figures.py`
- Test: `tests/test_research_figures.py`

**Interfaces:**
- Produces `load_manifest(repo_root: Path) -> list[FigureSpec]`.
- Produces `parse_frontmatter(text: str) -> dict[str, str]`.
- Produces `parse_transition_chain(text: str) -> list[str]`.

- [ ] **Step 1: Write failing tests** for unique figure IDs, safe output paths, frontmatter parsing, and ordered transition-chain extraction.
- [ ] **Step 2: Run** `pytest -q tests/test_research_figures.py` and confirm failure because the generator module does not exist.
- [ ] **Step 3: Implement** `FigureSpec`, manifest validation, frontmatter parsing, and transition-chain parsing with explicit `FigureGenerationError` failures.
- [ ] **Step 4: Run** `pytest -q tests/test_research_figures.py` and confirm the parser tests pass.

### Task 2: Canonical topology adapter and structural invariants

**Files:**
- Modify: `tools/research_figures/generate_research_figures.py`
- Test: `tests/test_research_figures.py`

**Interfaces:**
- Produces `load_topologies(repo_root: Path, reference_seed: int = 20270201) -> dict[str, nx.Graph]`.
- The function imports and calls canonical `build_topologies()` from `experiments/pdmal_topology/graph_harness.py`.

- [ ] **Step 1: Add failing tests** requiring topology names `ring`, `pdmal`, `random_regular`, `small_world`, `complete`; 20 nodes each; edge counts `20, 30, 30, 40, 190`; PDMAL degree set `{3}`.
- [ ] **Step 2: Run** the topology tests and confirm failure before implementation.
- [ ] **Step 3: Implement** dynamic canonical harness loading and invariant checks.
- [ ] **Step 4: Run** tests and confirm they pass.

### Task 3: Deterministic SVG renderers for FIG-001 through FIG-005

**Files:**
- Modify: `tools/research_figures/generate_research_figures.py`
- Test: `tests/test_research_figures.py`

**Interfaces:**
- Produces `render_all(repo_root: Path, output_root: Path | None = None) -> list[Path]`.
- Private renderers accept source-derived state and return UTF-8 SVG strings.

- [ ] **Step 1: Add failing tests** requiring exactly five SVGs, figure IDs and epistemic metadata in each file, source digests, deterministic byte equality across repeated runs, and no hidden mapping/outcome terms in FIG-003.
- [ ] **Step 2: Run** tests and confirm renderer tests fail before implementation.
- [ ] **Step 3: Implement** reusable SVG primitives and five renderers: architecture map, topology plate, design matrix, transition state machine, provenance DAG.
- [ ] **Step 4: Run** tests and confirm all renderer tests pass.

### Task 4: Register documentation and generated artifacts

**Files:**
- Create: `docs/research_figures/FIGURE_REGISTER.md`
- Generate: `docs/research_figures/generated/fig001_research_program_architecture.svg`
- Generate: `docs/research_figures/generated/fig002_topology_comparison.svg`
- Generate: `docs/research_figures/generated/fig003_epoch002_design_matrix.svg`
- Generate: `docs/research_figures/generated/fig004_governance_state_machine.svg`
- Generate: `docs/research_figures/generated/fig005_evidence_provenance_dag.svg`

**Interfaces:**
- Regeneration command: `python tools/research_figures/generate_research_figures.py --repo-root .`

- [ ] **Step 1: Generate** all five artifacts from canonical sources.
- [ ] **Step 2: Run generation a second time** and compare SHA-256 digests to prove byte stability.
- [ ] **Step 3: Write** the human-readable register with source bindings, epistemic class, status, and empirical deferral rule.
- [ ] **Step 4: Verify** SVG XML parses and no file is empty.

### Task 5: Full verification and branch handoff

**Files:**
- Verify all files above; no experiment/runtime file changes.

- [ ] **Step 1: Run** `pytest -q tests/test_research_figures.py` and require zero failures.
- [ ] **Step 2: Run** `python tools/research_figures/generate_research_figures.py --repo-root .` and require exit code 0.
- [ ] **Step 3: Run** a deterministic digest comparison across a fresh second generation.
- [ ] **Step 4: Inspect** the Git diff and confirm only the research-figure subsystem/spec/plan/docs are added.
- [ ] **Step 5: Open** a draft PR from the isolated feature branch; do not merge automatically.
