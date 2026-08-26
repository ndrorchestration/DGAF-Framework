# Negative-Control Matrix — Preauthorization

> **Status:** DESIGN / PREAUTHORIZATION
> **Current executable candidate:** `e6beeb66335e1b50a239697badab22dab50eb5ba`
> **Empirical N:** 0
> **Authorization:** NOT GRANTED

## Purpose

Define diagnostic negative controls before confirmatory execution. These controls test whether governance, evidence, provenance, semantic, and recovery mechanisms reject invalid inputs and transitions rather than silently converting them into positive evidence.

## Controls

| ID | Control | Purpose | Confirmatory treatment arm? | Required disposition |
|---|---|---|---|---|
| NC-01 | Null decision | Establish no-op/random decision behavior | No | Report separately |
| NC-02 | Evidence-decoupled | Test whether an observed effect depends on the DGAF evidence-coupling path | No | Report separately |
| NC-03 | Governance-signal falsification | Supply synthetic/invalid governance signals | No | Must fail closed |
| NC-04 | Provenance falsification | Alter or mismatch provenance identity | No | Must fail closed |
| NC-05 | Semantic-boundary | Introduce unsupported ontology/entity assertions | No | Must not modify canonical semantic state |
| NC-06 | Recovery-state | Attempt invalid SUCCESS/RECOVERED/UNRECOVERED_FAILURE transition | No | Must fail closed |

## Freeze requirements

Before authorization, each control must have a frozen definition, expected disposition, executable procedure, and evidence-capture format. Results must not be used to redefine the primary endpoint or statistical analysis after observation.

Negative-control results are diagnostic and are not silently promoted to treatment outcomes.

## Boundary

A failure of a negative control is a governance/engineering finding and must not be repaired by changing the expected result after execution. Any change affecting runner behavior, schema, protocol semantics, or analysis semantics creates a new candidate and requires candidate-scoped re-verification.
