# NDR Pattern: CDPO-v4.2-HGF

**Constraint-Dense Prompt Optimization v4.2 with Hensel Generative Firewall**

**DGAF-Framework · NDR Pattern Registry**
**Registered:** S070 · 2026-06-13
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)
**Attestation:** Pending — Apogee P-11 review required before CANONICAL
**Layer:** 7.0 — Meta-Agent Prompt Architecture
**P-36 classification:** ADVISORY

---

## Pattern Spec

**Name:** Constraint-Dense Prompt Optimization v4.2 with Hensel Generative Firewall (CDPO-v4.2-HGF)

**Core Skill:** Constraint-optimized prompt refinement with topology-plane firewall → raise enforceable compliance per character while preserving substrate agnosticism.

**Use:** Hard-limited meta-agent prompts that must keep φ-governance substrate-agnostic while consuming advisory topology ratios.

**Trigger:** When registry constants risk entrainment of the decision core.

**Spec summary:** Maximize MUST rules per character via literal triggers, micro budgets, three-plane firewall, polynomial-first registry, and self-audit footer.

---

## Mechanism

- **Literal trigger stems:** `architect|system|framework|orchestrat|topolog|multi-agent` → Taxonomy REQUIRED. `registry|closure|platinum|hyperplatinum|rho_P|hensel|a_n|delta_n` → Registry Advisory block REQUIRED.
- **Three-plane firewall as MUST rules:** Governance plane uses φ = 1.618… and φ* ≈ 0.618 only. Registry plane supplies tier records via P-39 PRS with schema `{tier, dimension, duration_class, policy_ratio, descriptor, residual, valid_flag, hash}`. Substrate plane uses AutoInit analytic gain per activation (Bingham & Miikkulainen).
- **Hyperplatinum h ≈ 11.0007511609:** Real root of `x^4 - 11x^3 - 1 = 0`, a Pisot-Vijayaraghavan number. Recurrence `a_{n+4} = 11*a_{n+3} + a_n`, seeds 0,0,0,1. Bound `|δ_n| ≤ Cρ^n`, ρ ≈ 0.4526, C = 3. Persist n and a_n only.
- **Standard Platinum ρ_P:** Either 1/(2sin(π/11)) ≈ 1.774732 or √π ≈ 1.772454. Not a metallic mean. Log residual if ρ_P² ≈ π heuristic used.
- **Identity anchoring:** `intent_hash = SHA256(canonical_author_id || domain_salt || version)`. Never embed literal personal name as runtime invariant.
- **Micro budgets:** Direct Answer ≤40 tokens, Breakdown ≤120 tokens. Degradation order: drop 7, 6, 5, Tradeoffs details; keep 1-4 inviolate.

---

## Pattern

Enforcement tightening under compression plus plane-separated verification. ADVISORY ratios to orchestration, BLOCKING seals to registry commit.

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
| Compute | Recurrence O(n), negligible to n=20 |
| Latency | Unchanged from v4 |
| Scale | Stable across DGAF agents |
| Alignment | Explicit role boundary + uncertainty expression reduce overconfidence |

---

## Failures

| Trigger | Mitigation | Tag |
|---------|-----------|-----|
| Registry ratio leaks into P-31 SCPE decay or P-32 Phi-Closure Gate | CI linter rejects `registry.*` imports in `governance/` and `PHI` imports in `registry/` | |
| Raw h^n logged causing overflow | Schema requires n and a_n only; hash with context salt | |
| ρ_P treated as metallic mean or identity for π | Require descriptor with residual field; fail validation if absent | |
| Personal name embedded as live key | Require `intent_hash` with key rotation metadata | `[NON-OBVIOUS]` |
| Almost-integer predictability attack on a_n | Salted hash before public exposure | `[NON-OBVIOUS]` |

---

## Expert Lens Upgrades

| Lens | Change | Why |
|------|--------|-----|
| Formal Methods | Store polynomials and recurrences, not floats; PV proof memo for h with ρ bound | Enables bit-identical replay and δ_n decay guarantee |
| Systems Architect | PRS v0 as single source of truth; P-37, P-39, P-40 as read-only telemetry in v0 | Implements ADVISORY vs BLOCKING classification |
| Security | Salted hash of a_n before public exposure; cryptographic intent commitment | Blocks almost-integer predictability attacks and preserves transferability |
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
    r'registry_tier=(?P<registry_tier>NONE|Subplatinum|rho_P|sigma_P|h|Ultraplatinum),\s*'
    r'registry_key_valid=(?P<registry_key_valid>Y|N|NA),\s*'
    r'closure_achieved=(?P<closure_achieved>Y|N|NA),\s*'
    r'firewall=(?P<firewall>PASS|FAIL),\s*'
    r'version=(?P<version>v[\d.\w-]+)'
)

def validate_compliance_footer(text: str) -> dict:
    """
    Parse and validate Compliance footer from Amethyst v4.2-hensel output.
    Returns parsed fields or raises ValueError with missing items.
    """
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

**Hypothesis:** 100-prompt Crucible campaign achieves taxonomy recall ≥95%, zero governance sections with raw ρ_P/h literals, Compliance parse ≥98%.
**Metric:** Per-section violation count per prompt.
**Threshold:** 0 firewall violations, ≥98% parse success.
**Method:** Agent Crucible × Amethyst v4.2-hensel, 50 governance + 50 registry prompts. Results → `docs/qa/CRUCIBLE_FIREWALL_RESULTS_v1.md`.

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
