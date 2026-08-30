# DGAF v1 Execution Readiness

**Status:** VALIDATION IN PROGRESS / NON-AUTHORIZING  
**Date:** 2026-08-29

## Candidate

PR #139: `feat/dgaf-v1-control-plane-finalize-20260829`

Current engineering head must be resolved directly from GitHub for every execution. The authoritative candidate SHA is the exact PR head reported by GitHub at the time of each execution. A CI result is valid only for the SHA actually checked out by that run.

## Required CI checks

- `pptl/tests/test_v1_control_plane.py`
- `pptl/tests/test_v1_tgl_integration.py`
- `pptl/tests/test_v1_adversarial_contract.py`
- `pptl/tests/test_v1_capability_boundaries.py`
- import/package integrity
- exact current-head checkout identity
- applicable repository/evidence/security workflows

## Adversarial acceptance criteria

The candidate must demonstrate, on the exact executed head:

1. child authority/tool/data/risk/resource scopes never widen;
2. child provenance metadata cannot overwrite inherited parent provenance;
3. lifecycle violations fail closed;
4. active nonterminal tasks have a safe terminal abort path;
5. task identity fields cannot be externally reassigned after construction;
6. lifecycle state, TGL status/seal, concurrency state, and runner configuration cannot be externally reassigned;
7. public task, ledger, state-registry, branch-registry, and event surfaces expose no mutating capability;
8. recursive depth and active concurrency ceilings are enforced;
9. budget overruns escalate without leaking active slots or persistent reservations;
10. repeated canonical states are rejected according to the documented state-identity contract;
11. child state is registered only after successful submission and reflects the post-submit lifecycle state;
12. TGL terminal failures and runner exceptions propagate to control-plane escalation;
13. merge readiness requires a current sealed TGL `PASS`; stale results cannot be reused after a new evaluation starts;
14. consequential commit cannot occur without explicit authorization, duplicate authorization, or commit replay;
15. commit request payloads and branch provenance remain immutable after capture;
16. multiple branches sharing a state ID retain distinct branch identities;
17. branch lineage cannot cycle;
18. PDMAL remains outside the generic control-plane authorization path.

## Evidence interpretation

Engineering CI, deterministic fixtures, synthetic evaluator outputs, deployment readiness, and documentation consistency are implementation evidence only. They do not constitute PDMAL efficacy evidence, experimental authorization, or a new freeze.

## Non-authorizing constraint

Passing engineering CI does not create a PDMAL freeze, authorize a pilot, increase empirical N, or establish efficacy.

Experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.
