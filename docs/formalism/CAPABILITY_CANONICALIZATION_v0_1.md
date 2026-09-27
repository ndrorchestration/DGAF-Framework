# DGAF Capability Action Canonicalization v0.1

> **Status:** PROSPECTIVE / NON-AUTHORIZING  
> **Identifier:** `dgaf-json-v0.1`

## Purpose

Action-specific approvals, authorization objects, receipts, and replay controls need a stable byte representation for digest binding.

DGAF JSON v0.1 defines a deliberately narrow canonicalization profile for the initial reference implementation. It is not claimed to be a universal canonical-JSON standard.

## Rules

The canonical payload:

- MUST be valid JSON data;
- MUST reject NaN and Infinity;
- MUST sort object keys lexicographically;
- MUST emit no insignificant whitespace;
- MUST encode as UTF-8;
- MUST preserve Unicode characters rather than ASCII-escape them;
- MUST preserve array ordering;
- MUST not infer missing values from defaults during digest generation.

The digest format is:

```text
sha256:<64 lowercase hexadecimal characters>
```

## Minimum action envelope

The digest-bound envelope SHOULD include:

- canonicalization profile identifier;
- capability ID and version;
- resource identity/scope;
- material parameters;
- initiating principal;
- executing principal;
- delegation-chain identity, if any;
- policy ID and version;
- volatile state guards selected for binding;
- single-use or replay-resistant nonce.

Material changes to any bound field MUST produce a different digest.

## Compatibility

A future canonicalization profile MUST use a new identifier. Implementations MUST NOT silently reinterpret an existing profile identifier.

Where interoperability requires an external canonicalization standard, DGAF may define a profile mapping, but an approval or authorization MUST identify the exact profile used.

## Security boundary

Canonicalization creates stable bytes; it does not establish authorization, trust, semantic equivalence, or provider identity by itself.
