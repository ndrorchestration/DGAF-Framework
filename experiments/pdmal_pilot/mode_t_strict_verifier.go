// Command mode_t_strict_verifier performs post-release P4-B continuity verification
// for one tlock ciphertext. It never writes decrypted plaintext to disk or stdout.
//
// Scientific state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"

	"github.com/drand/tlock"
	drandhttp "github.com/drand/tlock/networks/http"
)

const (
	tlockVersion      = "v1.2.0"
	tlockSourceCommit = "7b54141a9733fd6fa207587a11148280e6fb020d"
	quicknetChainHash = "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"
	quicknetScheme    = "bls-unchained-g1-rfc9380"
	quicknetPublicKey = "83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c8c4b450b6a0a6c3ac6a5776a2d1064510d1fec758c921cc22b0e17e63aaf4bcb5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a"
)

var (
	sha40RE = regexp.MustCompile(`^[0-9a-f]{40}$`)
	sha64RE = regexp.MustCompile(`^[0-9a-f]{64}$`)
)

type continuityReport struct {
	SchemaVersion                int    `json:"schema_version"`
	EvidenceClass                string `json:"evidence_class"`
	Status                       string `json:"status"`
	ControlPlaneSHA              string `json:"control_plane_sha"`
	GitHubRunID                  string `json:"github_run_id"`
	GitHubRunAttempt             string `json:"github_run_attempt"`
	TlockVersion                 string `json:"tlock_version"`
	TlockSourceCommit            string `json:"tlock_source_commit"`
	NetworkEndpoint              string `json:"network_endpoint"`
	ChainHash                    string `json:"chain_hash"`
	Scheme                       string `json:"scheme"`
	PublicKeyVerified            bool   `json:"public_key_verified"`
	NetworkMetadataVerified      bool   `json:"network_metadata_verified"`
	StrictChainEnforced          bool   `json:"strict_chain_enforced"`
	CiphertextSHA256             string `json:"ciphertext_sha256"`
	ExpectedPlaintextSHA256      string `json:"expected_plaintext_sha256"`
	PlaintextCommitmentMatch     bool   `json:"plaintext_commitment_match"`
	PlaintextPersisted           bool   `json:"plaintext_persisted"`
	PlaintextEmitted             bool   `json:"plaintext_emitted"`
	EmpiricalDataCollection      bool   `json:"empirical_data_collection"`
	FreezeEstablished            bool   `json:"freeze_established"`
	PilotAuthorized              bool   `json:"pilot_authorized"`
	EmpiricalN                   int    `json:"empirical_n"`
}

type failureReport struct {
	SchemaVersion   int    `json:"schema_version"`
	EvidenceClass   string `json:"evidence_class"`
	Status          string `json:"status"`
	Classification  string `json:"classification"`
	ControlPlaneSHA string `json:"control_plane_sha,omitempty"`
	GitHubRunID     string `json:"github_run_id,omitempty"`
	GitHubRunAttempt string `json:"github_run_attempt,omitempty"`
	EmpiricalN      int    `json:"empirical_n"`
}

func sha256Hex(data []byte) string {
	sum := sha256.Sum256(data)
	return hex.EncodeToString(sum[:])
}

func normalizePublicKey(rendered string) string {
	const prefix = "bls12-381.G2: "
	return strings.TrimPrefix(strings.TrimSpace(rendered), prefix)
}

func validateRunIdentity(evidenceSHA, runID, runAttempt string) error {
	if !sha40RE.MatchString(evidenceSHA) {
		return errors.New("invalid evidence SHA")
	}
	id, err := strconv.ParseUint(runID, 10, 64)
	if err != nil || id == 0 {
		return errors.New("invalid run ID")
	}
	attempt, err := strconv.ParseUint(runAttempt, 10, 64)
	if err != nil || attempt == 0 {
		return errors.New("invalid run attempt")
	}
	return nil
}

func validateExpectedCommitment(value string) error {
	if !sha64RE.MatchString(value) {
		return errors.New("expected plaintext commitment must be lowercase SHA-256")
	}
	return nil
}

func validateNetworkMetadata(network tlock.Network) error {
	if network.ChainHash() != quicknetChainHash {
		return errors.New("network chain hash mismatch")
	}
	if network.Scheme().String() != quicknetScheme {
		return errors.New("network scheme mismatch")
	}
	publicKey := network.PublicKey()
	if publicKey == nil || normalizePublicKey(publicKey.String()) != quicknetPublicKey {
		return errors.New("network public key mismatch")
	}
	return nil
}

func classifyDecryptError(err error) string {
	switch {
	case errors.Is(err, tlock.ErrWrongChainhash):
		return "WRONG_CHAINHASH"
	case errors.Is(err, tlock.ErrTooEarly):
		return "TOO_EARLY"
	default:
		return "DECRYPT_FAILED"
	}
}

func zeroBytes(data []byte) {
	for i := range data {
		data[i] = 0
	}
}

func verifyCiphertext(network tlock.Network, ciphertext []byte, expectedPlaintextSHA256 string) (continuityReport, error) {
	if len(ciphertext) == 0 {
		return continuityReport{}, errors.New("empty ciphertext")
	}
	if err := validateExpectedCommitment(expectedPlaintextSHA256); err != nil {
		return continuityReport{}, err
	}
	if err := validateNetworkMetadata(network); err != nil {
		return continuityReport{}, err
	}

	var plaintext bytes.Buffer
	err := tlock.New(network).Strict().Decrypt(&plaintext, bytes.NewReader(ciphertext))
	if err != nil {
		return continuityReport{}, fmt.Errorf("%s", classifyDecryptError(err))
	}

	plainBytes := plaintext.Bytes()
	actualPlaintextSHA256 := sha256Hex(plainBytes)
	match := actualPlaintextSHA256 == expectedPlaintextSHA256
	zeroBytes(plainBytes)
	plaintext.Reset()
	if !match {
		return continuityReport{}, errors.New("PLAINTEXT_COMMITMENT_MISMATCH")
	}

	return continuityReport{
		SchemaVersion:            1,
		EvidenceClass:            "P4_B_MODE_T_STRICT_CONTINUITY_V1",
		Status:                   "PASS",
		TlockVersion:             tlockVersion,
		TlockSourceCommit:        tlockSourceCommit,
		ChainHash:                quicknetChainHash,
		Scheme:                   quicknetScheme,
		PublicKeyVerified:        true,
		NetworkMetadataVerified:  true,
		StrictChainEnforced:      true,
		CiphertextSHA256:         sha256Hex(ciphertext),
		ExpectedPlaintextSHA256:  expectedPlaintextSHA256,
		PlaintextCommitmentMatch: true,
		PlaintextPersisted:       false,
		PlaintextEmitted:         false,
		EmpiricalDataCollection:  false,
		FreezeEstablished:        false,
		PilotAuthorized:          false,
		EmpiricalN:               0,
	}, nil
}

func emitFailure(classification, evidenceSHA, runID, runAttempt string) {
	_ = json.NewEncoder(os.Stderr).Encode(failureReport{
		SchemaVersion:    1,
		EvidenceClass:    "P4_B_MODE_T_STRICT_CONTINUITY_V1",
		Status:           "FAIL",
		Classification:   classification,
		ControlPlaneSHA:  evidenceSHA,
		GitHubRunID:      runID,
		GitHubRunAttempt: runAttempt,
		EmpiricalN:       0,
	})
}

func main() {
	endpoint := flag.String("endpoint", "", "explicit drand HTTP endpoint")
	ciphertextPath := flag.String("ciphertext", "", "path to released tlock ciphertext")
	expectedPlaintextSHA256 := flag.String("expected-plaintext-sha256", "", "precommitted expected plaintext SHA-256")
	evidenceSHA := flag.String("evidence-sha", "", "exact DGAF repository SHA")
	runID := flag.String("run-id", "", "verification run ID")
	runAttempt := flag.String("run-attempt", "", "verification run attempt")
	flag.Parse()

	if *endpoint == "" || *ciphertextPath == "" {
		emitFailure("INVALID_ARGUMENTS", *evidenceSHA, *runID, *runAttempt)
		os.Exit(2)
	}
	if err := validateRunIdentity(*evidenceSHA, *runID, *runAttempt); err != nil {
		emitFailure("INVALID_RUN_IDENTITY", *evidenceSHA, *runID, *runAttempt)
		os.Exit(2)
	}
	if err := validateExpectedCommitment(*expectedPlaintextSHA256); err != nil {
		emitFailure("INVALID_EXPECTED_COMMITMENT", *evidenceSHA, *runID, *runAttempt)
		os.Exit(2)
	}

	ciphertext, err := os.ReadFile(*ciphertextPath)
	if err != nil {
		emitFailure("CIPHERTEXT_READ_FAILED", *evidenceSHA, *runID, *runAttempt)
		os.Exit(2)
	}

	network, err := drandhttp.NewNetwork(*endpoint, quicknetChainHash)
	if err != nil {
		emitFailure("NETWORK_PREFLIGHT_FAILED", *evidenceSHA, *runID, *runAttempt)
		os.Exit(2)
	}

	report, err := verifyCiphertext(network, ciphertext, *expectedPlaintextSHA256)
	if err != nil {
		classification := err.Error()
		switch classification {
		case "WRONG_CHAINHASH", "TOO_EARLY", "DECRYPT_FAILED", "PLAINTEXT_COMMITMENT_MISMATCH":
		default:
			classification = "VERIFICATION_FAILED"
		}
		emitFailure(classification, *evidenceSHA, *runID, *runAttempt)
		os.Exit(2)
	}

	report.ControlPlaneSHA = *evidenceSHA
	report.GitHubRunID = *runID
	report.GitHubRunAttempt = *runAttempt
	report.NetworkEndpoint = *endpoint
	if err := json.NewEncoder(os.Stdout).Encode(report); err != nil {
		emitFailure("REPORT_ENCODING_FAILED", *evidenceSHA, *runID, *runAttempt)
		os.Exit(2)
	}
}
