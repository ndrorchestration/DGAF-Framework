# DGAF Discovery Harness v1

## Status

**ENGINEERING DISCOVERY ONLY · NON-AUTHORIZING · SCIENTIFIC N=0 EFFECT**

This harness is a second-order assurance layer. It searches for weaknesses in DGAF controls, weaknesses in the detectors that inspect those controls, and weaknesses shared by the discovery methods themselves.

It does not alter Track A or Mode T governance state, authorize collection, materialize empirical inputs, unblind results, promote evidence independence, or increment scientific N.

## Authority firewall

Every harness output must satisfy:

- repository mutation by an experiment: `false`;
- authorization effect: `false`;
- scientific state effect: `NONE`;
- scientific N increment: `0`;
- production execution: `false`;
- mutation scope: `EPHEMERAL_COPY_ONLY`.

Harness failure, timeout, missing evidence, malformed input, or unknown classification can never increase authority.

## v1 scope

The initial implementation provides a fail-closed output envelope, curated governance-semantic mutation operators, explicit legal/forbidden transition coverage metrics, and pairwise control-interaction analysis.

Critical mutant families begin with authorization promotion, evidence-independence promotion, predecessor/provenance removal, scientific-N increment, and fail-open decision promotion.

## Recursive assurance roadmap

Later layers add metamorphic relation registries, assumption expiry, a blind-spot ledger (`discovered_by` / `missed_by`), detector mutation, property mutation, stateful search, formal lifecycle models, bounded agent/API chaos, and versioned external-framework crosswalks.

A discovery method may generate a candidate finding or test. It may never promote itself into authoritative governance truth.

## Verification boundary

Passing these tests demonstrates only that the harness kernel obeys its non-authorizing contract and that its basic analyzers behave as specified. It is not evidence of DGAF efficacy, experiment authorization, production validation, or scientific findings.
