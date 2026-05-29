# resonant_decay/pdmal_monitor.py
# PDMAL Convergence Monitor
# Tracks row-stochastic graph reweight events; fires 3-turn divergence alert.
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time, hashlib


@dataclass
class PDMALEvent:
    turn:       int
    delta_norm: float   # Frobenius norm of row-weight shift
    alert:      str     # OK | DIVERGENCE_WARNING | DIVERGENCE_ALERT
    timestamp:  float   = field(default_factory=time.time)


class PDMALConvergenceMonitor:
    """Monitors row-stochastic PDMAL graph reweight convergence.

    divergence_threshold: per-turn Frobenius norm shift above which a turn
                          is counted as divergent.
    alert_window:         consecutive divergent turns before DIVERGENCE_ALERT
                          (default 3, matches design spec).
    """

    def __init__(self,
                 divergence_threshold: float = 0.05,
                 alert_window: int = 3):
        self.threshold    = divergence_threshold
        self.alert_window = alert_window
        self._weights:    Optional[List[float]] = None   # last known row weights
        self._consec_div: int = 0
        self.events:      List[PDMALEvent] = []
        self.turn_count:  int = 0

    # ── public API ────────────────────────────────────────────────────────
    def update(self, new_weights: List[float]) -> Dict[str, Any]:
        """Call each turn with the current PDMAL row-weight vector.
        Returns status dict and fires alert if warranted.
        """
        self.turn_count += 1
        n = len(new_weights)

        # Normalise to row-stochastic (sum=1)
        total = sum(new_weights) or 1.0
        w = [x / total for x in new_weights]

        if self._weights is None or len(self._weights) != n:
            # First update or topology change — baseline
            self._weights   = w
            self._consec_div = 0
            evt = PDMALEvent(self.turn_count, 0.0, "OK")
            self.events.append(evt)
            return self._result(evt, w)

        # Frobenius norm of weight shift
        delta = sum((a - b) ** 2 for a, b in zip(w, self._weights)) ** 0.5

        if delta > self.threshold:
            self._consec_div += 1
        else:
            self._consec_div = 0

        if self._consec_div >= self.alert_window:
            alert = "DIVERGENCE_ALERT"
        elif self._consec_div > 0:
            alert = "DIVERGENCE_WARNING"
        else:
            alert = "OK"

        self._weights = w
        evt = PDMALEvent(self.turn_count, round(delta, 6), alert)
        self.events.append(evt)
        return self._result(evt, w)

    def reset_baseline(self, weights: List[float]) -> None:
        """Force a new baseline (e.g. after RECIPROCITY arbitration)."""
        total = sum(weights) or 1.0
        self._weights    = [x / total for x in weights]
        self._consec_div = 0

    @property
    def is_alert(self) -> bool:
        return self._consec_div >= self.alert_window

    @property
    def summary(self) -> Dict[str, Any]:
        return {
            "turn_count":        self.turn_count,
            "consec_divergent":  self._consec_div,
            "alert":             "DIVERGENCE_ALERT" if self.is_alert else
                                 ("DIVERGENCE_WARNING" if self._consec_div > 0 else "OK"),
            "current_weights":   self._weights,
            "event_count":       len(self.events),
        }

    def _result(self, evt: PDMALEvent, weights: List[float]) -> Dict[str, Any]:
        return {
            "turn":        evt.turn,
            "delta_norm":  evt.delta_norm,
            "alert":       evt.alert,
            "consec_div":  self._consec_div,
            "weights":     weights,
        }
