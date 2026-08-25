# DGAF Ecosystem Boundary Crosswalk — 2026-08-25

This crosswalk connects the Pattern Commons, DGAF/PDMAL research, evidence governance, commercialization, security, privacy, and future certification boundaries.

## Architectural map

| Concern | Canonical layer | Primary DGAF reference | Epistemic rule |
|---|---|---|---|
| Pattern identity/provenance | Pattern Commons | `docs/PATTERN_COMMONS_ARCHITECTURE.md` | Registry membership ≠ truth |
| DGAF implementation | DGAF | `README.md`, source/tests | Implementation ≠ validation |
| PDMAL experiment | Research/evidence | `docs/experiment/`, `docs/evidence/` | Apparatus ≠ empirical result |
| Claims/evidence | Evidence governance | evidence registries/policies | Evidence must match claim scope |
| Commercialization | Asset governance | `docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md` | Commercial value ≠ technical validity |
| Trademark/certification | Legal/brand governance | `docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md` | Certification ≠ universal guarantee |
| Security | Security governance | `SECURITY.md` + repository controls | Security-sensitive ≠ proprietary by default |
| Privacy/confidentiality | Data governance | openness boundary | Private data must not be published for transparency theater |
| Cross-repository relationships | Ecosystem governance | `CROSS_REF.md` + Pattern Commons | Shared terms ≠ implementation equivalence |
| Funding | Sustainability | `.github/FUNDING.yml` | Funding ≠ endorsement or evidence |

## Cross/interdisciplinary relationships

### Software engineering ↔ epistemology

A reproducible build, passing unit test, or implemented function establishes an implementation fact; it does not automatically establish the broader claim that the system is effective, safe, convergent, or generally applicable.

### Mathematics ↔ empirical science

A mathematically coherent definition or derivation is distinct from empirical validation. Conversely, an observed effect does not automatically establish the proposed mathematical explanation.

### AI governance ↔ security

A governance control may reduce a defined risk without constituting a security guarantee. Security-sensitive implementation details may require controlled disclosure even when the associated governance claim remains public.

### Governance ↔ commercial strategy

An artifact can be commercially valuable while remaining open. The value may reside in implementation expertise, managed operation, assurance, integration, support, or domain-specific deployment rather than in hiding the reference mechanism.

### Open source ↔ trademark/certification

Apache-2.0 software rights are distinct from permission to claim official endorsement or certification. See the trademark/certification policy.

### Research ↔ commercialization

Commercial services should not retroactively convert unsupported research into validated product claims. Public claims must preserve the same evidence boundaries whether the surrounding offering is free, sponsored, or paid.

## Asset-class decision rule

For each artifact, determine independently:

1. epistemic status;
2. functional role;
3. public-reproducibility necessity;
4. privacy/security constraints;
5. licensing constraints;
6. commercial role;
7. trademark/certification role;
8. cross-repository provenance.

No single attribute should determine the others.

## Current unresolved questions

- Exact asset-by-asset classification across all repositories.
- Whether a dedicated Pattern Commons repository should be created.
- Whether the existing Apache-2.0 license remains the intended long-term license for all future contributions and artifacts.
- Which assets, if any, have genuine proprietary value and are not merely convenient to keep private.
- Whether and when a DGAF certification program is legally and empirically defensible.
- What objective evidence threshold should be required for paid assurance claims.
- How contributor rights and commercial participation should be handled as adoption grows.
- Which external standards, frameworks, or certification schemes can be safely cross-mapped without implying equivalence.

## Current non-decisions

This crosswalk does **not**:

- create a certification program;
- create new proprietary rights over existing Apache-2.0 code;
- authorize trademark claims;
- establish empirical efficacy;
- promote the four candidate NDR concepts to canonical P-numbers;
- create the Pattern Commons repository;
- move or delete existing artifacts.
