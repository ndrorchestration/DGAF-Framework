# DGAF/PDMAL Project Status

**Status date:** 2026-09-06  
**Live v0.7.6 source boundary:** `972edd41f16c69c6912af08c7d6c3aa627fdd8a9`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Historical runtime-evidence candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Historical candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Historical candidate deployment:** `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`  
**Final v0.7.6 candidate:** NOT DESIGNATED — tracked by Issue #309  
**Pilot status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED  
**Empirical N:** 0

## Executive state

DGAF is in pre-freeze closure. PR #308 changed the experimental apparatus to protocol v0.7.6 / artifact schema 1.1 at `972edd41…`. The previously designated runtime candidate `7c1cc4bb…` retains valid exact-scope evidence but, under Issue #309, is historical provenance only and is not eligible to become the final freeze/N=1 candidate.

No replacement final candidate has yet been explicitly designated. Issue #309 is the convergence authority for selecting an exact immutable v0.7.6 descendant and classifying or regenerating only the evidence that is actually identity-dependent.

Historical P1, P2, P3, P5, P6, and P6a results remain closed/verified within their explicitly bounded engineering/governance evidence contracts for `7c1cc4bb…`; they do not automatically close those predicates for the future final candidate. P4 remains operationally open because no admissible H/I/T custody mode has been instantiated and verified. P7 final binding, P8 immutable freeze/readiness, final P9, freeze establishment, and authorization remain open or absent.

None of these engineering states establishes empirical efficacy.

## Gate board

| Gate / control | Status | Evidence / limitation |
|---|---|---|
| Corrected apparatus provenance | CANONICAL ANCHOR | `2a54a67d…` |
| Consolidated control-state anchor | CANONICAL CONTROL/PROVENANCE ANCHOR | `89be386b…`; not a final-candidate designation |
| Historical runtime evidence | VERIFIED AT EXACT SCOPE | `7c1cc4bb…` / `586c00d6…` / `dpl_8Msuf…` |
| Final v0.7.6 candidate | NOT DESIGNATED | Issue #309 |
| P4 | OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED | H/I/T custody architecture defined; no real custody instance verified |
| P7 | ADOPTED / FINAL BINDING OPEN | final candidate and custody identities incomplete |
| P8 | OPEN / FAIL-CLOSED | immutable freeze not established/verified |
| P9 | NOT EXECUTED / OPEN | final frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance transition |
| Empirical data | N = 0 | no authorized pilot execution |

## Historical exact-scope execution evidence

On 2026-09-05, both `7c1cc4bb…`-scoped runtime evidence records were successfully re-retrieved:

- P2 artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

This is not a new runtime execution. P3/P5 evidence from run `33939955138` and the P6 round-trip record also remain valid within their recorded pre-v0.7.6 candidate scope. Issue #309 governs whether each item is transferable by construct, historical only, source/structure re-verifiable, runtime/deployment re-verifiable, re-archive/rebind, or not yet executable.

## P4 custody state

The canonical P4 control is effective control separation rather than a mandatory two-human topology:

- `H`: genuinely distinct human custody;
- `I`: institutional/third-party custody outside the analyst's unilateral control;
- `T`: independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

No H/I/T execution instance exists yet, so P4-A remains OPEN / NOT EXECUTED. Current Mode-T engineering and green CI are synthetic/mechanism evidence only and do not establish real Confidential Space admission or custody.

## Engineering-quality state

Issue #270 is **CLOSED / COMPLETED**. Its remediation restored a clean current-lineage flake8/Black/isort/mypy baseline and converted those checks to fail-closed workflow gates.

Issue #277 remains **OPEN** for branch-protection/ruleset enforcement. Current protected `main` requires only `PPTL CI`; broader merge-critical checks are not yet proven repository-required. This configuration gap is separate from the repaired workflow behavior.

## Reconciliation interpretation

PR #279 merged exact head `1373672b8db03d95d714737c1769d91f2998c164` as `c9765741cf8c3908bf35f81f46fe9a6ab681cd4e` and correctly replaced self-staling “current main” language in Issue #270 documentation with immutable technical-hardening-boundary terminology. That documentation-only change did not alter scientific state.

The control-state anchor `89be386b…` remains valid for its provenance/control role. It is not replaced merely because live source advanced, and it does not itself designate the final experimental candidate.

## Required closure sequence

`complete candidate-relevant P4 apparatus work → explicitly designate exact v0.7.6 final candidate under #309 → classify/regenerate identity-dependent evidence → close real P4-A custody → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
