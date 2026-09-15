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
PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
ALGORITHM_ID = "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
SEEDS = tuple(range(20270201, 20270251))
TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sidecar_bytes(name: str, payload: bytes) -> bytes:
    return f"{sha256_bytes(payload)}  {name}\n".encode("utf-8")


def write_flat_tar(path: Path, members: dict[str, bytes]) -> None:
    with tarfile.open(path, "w") as archive:
        for name in sorted(members):
            payload = members[name]
            info = tarfile.TarInfo(name)
            info.size = len(payload)
            info.mode = 0o600
            info.mtime = 0
            archive.addfile(info, io.BytesIO(payload))


def openssl(*args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.check_output(
        ["openssl", *args],
        input=input_bytes,
        stderr=subprocess.DEVNULL,
    )


class MaterializerPresenceTests(unittest.TestCase):
    def test_epoch_002_materializer_exists_at_accepted_path(self) -> None:
        self.assertTrue(
            MATERIALIZER.is_file(),
            "accepted Stage-1 materializer path is not implemented",
        )


@unittest.skipUnless(MATERIALIZER.is_file(), "Stage-1 materializer not implemented yet")
class TrackAEpoch002UnblindedMaterializerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if shutil.which("openssl") is None:
            raise unittest.SkipTest("OpenSSL is required for synthetic CMS tests")
        spec = importlib.util.spec_from_file_location("epoch002_materializer", MATERIALIZER)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot load materializer module")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="epoch002-materializer-test-")
        self.root = Path(self.temp.name)
        self.fixture = self._build_fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _build_fixture(self, root: Path) -> dict[str, Any]:
        private_key = root / "custody-key.pem"
        certificate = root / "custody-cert.pem"
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                str(private_key),
                "-out",
                str(certificate),
                "-subj",
                "/CN=DGAF Epoch 002 synthetic test/",
                "-days",
                "1",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        public_pem = openssl("x509", "-in", str(certificate), "-pubkey", "-noout")
        public_der = openssl("pkey", "-pubin", "-outform", "DER", input_bytes=public_pem)
        certificate_public_sha = sha256_bytes(public_der)
        certificate_bytes = certificate.read_bytes()
        certificate_sha = sha256_bytes(certificate_bytes)
        frozen_candidate_sha = "7" * 40

        public_members: dict[str, bytes] = {}
        protected_plain_members: dict[str, bytes] = {}
        manifest_rows: list[dict[str, Any]] = []

        for seed in SEEDS:
            mapping = {
                f"topology_{index:020x}": topology
                for index, topology in enumerate(TOPOLOGIES, start=1)
            }
            records = []
            for blind_id, topology in mapping.items():
                topology_index = TOPOLOGIES.index(topology)
                for failure_count in FAILURE_COUNTS:
                    records.append(
                        {
                            "protocol_id": PROTOCOL_ID,
                            "algorithm_id": ALGORITHM_ID,
                            "frozen_candidate_sha": frozen_candidate_sha,
                            "seed_id": seed,
                            "blinded_topology_id": blind_id,
                            "failure_count": failure_count,
                            "ffcr_success": (seed + topology_index + failure_count) % 2 == 0,
                            "excluded": False,
                        }
                    )
            public_doc = {
                "record_type": "TRACK_A_EPOCH_002_BLINDED_SEED_DATASET",
                "schema_version": 1,
                "protocol_id": PROTOCOL_ID,
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
                "protocol_id": PROTOCOL_ID,
                "seed_id": seed,
                "mapping": mapping,
                "custody": "PROTECTED_SAME_SYSTEM_NONINDEPENDENT",
                "custody_certificate_public_key_der_sha256": certificate_public_sha,
                "public_dataset_contains_plaintext_topology": False,
                "public_dataset_contains_topology_fingerprint": False,
                "unblinding_authorized": False,
                "primary_analysis_authorized": False,
            }
            public_name = f"track_a_epoch_002_seed_{seed}.json"
            mapping_name = f"track_a_epoch_002_mapping_{seed}.json"
            public_bytes = canonical_json_bytes(public_doc)
            mapping_bytes = canonical_json_bytes(mapping_doc)
            public_members[public_name] = public_bytes
            public_members[public_name + ".sha256"] = sidecar_bytes(public_name, public_bytes)
            protected_plain_members[mapping_name] = mapping_bytes
            protected_plain_members[mapping_name + ".sha256"] = sidecar_bytes(mapping_name, mapping_bytes)
            manifest_rows.append(
                {
                    "seed_id": seed,
                    "public_dataset_sha256": sha256_bytes(public_bytes),
                    "protected_mapping_sha256": sha256_bytes(mapping_bytes),
                    "record_count": 45,
                }
            )

        custody_doc = {
            "record_type": "TRACK_A_EPOCH_002_PROTECTED_BLINDING_KEY_CUSTODY",
            "schema_version": 1,
            "protocol_id": PROTOCOL_ID,
            "key_material_persisted": False,
            "key_fingerprint_sha256": "9" * 64,
            "custody": "SAME_SYSTEM_NONINDEPENDENT",
            "independent_custody": False,
            "custody_certificate_public_key_der_sha256": certificate_public_sha,
            "unblinding_authorized": False,
            "primary_analysis_authorized": False,
        }
        custody_name = "track_a_epoch_002_blinding_key_custody.json"
        custody_bytes = canonical_json_bytes(custody_doc)
        protected_plain_members[custody_name] = custody_bytes
        protected_plain_members[custody_name + ".sha256"] = sidecar_bytes(custody_name, custody_bytes)

        manifest = {
            "record_type": "TRACK_A_EPOCH_002_BLINDED_COLLECTION_MANIFEST",
            "schema_version": 1,
            "protocol_id": PROTOCOL_ID,
            "frozen_candidate_sha": frozen_candidate_sha,
            "seed_count": 50,
            "expected_observations": 2250,
            "custody_receipt_blob_sha": "8" * 40,
            "custody_certificate_sha256": certificate_sha,
            "custody_certificate_public_key_der_sha256": certificate_public_sha,
            "rows": manifest_rows,
            "outcomes_inspected_by_collection_workflow": False,
            "outcome_aggregation_performed": False,
            "unblinding_authorized": False,
            "primary_analysis_authorized": False,
            "historical_pooling_allowed": False,
            "epoch_004_substitution_allowed": False,
        }
        manifest_name = "track_a_epoch_002_manifest.json"
        manifest_bytes = canonical_json_bytes(manifest)
        public_members[manifest_name] = manifest_bytes
        public_members[manifest_name + ".sha256"] = sidecar_bytes(manifest_name, manifest_bytes)

        public_archive = root / "public.tar"
        write_flat_tar(public_archive, public_members)

        protected_plain_tar = root / "protected-plaintext.tar"
        write_flat_tar(protected_plain_tar, protected_plain_members)
        protected_plain_sha = sha256_bytes(protected_plain_tar.read_bytes())

        ciphertext = root / "track_a_epoch_002_protected.cms"
        subprocess.run(
            [
                "openssl",
                "cms",
                "-encrypt",
                "-binary",
                "-outform",
                "DER",
                "-in",
                str(protected_plain_tar),
                "-out",
                str(ciphertext),
                str(certificate),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        ciphertext_bytes = ciphertext.read_bytes()
        protected_members = {
            "track_a_epoch_002_custody_cert.pem": certificate_bytes,
            "track_a_epoch_002_custody_cert.sha256": sidecar_bytes(
                "track_a_epoch_002_custody_cert.pem",
                certificate_bytes,
            ),
            "track_a_epoch_002_protected.cms": ciphertext_bytes,
            "track_a_epoch_002_protected_ciphertext.sha256": sidecar_bytes(
                "track_a_epoch_002_protected.cms",
                ciphertext_bytes,
            ),
            "track_a_epoch_002_protected_plaintext_tar.sha256": (
                f"{protected_plain_sha}  track_a_epoch_002_protected.tar\n".encode("utf-8")
            ),
        }
        protected_archive = root / "protected.tar"
        write_flat_tar(protected_archive, protected_members)

        dataset_lock_receipt = {
            "record_type": "DATASET_LOCK_RECEIPT",
            "schema_version": 1,
            "protocol_id": PROTOCOL_ID,
            "epoch": 2,
            "record_id": "E002-DATASET-LOCK-SYNTHETIC",
            "status": "PASS",
        }
        dataset_lock_receipt_bytes = canonical_json_bytes(dataset_lock_receipt)
        unblinding_decision = {
            "record_type": "UNBLINDING_DECISION_RECORD",
            "schema_version": 1,
            "protocol_id": PROTOCOL_ID,
            "epoch": 2,
            "record_id": "E002-UNBLINDING-SYNTHETIC",
            "evidence_scope": "CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY",
            "predecessor_record_ids": [dataset_lock_receipt["record_id"]],
            "immutable_subject": {"sha256": sha256_bytes(dataset_lock_receipt_bytes)},
            "status": "PASS",
        }
        dataset_lock_evidence = {
            "record_type": "TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE",
            "schema_version": 1,
            "protocol_id": PROTOCOL_ID,
            "epoch": 2,
            "frozen_candidate_sha": frozen_candidate_sha,
            "paired_seed_units": 50,
            "blinded_observations": 2250,
            "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
            "independent_custody": False,
            "custody_receipt_blob_sha": "8" * 40,
            "public_artifact": {
                "name": "track-a-epoch-002-public-blinded",
                "size_bytes": public_archive.stat().st_size,
                "archive_sha256": sha256_bytes(public_archive.read_bytes()),
                "manifest_sha256": sha256_bytes(manifest_bytes),
            },
            "protected_artifact": {
                "name": "track-a-epoch-002-protected-encrypted",
                "size_bytes": protected_archive.stat().st_size,
                "archive_sha256": sha256_bytes(protected_archive.read_bytes()),
                "ciphertext_sha256": sha256_bytes(ciphertext_bytes),
                "plaintext_tar_sha256": protected_plain_sha,
                "custody_certificate_sha256": certificate_sha,
                "custody_certificate_public_key_der_sha256": certificate_public_sha,
            },
        }
        contracts = {
            "dataset_lock_evidence": dataset_lock_evidence,
            "dataset_lock_receipt": dataset_lock_receipt,
            "dataset_lock_receipt_sha256": sha256_bytes(dataset_lock_receipt_bytes),
            "unblinding_decision": unblinding_decision,
            "unblinding_decision_sha256": sha256_bytes(canonical_json_bytes(unblinding_decision)),
        }
        return {
            "public_archive": public_archive,
            "protected_archive": protected_archive,
            "private_key": private_key,
            "contracts": contracts,
        }

    def test_synthetic_materialization_is_deterministic_and_nonanalytical(self) -> None:
        first = self.root / "out-a"
        second = self.root / "out-b"
        result_a = self.module.materialize(
            self.fixture["public_archive"],
            self.fixture["protected_archive"],
            self.fixture["private_key"],
            first,
            contracts=self.fixture["contracts"],
        )
        result_b = self.module.materialize(
            self.fixture["public_archive"],
            self.fixture["protected_archive"],
            self.fixture["private_key"],
            second,
            contracts=self.fixture["contracts"],
        )
        self.assertEqual(result_a["materialized_input_sha256"], result_b["materialized_input_sha256"])
        output = json.loads((first / self.module.OUTPUT_NAME).read_text(encoding="utf-8"))
        self.assertEqual(output["record_type"], "TRACK_A_EPOCH_002_UNBLINDED_ANALYSIS_INPUT")
        self.assertEqual(output["paired_seed_units"], 50)
        self.assertEqual(output["record_count"], 2250)
        self.assertEqual(len(output["records"]), 2250)
        self.assertFalse(output["primary_analysis_authorized"])
        self.assertFalse(output["primary_analysis_run"])
        self.assertFalse(output["outcome_aggregation_performed"])
        self.assertEqual(output["scientific_n_increment"], 0)
        self.assertEqual(output["canonical_dgaf_efficacy"], "NOT_ESTABLISHED")

    def test_wrong_private_key_fails_closed_without_output(self) -> None:
        wrong_key = self.root / "wrong-key.pem"
        subprocess.run(
            ["openssl", "genpkey", "-algorithm", "RSA", "-out", str(wrong_key)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        output_dir = self.root / "wrong-key-output"
        with self.assertRaises(SystemExit):
            self.module.materialize(
                self.fixture["public_archive"],
                self.fixture["protected_archive"],
                wrong_key,
                output_dir,
                contracts=self.fixture["contracts"],
            )
        self.assertFalse((output_dir / self.module.OUTPUT_NAME).exists())

    def test_archive_identity_drift_fails_before_materialization(self) -> None:
        contracts = json.loads(json.dumps(self.fixture["contracts"]))
        contracts["dataset_lock_evidence"]["public_artifact"]["archive_sha256"] = "0" * 64
        output_dir = self.root / "bad-archive-output"
        with self.assertRaises(SystemExit):
            self.module.materialize(
                self.fixture["public_archive"],
                self.fixture["protected_archive"],
                self.fixture["private_key"],
                output_dir,
                contracts=contracts,
            )
        self.assertFalse((output_dir / self.module.OUTPUT_NAME).exists())

    def test_tar_reader_rejects_traversal_and_links(self) -> None:
        traversal = self.root / "traversal.tar"
        with tarfile.open(traversal, "w") as archive:
            payload = b"x"
            info = tarfile.TarInfo("../escape")
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
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

    def test_source_has_no_analysis_import_or_secret_argument(self) -> None:
        text = MATERIALIZER.read_text(encoding="utf-8")
        self.assertNotIn("track_a_epoch_002_analysis", text)
        self.assertNotIn("--passphrase", text)
        self.assertNotIn("--private-key-passphrase", text)
        self.assertIn("--custody-private-key", text)
        self.assertIn("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN", text)


if __name__ == "__main__":
    unittest.main()
