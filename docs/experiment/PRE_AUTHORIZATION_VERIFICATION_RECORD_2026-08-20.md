# PDMAL Pre-Authorization Verification Record — 2026-08-20

## Current disposition

**BLOCKED / NOT AUTHORIZED**

This record is the consolidated closure checklist for the corrected pilot apparatus. It deliberately distinguishes verified engineering properties from items that require execution evidence or human methodological/governance decisions.

## Historical evidence boundary

- Historical implementation freeze: `3510b86889cd341f7a7cf9ab684fd37b2fafd758`.
- Historical executor implementation: `75a7f18c2d5268075e6fc8064eb9a79018845da0`.
- Historical acceptance: 2 seeds × 180 = 360 observations; all SUCCESS.
- Empirical N: `0`.

The historical freeze is not reused for the corrected runner because the live audit identified material runner defects.

## Corrected candidate

- Runner correction: `fec7a6f577373aeb5037b8b5960bcfa7e0384a0d`.
- Pilot artifact schema: `b1744e02e643515c2b49d8736e036bc40ecf4d7d`.
- Security suite: `6a95dffe985d5e40ef515f39b7d407068580c0de`.
- Candidate branch: `chore/preauth-completeness-2026-08-20`.

A new freeze SHA must be created only after the following gates pass.

## Verification matrix

| Gate | State | Required evidence |
|---|---|---|
| Runner SHA binding | IMPLEMENTED | Exact full-SHA comparison in runner; wrong-SHA test |
| Pilot authorization gate | IMPLEMENTED | Explicit environment authorization required |
| Blinding | IMPLEMENTED PRIMITIVE | HMAC blinding; operational custody still requires external evidence |
| Real condition hidden from artifact | IMPLEMENTED | Pilot artifact contains blinded condition ID only |
| Artifact internal hash | IMPLEMENTED | Canonical record SHA validated by pilot schema |
| Artifact sidecar | IMPLEMENTED | SHA-256 sidecar generation |
| Task identity | IMPLEMENTED | Pilot path uses `ConsensusTask`; security test rejects scripted substitution in pilot AST |
| Runtime ceiling | IMPLEMENTED | 300s seed ceiling; boundary test |
| Python 3.12.0 | OPEN | Fresh locked environment verification |
| NumPy 2.5.1 | OPEN | Exact environment verification |
| NetworkX 3.6.1 | OPEN | Exact environment verification |
| One-seed smoke | OPEN | Full artifact/schema/sidecar/provenance check |
| Security suite CI | OPEN | GitHub Actions pass required |
| Topology fingerprints | OPEN | Final fingerprint-to-manifest reconciliation |
| Durable retention | OPEN | Archive location and checksum evidence |
| Primary contrast | OPEN | Explicit methodological adjudication |
| Analysis implementation SHA | OPEN | Identify, verify, freeze implementation/configuration |
| New freeze manifest | BLOCKED | Depends on all required gates above |
| Pilot authorization | NOT GRANTED | Human governance decision |
| Empirical N | 0 | Must remain 0 until authorized pilot |

## Sample-size control

The repository-local planning utility specifies a paired-difference normal approximation with alpha 0.05, power 0.80, MDD 0.15, and externally supplied paired-difference SD. The external SD must not be estimated from unauthorized pilot observations. Any final sample-size claim must be explicitly recorded before authorization.

## Analysis control

The repository contains the planning utility but the previously reported external analysis-plan and pipeline documents were not located at their expected repository paths during the audit. Exact authoritative paths/SHAs must be established before unblinding. The analysis implementation and configuration must be frozen before unblinding.

## Authorization rule

No combination of passing engineering tests changes authorization state. Authorization requires an explicit governance decision after the pre-authorization matrix is closed.

```text
Corrected apparatus verified:   NO
New freeze created:             NO
Pilot authorized:               NO
Empirical N:                    0
```
