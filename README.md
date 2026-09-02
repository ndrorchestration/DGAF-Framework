# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, formation governance, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and current pre-freeze governance state. Individual claims require exact evidence and defined scope. Historical evidence remains scoped to the SHA/run/deployment that produced it.

## Current project state — 2026-09-02

The DGAF/PDMAL experimental track remains **PRE-FREEZE / FAIL-CLOSED**. No pilot authorization has been granted and empirical **N = 0**.

`main` is documentation/control-plane lineage. The current mainline runtime candidate is `92ff830b1c67413df745e37087e6447c9c251b9a` with exact tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`. The latest controlled completion candidate is `a43219b4ed91fff8615f6c655ab3d17ca871fc29` on `completion/2026-09-01-exact-candidate`; these identities are not interchangeable.

## Active remediation boundary

PR #188 / branch `remediation/p35-premise-hook-2026-09-01` is currently at `d83ea74c0f7ef7dd3e39a25345d6b201770a370c`. The candidate-scoped P-35 remediation has passed exact-head pre-freeze runner validation in run `33590352168`. The uploaded PRE-FREEZE manifest is artifact `9831586822` with workflow artifact digest `sha256:dedacba56b8430fd995c4230e52fe208d2380f5e5015fa3816073cda3e9d774e`.

This remediation evidence is engineering/pre-freeze evidence only. It does not redefine the current runtime/completion candidate, establish P8 closure, create a freeze, authorize the pilot, or transfer evidence from `a43219b…`.

## Canonical engineering lane

The completion work is maintained in controlled candidate branches and must be explicitly rebound before any freeze or experiment. Current engineering controls include candidate identity checks, provenance binding, fail-closed governance, and independent verification paths. Documentation commits do not silently redefine the experimental candidate.

The trusted completion controller is active on `main`. Its latest successful evaluation used the workflow-run candidate input `a43219b4ed91fff8615f6c655ab3d17ca871fc29`, reconciled exact-candidate P9 evidence, and returned `OPEN_GAPS`. It does not freeze or authorize a pilot.

## Current TGL contract boundary

- required unwired gates are `SKIP` and reduce the turn to `ESCALATE`;
- `WARN` propagates to `TurnStatus.WARN` unless a stronger failure applies;
- HPG is conditional on Phi-Closure and cannot run after terminal failure;
- terminal failures stop downstream gate execution;
- the final audit seal covers the complete gate set, including Herald;
- invalid gate outcomes do not silently become PASS.

## Canonical agent-role boundary

- Sentinel-Phi — canonical governance/security identity.
- Professor Prodigy — formalization/proof; non-orchestrating.
- DemiJoule — advisory resource/constraint analysis; no independent normative authorization.
- Reciprocity — fairness and affected-party review.
- Herald — evidence/public-surface publication; cannot manufacture evidence or approval.
- Amethyst — meta-orchestration/lifecycle coordination.
- COLLEEN — continuity/archive/provenance/routing integrity.
- Apogee — independent evidence/integrity review.

Generic execution roles do not create or elevate agent authority.

## Experimental gate state

| Boundary | Status |
|---|---|
| Corrected apparatus source | `2a54a67d…` |
| Mainline runtime candidate | `92ff830b…` / tree `73cf3ad…` |
| Latest completion candidate | `a43219b…` / branch `completion/2026-09-01-exact-candidate` |
| Active P-35 remediation | `d83ea74c…` / PR #188 / engineering only |
| P-35 pre-freeze runner verification | `PASS` for `d83ea74c…` via run `33590352168`; manifest artifact `9831586822` |
| P2 runtime verification | `VERIFIED` for `92ff830b…` / deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| P6a CORS verification | `VERIFIED` for `92ff830b…` / deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| P3 | Candidate-bound structural/dry-run evidence present; operational closure remains OPEN |
| P4 | OPEN — dry-run blinding evidence is not operational closure |
| P5 | OPEN — dry-run reproducibility evidence is not full closure |
| P6 | OPEN / fail-closed — durable external archive round-trip still required |
| P7 | Technically adjudicated / formally OPEN; exact authority adoption and freeze binding remain required |
| P8 | OPEN / fail-closed; P-35 remediation is verified at engineering/pre-freeze scope but a new experimental candidate is still required |
| P9 scoped independent verification | `PASS` for `a43219b…` via run `33572123857`; new candidate re-verification required |
| Trusted completion controller | `SUCCESS` — `OPEN_GAPS` for `a43219b…` |
| New immutable freeze | Not created |
| Pilot authorization | Not granted |
| Empirical N | 0 |

## Latest remediation evidence

The exact-head PDMAL Pre-Freeze Runner Validation run `33590352168` completed successfully against `d83ea74c0f7ef7dd3e39a25345d6b201770a370c`.

The workflow completed exact checkout, hash-locked dependency installation, the full pre-freeze contract suite including `test_run_pilot_p35.py`, contract-mode execution, pilot-mode failure without freeze/authorization, artifact schema/integrity checks, and PRE-FREEZE manifest upload.

The new remediation head also corrected the P-35 premise-KILL audit-return path so that a sealed KILL audit is retained and returned to the adapter rather than re-raised and discarded.

This evidence establishes the remediation behavior at engineering/pre-freeze scope. It is not efficacy evidence, does not close P8, and does not authorize experimentation.

## Latest exact-candidate evidence

### PDMAL instrumentation dry run

Run `33572123862` completed successfully against exact candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

Latest rerun evidence:

- artifact ID `9825740072`, ZIP digest `sha256:1a9f520bac2bf12ca8386c5c050489620028657866e4fee66e64905507ec31ae`;
- inner CSV SHA-256 `c12098da63ae1508edbb350799360e1edccfebb16c9d0faf0db4d593ffea8ce2`;
- evidence registry artifact `9825740649`, ZIP digest `sha256:c6c2fda4ce18d476ef95927a1430193ef34631dcce928c15695d43826678a205`.

The rerun verified exact checkout identity, deterministic smoke behavior, RNG stream separation, structural tests, schema/checksum validation, artifact round-trip retrieval, and environment fingerprint capture. These are engineering/structural controls, not efficacy evidence. The source registry still emits P4/P5/P6 as `VERIFIED`; the trusted external controller conservatively reclassifies those statuses to `OPEN` because the current governance contract requires stronger candidate-bound closure evidence.

### P9 independent verification

Run `33572123857` completed successfully against exact candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

The independent verification workflow:

- verified exact checkout identity (`HEAD == GITHUB_SHA`);
- independently canonicalized the deterministic case with `jq -S -c` and hashed it with `sha256sum`;
- required digest equality;
- ran the authority-identity regression with `4 passed`;
- retained exact-candidate P9 evidence with authorization marked external and empirical execution requested as false.

The latest P9 evidence artifact is `9825660346` with ZIP digest `sha256:cf5e475c31bd9258731dcec3e6f36588f9fbfa80c3bb787419b54770ccae7976`.

This is **scoped verification evidence**, not a declaration that all P9 prerequisites are closed. It does not establish empirical efficacy, authorization, or a freeze.

## Trusted completion-controller result

The trusted controller run `33573171970` successfully accepted the exact candidate SHA as workflow-run data, retrieved the exact-candidate evidence registry, retrieved and validated P9 evidence, reconciled P9 into the registry, and produced `OPEN_GAPS`.

The controller's blocking predicates were:

- **P2 — OPEN:** exact completion-candidate runtime verification is still required.
- **P4 — OPEN:** structural/dry-run evidence does not satisfy the current operational closure predicate.
- **P5 — OPEN:** structural/dry-run reproducibility evidence does not satisfy the full closure predicate.
- **P6 — OPEN:** the current run performed artifact round-trip custody, but the governance checklist requires durable external archive write, independent retrieval, hash equality, and retention binding.
- **P7 — OPEN:** formal authority adoption and exact freeze binding remain outstanding.
- **P8 — FAIL_CLOSED:** current-candidate analysis lock is not established.

P3 and scoped P9 were present as exact-candidate evidence. The controller explicitly reported `freeze_authorized=false`, `pilot_authorized=false`, and `empirical_execution_requested=false`.

## Evidence boundary

Engineering CI success, synthetic fixtures, deployment readiness, runtime predicate verification, or documentation updates do not constitute PDMAL efficacy evidence or experimental authorization. Historical evidence is not transferable across SHA/run/deployment boundaries without fresh exact-scope evidence.

## Historical-priority boundary

DGAF is not established as first in the individual mechanisms of agent governance, dynamic formation, authority, veto, escalation, idempotency, provenance, exact artifact identity, candidate immutability, or independent verification. The remaining historical hypothesis is a potentially distinctive cross-domain integration coupling formation-state governance to candidate-bound experimental verification and authorization. See `docs/research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
