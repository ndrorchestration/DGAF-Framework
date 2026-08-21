# PDMAL Freeze Manifest Reconciliation — 2026-08-20

## Purpose

This record reconciles the historical implementation freeze with the current pre-authorization engineering branch. It prevents post-freeze edits from being silently represented as part of the original frozen apparatus.

## Historical freeze

- Historical implementation freeze: `3510b86889cd341f7a7cf9ab684fd37b2fafd758`
- Historical executor implementation: `75a7f18c2d5268075e6fc8064eb9a79018845da0`
- Historical acceptance characterization: 2 seeds × 180 trials = 360 observations
- Empirical N: `0`
- Pilot authorization: `NOT GRANTED`

## Reconciliation finding

The live runner was subsequently audited and found to have two material pre-pilot defects:

1. pilot artifacts were still labeled `PRE-FREEZE` / `empirical_data_collection=false`;
2. pilot execution did not require an exact frozen git SHA;
3. the pilot artifact path exposed the real condition in `secondary_outcomes`, defeating the intended blinded analytical boundary.

These are apparatus-level findings. Therefore the historical freeze must **not** be treated as the freeze of the corrected runner.

## Corrective candidate branch

Branch: `chore/preauth-completeness-2026-08-20`

Corrective commits include:

- `fec7a6f577373aeb5037b8b5960bcfa7e0384a0d` — runner SHA binding and pilot artifact/blinding corrections.
- `b1744e02e643515c2b49d8736e036bc40ecf4d7d` — frozen pilot artifact schema.
- `6a95dffe985d5e40ef515f39b7d407068580c0de` — adversarial security tests.

## Freeze rule

The corrected runner is a **new freeze candidate**, not a silent amendment to `3510b868`.

A new freeze may be created only after:

1. CI passes;
2. Python 3.12.0 environment verification passes;
3. final smoke test passes;
4. adversarial security suite passes;
5. topology fingerprints and retention controls are reconciled;
6. primary contrast is explicitly adjudicated;
7. analysis implementation/configuration is identified and SHA-bound;
8. the resulting candidate SHA is recorded in a new freeze manifest.

Until those gates close, pilot authorization remains `NOT GRANTED` and empirical N remains `0`.
