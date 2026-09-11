# Security Policy

## Supported Versions

This repository contains governance specifications, evaluation rubrics, agent protocol documents, **and a Next.js application package** (see `package.json` for build/dev/start scripts). Security concerns relate to:

- Specification integrity (unauthorized modifications to governance schemas)
- Credential or secret exposure in committed files
- Misrepresentation of DGAF certification status

## Reporting a Vulnerability

To report a security concern with this repository or the broader DGAF ecosystem:

1. **Do not open a public GitHub issue** for security matters.
2. Contact the maintainer directly via GitHub: [@ndrorchestration](https://github.com/ndrorchestration)
3. Include:
   - Repository and file path affected
   - Nature of the concern (integrity, exposure, misrepresentation)
   - Steps to reproduce or evidence

## Response Commitment

- Acknowledgment within **48 hours** of report
- Assessment and remediation timeline communicated within **5 business days**
- Critical integrity issues (e.g., unauthorized schema modification, exposed credentials) treated as P1 — addressed in the next governance sweep session

## Scope

| In Scope | Out of Scope |
|----------|--------------|
| Governance schema integrity | Theoretical framework disagreements |
| Exposed secrets or tokens in committed files | Feature requests |
| Misuse of DGAF certification marks | Stylistic/formatting preferences |
| CI/CD workflow vulnerabilities | Third-party dependency CVEs (report upstream) |

## Governance Context

This repository is governed by the DGAF framework under Agent Amethyst (meta-orchestrator) and Agent Sentinel (integrity enforcement). Security reports may be escalated to the [sentinel-governance](https://github.com/ndrorchestration/sentinel-governance) CI/CD layer for automated remediation verification.
