# Epoch 002 protected-sidecar hotfix

Controller: #679.

Observed operator-local failure on accepted main `1fb2c665587d5a0e7b213aef1cc5c870097cdc9b`:

`prepare_track_a_epoch_002_operator_dataset_lock_evidence.py` reached retained protected-root validation after operator admission and the 53-record pre-lock ledger had both passed, then failed because the dataset-lock validator attempted to read `track_a_epoch_002_protected.cms.sha256`.

The accepted retained archive contract instead contains:

- `track_a_epoch_002_protected_ciphertext.sha256`, bound to `track_a_epoch_002_protected.cms`;
- `track_a_epoch_002_custody_cert.sha256`, bound to `track_a_epoch_002_custody_cert.pem`.

The generic `_require_sidecar(target)` convention is therefore invalid for these two protected members. The fix must be limited to explicit canonical sidecar-path validation and a regression test. It must not change retained archive bytes, admission outputs, the pre-lock ledger contract, authorization state, dataset-lock state, unblinding state, primary-analysis state, scientific N, or efficacy claims.

TDD sequence:

1. Add a regression test using the exact canonical protected member names; confirm failure on the missing `.cms.sha256` lookup.
2. Replace only the two protected generic sidecar lookups with explicit canonical sidecar paths while preserving digest/name binding checks.
3. Run focused and repository validation on the exact fix head.
4. Merge only after exact-head CI is terminal green; then rerun operator step 5 onward on the new protected main.
