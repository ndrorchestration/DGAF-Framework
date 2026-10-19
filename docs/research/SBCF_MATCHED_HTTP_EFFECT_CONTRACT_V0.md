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

Headers are not generally part of the HTTP effect identity. The one fixed
exception is receiver correlation for the already-declared `trial_id` field:
the candidate requires the sender to carry that value in
`X-SBCF-Trial-ID`, and the receiver copies that exact header value into the
receipt's `trial_id` field. The header name is therefore witness transport
metadata for an identity field, not an invitation to compare arbitrary
headers. Query and fragment semantics remain excluded from v0. Any future
inclusion requires a new contract version rather than silent reinterpretation.

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

The current SBCF candidate mapping is evaluated on top of main-target draft #1395 at exact verification head `5526d3535cdd07d15c7d11bede66ec1a60a6fca9`; exact system/source identities remain governed by the parent matched-comparator manifest rather than duplicated into this semantic contract.

- **SBCF:** candidate reference-runtime mapping. The bounded loopback adapter
  performs a real HTTP effect through the accepted DGAF capability PEP, but the
  strict direct-socket counterexample shows same-process bypass remains.
- **OWASP ACS:** **UNRESOLVED**, with a partial executable candidate mapping.
  At pinned ACS commit `9c05f0402d76dea6b67a12a93672c2131137e572`,
  the stock egress policy can express exact-host allow and adjacent-host deny.
  The candidate harness uses an explicit, unfrozen benchmark fixture overlay
  whose only policy-data change is an egress allowlist containing
  `127.0.0.1`; the pinned upstream checkout remains unmodified. Adjacent
  HTTP method is not bound by the stock egress policy, authority revocation
  has no frozen matched semantic, and control-plane-unavailable behavior still
  depends on an unfrozen failure-posture mapping. Those three cases therefore
  remain blockers rather than being synthesized by the adapter.
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

1. execute/review the ACS partial candidate mapping, then resolve the three
   still-unmapped semantics without inventing controls that the pinned ACS
   runtime does not demonstrate;
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
