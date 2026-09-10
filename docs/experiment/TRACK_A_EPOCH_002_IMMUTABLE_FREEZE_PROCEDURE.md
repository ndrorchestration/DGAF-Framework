# Track A Epoch 002 Immutable Freeze Procedure

## Status

This procedure defines a future non-authorizing immutable-freeze transition for
Track A Epoch 002. The procedure and tooling do not establish the freeze by
existing.

Current state remains:

`PRE-FREEZE / FAIL-CLOSED / SUCCESSOR COLLECTION NOT AUTHORIZED / N=0`

Canonical DGAF efficacy remains `NOT_ESTABLISHED`.

## Purpose

The immutable freeze binds one already-validated Epoch 002 precollection
candidate to the exact source and custody artifacts that the collection runner
will later require. It prevents later source drift from being silently treated
as the frozen experiment.

The freeze is a provenance and immutability event. It is not collection
authorization, unblinding authorization, primary-analysis authorization, or a
High-Assurance transition.

## Preconditions

A freeze record may be prepared only after all of these conditions hold:

1. The canonical public custody certificate and non-secret schema-v2 recovery
   receipt have been admitted to the repository and accepted by the existing
   custody validation path.
2. The canonical Epoch 002 precollection preflight exists and validates against
   its exact candidate SHA and tree.
3. The preflight path has exactly one immutable introduction commit after the
   candidate.
4. Every runner-designated protected source exists at the candidate and remains
   byte-identical at the freeze head.
5. Final closure, verification classification, and collection authorization
   records remain absent.
6. The runner contract remains explicitly non-authorizing and scientific N
   remains zero.

At the present repository state, the first two preconditions are not satisfied
because the exact operator-local non-secret custody artifacts have not been
admitted. The freeze therefore remains unavailable by design.

## Protected source set

The helper mirrors the exact `PROTECTED_SOURCE_PATHS` contract already defined
by `experiments/pdmal_pilot/run_track_a_epoch_002.py`. The set includes the
prospective preregistration, analysis lock and implementation, runner contract,
full dependency lock, task engine, harness contract, topology utilities, the
Epoch 002 runner, custody contract and validator, and the accepted public
custody receipt and certificate.

The preflight record is not part of that source set. It is bound separately by
its exact Git blob identity in the freeze manifest.

## Freeze record

The only admissible freeze record is:

`docs/experiment/track_a_runs/TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST.json`

Its schema is not independently invented by the helper. Tests require exact
parity with the runner's existing `expected_freeze` constructor. The record
binds:

- the frozen candidate SHA and tree;
- the exact preflight Git blob SHA;
- every protected source path and candidate Git blob SHA;
- `freeze_status = ESTABLISHED`;
- `scientific_n_increment = 0`; and
- every collection, unblinding, primary-analysis, and High-Assurance
  authorization flag to `false`.

## Tool modes

The helper is:

`scripts/prepare_track_a_epoch_002_immutable_freeze.py`

`--expect-absent` proves the current freeze and downstream gates remain absent.
If a preflight exists, the same mode also requires that preflight to validate.

`--write` is a future local preparation mode. It refuses to operate until a
valid preflight exists, derives the candidate from that preflight, recomputes
candidate protected-source blobs, verifies no protected-source drift, and
writes only the proposed freeze JSON to the working tree. Writing a proposed
record is not acceptance.

`--validate` validates an existing canonical freeze record. In pull-request
validation, `--expected-base-sha` additionally requires that the freeze record
was absent from the exact base, that the preflight was already present at that
base, and that the pull request changes only the freeze record.

## Acceptance sequence

The intended sequence is:

`accepted custody evidence -> accepted preflight -> immutable freeze -> final closure -> verification classification -> separate collection authorization`

Every transition remains independently validated. A later gate must not be
created merely because an earlier gate's tooling exists.

## Secret boundary

The freeze path consumes no private key, passphrase, encrypted private-key
backup, blinding secret, or recoverable secret material. Those materials remain
outside GitHub, Notion, chat, workflow inputs, logs, and CI.

Only the already-designated public certificate and non-secret custody receipt
may become protected freeze sources.

## Non-effects

Acceptance of the tooling in this procedure does not establish:

- repository-level real custody;
- the Epoch 002 precollection preflight;
- the immutable freeze itself;
- collection authorization;
- empirical execution;
- unblinding authorization;
- primary-analysis authorization;
- canonical DGAF efficacy;
- independent custody or independent verification;
- High-Assurance status; or
- any increase in scientific N.

The controlling state remains `PRE-FREEZE / FAIL-CLOSED / SUCCESSOR COLLECTION
NOT AUTHORIZED / N=0` until separately admissible evidence changes it.
