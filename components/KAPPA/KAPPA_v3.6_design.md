# DGAF-GATE-KAPPA v3.6 Design Specification
## governance_clear Accuracy Improvement: 82.6% → Target ≥95%

**Status:** 🟡 IN DESIGN  
**Co-Orchestrated by:** Amethyst (meta-orchestrator) × COLLEEN (routing/automation)  
**NDR Pattern:** Adaptive Weighting with Confidence Gates  
**GitHub Issue:** [#5](https://github.com/ndrorchestration/DGAF-Framework/issues/5)  
**Predecessor:** DGAF-GATE-KAPPA-v3.5 (95% overall, 0 adversarial failures)  
**Date:** 2026-05-30  

---

## 1. Problem Statement

KAPPA v3.5 achieves **95% overall accuracy** across all categories with **0 critical adversarial failures**. However, one category underperforms:

| Category | v3.5 Accuracy | Target | Gap |
|----------|--------------|--------|-----|
| adversarial | 100% | 100% | ✅ None |
| ambiguous | 94.7% | ≥90% | ✅ None |
| **governance_clear** | **82.6%** | **≥95%** | **⚠️ -12.4pp** |
| creative_clear | 100% | ≥90% | ✅ None |
| unclear | 100% | 100% | ✅ None |

**Root Cause:** Governance inputs with moderate confidence (0.33–0.49) are classified as `apply_strong` when the expected policy is `apply_blended`. The current regex-only detection produces over-calibrated confidence scores that land in the `apply_strong` band (≥0.28) when the semantic signal points to a softer blended application.

**Risk Assessment:** This is a **safe over-application** — not a security vulnerability. No critical adversarial failures introduced. The fix improves routing precision only.

---

## 2. Root Cause Deep Dive

### Current Architecture (v3.5)
```
Input → Regex Pattern Matcher → Raw Score → Confidence Band Classifier → Route
                                    ↑
                           governance_clear inputs
                           score: 0.33–0.49 (lands in apply_strong band)
                           expected: apply_blended band
```

### Failure Mode
The regex patterns for `governance_clear` are over-sensitive — they fire on partial matches and inflate the raw score above the `apply_strong` threshold (0.28). The semantic content of governance_clear inputs is "apply policy but with discretion" — this should route to `apply_blended`, not `apply_strong`.

### Confidence Band Collision
```
Current bands (v3.5):
  apply_strong:  score ≥ 0.28
  apply_blended: score 0.15–0.28
  apply_light:   score < 0.15

Problem: governance_clear inputs score 0.33–0.49 → incorrectly route to apply_strong
Fix:     governance_clear inputs should route to apply_blended regardless of raw score
```

---

## 3. Proposed Fix: v3.6 Architecture

### 3.1 Lightweight ML Classifier (Primary Fix)

Replace regex-only `governance_clear` detection with a **logistic regression classifier over TF-IDF features**:

```python
# v3.6 governance_clear classifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

governance_clear_classifier = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=5000,
        sublinear_tf=True
    )),
    ('clf', LogisticRegression(
        C=1.0,
        class_weight='balanced',
        max_iter=1000,
        random_state=42
    ))
])
```

**Why logistic regression over TF-IDF:**
- Produces well-calibrated probability scores (not over-inflated binary regex hits)
- Interpretable coefficients — auditable under DGAF governance requirements
- Low compute overhead — consistent with KAPPA's latency SLA
- `class_weight='balanced'` handles moderate class imbalance in governance_clear category
- Probability outputs map cleanly to the new confidence band structure

### 3.2 Governance-Specific Confidence Band Split (Secondary Fix)

Add a dedicated governance confidence sub-band to resolve the collision:

```
v3.6 confidence bands:
  governance_strong:   p_governance_clear ≥ 0.45 AND intent = directive
  governance_blended:  p_governance_clear 0.25–0.45 OR intent = discretionary  ← NEW
  apply_strong:        score ≥ 0.28 (non-governance)
  apply_blended:       score 0.15–0.28 (non-governance)
  apply_light:         score < 0.15
```

**Routing logic change:**
```
IF category == governance_clear:
    IF p_governance_clear ≥ 0.45 AND intent_flag == 'directive':
        route → governance_strong
    ELSE:
        route → governance_blended   # was incorrectly routing to apply_strong
ELSE:
    use existing v3.5 band logic
```

### 3.3 Intent Flag Detection

Add lightweight intent classifier to distinguish `directive` vs `discretionary` governance inputs:

| Intent | Signal Words | Routing |
|--------|-------------|--------|
| directive | "must", "shall", "required", "mandatory", "enforce" | governance_strong |
| discretionary | "should", "consider", "recommended", "may", "if appropriate" | governance_blended |
| ambiguous | no clear signal | governance_blended (safe default) |

---

## 4. Validation Plan: 100-Pass Calibration

### 4.1 Test Suite Design

```
Total: 100 pass stochastic validation
Category distribution (matching v3.5 baseline):
  governance_clear:  ~23 items (target: ≥95% = ≥22/23)
  adversarial:       ~20 items (maintain: 100%)
  ambiguous:         ~19 items (maintain: ≥90%)
  creative_clear:    ~20 items (maintain: ≥90%)
  unclear:           ~18 items (maintain: 100%)
```

### 4.2 governance_clear Sub-Category Breakdown

```
governance_clear test items:
  directive (high confidence):     8 items — must route to governance_strong
  discretionary (moderate conf.):  10 items — must route to governance_blended (was failing)
  ambiguous governance:            5 items — must route to governance_blended (safe default)

Pass condition: ≥22/23 correct (≥95.6%)
```

### 4.3 Regression Guard

All v3.5 passing categories must maintain or improve:
- adversarial: 100% (hard floor — any regression = BLOCK)
- unclear: 100% (hard floor — any regression = BLOCK)  
- ambiguous: ≥90%
- creative_clear: ≥90%

---

## 5. Component Card Update Plan

Upon passing 100-pass validation:
- [ ] Create `components/KAPPA/DGAF_GATE_KAPPA_v3_6_component_card.json`
- [ ] Update version field: `3.5` → `3.6`
- [ ] Update `governance_clear_accuracy`: `0.826` → measured result
- [ ] Update `classifier_type`: `regex_only` → `logistic_regression_tfidf`
- [ ] Add `confidence_bands` section with new governance sub-bands
- [ ] Add `intent_classifier` section
- [ ] Archive v3.5 component card (do not delete)

---

## 6. Best Practices & Governance Constraints

### NDR Pattern: Adaptive Weighting with Confidence Gates
- Each confidence band transition is an explicit governance gate
- No routing decision is made without a calibrated probability score
- Governance_clear band split is the minimal change required — no other bands modified

### AXIS Constraints
- ✅ No S-Tier / Gold Star claim until Apogee Lens validation of v3.6 component card
- ✅ v3.5 archived, not deleted — full audit trail maintained
- ✅ All classifier weights must be reproducible (random_state=42)
- ✅ Axiom 1 Guard: any v3.6 component card change requires Amethyst sign-off

### COLLEEN Routing (Post-Validation)
- Update ENSEMBLE_ROSTER.md with KAPPA v3.6 entry
- Route validation report to `AI_Governance&_Ethics` label
- Update CHANGELOG.md: add v3.6 entry under Unreleased

### DemiJoule Safety Check (Pre-Merge)
- [ ] Confirm no unsafe routing states reachable in v3.6 band logic
- [ ] Confirm regression guard holds (adversarial + unclear = 100% maintained)
- [ ] Confirm no PII in training data or test suite

---

## 7. Open Questions

1. **Training data source**: What labeled dataset will be used for the logistic regression? Options: (a) manually labeled from existing test suite, (b) synthetic generation under DGAF constraints, (c) bootstrap from v3.5 false positive analysis.
2. **λ coefficient for regularization**: C=1.0 is the default — should this be tuned via cross-validation against the governance_clear sub-corpus?
3. **Intent classifier scope**: Should the directive/discretionary intent flag be a separate micro-model or integrated into the logistic regression features?
4. **Band threshold tuning**: Are 0.45 and 0.25 the right governance sub-band thresholds, or should these be calibrated empirically against the 100-pass suite?

---

*Design spec authored by Amethyst × COLLEEN | NDR Adaptive Weighting | DGAF-Framework Issue #5*
