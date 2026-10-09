# SBCF prior-art verification ledger — v0

Status: PARTIAL PRIMARY-SOURCE VERIFICATION / NO PERFORMANCE PARITY. Checkpoint C1 remains open.

## NVIDIA OpenShell (primary documentation)
- Sources: https://docs.nvidia.com/openshell/latest/sandboxes/policies and https://docs.nvidia.com/openshell/latest/reference/policy-schema
- Verified documentation: policy v1 specifies filesystem_policy, landlock, process, network_policies, network_middlewares. Filesystem, Landlock and process controls are fixed at creation; network policy and middleware can be updated at runtime. Enforcement is not merely agent-prompt instruction.
- Minimum comparable requirement: independently enforced default-deny resource policy, process/user boundary, network destinations, explicit update semantics, versioned policy and evidence of effective application.
- SBCF current result: FAIL / NOT IMPLEMENTED. The in-memory test gate is only an executable specification and must not be described as OpenShell-equivalent.
- Reproduction still needed: pinned exact OpenShell release, fixture environment, isolation bypass and update-race tests, artifact provenance and independent reviewer.

## Remaining literature candidates
OWASP ACS / Agentic Top 10: source version and publication provenance still require a method-level crosswalk. LLM Agent Honeypot: detection evidence, not containment validation. Cisco Zero Trust, BRaVeS/LBCF, MARIS-TRA: verify exact papers, release/accessibility and reproduced metrics before claiming baseline match.

## Negative QA gate
Do not promote a benchmark candidate on title/abstract similarity alone. Primary-source inspection without implementation reproduction is only source verification, not functional parity. C1 must include an explicit NOT ESTABLISHED mark for inaccessible references or impossible matched tests.
