# DGAF Evidence Card Consistency Rules

These rules are normative for machine-readable Evidence Cards.

## 1. Claim class and evidence maturity are separate dimensions

A claim may remain `HYPOTHESIS` while an experiment is `REPRODUCIBLE`. Reproducibility describes evidence about the test process; it does not establish that the hypothesis is true.

## 2. Verification is not validation

`VERIFIED` evidence means the implementation or measurement conforms to its specified behavior under the tested conditions. `VALIDATED` evidence requires evidence that the system or measurement is appropriate for the stated intended context.

## 3. External references do not automatically support DGAF claims

A reference classified as `methodology` or `background` may establish terminology or inform experimental design. It cannot be treated as empirical evidence for a DGAF claim unless its evidence is directly applicable to the claim, construct, context, and method.

## 4. Quantitative claims require measurement context

A quantitative Evidence Card must identify a metric, unit where applicable, baseline or comparator, measurement method, and ground truth or explicit reason ground truth is unavailable.

## 5. Evidence cannot be stronger than its provenance

A card cannot claim independent replication unless independent evidence is actually recorded. A local test cannot be represented as external validation.

## 6. Limitations are first-class evidence metadata

Known scope limitations, uncertainty, and threats to validity must be recorded rather than hidden in narrative prose.

## 7. No automatic promotion

Creating or validating an Evidence Card schema never promotes a claim's evidence maturity. Promotion requires execution of the corresponding evidence-producing activity.
