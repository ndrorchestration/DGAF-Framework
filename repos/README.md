# Historical Repository Governance Mirrors

The `repos/*` subtree preserves historical governance-propagation records from the July 2026 ecosystem rollout and later audit work.

These mirrors are **historical evidence**, not current cross-repository authority and not a source of truth for the corresponding external repositories.

## Current-authority rule

For a repository represented under this subtree:

1. the repository's own current default-branch source, CI, governance, and retained evidence are authoritative for that repository;
2. `registry/ecosystem_registry.json` is a bounded projection only and must not promote these mirrors into current authority;
3. historical persona labels, DGAF tiers, protocol labels, or governance-owner fields in `repos/*/GOVERNANCE.md` remain searchable provenance but do not reactivate current authority;
4. verification, certification, compliance, runtime health, scientific validity, or production readiness do not transfer across repository boundaries merely because an old mirror says they do.

## Supersession boundary

Current functional-role and authority semantics must be established from current project-local evidence. Historical Amethyst, Sentinel, COLLEEN, DGAF-tier, and related propagation records are retained rather than rewritten so chronology and prior operating assumptions remain auditable.

When a historical mirror conflicts with current project-local evidence, classify the mirror as `HISTORICAL` and preserve it; do not silently use it to overwrite the current source.

This boundary has no scientific-state effect and does not authorize any DGAF transition.
