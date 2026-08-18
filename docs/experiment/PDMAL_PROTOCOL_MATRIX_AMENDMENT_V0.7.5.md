---
status: APPROVED PENDING PANEL RECORD
state: PRE-FREEZE AMENDMENT
authority: Both
owner: DGAF/PDMAL experimental-design control
last_verified: 2026-08-18
applies_to_sha: pending-amendment-commit
supersedes: conflicting pilot-matrix language in prior protocol text
---

# PDMAL Protocol Matrix Amendment v0.7.5

## Purpose

This amendment resolves the pilot-matrix inconsistency between the consolidated protocol and the expert-panel-approved task specification v0.7.4. It is an additive pre-freeze clarification and must be incorporated into the final frozen protocol before pilot authorization.

## Authoritative pilot scope

The pre-registered 50-seed pilot uses exactly four conditions:

```text
null
simple
static
dgaf
```

The repository-recognized condition `dgaf_pdmal` is explicitly out of scope for this pilot and is reserved for later experiments.

## Topology scope

The pilot uses exactly five topologies:

```text
ring
pdmal
a random regular degree-3 topology
small-world
complete K20
```

The exact implementation parameters and provenance SHAs for each topology must be recorded in the freeze manifest.

## Failure-count scope

The pilot uses exactly nine failure-count levels:

```text
0, 1, 2, 3, 4, 5, 6, 8, 10
```

These levels are part of the pre-registered workload matrix and must remain unchanged after protocol freeze except through a formally approved protocol amendment before data collection.

## Observation count

The complete crossed workload matrix is:

```text
4 conditions × 5 topologies × 9 failure-count levels = 180 observations per seed
```

For the authorized 50-seed pilot:

```text
50 seeds × 180 observations = 9,000 planned raw observations
```

This is the planned raw observation count before any objectively defined exclusions or missing records. It is not a guarantee that every record will be analyzable; exclusions remain governed by the frozen exclusion rules.

## Statistical unit

One seed remains one paired experimental block for the primary FFCR analysis. The 180 workload observations within a seed are component trial records used to derive the condition-level outcomes required by the frozen analysis plan.

## Status

This amendment does not authorize execution. The protocol remains PRE-FREEZE until the amendment is incorporated into the final frozen protocol, the required provenance and custody controls are independently verified, the freeze commit is created, and explicit pilot authorization is recorded.
