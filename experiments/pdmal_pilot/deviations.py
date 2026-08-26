"""Append-only protocol-deviation register for the PDMAL experiment."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path


@dataclass(frozen=True)
class Deviation:
    deviation_id: str
    timestamp: str
    seed_id: str | None
    trial_id: str | None
    condition: str | None
    cause: str
    description: str
    affected_metrics: tuple[str, ...]
    comparability_impact: str
    include_exclude_decision: str
    authorization: str


class DeviationRegister:
    def __init__(self) -> None:
        self._items: list[Deviation] = []
        self._ids: set[str] = set()

    def record(
        self,
        deviation_id: str,
        *,
        cause: str,
        description: str,
        seed_id: str | None = None,
        trial_id: str | None = None,
        condition: str | None = None,
        affected_metrics: tuple[str, ...] = (),
        comparability_impact: str = "none",
        include_exclude_decision: str = "pending",
        authorization: str = "unreviewed",
    ) -> Deviation:
        if not isinstance(deviation_id, str) or not deviation_id.strip():
            raise ValueError("deviation_id must be a non-empty string")
        if deviation_id in self._ids:
            raise ValueError(f"duplicate deviation_id: {deviation_id}")
        deviation = Deviation(
            deviation_id=deviation_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            seed_id=seed_id,
            trial_id=trial_id,
            condition=condition,
            cause=cause,
            description=description,
            affected_metrics=affected_metrics,
            comparability_impact=comparability_impact,
            include_exclude_decision=include_exclude_decision,
            authorization=authorization,
        )
        self._items.append(deviation)
        self._ids.add(deviation_id)
        return deviation

    def to_dicts(self) -> list[dict]:
        return [asdict(item) for item in self._items]

    def write_json(self, path: str | Path) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(self.to_dicts(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def __len__(self) -> int:
        return len(self._items)
