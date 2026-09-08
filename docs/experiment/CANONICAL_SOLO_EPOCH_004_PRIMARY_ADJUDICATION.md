# Canonical Solo Epoch 004 — Primary Adjudication

**Epoch:** `PDMAL-SOLO-CANONICAL-EPOCH-004`  
**Validation track:** `SOLO_DEVELOPER`  
**Independent verification:** `NOT ESTABLISHED`  
**Frozen collection SHA:** `9725ffd80d5386826d61b7f824524f7f8d89fce8`  
**Execution run:** `34181212217`

## Evidence chain

The run completed the preregistered 50-seed, 9,000-observation collection and locked the dataset while blinded. Before the key was retrieved, a separate structural recheck confirmed the exact seed panel, 180 unique matrix cells per seed, four balanced blind arms, SHA-256 sidecars, byte-identical retained archive copies, a single environment fingerprint, no historical pooling, and `unblinding_authorized=false`.

Locked dataset artifact: `10039138297`, digest `sha256:6a11f4748eb40e10fa2c0476f759fb800bb43181a266ec3e0b4a457c7b7d1876`.

Separate key artifact: `10039138610`, digest `sha256:dc4c0aada6baaed556eabd4ad179b945228600959a78b48b8620b144e28d1a68`. Custody is same-system GitHub Actions artifact custody and is not independent custody. The key value is not published.

Pre-unblinding lock record: GitHub #381 comment `5578420073`. Controlled unblinding authorization: GitHub #309 comment `5578422132`. The primary result was recorded first on GitHub #309 comment `5578430005`, before any secondary or exploratory analysis.

## Frozen primary analysis

The statistical source remained `experiments/pdmal_pilot/analysis.py`, blob `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`, with analysis-config SHA-256 `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`.

The preregistered primary contrast was `dgaf-vs-null`; the estimand was the mean paired seed-level FFCR difference. Bootstrap resampling was over the 50 paired seed effects with 10,000 percentile-bootstrap resamples, RNG seed `20260823`, and alpha `0.05`. Directional support required both a positive estimate and a two-sided 95% confidence interval lower bound above zero.

## Primary result

- DGAF aggregate FFCR: `0.7337777777777778`
- null aggregate FFCR: `0.8275555555555555`
- paired effect, DGAF minus null: **`-0.0937777777777778`**
- two-sided 95% paired-bootstrap CI: **`[-0.11822222222222223, -0.07066666666666668]`**
- locked-rule classification: **`EVIDENCE_AGAINST_DIRECTIONAL_DGAF`**

## Adjudication

Epoch 004 provides empirical evidence against the preregistered directional canonical-DGAF hypothesis under this Solo developer, non-independent apparatus and canonical treatment definition. The primary directional hypothesis is not supported; the confidence interval is wholly negative under the locked estimator.

This result does **not** establish independent validation, High-Assurance acceptance, production readiness, or universal inferiority of every possible DGAF design. It also does not retroactively alter Experiment 001, Epoch 002, or Epoch 003. Historical datasets remain separate and unpooled.

Any subsequent topology-, failure-level-, mechanism-, or component-specific examination is secondary/exploratory unless a separate prospective protocol says otherwise. Such analysis may diagnose why the treatment underperformed, but it cannot replace or rescue the locked primary result.

**High-Assurance remains `NOT AUTHORIZED / N=0`.**
