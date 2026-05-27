"""
HeraldAgent — trace sink and audit fan-out for the PPTL orchestration stack.

Responsibilities:
  - Emit structured TraceEvent records for every governance event
  - Fan-out synchronously to all registered sinks
  - Maintain in-process event log + count index
  - Provide query interface (filter by event_type, task_id)
  - Export full session as pandas DataFrame

Sink contract: any object with .emit(event: dict) -> None
"""
from __future__ import annotations
import uuid, time, hashlib
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from typing import Any, Callable

import pandas as pd


class TraceEventType(str, Enum):
    TASK_START   = "task_start"
    TASK_END     = "task_end"
    LLM_CALL     = "llm_call"
    JUDGE_CALL   = "judge_call"
    RAG_CALL     = "rag_call"
    GATE         = "gate"
    ROUTE        = "route"
    INPUT_VETO   = "input_veto"
    OUTPUT_VETO  = "output_veto"
    HERALD_FLUSH = "herald_flush"


@dataclass
class TraceEvent:
    event_type: TraceEventType
    session_id: str
    task_id:    str      = ""
    agent:      str      = ""
    round_num:  int      = 0
    payload:    dict     = field(default_factory=dict)
    trace_id:   str      = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp:  float    = field(default_factory=time.time)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["event_type"] = self.event_type.value
        d["ts_iso"]     = time.strftime(
            "%Y-%m-%dT%H:%M:%S", time.gmtime(self.timestamp)
        ) + f".{int((self.timestamp % 1) * 1000):03d}Z"
        d.update(d.pop("payload", {}))
        return d


class HeraldAgent:
    """
    Trace sink aggregator. Register sinks via .register_sink().
    All emit() calls are synchronous and isolated — a broken sink
    logs the error but never blocks orchestration.
    """

    def __init__(self, session_id: str | None = None):
        self.session_id = session_id or f"sess_{int(time.time())}"
        self.sinks:  list[Any] = []
        self._log:   list[dict] = []
        self._counts: dict[TraceEventType, int] = {}

    def register_sink(self, sink: Any) -> None:
        self.sinks.append(sink)

    def _emit(self, event: TraceEvent) -> None:
        d = event.to_dict()
        self._log.append(d)
        self._counts[event.event_type] = self._counts.get(event.event_type, 0) + 1
        for sink in self.sinks:
            try:
                sink.emit(d)
            except Exception as exc:
                print(f"[Herald] sink {type(sink).__name__} error: {exc}")

    def task_start(self, task_id: str, prompt: str) -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.TASK_START, session_id=self.session_id,
            task_id=task_id,
            payload={"prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
                     "prompt_len": len(prompt)},
        ))

    def task_end(self, task_id: str, status: str, rounds: int,
                 output_len: int = 0) -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.TASK_END, session_id=self.session_id,
            task_id=task_id,
            payload={"status": status, "rounds": rounds, "output_len": output_len},
        ))

    def llm_call(self, agent: str, provider: str, prompt_hash: str,
                 response_len: int, elapsed_ms: float, round_num: int = 0) -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.LLM_CALL, session_id=self.session_id,
            agent=agent, round_num=round_num,
            payload={"provider": provider, "prompt_hash": prompt_hash,
                     "response_len": response_len, "elapsed_ms": elapsed_ms},
        ))

    def judge_call(self, system_key: str, provider: str, prompt_hash: str,
                   elapsed_ms: float, result_summary: dict) -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.JUDGE_CALL, session_id=self.session_id,
            agent="Sentinel",
            payload={"system_key": system_key, "provider": provider,
                     "prompt_hash": prompt_hash, "elapsed_ms": elapsed_ms,
                     "result_summary": result_summary},
        ))

    def rag_call(self, n_segments: int, max_hallu_risk: float, n_flagged: int,
                 citation_risk: bool, elapsed_ms: float) -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.RAG_CALL, session_id=self.session_id,
            agent="DemiJoule",
            payload={"n_segments": n_segments, "max_hallu_risk": max_hallu_risk,
                     "n_flagged": n_flagged, "citation_risk": citation_risk,
                     "elapsed_ms": elapsed_ms},
        ))

    def gate(self, gate_id: str, round_num: int, scores: dict,
             vetoed: bool, veto_reason: str = "") -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.GATE, session_id=self.session_id,
            agent=gate_id, round_num=round_num,
            payload={"scores": scores, "vetoed": vetoed, "veto_reason": veto_reason},
        ))

    def route(self, src: str, dst: str, edge_weight: float,
              round_num: int = 0, msg_hash: str = "") -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.ROUTE, session_id=self.session_id,
            agent=src, round_num=round_num,
            payload={"dst": dst, "edge_weight": edge_weight, "msg_hash": msg_hash},
        ))

    def input_veto(self, reason: str, signal: str = "") -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.INPUT_VETO, session_id=self.session_id,
            payload={"reason": reason, "signal": signal},
        ))

    def output_veto(self, gate_id: str, reason: str, scores: dict) -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.OUTPUT_VETO, session_id=self.session_id,
            agent=gate_id,
            payload={"reason": reason, "scores": scores},
        ))

    def query(self, event_type: str | None = None,
              task_id: str | None = None) -> list[dict]:
        results = self._log
        if event_type:
            results = [e for e in results
                       if e.get("event_type") == event_type
                       or e.get("event_type", "").endswith(event_type)]
        if task_id:
            results = [e for e in results if e.get("task_id") == task_id]
        return results

    def export_df(self) -> pd.DataFrame:
        return pd.DataFrame(self._log)

    def health(self) -> dict:
        sink_health = {}
        for s in self.sinks:
            if hasattr(s, "health"):
                sink_health[type(s).__name__.lower().replace("sink", "")] = s.health()
        return {
            "session_id":    self.session_id,
            "total_events":  len(self._log),
            "event_counts":  dict(self._counts),
            "sinks":         sink_health,
        }

    def close(self) -> None:
        self._emit(TraceEvent(
            event_type=TraceEventType.HERALD_FLUSH,
            session_id=self.session_id,
            task_id=self._log[-1].get("task_id", "") if self._log else "",
        ))
        for s in self.sinks:
            if hasattr(s, "close"):
                try: s.close()
                except Exception: pass
