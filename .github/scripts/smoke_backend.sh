#!/usr/bin/env bash
set -euo pipefail

IMAGE="$1"          # registry/ortho_backend:tag
SECRET="$2"         # RECAPTCHA_SECRET

echo "▶️  Smoke-test $IMAGE"

docker run -d --name ortho_test \
  -e DJANGO_SETTINGS_MODULE=orthodontist_site.settings.docker \
  -e RECAPTCHA_SECRET="$SECRET" \
  -p 8000:8000 "$IMAGE"

for i in {1..15}; do
  if curl -sf http://localhost:8000/api/health/ >/dev/null; then
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
