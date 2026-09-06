package main

import (
	"strings"
	"testing"
)

type wrongChainMetadataNetwork struct {
	mismatchNetwork
}

func (n *wrongChainMetadataNetwork) ChainHash() string {
	return strings.Repeat("0", 64)
}

func TestNetworkMetadataPreflightRejectsWrongFrozenChain(t *testing.T) {
	network := &wrongChainMetadataNetwork{}
	err := validateNetworkMetadata(network)
	if err == nil {
		t.Fatal("expected frozen-chain metadata preflight failure")
	}
	if err.Error() != "network chain hash mismatch" {
		t.Fatalf("unexpected preflight error: %v", err)
	}
	if network.switched {
		t.Fatal("metadata preflight must not switch chain identity")
	}
}
