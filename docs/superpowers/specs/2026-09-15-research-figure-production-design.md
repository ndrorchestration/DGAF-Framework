# Research Figure Production System — Design

## Purpose

Add a small, reproducible research-figure subsystem to DGAF-Framework. The subsystem turns canonical repository evidence into publication-ready SVG figures without consuming or exposing governed experimental outcomes.

## Scope

The first wave contains five P0 figures:

1. `FIG-001` Research Program Architecture Map.
2. `FIG-002` Five-Topology Structural Comparison.
3. `FIG-003` Track A Epoch 002 Design Matrix.
4. `FIG-004` Governance Transition State Machine.
5. `FIG-005` Evidence and Provenance DAG.

Empirical outcome figures are explicitly out of scope until the governed primary-analysis stage authorizes them.

## Architecture

A declarative JSON manifest defines stable figure IDs, epistemic classes, source bindings, and output paths. A single Python generator reads that manifest plus canonical repository sources, renders deterministic SVG, and writes only under `docs/research_figures/generated/`. Tests verify source binding, topology invariants, fail-closed design semantics, deterministic output, and absence of outcome claims.

The generator is intentionally separate from experiment execution. It does not import analysis outputs, blinding mappings, protected material, custody secrets, or result datasets. For topology rendering it imports the existing canonical `experiments/pdmal_topology/graph_harness.py` so topology definitions are not silently duplicated.

## Source and epistemic rules

- `docs/CURRENT_STATE.md` is the repository source for current-facing state labels and ordered transition-chain text.
- `experiments/pdmal_topology/graph_harness.py` is the source for topology generators.
- Figure metadata records an epistemic class: DESIGN, STRUCTURAL, GOVERNANCE, or PROVENANCE.
- Generated SVGs include figure ID, epistemic class, source-binding metadata, and a generated-from-source disclaimer.
- `FIG-003` may describe the blinded design matrix (five topologies, nine failure counts, 50 paired seed units, 2,250 blinded cells) but must not display hidden condition mappings or outcomes.
- No figure generation changes scientific state, authorization, N, or efficacy claims.

## Determinism

- SVG geometry is deterministic.
- The topology comparison uses reference seed `20270201` solely to instantiate stochastic topology generators consistently; the figure labels the seed and states that it is a structural illustration, not an outcome.
- Stable layout functions use fixed arithmetic rather than randomized layout algorithms.
- SVG metadata includes a SHA-256 digest of each bound source file used for generation.

## Error handling

Generation fails closed when:

- a manifest entry is invalid or duplicated;
- a declared source file does not exist;
- canonical topology construction fails;
- expected Track A design constants cannot be found in current state;
- an output path escapes the designated generated-figure directory.

A failed figure does not silently emit a partial file.

## QA model

Four review roles are applied to each figure:

1. Methodology review: question, unit, and comparison are correct.
2. Visualization review: layout and labels are interpretable and deterministic.
3. Epistemic QA: every substantive label is source-bound and no unsupported transition/result is implied.
4. Integration review: manifest, generator, output path, tests, and documentation agree.

These same-system reviews are not independent validation. If independent/custom agents become available later, they can re-run the same role-specific checklist.

## Repository layout

- `tools/research_figures/figure_manifest.json` — stable figure contracts.
- `tools/research_figures/generate_research_figures.py` — parser and SVG generator.
- `tests/test_research_figures.py` — source-binding and rendering tests.
- `docs/research_figures/FIGURE_REGISTER.md` — human-readable register and regeneration instructions.
- `docs/research_figures/generated/*.svg` — generated first-wave outputs.

## Acceptance criteria

- One command regenerates all five P0 SVGs.
- Re-running generation with unchanged sources produces byte-identical SVGs.
- Tests verify canonical topology node/edge counts and PDMAL degree-3 invariant.
- The design matrix visibly encodes 5 × 9 × 50 = 2,250 blinded cells without outcome values.
- The governance figure is derived from the ordered chain in `docs/CURRENT_STATE.md` rather than a manually maintained duplicate.
- No output represents blinded collection as an efficacy result or primary analysis.
