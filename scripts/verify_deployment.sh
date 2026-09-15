#!/usr/bin/env bash
# scripts/verify_deployment.sh
# Usage:
#   DGAF_URL=https://your-project.vercel.app bash scripts/verify_deployment.sh
#   VERCEL_AUTOMATION_BYPASS_SECRET=... bash scripts/verify_deployment.sh
set -euo pipefail

URL="${DGAF_URL:-https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app}"
CURL_ARGS=(-sS -f)
if [[ -n "${VERCEL_AUTOMATION_BYPASS_SECRET:-}" ]]; then
  CURL_ARGS+=(-H "x-vercel-protection-bypass: ${VERCEL_AUTOMATION_BYPASS_SECRET}")
fi

echo "[DGAF] Verifying deployment at: $URL"
echo "---"

# 1 — Health
echo "[1] GET /api/health"
HEALTH=$(curl "${CURL_ARGS[@]}" "$URL/api/health")
echo "$HEALTH" | python3 -m json.tool
HEALTH_OK=$(echo "$HEALTH" | python3 -c "import sys,json; d=json.load(sys.stdin); ok=(d.get('status') == 'ok' and d.get('psi_cubic') is True and d.get('version') == '1.8.0'); print(str(ok).lower())")
[ "$HEALTH_OK" = "true" ] || { echo "  ✗ health response contract FAIL"; exit 1; }
echo '  ✓ status="ok", psi_cubic=true, version="1.8.0"'
echo ""

# 2 — Orchestrate
echo "[2] POST /api/orchestrate"
ORCH=$(curl "${CURL_ARGS[@]}" "$URL/api/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{ "payload": "Validate schema hash against SSoT.",
         "turn": 1,
         "confidence": 0.80, "claim": "Schema hash validated.",
         "entropy_score": 0.25, "kappa_score_hint": 0.50 }')
echo "$ORCH" | python3 -m json.tool
ORCH_OK=$(echo "$ORCH" | python3 -c "import sys,json,math; d=json.load(sys.stdin); c=d.get('effective_confidence'); ok=(d.get('decision') == 'PASS' and d.get('turn') == 1 and not isinstance(c,bool) and isinstance(c,(int,float)) and math.isfinite(c) and d.get('psi_cubic_check') is True and isinstance(d.get('trace'),list) and d.get('evidence',{}).get('status') == 'PARTIAL'); print(str(ok).lower())")
[ "$ORCH_OK" = "true" ] || { echo "  ✗ orchestrate response contract FAIL"; exit 1; }
echo '  ✓ decision="PASS", turn=1, finite effective_confidence, psi_cubic_check=true, trace=array, evidence.status="PARTIAL"'
echo ""

# 3 — Dashboard
echo "[3] GET / (dashboard)"
HTTP_CODE=$(curl "${CURL_ARGS[@]}" -o /dev/null -w "%{http_code}" "$URL/")
[ "$HTTP_CODE" = "200" ] || { echo "  ✗ dashboard HTTP contract FAIL: $HTTP_CODE"; exit 1; }
echo "  ✓ dashboard HTTP 200"
echo ""

# 4 — Audit
echo "[4] GET /api/audit"
AUDIT=$(curl "${CURL_ARGS[@]}" "$URL/api/audit")
echo "$AUDIT" | python3 -m json.tool
AUDIT_OK=$(echo "$AUDIT" | python3 -c "import sys,json; d=json.load(sys.stdin); expected_warning='Audit counters are in-memory and reset on each serverless cold start. Wire to Vercel KV for persistence.'; ok=(d.get('status') == 'ok' and d.get('version') == '1.8.0' and d.get('_warning') in (None, expected_warning)); print(str(ok).lower())")
[ "$AUDIT_OK" = "true" ] || { echo "  ✗ audit response contract FAIL"; exit 1; }
echo '  ✓ audit status="ok", version="1.8.0", warning contract valid'
echo ""

echo "[DGAF] Verification complete."
