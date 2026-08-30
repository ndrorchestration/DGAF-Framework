# DGAF Documentation Style Guide

**Status:** ACTIVE  
**Applies to:** GitHub-visible documentation, project records, specifications, research notes, and governance artifacts  
**Principle:** Preserve rigor without making every document read like an audit log.

## 1. Write for the document's job

Every document should have one primary job and a clear audience.

| Surface | Primary job | Default style |
|---|---|---|
| `README.md` | Orient, explain value, and route the reader | concise, accessible, persuasive without hype |
| Project/current-state records | Establish authoritative status | precise, compact, evidence-oriented |
| Architecture/specifications | Explain design and contracts | technical, structured, normative where required |
| Experiment protocols | Define reproducible procedures | formal, explicit, unambiguous |
| Evidence/audit records | Preserve verification history | forensic, exact, minimally interpretive |
| Historical records | Preserve provenance | descriptive, clearly time-scoped |
| Contribution/community docs | Help people participate | practical, welcoming, actionable |

Do not make a public landing page carry the full burden of an evidence ledger. Link to the authoritative record instead.

## 2. Separate facts, interpretation, and policy

Use language that makes the type of statement obvious:

- **Fact:** what the repository, test, run, or source actually shows.
- **Interpretation:** what that evidence reasonably supports.
- **Policy:** what DGAF requires or prohibits.
- **Hypothesis:** what remains to be tested.
- **Historical record:** what was true or claimed at an earlier point.

Avoid turning a policy requirement into evidence that the implementation satisfies it.

## 3. Lead with value before caveat

For public-facing material, use this order where appropriate:

1. What it is.
2. Why it matters.
3. What is actually present.
4. How to inspect or use it.
5. What is currently established.
6. Important limitations and boundaries.
7. Deeper records.

Transparency is strongest when readers understand the project before encountering its qualifications.

## 4. Use bounded claims, not defensive prose

Prefer:

> "The control-plane test suite covers X and Y. The reported result applies to commit Z."

Over:

> "Do not infer repository-wide validation from a component-level test..."

The second formulation remains appropriate when preventing a likely misunderstanding, but repeated negative formulations should be consolidated into one authoritative boundary statement.

## 5. Control status vocabulary

Use the repository's epistemic vocabulary consistently:

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

Do not use broad terms such as `validated`, `proven`, `production-ready`, `certified`, or `safe` unless their precise scope is established and the supporting evidence is linked.

## 6. Status records must be temporally honest

Current documents should identify their status date and authoritative reference where practical. Active work should reference the current engineering lane. Closed or superseded PRs belong in historical records unless they remain directly relevant to a current blocker.

When a historical item is necessary, label it as historical in the same sentence or table row rather than relying on a distant disclaimer.

## 7. Avoid internal-process overload

A public document normally does not need:

- every predicate identifier;
- every intermediate SHA;
- every historical remediation branch;
- internal coordination details;
- repeated authorization disclaimers;
- private workspace references;
- agent deliberation or role-play;
- exhaustive closure sequences.

Retain these details in the appropriate governance or evidence record when they have operational or provenance value.

## 8. Prefer concrete nouns and active verbs

Prefer:

- "The workflow binds the candidate SHA to the executing SHA."
- "The protocol defines the primary endpoint."
- "The audit record preserves the exact run identity."

Avoid:

- "It is important to note that..."
- "It should be understood that..."
- "This must not be construed as..." repeated across sections.
- dense noun chains when a short verb phrase is available.

## 9. Make navigation task-oriented

Link labels should answer a reader's question: **What do I click next?**

Prefer `Current state`, `Architecture`, `Experiment protocol`, `Evidence index`, and `Contributing` over long descriptive filenames in high-level navigation.

Detailed records may use exact filenames when precision is useful.

## 10. Preserve technical density where it earns its place

Technical detail belongs in technical documents. Do not simplify away information required to reproduce a result, understand a contract, or audit provenance. Instead, separate layers so readers can choose their depth.

### Documentation depth hierarchy

`overview → architecture → contract → implementation → evidence → audit trail`

## 11. Public-facing social quality

GitHub readers include engineers, researchers, maintainers, potential contributors, employers, collaborators, funders, and technically curious visitors. Public writing should therefore be:

- readable without prior knowledge of the project's internal process;
- confident about what exists without exaggerating what it proves;
- respectful of the reader's time;
- explicit about uncertainty without sounding evasive;
- easy to scan on a phone and desktop;
- free of unnecessary personal or private information.

## 12. Review test

Before publishing a document, ask:

1. What is the reader here to learn or do?
2. Can they understand that purpose in the first few lines?
3. Is the most important information visible before implementation detail?
4. Which claims require evidence, and is that evidence discoverable?
5. Are historical and current states clearly separated?
6. Are we repeating a caveat that belongs in one canonical policy?
7. Does every link take the reader somewhere intentionally public and useful?
8. Would an informed outsider describe the document as clear, credible, and appropriately scoped?

## Relationship to governance

This guide governs presentation and information architecture. It does not alter technical contracts, evidence states, experimental authorization, or repository authority. The [Public Surface QA Standard](PUBLIC_SURFACE_QA_STANDARD.md) remains the publication control; this guide supplies the editorial layer beneath it.
