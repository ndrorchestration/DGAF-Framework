const CASES = ['SC-01', 'SC-05', 'SC-13', 'SC-16', 'SC-28']
const PREDICATES = ['capabilities_restricted', 'workers_covered', 'pending_actions_contained', 'egress_covered', 'persistence_contained']
const CLOCK = '2026-10-11T08:00:00Z'
const BOUNDARY = {
  live_containment: 'NOT_ESTABLISHED', source_authenticity: 'NOT_ESTABLISHED',
  live_cross_system_integration: 'NOT_RUN', independent_validation: 'NOT_ESTABLISHED',
  canonical_dgaf_efficacy: 'NOT_ESTABLISHED', high_assurance: 'NOT_AUTHORIZED',
  scientific_n_increment: 0, execution_permitted: false,
}

function require(condition, message) {
  if (!condition) throw new Error(message)
}

function record(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
}

function sameKeys(value, keys) {
  return record(value) && Object.keys(value).length === keys.length && keys.every((key) => Object.hasOwn(value, key))
}

function digest(value) {
  return typeof value === 'string' && /^sha256:[a-f0-9]{64}$/.test(value)
}

function strings(value, nonempty = false) {
  return Array.isArray(value) && (!nonempty || value.length > 0) &&
    value.every((item) => typeof item === 'string' && item.trim().length > 0)
}

function noAuthority(value) {
  require(value.authority_effect === 'NONE' && value.follow_on_authority === 'FRESH_ADJUDICATION_REQUIRED' &&
    value.execution_permitted === false && value.scientific_n_increment === 0, 'Authority boundary mismatch')
}

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize)
  if (record(value)) return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonicalize(value[key])]))
  return value
}

async function assessmentDigest(value) {
  const bytes = new TextEncoder().encode(JSON.stringify(canonicalize(value)))
  const result = await globalThis.crypto.subtle.digest('SHA-256', bytes)
  return 'sha256:' + Array.from(new Uint8Array(result), (byte) => byte.toString(16).padStart(2, '0')).join('')
}

export async function validateProjection(value) {
  require(sameKeys(value, ['schema_version', 'evidence_class', 'evaluation_mode', 'evaluation_time',
    'source_baseline_commit', 'implementation_digests', 'cases', 'claim_boundary']), 'Projection schema mismatch')
  require(value.schema_version === 'TEKTITE_SYNTHETIC_CONTAINMENT_V1' && value.evidence_class === 'SYNTHETIC' &&
    value.evaluation_mode === 'FIXED_TIME_SNAPSHOT_REPLAY' && value.evaluation_time === CLOCK &&
    value.source_baseline_commit === 'aabf1163515af291dc564bd7564fd12762a898c8', 'Synthetic replay identity mismatch')
  require(sameKeys(value.implementation_digests, ['dgaf_containment_assessment.py', 'dgaf_containment_observation.py', 'generate_tektite_containment.py']) &&
    Object.values(value.implementation_digests).every(digest), 'Implementation identities missing')
  require(sameKeys(value.claim_boundary, Object.keys(BOUNDARY)) &&
    Object.entries(BOUNDARY).every(([key, expected]) => value.claim_boundary[key] === expected), 'Claim boundary mismatch')
  require(Array.isArray(value.cases) && value.cases.length === CASES.length &&
    value.cases.every((item, index) => record(item) && item.case_id === CASES[index]), 'Case coverage mismatch')
  for (const item of value.cases.slice(0, 4)) {
    require(sameKeys(item, ['case_id', 'assessment', 'assessment_digest']) && digest(item.assessment_digest), 'Assessment linkage missing')
    const a = item.assessment
    require(sameKeys(a, ['schema_version', 'evidence_class', 'contract_digest', 'subject_id', 'session_id',
      'environment_id', 'observed_at', 'assessed_at', 'time_basis', 'disposition', 'reasons', 'predicate_results',
      'evidence_ids', 'blocking_defeaters', 'authority_effect', 'follow_on_authority', 'execution_permitted',
      'scientific_n_increment', 'observation_digest', 'integrity_binding', 'source_authenticity']), 'Assessment schema mismatch')
    noAuthority(a)
    require(a.schema_version === 'SYNTHETIC_CONTAINMENT_ASSESSMENT_V1' && a.evidence_class === 'SYNTHETIC' &&
      a.time_basis === 'SNAPSHOT' && a.assessed_at === CLOCK && a.source_authenticity === 'NOT_ESTABLISHED' &&
      a.integrity_binding === 'EXPECTED_DIGEST_MATCH' && digest(a.observation_digest) && digest(a.contract_digest), 'Evidence binding mismatch')
    require(a.subject_id === 'synthetic-agent' && a.session_id === 'synthetic-session' &&
      a.environment_id === 'synthetic-environment', 'Synthetic scope mismatch')
    require(sameKeys(a.predicate_results, PREDICATES) &&
      Object.values(a.predicate_results).every((state) => ['ESTABLISHED', 'UNKNOWN', 'CONTRADICTED'].includes(state)), 'Predicate coverage mismatch')
    require(strings(a.reasons) && strings(a.evidence_ids, true) && strings(a.blocking_defeaters), 'Evidence lists malformed')
    const expectedReasons = { 'SC-01': [], 'SC-05': ['UNKNOWN:workers_covered'], 'SC-13': ['STALE'], 'SC-16': ['CONTRACT_BINDING_MISMATCH'] }
    require(JSON.stringify(a.reasons) === JSON.stringify(expectedReasons[item.case_id]) && a.blocking_defeaters.length === 0, 'Case semantics mismatch')
    require(a.disposition === (item.case_id === 'SC-01' ? 'ESTABLISHED_IN_SCOPE' : 'NOT_ESTABLISHED'), 'Disposition mismatch')
    require(a.observed_at === (item.case_id === 'SC-13' ? '2026-10-11T07:59:00Z' : '2026-10-11T07:59:50Z'), 'Snapshot clock mismatch')
    require(PREDICATES.every((name) => a.predicate_results[name] ===
      (item.case_id === 'SC-05' && name === 'workers_covered' ? 'UNKNOWN' : 'ESTABLISHED')), 'Predicate semantics mismatch')
    require(await assessmentDigest(a) === item.assessment_digest, 'assessment digest mismatch')
  }
  const follow = value.cases[4]
  require(sameKeys(follow, ['case_id', 'observed', 'reason', 'dispatcher_calls', 'prior_assessment_digest',
    'authority_effect', 'follow_on_authority', 'execution_permitted', 'scientific_n_increment']), 'Refusal schema mismatch')
  noAuthority(follow)
  require(follow.observed === 'REFUSED' && follow.dispatcher_calls === 0 &&
    follow.reason === 'fresh adjudication is required after prior execution' &&
    follow.prior_assessment_digest === value.cases[0].assessment_digest, 'Refusal linkage mismatch')
  return value
}

function element(doc, tag, text, className) {
  const node = doc.createElement(tag)
  node.textContent = text
  if (className) node.className = className
  return node
}

const MEANINGS = {
  'SC-01': 'All declared predicates hold in the supplied bounded synthetic snapshot.',
  'SC-05': 'Worker coverage is unknown; the claim cannot be established.',
  'SC-13': 'The snapshot exceeds the declared 30-second synthetic age bound.',
  'SC-16': 'The observation belongs to a previous definition; it cannot establish the changed contract.',
  'SC-28': 'An established assessment carries no authority into the next protected effect.',
}

export async function mountProjection(doc) {
  const target = doc.getElementById('cases')
  if (!target) return
  try {
    const value = await validateProjection(JSON.parse(doc.getElementById('projection')?.textContent ?? 'null'))
    target.replaceChildren()
    for (const item of value.cases) {
      const article = element(doc, 'article', '')
      const a = item.assessment
      article.append(element(doc, 'span', item.case_id, 'eyebrow'),
        element(doc, 'h2', a?.disposition ?? item.observed), element(doc, 'p', MEANINGS[item.case_id]))
      article.append(element(doc, 'span', 'AUTHORITY NONE · FRESH ADJUDICATION REQUIRED', 'tag'))
      if (a) {
        article.append(element(doc, 'p', a.reasons.join(' · ') || 'No unmet predicates in this synthetic fixture.', 'reasons'))
        const list = doc.createElement('dl')
        for (const [label, text] of [['Scope', `${a.subject_id} / ${a.session_id} / ${a.environment_id}`],
          ['Definition digest', a.contract_digest], ['Observation pin', a.observation_digest],
          ['Source authenticity', a.source_authenticity], ['Evidence', a.evidence_ids.join(', ')]]) {
          list.append(element(doc, 'dt', label), element(doc, 'dd', text))
        }
        article.append(list)
      } else {
        article.append(element(doc, 'p', `${item.reason}. Dispatcher calls: ${item.dispatcher_calls}.`))
      }
      const details = doc.createElement('details')
      details.append(element(doc, 'summary', 'Show retained record'), element(doc, 'pre', JSON.stringify(item, null, 2)))
      article.append(details)
      target.append(article)
    }
  } catch {
    target.replaceChildren()
    target.append(element(doc, 'h2', 'Evidence unavailable'),
      element(doc, 'p', 'The retained record failed validation. No containment or execution authority is established.'))
  }
}
