# Track A Epoch 002 Collection-Authorization Procedure

## Status and purpose

This procedure defines the repository validation boundary for a future Track A
Epoch 002 collection-authorization event.

The actual authorization transition is **human-controlled**. The tooling described
here cannot create the authorization record, cannot execute empirical collection,
and cannot turn pull-request validation into authorization.

Current controlling state remains:

> **PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0 · CANONICAL DGAF EFFICACY NOT ESTABLISHED**

## Authority split

The canonical authorization object is owned by
`experiments/pdmal_pilot/run_track_a_epoch_002.py::expected_authorization`.

The Completion State Reconciler independently classifies the
`collection_authorization` node as `human_controlled`.

`scripts/validate_track_a_epoch_002_collection_authorization.py` is therefore a
validator only. It intentionally exposes no `--write` mode and no empirical
execution mode.

## Meaning of the eventual authorization record

A valid human-authored record makes exactly one new decision:

```text
authorize_empirical_collection = true
```

The same record must keep all of the following false:

```text
authorize_unblinding = false
authorize_primary_analysis = false
historical_pooling_allowed = false
epoch_004_substitution_allowed = false
high_assurance_authorized = false
```

The record also preserves `SAME_SYSTEM_NONINDEPENDENT` custody and binds the
successful custody recovery drill.

Authorization itself does not execute collection and does not increment scientific
N. Scientific N changes only if a separately invoked empirical collection later
passes every runtime predicate and actually produces admissible observations.

## Preconditions for a future authorization event

A human authorization decision may be proposed only after all predecessor records
are accepted on protected `main`:

1. exact public custody certificate plus non-secret schema-v2 recovery receipt;
2. accepted precollection preflight;
3. accepted immutable freeze;
4. accepted final closure;
5. accepted verification classification with
   `DEVELOPER_SELF_ATTESTED_NONINDEPENDENT`, `independent_verification=false`, and
   `same_system_custody=true`;
6. singular immutable histories and strict predecessor ordering;
7. unchanged protected frozen sources.

No predecessor gate implies authorization.

## Current absence proof

Run:

```bash
python scripts/validate_track_a_epoch_002_collection_authorization.py --expect-absent
```

A successful result proves only that the authorization record is absent, the
reconciler still classifies the transition as human-controlled, PR validation has
no authorization authority, empirical execution did not occur, and scientific N
remains zero.

## Human-authored authorization event

When the predecessor chain is actually complete, the human operator must make an
explicit authorization decision and author the one canonical JSON record at:

```text
docs/experiment/track_a_runs/TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json
```

The validator deliberately does not generate this record. The human-authored
object must match the runner's canonical `expected_authorization` object exactly,
including:

- exact authorization-parent SHA;
- frozen candidate SHA and tree;
- exact preflight, freeze, closure, and verification Git blobs;
- preregistration and analysis-lock identities;
- analysis and dependency-lock identities;
- exact seed-panel bounds and expected observation count;
- exact accepted custody receipt/certificate bindings and fingerprints;
- `SAME_SYSTEM_NONINDEPENDENT` custody classification;
- the narrowly scoped empirical-collection authorization decision.

The validator reports any missing, extra, or mismatched fields instead of repairing
or silently normalizing the proposed record.

## One-record event shape

The actual authorization PR must be created from the exact current protected
`main` and contain exactly one commit whose only changed path is the authorization
JSON file. The authorization file must not exist at that parent, while the accepted
verification classification must already exist there.

Validate the proposed event with:

```bash
python scripts/validate_track_a_epoch_002_collection_authorization.py \
  --validate \
  --expected-base-sha <EXACT_PR_BASE_SHA>
```

The validator fails closed if:

- authorization is not still classified `human_controlled`;
- the runner contract allows PR validation to authorize;
- any predecessor record is absent, malformed, reordered, or has non-singular
  history;
- candidate, tree, source, predecessor-blob, or custody bindings drift;
- the authorization parent differs from the exact PR base;
- the authorization file already existed at the parent;
- the authorization commit changes any path other than the one authorization file;
- the authorization record differs from the canonical runner object;
- unblinding, primary analysis, historical pooling, Epoch 004 substitution, or
  High-Assurance authority is promoted;
- custody independence is overstated.

## Pull-request validation is not authorization

The dedicated workflow
`.github/workflows/track-a-epoch-002-collection-authorization-boundary.yml` may
validate a future human-authored proposal, but the runner contract explicitly sets:

```text
pr_validation_can_authorize = false
```

The workflow never calls the empirical runner with `--execute`, never sets the
Epoch 002 authorization environment variable, never supplies a topology blinding
secret, and never supplies public/protected empirical output roots.

Therefore a green authorization-boundary PR means only that the proposed one-record
human decision is structurally consistent with the frozen predecessor chain. It is
not empirical execution and it is not scientific evidence.

## Post-merge execution remains separate

Even after a human-controlled authorization record is accepted into protected
`main`, empirical collection remains a separate explicit operation. The runner
still requires all runtime predicates, including the exact authorization commit
shape, frozen source integrity, custody validation, explicit Epoch 002 environment
authorization, a fresh topology blinding secret, and distinct public/protected
retention roots.

Unblinding and primary analysis remain separate later authorization events.

## Secret boundary

No private key, passphrase, encrypted private-key backup, topology blinding secret,
or other recoverable secret material belongs in GitHub, Notion, chat, committed
files, pull-request text, or CI inputs/logs.

The authorization record binds only non-secret custody evidence and fingerprints.
The fresh topology blinding secret exists only at the later authorized collection
runtime and must not be persisted by this authorization tooling.
