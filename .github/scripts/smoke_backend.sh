#!/usr/bin/env bash
# Fail on any error & show commands
set -euo pipefail

IMAGE="$1"          # registry/ortho_backend:tag
SECRET="$2"         # RECAPTCHA_SECRET

echo "▶️  Smoke-test $IMAGE"

docker run -d --name ortho_test \
  -e DJANGO_SETTINGS_MODULE=orthodontist_site.settings.docker \
  -e RECAPTCHA_SECRET="$SECRET" \
  -p 8000:8000 "$IMAGE"

# ждём max 30 сек, пока health-endpoint ответит 200
for _ in {1..15}; do
  if curl -sf http://localhost:8000/health/ >/dev/null; then
    echo "✅ backend is healthy"
    docker rm -f ortho_test
    exit 0
  fi
  sleep 2
done

echo "❌ health-check failed"
docker logs ortho_test || true
docker rm -f ortho_test
exit 1
