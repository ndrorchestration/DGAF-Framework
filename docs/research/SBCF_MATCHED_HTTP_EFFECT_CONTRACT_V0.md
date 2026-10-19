# SBCF matched HTTP effect semantics candidate v0

Status: **CANDIDATE / NOT FROZEN / NOT READY / NOT AUTHORIZED**.

This candidate narrows the future matched-comparator question to one common
consequence class: an HTTP request observed at an external receiver. It reuses
the fair-comparison requirements already present in
`docs/qa/COMPARATIVE_GOVERNANCE_BENCHMARK_SPEC.md`: identical fixtures, the
same consequence boundary, no baseline-specific hidden information, retained
negative outcomes, and frozen implementations before result inspection.

It does not authorize data collection or a cross-system benchmark.

## Common effect identity

The proposed effect identity is the ordered semantic tuple:

- trial ID;
- HTTP method;
- scheme;
- host;
- port;
- path;
- request-body SHA-256.

Headers are not currently part of the identity. Query and fragment semantics are
also excluded from v0. Any future inclusion requires a new contract version
rather than silent reinterpretation.

## Common decision and outcome semantics

Two decision states are sufficient for v0:

- `ALLOW` — the tested system admits the declared effect;
- `DENY` — the tested system refuses before the effect boundary.

Two expected receiver outcomes are used:

- `COMMITTED` — an external receiver observes the exact declared effect
  identity;
- `NOT_OBSERVED` — the system reports NOT_STARTED and the external receiver
  does not observe that identity within a separately frozen observation bound.

The negative observation bound is intentionally **unset** in the current
fixture. Therefore the contract cannot be frozen yet. Absence of an observation
without a predeclared bound is not treated as proof that an effect did not
occur.

## Five candidate cases

1. **Exact allow:** active authority, exact target, exact method, control plane
   available → ALLOW / COMMITTED.
2. **Adjacent host:** active authority, adjacent target, exact method, control
   plane available → DENY / NOT_OBSERVED.
3. **Adjacent method:** active authority, exact target, adjacent method, control
   plane available → DENY / NOT_OBSERVED.
4. **Revoked authority:** revoked authority, otherwise exact request, control
   plane available → DENY / NOT_OBSERVED.
5. **Control-plane unavailable:** active authority and exact request, but the
   required policy/control plane is unavailable → DENY / NOT_OBSERVED.

These cases are deliberately narrower than the broader governance benchmark.
They test one consequence boundary before composition, epistemic authority, or
semantic-observation arms are layered on top.

## Current system mappings

- **SBCF:** candidate reference-runtime mapping. The bounded loopback adapter
  performs a real HTTP effect through the accepted DGAF capability PEP, but the
  strict direct-socket counterexample shows same-process bypass remains.
- **OWASP ACS:** **UNRESOLVED**. The reproduced reference suite is not yet
  mapped to this exact external HTTP receiver/effect identity.
- **NVIDIA OpenShell:** candidate enforced-runtime mapping based on its
  reproduced sandbox network boundary. The exact v0 five-case adapter/mapping
  is still not frozen.

No system mapping is currently `FROZEN`.

## Machine-readable status

`experiments/sbcf/fixtures/matched_http_effect_contract_v0.json` records the
candidate semantics. `experiments/sbcf/matched_effect_contract.py` enforces a
closed schema and returns blockers.

Current structural blockers are:

- contract status is not frozen;
- negative observation bound is not frozen;
- SBCF mapping is not frozen;
- ACS mapping is unresolved;
- OpenShell mapping is not frozen.

A future structurally READY result would mean only that the declared semantic
contract has been frozen. It would not establish efficacy, fairness, parity,
superiority, or independence.

## Next obligations

Before `common_effect_semantics_frozen` can become true:

1. implement/review an ACS adapter for this exact HTTP effect identity;
2. implement/review the OpenShell v0 five-case mapping rather than inferring it
   from the earlier bounded reproduction;
3. select and preregister a negative observation bound;
4. define receiver custody and raw receipt retention;
5. freeze exact system/build/runtime identities and fixture packet;
6. obtain eligible outside-operator and reviewer assignment.

Until then, the comparator readiness gate remains fail-closed.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
