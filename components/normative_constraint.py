"""
DGAF Normative Constraint Module
components/normative_constraint.py

Implements the Normative Constraint (Ethical Cognition) formalism:
  - Deontic logic: permitted / obligated / forbidden / escalate
  - Optimization constraint: score ceiling under forbidden/escalate state
  - Epistemic integrity: intellectual honesty meta-constraint
  - Audit trace: every gate decision is logged

Reference: NDR Pattern P-10 | NIST AI RMF: Govern | EU AI Act: Art. 9, 13
Session: S035 | 2026-05-22
"""

from dataclasses import dataclass, field
from typing import Literal, Optional
from datetime import datetime, timezone

DeonticState = Literal["permitted", "obligated", "forbidden", "escalate"]

@dataclass
class NormativeConstraint:
    """
    Formal ethical boundary for a single evaluation record.
    Integrates deontic logic + optimization constraint + epistemic integrity.
    """
    record_id:       str
    category:        str
    confidence:      float
    content:         Optional[str] = None
    deontic_state:   DeonticState  = "permitted"
    reason:          str           = ""
    score_ceiling:   float         = 1.0
    epistemic_flag:  bool          = False
    audit_entry:     dict          = field(default_factory=dict)

    def evaluate(self) -> "NormativeConstraint":
        """Apply deontic rules and optimization constraints."""
        ts = datetime.now(timezone.utc).isoformat()

        if self.category == "adversarial" and self.confidence < 0.10:
            self.deontic_state  = "forbidden"
            self.reason         = "Adversarial input below detection floor"
            self.score_ceiling  = 0.0
            self.epistemic_flag = True

        elif self.category == "governance":
            self.deontic_state = "obligated"
            self.reason        = "Governance record: strong weights obligated"
            self.score_ceiling = 1.0

        elif self.category == "ambiguous" and self.confidence < 0.20:
            self.deontic_state = "escalate"
            self.reason        = "Ambiguous at low confidence: escalate to human review"
            self.score_ceiling = 0.5

        else:
            self.deontic_state = "permitted"
            self.reason        = "Within normative bounds"
            self.score_ceiling = 1.0

        if self.score_ceiling == 0.0 and not self.epistemic_flag:
            self.epistemic_flag = True
            self.reason += " | Epistemic: scoring suppressed for integrity"

        self.audit_entry = {
            "timestamp":      ts,
            "record_id":      self.record_id,
            "category":       self.category,
            "confidence":     round(self.confidence, 4),
            "deontic_state":  self.deontic_state,
            "reason":         self.reason,
            "score_ceiling":  self.score_ceiling,
            "epistemic_flag": self.epistemic_flag,
            "nist_rmf":       "Govern",
            "eu_ai_act":      "Art.9, Art.13",
            "pattern":        "P-10"
        }
        return self

    def apply_ceiling(self, raw_score: float) -> float:
        """Enforce optimization constraint: score cannot exceed ceiling."""
        return min(raw_score, self.score_ceiling)


def run_normative_pass(records: list) -> list:
    """
    Run NormativeConstraint evaluation across a batch.
    Returns list of NormativeConstraint objects with audit entries.
    Call before weight selection in the pipeline.
    """
    return [
        NormativeConstraint(
            record_id  = r.get("id", "unknown"),
            category   = r.get("category", "unknown"),
            confidence = r.get("confidence", 0.5),
            content    = r.get("content", "")
        ).evaluate()
        for r in records
    ]
