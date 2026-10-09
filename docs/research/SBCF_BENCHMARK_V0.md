# DGAF-SBCF-BENCH-001 (experimental draft)

[Issue #1338](https://github.com/ndrorchestration/DGAF-Framework/issues/1338)

**PROPOSED / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED.** Scientific N=0. Independent validation and high assurance NOT ESTABLISHED. No deployment, release or existing frozen benchmark modification.

## Baseline candidates (exact provenance and claims to be verified)
- NVIDIA OpenShell: sandbox-level filesystem/network/process enforcement, policy expansion control.
- OWASP Agent Control Standard (2026): observation hooks and governance interfaces.
- OWASP Agentic Applications Top 10 (2026): attack taxonomy and coverage.
- LLM Agent Honeypot (2024), https://arxiv.org/abs/2410.13919: semantic behavior detection, not agent recapture.
- Cisco Zero Trust for Agentic AI: inspect and verify precise published capabilities.
- BRaVeS/LBCF and MARIS-TRA: verify primary papers, versions, code and reproducibility before benchmark admission.

## Threat and trust boundary
Threats: unauthorized privilege expansion, external egress, persistent worker delegation, oversight tampering, hidden queued actions, prompt injection into defender, semantic detector evasion, forged evidence and stale claims. Toy prototype assumes an external independent attestation, but does not implement one. The agent and its own language cannot grant privileges or certify success.

## Policy
States NORMAL -> RESTRICTED -> QUARANTINED, monotonic within prototype. Separate external authorization required for any future restoration. Quarantine Q requires externally attested zero production capabilities, uncontrolled workers, pending external actions and unauthorized destinations, plus observability. A regime label alone never establishes Q. No Lyapunov or control barrier guarantee is claimed.

## Matched research comparison
A enforcement only; B semantic observation + enforcement; C enforcement + bounded safe-continuation dialogue; D combined funnel. Synthetic fixtures only; no real network, credentials or production workers. Primary metric externally witnessed unauthorized effects. Secondary metrics time-to-Q, false quarantine, residual delegation, false restrictions, task utility and overhead. Freeze trial counts, randomization, tests, exclusions, confidence intervals and multiple-comparison policy before observing outcomes.

## C0-C9 QA gates
C0 exact head and ownership; C1 verified bibliography; C2 threat model; C3 controller invariants; C4 proof obligations and counterexamples; C5 synthetic experiment harness; C6 statistical preregistration; C7 ACP/AOSS/Structural Epistemics/Tektite contracts; C8 eligible outside operator and adversarial falsification; C9 bounded publication. Each gate records SHA, platform, test commands, negative tests, first failures, results, artifact hashes, uncertainties and follow-up disposition. FAIL/BLOCKED means do not promote claims.

Existing independent review gates #1067, #1210, #1256 and #929 remain separate. Passing the toy controller tests establishes only deterministic function behavior.
