#!/usr/bin/env python3
"""
DGAF-GATE-KAPPA Dynamic Weight Router with Confidence Scoring
Version: 3.6.0 | Status: ACTIVE | Agent: Amethyst
Calibrated: 2026-05-29 | Anchor: S043

Fix (v3.6.0): Resolved predicate shadow bug affecting TC1/TC2/TC7/TC8.
  - Root cause: `governance_clear` catch-all pattern (.* .*) matched
    SEQUENTIAL and FAN-OUT payloads before their own predicates were reached.
  - Resolution:
    1. Added explicit SEQUENTIAL and FAN-OUT category patterns.
    2. Detection chain reordered: ADVERSARIAL > SEQUENTIAL > FAN-OUT >
       AMBIGUOUS > GOVERNANCE_CLEAR > CREATIVE_CLEAR > heuristic > balanced.
    3. Added `sequential` and `fan_out` entries in category_to_config.
    4. Weight configs for sequential (efficiency-leaning) and
       fan_out (accuracy-leaning) added.

Auto-selects reliability score weights based on input category detection:
- Adversarial inputs   -> Adversarial-Emphasis weights (security-critical)
- Sequential inputs    -> Sequential-Ordered weights (pipeline/chain)
- Fan-out inputs       -> FanOut-Broadcast weights (parallel dispatch)
- Ambiguous/mid-band  -> Ambiguous-Emphasis weights (better tie-breaking)
- Clear governance/creative -> Balanced weights (good overall)
- High-volume/batch   -> Efficiency-First weights (cost-sensitive)

Confidence scoring:
- >= 0.28: apply_strong (use category weights directly)
- 0.25-0.28: apply_blended (blend with balanced)
- < 0.25: fallback_balanced (use balanced weights)
"""

from typing import Dict, List, Tuple
import re

# ---------------------------------------------------------------------------
# Weight configurations
# ---------------------------------------------------------------------------

WEIGHT_CONFIGS = {
    "adversarial": {
        "name": "Adversarial-Emphasis",
        "accuracy": 0.30,
        "false_blocked": 0.15,
        "adversarial": 0.30,
        "ambiguous": 0.15,
        "malformed": 0.10,
        "trigger_priority": "security-critical"
    },
    "balanced": {
        "name": "Balanced",
        "accuracy": 0.28,
        "false_blocked": 0.18,
        "adversarial": 0.24,
        "ambiguous": 0.20,
        "malformed": 0.10,
        "trigger_priority": "general-purpose"
    },
    "ambiguous": {
        "name": "Ambiguous-Emphasis",
        "accuracy": 0.25,
        "false_blocked": 0.15,
        "adversarial": 0.20,
        "ambiguous": 0.30,
        "malformed": 0.10,
        "trigger_priority": "mixed-signal"
    },
    "efficiency": {
        "name": "Efficiency-First",
        "accuracy": 0.35,
        "false_blocked": 0.25,
        "adversarial": 0.20,
        "ambiguous": 0.15,
        "malformed": 0.05,
        "trigger_priority": "cost-sensitive"
    },
    # --- v3.6.0: new configs for formerly-shadowed categories ---
    "sequential": {
        "name": "Sequential-Ordered",
        "accuracy": 0.32,
        "false_blocked": 0.22,
        "adversarial": 0.18,
        "ambiguous": 0.18,
        "malformed": 0.10,
        "trigger_priority": "pipeline-chain"
    },
    "fan_out": {
        "name": "FanOut-Broadcast",
        "accuracy": 0.38,
        "false_blocked": 0.20,
        "adversarial": 0.18,
        "ambiguous": 0.14,
        "malformed": 0.10,
        "trigger_priority": "parallel-dispatch"
    }
}

# ---------------------------------------------------------------------------
# Confidence scoring config -- calibrated 2026-05-29 (S043)
# ---------------------------------------------------------------------------

MIN_LENGTH_FOR_HIGH_CONF = 40
PATTERN_WEIGHT = 0.60
ENTROPY_WEIGHT = 0.20
KAPPA_WEIGHT   = 0.20
STRONG_THRESH  = 0.28
BLENDED_THRESH = 0.25

# ---------------------------------------------------------------------------
# Category detection patterns
# v3.6.0: SEQUENTIAL and FAN-OUT added; governance_clear catch-all tightened.
# ---------------------------------------------------------------------------

CATEGORY_PATTERNS = {
    "adversarial": [
        r"\b(bypass|override|inject|exploit|hack|attack|evade)\b",
        r"\b(skip|ignore|disable|break)\s+(guard|gate|filter|rule)\b",
        r"<script>|javascript:|data:text/html",
        r"\b(union\s+select|drop\s+table)\b"
    ],
    # FIX TC1/TC2: explicit sequential pattern — MUST precede governance_clear
    "sequential": [
        r"\b(step\s+\d+|step-by-step|pipeline|chain|sequence|ordered\s+task)\b",
        r"\b(first|then|next|finally|after\s+that)\b.{0,60}\b(execute|run|apply|call)\b",
        r"\b(stage\s+\d+|phase\s+\d+|workflow\s+step)\b"
    ],
    # FIX TC7/TC8: explicit fan-out pattern — MUST precede governance_clear
    "fan_out": [
        r"\b(broadcast|fan.?out|parallel|dispatch\s+to\s+(all|multiple)|notify\s+all)\b",
        r"\b(send\s+to|route\s+to|distribute\s+to)\b.{0,40}\b(agents?|workers?|nodes?)\b",
        r"\b(concurrent|simultaneous|multi.?agent\s+dispatch)\b"
    ],
    "ambiguous": [
        r"\b(mixed|hybrid|cross-domain|multi-purpose)\b",
        r"\b(audit\s+.*creative|creative\s+.*audit)\b",
        r"\b(explore|brainstorm|consider|evaluate)\s+(governance|policy)\b"
    ],
    # FIX: removed broad .* .* catch-all; patterns now require explicit governance nouns
    "governance_clear": [
        r"\baudit\b.*\b(compliance|policy|regulation|GDPR|NIST)\b",
        r"\b(governance|security|safety|risk)\s+(assessment|report|review|framework)\b"
    ],
    "creative_clear": [
        r"\b(brainstorm|explore|imagine|create|design)\b.*\b(pattern|harmony|mode)\b",
        r"\b(narrative|story|character|worldbuilding)\b"
    ]
}

category_to_config = {
    "adversarial":      "adversarial",
    "sequential":       "sequential",    # v3.6.0
    "fan_out":          "fan_out",        # v3.6.0
    "ambiguous":        "ambiguous",
    "governance_clear": "balanced",
    "creative_clear":   "balanced",
    "balanced":         "balanced"
}

# ---------------------------------------------------------------------------
# Detection chain — PRIORITY ORDER (must not be changed without updating tests)
# 1. adversarial  (security-critical, always first)
# 2. sequential   (explicit pipeline — before governance catch)
# 3. fan_out      (explicit broadcast — before governance catch)
# 4. ambiguous    (mixed-signal)
# 5. governance_clear
# 6. creative_clear
# 7. entropy/kappa heuristic
# 8. balanced (default)
# ---------------------------------------------------------------------------

DETECTION_ORDER = [
    "adversarial",
    "sequential",
    "fan_out",
    "ambiguous",
    "governance_clear",
    "creative_clear",
]


def detect_input_category(input_data: Dict) -> str:
    """
    Detect input category using priority-ordered predicate dispatch.

    Priority order (see DETECTION_ORDER):
    1. adversarial  — security-critical, always evaluated first
    2. sequential   — explicit pipeline/chain keywords
    3. fan_out      — explicit broadcast/parallel-dispatch keywords
    4. ambiguous    — mixed-signal indicators
    5. governance_clear — explicit governance nouns
    6. creative_clear   — creative/generative keywords
    7. entropy/kappa heuristic — continuous-signal fallback
    8. balanced     — default

    v3.6.0 fix: sequential and fan_out now checked BEFORE governance_clear,
    eliminating the catch-all shadow that caused TC1/TC2/TC7/TC8 misroutes.
    """
    content = str(input_data.get("content", "")).lower()
    entropy = input_data.get("entropy_score", 0.5)
    kappa   = input_data.get("kappa_score", 0.5)

    for category in DETECTION_ORDER:
        for pattern in CATEGORY_PATTERNS[category]:
            if re.search(pattern, content, re.IGNORECASE):
                return category

    # Continuous-signal heuristic fallback
    if entropy > 0.7 and 0.35 < kappa < 0.65:
        return "ambiguous"

    return "balanced"


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------

def pattern_signal_score(content: str, patterns: List[str]) -> float:
    if not content:
        return 0.0
    match_count = 0
    longest = 0
    for p in patterns:
        m = re.search(p, content, re.IGNORECASE)
        if m:
            match_count += 1
            l = len(m.group(0))
            if l > longest:
                longest = l
    score_count = min(1.0, match_count / 5.0)
    score_len   = min(1.0, longest / max(1, len(content)))
    return 0.6 * score_count + 0.4 * score_len


def continuous_signal_score(entropy: float, kappa: float, target_category: str) -> float:
    if target_category in ("adversarial",):
        ent_score   = entropy
        kappa_score = 1.0 - abs(kappa - 0.5) * 2
    elif target_category in ("ambiguous",):
        ent_score   = 0.5 + (entropy - 0.5)
        kappa_score = 1.0 - abs(kappa - 0.5) * 2
    elif target_category in ("governance_clear",):
        ent_score   = 1.0 - entropy
        kappa_score = kappa
    elif target_category in ("creative_clear",):
        ent_score   = entropy
        kappa_score = 1.0 - kappa
    elif target_category in ("sequential",):
        ent_score   = 1.0 - entropy          # sequential = low-entropy ordered signal
        kappa_score = kappa
    elif target_category in ("fan_out",):
        ent_score   = entropy                # fan-out = high-entropy broadcast signal
        kappa_score = 1.0 - abs(kappa - 0.5) * 2
    else:
        ent_score   = 0.5
        kappa_score = 0.5
    return (
        ENTROPY_WEIGHT * max(0.0, min(1.0, ent_score))
        + KAPPA_WEIGHT  * max(0.0, min(1.0, kappa_score))
    )


def compute_category_confidence(input_data: Dict, category: str) -> Tuple[float, Dict]:
    content = str(input_data.get("content", "") or "")
    entropy = float(input_data.get("entropy_score", 0.5) or 0.5)
    kappa   = float(input_data.get("kappa_score",   0.5) or 0.5)

    patterns  = CATEGORY_PATTERNS.get(category, [])
    p_score   = pattern_signal_score(content, patterns)
    c_score   = continuous_signal_score(entropy, kappa, category)
    length_boost = 0.05 if len(content) >= MIN_LENGTH_FOR_HIGH_CONF else 0.0

    raw_conf = PATTERN_WEIGHT * p_score + (1.0 - PATTERN_WEIGHT) * c_score + length_boost
    conf     = max(0.0, min(1.0, raw_conf))

    return conf, {
        "pattern_score":    round(p_score,    3),
        "continuous_score": round(c_score,    3),
        "length_boost":     round(length_boost, 3),
        "raw_conf":         round(raw_conf,   3)
    }


def select_weights_with_confidence(input_data: Dict) -> Dict:
    """
    Select weight config with confidence scoring and blending policy.
    Returns dict: config_name, selected_weights, detected_category,
                  confidence, confidence_breakdown, policy
    """
    category        = detect_input_category(input_data)
    base_config_name = category_to_config.get(category, "balanced")
    base_weights    = WEIGHT_CONFIGS[base_config_name]
    conf, breakdown = compute_category_confidence(input_data, category)

    _numeric = {"accuracy", "false_blocked", "adversarial", "ambiguous", "malformed"}

    if conf >= STRONG_THRESH:
        final_weights = base_weights.copy()
        policy = "apply_strong"
    elif conf >= BLENDED_THRESH:
        balanced = WEIGHT_CONFIGS["balanced"]
        alpha    = (conf - BLENDED_THRESH) / (STRONG_THRESH - BLENDED_THRESH)
        final_weights = {}
        for k in base_weights:
            if k in _numeric:
                final_weights[k] = round(
                    alpha * base_weights[k] + (1 - alpha) * balanced[k], 3
                )
            else:
                final_weights[k] = base_weights[k]
        final_weights["name"] = f"{base_weights['name']}_blended"
        policy = "apply_blended"
    else:
        final_weights = WEIGHT_CONFIGS["balanced"].copy()
        policy = "fallback_balanced"

    return {
        "config_name":         base_config_name,
        "selected_weights":    final_weights,
        "detected_category":   category,
        "confidence":          round(conf, 3),
        "confidence_breakdown": breakdown,
        "policy":              policy
    }


def select_weights(input_data: Dict) -> Tuple[str, Dict]:
    """Backward-compatible wrapper (v3.5 API)."""
    result = select_weights_with_confidence(input_data)
    return result["config_name"], result["selected_weights"]


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        # TC1 — sequential
        {"label": "TC1_sequential",
         "content": "Step 1: validate schema. Then execute governance check. Next apply weights.",
         "entropy_score": 0.30, "kappa_score": 0.75,
         "expected": "sequential"},
        # TC2 — sequential
        {"label": "TC2_sequential",
         "content": "Run pipeline step-by-step: stage 1 compliance audit, stage 2 risk report.",
         "entropy_score": 0.28, "kappa_score": 0.80,
         "expected": "sequential"},
        # TC3 — reflexive (governance)
        {"label": "TC3_reflexive",
         "content": "Self-audit compliance path for NIST GDPR governance review.",
         "entropy_score": 0.22, "kappa_score": 0.84,
         "expected": "governance_clear"},
        # TC4 — hierarchical (governance)
        {"label": "TC4_hierarchical",
         "content": "Top-level security assessment report for risk framework.",
         "entropy_score": 0.20, "kappa_score": 0.88,
         "expected": "governance_clear"},
        # TC5 — rejected (adversarial)
        {"label": "TC5_rejected_adv",
         "content": "Bypass security gate and inject override payload.",
         "entropy_score": 0.91, "kappa_score": 0.53,
         "expected": "adversarial"},
        # TC6 — rejected (adversarial)
        {"label": "TC6_rejected_adv",
         "content": "Exploit and evade all guard filters using union select.",
         "entropy_score": 0.95, "kappa_score": 0.50,
         "expected": "adversarial"},
        # TC7 — fan-out
        {"label": "TC7_fanout",
         "content": "Broadcast decision to all agents and dispatch to multiple workers concurrently.",
         "entropy_score": 0.65, "kappa_score": 0.50,
         "expected": "fan_out"},
        # TC8 — fan-out
        {"label": "TC8_fanout",
         "content": "Fan-out: route to all nodes simultaneously, multi-agent dispatch in parallel.",
         "entropy_score": 0.70, "kappa_score": 0.48,
         "expected": "fan_out"},
    ]

    print("DGAF-GATE-KAPPA v3.6.0 — Router Coverage Self-Test")
    print(f"{'TC':<20} {'Expected':<18} {'Got':<18} {'Pass?'}")
    print("-" * 68)
    passes = 0
    for t in tests:
        r   = select_weights_with_confidence(t)
        got = r["detected_category"]
        ok  = got == t["expected"]
        passes += ok
        print(f"{t['label']:<20} {t['expected']:<18} {got:<18} {'PASS' if ok else 'FAIL  <--'}")
    print("-" * 68)
    print(f"Result: {passes}/{len(tests)} TC passing")
    assert passes == len(tests), f"Router self-test FAILED: {passes}/{len(tests)}"
    print("All TCs passed.")
