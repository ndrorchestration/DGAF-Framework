# AOSS v0.6 Stage-A synthetic five-bundle replay boundary

This draft tranche implements only the replay-verification mechanics required by
the frozen Stage-A artifact/replay contract.

It verifies the five required artifact roles:

- `study_manifest_sha256`
- `source_episode_bundle_sha256`
- `normalized_bundle_sha256`
- `decision_bundle_sha256`
- `analysis_bundle_sha256`

Exactly five replay passes are required. Every pass computes the frozen
verification booleans from actual byte comparisons. Any source identity mismatch,
contract digest mismatch, missing artifact role, wrong replay count, or byte
tampering yields FAIL or schema rejection.

This is synthetic apparatus validation only. It does not execute ACP, generate
study outcomes, create an accepted whole-study replay receipt, enable collection,
establish external validation, or establish collection execution readiness.

Replay passes remain non-independent and `SCIENTIFIC_N_INCREMENT=0`.
