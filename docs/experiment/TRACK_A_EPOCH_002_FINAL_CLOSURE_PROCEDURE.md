# Track A Epoch 002 Final-Closure Procedure

## Status and purpose

This procedure defines the repository-side preparation and validation path for the
Track A Epoch 002 final-closure packet.

The tooling described here is **non-authorizing**. Its presence does not establish
custody, precollection preflight, immutable freeze, final closure, verification,
collection authorization, empirical execution, unblinding, primary analysis,
High-Assurance status, efficacy, or scientific N.

Current controlling state remains:

> **PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0 · CANONICAL DGAF EFFICACY NOT ESTABLISHED**

## Authority

The canonical closure schema is owned by
`experiments/pdmal_pilot/run_track_a_epoch_002.py::expected_closure`.

`scripts/prepare_track_a_epoch_002_final_closure.py` is an implementation helper
for that existing contract. It does not create a second schema or authority plane.
Focused tests extract `expected_closure` from the runner and require exact object
parity with the helper.

## Preconditions for an actual closure event

An actual final-closure packet may be prepared only after all of the following are
true and independently validated by the existing successor chain:

1. the schema-v2 successor custody recovery receipt and matching public
   certificate have been accepted into the repository;
2. the precollection recovery drill is recorded as `PASS` with
   `SAME_SYSTEM_NONINDEPENDENT` custody classification;
3. the canonical Epoch 002 precollection preflight exists and validates exactly;
4. the canonical Epoch 002 immutable-freeze manifest exists and validates exactly;
5. the freeze path has exactly one immutable history commit;
6. the frozen candidate and protected-source blobs remain unchanged;
7. no Epoch 002 verification-classification or collection-authorization record
   already exists.

Until those conditions hold, the only valid use of the closure helper is the
current-state absence check.

## Current-state validation

Run:

```bash
python scripts/prepare_track_a_epoch_002_final_closure.py --expect-absent
```

A successful result proves only that the closure packet and downstream gates are
absent while the runner contract remains non-authorizing. It is not evidence of
closure readiness beyond that bounded statement.

## Preparing a future closure packet

After an accepted immutable freeze exists, create a fresh branch from the exact
current protected `main` and run:

```bash
python scripts/prepare_track_a_epoch_002_final_closure.py --write
```

The helper derives the packet from the already-validated freeze and writes only:

```text
docs/experiment/track_a_runs/TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET.json
```

The generated record must match the runner's canonical closure object exactly. It
binds:

- the Epoch 002 protocol identity;
- the exact frozen candidate SHA;
- the exact immutable-freeze manifest Git blob;
- an empty `open_blockers` list for the bounded freeze-to-closure gate;
- `CLOSED_VERIFIED_FOR_AUTHORIZATION_REVIEW` as closure status;
- `scientific_n_increment = 0`;
- every collection, unblinding, primary-analysis, and High-Assurance authorization
  field to `false`.

`CLOSED_VERIFIED_FOR_AUTHORIZATION_REVIEW` means only that the frozen repository
chain is eligible for the separately governed verification/authorization review.
It does **not** itself authorize collection.

## Closure-event pull request boundary

The actual closure-event pull request must be a one-record transition. Relative to
its exact base SHA, it may change only:

```text
docs/experiment/track_a_runs/TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET.json
```

Validate it with:

```bash
python scripts/prepare_track_a_epoch_002_final_closure.py \
  --validate \
  --expected-base-sha <EXACT_PR_BASE_SHA>
```

The validator fails closed if:

- the freeze is missing or malformed;
- the freeze candidate differs from the validated preflight candidate;
- the frozen protected sources drift;
- the freeze lacks exactly one immutable history commit;
- the closure packet differs from the runner-defined canonical object;
- the closure path is not new relative to the exact PR base;
- the immutable freeze did not already exist at the exact PR base;
- any file other than the closure packet changed in the closure-event PR;
- closure is not strictly later than freeze;
- verification or collection authorization already exists.

## Required CI evidence

The dedicated workflow
`.github/workflows/track-a-epoch-002-final-closure.yml` must run against the exact
pull-request head. It checks:

- exact checkout identity;
- the hash-locked experimental Python environment;
- helper-to-runner closure-schema parity;
- adversarial mutation rejection;
- current closure absence or, later, the closure-only transition;
- explicit preservation of non-authorization and `N=0`.

Repository merge policy remains stricter than the dedicated lane: merge only after
the complete exact-head repository workflow wave is terminal-green and the PR base
has not raced.

## Secret boundary

No private key, passphrase, encrypted private-key backup, blinding secret, or
recoverable secret material belongs in this procedure, GitHub, Notion, workflow
inputs, logs, committed files, or chat.

The closure helper does not generate, accept, read, or log secret custody material.
It consumes only already-accepted public/non-secret repository evidence through the
validated predecessor gates.

## Gate ordering after closure

Final closure is not collection authorization. The successor chain remains ordered:

```text
custody recovery evidence
  -> precollection preflight
  -> immutable freeze
  -> final closure
  -> verification classification
  -> separate collection authorization
  -> empirical collection
```

Each transition must remain independently explicit and fail closed. No earlier gate
may imply a later one.
