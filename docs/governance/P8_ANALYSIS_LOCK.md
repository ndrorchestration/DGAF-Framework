# P8 Analysis Lock

**Status:** OPEN / PRE-FREEZE
**Authority:** DGAF/PDMAL experimental-design control
**Purpose:** Bind the executable primary analysis to the adopted P7 scientific target before any unblinding or empirical interpretation.

## P7 inputs now fixed

- Primary contrast: full `dgaf` versus `null`.
- Primary endpoint: FFCR.
- Statistical unit: seed.
- Seed pairing key: seed identity.
- Seed-level primary difference: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`.
- Primary estimand: expected seed-level paired difference over the pre-specified seed population.
- Positive difference favors DGAF.
- Secondary/exploratory family: PDMAL vs Ring; condition × topology interaction; structural/execution diagnostics.
- No post-observation weighting changes are permitted.
- No outcome-dependent seed exclusion or silent seed-level imputation is permitted.

## Required P8 bindings

The following values must be populated from the executable analysis implementation before P8 can close:

| Binding | Required state |
|---|---|
| Analysis implementation path | OPEN — exact repository path required |
| Analysis implementation SHA | OPEN — exact candidate commit/blob required |
| Configuration path | OPEN — exact repository path or canonical configuration required |
| Configuration SHA | OPEN — canonical digest required |
| Bootstrap resample count | OPEN — must be fixed before unblinding |
| Bootstrap RNG policy | OPEN — must be fixed before unblinding |
| Confidence interval convention | OPEN — must be fixed before unblinding |
| Alpha / decision threshold | OPEN — must be fixed before unblinding |
| Exclusion/missing-data executable behavior | OPEN — must match adopted P7 contract |
| Secondary multiplicity procedure | OPEN — must be fixed before confirmatory interpretation |
| Protocol identity | OPEN — exact protocol blob SHA required after final protocol commit |
| Manifest identity | OPEN — exact freeze/manifest binding required |

## Lock rules

1. No empirical observation may be used to choose any open binding.
2. No unblinding may occur before every required binding is populated and independently checked.
3. Changing a locked binding after unblinding invalidates the current analysis lock and requires a new governance decision.
4. Historical analysis or characterization artifacts cannot substitute for the exact candidate implementation/configuration binding.
5. P8 closure does not authorize the pilot; authorization remains a separate governance transition after freeze and P9 verification.

## Current blocker

The repository currently contains the P7 scientific target and analysis-control boundary, but an independently identifiable executable analysis implementation/configuration with all required P8 parameters is not yet established as the locked artifact. Therefore P8 is intentionally **OPEN**, not inferred closed from documentation.

## Required next actions

1. Locate or implement the executable seed-level primary analysis.
2. Add deterministic configuration for bootstrap, RNG, interval, alpha/decision threshold, exclusions, and secondary multiplicity.
3. Add tests covering the adopted P7 contract and negative-path behavior.
4. Compute canonical implementation/configuration hashes.
5. Bind those hashes to the exact protocol and candidate manifest.
6. Run candidate-scoped verification.
7. Close P8 only after the resulting lock record is internally consistent.

**Pilot authorization:** NOT GRANTED.
**Empirical N:** 0.
**New freeze:** NOT CREATED.
