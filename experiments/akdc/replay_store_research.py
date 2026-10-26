"""SQLite proof-of-concept for atomic admission-record deduplication.

RESEARCH ONLY. Not a production admission service, identity verifier, security
control, exactly-once executor, event bus, or substitute for DGAF CommitGate.
Uses file-backed SQLite locally; creates no network listeners. Never execute
an action from this store. Protocol identity fields are UNTRUSTED until separately
authenticated. One persistent store instance is required for all participants.
"""
from __future__ import annotations

from contextlib import closing
from datetime import datetime
from pathlib import Path
import sqlite3
from typing import Any, Callable

from experiments.akdc.akdc_ingress_bridge import (
    A2A_TERMINAL,
    ProtocolObservation,
    classify,
    content_digest,
    make_dgaf_envelope,
)


SCHEMA_VERSION = 1


class ReplayRefusal(ValueError):
    """A candidate observation violates a persistent ordering/dedup rule."""


class AdmissionContractError(RuntimeError):
    """The injected DGAF validator violated the pinned admission contract."""


class SQLiteResearchAdmissionStore:
    """A *local* transactional record-admission fixture, not an action gate.

    SQLite BEGIN IMMEDIATE ensures no two concurrent writers in this same DB
    pass the identity/ordering checks before either writes. This is not a claim
    about availability, authentication, distributed consensus, durability on
    all filesystems, external effects, or exactly-once delivery.
    """

    def __init__(self, path: str | Path):
        if str(path) == ':memory:':
            raise ValueError('research store requires a file path')
        self.path = str(path)
        with closing(self._connect()) as conn:
            version = conn.execute('PRAGMA user_version').fetchone()[0]
            if version not in (0, SCHEMA_VERSION):
                raise ValueError(f'unsupported persistent replay schema: {version}')
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS akdc_event (
                    provider_id TEXT NOT NULL,
                    runtime_id TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    effect_id TEXT NOT NULL,
                    envelope_digest TEXT NOT NULL,
                    PRIMARY KEY (provider_id, runtime_id, event_id)
                );
                CREATE TABLE IF NOT EXISTS akdc_effect (
                    provider_id TEXT NOT NULL,
                    runtime_id TEXT NOT NULL,
                    effect_id TEXT NOT NULL,
                    envelope_digest TEXT NOT NULL,
                    PRIMARY KEY (provider_id, runtime_id, effect_id)
                );
                CREATE TABLE IF NOT EXISTS akdc_a2a_task (
                    provider_id TEXT NOT NULL,
                    runtime_id TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    context_id TEXT NOT NULL,
                    last_sequence INTEGER NOT NULL,
                    last_state TEXT NOT NULL,
                    PRIMARY KEY (provider_id, runtime_id, source_id, task_id)
                );
            ''')
            if version == 0:
                conn.execute(f'PRAGMA user_version={SCHEMA_VERSION}')

    def _connect(self):
        conn = sqlite3.connect(self.path, timeout=15.0, isolation_level=None)
        conn.execute('PRAGMA busy_timeout=15000')
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA synchronous=FULL')
        return conn

    def count_admitted(self) -> int:
        with closing(self._connect()) as conn:
            return conn.execute('SELECT COUNT(*) FROM akdc_event').fetchone()[0]

    def admit(
        self,
        observation: ProtocolObservation,
        validator: Callable[..., dict[str, Any]],
        *,
        now: datetime,
    ) -> dict[str, Any]:
        """Admit one immutable record under one SQLite write transaction.

        Does NOT give permission to run tools or perform other side effects.
        All caller-visible refusal/exception paths roll back store mutations.
        """
        # Prevalidate outside transaction, but all replay/ordering checks and
        # state transitions are inside the same BEGIN IMMEDIATE critical region.
        classify(observation)
        envelope = make_dgaf_envelope(observation)
        digest = content_digest(envelope)
        p, r = observation.provider_id, observation.runtime_id
        e, fx = observation.event_id, observation.effect_id

        conn = self._connect()
        try:
            conn.execute('BEGIN IMMEDIATE')
            old_event = conn.execute(
                'SELECT envelope_digest FROM akdc_event WHERE provider_id=? AND runtime_id=? AND event_id=?',
                (p, r, e),
            ).fetchone()
            if old_event is not None:
                reason = 'duplicate_event' if old_event[0] == digest else 'event_collision'
                raise ReplayRefusal(reason)

            old_effect = conn.execute(
                'SELECT 1 FROM akdc_effect WHERE provider_id=? AND runtime_id=? AND effect_id=?',
                (p, r, fx),
            ).fetchone()
            if old_effect is not None:
                raise ReplayRefusal('duplicate_effect')

            if observation.protocol == 'a2a':
                task_id = observation.payload['task_id']
                context_id = observation.payload['context_id']
                seq = observation.payload['sequence']
                old_task = conn.execute(
                    'SELECT context_id, last_sequence, last_state FROM akdc_a2a_task '
                    'WHERE provider_id=? AND runtime_id=? AND source_id=? AND task_id=?',
                    (p, r, observation.source_id, task_id),
                ).fetchone()
                if old_task is not None:
                    if old_task[0] != context_id:
                        raise ReplayRefusal('context_rebinding')
                    if seq <= old_task[1]:
                        raise ReplayRefusal('out_of_order_sequence')
                    if old_task[2] in A2A_TERMINAL:
                        raise ReplayRefusal('terminal_task_transition')

            # The validator must be a side-effect-free ingress checker. It is
            # invoked while the write transaction is held; no tool execution.
            seen_events = dict(conn.execute(
                'SELECT event_id, envelope_digest FROM akdc_event '
                'WHERE provider_id=? AND runtime_id=?', (p, r)
            ).fetchall())
            seen_effects = {row[0] for row in conn.execute(
                'SELECT effect_id FROM akdc_effect '
                'WHERE provider_id=? AND runtime_id=?', (p, r)
            ).fetchall()}
            result = validator(envelope, seen_events=seen_events,
                               seen_effect_ids=seen_effects, now=now)
            if content_digest(envelope) != digest:
                raise AdmissionContractError('validator mutated the submitted record')
            if not isinstance(result, dict) or type(result.get('admitted')) is not bool:
                raise AdmissionContractError('validator response not a valid DGAF ingress result')
            if not result['admitted']:
                conn.execute('ROLLBACK')
                return result
            if (result.get('authority_status') != 'PRESENTED_NOT_GRANTED'
                    or result.get('dgaf_verification_class') != 'UNVERIFIED_EXTERNAL_ASSERTION'
                    or result.get('record_id') != digest
                    or result.get('effect_id') != fx
                    or result.get('requested_action_class') != 'NON_CONSEQUENTIAL_RECORD_INGRESS'
                    or result.get('requested_transition') != 'RECORD_ONLY'):
                raise AdmissionContractError('validator unexpectedly promoted/changed admission semantics')

            conn.execute('INSERT INTO akdc_event VALUES (?, ?, ?, ?, ?)', (p, r, e, fx, digest))
            conn.execute('INSERT INTO akdc_effect VALUES (?, ?, ?, ?)', (p, r, fx, digest))
            if observation.protocol == 'a2a':
                conn.execute('''INSERT INTO akdc_a2a_task VALUES (?, ?, ?, ?, ?, ?, ?)
                                ON CONFLICT(provider_id, runtime_id, source_id, task_id)
                                DO UPDATE SET context_id=excluded.context_id,
                                              last_sequence=excluded.last_sequence,
                                              last_state=excluded.last_state''',
                             (p, r, observation.source_id, observation.payload['task_id'],
                              observation.payload['context_id'], observation.payload['sequence'],
                              observation.payload['state']))
            conn.execute('COMMIT')
            return result
        except BaseException:
            if conn.in_transaction:
                conn.execute('ROLLBACK')
            raise
        finally:
            conn.close()