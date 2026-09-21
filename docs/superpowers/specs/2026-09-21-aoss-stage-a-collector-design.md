# AOSS Stage-A Collector Design

Date: 2026-09-21
Status: PROPOSED / NON-EXECUTING / REQUIRES DESIGN REVIEW
Controller: #890

## Purpose and scope

Implement an external collector for the already authorized finite Stage-A study.
Success means reproducible, content-addressed execution of the frozen 16 classes
against unchanged ACP, without upgrading fixtures, replay counts, or decision
divergence into empirical efficacy claims. This document is not an execution
authorization or a change to any frozen contract.

Verified starting point: DGAF receipt commit
`6baea5a6b6a316add6292cc647f5b455eb235ce3`, authorization
`854b9d5adb33c6ee6158a63017f133f20b90742e`, protected design basis
`807216df1bd5b28c677b8c42822975b2941c1211`, ACP
`dbab7c1afafec524ce7c18157de2089cafe79c87`, adapter apparatus
`69821cdcc1b9b9432b7001c6f52c867f9669f54d`.
All nine receipt contract blobs and adapter bytes matched during static audit.

## Approach

Recommended: a separate Python collector in DGAF, with a source driver separated
from the read-only observer by exported manifest files. It reuses the frozen
adapter, policy, and baseline without editing them. The observer cannot call
back into the driver, schedule ACP work, or modify ACP configuration.
A source driver necessarily selects the preregistered workloads; it is not the
observer. The boundary must be explicit in code and reviewed before execution.

Alternatives rejected:

- Replaying the existing fixture bundle as collection would misclassify apparatus
  as new outcomes and would not establish live freshness.
- Adding instrumentation to ACP would change the exact authorized target.

Neither is an admissible shortcut.

## Newly identified semantic prerequisite

The frozen adapter normalizes manifests and exposes a terminal-event summary.
The frozen policy accepts PolicyInput booleans and tri-state predicates.
In the inspected modules there is no executable bridge defining how every
normalized observation becomes terminal, blocked, conflicted, uncertain,
deadlock_candidate, and provenance_valid.

This is consequential: the frozen policy evaluates terminal before blocked and
before uncertainty. Equating every terminal event with terminal=True would
record failed/denied outcomes before the blocked rule. Similarly, merely setting
uncertain=True for stale data cannot override terminal=True. Do not infer the
mapping from class labels or expected results.

Before implementing policy input reconstruction, recover an authoritative
mapping or submit a separate prospective mapping specification for acceptance.
It must define each predicate from observables, precedence of structural and
freshness rejection, treatment of multiple terminals/duplicates/order ambiguity,
and the provenance semantics. Preserve absent authority and validator evidence
as INCONCLUSIVE. No new default may silently settle these questions.

Development can implement non-outcome preflight, custody and synthetic replay
tests while this mapping gate remains closed. The production collection entry
point must reject execution until the mapping and collector identity are accepted.

## Components and proposed files

- `scripts/aoss_stage_a/preflight.py`: read-only Git identity, blob and runtime
  checks; no ACP import or execution.
- `scripts/aoss_stage_a/source_driver.py`: exact-source workload execution and
  raw export; separate process from the observer.
- `scripts/aoss_stage_a/observer.py`: frozen adapter and comparator calls,
  accepted mapping, freshness adjudication and frozen policy evaluation.
- `scripts/aoss_stage_a/custody.py`: canonical serialization, SHA-256 objects,
  atomic creation and attempt ledger.
- `scripts/aoss_stage_a/replay.py`: five read-only replays using retained bytes
  and captured ingest references.
- `scripts/run_aoss_v0_6_stage_a.py`: preflight and guarded collection commands.
- `tests/test_aoss_stage_a_collector.py`: synthetic contract and fault tests.
- `requirements-aoss-stage-a.lock`: exact runner dependencies with hashes.
  Interpreter version and platform identity are separately bound in the
  execution manifest; a pyproject version floor is not a runtime lock.

These are proposed interfaces, not implemented or accepted files.

## Preflight

Require explicit paths for DGAF, ACP, accepted collector binding and a new
attempt destination. Resolve commit identities locally and prove the accepted
authorization/receipt lineage. Verify receipt contract blobs plus the frozen
policy and comparator executable bindings and adapter bytes. Reject dirty
source trees, substituted import locations and missing files.

Bind actual interpreter, dependency lock and installed environment to the
accepted execution manifest. Hash a lock file only after checking the
environment against it. Fail on drift. Preflight must be independently callable
without creating episodes, running policy decisions or allocating a study attempt.

## Collection and attempt custody

Require acceptance of the exact collector and mapping identities before the
collection command runs. Create the attempt reservation exclusively before
source dispatch; never overwrite or resume an existing attempt. Record STARTED,
COMPLETE, INVALID or INCONCLUSIVE events without erasing earlier evidence.
A crash leaves an incomplete attempt, not permission to rerun after inspection.

Generate one canonical episode per frozen class. Keep the original ACP export
bytes for every episode and record every declared post-export transformation
with original and transformed digests. No observer mutation of the source,
timestamp monkeypatching, callbacks or source instrumentation.

Capture source export and observer ingest times on the same host. Use frozen
limits of age <=30 seconds and future skew <=2 seconds. Preserve the original
ingest reference for replay so wall-clock passage does not change the replay
question. Replay never refreshes stale telemetry.

The 16 classes remain those in the accepted eligibility record. Malformed
manifest and mismatched run ID remain structural-rejection controls outside the
primary denominator. Unknown/missing classes or identity/hash drift invalidate
the attempt; infrastructure failures are retained, not silently excluded.

## Artifacts and replay

Retain study manifest, source episode bundle, normalized bundle, decision bundle
and analysis bundle as separate SHA-256-addressed objects. Study manifest binds
all source, contract, code and runtime identities plus attempt identity and
the declared class set. Original exports and transformation records remain
available; hashes do not replace source retention.

Canonical study JSON is UTF-8, sorted keys, compact separators, trailing newline,
and no NaN. Existing adapter digests keep their frozen serialization; do not
silently replace that digest convention with bundle serialization.

Replay each canonical source episode five times from identical retained bytes.
Verify normalized, decision and analysis digests independently. Compute every
receipt boolean from the actual comparison; no literal PASS defaults.
Any false/missing verification field makes replay fail or schema-reject.
The whole-study receipt contains hashes/status, not outcome payloads.

## Analysis and claims

Use only the accepted finite descriptive endpoint with explicit numerator and
denominator and retained UNMEASURED/INCONCLUSIVE states. No p-values, confidence
intervals, bootstrap, superiority or population generalization. Replays do not
add independent units. Do not resolve the historical O/M/R gap by invention.
Keep scientific-N increment at 0 and preserve Track A separation.

## Verification before acceptance

Write tests before implementation. Synthetic inputs are classified
SYNTHETIC_TEST_ONLY and use temporary artifact stores; tests must not run a
registered study attempt or emit accepted-study receipts.

Required tests:

1. Wrong commit, dirty ACP, mismatched contract/code blob, substituted import,
   dependency drift, missing receipt and broken lineage each block preflight.
2. Preflight imports no ACP driver and produces no episode or outcome files.
3. Duplicate attempt, symlink destination, path traversal, partial write and
   interrupted execution cannot overwrite or masquerade as a complete attempt.
4. Every declared transformation preserves raw source bytes and records digests.
5. Freshness thresholds at -2 and 30 seconds are inclusive; values outside them,
   naive timestamps and cross-host timing are rejected or held as contracted.
6. Frozen baseline is unaffected by observer-only fields or injected class labels.
7. Policy-input mapping tests follow the separately accepted mapping, including
   terminal-plus-blocked and terminal-plus-stale cases; never derive expected
   decisions from ground-truth labels.
8. Five exact-byte synthetic replays match; tampering in each artifact layer
   fails the corresponding receipt comparison.
9. Missing classes invalidate; two structural controls remain excluded; replay
   passes never inflate the denominator.
10. Invalid/incomplete attempts retain evidence and cannot be silently retried.

## Implementation sequence

First implement and test read-only preflight and exclusive custody on synthetic
inputs. Then accept the recovered/proposed policy mapping and source-driver
boundary, implement the driver/observer, and test replay/analysis end to end
with synthetic inputs. Review the exact collector, lock and execution binding.
Only after acceptance, rerun preflight and begin the bounded study separately.

## Review disposition

The source contracts provide most requirements, but do not by themselves prove
the missing executable mapping or collector. Approving this design permits
implementation planning; it does not resolve that semantic gap, accept a future
collector commit, or authorize any wider study.
