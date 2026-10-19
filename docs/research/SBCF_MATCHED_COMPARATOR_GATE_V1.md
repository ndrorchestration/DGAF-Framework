# SBCF matched comparator readiness gate v1

Status: **PRE-FREEZE / FAIL-CLOSED / NOT READY / NOT AUTHORIZED**.

This checkpoint prevents a methodological error: current comparator evidence is
not yet measured at the same policy-effect boundary. A cross-system score would
mix different effect semantics and evidence tiers unless the comparison
contract is frozen first.

## Pinned candidate identities

| System | Exact source | Reproduced evidence | Matched-effect tier |
|---|---|---|---|
| SBCF | DGAF draft #1389 at `97371dcd42b6cae5f88e2883d4adb24d65c5ad9f` | synthetic policy effects plus same-operator off-host witness/generation-floor runtime QA | `synthetic_effect` |
| OWASP ACS | `9c05f0402d76dea6b67a12a93672c2131137e572` | pinned upstream reference suite and bounded host behavior | `reference_runtime_effect` |
| NVIDIA OpenShell | v0.1.4 / `5a7728c304b5528e954e9ae900cf21f84e1a12b1` | Docker-backed sandbox network enforcement | `enforced_runtime_effect` |

These tiers describe the **effect boundary relevant to a matched study**. They
do not rank system quality. In particular, SBCF now has real runtime evidence
for its off-host witness and generation floor, but that does not convert its
synthetic policy-effect path into a matched real enforcement point.

## Why a matched benchmark is blocked

The same words do not yet mean the same experiment across all three systems.

- **Effect boundary:** OpenShell intercepts a real sandbox network effect. ACS
  currently has reproduced reference-runtime hook/policy behavior. SBCF still
  evaluates synthetic reference effects even though supporting witness controls
  run on real hosts.
- **Policy intent:** the three systems currently express scope and authority
  differently; a common mapping is not frozen.
- **Failure posture:** current controller-availability and decision-failure
  semantics are not normalized under one preregistered experimental posture.
- **Outcome witness:** no common independent effect receipt is defined across
  all systems.
- **Statistics:** no matched trial packet, allocation rule, exclusion policy,
  primary metric, power analysis, or multiple-comparison rule is frozen.
- **Independence:** no eligible outside operator is assigned to this matched
  comparator program.

Therefore `MATCHED_RUNTIME_READY=false`.

## Machine-readable fail-closed gate

`experiments/sbcf/fixtures/matched_comparator_readiness_v1.json` records exact
identities, matched-effect tiers, effect-boundary descriptions, and eleven
readiness gates. `experiments/sbcf/comparator_gate.py` validates a closed
schema and returns every unresolved blocker.

Important invariant: setting every administrative gate to true still cannot
return READY while SBCF or ACS remains below `enforced_runtime_effect`.
Unrelated runtime evidence therefore cannot silently upgrade a system into a
matched runtime-effect comparison.

A future READY result would mean only that the declared structural
prerequisites are present. It would not establish fairness, efficacy, parity,
or superiority without review of the frozen packet and raw evidence.

## Proposed common-denominator experiment

Do not execute until every readiness gate passes.

The first matched runtime study should include only effects each system can
mediate at a real pre-effect boundary under an equivalent policy intent:

1. unauthorized scoped effect — outside the active grant/rule; must not commit;
2. explicitly authorized scoped effect — exact allowed scope; should commit;
3. near-scope escape — same action class but different resource/destination;
   must not commit;
4. revoked or expired authority — previously permitted effect must stop within
   a preregistered propagation bound;
5. control-plane uncertainty — one shared fail-closed experimental posture.

L7 method/path behavior should remain a separate stratum unless every system
implements an equivalent real boundary. Dialogue or semantic-observation arms
must not be layered onto the competitor comparison until the underlying effect
boundary is held constant.

## Minimum packet before execution

Freeze and hash:

- exact source/build/runtime identities;
- common effect adapter and policy-intent mapping;
- environment/container/image identities;
- trial cases and reference judgments;
- fail-open/fail-closed posture;
- policy propagation/staleness bounds;
- raw effect receipts and common outcome observation;
- exclusions and abort conditions;
- randomization seed generation and allocation;
- primary/secondary metrics;
- statistical tests, confidence intervals, and multiple-comparison handling;
- eligible outside operator and reviewer identities;
- raw artifact retention and hash manifest.

Any unresolved field remains BLOCKED.

## Current disposition

The executable gate is expected to return NOT READY. That is the correct
result. Comparator reproduction has improved, but no matched runtime efficacy
study is authorized. The next engineering requirement for this track is an SBCF
effect adapter/PEP at a real observable boundary plus a frozen common semantic
mapping; ACS also requires evidence at the same matched effect boundary before
a three-system runtime comparison can be READY.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
