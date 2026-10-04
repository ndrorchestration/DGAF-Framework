export function trustedTektiteAuditOrigin(rawOrigin: string | undefined): string {
  if (!rawOrigin) throw new Error('TEKTITE_DEMO_AUDIT_ORIGIN_UNAVAILABLE')

  let parsed: URL
  try {
    parsed = new URL(rawOrigin)
  } catch {
    throw new Error('TEKTITE_DEMO_AUDIT_ORIGIN_INVALID')
  }

  if (parsed.protocol !== 'https:') throw new Error('TEKTITE_DEMO_AUDIT_ORIGIN_HTTPS_REQUIRED')
  if (parsed.username || parsed.password) throw new Error('TEKTITE_DEMO_AUDIT_ORIGIN_CREDENTIALS_FORBIDDEN')
  if (parsed.pathname !== '/' || parsed.search || parsed.hash) {
    throw new Error('TEKTITE_DEMO_AUDIT_ORIGIN_MUST_BE_ORIGIN_ONLY')
  }

  return parsed.origin
}
