# DGAF Instrument Identity Policy v1.0

**Status:** Audit control / non-authoritative until ratified
**Date:** 2026-09-04

## Core rule

A numerical or control result is not authoritative when identified only by a human-readable label. Authoritative evidence must bind at minimum to:

`instrument_id + instrument_version + instrument_type + canonical_source + formula_or_algorithm + parameter_set + score_range + thresholds_or_predicates + scope + authority + binding_strength + implementation_ref + source_commit + execution_run + execution_timestamp + upstream_dependencies + epistemic_status`

## Distinct classes

RUBRIC, GATE, METRIC/SCORE, PROTOCOL, ATTESTATION, EVIDENCE/REPORT, and HISTORICAL LINEAGE remain distinct even when names overlap.

## Lineage

Derivatives must declare `IMPLEMENTS`, `EXTENDS`, `ADAPTS`, `HISTORICAL`, or `SUPERSEDES`. A derivative may not claim `IMPLEMENTS` when score domain, dimensions, aggregation, or governing predicates materially differ.

## Mathematical integrity

Where applicable, validation must check weight sums, score-domain consistency, normalization, threshold reachability, boundary behavior, critical-fail precedence, parameter-set identity, deterministic replay inputs, and derivative-to-canonical correspondence. No check may silently normalize, rescale, substitute thresholds, or resolve aliases.

## Evidence dependency

Derived evidence inherits the status and limitations of the instruments and artifacts it depends on. Unresolved upstream formula, parameters, scope, or execution identity block promotion.

## Current audit examples

Known unresolved families include QA-11Q, GATE-11Q/P-11 naming, AXIS versus Apogee's derivative rubric, P-15 Reson thresholds, AHG Stability Index parameterization, NDR registry release identity, and agent A-ID mappings.

## Boundary

This is an audit/control artifact. It does not authorize freeze, pilot execution, unblinding, production certification, or empirical claims.

**DGAF:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
