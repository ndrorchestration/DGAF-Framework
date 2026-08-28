# NDR Pattern: CDPO-v4.2-HGF

**Constraint-Dense Prompt Optimization v4.2 with Hensel Generative Firewall**

**DGAF-Framework · NDR Pattern Registry**  
**Registered:** S070 · 2026-06-13  
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)  
**Attestation:** Pending — Apogee P-11 review required before CANONICAL  
**Layer:** 7.0 — Meta-Agent Prompt Architecture  
**P-36 classification:** ADVISORY

> **Notation control:** Current mathematical notation is governed by `docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`. `pP` is DGAF-specific Platinum Mean notation for `1/(2sin(π/11)) ≈ 1.774732842`; `ρ` is the plastic number; `ρP` is not canonical mathematical notation.
>
> **Epistemic boundary:** This pattern is a design specification. Its presence does not establish experimental efficacy, security, production readiness, or empirical validation.

---

## Pattern Spec

**Name:** Constraint-Dense Prompt Optimization v4.2 with Hensel Generative Firewall (CDPO-v4.2-HGF)

**Core Skill:** Constraint-optimized prompt refinement with topology-plane firewall → raise enforceable compliance per character while preserving substrate agnosticism.

**Use:** Hard-limited meta-agent prompts that keep φ-governance substrate-agnostic while consuming advisory topology ratios.

**Trigger:** When registry constants risk entrainment of the decision core.

**Spec summary:** Maximize MUST rules per character via literal triggers, micro budgets, three-plane firewall, polynomial-first registry, and self-audit footer.

---

## Mechanism

- **Literal trigger stems:** `architect|system|framework|orchestrat|topolog|multi-agent` → Taxonomy REQUIRED. `registry|closure|platinum|hyperplatinum|rho_P|hensel|a_n|delta_n` → Registry Advisory block REQUIRED. The `rho_P` stem is retained only for detection of legacy terminology; it does not define a current constant.
- **Three-plane firewall as MUST rules:** Governance plane uses φ = 1.618… and φ* ≈ 0.618 only. Registry plane supplies tier records via P-39 PRS with schema `{tier, dimension, duration_class, policy_ratio, descriptor, residual, valid_flag, hash}`. Substrate plane uses AutoInit analytic gain per activation.
- **Hyperplatinum h ≈ 11.0007511609:** Real root of `x^4 - 11x^3 - 1 = 0`, a Pisot-Vijayaraghavan number. Recurrence `a_{n+4} = 11*a_{n+3} + a_n`, seeds 0,0,0,1. Bound claims require their stated proof/source memo and reproduction.
- **Standard Platinum `pP`:** `1/(2sin(π/11)) ≈ 1.774732842`, the regular-hendecagon unit-side circumradius. It is DGAF-specific notation and is not the plastic number or a quadratic metallic mean.
- **Identity anchoring:** `intent_hash = SHA256(canonical_author_id || domain_salt || version)`. Never embed a literal personal name as a runtime invariant.
- **Micro budgets:** Direct Answer ≤40 tokens, Breakdown ≤120 tokens. Degradation order: drop 7, 6, 5, Tradeoffs details; keep 1–4 inviolate.

---

## Pattern

Enforcement tightening under compression plus plane-separated verification. Advisory ratios may inform registry diagnostics; blocking seals remain separate from governance-plane threshold selection.

---

## Tradeoffs

| Approach | Pro | Con | Recommended |
|----------|-----|-----|-------------|
| A — Inline firewall only | Zero tooling | Relies on model attention | Single-prompt, no harness |
| B — Inline + Compliance footer | Machine-checkable | Consumes ~90 chars | **Single-prompt deployments** |
| C — Core prompt + external PRS validator | Frees prompt budget | Adds CI latency | **When a harness exists** |

---

## Constraints

| Dimension | Value |
|-----------|-------|
| Compute | Recurrence O(n), where recurrence representation is used |
| Latency | Unmeasured by this specification |
| Scale | Design target across DGAF agents; empirical scaling not established here |
| Alignment | Explicit role boundary + uncertainty expression intended to reduce overconfidence |

---

## Failures

| Trigger | Mitigation | Tag |
|---------|-----------|-----|
| Registry ratio leaks into P-31 SCPE decay or P-32 Phi-Closure Gate | CI linter rejects `registry.*` imports in `governance/` and `PHI` imports in `registry/` | |
| Raw h^n logged causing overflow | Schema requires n and a_n only; hash with context salt | |
| `pP` treated as plastic number or identity for π | Require explicit descriptor and residual field; fail validation if absent | |
| Legacy `ρ_P` treated as current notation | Reject as current mathematical authority; map only through explicit historical/supersession classification | |
| Personal name embedded as live key | Require `intent_hash` with key rotation metadata | `[NON-OBVIOUS]` |
| Almost-integer predictability attack on a_n | Salted hash before public exposure | `[NON-OBVIOUS]` |

---

## Expert Lens Upgrades

| Lens | Change | Why |
|------|--------|-----|
| Formal Methods | Store polynomials and recurrences, not floats | Enables reproducible symbolic representation and replay |
| Systems Architect | PRS v0 as single source of truth; P-37, P-39, P-40 as read-only telemetry in v0 | Separates advisory and blocking boundaries |
| Security | Salted hash of a_n before public exposure; cryptographic intent commitment | Reduces predictable public exposure |
| Information Theory | Extend state to `goals[], constraints[], openQs[], registry_tier_used[]` | Makes cross-plane crossings visible across turns |
| HCI | Fixed failure syntax `trigger=>mitigation` with `[NON-OBVIOUS]` tag | Lowers reviewer load |
| QA | Compliance footer includes `registry_key_valid`, `closure_achieved`, `firewall` | Allows self-audit without parsing body |

---

## Concrete Artifact — Compliance Footer Validator (Python stub)

```python
import re

COMPLIANCE_PATTERN = re.compile(
    r'taxonomy=(?P<taxonomy>Y|N),\s*'
    r'failures=(?P<failures>\d+),\s*'
    r'artifact=(?P<artifact>[\w_]+),\s*'
    r'registry_tier=(?P<registry_tier>NONE|Subplatinum|pP|sigma_P|h|Ultraplatinum),\s*'
    r'registry_key_valid=(?P<registry_key_valid>Y|N|NA),\s*'
    r'closure_achieved=(?P<closure_achieved>Y|N|NA),\s*'
    r'firewall=(?P<firewall>PASS|FAIL),\s*'
    r'version=(?P<version>v[\d.\w-]+)'
)


def validate_compliance_footer(text: str) -> dict:
    """Parse and validate the Compliance footer."""
    match = COMPLIANCE_PATTERN.search(text)
    if not match:
        raise ValueError("[INVALID] Compliance footer absent or malformed")
    fields = match.groupdict()
    if fields['firewall'] == 'FAIL':
        raise ValueError(f"[INVALID] firewall=FAIL in Compliance footer: {fields}")
    return fields
```

---

## Next Experiment

**Hypothesis:** A 100-prompt Crucible campaign can measure taxonomy recall, legacy-notation leakage, and Compliance-footer parse success under the declared protocol.

**Metric:** Per-section violation count per prompt.

**Threshold:** 0 firewall violations and a pre-specified parse-success threshold agreed before execution.

**Method:** Agent Crucible × Amethyst v4.2-hensel, 50 governance + 50 registry prompts. Results → `docs/qa/CRUCIBLE_FIREWALL_RESULTS_v1.md`.

No threshold is treated as achieved until the retained experiment artifact supports it.

---

## Quick Check

- [ ] Sections 1–7 in order, Taxonomy line present on trigger
- [ ] Registry Advisory block present with n and a_n on registry trigger
- [ ] Compliance footer parses with `firewall=PASS`

---

## Pattern Reference

**NDR Name:** CDPO-v4.2-HGF  
**Supersedes:** CDPO-v4 (informal)  
**Related patterns:** P-37, P-38, P-39, P-40 · NDR Hensel Firewall Rules v1.0

---

*CDPO-v4.2-HGF · Registered S070 · 2026-06-13*  
*Attestation pending. Amethyst × COLLEEN*  
*See also: docs/agents/AMETHYST_AGENT_SPEC_v4.2-hensel.md*

**Current DGAF/PDMAL control state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.
