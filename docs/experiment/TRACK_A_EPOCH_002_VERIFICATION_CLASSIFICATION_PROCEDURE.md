# Track A Epoch 002 Verification-Classification Procedure

## Status and purpose

This procedure defines the repository-side preparation and validation path for the
Track A Epoch 002 verification-classification record.

The tooling is **non-authorizing**. Its presence does not establish custody,
precollection preflight, immutable freeze, final closure, verification, collection
authorization, empirical execution, unblinding, primary analysis, High-Assurance
status, efficacy, independent verification, or scientific N.

Current controlling state remains:

> **PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0 · CANONICAL DGAF EFFICACY NOT ESTABLISHED**

## Authority and evidence ceiling

The canonical verification schema is owned by
`experiments/pdmal_pilot/run_track_a_epoch_002.py::expected_verification`.

`scripts/prepare_track_a_epoch_002_verification_classification.py` implements that
existing contract and does not create a second schema or authority plane. Focused
tests extract the runner function and require exact object parity.

The accepted classification is deliberately bounded:

```text
verification_status = PASS
verification_class = DEVELOPER_SELF_ATTESTED_NONINDEPENDENT
independent_verification = false
same_system_custody = true
scientific_n_increment = 0
collection_authorized = false
unblinding_authorized = false
primary_analysis_authorized = false
high_assurance_authorized = false
```

`PASS` therefore means only that the same-system developer verification record
satisfies its declared deterministic contract. It must never be translated into
independent replication, independent custody, external review, empirical efficacy,
collection authorization, or High-Assurance status.

## Preconditions for an actual verification event

An actual verification-classification record may be prepared only after:

1. the exact public custody certificate and non-secret schema-v2 recovery receipt
   have been admitted and repository-validated;
2. the canonical precollection preflight has been accepted;
3. the canonical immutable-freeze manifest has been accepted;
4. the canonical final-closure packet has been accepted;
5. each predecessor gate retains exactly one immutable history commit and correct
   chronological ordering;
6. the frozen protected sources remain unchanged;
7. collection authorization remains absent.

Until those conditions hold, only the current-state absence check is valid.

## Current-state validation

Run:

```bash
python scripts/prepare_track_a_epoch_002_verification_classification.py --expect-absent
```

A successful result proves only that verification classification and collection
authorization remain absent while the runner contract remains non-authorizing.

## Preparing a future verification classification

After accepted final closure, create a fresh branch from exact protected `main` and
run:

```bash
python scripts/prepare_track_a_epoch_002_verification_classification.py --write
```

The helper derives the record from the already-validated closure chain and writes
only:

```text
docs/experiment/track_a_runs/TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION.json
```

It binds the exact frozen candidate and exact final-closure Git blob and preserves
the evidence ceiling `DEVELOPER_SELF_ATTESTED_NONINDEPENDENT`.

## Verification-event pull request boundary

The actual verification-event pull request must be a one-record transition.
Relative to its exact base SHA, it may change only the verification-classification
JSON file.

Validate with:

```bash
python scripts/prepare_track_a_epoch_002_verification_classification.py \
  --validate \
  --expected-base-sha <EXACT_PR_BASE_SHA>
```

The validator fails closed if:

- final closure is absent or malformed;
- predecessor freeze/closure identity or ordering is invalid;
- a predecessor gate has non-singular history;
- the verification object differs from the runner-defined canonical object;
- independent verification is asserted;
- same-system custody is omitted or negated;
- scientific N or any authorization field is promoted;
- the verification path already existed at the exact PR base;
- final closure did not already exist at the exact PR base;
- the event PR changes any file other than the verification record;
- collection authorization already exists.

## Required CI evidence

The dedicated workflow
`.github/workflows/track-a-epoch-002-verification-classification.yml` runs against
the exact pull-request head and checks:

- exact checkout identity;
- the hash-locked experimental environment;
- helper-to-runner schema parity;
- adversarial evidence-ceiling and authorization mutation rejection;
- current absence or, later, the one-record verification transition;
- explicit preservation of non-independence, non-authorization, and `N=0`.

The repository-wide merge rule remains stricter: merge only after every returned
exact-head workflow is terminal-green and the PR base has not raced.

## Secret boundary

No private key, passphrase, encrypted private-key backup, blinding secret, or
recoverable secret material is generated, accepted, read, logged, or committed by
this tooling. Verification consumes only accepted public/non-secret repository
evidence through predecessor gates.

## Gate ordering after verification

Verification classification is not collection authorization. The ordered successor
chain remains:

```text
custody recovery evidence
  -> precollection preflight
  -> immutable freeze
  -> final closure
  -> verification classification
  -> separate collection authorization
  -> empirical collection
```

The subsequent collection-authorization event must independently bind the accepted
verification blob and all predecessor evidence. No verification outcome may imply
that authorization transition.
