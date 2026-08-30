# NDR Pattern: CDPO-v4.2-HGF

## Full pattern name

Constraint-Dense Prompt Optimization v4.2 with Hensel Generative Firewall

**DGAF-Framework · NDR Pattern Registry**  
**Registered:** S070 · 2026-06-13  
**Status:** Registered design specification; attestation pending  
**Layer:** 7.0 — Meta-Agent Prompt Architecture  
**P-36 classification:** ADVISORY

> **Notation control:** Current mathematical notation is governed by [`MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`](../governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md). `pP` is DGAF-specific Platinum Mean notation for `1/(2sin(π/11)) ≈ 1.774732842`; `ρ` is the plastic number; `ρP` is not canonical mathematical notation.
>
> **Epistemic boundary:** This pattern is a design specification. Its presence does not establish experimental efficacy, security, production readiness, or empirical validation.

## Pattern summary

CDPO-v4.2-HGF specifies a constraint-dense prompt architecture intended to keep governance and registry information separated while allowing advisory topology information to be consumed by a meta-agent prompt.

**Use:** Hard-limited meta-agent prompts where registry constants must remain advisory rather than becoming decision-core authority.

**Trigger:** When registry constants risk being treated as governance authority.

**Design summary:** Literal triggers, micro budgets, a three-plane separation model, polynomial-first registry representation, and an explicit self-audit footer.

## Mechanism

- **Literal trigger stems:** `architect|system|framework|orchestrat|topolog|multi-agent` → Taxonomy REQUIRED. `registry|closure|platinum|hyperplatinum|rho_P|hensel|a_n|delta_n` → Registry Advisory block REQUIRED. The `rho_P` stem is retained only for detection of legacy terminology; it does not define a current constant.
- **Three-plane separation:** Governance uses φ = 1.618… and φ* ≈ 0.618 only. The registry plane supplies tier records through P-39 PRS with schema `{tier, dimension, duration_class, policy_ratio, descriptor, residual, valid_flag, hash}`. The substrate plane uses AutoInit analytic gain per activation.
- **Hyperplatinum:** `h ≈ 11.0007511609`, the real root of `x^4 - 11x^3 - 1 = 0`. Recurrence `a_{n+4} = 11*a_{n+3} + a_n`, seeds 0,0,0,1. Any bound claim requires its stated proof/source memo and reproduction.
- **Standard Platinum `pP`:** `1/(2sin(π/11)) ≈ 1.774732842`, the regular-hendecagon unit-side circumradius. This is DGAF-specific notation and is not the plastic number or a quadratic metallic mean.
- **Identity anchoring:** `intent_hash = SHA256(canonical_author_id || domain_salt || version)`. A literal personal name must not be embedded as a runtime invariant.
- **Micro budgets:** Direct Answer ≤40 tokens; Breakdown ≤120 tokens. Degradation order: drop 7, 6, 5, Tradeoffs details; keep 1–4 inviolate.

## Separation model

Enforcement tightening under compression is paired with plane-separated verification. Advisory ratios may inform registry diagnostics; blocking seals remain separate from governance-plane threshold selection.

## Tradeoffs

| Approach | Pro | Con | Recommended |
|----------|-----|-----|-------------|
| A — Inline firewall only | Zero tooling | Relies on model attention | Single-prompt, no harness |
| B — Inline + self-audit footer | Machine-checkable | Consumes prompt budget | Single-prompt deployments |
| C — Core prompt + external PRS validator | Frees prompt budget | Adds CI latency | When a harness exists |

## Constraints

| Dimension | Value |
|-----------|-------|
| Compute | Recurrence O(n), where recurrence representation is used |
| Latency | Unmeasured by this specification |
| Scale | Design target across DGAF agents; empirical scaling not established here |
| Alignment | Explicit role boundary + uncertainty expression intended to reduce overconfidence |

## Failure controls

| Trigger | Mitigation |
|---------|------------|
| Registry ratio leaks into P-31 SCPE decay or P-32 Phi-Closure Gate | CI linter rejects `registry.*` imports in `governance/` and `PHI` imports in `registry/` |
| Raw h^n logged causing overflow | Schema requires n and a_n only; hash with context salt |
| `pP` treated as plastic number or identity for π | Require explicit descriptor and residual field; fail validation if absent |
| Legacy `ρ_P` treated as current notation | Reject as current mathematical authority; map only through explicit historical/supersession classification |
| Personal name embedded as live key | Require `intent_hash` with key-rotation metadata |
| Almost-integer predictability attack on a_n | Salted hash before public exposure |

## Review considerations

| Lens | Design consideration |
|------|----------------------|
| Formal methods | Store polynomials and recurrences rather than relying on floating-point labels. |
| Systems architecture | Use PRS v0 as the intended source for registry state; keep advisory telemetry separate from blocking boundaries. |
| Security | Use salted hashes for predictable mathematical sequences and explicit identity commitments. |
| Information theory | Track goals, constraints, open questions, and registry use when cross-plane behavior matters. |
| HCI | Use fixed failure syntax and explicit tags to reduce reviewer ambiguity. |
| QA | Keep the self-audit footer machine-parseable when the surrounding deployment requires it. |

## Concrete artifact — Compliance Footer Validator

The following Python stub illustrates the parser contract. It is an implementation example, not evidence that the pattern has achieved its proposed threshold.

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

## Proposed evaluation

**Hypothesis:** A 100-prompt campaign can measure taxonomy recall, legacy-notation leakage, and self-audit-footer parse success under a declared protocol.

**Metric:** Per-section violation count per prompt.

**Threshold:** 0 firewall violations and a pre-specified parse-success threshold agreed before execution.

**Method:** Agent Crucible × Amethyst v4.2-hensel, 50 governance + 50 registry prompts. Proposed results location: `docs/qa/CRUCIBLE_FIREWALL_RESULTS_v1.md`.

No threshold is treated as achieved until a retained experiment artifact supports it.

## Quick check

- [ ] Sections 1–7 are present and ordered as specified by the pattern.
- [ ] Registry Advisory block is present with n and a_n on a registry trigger.
- [ ] Self-audit footer parses with `firewall=PASS` where the deployment requires it.

## Pattern reference

**NDR Name:** CDPO-v4.2-HGF  
**Supersedes:** CDPO-v4 (informal)  
**Related patterns:** P-37, P-38, P-39, P-40 · NDR Hensel Firewall Rules v1.0

*Registered design specification. Attestation pending.*

**Current DGAF/PDMAL control state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.
