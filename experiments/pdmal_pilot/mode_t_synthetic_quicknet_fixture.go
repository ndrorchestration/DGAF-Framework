// Command mode_t_synthetic_quicknet_fixture creates non-secret quicknet tlock
// fixtures for P4-B verifier behavior tests. It is test apparatus only.
package main

import (
	"bytes"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/drand/tlock"
	drandhttp "github.com/drand/tlock/networks/http"
)

const (
	quicknetChainHash = "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"
	quicknetScheme    = "bls-unchained-g1-rfc9380"
	quicknetPublicKey = "83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c8c4b450b6a0a6c3ac6a5776a2d1064510d1fec758c921cc22b0e17e63aaf4bcb5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a"
)

type fixtureManifest struct {
	SchemaVersion                 int    `json:"schema_version"`
	EvidenceClass                 string `json:"evidence_class"`
	Mode                          string `json:"mode"`
	NetworkEndpoint               string `json:"network_endpoint"`
	ChainHash                     string `json:"chain_hash"`
	Scheme                        string `json:"scheme"`
	PublicKeyVerified             bool   `json:"public_key_verified"`
	CurrentRoundAtCreation        uint64 `json:"current_round_at_creation"`
	TargetRound                   uint64 `json:"target_round"`
	TargetExpectedAvailable       bool   `json:"target_expected_available"`
	CiphertextSHA256              string `json:"ciphertext_sha256"`
	ExpectedPlaintextSHA256       string `json:"expected_plaintext_sha256"`
	SyntheticPlaintext            bool   `json:"synthetic_plaintext"`
	ProtectedMaterialPresent      bool   `json:"protected_material_present"`
	PlaintextCanaryLocalOnly      bool   `json:"plaintext_canary_local_only"`
	EmpiricalDataCollection       bool   `json:"empirical_data_collection"`
	FreezeEstablished             bool   `json:"freeze_established"`
	PilotAuthorized               bool   `json:"pilot_authorized"`
	EmpiricalN                    int    `json:"empirical_n"`
}

func sha256Hex(data []byte) string {
	sum := sha256.Sum256(data)
	return hex.EncodeToString(sum[:])
}

func normalizePublicKey(rendered string) string {
	const prefix = "bls12-381.G2: "
	return strings.TrimPrefix(strings.TrimSpace(rendered), prefix)
}

func validateQuicknet(network tlock.Network) error {
	if network.ChainHash() != quicknetChainHash {
		return errors.New("quicknet chain hash mismatch")
	}
	scheme := network.Scheme()
	if scheme.String() != quicknetScheme {
		return errors.New("quicknet scheme mismatch")
	}
	publicKey := network.PublicKey()
	if publicKey == nil || normalizePublicKey(publicKey.String()) != quicknetPublicKey {
		return errors.New("quicknet public key mismatch")
	}
	return nil
}

func zeroBytes(data []byte) {
	for i := range data {
		data[i] = 0
	}
}

func writeFile(path string, data []byte, mode os.FileMode) error {
	if path == "" {
		return errors.New("required output path is empty")
	}
	return os.WriteFile(path, data, mode)
}

func main() {
	endpoint := flag.String("endpoint", "", "explicit drand HTTP endpoint")
	fixtureMode := flag.String("mode", "", "available or future")
	ciphertextPath := flag.String("ciphertext", "", "ciphertext output path")
	commitmentPath := flag.String("commitment", "", "plaintext SHA-256 output path")
	canaryPath := flag.String("canary", "", "local-only synthetic plaintext canary path")
	manifestPath := flag.String("manifest", "", "non-secret manifest output path")
	flag.Parse()

	if *endpoint == "" || *ciphertextPath == "" || *commitmentPath == "" || *canaryPath == "" || *manifestPath == "" {
		fmt.Fprintln(os.Stderr, "invalid fixture arguments")
		os.Exit(2)
	}
	if *fixtureMode != "available" && *fixtureMode != "future" {
		fmt.Fprintln(os.Stderr, "fixture mode must be available or future")
		os.Exit(2)
	}

	network, err := drandhttp.NewNetwork(*endpoint, quicknetChainHash)
	if err != nil {
		fmt.Fprintln(os.Stderr, "quicknet metadata retrieval failed")
		os.Exit(2)
	}
	if err := validateQuicknet(network); err != nil {
		fmt.Fprintln(os.Stderr, "quicknet metadata validation failed")
		os.Exit(2)
	}

	currentRound := network.Current(time.Now())
	var targetRound uint64
	var expectedAvailable bool
	if *fixtureMode == "available" {
		targetRound = network.RoundNumber(time.Now().Add(-30 * time.Second))
		expectedAvailable = true
		if targetRound > currentRound {
			fmt.Fprintln(os.Stderr, "available fixture target is unexpectedly in the future")
			os.Exit(2)
		}
	} else {
		targetRound = network.RoundNumber(time.Now().Add(60 * time.Second))
		expectedAvailable = false
		if targetRound <= currentRound {
			fmt.Fprintln(os.Stderr, "future fixture target is not in the future")
			os.Exit(2)
		}
	}

	randomBytes := make([]byte, 32)
	if _, err := rand.Read(randomBytes); err != nil {
		fmt.Fprintln(os.Stderr, "synthetic random generation failed")
		os.Exit(2)
	}
	plaintext := []byte("DGAF-SYNTHETIC-P4B-" + hex.EncodeToString(randomBytes))
	zeroBytes(randomBytes)

	var cipher bytes.Buffer
	if err := tlock.New(network).Encrypt(&cipher, bytes.NewReader(plaintext), targetRound); err != nil {
		zeroBytes(plaintext)
		fmt.Fprintln(os.Stderr, "synthetic tlock encryption failed")
		os.Exit(2)
	}

	commitment := sha256Hex(plaintext)
	cipherBytes := cipher.Bytes()
	cipherDigest := sha256Hex(cipherBytes)

	// The canary exists only to prove verifier outputs/artifact candidates do not
	// contain the recovered plaintext. It is synthetic test data, never protected
	// DGAF material, and the workflow deletes it before artifact upload.
	if err := writeFile(*canaryPath, plaintext, 0o600); err != nil {
		zeroBytes(plaintext)
		fmt.Fprintln(os.Stderr, "writing local synthetic canary failed")
		os.Exit(2)
	}
	if err := writeFile(*ciphertextPath, cipherBytes, 0o600); err != nil {
		zeroBytes(plaintext)
		fmt.Fprintln(os.Stderr, "writing synthetic ciphertext failed")
		os.Exit(2)
	}
	if err := writeFile(*commitmentPath, []byte(commitment+"\n"), 0o644); err != nil {
		zeroBytes(plaintext)
		fmt.Fprintln(os.Stderr, "writing synthetic commitment failed")
		os.Exit(2)
	}

	manifest := fixtureManifest{
		SchemaVersion:            1,
		EvidenceClass:            "P4_B_MODE_T_SYNTHETIC_QUICKNET_FIXTURE_V1",
		Mode:                     *fixtureMode,
		NetworkEndpoint:          *endpoint,
		ChainHash:                quicknetChainHash,
		Scheme:                   quicknetScheme,
		PublicKeyVerified:        true,
		CurrentRoundAtCreation:   currentRound,
		TargetRound:              targetRound,
		TargetExpectedAvailable:  expectedAvailable,
		CiphertextSHA256:         cipherDigest,
		ExpectedPlaintextSHA256:  commitment,
		SyntheticPlaintext:       true,
		ProtectedMaterialPresent: false,
		PlaintextCanaryLocalOnly: true,
		EmpiricalDataCollection:  false,
		FreezeEstablished:        false,
		PilotAuthorized:          false,
		EmpiricalN:               0,
	}
	raw, err := json.MarshalIndent(manifest, "", "  ")
	if err != nil {
		zeroBytes(plaintext)
		fmt.Fprintln(os.Stderr, "encoding fixture manifest failed")
		os.Exit(2)
	}
	raw = append(raw, '\n')
	if err := writeFile(*manifestPath, raw, 0o644); err != nil {
		zeroBytes(plaintext)
		fmt.Fprintln(os.Stderr, "writing fixture manifest failed")
		os.Exit(2)
	}

	zeroBytes(plaintext)
}
