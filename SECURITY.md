# Security Policy

## Supported Versions

This repository contains governance specifications, evaluation rubrics, agent protocol documents, **and an executable Next.js application package** (see `package.json` for build/dev/start scripts). Security concerns include:

- Specification and governance-schema integrity
- Credential, token, key, or other secret exposure
- Application/runtime vulnerabilities in repository-owned code
- CI/CD and deployment-workflow vulnerabilities
- Dependency vulnerabilities that create an exploitable condition in this repository's application, build, or CI surface
- Misrepresentation or unauthorized use of DGAF certification/status claims

## Reporting a Vulnerability

To report a security concern with this repository or the broader DGAF ecosystem:

1. **Do not open a public GitHub issue** for security matters.
2. Contact the maintainer directly via GitHub: [@ndrorchestration](https://github.com/ndrorchestration)
3. Include:
   - Repository and file path affected
   - Nature of the concern
   - Steps to reproduce or evidence
   - Affected runtime/build/CI surface when applicable

## Response Commitment

- Acknowledgment within **48 hours** of report
- Assessment and remediation timeline communicated within **5 business days**
- Critical integrity or secret-exposure issues are treated as P1 and addressed through the applicable security/governance remediation path

## Scope

| In Scope | Out of Scope |
|----------|--------------|
| Governance schema and control-plane integrity | Theoretical framework disagreements |
| Exposed secrets or tokens in repository content or workflows | Feature requests |
| Repository-owned application/runtime vulnerabilities | Stylistic/formatting preferences |
| CI/CD and deployment-workflow vulnerabilities | Upstream-only CVEs with no demonstrated effect on this repository |
| Dependency vulnerabilities that are exploitable through this repository | Generic upstream vulnerability reports without a repository-specific impact path |
| Unauthorized or misleading DGAF certification/status presentation | Unsupported requests to weaken security or governance controls |

## Governance Context

Current governance and security authority are role-based:

- `role.governance-orchestrator` owns the applicable governance-orchestration and normative-disposition lane;
- `role.security-containment-gate` owns scoped security containment, sovereign/IP protection, protected-disclosure, and fail-closed blocking within its governing contract;
- `role.evidence-verification-reviewer` may verify retained remediation evidence where the applicable contract requires independent review.

Functional authority is defined in `governance/role_capability_registry.v1.json`. Persona names and historical agent repositories may be retained as provenance, but they do not independently grant current security or governance authority. Security remediation must remain bound to this repository's current source, CI evidence, and applicable private reporting path.
