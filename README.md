# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, formation governance, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and current pre-freeze governance state. Individual claims require exact evidence and defined scope. Historical evidence remains scoped to the SHA/run/deployment that produced it.

## Current project state — 2026-09-01

The DGAF/PDMAL experimental track remains **PRE-FREEZE / FAIL-CLOSED**. No pilot authorization has been granted and empirical **N = 0**.

`main` is documentation/control-plane lineage. The current mainline runtime candidate is `92ff830b1c67413df745e37087e6447c9c251b9a` with exact tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`. The latest controlled completion candidate is `562753b3053b3566b0fcad1b0b1df151d7de119a` on `completion/2026-09-01-exact-candidate`; these identities are not interchangeable.

## Canonical engineering lane

The completion work is maintained in controlled candidate branches and must be explicitly rebound before any freeze or experiment. Current engineering controls include candidate identity checks, provenance binding, fail-closed governance, and independent verification paths. Documentation commits do not silently redefine the experimental candidate.

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
| Latest completion candidate | `562753b…` / branch `completion/2026-09-01-exact-candidate` |
| P2 runtime verification | `VERIFIED` for `92ff830b…` / deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| P6a CORS verification | `VERIFIED` for `92ff830b…` / deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| P9 scoped independent verification | `PASS` for `562753b…` via run `33567199896` |
| P3 | Open |
| P4 | Open |
| P5 | Open |
| P6 | Open / fail-closed |
| P7 | Adopted / final exact binding open |
| P8 | Open / fail-closed |
| Broader P9 closure | Open / conditional |
| New immutable freeze | Not created |
| Pilot authorization | Not granted |
| Empirical N | 0 |

## Latest P9 scoped result

Run `33567199896` completed successfully for exact candidate `562753b3053b3566b0fcad1b0b1df151d7de119a`.

The independent verification workflow:

- verified `git rev-parse HEAD == GITHUB_SHA`;
- generated a deterministic case through the DGAF/Python path;
- independently canonicalized it with `jq -S -c` and hashed it with `sha256sum`;
- required digest equality;
- ran `tests/test_agent_authority_matrix.py` with `4 passed`;
- emitted and uploaded an independent P9 evidence artifact.

Artifact ID: `9823570326`  
Artifact digest: `sha256:8e3435a3af0dc5de7376d970b9f1665a18db8ff04b26a2c0eaae8acf8b095d85`

This is **scoped verification evidence**, not a declaration that all P9 prerequisites are closed. It does not establish empirical efficacy, authorization, or a freeze.

## Evidence boundary

Engineering CI success, synthetic fixtures, deployment readiness, runtime predicate verification, or documentation updates do not constitute PDMAL efficacy evidence or experimental authorization. Historical evidence is not transferable across SHA/run/deployment boundaries without fresh exact-scope evidence.

## Historical-priority boundary

DGAF is not established as first in the individual mechanisms of agent governance, dynamic formation, authority, veto, escalation, idempotency, provenance, exact artifact identity, candidate immutability, or independent verification. The remaining historical hypothesis is a potentially distinctive cross-domain integration coupling formation-state governance to candidate-bound experimental verification and authorization. See `docs/research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
