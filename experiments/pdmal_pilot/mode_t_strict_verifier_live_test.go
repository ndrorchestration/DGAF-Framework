//go:build mode_t_live

package main

import (
	"bytes"
	"os"
	"testing"
	"time"

	"github.com/drand/tlock"
	drandhttp "github.com/drand/tlock/networks/http"
)

const defaultLiveQuicknetEndpoint = "https://api.drand.sh/"

func liveQuicknetEndpoint() string {
	if endpoint := os.Getenv("DGAF_QUICKNET_ENDPOINT"); endpoint != "" {
		return endpoint
	}
	return defaultLiveQuicknetEndpoint
}

func newLiveQuicknet(t *testing.T) tlock.Network {
	t.Helper()
	network, err := drandhttp.NewNetwork(liveQuicknetEndpoint(), quicknetChainHash)
	if err != nil {
		t.Fatalf("create frozen quicknet network: %v", err)
	}
	if err := validateNetworkMetadata(network); err != nil {
		t.Fatalf("validate frozen quicknet metadata: %v", err)
	}
	return network
}

func syntheticCiphertextForTime(t *testing.T, network tlock.Network, plaintext []byte, target time.Time) []byte {
	t.Helper()
	round := network.Current(target)
	if round == 0 {
		t.Fatal("derived zero drand round")
	}
	var ciphertext bytes.Buffer
	if err := tlock.New(network).Encrypt(&ciphertext, bytes.NewReader(plaintext), round); err != nil {
		t.Fatalf("encrypt synthetic fixture: %v", err)
	}
	return append([]byte(nil), ciphertext.Bytes()...)
}

func assertNoScientificPromotion(t *testing.T, report continuityReport) {
	t.Helper()
	if report.PlaintextPersisted || report.PlaintextEmitted || report.EmpiricalDataCollection || report.FreezeEstablished || report.PilotAuthorized || report.EmpiricalN != 0 {
		t.Fatal("synthetic live verification promoted forbidden state")
	}
}

func TestLiveQuicknetCorrectCommitmentPasses(t *testing.T) {
	network := newLiveQuicknet(t)
	plaintext := []byte("P4_B_SYNTHETIC_CONTINUITY_FIXTURE_V1")
	ciphertext := syntheticCiphertextForTime(t, network, plaintext, time.Now().Add(-45*time.Second))

	report, err := verifyCiphertext(network, ciphertext, sha256Hex(plaintext))
	if err != nil {
		t.Fatalf("strict correct-chain verification failed: %v", err)
	}
	if report.Status != "PASS" || !report.StrictChainEnforced || !report.NetworkMetadataVerified || !report.PlaintextCommitmentMatch {
		t.Fatalf("unexpected strict continuity report state: status=%q strict=%t metadata=%t commitment=%t", report.Status, report.StrictChainEnforced, report.NetworkMetadataVerified, report.PlaintextCommitmentMatch)
	}
	assertNoScientificPromotion(t, report)
}

func TestLiveQuicknetWrongCommitmentFailsClosed(t *testing.T) {
	network := newLiveQuicknet(t)
	plaintext := []byte("P4_B_SYNTHETIC_CONTINUITY_FIXTURE_V1")
	ciphertext := syntheticCiphertextForTime(t, network, plaintext, time.Now().Add(-45*time.Second))
	wrongCommitment := sha256Hex([]byte("P4_B_INTENTIONALLY_WRONG_SYNTHETIC_COMMITMENT"))

	_, err := verifyCiphertext(network, ciphertext, wrongCommitment)
	if err == nil || err.Error() != "PLAINTEXT_COMMITMENT_MISMATCH" {
		t.Fatalf("expected fail-closed commitment mismatch, got %v", err)
	}
}

func TestLiveQuicknetFutureRoundClassifiesTooEarly(t *testing.T) {
	network := newLiveQuicknet(t)
	plaintext := []byte("P4_B_SYNTHETIC_TOO_EARLY_FIXTURE_V1")
	ciphertext := syntheticCiphertextForTime(t, network, plaintext, time.Now().Add(2*time.Minute))

	_, err := verifyCiphertext(network, ciphertext, sha256Hex(plaintext))
	if err == nil || err.Error() != "TOO_EARLY" {
		t.Fatalf("expected explicit TOO_EARLY classification, got %v", err)
	}
}

func TestLiveQuicknetReplayDoesNotPromoteState(t *testing.T) {
	network := newLiveQuicknet(t)
	plaintext := []byte("P4_B_SYNTHETIC_REPLAY_FIXTURE_V1")
	ciphertext := syntheticCiphertextForTime(t, network, plaintext, time.Now().Add(-45*time.Second))
	commitment := sha256Hex(plaintext)

	first, err := verifyCiphertext(network, ciphertext, commitment)
	if err != nil {
		t.Fatalf("first strict replay verification failed: %v", err)
	}
	second, err := verifyCiphertext(network, ciphertext, commitment)
	if err != nil {
		t.Fatalf("second strict replay verification failed: %v", err)
	}
	assertNoScientificPromotion(t, first)
	assertNoScientificPromotion(t, second)
	if first.Status != "PASS" || second.Status != "PASS" || first.CiphertextSHA256 != second.CiphertextSHA256 || first.ExpectedPlaintextSHA256 != second.ExpectedPlaintextSHA256 {
		t.Fatal("replayed continuity verification changed accepted identity/state")
	}
}
