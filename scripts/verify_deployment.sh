#!/usr/bin/env bash
# scripts/verify_deployment.sh
# Usage: DGAF_URL=https://your-project.vercel.app bash scripts/verify_deployment.sh
set -euo pipefail

URL="${DGAF_URL:-https://dgaf-framework.vercel.app}"
echo "[DGAF] Verifying deployment at: $URL"
echo "---"

# 1 — Health
echo "[1] GET /api/health"
HEALTH=$(curl -sf "$URL/api/health")
echo "$HEALTH" | python3 -m json.tool
PSI_OK=$(echo "$HEALTH" | python3 -c "import sys,json; d=json.load(sys.stdin); print(str(d.get('psi_cubic',False)).lower())")
[ "$PSI_OK" = "true" ] && echo "  ✓ psi_cubic" || { echo "  ✗ psi_cubic FAIL"; exit 1; }
VER=$(echo "$HEALTH" | python3 -c "import sys,json; print(json.load(sys.stdin).get('version',''))")
[ "$VER" = "1.7.0" ] && echo "  ✓ version=1.7.0" || echo "  ⚠  version=$VER (expected 1.7.0)"
echo ""

# 2 — Orchestrate
echo "[2] POST /api/orchestrate"
ORCH=$(curl -sf "$URL/api/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{ "payload": "Validate schema hash against SSoT.",
         "confidence": 0.80, "claim": "Schema hash validated.",
         "entropy_score": 0.25, "kappa_score_hint": 0.50 }')
echo "$ORCH" | python3 -m json.tool
for field in turn_id dgaf_decision phi_decision effective_confidence seal_hash; do
  VAL=$(echo "$ORCH" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('$field','MISSING'))")
  [ "$VAL" != "MISSING" ] && echo "  ✓ $field=$VAL" || echo "  ✗ $field MISSING"
done
echo ""

# 3 — Dashboard
echo "[3] GET / (dashboard)"
HTTP_CODE=$(curl -so /dev/null -w "%{http_code}" "$URL/")
[ "$HTTP_CODE" = "200" ] && echo "  ✓ dashboard HTTP 200" || echo "  ✗ dashboard HTTP $HTTP_CODE"
echo ""

# 4 — Audit
echo "[4] GET /api/audit"
curl -sf "$URL/api/audit" | python3 -m json.tool
echo ""

echo "[DGAF] Verification complete."
