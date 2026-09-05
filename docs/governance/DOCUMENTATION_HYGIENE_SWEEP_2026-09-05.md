# Documentation Hygiene Sweep — 2026-09-05

**Status:** COMPLETED ON HYGIENE BRANCH / PENDING PR VALIDATION  
**Source boundary audited:** `a3bafa6fca8599df479a685828f5fdddb6bae589`  
**Branch:** `docs/multi-hygiene-sweeps-20260905`  
**Scientific boundary:** `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`

## Purpose

Perform multiple documentation-hygiene passes after the P4 custody-architecture correction without changing the designated runtime candidate, promoting historical evidence, creating a freeze, granting authorization, or fabricating empirical results.

This record distinguishes current-facing corrections from historical provenance. A historical document may truthfully describe what was current at its own exact boundary; it is not rewritten merely because later repository state changed. Current-facing surfaces are corrected when they continue to present superseded state as current.

## Sweep 1 — mathematical/constants hygiene

### Verified current authority

The repository already contains the corrected PDMAL mathematical boundary:

- plastic constant `ρ ≈ 1.3247179572447454`, the real root of `x³-x-1=0`;
- DGAF-specific Platinum Mean `pP = 1/(2 sin(π/11)) ≈ 1.774732842`, kept distinct from `ρ`;
- dodecahedral base graph: 20 vertices, 30 edges, 3-regular, vertex connectivity 3;
- exact Cheeger constant `h(G)=0.6`;
- unweighted Forman-Ricci curvature `-2` on every dodecahedral edge, yielding zero variance and no useful discriminator on the unweighted topology;
- contraction sampling classified as an empirical proxy rather than a Banach proof;
- normalized admission distance requiring data-calibrated `τ` rather than the legacy unit-dependent `D_a≤10` threshold.

### Defect corrected

`docs/formalism/hensel-general-formalism.md` remained canonical but still presented two older architectural targets too strongly:

1. `D_a≤10` as an operational measurable;
2. unweighted Forman-Ricci edge scanning as if low computational cost implied useful audit signal.

The formalism is now v1.2 and explicitly separates historical design targets from current PDMAL mathematical authority. It preserves the O(|E|) computational-cost observation while recording that the current unweighted graph has no curvature discrimination signal. Real-trace `D_a` calibration and weighted-curvature semantics remain open R&D items.

Historical `docs/gates/GATE_SPECS.md` already labels `D_a≤10` and related values as historical targets and was therefore not rewritten.

## Sweep 2 — P4 custody/governance hygiene

### Defects corrected

Several current-facing surfaces still described P4 as blocked specifically on distinct-human custody after PR #286 had changed the canonical criterion to effective control separation.

Corrected surfaces now state:

- Mode `H`: genuinely distinct human custody;
- Mode `I`: institutional/third-party custody outside the analyst's unilateral control;
- Mode `T`: independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

No custody mode has been instantiated or verified. P4 remains OPEN / NOT EXECUTED.

### Issue routing corrected

- Issue #285: **COMPLETED** governance-architecture correction via PR #286 / merge `a3bafa6f…`.
- Issue #255: **SUPERSEDED / HISTORICAL** human-only checkpoint.
- Issue #287: **OPEN / DESIGN-THREAT-MODEL ONLY** for a possible zero-human Mode-T lifecycle.

The canonical P4 procedure, execution handoff, P8 checklist, freeze-readiness record, and next-stage expert plan now use this routing.

## Sweep 3 — Mode-T epistemic-boundary hygiene

The repository now explicitly distinguishes:

- Mode T as an admissible **control class**; from
- any specific zero-human technical mechanism as an **accepted implementation**.

No zero-human Mode-T mechanism has been accepted or executed.

Issue #287 explores a transient-runner/timelock design, but that concept may require a future mode-specific lifecycle revision because the current universal P4-A predicates expect real key/mapping commitments before freeze. Until a future revision is independently reviewed, merged, and verified, the current canonical pre-freeze lifecycle remains controlling.

GitHub-hosted runners, drand/timelock tooling, KMS/HSM products, preregistration, or design prose are not promoted into P4 evidence by association.

## Sweep 4 — engineering-quality status hygiene

### Stale state found

README, current-state/project-status records, and Issue #32/#64 status files still described flake8/Black/isort/mypy as current advisory `continue-on-error` diagnostics based on run `33957199893`.

That statement is valid historically for the exact run, but it became stale after Issue #270 closed.

### Current distinction restored

Issue #270 is **CLOSED / COMPLETED**:

- current-lineage flake8/Black/isort/mypy baseline repaired;
- quality stages converted to fail-closed workflow gates;
- Python 3.10/3.11/3.12 execution passed at the recorded exact boundaries;
- deterministic negative controls demonstrated that intentional violations are rejected.

Issue #277 remains **OPEN** for a separate repository-administration layer: available branch-protection/ruleset readback did not establish that the Python quality matrix is required before every merge.

Therefore the correct current wording is:

- workflow quality behavior: `VERIFIED / FAIL-CLOSED WHEN EXECUTED`;
- branch-protection enforcement: `NOT ESTABLISHED / TRACKED BY #277`.

## Sweep 5 — SHA/provenance/current-language hygiene

Current-facing documents embedded `17fbe054…` as “current main,” even though later commits necessarily made that phrasing stale.

The refreshed documents use immutable language such as:

- `reconciliation_source_boundary`;
- `documentation-hygiene reconciliation source boundary`;
- exact historical merge/verification boundary.

The current hygiene source boundary is `a3bafa6fca8599df479a685828f5fdddb6bae589`. The branch commits containing this report are descendants, so this record deliberately does not self-embed a SHA and call it “current main.”

The designated executable runtime/scientific candidate remains:

- candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`;
- tree: `586c00d6dedb589e52108279f9759be3c4f927e1`;
- deployment reference: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.

Documentation descendants neither replace that candidate nor inherit its runtime evidence automatically.

## Sweep 6 — historical-vs-current preservation

Historical evidence was not bulk-edited to erase superseded claims. The following rule was applied:

1. **Current-facing state/control docs:** correct stale present-tense claims.
2. **Canonical procedures/formalisms:** correct current authority while preserving historical design provenance explicitly.
3. **Historical exact-run/issue/evidence records:** preserve factual historical observations unless the document incorrectly promotes them as current.
4. **Scientific evidence:** never transfer across candidate/workflow/artifact/deployment/control-state identities without explicit provenance.

This avoids both forms of documentation drift: leaving stale claims current and retroactively rewriting historical evidence.

## Files changed in this sweep

- `README.md`
- `docs/CURRENT_STATE.md`
- `docs/PROJECT_STATUS.md`
- `docs/ISSUE_32_STATUS.md`
- `docs/ISSUE_64_STATUS.md`
- `docs/experiment/NEW_CANDIDATE_MANIFEST.md`
- `docs/formalism/hensel-general-formalism.md`
- `docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md`
- `docs/governance/P4_INDEPENDENT_CUSTODY_EXECUTION_RECORD_2026-09-05.md`
- `docs/governance/P8_VERIFICATION_CHECKLIST.md`
- `docs/governance/P8_P9_FREEZE_READINESS_2026-08-26.md`
- `docs/governance/NEXT_STAGE_EXPERT_PANEL_PLAN_2026-09-05.md`
- this hygiene record

## Explicit non-effects

This documentation work does **not**:

- change the designated runtime candidate;
- create or expose a blinding key, mapping, nonce, or recovery material;
- instantiate or close P4-A;
- close P7, P8, or final P9;
- create immutable freeze object F or verification record V;
- grant pilot authorization;
- execute or unblind an empirical pilot;
- establish PDMAL efficacy;
- convert synthetic/engineering evidence into empirical evidence;
- increase empirical N.

**Scientific state remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
