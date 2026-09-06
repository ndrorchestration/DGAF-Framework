package main

import (
	"bytes"
	"errors"
	"strings"
	"testing"
	"time"

	"github.com/drand/drand/v2/crypto"
	"github.com/drand/kyber"
	"github.com/drand/tlock"
)

type mismatchNetwork struct {
	switched bool
}

func (n *mismatchNetwork) ChainHash() string { return quicknetChainHash }
func (n *mismatchNetwork) Current(time.Time) uint64 { return 0 }
func (n *mismatchNetwork) PublicKey() kyber.Point { return nil }
func (n *mismatchNetwork) Scheme() crypto.Scheme { return crypto.Scheme{} }
func (n *mismatchNetwork) Signature(uint64) ([]byte, error) { return nil, errors.New("signature must not be requested") }
func (n *mismatchNetwork) SwitchChainHash(string) error {
	n.switched = true
	return errors.New("strict verifier must not switch chain")
}

func TestValidateRunIdentity(t *testing.T) {
	if err := validateRunIdentity(strings.Repeat("a", 40), "123", "1"); err != nil {
		t.Fatalf("expected valid identity: %v", err)
	}
	for _, tc := range []struct {
		sha, run, attempt string
	}{
		{"abc", "123", "1"},
		{strings.Repeat("a", 40), "0", "1"},
		{strings.Repeat("a", 40), "123", "0"},
		{strings.Repeat("a", 40), "not-a-run", "1"},
	} {
		if err := validateRunIdentity(tc.sha, tc.run, tc.attempt); err == nil {
			t.Fatalf("expected identity rejection for %#v", tc)
		}
	}
}

func TestExpectedCommitmentMustBeLowercaseSHA256(t *testing.T) {
	if err := validateExpectedCommitment(strings.Repeat("b", 64)); err != nil {
		t.Fatalf("expected valid commitment: %v", err)
	}
	for _, bad := range []string{"", "abcd", strings.Repeat("B", 64), strings.Repeat("g", 64)} {
		if err := validateExpectedCommitment(bad); err == nil {
			t.Fatalf("expected commitment rejection: %q", bad)
		}
	}
}

func TestDecryptErrorClassification(t *testing.T) {
	if got := classifyDecryptError(tlock.ErrWrongChainhash); got != "WRONG_CHAINHASH" {
		t.Fatalf("wrong chain classification: %s", got)
	}
	if got := classifyDecryptError(errors.Join(errors.New("wrapped"), tlock.ErrTooEarly)); got != "TOO_EARLY" {
		t.Fatalf("too-early classification: %s", got)
	}
	if got := classifyDecryptError(errors.New("other")); got != "DECRYPT_FAILED" {
		t.Fatalf("generic classification: %s", got)
	}
}

func TestStrictDecryptRejectsCiphertextChainWithoutSwitching(t *testing.T) {
	// Public upstream tlock v1.2.0 fixture from TestDecryptText. Its ciphertext
	// is bound to mainnet fastnet, while this fake network is frozen quicknet.
	cipher := `-----BEGIN AGE ENCRYPTED FILE-----
YWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IHRsb2NrIDIgZGJkNTA2ZDZlZjc2ZTVm
Mzg2ZjQxYzY1MWRjYjgwOGM1YmNiZDc1NDcxY2M0ZWFmYTNmNGRmN2FkNGU0YzQ5
MwpzRXAvVVpBQXlDSjE1QUxDaUFnQ1E2cEd1elJXS0kzMkpsQnBxUFAzcHVvdWRT
a2w0OXJ0NC9rMmd0UHlVMTRxCkN3MERjVUJVUlloT2UrRjZsSE9lTFgwMkZNMjk3
UGpwNlBZL09WY3NoblhqMTVMbU9FeXV1MjlDcmJGQXU3SmgKcWxlbjFtaXBONWUz
eFpVQysxQWtjS1Z3SU9uRjJWaW8veUpkNEUyVHhQWQotLS0gN21xSHhranNqMEND
UG9qN2haU0FWdEpFK0pUZzUwWmVsVS9YRWdOaDRadwpeDBRfXZtLOC49GlI+Kozr
z6hgtLUPYvAimgekc+CeyJ8fb/0MVrpq/Ewnx1MpKig8nQ==
-----END AGE ENCRYPTED FILE-----`

	network := &mismatchNetwork{}
	var plaintext bytes.Buffer
	err := tlock.New(network).Strict().Decrypt(&plaintext, strings.NewReader(cipher))
	if !errors.Is(err, tlock.ErrWrongChainhash) {
		t.Fatalf("expected ErrWrongChainhash, got %v", err)
	}
	if network.switched {
		t.Fatal("strict decrypt attempted SwitchChainHash")
	}
	if plaintext.Len() != 0 {
		t.Fatal("wrong-chain failure emitted plaintext")
	}
}

func TestMalformedCiphertextFailsWithoutPlaintext(t *testing.T) {
	network := &mismatchNetwork{}
	var plaintext bytes.Buffer
	err := tlock.New(network).Strict().Decrypt(&plaintext, strings.NewReader("not a tlock ciphertext"))
	if err == nil {
		t.Fatal("expected malformed ciphertext failure")
	}
	if plaintext.Len() != 0 {
		t.Fatal("malformed ciphertext emitted plaintext")
	}
}

func TestQuicknetConstantsAreFrozen(t *testing.T) {
	if len(quicknetChainHash) != 64 || quicknetScheme != "bls-unchained-g1-rfc9380" {
		t.Fatal("quicknet identity drift")
	}
	if len(quicknetPublicKey) != 192 {
		t.Fatalf("unexpected quicknet public key length: %d", len(quicknetPublicKey))
	}
	if tlockSourceCommit != "7b54141a9733fd6fa207587a11148280e6fb020d" || tlockVersion != "v1.2.0" {
		t.Fatal("tlock identity drift")
	}
}
