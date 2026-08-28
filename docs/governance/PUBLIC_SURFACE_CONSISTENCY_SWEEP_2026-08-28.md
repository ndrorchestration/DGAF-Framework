# Public Surface & Cross-Consistency Sweep — 2026-08-28

## Purpose

Record a non-execution documentation QA sweep performed against the DGAF public repository surface. This sweep evaluates coherence, cross-document consistency, navigation integrity, epistemic scope, and separation of internal versus public project surfaces.

## Sweep result

**Publication posture: controlled / fail-closed.** No experimental authorization, freeze, or empirical execution was performed.

### 1. Public-surface lens

`docs/governance/PUBLIC_SURFACE_QA_STANDARD.md` is the governing publication-quality control for GitHub-visible material. It requires review of truth, authority, audience, utility, placement, navigation, professional representation, disclosure, community fit, maintenance, identity integrity, and reader friction.

Personal Notion pages and private operational records are not public GitHub navigation targets by default. Public landing surfaces should resolve to repository-local or intentionally designated public resources.

### 2. README navigation sweep

The README was reviewed for repository-local navigation. Governance links were normalized to the repository's actual case-sensitive `docs/GOVERNANCE/` paths where those directories are named in uppercase. This prevents the public landing surface from pointing at non-resolving paths while retaining the existing project organization.

### 3. Current-state separation

The README distinguishes repository `main` from the experimental apparatus candidate. Documentation-only commits do not redefine the candidate. Historical candidates, freezes, runs, and acceptance records remain provenance unless explicitly rebound.

### 4. Mathematical-hygiene sweep

The repository still contains historical references to the former `1.7747` value, including formalism material. These references are not silently deleted. They require historical/superseded classification and must not be used as current PDMAL mathematics.

A specific legacy formalism document, `docs/formalism/constants/11Q-derivation.md`, still contains language that describes `1.7747` as previously verified and uses it in a derivation context. This is a **follow-up classification/control item**, not evidence for current PDMAL mathematics. The appropriate treatment is to preserve provenance while making supersession unmistakable and preventing downstream interpretation as current truth.

### 5. Epistemic boundary sweep

Current public documentation preserves the distinction between:

`defined → implemented → computed → verified → attested → historical`

and does not treat a mathematical correction, component test, deployment state, or historical attestation as proof of system-level convergence, robustness, security, production validity, or superiority.

### 6. Experimental-state sweep

The public surface continues to represent the experimental track as:

- PRE-FREEZE
- FAIL-CLOSED
- NO FREEZE
- PILOT AUTHORIZATION NOT GRANTED
- EMPIRICAL N = 0

No documentation-only sweep changes these states.

## Follow-up queue

1. Classify/supersede the remaining legacy `1.7747` formalism references without erasing provenance.
2. Continue repository-wide public-link and navigation verification.
3. Continue cross-document terminology/state consistency sweeps.
4. Keep internal Notion operational records separated from public GitHub navigation unless a specific public surface is intentionally designated.
5. Do not infer authorization, freeze, or empirical evidence from documentation changes.

## Non-execution declaration

This sweep is documentation QA only. It does not execute the PDMAL pilot, alter candidate identity, create a freeze, grant authorization, or increase empirical N.
