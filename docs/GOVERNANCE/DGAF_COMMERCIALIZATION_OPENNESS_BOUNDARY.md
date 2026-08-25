# DGAF Commercialization & Openness Boundary

**Status:** Proposed strategic governance specification  
**Date:** 2026-08-25

## Purpose

Define the boundary between what DGAF should publish for reproducibility, independent evaluation, and ecosystem adoption and what may legitimately remain non-public for commercial, security, privacy, or operational reasons.

This document does **not** establish a proprietary claim over material that is already open-source or otherwise publicly committed under an existing license. It establishes a decision framework for future work and commercialization.

## Core principle

DGAF should be sufficiently open that an independent user can clone, inspect, run, and evaluate the public reference implementation without requiring access to undisclosed core functionality.

Commercial differentiation should primarily come from services, operational capability, expertise, assurance, integration, hosted infrastructure, support, certification/trademark governance, and specialized offerings rather than from making the public implementation intentionally incomplete.

## Asset classes

### OPEN

Appropriate for public GitHub publication:

- reference implementation;
- core specifications and schemas;
- reproducible examples;
- public test harnesses;
- benchmark definitions;
- public evidence and negative results;
- governance principles;
- public research protocols;
- non-sensitive Pattern Commons material;
- contribution and extension interfaces.

### RESEARCH / EXPERIMENTAL

Public by default when publication improves reproducibility, but explicitly labeled as hypothesis, candidate, experimental, or unresolved:

- candidate NDR patterns;
- experimental metrics;
- proposed algorithms;
- preliminary benchmarks;
- failed approaches;
- unresolved epistemic questions.

Experimental status must not be represented as validation.

### PROPRIETARY / COMMERCIAL

May legitimately remain non-public when it represents independently developed commercial differentiation, subject to applicable licenses and law:

- private deployment automation;
- proprietary operational tooling;
- specialized enterprise integrations;
- managed evaluation infrastructure;
- premium service tooling;
- private implementation accelerators;
- customer-specific configurations;
- private benchmark programs.

The existence of a commercial boundary does not justify withholding evidence necessary to substantiate public claims about the open implementation.

### PRIVATE / CONFIDENTIAL

Never publish by default:

- customer data;
- credentials or secrets;
- private deployment information;
- confidential contracts;
- private security findings before responsible disclosure;
- personally identifiable information;
- protected customer telemetry.

### SECURITY-SENSITIVE

Withhold or delay publication when disclosure creates a material security risk. Publication should be reconsidered after mitigation or responsible disclosure where appropriate.

### TRADEMARK / CERTIFICATION-GOVERNED

The DGAF name, marks, certification terminology, and claims of official status are governed separately from software licensing. Open-source use of the software does not by itself establish entitlement to represent a product or service as officially DGAF-certified or endorsed.

See [`DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`](DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md). No active certification program is established by that policy.

## Commercialization model

Potential revenue channels include:

1. implementation and integration services;
2. managed/hosted DGAF infrastructure;
3. evaluation and assurance services;
4. enterprise support and maintenance;
5. specialized governance/compliance packages;
6. training and professional services;
7. certification or assessment programs if independently defensible;
8. sponsorship and community funding;
9. specialized research engagements.

These are candidate business models, not claims of current revenue or market validation.

## Pattern Commons relationship

Pattern Commons is the ecosystem-level knowledge and provenance layer. Commercialization status is an attribute of an asset or offering, not evidence that a pattern is valid. Pattern Commons records should preserve provenance and epistemic status independently of commercial ownership.

See [`../PATTERN_COMMONS_ARCHITECTURE.md`](../PATTERN_COMMONS_ARCHITECTURE.md) and [`DGAF_ECOSYSTEM_BOUNDARY_CROSSWALK_2026-08-25.md`](DGAF_ECOSYSTEM_BOUNDARY_CROSSWALK_2026-08-25.md).

## Public evidence rule

When a commercial or private component is necessary to support a public claim, disclose enough evidence to substantiate the claim without exposing protected implementation details, customer data, credentials, or security-sensitive material.

The commercial boundary must never become an epistemic loophole.

## Open questions

- Which open-source license best matches DGAF's intended long-term freedoms and ecosystem strategy?
- What exact capabilities constitute the public reference implementation?
- Which assets, if any, have genuine proprietary value rather than merely perceived value?
- What may competitors commercially provide using DGAF?
- What constitutes official DGAF compatibility, endorsement, or certification?
- Who controls and governs the DGAF trademark?
- What evidence standard is required before a commercial assurance claim can be made?
- What recurring service has sufficient customer value to support the project sustainably?
- Which security, privacy, and customer-data boundaries require separate controls?
- How should contributor rights, attribution, and commercial participation be handled?

## Anti-patterns

DGAF should avoid:

- calling withheld core functionality “open source”;
- using secrecy as a substitute for product differentiation;
- claiming universal guarantees from empirical evidence;
- treating certification as proof of safety or correctness beyond its defined scope;
- using proprietary status to obscure unsupported claims;
- publishing customer/private/security-sensitive material merely to appear transparent.

## Decision rule

When deciding whether an artifact should be public, ask in order:

1. Is it necessary for independent reproduction or evaluation of a public claim?
2. Is there a legitimate privacy, security, legal, or confidentiality reason not to publish it?
3. Does withholding it create a misleading impression about the public implementation?
4. Does it constitute legitimate commercial differentiation rather than arbitrary restriction?
5. Can the commercial value instead be delivered through services, operations, support, integration, or assurance?
6. Is the resulting boundary clearly documented and cross-linked to the relevant Pattern Commons/evidence record?

The default for core scientific/technical claims is **evidence-preserving openness**. The default for private data, secrets, security-sensitive material, and legitimate customer-specific or operational assets is **controlled disclosure**.
