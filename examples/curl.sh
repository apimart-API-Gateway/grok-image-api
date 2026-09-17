#!/usr/bin/env bash
# Grok Image (grok-imagine-1.5-apimart): submit, poll, print the reported cost.
set -euo pipefail
: "${APIMART_API_KEY:?export APIMART_API_KEY first}"
BASE="${APIMART_BASE_URL:-https://api.apimart.ai/v1}"
PROMPT="${1:-A bamboo forest path under moonlight}"
SIZE="${2:-1:1}"
RESOLUTION="${3:-1K}"

read -r -d '' BODY <<JSON || true
{"model":"grok-imagine-1.5-apimart","prompt":"$PROMPT","size":"$SIZE","resolution":"$RESOLUTION","n":1}
JSON

TASK=$(curl -sS "$BASE/images/generations" \
  -H "Authorization: Bearer $APIMART_API_KEY" -H 'Content-Type: application/json' \
  -H "Idempotency-Key: $(uuidgen)" -d "$BODY" \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["data"]["id"])')
echo "task: $TASK"

for _ in $(seq 1 30); do
  RESPONSE=$(curl -sS "$BASE/tasks/$TASK" -H "Authorization: Bearer $APIMART_API_KEY")
  STATUS=$(printf '%s' "$RESPONSE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["data"]["status"])')
  echo "status: $STATUS"
  [ "$STATUS" = "completed" ] && break
  [ "$STATUS" = "failed" ] && { printf '%s\n' "$RESPONSE"; exit 1; }
  sleep 5
done
printf '%s' "$RESPONSE" | python3 -c 'import json,sys; d=json.load(sys.stdin)["data"]; print("cost:", d.get("cost"), "urls:", d.get("result",{}).get("images",[{}])[0].get("url"))'
