# DGAF Transversal Audit Template v1.0

**Status:** Control template; non-authoritative until ratified

## Subject

- Concept / ID:
- Human-readable name:
- Audit date:
- Source commit:
- Owner:

## Trace across dimensions

| Dimension | Required question | Result | Source | Status |
|---|---|---|---|---|
| Identity | Is identity stable and unique? | | | |
| Taxonomy | Is classification unambiguous? | | | |
| Temporal | Are event/effective/discovery/resolution times distinct? | | | |
| Pattern | Is pattern identity/version/class/trigger explicit? | | | |
| Agentic | Are agent/seat/formation/variant/state roles distinct? | | | |
| Layer | Is the control layer explicit? | | | |
| Specification | Does prose define the same semantics as implementation? | | | |
| Implementation | Is there an exact implementation reference? | | | |
| Test | Are relevant invariants and failure conditions tested? | | | |
| Evidence | Is evidence candidate/run/configuration bound? | | | |
| Governance | Is authority and binding strength explicit? | | | |
| Historical | Are older states preserved without promotion? | | | |

## Cross-layer checks

1. L0 identity does not conflict with L1 structure.
2. L1 invariants match L2 implementation.
3. L2 execution produces evidence sufficient for L3 measurement.
4. L3 conclusions do not exceed evidence status.
5. L4 governance decisions reference the exact lower-layer state they govern.

## Failure classes

- `MATHEMATICAL_DEFECT`
- `IDENTITY_COLLISION`
- `LINEAGE_BREAK`
- `SCOPE_OR_AUTHORITY_CONFLICT`
- `TEMPORAL_DRIFT`
- `DOCUMENTATION_DRIFT`
- `IMPLEMENTATION_DRIFT`
- `EVIDENCE_CONTAMINATION`
- `MISSING_DEPENDENCY`
- `HISTORICAL_BOUNDARY_FAILURE`

## Disposition

- Confirmed
- Contradiction
- Gap
- Duplicate review
- Historical
- Candidate

## Promotion rule

No unresolved transversal defect may be hidden by a summary document. The summary must inherit the most restrictive applicable epistemic status and explicitly link the underlying defect.

## Safety boundary

Completion of this audit template does not authorize freeze, pilot execution, unblinding, production certification, or empirical claims.
