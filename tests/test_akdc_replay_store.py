"""Synthetic Gate-4 SQLite atomicity tests against pinned DGAF ingress code.

No live transports, authorization, production data, or scientific trials.
"""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime, timedelta, timezone
import multiprocessing
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest

from experiments.akdc.akdc_ingress_bridge import ProtocolObservation
from experiments.akdc.replay_store_research import (
    SQLiteResearchAdmissionStore,
    ReplayRefusal,
    AdmissionContractError,
)
from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)


def a2a(seq=1, state="TASK_STATE_WORKING", **fields):
    d = dict(
        protocol="a2a",
        version="1.0.1",
        provider_id="akdc-provider",
        runtime_id="akdc-run-01",
        source_id="akdc-source",
        event_id=f"akdc-event-{seq}",
        effect_id=f"akdc-effect-{seq}",
        observed_at="2026-10-26T12:00:00Z",
        payload={"task_id": "task-101", "context_id": "ctx-101", "sequence": seq, "state": state},
    )
    d.update(fields)
    return ProtocolObservation(**d)


def mcp(seq=1, **fields):
    d = dict(
        protocol="mcp",
        version="2026-07-28",
        provider_id="akdc-provider",
        runtime_id="akdc-run-01",
        source_id="akdc-mcp-source",
        event_id=f"akdc-mcp-event-{seq}",
        effect_id=f"akdc-mcp-effect-{seq}",
        observed_at="2026-10-26T12:00:00Z",
        payload={
            "method": "tools/call",
            "response": {
                "jsonrpc": "2.0",
                "id": seq,
                "result": {"resultType": "complete", "content": [], "isError": False},
            },
        },
    )
    d.update(fields)
    return ProtocolObservation(**d)


def process_worker(db_path, queue):
    try:
        store = SQLiteResearchAdmissionStore(db_path)
        result = store.admit(a2a(seq=1), validate_external_runtime_envelope, now=NOW)
        queue.put("accepted" if result["admitted"] else "validator-refused")
    except ReplayRefusal:
        queue.put("replay-refused")
    except Exception as exc:
        queue.put("ERROR:" + repr(exc))


def uncommitted_writer_crash(db_path):
    """Inject abrupt death inside a synthetic uncommitted SQL transaction."""
    conn = sqlite3.connect(db_path, timeout=10.0, isolation_level=None)
    conn.execute("BEGIN IMMEDIATE")
    conn.execute(
        "INSERT INTO akdc_event VALUES (?, ?, ?, ?, ?)",
        ("akdc-provider", "akdc-run-01", "akdc-event-1", "akdc-effect-1", "synthetic-digest"),
    )
    os._exit(29)


class DurableResearchGate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.temp.name) / "test-only-replay.sqlite")
        self.store = SQLiteResearchAdmissionStore(self.db)

    def tearDown(self):
        self.temp.cleanup()

    def admit(self, obj, store=None, now=NOW, validator=validate_external_runtime_envelope):
        return (store or self.store).admit(obj, validator, now=now)

    def test_one_record_admitted_only_as_non_authoritative(self):
        result = self.admit(a2a())
        self.assertTrue(result["admitted"])
        self.assertEqual(result["authority_status"], "PRESENTED_NOT_GRANTED")
        self.assertEqual(result["dgaf_verification_class"], "UNVERIFIED_EXTERNAL_ASSERTION")
        self.assertEqual(self.store.count_admitted(), 1)

    def test_reject_exact_replay_without_mutation(self):
        self.admit(a2a())
        with self.assertRaisesRegex(ReplayRefusal, "duplicate_event"):
            self.admit(a2a())
        self.assertEqual(self.store.count_admitted(), 1)

    def test_event_collision_rejected(self):
        self.admit(a2a())
        with self.assertRaisesRegex(ReplayRefusal, "event_collision"):
            self.admit(a2a(seq=2, event_id="akdc-event-1"))
        self.assertEqual(self.store.count_admitted(), 1)

    def test_effect_duplicate_different_event_rejected(self):
        self.admit(a2a())
        with self.assertRaisesRegex(ReplayRefusal, "duplicate_effect"):
            self.admit(a2a(seq=2, effect_id="akdc-effect-1"))
        self.assertEqual(self.store.count_admitted(), 1)

    def test_ordering_reversed_and_equal_sequence_rejected(self):
        self.admit(a2a(seq=4))
        with self.assertRaisesRegex(ReplayRefusal, "out_of_order_sequence"):
            self.admit(a2a(seq=2))
        with self.assertRaisesRegex(ReplayRefusal, "out_of_order_sequence"):
            self.admit(a2a(seq=4, event_id="new-event", effect_id="new-effect"))
        self.assertEqual(self.store.count_admitted(), 1)

    def test_context_rebinding_rejected(self):
        self.admit(a2a(seq=1))
        changed = a2a(seq=2)
        changed.payload["context_id"] = "ctx-999"
        with self.assertRaisesRegex(ReplayRefusal, "context_rebinding"):
            self.admit(changed)
        self.assertEqual(self.store.count_admitted(), 1)

    def test_task_after_terminal_is_rejected(self):
        self.admit(a2a(state="TASK_STATE_COMPLETED"))
        with self.assertRaisesRegex(ReplayRefusal, "terminal_task_transition"):
            self.admit(a2a(seq=2))

    def test_sequential_nonterminal_accepted(self):
        self.assertTrue(self.admit(a2a(seq=1))["admitted"])
        self.assertTrue(self.admit(a2a(seq=2, state="TASK_STATE_INPUT_REQUIRED"))["admitted"])
        self.assertTrue(self.admit(a2a(seq=3, state="TASK_STATE_COMPLETED"))["admitted"])
        self.assertEqual(self.store.count_admitted(), 3)

    def test_connection_restart_preserves_seen_ids(self):
        self.admit(a2a())
        resumed = SQLiteResearchAdmissionStore(self.db)
        with self.assertRaisesRegex(ReplayRefusal, "duplicate_event"):
            self.admit(a2a(), store=resumed)
        self.assertEqual(resumed.count_admitted(), 1)

    def test_stale_validator_failure_not_recorded(self):
        rejected = self.admit(a2a(), now=NOW + timedelta(hours=3))
        self.assertFalse(rejected["admitted"])
        self.assertEqual(self.store.count_admitted(), 0)
        self.assertTrue(self.admit(a2a())["admitted"])

    def test_validator_exception_rolls_back(self):
        def raises(*args, **kwargs):
            raise RuntimeError("simulated validator crash")

        with self.assertRaisesRegex(RuntimeError, "crash"):
            self.admit(a2a(), validator=raises)
        self.assertEqual(self.store.count_admitted(), 0)
        self.assertTrue(self.admit(a2a())["admitted"])

    def test_validator_forged_authorization_never_recorded(self):
        def forged(e, **kwargs):
            r = validate_external_runtime_envelope(e, **kwargs)
            r["authority_status"] = "DGAF_GRANTED"
            return r

        with self.assertRaises(AdmissionContractError):
            self.admit(a2a(), validator=forged)
        self.assertEqual(self.store.count_admitted(), 0)

    def test_validator_mutates_envelope_rolls_back(self):
        def alters(e, **kwargs):
            r = validate_external_runtime_envelope(e, **kwargs)
            e["identity"]["source_id"] = "tampered"
            return r

        with self.assertRaisesRegex(AdmissionContractError, "mutated"):
            self.admit(a2a(), validator=alters)
        self.assertEqual(self.store.count_admitted(), 0)

    def test_mcp_error_distinction_and_no_authority(self):
        self.assertTrue(self.admit(mcp(seq=1))["admitted"])
        err = mcp(seq=2)
        err.payload["response"]["result"]["isError"] = True
        self.assertTrue(self.admit(err)["admitted"])
        self.assertEqual(self.store.count_admitted(), 2)

    def test_identity_scoping_different_providers_not_a_trust_claim(self):
        self.admit(a2a())
        second = a2a(provider_id="other-provider")
        self.assertTrue(self.admit(second)["admitted"])
        self.assertEqual(self.store.count_admitted(), 2)

    def test_thread_race_only_one_commit(self):
        obs = a2a()

        def worker(_):
            try:
                r = SQLiteResearchAdmissionStore(self.db).admit(obs, validate_external_runtime_envelope, now=NOW)
                return "accepted" if r["admitted"] else "refused"
            except ReplayRefusal:
                return "replay"

        with ThreadPoolExecutor(max_workers=8) as ex:
            outcomes = list(ex.map(worker, range(8)))
        self.assertEqual(outcomes.count("accepted"), 1)
        self.assertEqual(outcomes.count("replay"), 7)
        self.assertEqual(self.store.count_admitted(), 1)

    def test_spawn_process_race_only_one_commit(self):
        ctx = multiprocessing.get_context("spawn")
        queue = ctx.Queue()
        processes = [ctx.Process(target=process_worker, args=(self.db, queue)) for _ in range(4)]
        for p in processes:
            p.start()
        for p in processes:
            p.join(12)
        if any(p.is_alive() for p in processes):
            for p in processes:
                if p.is_alive():
                    p.terminate()
            self.fail("spawn worker exceeded test timeout")
        outcomes = [queue.get(timeout=5) for _ in processes]
        self.assertEqual(outcomes.count("accepted"), 1, outcomes)
        self.assertEqual(outcomes.count("replay-refused"), 3, outcomes)
        self.assertEqual(self.store.count_admitted(), 1)

    def test_future_schema_version_refused_without_downgrade(self):
        with closing(sqlite3.connect(self.db)) as conn:
            conn.execute("PRAGMA user_version=999")
        with self.assertRaisesRegex(ValueError, "unsupported persistent replay schema"):
            SQLiteResearchAdmissionStore(self.db)
        with closing(sqlite3.connect(self.db)) as conn:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 999)

    def test_invalid_protocol_does_not_create_record(self):
        with self.assertRaises(ValueError):
            self.admit(a2a(version="0.1"))
        self.assertEqual(self.store.count_admitted(), 0)

    def test_sql_insert_fault_after_validation_rolls_back_all_records(self):
        # Fail after inserting the event but before saving its effect.
        with closing(sqlite3.connect(self.db)) as conn:
            conn.execute("""CREATE TRIGGER akdc_inject_effect_abort
                BEFORE INSERT ON akdc_effect
                BEGIN SELECT RAISE(ABORT, 'injected receipt failure'); END""")
        with self.assertRaisesRegex(sqlite3.IntegrityError, "injected receipt failure"):
            self.admit(a2a())
        self.assertEqual(self.store.count_admitted(), 0)
        with closing(sqlite3.connect(self.db)) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM akdc_effect").fetchone()[0], 0)
            conn.execute("DROP TRIGGER akdc_inject_effect_abort")
        self.assertTrue(self.admit(a2a())["admitted"])

    def test_uncommitted_writer_process_death_recovers_without_partial_receipt(self):
        ctx = multiprocessing.get_context("spawn")
        crashed = ctx.Process(target=uncommitted_writer_crash, args=(self.db,))
        crashed.start()
        crashed.join(10)
        if crashed.is_alive():
            crashed.terminate()
            crashed.join(5)
            self.fail("fault injection process never exited")
        self.assertEqual(crashed.exitcode, 29)
        self.assertEqual(self.store.count_admitted(), 0)
        self.assertTrue(self.admit(a2a())["admitted"])

    def test_separate_databases_do_not_share_replay_state_negative_control(self):
        self.assertTrue(self.admit(a2a())["admitted"])
        independent = SQLiteResearchAdmissionStore(Path(self.temp.name) / "separate.sqlite")
        self.assertTrue(self.admit(a2a(), store=independent)["admitted"])
        self.assertEqual(self.store.count_admitted(), 1)
        self.assertEqual(independent.count_admitted(), 1)

    def test_missing_effect_table_refuses_without_resetting_admitted_events(self):
        self.assertTrue(self.admit(a2a())["admitted"])
        with closing(sqlite3.connect(self.db)) as conn:
            conn.execute("DROP TABLE akdc_effect")
        with self.assertRaises(sqlite3.OperationalError):
            self.admit(a2a(seq=2))
        self.assertEqual(self.store.count_admitted(), 1)

    def test_restart_refuses_missing_table_on_existing_version(self):
        self.admit(a2a())
        with closing(sqlite3.connect(self.db)) as conn:
            conn.execute("DROP TABLE akdc_effect")
        with self.assertRaisesRegex(ValueError, "invalid replay schema"):
            SQLiteResearchAdmissionStore(self.db)

    def test_restart_refuses_weakened_effect_primary_key(self):
        self.admit(a2a())
        with closing(sqlite3.connect(self.db)) as conn:
            conn.execute("DROP TABLE akdc_effect")
            conn.execute(
                "CREATE TABLE akdc_effect ("
                "provider_id TEXT NOT NULL, runtime_id TEXT NOT NULL, "
                "effect_id TEXT NOT NULL, envelope_digest TEXT NOT NULL)"
            )
        with self.assertRaisesRegex(ValueError, "invalid replay schema"):
            SQLiteResearchAdmissionStore(self.db)

    def test_unversioned_partial_store_refused(self):
        with closing(sqlite3.connect(self.db)) as conn:
            conn.execute("PRAGMA user_version=0")
        with self.assertRaisesRegex(ValueError, "unversioned replay schema"):
            SQLiteResearchAdmissionStore(self.db)

    def test_runtime_rotation_is_not_bound_to_principal_negative_control(self):
        self.assertTrue(self.admit(a2a())["admitted"])
        # Same event+effect under a different unverified runtime id is accepted.
        # This intentionally proves the need for authenticated identity policy.
        self.assertTrue(self.admit(a2a(runtime_id="rotated-runtime-untrusted"))["admitted"])
        self.assertEqual(self.store.count_admitted(), 2)

    def test_record_is_only_receipt_not_execution(self):
        self.admit(a2a())
        with closing(sqlite3.connect(self.db)) as conn:
            names = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertEqual(names, {"akdc_event", "akdc_effect", "akdc_a2a_task"})


if __name__ == "__main__":
    unittest.main()
