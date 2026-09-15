# DGAF / PDMAL Research Figure Register

Status: ACTIVE · evidence-bound · same-system QA only

This register is the repository companion to the Notion `DGAF / PDMAL — Research Figure Register`. It defines the current first-wave research figures and the repeatable generation/QA process. Generated figures are explanatory artifacts; they do not create scientific state, authorization, empirical N, or efficacy evidence.

## First-wave figures

| ID | Figure | Priority | Epistemic class | Source binding | Repository output | Current status |
|---|---|---|---|---|---|---|
| FIG-001 | Research Program Architecture Map | P0 | DESIGN | `docs/CURRENT_STATE.md` | `generated/fig001_research_program_architecture.svg` | GENERATED / SAME-SYSTEM QA REVIEWED |
| FIG-002 | Five-Topology Structural Comparison | P0 | STRUCTURAL | `experiments/pdmal_topology/graph_harness.py`, `seeds.py` | `generated/fig002_topology_comparison.svg` | GENERATED / SAME-SYSTEM QA REVIEWED |
| FIG-003 | Track A Epoch 002 Design Matrix | P0 | DESIGN | `docs/CURRENT_STATE.md` | `generated/fig003_epoch002_design_matrix.svg` | GENERATED / SAME-SYSTEM QA REVIEWED |
| FIG-004 | Governance Transition State Machine | P0 | GOVERNANCE | ordered transition chain in `docs/CURRENT_STATE.md` | `generated/fig004_governance_state_machine.svg` | GENERATED / SAME-SYSTEM QA REVIEWED; SOURCE FRESHNESS MUST BE CHECKED |
| FIG-005 | Evidence and Provenance DAG | P0 | PROVENANCE | evidence/authority rules in `docs/CURRENT_STATE.md` | `generated/fig005_evidence_provenance_dag.svg` | GENERATED / SAME-SYSTEM QA REVIEWED |
| FIG-006 | Robustness Outcome Curves | P1 | EMPIRICAL | future governed primary-analysis output | reserved | DEFERRED — RESULTS NOT AUTHORIZED |

## Current source-freshness boundary

`docs/CURRENT_STATE.md` currently declares `last_verified: 2026-09-14`. Figures derived from current-state labels display that date explicitly. Before publication or external use, refresh the source document if repository/control-plane truth has advanced, regenerate, and rerun QA. A stale but correctly rendered source snapshot must not be presented as live state.

## Regeneration

From the repository root:

```bash
python tools/research_figures/generate_research_figures.py --repo-root .
pytest -q tests/test_research_figures.py
```

The test suite checks that committed SVGs are byte-identical to a fresh regeneration. Any source or generator change that makes a committed figure stale therefore fails the figure-specific test until the figure is deliberately regenerated.

## Figure contract

Every admitted figure must define all of the following before generation:

1. Stable `FIG-NNN` identifier.
2. Research purpose and priority.
3. Epistemic class.
4. Canonical source binding(s).
5. Deterministic generator path.
6. Repository output path.
7. Whether the figure is allowed under the current data/authorization state.
8. Methodology, visualization, epistemic, and integration QA state.

The machine-readable contracts live in `tools/research_figures/figure_manifest.json`.

## Repeatable QA sweep

Apply these four roles in order. When only one system performs them, record the review as same-system/non-independent.

### 1. Methodology review

- Does the figure answer a defined research/method question rather than decorate the document?
- Are the experimental unit, matrix dimensions, topology definitions, and comparisons correct?
- Does any visual encoding imply a result that the underlying source does not establish?

### 2. Visualization review

- Are titles, labels, node/edge representations, matrix axes, and transition ordering readable?
- Is layout deterministic and stable across regeneration?
- Are dense structures still interpretable without changing the underlying graph?
- Are source-snapshot or other qualification labels visible where needed?

### 3. Epistemic QA

- Is every substantive claim bound to an admitted source?
- Are DESIGN, STRUCTURAL, GOVERNANCE, PROVENANCE, and EMPIRICAL classes kept distinct?
- Are blinded collection, CI/test success, governance readiness, or historical evidence prevented from appearing as efficacy evidence?
- Do historical identities remain exact-scoped rather than silently transferring to a later candidate/epoch?

### 4. Integration/reproducibility review

- Does `figure_manifest.json` agree with the register and generated filenames?
- Does a clean regeneration produce the committed bytes?
- Do all figure-specific tests pass?
- Did generation touch only the research-figure subsystem and outputs?

## Empirical-figure admission rule

Outcome curves, effect-size plots, confidence intervals, structure-performance correlations, forest plots, and other empirical-result figures are not admitted merely because blinded observations exist. They require the appropriate governed dataset-lock/materialization/primary-analysis sequence and a source artifact that is authorized for interpretation. Until then, empirical figure entries remain deferred and non-generating.

## First-wave QA record — 2026-09-15

- Methodology review: PASS, same-system/non-independent.
- Visualization review: PASS after correcting machine-token overflow in FIG-001 and adding source-freshness visibility to state-derived figures.
- Epistemic QA: PASS for first-wave scope; no protected mapping, outcome values, effect estimates, or efficacy claims are consumed or rendered.
- Integration review: PASS locally; nine figure-specific tests pass and two consecutive generations are byte-stable. Repository/PR CI remains a separate verification step.
