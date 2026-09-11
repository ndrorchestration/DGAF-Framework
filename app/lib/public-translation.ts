const AGENT_LABELS: Record<string, string> = {
  amethyst: 'Governance Orchestrator (Amethyst)',
  colleen: 'Continuity & Provenance Coordinator (COLLEEN)',
  apogee: 'Evidence & Verification Reviewer (Apogee)',
  demijole: 'Runtime Safety & Constraint Adviser (DemiJoule)',
  demijoule: 'Runtime Safety & Constraint Adviser (DemiJoule)',
  reciprocity: 'Reciprocal-Impact & Fairness Reviewer (Reciprocity)',
  prodigy: 'Formal Methods & Mathematical Analyst (Professor Prodigy)',
  'professor prodigy': 'Formal Methods & Mathematical Analyst (Professor Prodigy)',
  herald: 'Publication & External Communication Gatekeeper (Herald)',
  sentinel: 'Security Lineage / Policy Boundary Role (Sentinel)',
  'sentinel-phi': 'Security & Policy Boundary Enforcer (Sentinel-Phi)',
  reson: 'Coherence & Drift Reviewer (Reson)',
  echolette: 'Pattern & Temporal-Coherence Reviewer (Echolette)',
  lyra: 'Synthesis & Narrative Adviser (Lyra)',
  nova: 'Simulation & Hypothesis Explorer (Nova)',
  perigee: 'Boundary & Input-Safety Filter (Perigee)',
  librarian: 'Provenance & Decision Archivist (The Librarian)',
  'the librarian': 'Provenance & Decision Archivist (The Librarian)',
  auditor: 'Quality & Constraint Reviewer (The Auditor)',
  'the auditor': 'Quality & Constraint Reviewer (The Auditor)',
  actualizer: 'Authorized Execution Worker (The Actualizer)',
  'the actualizer': 'Authorized Execution Worker (The Actualizer)',
  zenith: 'Compute & Resource Coordinator (Zenith)',
  ionia: 'Convergence & Modal-Lock Agent (Ionia)',
}

export function agentDisplayName(id: string): string {
  const key = id.trim().toLowerCase()
  return AGENT_LABELS[key] ?? id
}

export function agentFunctionalLabel(id: string): string {
  const display = agentDisplayName(id)
  const codenameStart = display.lastIndexOf(' (')
  return codenameStart > 0 ? display.slice(0, codenameStart) : display
}

export const ONTOLOGY_NOTE =
  'Runtime roster data is an operational snapshot, not an authority for sovereign identity adjudication. Canonical identity and alias disputes remain governed by the repository ontology records.'
