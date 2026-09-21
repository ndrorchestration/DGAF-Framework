# AOSS v0.6 Stage-A synthetic attempt-integrity boundary

This tranche implements the remaining synthetic attempt-integrity semantics under
Issue #901, downstream of the accepted five-bundle replay mechanics in PR #913.

The contract fails closed when any of the following drifts:

- exact source identity;
- frozen contract digests;
- retained artifact digests;
- the required Stage-A class set.

A missing or extra class invalidates the synthetic attempt. Identity or digest
drift also invalidates it.

The retry rule is independent of validity: once outcome inspection is recorded,
retry is prohibited. An invalid attempt after outcome inspection remains
non-retryable; invalidity is not permission to erase evidence or try again.

This layer is synthetic apparatus validation only. It does not execute ACP,
generate outcomes, mutate accepted study state, enable collection, establish
collection execution readiness, or increment scientific N.
