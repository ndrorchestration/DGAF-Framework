from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZER = ROOT / "scripts" / "materialize_track_a_epoch_002_unblinded_input.py"
PROTOCOL = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
ALGORITHM = "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
SEEDS = range(20270201, 20270251)
TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
FAILURES = (0, 1, 2, 3, 4, 5, 6, 8, 10)


def canonical(value: Any) -> bytes:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return (text + "\n").encode()


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sidecar(name: str, value: bytes) -> bytes:
    return f"{digest(value)}  {name}\n".encode()


def flat_tar(path: Path, members: dict[str, bytes]) -> None:
    with tarfile.open(path, "w") as archive:
        for name, value in sorted(members.items()):
            info = tarfile.TarInfo(name)
            info.size = len(value)
            info.mode = 0o600
            info.mtime = 0
            archive.addfile(info, io.BytesIO(value))


class MaterializerPresenceTests(unittest.TestCase):
    def test_accepted_materializer_path_exists(self) -> None:
        self.assertTrue(MATERIALIZER.is_file(), "accepted Stage-1 materializer path is absent")


@unittest.skipUnless(MATERIALIZER.is_file(), "Stage-1 materializer not implemented yet")
class TrackAEpoch002MaterializerTests(unittest.TestCase):
    module: Any

    @classmethod
    def setUpClass(cls) -> None:
        if shutil.which("openssl") is None:
            raise unittest.SkipTest("OpenSSL is required")
        spec = importlib.util.spec_from_file_location("epoch002_materializer", MATERIALIZER)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot load materializer")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="epoch002-materializer-test-")
        self.root = Path(self.temp.name)
        self.fixture = self._fixture()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _fixture(self) -> dict[str, Any]:
        key = self.root / "key.pem"
        cert = self.root / "cert.pem"
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                str(key),
                "-out",
                str(cert),
                "-subj",
                "/CN=Epoch002 synthetic/",
                "-days",
                "1",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        cert_bytes = cert.read_bytes()
        public_pem = subprocess.check_output(
            ["openssl", "x509", "-in", str(cert), "-pubkey", "-noout"],
            stderr=subprocess.DEVNULL,
        )
        public_der = subprocess.check_output(
            ["openssl", "pkey", "-pubin", "-outform", "DER"],
            input=public_pem,
            stderr=subprocess.DEVNULL,
        )
        cert_public_sha = digest(public_der)
        frozen_sha = "7" * 40
        public_members: dict[str, bytes] = {}
        protected_members: dict[str, bytes] = {}
        rows: list[dict[str, Any]] = []

        for seed in SEEDS:
            mapping = {f"topology_{index:020x}": topology for index, topology in enumerate(TOPOLOGIES, 1)}
            records = []
            for blind_id, topology in mapping.items():
                topology_index = TOPOLOGIES.index(topology)
                for failure in FAILURES:
                    records.append(
                        {
                            "protocol_id": PROTOCOL,
                            "algorithm_id": ALGORITHM,
                            "frozen_candidate_sha": frozen_sha,
                            "seed_id": seed,
                            "blinded_topology_id": blind_id,
                            "failure_count": failure,
                            "ffcr_success": (seed + topology_index + failure) % 2 == 0,
                            "excluded": False,
                        }
                    )
            public_doc = {
                "record_type": "TRACK_A_EPOCH_002_BLINDED_SEED_DATASET",
                "schema_version": 1,
                "protocol_id": PROTOCOL,
                "seed_id": seed,
                "records": records,
                "environment_fingerprint": {"synthetic": True},
                "runtime_seconds": 0.01,
                "outcomes_inspected_by_collection_workflow": False,
                "unblinding_authorized": False,
                "primary_analysis_authorized": False,
            }
            mapping_doc = {
                "record_type": "TRACK_A_EPOCH_002_PROTECTED_TOPOLOGY_MAPPING",
                "schema_version": 1,
                "protocol_id": PROTOCOL,
                "seed_id": seed,
                "mapping": mapping,
                "custody": "PROTECTED_SAME_SYSTEM_NONINDEPENDENT",
                "custody_certificate_public_key_der_sha256": cert_public_sha,
                "public_dataset_contains_plaintext_topology": False,
                "public_dataset_contains_topology_fingerprint": False,
                "unblinding_authorized": False,
                "primary_analysis_authorized": False,
            }
            public_name = f"track_a_epoch_002_seed_{seed}.json"
            mapping_name = f"track_a_epoch_002_mapping_{seed}.json"
            public_bytes = canonical(public_doc)
            mapping_bytes = canonical(mapping_doc)
            public_members[public_name] = public_bytes
            public_members[public_name + ".sha256"] = sidecar(public_name, public_bytes)
            protected_members[mapping_name] = mapping_bytes
            protected_members[mapping_name + ".sha256"] = sidecar(mapping_name, mapping_bytes)
            rows.append(
                {
                    "seed_id": seed,
                    "public_dataset_sha256": digest(public_bytes),
                    "protected_mapping_sha256": digest(mapping_bytes),
                    "record_count": 45,
                }
            )

        custody_name = "track_a_epoch_002_blinding_key_custody.json"
        custody_bytes = canonical(
            {
                "record_type": "TRACK_A_EPOCH_002_PROTECTED_BLINDING_KEY_CUSTODY",
                "schema_version": 1,
                "protocol_id": PROTOCOL,
                "key_material_persisted": False,
                "key_fingerprint_sha256": "9" * 64,
                "custody": "SAME_SYSTEM_NONINDEPENDENT",
                "independent_custody": False,
                "custody_certificate_public_key_der_sha256": cert_public_sha,
                "unblinding_authorized": False,
                "primary_analysis_authorized": False,
            }
        )
        protected_members[custody_name] = custody_bytes
        protected_members[custody_name + ".sha256"] = sidecar(custody_name, custody_bytes)

        manifest_name = "track_a_epoch_002_manifest.json"
        manifest_bytes = canonical(
            {
                "record_type": "TRACK_A_EPOCH_002_BLINDED_COLLECTION_MANIFEST",
                "schema_version": 1,
                "protocol_id": PROTOCOL,
                "frozen_candidate_sha": frozen_sha,
                "seed_count": 50,
                "expected_observations": 2250,
                "custody_receipt_blob_sha": "8" * 40,
                "custody_certificate_sha256": digest(cert_bytes),
                "custody_certificate_public_key_der_sha256": cert_public_sha,
                "rows": rows,
                "outcomes_inspected_by_collection_workflow": False,
                "outcome_aggregation_performed": False,
                "unblinding_authorized": False,
                "primary_analysis_authorized": False,
                "historical_pooling_allowed": False,
                "epoch_004_substitution_allowed": False,
            }
        )
        public_members[manifest_name] = manifest_bytes
        public_members[manifest_name + ".sha256"] = sidecar(manifest_name, manifest_bytes)
        public_archive = self.root / "public.tar"
        flat_tar(public_archive, public_members)

        plaintext_tar = self.root / "protected-plaintext.tar"
        flat_tar(plaintext_tar, protected_members)
        plaintext_sha = digest(plaintext_tar.read_bytes())
        ciphertext = self.root / "protected.cms"
        subprocess.run(
            [
                "openssl",
                "cms",
                "-encrypt",
                "-binary",
                "-outform",
                "DER",
                "-in",
                str(plaintext_tar),
                "-out",
                str(ciphertext),
                str(cert),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        ciphertext_bytes = ciphertext.read_bytes()
        protected_archive = self.root / "protected.tar"
        flat_tar(
            protected_archive,
            {
                "track_a_epoch_002_custody_cert.pem": cert_bytes,
                "track_a_epoch_002_custody_cert.sha256": sidecar("track_a_epoch_002_custody_cert.pem", cert_bytes),
                "track_a_epoch_002_protected.cms": ciphertext_bytes,
                "track_a_epoch_002_protected_ciphertext.sha256": sidecar(
                    "track_a_epoch_002_protected.cms", ciphertext_bytes
                ),
                "track_a_epoch_002_protected_plaintext_tar.sha256": (
                    f"{plaintext_sha}  track_a_epoch_002_protected.tar\n".encode()
                ),
            },
        )

        receipt = {
            "record_type": "DATASET_LOCK_RECEIPT",
            "schema_version": 1,
            "protocol_id": PROTOCOL,
            "epoch": 2,
            "record_id": "E002-DATASET-LOCK-SYNTHETIC",
            "status": "PASS",
        }
        receipt_bytes = canonical(receipt)
        decision = {
            "record_type": "UNBLINDING_DECISION_RECORD",
            "schema_version": 1,
            "protocol_id": PROTOCOL,
            "epoch": 2,
            "record_id": "E002-UNBLINDING-SYNTHETIC",
            "evidence_scope": "CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY",
            "predecessor_record_ids": [receipt["record_id"]],
            "immutable_subject": {"sha256": digest(receipt_bytes)},
            "status": "PASS",
        }
        evidence = {
            "record_type": "TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE",
            "schema_version": 1,
            "protocol_id": PROTOCOL,
            "epoch": 2,
            "frozen_candidate_sha": frozen_sha,
            "paired_seed_units": 50,
            "blinded_observations": 2250,
            "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
            "independent_custody": False,
            "custody_receipt_blob_sha": "8" * 40,
            "public_artifact": {
                "name": "track-a-epoch-002-public-blinded",
                "size_bytes": public_archive.stat().st_size,
                "archive_sha256": digest(public_archive.read_bytes()),
                "manifest_sha256": digest(manifest_bytes),
            },
            "protected_artifact": {
                "name": "track-a-epoch-002-protected-encrypted",
                "size_bytes": protected_archive.stat().st_size,
                "archive_sha256": digest(protected_archive.read_bytes()),
                "ciphertext_sha256": digest(ciphertext_bytes),
                "plaintext_tar_sha256": plaintext_sha,
                "custody_certificate_sha256": digest(cert_bytes),
                "custody_certificate_public_key_der_sha256": cert_public_sha,
            },
        }
        return {
            "public_archive": public_archive,
            "protected_archive": protected_archive,
            "private_key": key,
            "contracts": {
                "dataset_lock_evidence": evidence,
                "dataset_lock_receipt": receipt,
                "dataset_lock_receipt_sha256": digest(receipt_bytes),
                "unblinding_decision": decision,
                "unblinding_decision_sha256": digest(canonical(decision)),
            },
        }

    def _run(
        self,
        output_dir: Path,
        *,
        key: Path | None = None,
        contracts: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.module.materialize(
            self.fixture["public_archive"],
            self.fixture["protected_archive"],
            key or self.fixture["private_key"],
            output_dir,
            contracts=contracts or self.fixture["contracts"],
        )

    def test_synthetic_materialization_is_deterministic_and_nonanalytical(self) -> None:
        first = self.root / "out-a"
        second = self.root / "out-b"
        result_a = self._run(first)
        result_b = self._run(second)
        self.assertEqual(result_a["materialized_input_sha256"], result_b["materialized_input_sha256"])
        output = json.loads((first / self.module.OUTPUT_NAME).read_text())
        self.assertEqual(output["record_type"], "TRACK_A_EPOCH_002_UNBLINDED_ANALYSIS_INPUT")
        self.assertEqual((output["paired_seed_units"], output["record_count"]), (50, 2250))
        self.assertEqual(len(output["records"]), 2250)
        self.assertFalse(output["primary_analysis_authorized"])
        self.assertFalse(output["primary_analysis_run"])
        self.assertFalse(output["outcome_aggregation_performed"])
        self.assertEqual(output["scientific_n_increment"], 0)
        self.assertEqual(output["canonical_dgaf_efficacy"], "NOT_ESTABLISHED")

    def test_wrong_key_and_archive_drift_fail_closed(self) -> None:
        wrong_key = self.root / "wrong.pem"
        subprocess.run(
            ["openssl", "genpkey", "-algorithm", "RSA", "-out", str(wrong_key)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        with self.assertRaises(SystemExit):
            self._run(self.root / "wrong-key", key=wrong_key)

        contracts = json.loads(json.dumps(self.fixture["contracts"]))
        contracts["dataset_lock_evidence"]["public_artifact"]["archive_sha256"] = "0" * 64
        with self.assertRaises(SystemExit):
            self._run(self.root / "drift", contracts=contracts)

    def test_tar_reader_rejects_traversal_and_links(self) -> None:
        traversal = self.root / "traversal.tar"
        with tarfile.open(traversal, "w") as archive:
            info = tarfile.TarInfo("../escape")
            info.size = 1
            archive.addfile(info, io.BytesIO(b"x"))
        with self.assertRaises(SystemExit):
            self.module.read_exact_tar_members(traversal, frozenset({"safe"}), "synthetic")

        linked = self.root / "link.tar"
        with tarfile.open(linked, "w") as archive:
            info = tarfile.TarInfo("safe")
            info.type = tarfile.SYMTYPE
            info.linkname = "elsewhere"
            archive.addfile(info)
        with self.assertRaises(SystemExit):
            self.module.read_exact_tar_members(linked, frozenset({"safe"}), "synthetic")

    def test_duplicate_tar_members_are_rejected(self) -> None:
        archive_path = self.root / "duplicate.tar"
        with tarfile.open(archive_path, "w") as archive:
            for value in (b"first", b"second"):
                info = tarfile.TarInfo("safe")
                info.size = len(value)
                archive.addfile(info, io.BytesIO(value))
        with self.assertRaises(SystemExit):
            self.module.read_exact_tar_members(archive_path, frozenset({"safe"}), "synthetic")

    def test_existing_output_is_preserved(self) -> None:
        output_dir = self.root / "existing"
        output_dir.mkdir()
        destination = output_dir / self.module.OUTPUT_NAME
        destination.write_bytes(b"previous result")
        with self.assertRaises(SystemExit):
            self._run(output_dir)
        self.assertEqual(destination.read_bytes(), b"previous result")

    def test_source_preserves_nonanalysis_and_secret_boundary(self) -> None:
        text = MATERIALIZER.read_text()
        self.assertNotIn("track_a_epoch_002_analysis", text)
        self.assertNotIn("--passphrase", text)
        self.assertNotIn("--private-key-passphrase", text)
        self.assertIn("--custody-private-key", text)
        self.assertIn("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN", text)


if __name__ == "__main__":
    unittest.main()
