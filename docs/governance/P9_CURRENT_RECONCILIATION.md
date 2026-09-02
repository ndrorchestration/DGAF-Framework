# P9 Current Reconciliation

**Status:** HISTORICAL SCOPED PASS EXISTS / CURRENT-CANDIDATE REVERIFICATION REQUIRED  
**Last verified:** 2026-09-02  
**Authority class:** Living control reconciliation; non-authorizing

## Current identity boundary

- Corrected apparatus provenance anchor: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Current mainline runtime candidate: `92ff830b1c67413df745e37087e6447c9c251b9a`
- Current runtime candidate tree: `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`
- Controlled completion candidate: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`
- Active P-35 remediation head: `d83ea74c0f7ef7dd3e39a25345d6b201770a370c`

No P9 evidence transfers across candidate identities. A successor candidate requires fresh independent verification against its exact immutable identity.

## Latest scoped P9 evidence

Run `33572123857` completed successfully for exact candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

The retained verification established:

- exact candidate identity;
- independent canonicalization/hash computation;
- authority-identity regression;
- external authorization representation;
- explicit non-execution representation.

Artifact: `9825660346`  
Artifact ZIP digest: `sha256:cf5e475c31bd9258731dcec3e6f36588f9fbfa80c3bb787419b54770ccae7976`  
Independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`

This is a **historical scoped P9 PASS for `a43219b…`**. It is not current evidence for the mainline runtime candidate `92ff830b…`, the active P-35 remediation head `d83ea74c…`, or any successor candidate.

## Superseded P9 evidence

Run `33567199896` verified prior completion candidate `562753b3053b3566b0fcad1b0b1df151d7de119a`, with artifact `9823570326`. That candidate is superseded. Its evidence is retained for provenance and must not be described as the latest P9 execution.

## Current disposition

| Boundary | Status |
|---|---|
| P9 on `a43219b…` | HISTORICAL SCOPED PASS |
| P9 on `92ff830b…` | REVERIFICATION REQUIRED for pilot use |
| P9 on `d83ea74c…` | ENGINEERING/PRE-FREEZE ONLY; not experimental candidate |
| P9 on future selected candidate | REQUIRED |
| Freeze | NOT ESTABLISHED |
| Authorization | NOT GRANTED |
| Empirical N | 0 |

## Naming rule

This file intentionally uses **CURRENT RECONCILIATION**, not **LATEST RECONCILIATION**, because a dated verification record can remain valid historical evidence after a newer candidate supersedes it. Historical records must be named or labeled so they cannot masquerade as current authority.

The former `P9_LATEST_RECONCILIATION_2026-09-01.md` record, where retained, is historical evidence for its recorded candidate and must not be used as the current P9 authority record.

## Boundary

This document does not authorize P9 execution, freeze creation, pilot execution, unblinding, or an increase in empirical N.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
